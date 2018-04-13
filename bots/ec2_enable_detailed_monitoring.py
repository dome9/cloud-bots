'''
## ec2_enable_detailed_monitoring
What it does: Turns on detailed monitoring for an ec2 instance
Usage: AUTO: ec2_enable_detailed_monitoring
Limitations: none 
'''

import boto3

def run_action(boto_session,rule,entity,params):
    instance = entity['id']
    ec2_client = boto_session.client('ec2')
    
    result = ec2_client.monitor_instances(InstanceIds=[instance])

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Detailed monitoring enabled for instance: %s \n" % instance

    return text_output 
