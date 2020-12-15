"""
## delete_access_key
What is does: Delete an IAM user access key
Usage : AUTO: delete_access_key
Limitations: none
"""

import boto3
from botocore.exceptions import ClientError
import bots_utils

EVENT_NAME = 'CreateAccessKey'
DEFAULT_CLOUDTRAIL_LOOKUP_TIME_DIFF=5


def run_action(boto_session, rule, entity, params):
    # create iam resource
    iam_resource = boto3.resource('iam')

    # get the event time from the entity
    event_time = entity['eventTime']

    # look for event in cloudtrail
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)

    # take the access key details from the event
    access_key_id = [i for i in event['Resources'] if i['ResourceType'] == 'AWS::IAM::AccessKey'][0]['ResourceName']

    # take the user name
    username = event['Username']

    # create access key resource
    access_key = iam_resource.AccessKey(username, access_key_id)

    try:
        # delete the access key
        access_key.delete()
        # create the text output
        text_output = f'user: {username} access key with id : {access_key_id} was deleted'

    except ClientError as e:
        # in case of an unexpected error
        return "Unexpected error: %s \n" % e

    return text_output

