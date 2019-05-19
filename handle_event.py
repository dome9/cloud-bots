import re
import os
import boto3
import importlib
from botocore.exceptions import ClientError

account_mode = os.getenv('ACCOUNT_MODE', '')
cross_account_role_name = os.getenv('CROSS_ACCOUNT_ROLE_NAME', '')


def get_data_from_message(message):
    data = {}
    if message['rule'] and message['rule']['name']:
        data['rule_name'] = message['rule']['name']
    if message['status']:
        data['status'] = message['status']
    if message['entity']:
        data['entity_id'] = message['entity']['id']
        data['entity_name'] = message['entity']['name']
        data['region'] = message['entity']['region']
    # Some events come through with 'null' as the region. If so, default to us-east-1
    if data['region'] == None or data['region'] == "":
        data['region'] = 'us-east-1'
    else:
        data['region'] = data['region'].replace("_", "-")
    # All of the remediation values are coming in on the compliance tags and they're pipe delimited
    if message['rule']:
        if message['rule']['complianceTags']:
            data['compliance_tags'] = message['rule']['complianceTags'].split("|")
    return data


def handle_event(message, output_message):
    post_to_sns = True
    message_data = get_data_from_message(message)

    # evaluate the event and tags and decide is there's something to do with them.
    if message_data.get('status') == "Passed":
        output_message['Previously failing rule has been resolved'] = dict(rule=message_data.get('rule_name'),
                                                                           ID=message_data.get('entity_id'),
                                                                           Name=message_data.get('entity_name'))
        post_to_sns = False
        return post_to_sns

    # Check if any of the tags have AUTO: in them. If there's nothing to do at all, skip it.
    auto_pattern = re.compile("AUTO:")
    compliance_tags = message_data.get('compliance_tags')
    if not compliance_tags or not filter(auto_pattern.search, compliance_tags):
        output_message['Rule'] = "{} - Doesnt have any 'AUTO:' tags. Skipping.".format(message_data['rule_name'])
        post_to_sns = False
        return post_to_sns

    for tag in compliance_tags:
        tag = tag.strip()  # Sometimes the tags come through with trailing or leading spaces.

        # Check the tag to see if we have AUTO: in it
        pattern = re.compile("^AUTO:\s.+")
        if pattern.match(tag):
            output_message['Rule violation found'] = message_data.get('rule_name')
            output_message['ID'] = message_data.get('entity_id')
            output_message['Name'] = message_data.get('entity_name')
            output_message['Remediation'] = tag
            # Pull out only the bot verb to run as a function
            # The format is AUTO: bot_name param1 param2
            tag_pattern = tag.split(' ')
            if len(tag_pattern) < 2:
                output_message['Empty Auto'] = 'tag. No bot was specified'
                continue

            bot = tag_pattern[1]
            params = tag_pattern[2:]

            try:
                bot_module = importlib.import_module('bots.' + bot, package=None)
            except:
                print("Dome9 Cloud bots - handle_event.py - Error - could not find bot: {}".format(bot))
                output_message['Bot'] = "{} is not a known bot. skipping".format(bot)
                continue

            bot_msg = ""
            try:
                # Get the session info here. No point in waisting cycles running it up top if we aren't going to run an bot anyways:
                try:
                    # get the accountID
                    sts = boto3.client("sts")
                    lambda_account_id = sts.get_caller_identity()["Account"]

                except ClientError as e:
                    output_message['Unexpected STS error'] = e
                event_account_id = output_message['Account id']
                # Account mode will be set in the lambda variables. We'll default to single mdoe
                if lambda_account_id != event_account_id:  # The remediation needs to be done outside of this account
                    if account_mode == "multi":  # multi or single account mode?
                        # If it's not the same account, try to assume role to the new one
                        if cross_account_role_name:  # This allows users to set their own role name if they have a different naming convention they have to follow
                            role_arn = "arn:aws:iam::" + event_account_id + ":role/" + cross_account_role_name
                        else:
                            role_arn = "arn:aws:iam::" + event_account_id + ":role/Dome9CloudBots"

                        output_message['Compliance failure was found for an account outside of the one the function is running in. Trying to assume_role to target account'] = event_account_id

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
                                credentials_for_event = all_session_credentials[event_account_id] = assumedRoleObject[
                                    'Credentials']

                            except ClientError as e:
                                error = e.response['Error']['Code']
                                print("Dome9 Cloud bots - handle_event.py - Error - {}".format(e))
                                if error == 'AccessDenied':
                                    output_message['Access Denied'] = "Tried and failed to assume a role in the target account. Please verify that the cross account role is createad."
                                else:
                                    output_message['Unexpected error'] = e
                                continue

                        boto_session = boto3.Session(
                            region_name=message_data.get('region'),
                            aws_access_key_id=credentials_for_event['AccessKeyId'],
                            aws_secret_access_key=credentials_for_event['SecretAccessKey'],
                            aws_session_token=credentials_for_event['SessionToken']
                        )

                    else:
                        # In single account mode, we don't want to try to run bots outside of this one
                        output_message['Error'] = "This finding was found in account id {}. The Lambda function is running in account id: {}. Remediations need to be ran from the account there is the issue in.".format(event_account_id, lambda_account_id)
                        post_to_sns = False
                        return post_to_sns

                else:
                    # Boto will default to default session if we don't need assume_role credentials
                    boto_session = boto3.Session(region_name=message_data.get('region'))

                    ## Run the bot
                bot_msg = bot_module.run_action(boto_session, message['rule'], message['entity'], params)

            except Exception as e:
                bot_msg = "Error while executing function '{}'. Error: {}" (bot, e)
                print("Dome9 Cloud bots - handle_event.py - Error - {}".format(bot_msg))
            finally:
                output_message['Bot message'] = bot_msg

    # After the remediation functions finish, send the notification out.
    return post_to_sns
