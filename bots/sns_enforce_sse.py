"""
## sns_enforce_sse
What it does: make sns topic use server side encryption (sse)
Usage:  sns_enforce_sse <kmsKeyId> <kmsRegion> (<kmsRegion> is not required - provide it if the kms key is in a different region than the SNS).
Examples:
# sns_enforce_sse aaaaaaaa-bbbb-cccc-dddd-eeeeeeee
# sns_enforce_sse aaaaaaaa-bbbb-cccc-dddd-eeeeeeee us-east-2
Limitations: none
"""


def get_kms_key(boto_session, key_id, region):
    kms_client = boto_session.client("kms", region_name=region)
    kms_key = kms_client.describe_key(KeyId=key_id)
    return kms_key['KeyMetadata']['Arn']


def run_action(session, rule, entity, params):
    if not 1 <= len(params) <= 2:
        return f"Error: Wrong use of the sns_enforce_sse bot. Usage: sns_enforce_sse <kmsKeyId> or sns_enforce_sse <kmsKeyId> <kmsRegion> if the key is in a different region than the SNS. \n"

    key_id = params[0]
    if len(params) == 2:
        region = params[1]
    else:
        region = None

    sns_client = session.client('sns')
    topic_arn = entity['topicArn']
    kms_key_arn = get_kms_key(session, key_id, region)
    text_output = ''

    result = sns_client.set_topic_attributes(
        TopicArn=topic_arn,
        AttributeName='KmsMasterKeyId',
        AttributeValue=kms_key_arn
    )
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = text_output + "Unexpected error: %s \n" % str(result)
    else:
        text_output = text_output + f'Topic {topic_arn} is now encrypted using kms key {kms_key_arn} \n'

    text_output = f'Topic {topic_arn} is now encrypted using kms key {kms_key_arn}'
    return text_output
