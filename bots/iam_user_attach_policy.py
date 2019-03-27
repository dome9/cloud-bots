'''
## iam_user_attach_policy  
What it does: Attaches a policy (passed in as a variable) to the user  
Usage: AUTO: iam_user_attach_policy policy_arn=<policy_arn>  
Limitations: none  
Examples:  
    AUTO: iam_user_attach_policy policy_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccess  
    AUTO: iam_user_attach_policy policy_arn=arn:aws:iam::621958466464:policy/sumo_collection  
    AUTO: iam_user_attach_policy policy_arn=arn:aws:iam::$ACCOUNT_ID:policy/sumo_collection  
'''

import boto3
from botocore.exceptions import ClientError

#Poll the account and check if the provided policy exists. 
def check_for_policy(iam_client,policy_arn):    
    found_policy = False
    try:
        #Check to see if the policy exists in the account currently
        get_policy_response = iam_client.get_policy(PolicyArn=policy_arn)
        
        if get_policy_response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output =  "IAM policy exists in this account."
            found_policy = True

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            text_output = "The policy %s does not exist. Please check and try again." % policy_arn
        else:
            text_output = "Unexpected error: %s " % e

    return text_output,found_policy

#Create attach the policy to the group
def add_policy_to_user(iam_client,user,policy_arn):        
    try:
        attach_policy_response = iam_client.attach_user_policy(
            UserName=user,
            PolicyArn=policy_arn
        )
        
        text_output = "Policy attached to user: \" %s \"" % user

    except ClientError as e:
            text_output = "Unexpected error: %s " % e

    return text_output

### Update user - core method
def run_action(boto_session,rule,entity,params):
    text_output = ""
    account_id = entity['accountNumber']
    user = entity['name']

    iam_client = boto_session.client('iam')

    # Get the policy_arn from the params
    usage = "Usage: AUTO: iam_user_attach_policy policy_arn=<policy_arn>Examples: AUTO: iam_user_attach_policy policy_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccessAUTO: iam_user_attach_policy policy_arn=arn:aws:iam::621958466464:policy/sumo_collectioniam_user_attach_policy policy_arn=arn:aws:iam::$ACCOUNT_ID:policy/sumo_collection"
    if len(params) == 1:
        try:
            key_value = params[0].split("=")
            key = key_value[0]
            value = key_value[1]

            if key == "policy_arn":     
                if "arn:aws:iam::aws:policy" in value:
                    policy_arn = value
                    text_output = text_output + "AWS Managed policy specified for attachmentARN: %s " % value
                
                elif "$ACCOUNT_ID" in value:
                    # Look for "$ACCOUNT_ID" and replace it with the current account number
                    account_id = entity['accountNumber']
                    policy_arn = value.replace("$ACCOUNT_ID", account_id)
                    text_output = text_output + "Policy ARN that we're attaching to the user: %s " % policy_arn

                else:
                    policy_arn = value
                    text_output = text_output + "Policy ARN specified for attachment: %s " % value

            else:
                text_output = text_output + "Params don't match expected values. Exiting." + usage
                return text_output  

        except:
            text_output = text_output + "Params handling error. Please check params and try again." + usage
            return text_output

    else:
        text_output = "Wrong amount of params inputs detected. Exiting." + usage
        return text_output

    ## Check and add the policy to the user
    try:
        function_output, found_policy = check_for_policy(iam_client,policy_arn)
        text_output = text_output + function_output
        
        if found_policy:
            text_output = text_output + add_policy_to_user(iam_client,user,policy_arn)
        else:
            return text_output
        
    except ClientError as e:
        text_output = "Unexpected error: %s " % e
    
    return text_output




