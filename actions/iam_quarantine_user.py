import boto3
import json
import os
from botocore.exceptions import ClientError

#This will make the quarantining IAM policy that'll be applied to the users or roles that need to be locked down.
def create_deny_policy(event_log):
	# Create IAM client
	iam = boto3.client('iam')

	try:
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
			event_log.append("Unexpected error: %s" % create_policy_response + "\n")
		else:
			event_log.append("IAM deny-all policy successfully created.\n")	

	except (ClientError) as e:
		event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)

#Poll the account and check if the quarantine_deny_all policy exists. If not - make it
def check_for_deny_policy(policy_arn,event_log):
	# Create IAM client
	iam = boto3.client('iam')

	try:
		#Check to see if the deny policy exists in the account currently
		get_policy_response = iam.get_policy(PolicyArn=policy_arn)
		
		if get_policy_response['ResponseMetadata']['HTTPStatusCode'] < 400:
			event_log.append ("IAM deny-all policy exists in this account.\n")

	except (ClientError) as e:
		error = e.response['Error']['Code']
		if error == 'NoSuchEntity':
			#If the policy isn't there - add it into the account
			event_log = create_deny_policy(event_log)
		else:
			event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)

#Create the deny group that we'll add the deny policy and offending users to
def create_IAM_group(event_log):
	# Create IAM client
	iam = boto3.client('iam')

	try:
		#If the group isn't there - add it into the account and attach the policy to it.
		create_group_response = iam.create_group(GroupName='quarantine_user_deny_all_group')
		event_log.append("IAM Group (quarantine_user_deny_all_group) successfully created\n")

	except (ClientError) as e:
		error = e.response['Error']['Code']
		if error == 'entityAlredyExists':
			event_log.append("Group already exists.\n")
		else:
			event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)

#Check for an IAM group that we can attach our deny policy to. Create one if it's not there already
def check_for_deny_group(event_log):
	# Create IAM client
	iam = boto3.client('iam')

	try:
		#Check to see if the deny group exists in the account currently
		event_log.append("Checking to see if group quarantine_user_deny_all_group exists in this account.\n")
		get_group_response = iam.get_group(GroupName='quarantine_user_deny_all_group')
		event_log.append ("Deny-all group exists in this account.\n")

	except (ClientError, AttributeError) as e:
		error = e.response['Error']['Code']
		if error == 'NoSuchEntity':
			event_log.append("Deny-all group not found. Creating.\n")
			event_log = create_IAM_group(event_log)
		else:
			event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)

#Attach the deny policy to the deny group
def attach_policy_to_group(policy_arn,event_log):
	# Create IAM client
	iam = boto3.client('iam')

	try:
		attach_policy_response = iam.attach_group_policy(
		    GroupName='quarantine_user_deny_all_group',
		    PolicyArn=policy_arn
		)
		event_log.append ("Attached policy " + policy_arn + " to quarantine_user_deny_all_group.\n")

	except (ClientError) as e:
		event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)


#Attach the user to the deny group
def add_user_to_group(user,event_log):
	# Create IAM client
	iam = boto3.client('iam')

	try:
		attach_policy_response = iam.add_user_to_group(
		    GroupName='quarantine_user_deny_all_group',
		    UserName=user
		)
		event_log.append ("User \"" + user + "\" attached to quarantine_user_deny_all_group.\n")

	except (ClientError, AttributeError) as e:
		event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)

### Quarantine user - core method
def main(message,event_log,):
	account_id = message['Account']['Id']
	policy_arn = "arn:aws:iam::" + account_id + ":policy/quarantine_deny_all_policy"

	user = message['Entity']['Name']

	try:
		check_for_deny_policy(policy_arn,event_log)
		check_for_deny_group(event_log)
		attach_policy_to_group(policy_arn,event_log)
		add_user_to_group(user,event_log)

	except (ClientError, AttributeError) as e:
		event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)

