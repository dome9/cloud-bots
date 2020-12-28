"""
## iam_delete_access_key
What it does: Delete an IAM user access key
Usage : AUTO: iam_delete_access_key
Limitations: none

This bot is relevant to logic only and it's Running Following the CreateAccessKey event
"""

import boto3
from botocore.exceptions import ClientError
import bots_utils

EVENT_NAME = 'CreateAccessKey'

def run_action(boto_session, rule, entity, params):
    # create iam client
    iam_client = boto3.client('iam')

    # look for event in cloudtrail
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)

    # in case that the cloudtrail_event_lookup failed to find events
    if event is None:
        return "Error when looking for the CreateAccessKey event, 0 events returned"

    # take the access key details from the event
    access_key_id = [i for i in event['Resources'] if i['ResourceType'] == 'AWS::IAM::AccessKey'][0]['ResourceName']

    # take the user name
    username = event['Username']

    try:
        # delete the access key
        iam_client.delete_access_key(
            UserName=username,
            AccessKeyId=access_key_id
        )
        # create the text output
        return f'user: {username} access key with id : {access_key_id} was deleted'

    except ClientError as e:
        # in case of an unexpected error
        return f"Unexpected error: {e} \n"
