"""
## sqs_configure_dlq
What it does: Configures a Dead-Letter Queue (DLQ) for a source queue.
Usage: AUTO sqs_configure_dlq
Notes: A dead-Letter Queue is also a queue. The bot doesn't create a DLQ if the queue is a DLQ itself.
Limitations: None
"""
import json

from botocore.exceptions import ClientError

permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'


def create_queue(sqs_resource, queue_name, is_fifo):
    dlq_name = f'dlq-for-{queue_name}'
    attributes = {'FifoQueue': 'true'} if is_fifo else {}
    try:
        print(f'{__file__} - Creating a Dead-Letter Queue for source queue: {queue_name}... \n')
        dlq = sqs_resource.create_queue(QueueName=dlq_name, Attributes=attributes)
        print(f'{__file__} - Done. Successfully created a queue named {dlq_name}. \n')
        dlq_arn = dlq.attributes['QueueArn']
        return 1, dlq_arn

    except ClientError as e:
        msg = f"Unexpected client error while creating DLQ: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            msg += f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
        return 0, msg


def run_action(boto_session, rule, entity, params):
    queue_name = entity['name']
    url = entity['queueUrl']
    region = entity['region'].replace("_", "-")
    sqs_resource = boto_session.resource('sqs', region_name=region)
    queue = sqs_resource.Queue(url)
    target_dlq = entity['redrivePolicy']['deadLetterTargetArn'] if entity['redrivePolicy'] != None else False
    text_output = ''
    try:
        print(f'{__file__} - Checking if the queue is a Dead-Letter Queue... \n')
        source_queues = list(queue.dead_letter_source_queues.all())
        if len(source_queues) > 0:
            if entity['id'] == target_dlq: # if the queue a DLQ of itself, need to change it to a different queue
                print(f'{__file__} - The Dead-Letter Queue of the queue is itself. Changing it... \n')
                text_output += 'The Dead-Letter queue of the queue was itself. \n'
            else:
                print(f'{__file__} - A Dead Letter Queue, skipping. \n')
                return f"Queue named {queue_name} is a Dead-Letter Queue of another queue. Won't create a DLQ for it. If youre using CSPM you may want to exclude this finding. Skipping. \n"
        print(f'{__file__} - Not a Dead-Letter Queue. \n')
    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
        return text_output

    is_fifo = False
    if queue_name.endswith(".fifo"):
        is_fifo = True
    success, msg = create_queue(sqs_resource, queue_name, is_fifo)
    if success:
        dlq_arn = msg
    else:
        return msg

    try:
        print(f'{__file__} - Setting as a Dead-Letter Queue... \n')
        redrive_policy = json.dumps({"deadLetterTargetArn": dlq_arn, "maxReceiveCount": 50})
        queue.set_attributes(
            Attributes={
                'RedrivePolicy': redrive_policy
            }
        )
        print(f'{__file__} - Done.\n')
        text_output = text_output + f'Successfully configured a Dead-Letter Queue for {queue_name}. Target DLQ arn: {dlq_arn}. \n'

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output
