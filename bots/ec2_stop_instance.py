'''
## ec2_stop_instance
What it does: Stops an ec2 instance  
Usage: AUTO: ec2_stop_instance  
Limitations: none  
'''

import boto3
from botocore.exceptions import ClientError


### Turn off EC2 instance ###
def run_action(boto_session,rule,entity,params):
    instance = entity['id']
    ec2_client = boto_session.client('ec2')
    try:
        result = ec2_client.stop_instances(InstanceIds=[instance])
    except ClientError as e:
        if 'InvalidInstanceID' in e.response['Error']['Code']:
            raise Exception('ERROR! Invalid instance id')
        else:
            raise e

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance stopped: %s \n" % instance

    return text_output 


