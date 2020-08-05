"""
## cloudtrail_encrypt_log_files_with_kms
What it does: create Customer keys with the correct policy for encrypt logs file,
              and then use the key to encrypt log file in the cloudTrial
Note: This bot create a new Customer keys
Limitations:None
"""

import json
from botocore.exceptions import ClientError

KMS_POLICY = {
    "Version": "2012-10-17",
    "Statement": []
}
IAM_STATEMENT = {
    "Sid": "Enable IAM User Permissions",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::account_id:user/user_name"
    },
    "Action": "kms:*",
    "Resource": "*"
}
ENCRYPT_STATEMENT = {
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
DESCRIBE_STATEMENT = {
    "Sid": "Allow CloudTrail to describe key",
    "Effect": "Allow",
    "Principal": {
        "Service": "cloudtrail.amazonaws.com"
    },
    "Action": "kms:DescribeKey",
    "Resource": "*"
}
DECRYPT_STATEMENT = {
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
        if not params:
            key_id = create_customer_key(kms_client, iam_client, account_id)
        else:
            key_id = params[0]

        # Enable the encryption in the cloudtrail
        cloudtrail_client.update_trail(
            Name=cloudTrail_name,
            KmsKeyId=key_id,
            EnableLogFileValidation=True,
        )

        text_output = text_output + "CloudTrial: %s encrypt log file with key: %s." % (cloudTrail_name.split('/')[-1], key_id)

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output


# The function create a customer key by creating the correct policy.
# The function also enable key rotation and add an alias to the key
def create_customer_key(kms_client, iam_client, account_id):
    text_output = ''
    try:

        kms_policy = create_kms_policy(iam_client, account_id)

        result = kms_client.create_key(
            Policy=kms_policy
        )

        key_id = result['KeyMetadata']['KeyId']

        # Rotate the key
        kms_client.enable_key_rotation(
            KeyId=key_id
        )
        # Create an alias for the key
        kms_client.create_alias(
            AliasName='alias/CloudTrail_CK',
            TargetKeyId=key_id
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

        # Add user name and account id to statements
        IAM_STATEMENT["Principal"]["AWS"] = IAM_STATEMENT.get("Principal").get("AWS").replace("user_name", user_name)
        IAM_STATEMENT["Principal"]["AWS"] = IAM_STATEMENT.get("Principal").get("AWS").replace("account_id", account_id)

        ENCRYPT_STATEMENT["Condition"]["StringLike"][
            "kms:EncryptionContext:aws:cloudtrail:arn"] = ENCRYPT_STATEMENT.get("Condition").get("StringLike").get(
            "kms:EncryptionContext:aws:cloudtrail:arn").replace("account_id", account_id)

        DECRYPT_STATEMENT["Condition"]["StringLike"][
            "kms:EncryptionContext:aws:cloudtrail:arn"] = DECRYPT_STATEMENT.get("Condition").get("StringLike").get(
            "kms:EncryptionContext:aws:cloudtrail:arn").replace("account_id", account_id)
        DECRYPT_STATEMENT["Condition"]["StringEquals"]['kms:CallerAccount'] = account_id

        # Add the statements to the policy
        KMS_POLICY['Statement'].append(IAM_STATEMENT)
        KMS_POLICY['Statement'].append(ENCRYPT_STATEMENT)
        KMS_POLICY['Statement'].append(DESCRIBE_STATEMENT)
        KMS_POLICY['Statement'].append(DECRYPT_STATEMENT)

        text_output = text_output + json.dumps(KMS_POLICY)

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output
