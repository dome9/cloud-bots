"""
## BOT NAME (EXAMPLE: lambda_tag)
What it does: BOT DESCRIPTION (EXAMPLE: Tags a lambda function)
Usage: AUTO BOT NAME <PARAMETER1> <PARAMETER2> (EXAMPLE: AUTO: lambda_tag <key> <value>)
Notes: IF NEEDED.
Limitations: IF NEEDED.
"""


def run_action(boto_session, rule, entity, params):

    '''
    # PARAMETERS VALIDATION (COUNT, TYPE, ETC.)
    EXAMPLE:
    if len(params) != 1:
        raise ValueError(f"Error: Wrong use of the BOT NAME bot. Usage: ... \n")

    client = boto_session.client('SERVICE NAME')
    text_output = ''

    print(f'{__file__} - Trying to... \n') # logging to cloudwatch
    result = client.BOTO3_CLIENT_OPERATION(...)

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        raise ValueError("Unexpected error: %s \n" % str(result))
    else:
        print(f'{__file__} - Done. \n')
        text_output = text_output + f'BOT SUCCESS MESSAGE \n'

    return text_output

'''