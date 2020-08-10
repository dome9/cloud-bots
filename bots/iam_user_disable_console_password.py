'''
## iam_user_disable_console_password

What it does:  disable console password for IAM user.

Usage: iam_user_disable_console_password

Limitations: Deleting a user's password does not prevent a user from accessing AWS through the command line interface or
the API. To prevent all user access, you must also either make any access keys inactive or delete them.
'''

import boto3
from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    text_output = 'Start iam_user_disable_console_password; '
    username = entity['name']
    # Create an IAM resource
    iam_res = boto3.resource('iam')

    # ----------------------- Disable Console Password ----------------------------------#
    try:
        # load the login profile of the username
        login_profile = iam_res.LoginProfile(username)
        # deletes the password for the specified IAM use
        login_profile.delete()
        text_output = text_output + f'Iam user: {username}\'s console password was removed; '

    except ClientError as e:
        text_output = text_output + f'Unexpected error: {e}.'

    return text_output
