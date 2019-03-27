import re
import os
import boto3
import importlib
from botocore.exceptions import ClientError

account_mode = os.getenv('ACCOUNT_MODE', '')
cross_account_role_name = os.getenv('CROSS_ACCOUNT_ROLE_NAME', '')


def handle_event(message, output):
    post_to_sns = True
    # Break out the values from the JSON payload from Dome9
    rule_name = message['rule']['name']
    status = message['status']
    entity_id = message['entity']['id']
    entity_name = message['entity']['name']
    region = message['entity']['region']

    # Some events come through with 'null' as the region. If so, default to us-east-1
    if not region:
        region = 'us-east-1'
    else:
        region = region.replace("_", "-")

    # Make sure that the event that's being refercenced is for the account this function is running in.
    event_account_id = message['account']['id']

    # All of the remediation values are coming in on the compliance tags and they're pipe delimited
    compliance_tags = message['rule']['complianceTags'].split("|")

    # evaluate the event and tags and decide is there's something to do with them. 
    if status == "Passed":
        output[rule_name] = "Previously failing rule has been resolved name"
        output[entity_id] = "Previously failing rule has been resolved name"
        output[entity_name] = "Previously failing rule has been resolved name"
        post_to_sns = False
        return output, post_to_sns

    # Check if any of the tags have AUTO: in them. If there's nothing to do at all, skip it. 
    auto_pattern = re.compile("AUTO:")
    if not auto_pattern.search(message['rule']['complianceTags']):
        output[rule_name] = "Rule Doesn't have any 'AUTO:' tags. Skipping."
        post_to_sns = False
        return output, post_to_sns

    for tag in compliance_tags:
        tag = tag.strip()  # Sometimes the tags come through with trailing or leading spaces. 

        # Check the tag to see if we have AUTO: in it
        pattern = re.compile("^AUTO:\s.+")
        if pattern.match(tag):
            output["Rule violation found"] = rule_name
            output["ID"] = entity_id
            output["name"] = entity_name
            output["tag"] = tag

            # Pull out only the bot verb to run as a function
            # The format is AUTO: bot_name param1 param2 so if len<2 no bot was mentioned
            arr = tag.split(' ')
            if len(arr) < 2:
                err_msg = "Empty AUTO: tag. No bot was specified"
                print(err_msg)
                # output.append(err_msg)
                output["Error"] = err_msg

                continue

            bot = arr[1]
            params = arr[2:]

            try:
                bot_module = importlib.import_module('bots.' + bot, package=None)
            except ImportError as error:
                print("Error: could not find bot: " + bot)
                output[bot] = "Bot: is not a known bot. Skipping"
                output["error"] = error.message

                continue

            print("Found bot {bot}, about to invoke it".format(bot=bot))
            bot_msg = ""
            try:
                # Get the session info here. No point in waisting cycles running it up top if we aren't going to run an bot anyways:
                try:
                    # get the accountID
                    sts = boto3.client("sts")
                    lambda_account_id = sts.get_caller_identity()["Account"]

                except ClientError as e:
                    output["Unexpected STS error"] = e

                # Account mode will be set in the lambda variables. We'll default to single mdoe
                if lambda_account_id != event_account_id:  # The remediation needs to be done outside of this account
                    if account_mode == "multi":  # multi or single account mode?
                        # If it's not the same account, try to assume role to the new one
                        if cross_account_role_name:  # This allows users to set their own role name if they have a different naming convention they have to follow
                            role_arn = "arn:aws:iam::" + event_account_id + ":role/" + cross_account_role_name
                        else:
                            role_arn = "arn:aws:iam::" + event_account_id + ":role/Dome9CloudBots"

                        output[event_account_id] = "Compliance failure was found for an account outside of the one the function is running in. Trying to assume_role to target account"
                        try:
                            credentials_for_event = globals()['all_session_credentials'][event_account_id]

                        except (NameError, KeyError):
                            # If we can't find the credentials, try to generate new ones

                            global all_session_credentials
                            all_session_credentials = {}
                            # create an STS client object that represents a live connection to the STS service
                            sts_client = boto3.client('sts')

                            # Call the assume_role method of the STSConnection object and pass the role ARN and a role session name.
                            try:
                                assumedRoleObject = sts_client.assume_role(
                                    RoleArn=role_arn,
                                    RoleSessionName="CloudBotsAutoRemedation"
                                )
                                # From the response that contains the assumed role, get the temporary credentials that can be used to make subsequent API calls
                                credentials_for_event = all_session_credentials[event_account_id] = assumedRoleObject['Credentials']

                            except ClientError as e:
                                error = e.response['Error']['Code']
                                print(e)
                                if error == 'AccessDenied':
                                    output["Error AccessDenied"] = "Tried and failed to assume a role in the target account. Please verify that the cross account role is createad"
                                else:
                                    output["Unexpected error"] = e
                                continue

                        boto_session = boto3.Session(
                            region_name=region,
                            aws_access_key_id=credentials_for_event['AccessKeyId'],
                            aws_secret_access_key=credentials_for_event['SecretAccessKey'],
                            aws_session_token=credentials_for_event['SessionToken']
                        )

                    else:
                        # In single account mode, we don't want to try to run bots outside of this one
                        post_to_sns = False
                        return output, post_to_sns

                else:
                    # Boto will default to default session if we don't need assume_role credentials
                    boto_session = boto3.Session(region_name=region)

                    ## Run the bot
                bot_msg = bot_module.run_action(boto_session, message['rule'], message['entity'], params)

            except Exception as e:
                bot_msg = "Error while executing function {bot}. Error: {error} ".format(bot=bot, error=e)
                print(bot_msg)
            finally:
                output["Bot message"] = bot_msg


    # After the remediation functions finish, send the notification out. 
    return output, post_to_sns
