import boto3
import json
import os
from botocore.exceptions import ClientError

### DeleteSecurityGroup ###
def run_action(message):
    region = message['Entity']['Region']
    region = region.replace("_","-")

    sg_id = message['Entity']['Id']
    ec2 = boto3.resource('ec2', region_name=region)

    try:
        delete_sg = ec2.SecurityGroup(sg_id).delete()
        text_output = ("Security Group " + sg_id + " successfully deleted\n")
        
    except (ClientError, AttributeError) as e:
        error = e.response['Error']['Code']
        if error == 'DependencyViolation':
            text_output = ("Security group (id: " + sg_id + ") Still has assets attahced to it. Can't delete / Skipping.\n")
        else:    
            text_output = ("Unexpected error: %s" % e + "\n")
        #Add in "SG is in use error. Dump current attachments"

    return text_output 