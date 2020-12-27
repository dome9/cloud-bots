"""
## revoke_access_key
What it does: deactivate an IAM user access key
Usage : AUTO: revoke_access_key
Limitations: none

This bot is relevant to logic only and it's Running Following the CreateAccessKey event
"""

import boto3
from botocore.exceptions import ClientError
import bots_utils


EVENT_NAME = 'CreateAccessKey'

def run_action(boto_session, rule, entity, params):
    # create iam resource
    iam_resource = boto3.resource('iam')

    # look for the event in cloudtrail
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)

    # in case that the cloudtrail_event_lookup failed to find events
    if event is None:
        return "Error, returned 0 events"

    # take the access key details from the event
    access_key_id = [i for i in event['Resources'] if i['ResourceType'] == 'AWS::IAM::AccessKey'][0]['ResourceName']

    # take the user name
    username = event['Username']

    try:
        # create access key resource
        access_key = iam_resource.AccessKey(username, access_key_id)

        # revoke the access key
        access_key.deactivate()

        # create the text output
        return f'user: {username} access key with id : {access_key_id} was revoked'

    except ClientError as e:
        # in case of an unexpected error
        return f"Unexpected error: {e} \n"
