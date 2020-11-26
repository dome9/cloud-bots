'''
## lambda_disable
What it does:
    Disable lambda function (by put function concurrency = 0).
Sample GSL:
    cloudtrail where event.name like 'UpdateFunctionCode%' and issuer.type='Role'
Usage:
    AUTO: lambda_disable
Limitations: none
'''

from botocore.exceptions import ClientError

### Disable lambda function
def run_action(boto_session, rule, entity, params):
    text_output = ''
    lambda_function_name = entity.get('name')
    lambda_client = boto_session.client('lambda')

    # try to set the function concurrency value to 0
    try:
        response = lambda_client.put_function_concurrency(
            FunctionName=lambda_function_name,
            ReservedConcurrentExecutions=0
        )

        text_output = f'lambda function: {lambda_function_name} disabled successfully\nExiting'

    except ClientError as e:
        text_output = f"can't disable the lambda function: {lambda_function_name}, Unexpected error: {e} \n"

    return text_output
