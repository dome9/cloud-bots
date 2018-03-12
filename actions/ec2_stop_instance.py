'''
## ec2_stop_instance
What it does: Stops an ec2 instance  
Usage: AUTO: ec2_stop_instance  
Limitations: none  
'''

import boto3

### Turn off EC2 instance ###
def run_action(rule,entity,params):
    instance = entity['id']
    region = entity['region']
    region = region.replace("_","-")

    ec2 = boto3.client('ec2', region_name=region)
    result = ec2.stop_instances(InstanceIds=[instance])

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance stopped: %s \n" % instance

    return text_output 