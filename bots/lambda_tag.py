'''
## lambda_tag
What it does: Tags a lambda function
Usage: AUTO: lambda_tag <key> <value>
Notes:
# <value> is an optional parameter. you can pass only key, without value. Usage: lambda_tag <key>
Limitations: Tags/values with spaces are currently not supported. it will be added in the future.
'''

from botocore.exceptions import ClientError
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'

def run_action(boto_session, rule, entity, params):

    function_id = entity['id']

    if len(params) == 2:  # provided key and value
        key = params[0].replace('"', '')
        value = params[1].replace('"', '')

    elif len(params) == 1:  # provided key only
        key = params[0].replace('"', '')
        value = ''

    else:
        text_output = f"Error: Wrong use of the lambda_tag bot. Usage: lambda_tag <key> <value> (<value> is optional). Make sure the correct parameters are provided. \
                if the parameters include spaces make sure each one surrounded bu quotes."
        return text_output

    client = boto_session.client('lambda')
    try:
        result = client.tag_resource(
            Resource=function_id,
            Tags={
                key: value,
            },
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "Lambda function: %s successfully tagged with key: %s and value: %s \n" % (function_id, key, value)

        return text_output

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output
