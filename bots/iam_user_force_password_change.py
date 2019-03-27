'''
## iam_user_force_password_change
What it does: Updates the setting for an IAM user so that they need to change their console password the next time they log in.  
Usage: AUTO: iam_user_force_password_change
Limitations: none  
'''

import boto3
from botocore.exceptions import ClientError

def run_action(boto_session,rule,entity,params):
    username = entity['name']

    iam_client = boto_session.client('iam')

    try:
        result = iam_client.update_login_profile(
            UserName=username,
            PasswordResetRequired=True
        )
 
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "User %s updated. Their password will have to be changed at their next login.\n" % username
        
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e
    
    return text_output
