import boto3
import json
import os
from botocore.exceptions import ClientError

### Kill EC2 Instance ###
# def ec2_terminate_instance(instance,tags,event_log):
def run_action(message,event_log):
    #House keeping - set up variables    
    instance = message['Entity']['Id']
    region = message['Entity']['Region']
    region = region.replace("_","-")
    
    #initialize ec2
    ec2 = boto3.resource('ec2', region_name=region)

    try:
        #Apply the tags
        stop_instance = ec2.terminate_instances(InstanceIds=[instance])
        responseCode = stop_instance['ResponseMetadata']['HTTPStatusCode']

        if responseCode >= 400:
            text_output = ("Unexpected error:" + stop_instance + "\n")
        else:
            text_output = ("Instance terminated: " + instance + " \n")
        
    except (ClientError, AttributeError) as e:
        text_output = ("Unexpected error: %s" % e + "\n")

    return text_output