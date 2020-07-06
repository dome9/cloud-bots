"""
## cloudtrail_encrypt_log_files_with_kms
What it does: create Customer keys with policy and then use the key to encrypt log file in the cloudTrial
Pre-set Settings:
Note: This bot create a new Customer keys
Limitations:None
"""

import json
from botocore.exceptions import ClientError

KMS_POLICY = {
    "Version": "2012-10-17",
    "Statement": [

    ]
}
IAM_STAT = {
    "Sid": "Enable IAM User Permissions",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::account_id:user/user_name"
    },
    "Action": "kms:*",
    "Resource": "*"
}
ENCRYPT_STAT = {
    "Sid": "Allow CloudTrail to encrypt logs",
    "Effect": "Allow",
    "Principal": {
        "Service": "cloudtrail.amazonaws.com"
    },
    "Action": "kms:GenerateDataKey*",
    "Resource": "*",
    "Condition": {
        "StringLike": {
            "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:account_id:trail/*"
        }
    }
}
DESCRIBE_STAT = {
    "Sid": "Allow CloudTrail to describe key",
    "Effect": "Allow",
    "Principal": {
        "Service": "cloudtrail.amazonaws.com"
    },
    "Action": "kms:DescribeKey",
    "Resource": "*"
}
DECRYPT_STAT = {
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
            "kms:CallerAccount": "account_id"
        },
        "StringLike": {
            "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:account_id:trail/*"
        }
    }
}


def run_action(boto_session, rule, entity, params):
    # create a cloudTrail session
    cloudtrail_client = boto_session.client('cloudtrail')
    # create a iam session
    iam_client = boto_session.client('iam')
    # create a kms session
    kms_client = boto_session.client('kms')

    cloudTrail_name = entity['name']
    account_id = entity['accountNumber']

    try:

        key_id = create_customer_key(kms_client, iam_client, account_id)

        cloudtrail_client.update_trail(
            Name=cloudTrail_name,
            KmsKeyId=key_id,
            EnableLogFileValidation=True,
        )

        text_output = "CloudTrial %s encrypt log file with kms %s." % (cloudTrail_name, key_id)

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output


# The function get the policy and create a customer key
def create_customer_key(kms_client, iam_client, account_id):
    try:

        kms_policy = create_kms_policy(iam_client, account_id)

        result = kms_client.create_key(
            Policy=kms_policy
        )

        key_id = result['KeyMetadata']['KeyId']
        text_output = key_id

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output


# Create a kms policy with Allow CloudTrail to encrypt logs
def create_kms_policy(iam_client, account_id):
    try:

        result = iam_client.get_user()
        user_name = result['User']['UserName']

        IAM_STAT["Principal"]["AWS"] = IAM_STAT.get("Principal").get("AWS").replace("user_name", user_name)
        IAM_STAT["Principal"]["AWS"] = IAM_STAT.get("Principal").get("AWS").replace("account_id", account_id)
        ENCRYPT_STAT["Condition"]["StringLike"]["kms:EncryptionContext:aws:cloudtrail:arn"] = ENCRYPT_STAT.get(
            "Condition").get(
            "StringLike").get(
            "kms:EncryptionContext:aws:cloudtrail:arn").replace("account_id", account_id)
        DECRYPT_STAT["Condition"]["StringLike"]["kms:EncryptionContext:aws:cloudtrail:arn"] = DECRYPT_STAT.get("Condition").get(
            "StringLike").get(
            "kms:EncryptionContext:aws:cloudtrail:arn").replace("account_id", account_id)
        DECRYPT_STAT["Condition"]["StringEquals"]['kms:CallerAccount'] = account_id

        KMS_POLICY['Statement'].append(IAM_STAT)
        KMS_POLICY['Statement'].append(ENCRYPT_STAT)
        KMS_POLICY['Statement'].append(DESCRIBE_STAT)
        KMS_POLICY['Statement'].append(DECRYPT_STAT)

        text_output = json.dumps(KMS_POLICY)

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output
