'''
## sns_delete_topic
What it does: Deletes sns topic and all its subscriptions.
Usage: AUTO: sns_delete_topic
Limitations: None
'''

import boto3
from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    region = entity['region'].replace('_', '-')
    sns_client = boto3.client('sns', region_name=region)
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

        text_output = "Unexpected error: %s \n" % e

    return text_output
