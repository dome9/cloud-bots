'''
## lambda_disable
What it does: Disable Lambda function
Usage: AUTO: labmda_disable  
Limitations: 1. Functions is throttled, which is easy to reverse
             2. Need to add lambda:PutFunctionConcurrency to the CloudBot role
'''

import boto3

def run_action(boto_session,rule,entity,params):
    try:
        client = boto3.client('lambda')
        resp = client.put_function_concurrency(
            FunctionName = entity['arn'],
            ReservedConcurrentExecutions = 0
        )
        return "Success %s" % str(resp)
        
    except Exception as err:
        return 'Error: %s' % str(err)
