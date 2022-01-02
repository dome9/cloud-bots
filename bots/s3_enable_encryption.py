'''
## s3_enable_encryption
What it does: Turns on encryption on the target bucket.
Usage: AUTO: s3_enable_encryption <encryption_type> <kms-key-arn> (<kms-key-arn> should be provided only if <encryption_type> is KMS)
Note: <encryption_type> can be one of the following:
1. s3 (for s3-managed keys)
2. kms (for customer managed keys - RECOMMENDED) - for kms you MUST provide the <kms-key-arn>.
EXAMPLES:
s3_enable_encryption s3
s3_enable_encryption kms arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab

As a security best practice, we recommend encrypting with kms. Please refer our rule: https://gsl.dome9.com/D9.AWS.CRY.03.html
'''


def run_action(boto_session, rule, entity, params):
    if not 1 <= len(params) <= 2:
        raise ValueError(
            f"Error: Wrong use of s3_enable_encryption. Usage: s3_enable_encryption <encryption_type> <kms-key-arn> (<kms-key-arn> should be provided only if <encryption_type> is KMS) \n")
    encryption_type = params[0].lower()
    if len(params) == 1 and encryption_type == 'kms':
        raise ValueError(
            f"Error: Wrong use of s3_enable_encryption. If <encryption_type> is KMS, you must provide the key's arn. \n")

    if encryption_type == 'kms':
        kms_arn = params[1]
        encryption_config = {'SSEAlgorithm': 'aws:kms', 'KMSMasterKeyID': kms_arn}
    elif encryption_type == 's3':
        encryption_config = {'SSEAlgorithm': 'AES256'}

    bucket_name = entity['id']
    s3_client = boto_session.client('s3')

    print(f'{__file__} - Trying to enable encryption... \n')
    result = s3_client.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': encryption_config
                },
            ]
        }
    )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        raise ValueError("Unexpected error: %s \n" % str(result))
    else:
        print(f'{__file__} - Done. \n')
        text_output = f"Bucket encryption has successfully enabled. Bukcet name: {bucket_name}, encryption type: {encryption_type}. \n"
        if encryption_type == 'kms':
            text_output += f"Bucket encrypted with aws key arn: {params[1]} \n"

    return text_output
