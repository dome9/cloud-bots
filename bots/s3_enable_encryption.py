'''
## s3_enable_encryption
What it does: Turns on AES-256 encryption on the target bucket  
Usage: AUTO: s3_enable_encryption  
Limitations: none  
'''

import boto3
from botocore.exceptions import ClientError

## Turn on S3 AES-256 encryption
def run_action(boto_session,rule,entity,params):
    bucket_name = entity['id']
    s3_client = boto_session.client('s3')

    try:
        result = s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    },
                ]
            }
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Bucket encryption enabled: %s \n" % bucket_name

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output 
