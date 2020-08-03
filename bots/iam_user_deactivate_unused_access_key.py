'''
## iam_user_deactivate_unused_access_key
What it does: deactivate unused access key that haven't been in use for some time
Usage: iam_user_deactivate_unused_access_key <number of days>
Examples: iam_user_inactivate_unused_access_key 90
Limitations: default time is 90 days, if there are more then 200 access keys for user should increase maxItems
'''

import boto3
from botocore.exceptions import ClientError
from datetime import datetime

MAX_ITEMS = 200


def run_action(boto_session, rule, entity, params):
    text_output = 'Start iam_user_inactivate_unused_access_key'
    username = entity['name']
    max_days_unused_time = params[0] if params else 90
    # Create an IAM client
    iam_client = boto3.client('iam')
    # get current time and date for comparision
    curr_time = datetime.now()

    # -----------------------  Deactivate unused access keys ----------------------------------#
    try:
        access_keys = iam_client.list_access_keys(UserName=username, MaxItems=MAX_ITEMS)['AccessKeyMetadata']

        for access_key in access_keys:
            access_key_id = access_key['AccessKeyId']
            access_key_last_use = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)['AccessKeyLastUsed']
            if 'LastUsedDate' in access_key_last_use:  # check if the access key is ever been used
                # ignore time zone (doesnt effect in the matter of days )
                passed_days_from_last_use = curr_time - access_key_last_use['LastUsedDate'].replace(tzinfo=None)
            else:
                # check how much time since the key created and is not used
                # ignore time zone (doesnt effect in the matter of days )
                passed_days_from_last_use = curr_time - access_key['CreateDate'].replace(tzinfo=None)

            if passed_days_from_last_use.days > max_days_unused_time:
                # make key inactive
                iam_client.update_access_key(
                    UserName=username,
                    AccessKeyId=access_key_id,
                    Status='Inactive'
                )
                text_output = text_output + f'Iam user: {username} access key with id : {access_key_id} was deactivated' \
                                            f'due of being unused for {passed_days_from_last_use.days} days '

    except ClientError as e:
        text_output = text_output + f'Unexpected error: {e}.'

    return text_output
