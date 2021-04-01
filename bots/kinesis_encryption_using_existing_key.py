"""
## kinesis_encryption_using_existing_key
What it does: Enable Server Side Encryption (SSE) of your AWS Kinesis Server data at rest.
Usage: AUTO: kinesis_encryption_using_existing_key <key_id>
Note:  - The key the user pass can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully
         specified ARN to a key,or a globally unique identifier
        Examples:
                * alias/MyAliasName
                * arn:aws:kms:us-east-2:123456789012:alias/MyAliasName
                * arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
                * 12345678-1234-1234-1234-123456789012
Limitations:None
"""


from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):

    text_output = ""
    stream_name = entity['name']
    kinesis_client = boto_session.client('kinesis')
    key_id = params[0]

    try:

        kinesis_client.start_stream_encryption(
            StreamName=stream_name,
            EncryptionType='KMS',
            KeyId=key_id
        )

        text_output = text_output + 'Kinesis: %s encryption enabled with key: %s:' % (stream_name, key_id)

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output
