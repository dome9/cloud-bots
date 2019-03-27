'''
## cloudtrail_enable
What it does: Creates a new S3 bucket and turns on a multi-region trail that logs to it. 
Pre-set Settings:  
Bucket name: acct<account_id>cloudtraillogs 
IsMultiRegionTrail: True (CIS for AWS V 1.1.0 Section 2.1)
IncludeGlobalServiceEvents: True
EnableLogFileValidation: True (CIS for AWS V 1.1.0 Section 2.2) 
Default trail name if unset: allRegionTrail
Usage: AUTO: cloudtrail_enable trail_name=<trail_name> bucket_name=<bucket_name>
Note: Trail_name and bucket_name are optional and don't need to be set. 
Limitations: none 

'''

import boto3
import json
import re
from botocore.exceptions import ClientError

# Create S3 bucket
def make_bucket(boto_session,region,account_id,bucket_name):
    s3_client = boto_session.client('s3')

    try:
        if region == "us-east-1":
            result = s3_client.create_bucket(Bucket=bucket_name)
        elif region == "eu-west-1":
            region = "EU"
            result = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
                )
        else:
            result = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
                )
        
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Bucket %s was created for storing trails\n" % bucket_name
   
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


# Add S3 policy
def add_bucket_policy(boto_session,account_id,bucket_name):
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": "arn:aws:s3:::" + bucket_name
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": "arn:aws:s3:::" + bucket_name + "/AWSLogs/" + account_id + "/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }

    try:
        # Create an S3 client
        s3_client = boto_session.client('s3')

        # Convert the policy to a JSON string
        bucket_policy = json.dumps(bucket_policy)

        # Set the new policy on the given bucket
        result = s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Bucket policy updated for cloudtrail delivery.\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output




# Create trail
def create_trail(boto_session,trail_name,bucket_name): 
    cloudtrail_client = boto_session.client('cloudtrail')

    try:
        result = cloudtrail_client.create_trail(
            Name=trail_name,
            S3BucketName=bucket_name, 
            S3KeyPrefix = '',
            IncludeGlobalServiceEvents=True, 
            IsMultiRegionTrail=True, 
            EnableLogFileValidation=True
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "CloudTrail created successfully. Enabling logging next.\n"
            try:
                trail_arn = result['TrailARN']
                response = cloudtrail_client.start_logging(Name=trail_arn)
                
                responseCode = result['ResponseMetadata']['HTTPStatusCode']
                if responseCode >= 400:
                    text_output = text_output +  "Unexpected error: %s \n" % str(result)
                else:
                    text_output = text_output +  "CloudTrail logging enabled\n"

            except ClientError as e:
                text_output = text_output +  "Unexpected error: %s \n" % e

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


def run_action(boto_session,rule,entity,params): 
    account_id = entity['accountNumber']

    region = entity['region']
    region = region.replace("_","-")
    text_output = ""

    env_variables = {} # Go through the params and pull out the key values that are optional for cloudtrail settings
    for param in params:
        name, var = param.partition("=")[::2]
        env_variables[name.strip()] = var

    # Check params for usable values and if not - go to defaults
    try: # Params[0] should be the traffic type. 
        trail_name = env_variables['trail_name']
        text_output = text_output + "CloudTrail name will be %s \n" % trail_name
    except:
        trail_name = "allRegionTrail"
        text_output = text_output +  "Trail name not set. Defaulting to allRegionTrail.\n"
        
    try:
        bucket_name = env_variables['bucket_name']
        text_output = text_output +  "Sending trails to bucket: %s \n" % bucket_name
    except:
        try:
            bucket_name = "acct%scloudtraillogs" % account_id
            text_output = text_output + "No target bucket defined in params. Creating a local bucket instead with bucket name %s \n" % bucket_name
            text_output = text_output + make_bucket(boto_session,region,account_id,bucket_name) 
            text_output = text_output + add_bucket_policy(boto_session,account_id,bucket_name) 
        except ClientError as e:
            text_output = text_output +  "Unexpected error: %s \n" % e
    
    try:
        text_output = text_output + create_trail(boto_session,trail_name,bucket_name)
        
    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output
