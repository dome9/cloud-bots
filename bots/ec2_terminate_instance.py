'''
## ec2_terminate_instance
What it does: Terminates an ec2 instance  
Usage: AUTO: ec2_terminate_instance  
Limitations: none  
'''

import boto3

### Kill EC2 Instance ###
def run_action(rule,entity,params):
    #House keeping - set up variables   
    instance = entity['id']
    region = entity['region']
    region = region.replace("_","-")
    
    ec2 = boto3.client('ec2', region_name=region)
    result = ec2.terminate_instances(InstanceIds=[instance])
    
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % result
    else:
        text_output = "Instance terminated: %s \n" % instance

    return text_output