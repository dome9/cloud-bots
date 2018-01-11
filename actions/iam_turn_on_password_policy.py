import boto3
import json
import os
import re
from botocore.exceptions import ClientError

#This will make the quarantining IAM policy that'll be applied to the users or roles that need to be locked down.
#EVERYTHING needs to be set at once. If you just set 1 property, it kills everything else off. 

'''
Sample PasswordPolicy:
{
   MinimumPasswordLength=int,
   RequireSymbols=True|False,
   RequireNumbers=True|False,
   RequireUppercaseCharacters=True|False,
   RequireLowercaseCharacters=True|False,
   AllowUsersToChangePassword=True|False,
   MaxPasswordAge=int,
   PasswordReusePrevention=int,
   HardExpiry=True|False
}

Sample tag: AUTO: iam_turn_on_password_policy (MinimumPasswordLength:5,RequireSymbols:True,RequireNumbers:True,RequireUppercaseCharacters:True,RequireLowercaseCharacters:True,AllowUsersToChangePassword:True,MaxPasswordAge:5,PasswordReusePrevention:5,HardExpiry:True)
'''
# Create IAM client
iam = boto3.client('iam')


def run_action(message):
	compliance_tags = message['Rule']['ComplianceTags'].split("|")

	#pull the tags and make sure to just take action on the one that matches the action we want
	for tag in compliance_tags:
		tag = tag.strip() #Sometimes the tags come through with trailing or leading spaces. 
		all_actions = re.match(r'AUTO:\siam_turn_on_password_policy\s\((?P<actions>.+)\)', tag) #we just want the tag that matches "AUTO: iam_turn_on_password_policy (actions)"

		#if we do have a tag that matches our requrements
		if all_actions:
			actions = all_actions.group(1)
			actions = actions.split(",") #take the list of password policies and turn it into an array
			action_values = []

			for action in actions:
				key_value = action.split(":") 
				property_to_update = key_value[0]
				value = key_value[1]
				#classify the values into int or bool depending on what is needed.
				if property_to_update in ("MinimumPasswordLength", "MaxPasswordAge", "PasswordReusePrevention"):
					value = int(value)
				else:
					if value == 'True':
						value = True
					elif value == 'False':
						value = False
				action_values.append(value)				

			if len(action_values) == 8:	#We need to make sure we have the exact amount of values for all of these properties
				try:
					response = iam.update_account_password_policy(
					    MinimumPasswordLength=action_values[0],
					    RequireSymbols=action_values[1],
					    RequireNumbers=action_values[2],
					    RequireUppercaseCharacters=action_values[3],
					    RequireLowercaseCharacters=action_values[4],
					    AllowUsersToChangePassword=action_values[5],
					    MaxPasswordAge=action_values[6],
					    PasswordReusePrevention=action_values[7],
					    HardExpiry=action_values[8]
					)

					responseCode = response['ResponseMetadata']['HTTPStatusCode']

					if responseCode >= 400:
					 	text_output = "Unexpected error:" + str(response) + "\n"
					else:
					 	text_output = "Account Password Policy updated successfully \n"	


				except ClientError as e:
					text_output = "Unexpected error: %s" % e + "\n"
			
			else:
				text_output = "Array length is less than 8. Are you sure ALL passwort policy properties were set?\n MinimumPasswordLength=int, \nRequireSymbols=True|False, \nRequireNumbers=True|False, \nRequireUppercaseCharacters=True|False, \nRequireLowercaseCharacters=True|False, \nAllowUsersToChangePassword=True|False, \nMaxPasswordAge=int, \nPasswordReusePrevention=int, \nHardExpiry=True|False \n"

	return text_output
