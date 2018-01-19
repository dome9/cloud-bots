import boto3
import json
import os
import re
from botocore.exceptions import ClientError


#Usage:
#AUTO: vpc_turn_on_flow_logs (All|Reject|Accept)
#ex: AUTO: vpc_turn_on_flow_logs (All)

#assumptions / settings: 
#log delivery policy is set as: 
#log relivery role is set as: 



vpc_id = "vpc-a7fb7fc0"
account_id = "621958466464"
compliance_tags = ["a", "b", "vpc-a7fb7fc0", "AUTO: vpc_turn_on_flow_logs (All)"]


#set defaults but allow them to be overridden


####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################

#This will make the quarantining IAM policy that'll be applied to the users or roles that need to be locked down.
def create_log_delivery_policy():
    # Create IAM client
    iam = boto3.client('iam')

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
        create_policy_response = iam.create_policy(
            PolicyName='FlowLogsDelivery',
            PolicyDocument=json.dumps(deny_policy)
        )

        responseCode = create_policy_response['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            print("Unexpected error: %s \n" % (create_policy_response))
        else:
            print("FlowLogsDelivery policy successfully created.\n")    

    except (ClientError) as e:
        print("Unexpected error: %s \n" % (e))

    return text_output

#Poll the account and check if the quarantine_deny_all policy exists. If not - make it
def check_for_log_delivery_policy(policy_arn):
    # Create IAM client
    iam = boto3.client('iam')

    try:
        #Check to see if the deny policy exists in the account currently
        get_policy_response = iam.get_policy(PolicyArn=policy_arn)
        
        if get_policy_response['ResponseMetadata']['HTTPStatusCode'] < 400:
            print ("IAM FlowLogsDelivery policy exists in this account.\n")

    except (ClientError) as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            #If the policy isn't there - add it into the account
            event_log = create_log_delivery_policy(event_log)
        else:
            print("Unexpected error: %s \n" % (e))

    return text_output


### NEED TO CHECK FOR ROLE
def create_role(policy_arn):
    iam = boto3.client('iam')

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
        response = client.create_role(
            RoleName='vpcFlowLogDelivery',
            AssumeRolePolicyDocument=trust_policy,
            Description='Created by Dome9 remediation function. This is to allow flow logs to be delivered to CloudWatch'
            )
    except (ClientError) as e:
        print("Unexpected error: %s \n" % (e))

    responseCode = create_policy_response['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        print("Unexpected error: %s" % str(response) + "\n")
    else:
        print("vpcFlowLogDelivery role successfully created.\n")    

    return text_output

def add_policy_to_role(policy_arn):        
    # Create IAM client
    iam = boto3.client('iam')
    
    try:
        attach_policy_response = iam.attach_role_policy(
            RoleName=vpcFlowLogDelivery,
            PolicyArn=policy_arn
        )
        print("IAM policy attached to role: \"" + role + "\"\n")

    except (ClientError) as e:
        print("Unexpected error: %s \n" % (e))

    return text_output



def run_action(compliance_tags,vpc):

    account_id = message['Entity']['AccountNumber']

    #Get the VPC ID out of the message
    
    ec2 = boto3.client('ec2')

    for tag in compliance_tags:
        tag = tag.strip() #Sometimes the tags come through with trailing or leading spaces. 
        remediate_tag = re.match(r'AUTO:\svpc_turn_on_flow_logs\s\((?P<traffic_type>.+)\)', tag) #we just want the tag that matches "AUTO: vpc_turn_on_flow_logs (Action)"

        if remediate_tag:
            traffic_type = remediate_tag.group(1) #The flag that we pulled from the parenthesis
            if traffic_type not in ("All", "Accept", "Reject"): #make sure we can handle this value
                print("The type of logs to capture needs to be specified. You put in: " + traffic_type + " and the approved values are \"Accept, All, or Reject\". Please tag the rule with one of those three and try again.\n")
                return

        policy_arn = "arn:aws:iam::" + account_id + ":policy/FlowLogsDelivery"

        output = check_for_log_delivery_policy(policy_arn) #Check for the policy to deliver logs from VPC to CloudWatch
        print(output)

        create_role(policy_arn)

        #check for role

        add_policy_to_role(policy_arn)

        # do we want to set the loggroup name to something different for each vpc?
        role_id = "arn:aws:iam::" + account_id + ":role/vpcFlowLogDelivery"

        try:
            response = ec2.create_flow_logs(
                DeliverLogsPermissionArn=role_id,
                LogGroupName='vpcFlowLogs',
                ResourceIds=vpc_id,
                ResourceType='VPC',
                TrafficType=traffic_type
            )

        except (ClientError) as e:
            print("Unexpected error: %s \n" % (e))

    print (text_output)
