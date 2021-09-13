"""
## sqs_enforce_sse
What it does: Configures server-side encryption (SSE) for a queue
Usage:  sqs_enforce_sse <kmsKeyId> <kmsRegion> (<kmsRegion> is not required - provide it if the kms key is in a different region than the SQS).
Examples:
# sqs_enforce_sse aaaaaaaa-bbbb-cccc-dddd-eeeeeeee
# sqs_enforce_sse aaaaaaaa-bbbb-cccc-dddd-eeeeeeee us-east-2
# sqs_enforce_sse mrk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (for multi-region key)
# sqs_enforce_sse mrk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (for multi-region key, if it's in a different region)
Limitations: The KMS key MUST be in the same AWS account as the SQS.
"""

from botocore.exceptions import ClientError

permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'


def get_kms_key(boto_session, key_id, region):
    kms_client = boto_session.client("kms", region_name=region)
    kms_key = kms_client.describe_key(KeyId=key_id)
    return kms_key['KeyMetadata']['Arn']


def run_action(boto_session, rule, entity, params):
    if not 1 <= len(params) <= 2:
        return f"Error: Wrong use of the sqs_enforce_sse bot. Usage: sqs_enforce_sse <kmsKeyId> or sqs_enforce_sse <kmsKeyId> <kmsRegion> if the key is in a different region than the SQS. \n"

    key_id = params[0]
    if len(params) == 2:
        region = params[1]
    else:
        region = None

    sqs_client = boto_session.client('sqs')
    queue_url = entity['queueUrl']
    text_output = ''

    try:
        kms_key_arn = get_kms_key(boto_session, key_id, region)
        result = sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={
                'KmsMasterKeyId': kms_key_arn
            }
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + f'Queue {queue_url} has successfully encrypted with KMS key: {kms_key_arn} \n'

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output
