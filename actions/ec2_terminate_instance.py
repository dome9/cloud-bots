import boto3
from botocore.exceptions import ClientError

### Kill EC2 Instance ###
# def ec2_terminate_instance(instance,tags,event_log):
def run_action(rule,entity,params):
    #House keeping - set up variables   
    instance = entity['Id']
    region = entity['Region']
    region = region.replace("_","-")
    
    #initialize ec2
    ec2 = boto3.resource('ec2', region_name=region)

    try:
        #Apply the tags
        stop_instance = ec2.terminate_instances(InstanceIds=[instance])
        responseCode = stop_instance['ResponseMetadata']['HTTPStatusCode']

        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % stop_instance
        else:
            text_output = "Instance terminated: %s \n" % instance
        
    except (ClientError, AttributeError) as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output