"""
## kinesis_encryption_using_new_key_creation
What it does: Enable Server Side Encryption (SSE) of your AWS Kinesis Server data at rest.
Usage: AUTO: kinesis_encryption_using_new_key_creation
Note: - The bot create a new customer key
Limitations:None
"""
import json
from botocore.exceptions import ClientError

KMS_POLICY = {
    "Version": "2012-10-17",
    "Id": "Key policy created by Auto Remediation",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::_ACCOUNT_NUMBER_:user/_USER_NAME_"
            },
            "Action": "kms:*",
            "Resource": "*"
        }
    ]
}


def run_action(boto_session, rule, entity, params):
    text_output = ""

    kinesis_client = boto_session.client('kinesis')
    # create a iam session
    iam_client = boto_session.client('iam')
    # create a kms session
    kms_client = boto_session.client('kms')

    account_id = entity['accountNumber']
    stream_name = entity['name']

    try:
        key_id = create_customer_key(kms_client, iam_client, account_id, stream_name)

        kinesis_client.start_stream_encryption(
            StreamName=stream_name,
            EncryptionType='KMS',
            KeyId=key_id
        )

        text_output = text_output + 'Kinesis: %s encryption enabled with key: %s:' % (stream_name, key_id)

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output


# The function create a customer key by creating the correct policy.
# The function also enable key rotation and add an description to the key
def create_customer_key(kms_client, iam_client, account_id, stream_name):
    text_output = ''
    try:

        kms_policy = create_kms_policy(iam_client, account_id)

        result = kms_client.create_key(
            Policy=kms_policy,
            Description=f"Key for Kinesis: {stream_name}"
        )

        key_id = result['KeyMetadata']['KeyId']

        # Rotate the key
        kms_client.enable_key_rotation(
            KeyId=key_id
        )

        text_output = text_output + key_id

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output


# Create a kms policy for the key
def create_kms_policy(iam_client, account_id):
    text_output = ''
    try:

        result = iam_client.get_user()  # To get the iam user for the policy
        user_name = result['User']['UserName']

        kms_policy = json.dumps(KMS_POLICY)

        kms_policy = kms_policy.replace("_ACCOUNT_NUMBER_", account_id)
        kms_policy = kms_policy.replace("_USER_NAME_", user_name)

        text_output = text_output + kms_policy

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output
