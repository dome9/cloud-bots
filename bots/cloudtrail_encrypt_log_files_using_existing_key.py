"""
## cloudtrail_encrypt_log_files_using_existing_key
What it does: Encrypt log file in the cloudTrial with a customer key that user pass as parameter.
Usage: AUTO: cloudtrail_encrypt_log_files_using_existing_key <key_id>
Note: - The key must have the correct policy for enable CloudTrail to encrypt, users to decrypt log files and user
            to describe key.
            For more information https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-kms-key-policy-for-cloudtrail.html
      - The key the user pass can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key,
        or a globally unique identifier
            Examples:
                * alias/MyAliasName
                * arn:aws:kms:us-east-2:123456789012:alias/MyAliasName
                * arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
                * 12345678-1234-1234-1234-123456789012
Limitations:None
"""

from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    text_output = ''

    # create a cloudTrail session
    cloudtrail_client = boto_session.client('cloudtrail')

    cloudTrail_name = entity['id']
    key_id = params[0]

    try:

        # Enable the encryption in the cloudtrail
        cloudtrail_client.update_trail(
            Name=cloudTrail_name,
            KmsKeyId=key_id,
        )

        text_output = text_output + "CloudTrial: %s encrypt log file with key: %s." % (
            cloudTrail_name.split('/')[-1], key_id)

    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output
