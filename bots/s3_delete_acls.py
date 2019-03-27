'''
## s3_delete_acls
What it does: Deletes all ACLs from a bucket. If there is a bucket policy, it'll be left alone.
Usage: AUTO: s3_delete_acls  
Limitations: none  
'''

import boto3
from botocore.exceptions import ClientError

def run_action(boto_session,rule,entity,params):
    text_output = ""
    # Create an S3 client
    s3_client = boto_session.client('s3')
    bucket = entity['id']

    #### Remove Bucket ACLs #####
    try:
        #list bucket ACLs
        bucket_acls = s3_client.get_bucket_acl(Bucket=bucket)['Grants']
        
        if len(bucket_acls) == 1:
            text_output = text_output + "Only the CanonicalUser ACL found. Skipping."
            return text_output

        text_output = text_output + "ACLs that will be removed: " + str(bucket_acls[1:]) + ""

        # Unset the bucket ACLs
        result = s3_client.put_bucket_acl(Bucket=bucket,ACL='private')
    
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s " % str(result) 
        else:
            text_output = text_output + "Bucket ACL deleted: %s " % bucket
    
    except ClientError as e:
        text_output = text_output + "Unexpected error: %s " % e

    return text_output