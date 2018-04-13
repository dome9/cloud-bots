import re
import os
import boto3
import importlib 
from botocore.exceptions import ClientError

account_mode = os.getenv('ACCOUNT_MODE','')
cross_account_role_name = os.getenv('CROSS_ACCOUNT_ROLE_NAME','')

def handle_event(message,text_output_array):
    post_to_sns = True
    #Break out the values from the JSON payload from Dome9
    rule_name = message['rule']['name']
    status = message['status']
    entity_id = message['entity']['id']
    entity_name = message['entity']['name']
    region = message['entity']['region']
    
    # Some events come through with 'null' as the region. If so, default to us-east-1
    if region != None:
        region = region.replace("_","-")
    else:
        region = 'us-east-1'

    #Make sure that the event that's being referenced is for the account this function is running in.
    event_account_id = message['account']['id']

    #All of the remediation values are coming in on the compliance tags and they're pipe delimited
    compliance_tags = message['rule']['complianceTags'].split("|")

    #evaluate the event and tags and decide is there's something to do with them. 
    if status == "Passed":
        text_output_array.append("Previously failing rule has been resolved: %s \n ID: %s \nName: %s \n" % (rule_name, entity_id, entity_name))
        post_to_sns = False
        return text_output_array,post_to_sns

    #Check if any of the tags have AUTO: in them. If there's nothing to do at all, skip it. 
    auto_pattern = re.compile("AUTO:")
    if not auto_pattern.search(message['rule']['complianceTags']):
        text_output_array.append("Rule %s \n Doesn't have any 'AUTO:' tags. \nSkipping.\n" % rule_name)
        post_to_sns = False
        return text_output_array,post_to_sns

    for tag in compliance_tags:
        tag = tag.strip() #Sometimes the tags come through with trailing or leading spaces. 

        #Check the tag to see if we have AUTO: in it
        pattern = re.compile("^AUTO:\s.+")
        if pattern.match(tag):
            text_output_array.append("Rule violation found: %s \nID: %s | Name: %s \nRemediation Bot: %s \n" % (rule_name, entity_id, entity_name, tag))

            # Pull out only the bot verb to run as a function
            # The format is AUTO: bot_name param1 param2
            arr = tag.split(' ')
            if len(arr) < 2:
                err_msg = "Empty AUTO: tag. No bot was specified"
                print(err_msg)
                text_output_array.append(err_msg)
                continue
            
            bot = arr[1]
            params = arr[2:]

            try:
                bot_module = importlib.import_module('bots.' + bot, package=None)
            except:
                print("Error: could not find bot: " + bot)
                text_output_array.append("Bot: %s is not a known bot. Skipping.\n" % bot)
                continue
            
            print("Found bot '%s', about to invoke it" % bot)
            bot_msg = ""
            try:
                # Get the session info here. No point in waisting cycles running it up top if we aren't going to run an bot anyways:
                try:
                    #get the accountID
                    sts = boto3.client("sts")
                    lambda_account_id = sts.get_caller_identity()["Account"]

                except ClientError as e:
                    text_output_array.append("Unexpected STS error: %s \n"  % e)


                #Account mode will be set in the lambda variables. We'll default to single mdoe 
                if lambda_account_id != event_account_id: #The remediation needs to be done outside of this account
                    if account_mode == "multi": #multi or single account mode?
                        #If it's not the same account, try to assume role to the new one
                        if cross_account_role_name: # This allows users to set their own role name if they have a different naming convention they have to follow
                            role_arn = "arn:aws:iam::" + event_account_id + ":role/" + cross_account_role_name
                        else:
                            role_arn = "arn:aws:iam::" + event_account_id + ":role/dome9-auto-remediations"

                        text_output_array.append("Compliance failure was found for an account outside of the one the function is running in. Trying to assume_role to target account %s .\n" % event_account_id) 

                        try:
                            credentials_for_event = globals()['all_session_credentials'][event_account_id]
                            text_output_array.append("Found existing credentials to use from still warm lambda functions. Skipping another STS assume role\n")        

                        except (NameError,KeyError):
                            #If we can't find the credentials, try to generate new ones
                            text_output_array.append("Session credentials weren't found cached in the function. Trying to generate new ones.\n")

                            global all_session_credentials
                            all_session_credentials = {}
                            # create an STS client object that represents a live connection to the STS service
                            sts_client = boto3.client('sts')
                            
                            # Call the assume_role method of the STSConnection object and pass the role ARN and a role session name.
                            try:
                                assumedRoleObject = sts_client.assume_role(
                                    RoleArn=role_arn,
                                    RoleSessionName="CloudSupervisorAutoRemedation"
                                    )
                                # From the response that contains the assumed role, get the temporary credentials that can be used to make subsequent API calls
                                credentials_for_event = all_session_credentials[event_account_id] = assumedRoleObject['Credentials']

                            except ClientError as e:
                                error = e.response['Error']['Code']
                                print(e)
                                if error == 'AccessDenied':
                                    text_output_array.append("Tried and failed to assume a role in the target account. Please verify that the cross account role is createad. \n")
                                    continue                          

                        boto_session = boto3.Session(
                            region_name=region,         
                            aws_access_key_id = credentials_for_event['AccessKeyId'],
                            aws_secret_access_key = credentials_for_event['SecretAccessKey'],
                            aws_session_token = credentials_for_event['SessionToken']
                            )

                    else:
                        # In single account mode, we don't want to try to run bots outside of this one
                        text_output_array.append("Error: This finding was found in account id %s. The Lambda function is running in account id: %s. Remediations need to be ran from the account there is the issue in.\n" % (event_account_id, lambda_account_id))
                        post_to_sns = False
                        return text_output_array,post_to_sns

                else:
                    #Boto will default to default session if we don't need assume_role credentials
                    boto_session = boto3.Session(region_name=region)                     

                ## Run the bot
                bot_msg = bot_module.run_bot(boto_session,message['rule'],message['entity'],params)

            except Exception as e: 
                bot_msg = "Error while executing function '%s'.\n Error: %s \n" % (bot,e)
                print(bot_msg)
            finally:
                text_output_array.append(bot_msg)

    #After the remediation functions finish, send the notification out. 
    return text_output_array,post_to_sns
