'''
s3_enable_logging
What it does: Turns on server access logging
Usage: AUTO: s3_enable_logging <target_bucket_name>
Limitations: none
Requirements: 
    The target bucket needs to be in the same region as the remediation bucket or it'll throw a CrossLocationLoggingProhibitted error. 
    The target bucket must have write_object and read_bucket_permissions S3 logging ACLs or it'll throw a InvalidTargetBucketForLogging error.
'''

import boto3
from botocore.exceptions import ClientError

## Turn on S3 bucket logging 
def run_action(rule,entity,params):
    bucket_name = entity['id']

    #target_bucket needs to be passed through params
    if not params:
        text_output = "No target_bucket found. Can't remediate.\nUsage: AUTO: s3_enable_logging <target_bucket_name>\n"
        return text_output

    target_bucket_name = params[0]

    s3 = boto3.resource('s3')
    bucket_logging = s3.BucketLogging(bucket_name)

    try:
        result = bucket_logging.put(
            BucketLoggingStatus={
                'LoggingEnabled': {
                    'TargetBucket': target_bucket_name,
                    'TargetPrefix': ''
                }
            }
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Bucket logging enabled from bucket: %s to bucket: %s \n" % (bucket_name,target_bucket_name)

    
    except ClientError as e:
            text_output = "Unexpected error: %s \n" % e

    return text_output 
