'''
s3_enable_logging
What it does: Turns on server access logging. The target bucket needs to be in the same region as the remediation bucket or it'll throw a CrossLocationLoggingProhibitted error. This bot will create a bucket to log to as well.
Usage: AUTO: s3_enable_logging 
Limitations: none
'''

import boto3
import json
from botocore.exceptions import ClientError


## Turn on S3 bucket logging
def run_action(boto_session, rule, entity, params):
    bucket_name = entity['id']
    accountNumber = entity['accountNumber']
    region = entity['region'].replace("_", "-")
    text_output = ""

    s3_client = boto_session.client('s3')
    s3_resource = boto_session.resource('s3')
    bucket_logging = s3_resource.BucketLogging(bucket_name)

    target_bucket_name = accountNumber + "s3accesslogs" + region

    # The target bucket needs to be in the same region as the remediation bucket or it'll throw a CrossLocationLoggingProhibitted error.
    try:
        # Check if the bucket exists. If not, create one
        s3_client.head_bucket(Bucket=target_bucket_name)  # Check if the bucket exists. If not, create one

    except ClientError:
        # The bucket does not exist or you have no access. Create it    
        try:
            if region == "us-east-1":
                result = s3_client.create_bucket(
                    Bucket=target_bucket_name,
                )
            elif region == "eu-west-1":
                region = "EU"
                result = s3_client.create_bucket(
                    Bucket=target_bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            else:
                result = s3_client.create_bucket(
                    Bucket=target_bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )

            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = "Unexpected error: %s \n" % str(result)
            else:
                text_output = "Logging bucket created %s \n" % target_bucket_name

        except ClientError as e:
            text_output = "Unexpected error: %s \n" % e

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
            text_output = text_output + "Unexpected error enable logging: %s \n" % str(result)
            raise Exception(text_output);

        loggingPolicy = {
            "Effect": "Allow",
            "Principal": {
                "Service": "logging.s3.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::" + target_bucket_name + "/*",
            "Condition": {
                "ArnLike": {
                    "aws:SourceArn": "arn:aws:s3:::" + bucket_name}
            }
        }
        try:
            existing_policy = s3_client.get_bucket_policy(Bucket=target_bucket_name)
            existing_policy_json = json.loads(existing_policy['Policy'])
            existing_policy_json['Statement'].append(loggingPolicy)
            resultUpdatePolicy = s3_resource.Bucket(target_bucket_name).Policy().put(
                Policy=json.dumps(existing_policy_json))

            responseCodeUpdatePolicy = resultUpdatePolicy['ResponseMetadata']['HTTPStatusCode']
            if responseCodeUpdatePolicy >= 400:
                text_output = text_output + "Unexpected error Update Policy: %s \n" % str(result)
                raise Exception(text_output)

        except s3_client.exceptions.from_code('NoSuchBucketPolicy'):
            policy = {
                "Version": "2012-10-17",
                "Statement": [loggingPolicy]}
            resultUpdatePolicy = s3_resource.Bucket(target_bucket_name).Policy().put(
                Policy=json.dumps(policy))

            responseCodeUpdatePolicy = resultUpdatePolicy['ResponseMetadata']['HTTPStatusCode']
            if responseCodeUpdatePolicy >= 400:
                text_output = text_output + "Unexpected error Update Policy: %s \n" % str(result)
                raise Exception(text_output)


        text_output = text_output + "Bucket logging enabled from bucket: %s to bucket: %s \n" % (
            bucket_name, target_bucket_name)

    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output
