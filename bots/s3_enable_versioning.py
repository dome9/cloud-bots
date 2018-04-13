'''
## s3_enable_versioning
What it does: Turns on versioning for an S3 bucket
Usage: AUTO: s3_enable_versioning
Limitations: none 
'''

import boto3

## Turn on S3 bucket versioning
def run_action(boto_session,rule,entity,params):
    bucket_name = entity['id']

    s3_resource = boto_session.resource('s3')
    bucket_versioning = s3_resource.BucketVersioning(bucket_name)
    
    result = bucket_versioning.enable()

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Bucket versioning enabled: %s \n" % bucket_name

    return text_output 
