'''
## cloudtrail_enable
What it does: Creates a new S3 bucket and turns on a multi-region trail that logs to it. 
Pre-set Settings:  
Bucket name: acct<account_id>cloudtraillogs
IsMultiRegionTrail: True (CIS for AWS V 1.1.0 Section 2.1)
IncludeGlobalServiceEvents: True
EnableLogFileValidation: True (CIS for AWS V 1.1.0 Section 2.2) 
Usage: AUTO: cloudtrail_enable 
Limitations: none 
'''

import boto3
import json
from botocore.exceptions import ClientError

# Create S3 bucket
def make_bucket(account_id,bucket_name):

    try:
        s3 = boto3.resource('s3', region_name='us-east-1')
        result = s3.create_bucket(Bucket=bucket_name)
        text_output = "Bucket %s will be used for storing trails\n" % bucket_name

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


# Add S3 policy
def add_bucket_policy(account_id,bucket_name):
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
        s3 = boto3.client('s3')

        # Convert the policy to a JSON string
        bucket_policy = json.dumps(bucket_policy)

        # Set the new policy on the given bucket
        result = s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Bucket policy updated for cloudtrail delivery.\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output




# Create trail
def create_trail(params,bucket_name): 
    cloudtrail = boto3.client('cloudtrail')
    # Check params for usable values and if not - go to defaults
    try: # Params[0] should be the traffic type. 
        trailName = params[0]
        text_output = "CloudTrail name will be %s and data will be sent to the S3 bucket: %s \n" % (trailName,bucket_name)
    except:
        trailName = allRegionTrail
        text_output = "Trail name not set. Defaulting to allRegionTrail.\n"
        
    try:
        result = cloudtrail.create_trail(
            Name=trailName, ### REQUIRED
            S3BucketName=bucket_name, ### REQUIRED
            S3KeyPrefix = '',
            IncludeGlobalServiceEvents=True, 
            IsMultiRegionTrail=True, 
            EnableLogFileValidation=True
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output +  "CloudTrail created successfully. Enabling logging next.\n"
            try:
                trail_arn = result['TrailARN']
                response = cloudtrail.start_logging(Name=trail_arn)
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


def run_action(rule,entity,params): 
    account_id = entity['accountNumber']
    bucket_name = "acct%scloudtraillogs" % account_id

    try:
        text_output = make_bucket(account_id,bucket_name) 
        text_output = text_output + add_bucket_policy(account_id,bucket_name) 
        text_output = text_output + create_trail(params,bucket_name)
        
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output
