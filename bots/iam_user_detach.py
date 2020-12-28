'''
## iam_user_detach
Log.ic bot only
What it does: Detaches an IAM user from an IAM group.
Usage: AUTO: iam_user_detach
Limitations: The bot will stop running if the proper 'AddUserToGroup' event is not found
             The bot will not notify if the IAM user is already detached or was not attached to the group in the
                 first place.
'''

import boto3
import botocore.exceptions
import json
import bots_utils


EVENT_NAME = 'AddUserToGroup'


def run_action(boto_session, rule, entity, params):
    text_output = ''
    user_to_remove = entity.get('name')

    # Get event from cloud trail
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME,
                                               resource_name_to_filter=user_to_remove)
    if not event:
        # If valid event was not found - bot will not run
        text_output = f'Error: No matching {EVENT_NAME} events were found in cloud trail. Bot wasn\'t executed.'
    
    else:
        # If there is a valid event - get relevant details from it
        try: 
            group_name = get_details_from_event(event)
        except:
            text_output = f'Error while parsing {EVENT_NAME} event. Bot wasn\'t executed.'
        else:
            # If event parsing was successful - remove user from grou
            text_output = remove_user_from_group(boto_session, user_to_remove, group_name)

    return text_output


def remove_user_from_group(boto_session, user_to_remove, group_name):
    iam_client = boto_session.client('iam')
    try:
        # Remove the IAM user from the IAM group
        iam_client.remove_user_from_group(GroupName=group_name, UserName=user_to_remove)
    except botocore.exceptions.ClientError as e:
        return f'Client error: {e} \n'
    else:
        return f'Success: The user: {user_to_remove} was successfully detached from the group: {group_name}'


def get_details_from_event(event):
    return json.loads(event['CloudTrailEvent'])['requestParameters']['groupName']

