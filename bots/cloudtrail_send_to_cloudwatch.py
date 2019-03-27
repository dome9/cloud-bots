'''
## cloudtrail_send_to_cloudwatch
What it does: Makes CloudTrail output logs to CloudWatchLogs. If the log group doesn't exist alredy, it'll reate a new one. 
Usage: AUTO: cloudtrail_send_to_cloudwatch <log_group_name>  
Limitations: none  
Defaults: 
    If no log group name is set, it'll default to CloudTrail/DefaultLogGroup
    Role name: CloudTrail_CloudWatchLogs_Role
    Log delivery policy name: CloudWatchLogsAllowDelivery
'''

import boto3
import json
from botocore.exceptions import ClientError

# Try to create the role
def create_role(iam_client):
    print("Creating role for CloudTrail log delivery")

    role_name = 'CloudTrail_CloudWatchLogs_Role'

    trust_policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
            "Service": "cloudtrail.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }

    try:
        result = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Created by Dome9 CloudBots. This is to allow CloudTrail to send logs to CloudWatch'
            )
    
        responseCode = result['ResponseMetadata']['HTTPStatusCode']    
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "CloudTrail to CLoudwatch role successfully created.\n"

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'EntityAlreadyExists':
             text_output =  "%s role already exists in this account\n" % role_name
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output

def create_log_delivery_policy(iam_client,log_group_arn):
    print("Creating log delivery policy")
    try:
        # Create a policy
        delivery_policy = {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "AWSCloudTrailCreateLogStream20141101",
              "Effect": "Allow",
              "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
              ],
              "Resource": "*"
            }
          ]
        }

        result = iam_client.create_policy(
            PolicyName='CloudWatchLogsAllowDelivery',
            PolicyDocument=json.dumps(delivery_policy)
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % create_policy_response
        else:
            text_output = "CloudWatchLogsAllowDelivery policy successfully created.\n"  

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'EntityAlreadyExists':
             text_output =  "CloudWatchLogsAllowDelivery policy already exists in this account\n" 
        else:
            text_output = "Unexpected error: %s \n" % e


    return text_output


def add_policy_to_role(iam_client,log_policy_arn):        
    print("Attaching policy to role")

    try:
        result = iam_client.attach_role_policy(
            RoleName="CloudTrail_CloudWatchLogs_Role",
            PolicyArn=log_policy_arn
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % attach_policy_response
        else:
            text_output = "CloudTrail log delivery policy attached to role.\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output




def create_log_group(boto_session,log_group_name):
    cloudwatchlogs_client = boto_session.client('logs')
    print("Creating log group")
    
    try:
        result = cloudwatchlogs_client.create_log_group(logGroupName=log_group_name)

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Log group created: %s \n" % log_group_name

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'ResourceAlreadyExistsException':
            text_output = "Log group already exists. Skipping\n"
        else:
            text_output = "Unexpected error: %s \n" % e
    

    return text_output 



def update_trail(boto_session,trail_name,log_group_arn,log_role_arn):
    cloudtrail_client = boto_session.client('cloudtrail')
    print("Updating trail")

    try:
        result = cloudtrail_client.update_trail(
            Name=trail_name,
            CloudWatchLogsLogGroupArn=log_group_arn,
            CloudWatchLogsRoleArn=log_role_arn,
        )
                 
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Cloudtrail updated to send logs to CloudWatchLogs\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output 


def run_action(boto_session,rule,entity,params):
    region = entity['region']
    region = region.replace("_","-")
    accountNumber = entity['accountNumber']
    trail_name = entity['id']

    iam_client = boto_session.client('iam')

    try:
        log_group_name = params[0]
        text_output = "Setting the log group to %s \n" % log_group_name
    except IndexError as e:
        log_group_name = "CloudTrail/DefaultLogGroup" 
        text_output = "No log_group_name defined in params. Defaulting to CloudTrail/DefaultLogGroup\n"

    
    log_group_arn = "arn:aws:logs:" + region + ":" + accountNumber + ":log-group:" + log_group_name + ":*"
    log_role_arn = "arn:aws:iam::" + accountNumber + ":role/CloudTrail_CloudWatchLogs_Role"
    log_policy_arn = "arn:aws:iam::" + accountNumber + ":policy/CloudWatchLogsAllowDelivery"

    text_output = text_output + create_log_group(boto_session,log_group_name)
    text_output = text_output + create_role(iam_client) # Create role
    text_output = text_output + create_log_delivery_policy(iam_client,log_group_arn) # Create policy
    text_output = text_output + add_policy_to_role(iam_client,log_policy_arn) # Attach policy > role
    text_output = text_output + update_trail(boto_session,trail_name,log_group_arn,log_role_arn)
    text_output = text_output + "Outputs:\n  Log Group ARN: %s \n  Log Role ARN: %s \n  Log Delivery Policy ARN: %s \n" % (log_group_arn,log_role_arn,log_policy_arn)

    return text_output 



