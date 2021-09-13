'''
## sns_topic_delete
What it does: Deletes sns topic and all its subscriptions.
Usage: AUTO: sns_topic_delete
Limitations: None
'''

from botocore.exceptions import ClientError
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'

def run_action(boto_session, rule, entity, params):
    region = entity['region'].replace('_', '-')
    sns_client = boto_session.client('sns', region_name=region)
    topicArn = entity['topicArn']

    try:
        result = sns_client.delete_topic(
            TopicArn=topicArn,
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "SNS topic with arn: %s has successfully deleted." % topicArn

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output
