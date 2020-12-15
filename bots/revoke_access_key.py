"""
## revoke_access_key
What is does: deactivate an IAM user access key
Usage : AUTO: revoke_access_key
Limitations: none
"""

import boto3
from botocore.exceptions import ClientError
import bots_utils


EVENT_NAME = 'CreateAccessKey'

def run_action(boto_session, rule, entity, params):
    # create iam resource
    iam_resource = boto_session.resource('iam')

    # get the event time from the entity
    event_time = entity['eventTime']

    # format the time from string to datetime object
    event_time = format_time(event_time)

    # look for the event in cloudtrail
    event = cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)

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
        text_output = f'user: {username} access key with id : {access_key_id} was revoked'

    except ClientError as e:
        # in case of an unexpected error
        return "Unexpected error: %s \n" % e

    return text_output
