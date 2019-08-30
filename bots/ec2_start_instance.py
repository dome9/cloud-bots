'''
## ec2_start_instance
What it does: Starts an ec2 instance  
Usage: AUTO: ec2_start_instance  
Limitations: none  
'''

import boto3

### Turn on EC2 instance ###
def run_action(boto_session,rule,entity,params):
    instance = entity['id']
    ec2_client = boto_session.client('ec2')
    
    result = ec2_client.start_instances(InstanceIds=[instance])

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance started: %s \n" % instance

    return text_output 


