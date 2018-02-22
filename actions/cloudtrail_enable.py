import boto3
import json
from botocore.exceptions import ClientError

# Usage:
# AUTO: cloudtrail_enable <trailName> <S3BucketName>

# Settings: 
# IsMultiRegionTrail: True (CIS for AWS V 1.1.0 Section 2.1)
# IncludeGlobalServiceEvents: True
# ElableLogFileValidation: True (CIS for AWS V 1.1.0 Section 2.2)
# Boto3 Cloudtrail docs:
# http://boto3.readthedocs.io/en/latest/reference/services/cloudtrail.html#CloudTrail.Client.create_trail

#### IAM Permissions needed ########
# s3:PutObject
# cloudtrail:CreateTrail

def run_action(rule,entity,params): 
    cloudtrail = boto3.client('cloudtrail')
    # Check params for usable values and if not - go to defaults
    try: # Params[0] should be the traffic type. 
        trailName = params[0]
        bucketName = params[1].lower()
        text_output = "CloudTrail name will be %s and data will be sent to the S3 bucket: %s \n" % (trailName,bucketName)
    except:
        text_output = "BOTH trailName and bucketName need to be specified in the tag. Please set the variables and try again\n"
        return text_output

    try:
        result = cloudtrail.create_trail(
            Name=trailName, ### REQUIRED
            S3BucketName=bucketName, ### REQUIRED
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
        error = e.response['Error']['Code']
        if error == 'InvalidS3BucketNameException':
            #If the policy isn't there - add it into the account
             text_output =  "S3 bucket name %s is invalid. Please verify and try again.\n" % bucketName
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output