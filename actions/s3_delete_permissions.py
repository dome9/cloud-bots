import boto3
import json
import os
from botocore.exceptions import ClientError

### DeleteS3BucketPermissions ###
def run_action(message):
    # Create an S3 client
    s3 = boto3.client('s3')

    bucket = message['Entity']['Id']

    try:
        #sendEvent out the S3 permissions first so we can reference them later
        bucket_policy = s3.get_bucket_policy(Bucket=bucket)['Policy']
        text_output = "Bucket policy that will be deleted: \n " + str(bucket_policy) + "\n"
                
        #Call S3 to delete the bucket policy for the given bucket
        bucket_policy_delete_output = s3.delete_bucket_policy(Bucket=bucket)
        
        responseCode = bucket_policy_delete_output['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s" % bucket_policy_delete_output + "\n"
        else:
            text_output = text_output + "Bucket policy deleted: " + bucket + " \n"

    except (ClientError, AttributeError) as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchBucketPolicy':
             text_output = "Bucket " + bucket + " does not have a bucket policy. Checking ACLs next.\n"
        else:
            text_output = "Unexpected error: %s" % e + "\n"

    try:
        #list bucket ACLs
        bucket_acls = s3.get_bucket_acl(Bucket=bucket)['Grants']
        
        if len(bucket_acls) == 1:
            text_output = text_output + "Only the CanonicalUser ACL found. Skipping.\n"
        else:
            text_output = text_output + "ACLs that will be removed: \n " + str(bucket_acls) + "\n"

            # Unset the bucket ACLs
            acl_delete_output = s3.put_bucket_acl(Bucket=bucket,ACL='private')
        
            responseCode = acl_delete_output['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s" % acl_delete_output + "\n"
            else:
                text_output = text_output + "Bucket ACL deleted: " + bucket + " \n"
    
    except (ClientError, AttributeError) as e:
        text_output = text_output + "Unexpected error: %s" % e + "\n"

    return text_output
