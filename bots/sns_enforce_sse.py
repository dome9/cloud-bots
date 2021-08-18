"""
## sns_enforce_sse
What it does: make sns topic use server side encryption (sse)
Usage:  sns_enforce_sse kmsKeyId=aaaaaaaa-bbbb-cccc-dddd-eeeeeeee
Limitations: none
"""

import boto3
from botocore.exceptions import ClientError


def get_kms_key(session, key_id):
    client = session.client("kms")
    kms_key = client.describe_key(KeyId=key_id,)
    return kms_key['KeyMetadata']['Arn']


def run_action(session, rule, entity, params):
    sns_client = session.client('sns')

    topic_arn = entity['topicArn']
    kms_key_arn = get_kms_key(session, params.get('kmsKeyId'))

    text_output = ''
    try:
        response = sns_client.set_topic_attributes(
            TopicArn=topic_arn,
            AttributeName='KmsMasterKeyId',
            AttributeValue=kms_key_arn
        )
        text_output = f'Topic {topic_arn} is now encrypted using kms key {kms_key_arn}'

    except ClientError as e:
        text_output = f"Unexpected error: {e}"

    return text_output
