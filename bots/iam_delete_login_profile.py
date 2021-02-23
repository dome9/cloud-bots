"""
## iam_delete_login_profile
What it does: Delete an IAM user login profile (disable Console Login)
Usage : AUTO: iam_delete_login_profile
Limitations: none

This bot is relevant to logic only and it's Running Following the SignInLogs event
"""

import boto3
from botocore.exceptions import ClientError
import bots_utils

EVENT_NAME = 'ConsoleLogin'

def run_action(boto_session, rule, entity, params):
    # create iam client
    iam_client = boto3.client('iam')

    # look for event in cloudtrail
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)

    # in case that the cloudtrail_event_lookup failed to find events
    if event is None:
        return "Error when looking for the CreateAccessKey event, 0 events returned"

    # take the user name
    username = event['Username']

    try:
        # delete the access key
        iam_client.delete_login_profile(
            UserName=username
        )
        # create the text output
        return f'user: {username} login profile was deleted - Console Login disabled'

    except ClientError as e:
        # in case of an unexpected error
        return f'Unexpected error: {e}'
