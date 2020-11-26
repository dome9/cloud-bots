'''
## lambda_disable
What it does:
    Disable lambda function (by put function concurrency = 0),
Sample GSL:
    Lambda Function Code was Updated by an enitity which assumed a Role
Usage:
    AUTO: lambda_disable
Limitations: none
'''

from botocore.exceptions import ClientError

### Disable lambda function - core method
def run_action(boto_session, rule, entity, params):
    text_output = ''
    lambda_function_name = entity.get('name')
    lambda_client = boto_session.client('lambda')

    # try to set the function concurrency value to 0, than the function will not be able to run:
    try:
        response = lambda_client.put_function_concurrency(
            FunctionName=lambda_function_name,
            ReservedConcurrentExecutions=0
        )

        text_output = "lambda function: %s disabled (function concurrency set to 0)\n" % lambda_function_name

    except ClientError as e: # error with put_function_concurrency request
        text_output = "can't disable the lambda function: %s, Unexpected error: %s \n" % (lambda_function_name, e)

    return text_output
