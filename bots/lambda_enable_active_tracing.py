"""
## lambda_enable_active_tracing
What it does: Enable lambda active tracing
Usage: lambda_enable_active_tracing
Limitations: none
"""

import boto3
from botocore.exceptions import ClientError

def run_action(session, rule, entity, params):
    lambda_client = boto3.client('lambda')
    lambda_name = entity['name']

    text_output = ''

    try:
        response = lambda_client.update_function_configuration(FunctionName=lambda_name,
                                                TracingConfig={
                                                    'Mode': 'Active'})
        text_output = f'Enabled active tracing in lambda: {lambda_name}'
    except ClientError as error:
        text_output = f"Unexpected error: {error} \n"

    return text_output

