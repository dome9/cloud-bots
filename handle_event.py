# import glob
import re
import boto3
import importlib 
# from importlib import util
from botocore.exceptions import ClientError


def handle_event(message,text_output_array):

    #Break out the values from the JSON payload from Dome9
    rule_name = message['Rule']['Name']
    status = message['Status']
    entity_id = message['Entity']['Id']
    entity_name = message['Entity']['Name']

    #Make sure that the event that's being referenced is for the account this function is running in.
    event_account_id = message['Account']['Id']
    try:
        #get the accountID
        sts = boto3.client("sts")
        lambda_account_id = sts.get_caller_identity()["Account"]
    except (ClientError, AttributeError) as e:
        text_output_array.append("Unexpected STS error: %s" % e + "\n")

    if lambda_account_id != event_account_id:
        text_output_array.append("Error: This finding was found in account id %s. The Lambda function is running in account id: %s. Remediations need to be ran from the account there is the issue in.\n" % (event_account_id, lambda_account_id))
        return text_output_array
    
    #All of the remediation values are coming in on the compliance tags and they're pipe delimited
    compliance_tags = message['Rule']['ComplianceTags'].split("|")

    #evaluate the event and tags and decide is there's something to do with them. 
    if status == "Passed":
        text_output_array.append("Previously failing rule has been resolved: %s \n ID: %s \nName: %s \n" % (rule_name, entity_id, entity_name))
        return text_output_array

    for tag in compliance_tags:
        tag = tag.strip() #Sometimes the tags come through with trailing or leading spaces. 

        #Check the tag to see if we have AUTO: in it
        pattern = re.compile("^AUTO:\s.+")
        if pattern.match(tag):
            text_output_array.append("Rule violation found: %s \nID: %s | Name: %s \nRemediation Action: %s \n" % (rule_name, entity_id, entity_name, tag))

            # Pull out only the action verb to run as a function
            # The format is AUTO: action name param1 param2
            arr = tag.split(' ')
            if len(arr) < 2:
                err_msg = "Empty AUTO: tag. No action was specified"
                print(err_msg)
                text_output_array.append(err_msg)
                continue
            
            action = arr[1]
            params = arr[2:]

            # action_regex_match = re.match(r'AUTO:\s(?P<action>\w+)', tag)
            # action = action_regex_match.group(1)
            
            try:
                action_module = importlib.import_module('actions.' + action, package=None)
            except:
                print("Error: could not find action: " + action)
                text_output_array.append("Action: %s is not a known action. Skipping.\n" % action)
                continue
            
            print("Found action '%s', about to invoke it" % action)
            action_msg = ""
            try:
                action_msg = action_module.run_action(message['Rule'],message['Entity'], params)
            except Exception as e: 
                action_msg = "Error while executing function '%s'. Ex=%s \n" % (action,e)
                print(action_msg)
            finally:
                text_output_array.append(action_msg)

    #After the remediation functions finish, send the notification out. 
    return text_output_array