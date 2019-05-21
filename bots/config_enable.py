'''
## config_enable
Description: Enables AWS Config. This DOES NOT create config rules. It only turns on the configuration recorders.
Required Permissions: config:PutConfigurationRecorder, config:PutDeliveryChannel, config:StartConfigurationRecorder, iam:CreateRole, iam:AttachRolePolicy, s3:HeadBucket, s3:CreateBucket, s3:PutBucketPolicy

Usage: AUTO: config_enable bucket_name=mybucketlogs bucket_region=us-west-1 include_global_resource_types_region=us-west-1
Limitations: none  
Variables (and their defaults): 
    bucket_name = accountNumber + "awsconfiglogs"
    bucket_region = us-west-1
    allSupported = True
    includeGlobalResourceTypes = True (if you want to change this, use the variable include_global_resource_types_region=<desired_region>)

Defaults (not changable currently via variable):
    file deliveryFrequency(to S3) is set to One_Hour
    config_name = default
'''

import boto3
import json
from botocore.exceptions import ClientError

# Try to create the role
def create_role(iam_client):
    print("Creating role for Config")

    trust_policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
            "Service": "config.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }


    try:
        response = iam_client.create_role(
            RoleName='AWSConfigRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Created by Dome9 CloudBots. This is to allow Config to collect data'
            )

        responseCode = response['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(response)
        else:
            text_output = "AWS Config role successfully created.\n"

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'EntityAlreadyExists':
             text_output =  "AWSConfigRole role already exists in this account\n"
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output


def add_policy_to_role(iam_client):        
    print("Adding policy to new role")
    try:
        attach_policy_response = iam_client.attach_role_policy(
            RoleName='AWSConfigRole',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSConfigRole'
        )
        text_output = "AWSConfigRole policy attached to role\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output

def create_config_recorder(config_client,accountNumber,region,include_global_resource_types_region):    
    print("Creating ConfigurationRecorder")

    role_id = "arn:aws:iam::" + accountNumber + ":role/AWSConfigRole"
 
    if region == include_global_resource_types_region:
        include_resource_types = True
        text_output = "Creating Configuration recorder\nincludeGlobalResourceTypes will be set to true\n"
    elif include_global_resource_types_region == "Null":
        ## include_global_resource_types_region is not set. Default to true
        include_resource_types = True
        text_output = "Creating Configuration recorder\nincludeGlobalResourceTypes will be set to true\n"
    else:
        include_resource_types = False
        text_output = "Creating Configuration recorder\nincludeGlobalResourceTypes will be set to false\n"
            
    try:
        result = config_client.put_configuration_recorder(
        ConfigurationRecorder={
            'name': 'default',
            'roleARN': role_id,
            'recordingGroup': {
                'allSupported': True,
                'includeGlobalResourceTypes': include_resource_types,
                }
            }
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "AWS Config recorder created\n"

    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output


def start_config_recorder(config_client):
    try:
        result = config_client.start_configuration_recorder(
            ConfigurationRecorderName='default'
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "AWS Config recorder started \n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


def create_bucket(s3_client,s3_resource,region,target_bucket_name,accountNumber):
    #This will work across regions so we only need one bucket. 
    text_output = ""
    try:
        s3_client.head_bucket(Bucket=target_bucket_name)
        text_output = "Bucket %s already exists. Checking bucket policy next\n" % target_bucket_name

    except ClientError as e:
        if e.response['Error']['Code'] == "403":
            text_output = "Bucket %s already exists. Skipping\n" % target_bucket_name
            return text_output

        # The bucket does not exist or you have no access. Create it    
        print("Creating S3 bucket")
        try: ## Currently getting an illegallocationconstraintexception on us-east-1. Still working on it
            if region == "us-east-1":
                result = s3_resource.create_bucket(
                        Bucket=target_bucket_name
                    )
            elif region == "eu-west-1":
                region = "EU"
                result = s3_resource.create_bucket(
                        Bucket=target_bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
            else:
                result = s3_resource.create_bucket(
                        Bucket=target_bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
            
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = "Unexpected error: %s \n" % str(result)
            else:
                text_output = "Config logs bucket created %s \n" % target_bucket_name
       
        except ClientError as e:
            error = e.response['Error']['Code']
            if error == 'BucketAlreadyOwnedByYou':
                text_output = "Bucket %s already owned by this account. Checking bucket policy next\n" % target_bucket_name
            elif error == 'BucketAlreadyExists':
                text_output = "Bucket %s already exists. Checking bucket policy next\n" % target_bucket_name
            elif error == 'OperationAborted':
                text_output = "Another bucket creation is in progress. Skipping.\n"
            else:
                text_output = "Unexpected error: %s \n" % e


        ### ATTACH BUCKET POLICY
        print("Attaching bucket policy")
        try:
            bucket_arn = "arn:aws:s3:::" + target_bucket_name

            resource_id = bucket_arn + "/AWSLogs/" + accountNumber + "/Config/*"

            bucket_policy = {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "AWSConfigBucketPermissionsCheck",
                  "Effect": "Allow",
                  "Principal": {
                    "Service": [
                     "config.amazonaws.com"
                    ]
                  },
                  "Action": "s3:GetBucketAcl",
                  "Resource": bucket_arn 
                },
                {
                  "Sid": "AWSConfigBucketDelivery",
                  "Effect": "Allow",
                  "Principal": {
                    "Service": [
                     "config.amazonaws.com"    
                    ]
                  },
                  "Action": "s3:PutObject",
                  "Resource": resource_id,
                  "Condition": { 
                    "StringEquals": { 
                      "s3:x-amz-acl": "bucket-owner-full-control" 
                    }
                  }
                }
              ]
            }  

            bucket_policy_string = json.dumps(bucket_policy)

            result = s3_client.put_bucket_policy(
                Bucket=target_bucket_name,
                Policy=bucket_policy_string
            )
             
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s \n" % str(result)
            else:
                text_output = text_output + "Bucket policy attached to bucket for Config file delivery\n"

        except ClientError as e:
            text_output = text_output + "Unexpected error: %s \n" % e

    return text_output

def put_delivery_channel(config_client,target_bucket_name):
    try:
        #Give the config somewhere to go
        result = config_client.put_delivery_channel(
            DeliveryChannel={
                'name': 'default',
                's3BucketName': target_bucket_name,
                'configSnapshotDeliveryProperties': {
                    'deliveryFrequency': 'One_Hour'
                }
            }
        )
         
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "DeliveryChannel set to deliver to S3\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output

def run_action(boto_session,rule,entity,params):
    region = entity['region']
    region = region.replace("_","-")
    accountNumber = entity['accountNumber']
    text_output = ""
    ### Params handling ###
    # 3 optional variables - bucket_name, bucket_region, include_global_resource_types_region
    if len(params) > 0:
        for i in params:
            try:
                key_value = i.split("=")
                key = key_value[0]
                value = key_value[1]

                if key == "bucket_name":
                    target_bucket_name = value
                    text_output = text_output + "S3 Bucket name will be %s \n" % target_bucket_name

                elif key == "bucket_region":
                    target_bucket_region = value
                    text_output = text_output + "S3 Bucket region will be %s \n" % target_bucket_region
                    
                elif key == "include_global_resource_types_region":
                    include_global_resource_types_region = value
                    text_output = text_output + "Include global_logs_region will be set as %s \n" % include_global_resource_types_region

            except:
                text_output = text_output + "Params formatting doesn't match required formatting. Using defaults."
                break

    #### IF VARIABLE ISN'T SET - FALL BACK
    try:
        print ("Target_bucket_name: %s" % target_bucket_name)
    except NameError:
        target_bucket_name = accountNumber + "awsconfiglogs"
        text_output = text_output +  "S3 Bucket name not set. Defaulting to %s.\n" % target_bucket_name

    try:
        print("Target bucket region: %s" % target_bucket_region) 
    except NameError:    
        target_bucket_region = "us-west-1"
        text_output = text_output +  "S3 Bucket region not set. Defaulting to %s.\n" % target_bucket_region

    try:
        print("Include global logs region: %s" % include_global_resource_types_region)
    except NameError:    
        text_output = text_output +  "All regions will have 'includeGlobalResourceTypes' set to true.\n" 
        include_global_resource_types_region = "Null"


    #The clients will be reused so we'll set them up just once
    config_client = boto_session.client('config')
    iam_client = boto_session.client('iam')
    s3_client = boto_session.client('s3')
    s3_resource = boto_session.resource('s3')

    text_output = "Setting up config for %s \n" % region

    #Do work
    text_output = text_output + create_role(iam_client) # Create a role for AWS Config
    text_output = text_output + add_policy_to_role(iam_client) # Attach the service policy to the role
    text_output = text_output + create_config_recorder(config_client,accountNumber,region,include_global_resource_types_region) # Set up the config recorders 
    text_output = text_output + create_bucket(s3_client,s3_resource,target_bucket_region,target_bucket_name,accountNumber) # Create a bucket for config to store logs in if it's not already there
    text_output = text_output + put_delivery_channel(config_client,target_bucket_name) # Tell config to send the logs to the bucket
    text_output = text_output + start_config_recorder(config_client) # Turn it on

    return text_output 





