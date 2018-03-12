'''
## iam_quarantine_user
What it does: Adds an explicit deny all policy to IAM and directly attaches it to a user  
Usage: AUTO: iam_quarantine_user  
Limitations: none  
'''

import boto3
import json
from botocore.exceptions import ClientError

#This will make the quarantining IAM policy that'll be applied to the users or roles that need to be locked down.
def create_deny_policy():
    # Create IAM client
    iam = boto3.client('iam')
    
    # Create a policy
    deny_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Deny",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }
    create_policy_response = iam.create_policy(
        PolicyName='quarantine_deny_all_policy',
        PolicyDocument=json.dumps(deny_policy)
    )

    responseCode = create_policy_response['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % create_policy_response
    else:
        text_output = "IAM deny-all policy successfully created.\n"
  
    return text_output

#Poll the account and check if the quarantine_deny_all policy exists. If not - make it
def check_for_deny_policy(policy_arn):
    # Create IAM client
    iam = boto3.client('iam')
    
    try:
        #Check to see if the deny policy exists in the account currently
        get_policy_response = iam.get_policy(PolicyArn=policy_arn)
        
        if get_policy_response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output =  "IAM deny-all policy exists in this account.\n"

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            #If the policy isn't there - add it into the account
            text_output = create_deny_policy()
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output


#Create attach the policy to the group
def add_policy_to_user(user,policy_arn):        
    # Create IAM client
    iam = boto3.client('iam')
    
    try:
        attach_policy_response = iam.attach_user_policy(
            UserName=user,
            PolicyArn=policy_arn
        )
        text_output = "Deny policy attached to user: \" %s \"\n" % user

    except ClientError as e:
            text_output = "Unexpected error: %s \n" % e

    return text_output



### Quarantine user - core method
def run_action(rule,entity,params):
    account_id = entity['accountNumber']
    policy_arn = "arn:aws:iam::" + account_id + ":policy/quarantine_deny_all_policy"
    user = entity['name']

    try:
        text_output = check_for_deny_policy(policy_arn)
        text_output = text_output + add_policy_to_user(user,policy_arn)
        
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e
    
    return text_output