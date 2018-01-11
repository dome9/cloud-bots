import glob
import re
import boto3
import importlib 
from importlib import util
from botocore.exceptions import ClientError


def filter_events(message,event_log):

	### Dynamically load all remediations in actions.py
	# Get file paths of all modules.
	modules = glob.glob('actions/*.py')

	# Dynamically load those modules here.
	for file_name in modules:
		#rename main functions to "main"
		spec = util.spec_from_file_location("main", file_name)

		#Strip off the file names to give us just the action names we want to run
		action_name = file_name.replace("actions/","")
		action_name = action_name.replace(".py","")

		action = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(action)
		globals()[action_name] = action


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
		event_log.append("Unexpected STS error: %s" % e + "\n")

	if account_id != compliance_account_id:
		event_log.append("Error: This rule was found for account id %s. This function is running in account id: %s. Remediations need to be ran from the account there is the issue in.\n" % (account_id, compliance_account_id))
		return(event_log)
	else:
		print("Account IDs match - continuing to check for remediations to do")

	#All of the remediation values are coming in on the compliance tags and they're pipe delimited
	compliance_tags = message['Rule']['ComplianceTags'].split("|")

	#evaluate the event and tags and decide is there's something to do with them. 
	if status == "Passed":
		event_log.append("Previously failing rule has been resolved: %s \n ID: %s \nName: %s \n" % (rule_name, entity_id, entity_name)) 
	else:
		for tag in compliance_tags:
			tag = tag.strip() #Sometimes the tags come through with trailing or leading spaces. 

			#check the tag to see if we have AUTO: in it
			pattern = re.compile("^AUTO:\s.+")
			if pattern.match(tag):
				#Pull out only the action verb to run as a function
				m = re.match(r'AUTO:\s(?P<action>\w+)', tag)
				action = m.group(1)
				#run the method
				possibles = globals().copy()
				possibles.update(locals())
				method = possibles.get(action)
				event_log.append("Rule violation found: %s \nID: %s | Name: %s \nRemediation Action: %s \n" % (rule_name, entity_id, entity_name, action))
				
				if method:
					event_log = method.run_action(message,event_log)	
				#Getting blank messages if auto matches. Clean up this else to stop sending things if nothing to do
				else:
					event_log.append("Action: " + action + " is not a known action. Skipping.\n")

			else:
				print("Tag detected: " + tag + " Doesn't say AUTO. Skipping.")  


	#After the remediation functions finish, send the notification out. 
	return(event_log)