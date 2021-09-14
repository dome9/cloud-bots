"""
## BOT NAME (EXAMPLE: lambda_tag)
What it does: BOT DESCRIPTION (EXAMPLE: Tags a lambda function)
Usage: AUTO BOT NAME <PARAMETER1> <PARAMETER2> (EXAMPLE: AUTO: lambda_tag <key> <value>)
Notes: IF NEEDED.
Limitations: IF NEEDED.
"""

from botocore.exceptions import ClientError
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'

def run_action(boto_session, rule, entity, params):

    '''
    # PARAMETERS VALIDATION (COUNT, TYPE, ETC.)
    EXAMPLE:
    if len(params) != 1:
        return f"Error: Wrong use of the BOT NAME bot. Usage: ... \n"

    client = boto_session.client('SERVICE NAME')
    text_output = ''

    try:
        result = client.BOTO3_CLIENT_OPERATION(...)

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + f'BOT SUCCESS MESSAGE \n'

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output

'''