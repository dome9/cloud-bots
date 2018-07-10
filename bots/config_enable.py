'''
## config_enable
What it does: Enables AWS Config. This DOES NOT create config rules. It only turns on the configuration recorders. 
Usage: AUTO: config_enable  
Limitations: none  
Defaults: 
    name = default
    allSupported = True
    includeGlobalResourceTypes = True
    file deliveryFrequency(to S3) = One_Hour
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

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
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

def create_config_recorder(config_client,accountNumber):    
    print("Creating ConfigurationRecorder")

    role_id = "arn:aws:iam::" + accountNumber + ":role/AWSConfigRole"

    try:
        result = config_client.put_configuration_recorder(
        ConfigurationRecorder={
            'name': 'default',
            'roleARN': role_id,
            'recordingGroup': {
                'allSupported': True,
                'includeGlobalResourceTypes': True,
                }
            }
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "AWS Config recorder created\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

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
    try:
        s3_client.head_bucket(Bucket=target_bucket_name)
        text_output = "Bucket %s already exists. Checking bucket policy next\n" % target_bucket_name

    except ClientError:
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

    target_bucket_name = accountNumber + "awsconfiglogs" 

    #The clients will be reused so we'll set them up just once
    config_client = boto_session.client('config')
    iam_client = boto_session.client('iam')
    s3_client = boto_session.client('s3')
    s3_resource = boto_session.resource('s3')

    text_output = "Setting up config for %s \n" % region

    #Do work
    text_output = text_output + create_role(iam_client) # Create a role for AWS Config
    text_output = text_output + add_policy_to_role(iam_client) # Attach the service policy to the role
    text_output = text_output + create_config_recorder(config_client,accountNumber) # Set up the config recorders 
    text_output = text_output + create_bucket(s3_client,s3_resource,region,target_bucket_name,accountNumber) # Create a bucket for config to store logs in if it's not already there
    text_output = text_output + put_delivery_channel(config_client,target_bucket_name) # Tell config to send the logs to the bucket
    text_output = text_output + start_config_recorder(config_client) # Turn it on

    return text_output 





