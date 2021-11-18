"""
## secretsmanager_enable_encryption
What it does: Enables data-at-rest encryption using KMS CMK (Customer Master Key).
Usage: AUTO secretsmanager_enable_encryption <kms-key-id>
EXAMPLE: secretsmanager_enable_encryption aaaaaaaa-bbbb-cccc-dddd-eeeeeeee
Notes:
# secretsmanagers can be encrypted by a symmetric key only.
# As a security best practice, we recommend to encrypt it with CMK. The bot will throw an error for aws-managed keys.
# The provided key must be in the same region as the secret.
Required permissions: "secretsmanager:UpdateSecret", "kms:GenerateDataKey", "kms:Decrypt".
"""

import bots_utils as utils


def run_action(boto_session, rule, entity, params):
    if len(params) != 1:
        raise ValueError("Error: Wrong use of secretsmanager_enable_encryption. Usage: AUTO secretsmanager_enable_encryption <kms-key-id>. \n")

    key_id = params[0]
    if utils.check_kms_type(boto_session, key_id) == 'AWS':
        raise ValueError("Error: The provided key is AWS-managed key. Please use a Customer-managed key (i.e CMK). \n")

    client = boto_session.client('secretsmanager')
    secret_arn = entity['arn']
    print(f'{__file__} - Trying to enable encryption... \n')
    result = client.update_secret(
        SecretId=secret_arn,
        KmsKeyId=key_id
    )
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        raise ValueError("Unexpected error: %s \n" % str(result))
    else:
        print(f'{__file__} - Done. \n')
        text_output = f'Successfully enabled encryption for secret: {secret_arn}. CMK is: {key_id}.'

    return text_output
