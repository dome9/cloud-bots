'''
## s3_delete_bucket
What it does: Deletes an S3 bucket  
Usage: AUTO: s3_delete_bucket  
Limitations: none  
'''

import boto3

### DeleteS3Bucket ###
def run_action(boto_session,rule,entity,params):
    bucket = entity['Id']
    
    s3_client = boto_session.client('s3')
    result = s3_client.delete_bucket(Bucket=bucket)

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Bucket deleted. Id: %s \n" % (bucket)

    return text_output