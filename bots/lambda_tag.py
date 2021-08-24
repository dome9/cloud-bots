'''
## lambda_tag
What it does: Tags a lambda function
Usage: AUTO: lambda_tag <key> <value>
Notes:
# <value> is an optional parameter. you can pass only key, without value. Usage: lambda_tag <key>
Limitations:
# Currently can't support tags/values with space. after enabling it, Tags/values with spaces can be added
if they are surrounded by quotes, e.g: lambda_tag "this is my key", "this is a value". (after that, there will be no limitations)
# need to add to the remediation role the Action - "lambda:TagResource". we may consider to keep this as a note, in case customers didn't relaunch the stack after the change.
'''

import boto3


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
        text_output = "Lambda function: %s successfully tagged with key: %s and value: %s \n" % (
        function_id, key, value)

    return text_output
