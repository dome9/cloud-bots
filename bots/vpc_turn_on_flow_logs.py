'''
## vpc_turn_on_flow_logs
What it does: Turns on flow logs for a VPC
Settings: 
Log Group Name: vpcFlowLogs
If traffic type to be logged isn't specified, it defaults to all.
Usage: AUTO: vpc_turn_on_flow_logs <all|accept|reject>
Limitations: none 

#log delivery policy name is set as: vpcFlowLogDelivery
#log relivery role is set as: vpcFlowLogDelivery
'''

import boto3
import json
from botocore.exceptions import ClientError

def create_log_delivery_policy(boto_session):
    # Create IAM client
    iam_client = boto_session.client('iam')

    try:
        # Create a policy
        deny_policy = {
            "Version": "2012-10-17",
            "Statement": [
            {
              "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents"
              ],
              "Effect": "Allow",
              "Resource": "*"
            }
          ]
        }

        create_policy_response = iam_client.create_policy(
            PolicyName='vpcFlowLogDelivery',
            PolicyDocument=json.dumps(deny_policy)
        )

        responseCode = create_policy_response['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % create_policy_response
        else:
            text_output = "vpcFlowLogDelivery policy successfully created.\n"  

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output

#Poll the account and check if the log delivery IAM policy exists. If not - make it
def check_for_log_delivery_policy(boto_session,policy_arn):
    # Create IAM client
    iam_client = boto_session.client('iam')

    try:
        #Check to see if the deny policy exists in the account currently
        get_policy_response = iam_client.get_policy(PolicyArn=policy_arn)
        
        if get_policy_response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output = "IAM vpcFlowLogDelivery policy exists in this account.\n"

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            #If the policy isn't there - add it into the account
            text_output = create_log_delivery_policy(boto_session)
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output


# Try to create the role
def create_role(boto_session,policy_arn):
    iam_client = boto_session.client('iam')

    trust_policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
            "Service": "vpc-flow-logs.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }

    try:
        response = iam_client.create_role(
            RoleName='vpcFlowLogDelivery',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Created by Dome9 remediation function. This is to allow flow logs to be delivered to CloudWatch'
            )

        if response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output =  "vpcFlowLogDelivery role successfully created.\n"

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'EntityAlreadyExists':
            #If the policy isn't there - add it into the account
             text_output =  "vpcFlowLogDelivery role already exists in this account.\n"
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output

def add_policy_to_role(boto_session,policy_arn):        
    # Create IAM client
    iam_client = boto_session.client('iam')
    
    try:
        attach_policy_response = iam_client.attach_role_policy(
            RoleName="vpcFlowLogDelivery",
            PolicyArn=policy_arn
        )
        text_output = "Flow log delivery policy attached to role.\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output

def create_logs(boto_session,role_id,vpc_id,traffic_type.region):
    ec2_client = boto_session.client('ec2')

    #Resource IDs need to be in a list - not string
    vpc_ids = []
    vpc_ids.append(vpc_id)

    try:
        response = ec2_client.create_flow_logs(
            DeliverLogsPermissionArn=role_id,
            LogGroupName='vpcFlowLogs',
            ResourceIds=vpc_ids,
            ResourceType='VPC',
            TrafficType=traffic_type
        )

        if response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output =  "VPC Flow Logs successfully created. FlowLogID: %s \n" % response['FlowLogIds']
        else:
            text_output = "Unexpected error: %s \n" % e
    
    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'FlowLogAlreadyExists':
            #If the policy isn't there - add it into the account
             text_output =  "There is an existing Flow Log in this VPC with the same configuration and log group. Skipping.\n"
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output



# Main function
def run_action(boto_session,rule,entity,params): 
    # Setup variables
    vpc_id = entity['id']
    account_id = entity['accountNumber']
    policy_arn = "arn:aws:iam::" + account_id + ":policy/vpcFlowLogDelivery"
    role_id = "arn:aws:iam::" + account_id + ":role/vpcFlowLogDelivery"

    ## Set to pull traffic type from params but default to all
    try: # Params[0] should be the traffic type. 
        traffic_type = params[0].upper()
        if traffic_type not in ('ALL', 'ACCEPT', 'REJECT'):
            traffic_type = "ALL"
            text_output = "Traffic_type is set to %s and the only accepted values are ALL, ACCEPT, REJECT. Defaulting to ALL\n." % traffic_type
        else:
            text_output = "%s traffic will be logged. Starting log creation\n" % traffic_type

    except: #If there's no params passed at all, we default to ALL
        traffic_type = "ALL" ## Set to all if not specified

    try:
        text_output = text_output + check_for_log_delivery_policy(boto_session,policy_arn) # Check for the policy to deliver logs from VPC to CloudWatch
        text_output = text_output + create_role(boto_session,policy_arn) # Check for role / create it if it doesn't exist
        text_output = text_output + add_policy_to_role(boto_session,policy_arn)
        text_output = text_output + create_logs(boto_session,role_id,vpc_id,traffic_type,region) # Create the flow logs
        
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e
    
    return text_output
