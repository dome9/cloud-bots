'''
## iam_user_deactivate_unused_access_key
What it does: deactivate unused access key that haven't been in use for some time
Usage: iam_user_deactivate_unused_access_key <number of days>
Example: iam_user_inactivate_unused_access_key 90
Limitations: default time is 90 days, if there are more then 200 access keys for user should increase maxItems
'''

import boto3
from botocore.exceptions import ClientError
from datetime import datetime

MAX_ITEMS = 200

"""
calc how many days passed from access key's last use 
"""


def get_passed_days_from_last_use(access_key, iam_client):
    # get current time and date for comparision
    curr_time = datetime.now()

    access_key_id = access_key['AccessKeyId']
    # get the acces key last used data
    access_key_last_use = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)['AccessKeyLastUsed']

    # check if the access key is ever been used , if it isn't , considers create date
    if 'LastUsedDate' in access_key_last_use:
        # ignore time zone (doesnt effect in the matter of days )
        return (curr_time - access_key_last_use['LastUsedDate'].replace(tzinfo=None)).days
    else:
        # check how much time since the key created and is not used
        # ignore time zone (doesnt effect in the matter of days )
        return (curr_time - access_key['CreateDate'].replace(tzinfo=None)).days


def run_action(boto_session, rule, entity, params):
    text_output = 'Start iam_user_inactivate_unused_access_key'
    username = entity['name']
    # default days is 90
    max_days_unused_time = params[0] if params else 90
    # Create an IAM client
    iam_client = boto3.client('iam')

    # -----------------------  Deactivate unused access keys ----------------------------------#
    try:
        # get all access keys
        access_keys = iam_client.list_access_keys(UserName=username, MaxItems=MAX_ITEMS)['AccessKeyMetadata']

        for access_key in access_keys:
            # get access key id
            access_key_id = access_key['AccessKeyId']
            # calc how many days passed from access key's last use
            passed_days_from_last_use = get_passed_days_from_last_use(access_key, iam_client)
            # if the access key is not used for more than 90 days it will be turn inactive
            if passed_days_from_last_use > max_days_unused_time:
                # make key inactive
                iam_client.update_access_key(
                    UserName=username,
                    AccessKeyId=access_key_id,
                    Status='Inactive'
                )
                text_output = text_output + f'Iam user: {username} access key with id : {access_key_id} was deactivated' \
                                            f'due of being unused for {passed_days_from_last_use} days '

    except ClientError as e:
        text_output = text_output + f'Unexpected error: {e}.'

    return text_output
