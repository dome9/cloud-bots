import glob
import re
import boto3
import importlib 
from importlib import util
from botocore.exceptions import ClientError


def filter_events(message,text_output_array):

	#Break out the values from the JSON payload from Dome9
	rule_name = message['Rule']['Name']
	status = message['Status']
	entity_id = message['Entity']['Id']
	entity_name = message['Entity']['Name']

	#Make sure that the event that's being referenced is for the account this function is running in.
	compliance_account_id = message['Account']['Id']
	try:
		#get the accountID
		sts = boto3.client("sts")
		account_id = sts.get_caller_identity()["Account"]
	except (ClientError, AttributeError) as e:
		text_output_array.append("Unexpected STS error: %s" % e + "\n")

	if account_id != compliance_account_id:
		text_output_array.append("Error: This rule was found for account id %s. This function is running in account id: %s. Remediations need to be ran from the account there is the issue in.\n" % (account_id, compliance_account_id))
		return text_output_array
	else:
		print("Account IDs match - continuing to check for remediations to do")


	#All of the remediation values are coming in on the compliance tags and they're pipe delimited
	compliance_tags = message['Rule']['ComplianceTags'].split("|")

	#evaluate the event and tags and decide is there's something to do with them. 
	if status == "Passed":
		text_output_array.append("Previously failing rule has been resolved: %s \n ID: %s \nName: %s \n" % (rule_name, entity_id, entity_name)) 
	else:
		for tag in compliance_tags:
			tag = tag.strip() #Sometimes the tags come through with trailing or leading spaces. 

			#Check the tag to see if we have AUTO: in it
			pattern = re.compile("^AUTO:\s.+")
			if pattern.match(tag):
				text_output_array.append("Rule violation found: %s \nID: %s | Name: %s \nRemediation Action: %s \n" % (rule_name, entity_id, entity_name, tag))

				#Pull out only the action verb to run as a function
				action_regex_match = re.match(r'AUTO:\s(?P<action>\w+)', tag)
				action = action_regex_match.group(1)

				#Check if the action we're trying to do, is a file in actions/. 
				#This needs to match the filename for the action in actions/
				#We could try to run this every time and catch the error, but it fails hard and the import isn't fast. This should be more efficient. 
				file_name = "actions/" + action + ".py"
				modules = glob.glob('actions/*.py')

				if file_name in modules:
					#from Importlib. Dynamically import the file/module

					##########
					### In the below line - "" can be replaced with "<anything>" and it works but it can't be removed. Probably needs to be cleaned up.
					##########
					spec = util.spec_from_file_location("", file_name) #ModuleSpec(name='run_action', loader=<_frozen_importlib_external.SourceFileLoader object at 0x101383f28>, origin='actions/sg_delete.py')
					action_file = importlib.util.module_from_spec(spec) #<module 'run_action' from 'actions/sg_delete.py'>
					spec.loader.exec_module(action_file) #load the module

					try: 
						action_output = action_file.run_action(message) #This is where we leave filtering and end up in the actual actions
						text_output_array.append(action_output)

					except AttributeError as e: # Probably need to clean this up for a different/better error handling
						text_output_array.append("Unexpected error: Can't find run_action module in %s \n" % (file_name))	
				else:
					text_output_array.append("Action: " + action + " is not a known action. Skipping.\n")

			else:
				print("Tag detected: " + tag + " Doesn't say AUTO. Skipping.")  


	#After the remediation functions finish, send the notification out. 
	return text_output_array