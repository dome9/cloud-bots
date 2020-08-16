"""
## cloudtrail_encrypt_log_files_using_new_key_creation
What it does: Create new customer key with the correct policy for encrypt log file in the cloudTrial.
Usage: AUTO: cloudtrail_encrypt_log_files_using_new_key_creation
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
        },
        {
            "Sid": "Allow CloudTrail to encrypt logs",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "kms:GenerateDataKey*",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:_ACCOUNT_NUMBER_:trail/*"
                }
            }
        },
        {
            "Sid": "Allow CloudTrail to describe key",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "kms:DescribeKey",
            "Resource": "*"
        },
        {
            "Sid": "Allow principals in the account to decrypt log files",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "kms:Decrypt",
                "kms:ReEncryptFrom"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "kms:CallerAccount": "_ACCOUNT_NUMBER_"
                },
                "StringLike": {
                    "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:_ACCOUNT_NUMBER_:trail/*"
                }
            }
        }
    ]
}


def run_action(boto_session, rule, entity, params):
    text_output = ''

    # create a cloudTrail session
    cloudtrail_client = boto_session.client('cloudtrail')
    # create a iam session
    iam_client = boto_session.client('iam')
    # create a kms session
    kms_client = boto_session.client('kms')

    cloudTrail_name = entity['id']
    account_id = entity['accountNumber']

    try:
        key_id = create_customer_key(kms_client, iam_client, account_id, cloudTrail_name)

        # Enable the encryption in the cloudtrail
        cloudtrail_client.update_trail(
            Name=cloudTrail_name,
            KmsKeyId=key_id,
            EnableLogFileValidation=True,
        )

        text_output = text_output + "CloudTrial: %s encrypt log file with key: %s." % (
            cloudTrail_name.split('/')[-1], key_id)

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output


# The function create a customer key by creating the correct policy.
# The function also enable key rotation and add an alias to the key
def create_customer_key(kms_client, iam_client, account_id, cloudTrail_name):
    text_output = ''
    try:

        kms_policy = create_kms_policy(iam_client, account_id)

        result = kms_client.create_key(
            Policy=kms_policy,
            Description=f"Key for CloudTrail: {cloudTrail_name}"
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


# Create a kms policy with Allow CloudTrail to encrypt decrypt and describe logs files
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
