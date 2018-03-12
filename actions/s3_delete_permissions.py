'''
## s3_delete_permissions
What it does: Deletes all ACLs and bucket policies from a bucket  
Usage: AUTO: s3_delete_permissions  
Limitations: none  
'''

import boto3
from botocore.exceptions import ClientError

### DeleteS3BucketPermissions ###
def run_action(rule,entity,params):
    # Create an S3 client
    s3 = boto3.client('s3')
    bucket = entity['Id']

    ##### Remove Bucket policy #####
    try:
        #sendEvent out the S3 permissions first so we can reference them later
        bucket_policy = s3.get_bucket_policy(Bucket=bucket)['Policy']
        text_output = "Bucket policy that will be deleted: \n " + str(bucket_policy) + "\n"
                
        #Call S3 to delete the bucket policy for the given bucket
        result = s3.delete_bucket_policy(Bucket=bucket)
        
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "Bucket policy deleted: %s \n" % bucket

    except ClientError as e:
        print(e)
        error = e.response['Error']['Code']
        if error == 'NoSuchBucketPolicy':
            text_output = "Bucket %s does not have a bucket policy. Checking ACLs next.\n" % bucket
        else:
            text_output = "Unexpected error: %s \n" % e

    #### Remove Bucket ACLs #####
    try:
        #list bucket ACLs
        bucket_acls = s3.get_bucket_acl(Bucket=bucket)['Grants']
        
        if len(bucket_acls) == 1:
            text_output = text_output + "Only the CanonicalUser ACL found. Skipping.\n"
            return text_output

        text_output = text_output + "ACLs that will be removed: \n " + str(bucket_acls[1:]) + "\n"

        # Unset the bucket ACLs
        result = s3.put_bucket_acl(Bucket=bucket,ACL='private')
    
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result) 
        else:
            text_output = text_output + "Bucket ACL deleted: %s \n" % bucket
    
    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output