"""
## sqs_enforce_sse
What it does: Configures server-side encryption (SSE) for a queue
Usage: sqs_enforce_sse <kmsKeyId> <kmsRegion>
Notes:
# For encryption with SQS-owned encryption keys, use the bot without any parameters (i.e: sqs_enforce_sse)
# For encryption using kms, provide <kmsKeyId>. <kmsRegion> is not required - provide it if the kms key is in a different region than the SQS.
Examples:
# sqs_enforce_sse (for encryption using SQS-owned encryption keys)
# sqs_enforce_sse kms aaaaaaaa-bbbb-cccc-dddd-eeeeeeee
# sqs_enforce_sse kms aaaaaaaa-bbbb-cccc-dddd-eeeeeeee us-east-2
# sqs_enforce_sse kms mrk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (for multi-region key)
# sqs_enforce_sse kms mrk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (for multi-region key, if it's in a different region)
Limitations: The KMS key MUST be in the same AWS account as the SQS.
"""


def get_kms_key(boto_session, key_id, region):
    kms_client = boto_session.client("kms", region_name=region)
    kms_key = kms_client.describe_key(KeyId=key_id)
    return kms_key['KeyMetadata']['Arn']


def run_action(boto_session, rule, entity, params):
    if not 0 <= len(params) <= 2:
        raise ValueError(f"Error: Wrong use of the sqs_enforce_sse bot. Usage: sqs_enforce_sse or sqs_enforce_sse <kmsKeyId> or sqs_enforce_sse <kmsKeyId> <kmsRegion> if the key is in a different region than the SQS. \n")

    sqs_client = boto_session.client('sqs')
    queue_url = entity['queueUrl']
    text_output = ''

    print(f'{__file__} - Trying to encrypt queue... \n')
    if len(params) > 0:
        print(f'{__file__} - Encryption type: KMS. \n')
        key_id = params[0]
        print(f'{__file__} - Key id = {key_id}. \n')
        if len(params) == 2:
            region = params[1]
        else:
            region = None
        kms_key_arn = get_kms_key(boto_session, key_id, region)
        result = sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={
                'KmsMasterKeyId': kms_key_arn
            }
        )
    else:
        print(f'{__file__} - Encryption type: SQS-Managed keys. \n')
        result = sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={
                'SqsManagedSseEnabled': 'true'
            }
        )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        raise ValueError("Unexpected error: %s \n" % str(result))
    else:
        print(f'{__file__} - Done. \n')
        text_output = text_output + f'Queue {queue_url} has successfully encrypted. \n'

    return text_output
