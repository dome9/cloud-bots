'''
## iam_role_attach_policy  
What it does: Attaches a policy (passed in as a variable) to the role  
Usage: AUTO: iam_role_attach_policy policy_arn=<policy_arn>  
Limitations: none  
Examples:  
    AUTO: iam_role_attach_policy policy_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccess  
    AUTO: iam_role_attach_policy policy_arn=arn:aws:iam::621958466464:policy/sumo_collection  
    AUTO: iam_role_attach_policy policy_arn=arn:aws:iam::$ACCOUNT_ID:policy/sumo_collection  
'''

import boto3
from botocore.exceptions import ClientError


# Poll the account and check if the provided policy exists.
def check_for_policy(iam_client, policy_arn):
    found_policy = False
    try:
        # Check to see if the policy exists in the account currently
        get_policy_response = iam_client.get_policy(PolicyArn=policy_arn)

        if get_policy_response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output = 'IAM policy exists in this account.\n'
            found_policy = True

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            text_output = 'The policy %s does not exist. Please check and try again.\n' % policy_arn
        else:
            text_output = 'Unexpected error: %s \n' % e

    return text_output, found_policy


# Create attach the policy to the group
def add_policy_to_role(iam_client, role, policy_arn):
    try:
        attach_policy_response = iam_client.attach_role_policy(
            RoleName=role,
            PolicyArn=policy_arn
        )
        text_output = 'Policy attached to role: \' %s \'\n' % role

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output


### Update role - core method
def run_action(boto_session, rule, entity, params):
    text_output = ''
    account_id = entity['accountNumber']
    role = entity['name']

    iam_client = boto_session.client('iam')

    # Get the policy_arn from the params
    usage = 'Usage: AUTO: iam_role_attach_policy policy_arn=<policy_arn>\n Examples: \nAUTO: iam_role_attach_policy policy_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccess\nAUTO: iam_role_attach_policy policy_arn=arn:aws:iam::621958466464:policy/sumo_collection\niam_role_attach_policy policy_arn=arn:aws:iam::$ACCOUNT_ID:policy/sumo_collection\n'
    if len(params) == 1:
        try:
            if '=' in params[0]:
                key, value = params[0].split('=')
            else:
                key = 'policy_arn'
                value = params[0]

            if key == 'policy_arn':
                if 'arn:aws:iam::aws:policy' in value:
                    policy_arn = value
                    text_output = text_output + 'AWS Managed policy specified for attachment\nARN: %s \n' % value

                elif '$ACCOUNT_ID' in value:
                    # Look for '$ACCOUNT_ID' and replace it with the current account number
                    account_id = entity['accountNumber']
                    policy_arn = value.replace('$ACCOUNT_ID', account_id)
                    text_output = text_output + 'Policy ARN that we are attaching to the role: %s \n' % policy_arn

                else:
                    policy_arn = value
                    text_output = text_output + 'Policy ARN specified for attachment: %s \n' % value

            else:
                text_output = text_output + 'Params do not match expected values. Exiting.\n' + usage
                return text_output

        except:
            text_output = text_output + 'Params handling error. Please check params and try again.\n' + usage
            return text_output

    else:
        text_output = 'Wrong amount of params inputs detected. Exiting.\n' + usage
        return text_output

    ## Check and add the policy to the role
    try:
        function_output, found_policy = check_for_policy(iam_client, policy_arn)
        text_output = text_output + function_output

        if found_policy:
            text_output = text_output + add_policy_to_role(iam_client, role, policy_arn)
        else:
            return text_output

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output
