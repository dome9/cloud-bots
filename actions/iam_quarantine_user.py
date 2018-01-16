import boto3
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
    result = iam.create_policy(
        PolicyName='quarantine_deny_all_policy',
        PolicyDocument=json.dumps(deny_policy)
    )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % result
    else:
        text_output = "IAM deny-all policy successfully created.\n"

    return text_output

#Poll the account and check if the quarantine_deny_all policy exists. If not - make it
def check_for_deny_policy(policy_arn):
    # Create IAM client
    iam = boto3.client('iam')

    try:
        #Check to see if the deny policy exists in the account currently
        result = iam.get_policy(PolicyArn=policy_arn)
        
        if result['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output =  "IAM deny-all policy exists in this account.\n"

    except (ClientError) as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            #If the policy isn't there - add it into the account
            text_output = create_deny_policy()
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output

#Create the deny group that we'll add the deny policy and offending users to
def create_IAM_group():
    # Create IAM client
    iam = boto3.client('iam')

    try:
        #If the group isn't there - add it into the account and attach the policy to it.
        result = iam.create_group(GroupName='quarantine_user_deny_all_group')
        text_output = "IAM Group (quarantine_user_deny_all_group) successfully created\n"

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'entityAlredyExists':
            text_output = "Group already exists.\n"
        else:
            text_output = "Unexpected error: %s \n" % (e)

    return text_output

#Check for an IAM group that we can attach our deny policy to. Create one if it's not there already
def check_for_deny_group():
    # Create IAM client
    iam = boto3.client('iam')

    try:
        #Check to see if the deny group exists in the account currently
        text_output = "Checking to see if group quarantine_user_deny_all_group exists in this account.\n"
        result = iam.get_group(GroupName='quarantine_user_deny_all_group')
        text_output =  text_output + "Deny-all group exists in this account.\n"

    except (ClientError, AttributeError) as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            text_output = "Deny-all group not found. Creating.\n"
            event_log = create_IAM_group(event_log)
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output

#Attach the deny policy to the deny group
def attach_policy_to_group(policy_arn):
    # Create IAM client
    iam = boto3.client('iam')

    attach_policy_response = iam.attach_group_policy(
        GroupName='quarantine_user_deny_all_group',
        PolicyArn=policy_arn
    )
    text_output =  "Attached policy %s to quarantine_user_deny_all_group.\n" % policy_arn

    return text_output


#Attach the user to the deny group
def add_user_to_group(user):
    # Create IAM client
    iam = boto3.client('iam')

    attach_policy_response = iam.add_user_to_group(
        GroupName='quarantine_user_deny_all_group',
        UserName=user
    )
    text_output =  "User \" %s \" attached to quarantine_user_deny_all_group.\n" % user

    return text_output

### Quarantine user - core method
def run_action(rule,entity,params):
    account_id = entity['AccountNumber']
    policy_arn = "arn:aws:iam::" + account_id + ":policy/quarantine_deny_all_policy"
    user = entity['Name']

    try:
        text_output = check_for_deny_policy(policy_arn)
        text_output = text output + check_for_deny_group()
        text_output = text output + attach_policy_to_group(policy_arn)
        text_output = text output + add_user_to_group(user)

    except (ClientError, AttributeError) as e:
        text_output = "Unexpected error: %s \n" % (e)

    return text_output

