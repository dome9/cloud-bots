
'''
## instance_quarantine
What it does: Attaches the instance a SG with no rules so it can't communicate with the outside world
Usage: AUTO: instance_quarantine
Limitations: None


# Create a quarantine SG in the VPC (if fail, it exists)
# Attach instance to SG (detaches existing SGs at the same time)
'''

import boto3
from botocore.exceptions import ClientError

def run_action(rule,entity,params):
    instance_id = entity['id']
    region = entity['region']
    region = region.replace("_","-")

    vpc_id = entity['vpc']['id']

    ec2_resource = boto3.resource('ec2', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)

    #Create the Quarantine SG
    try:    
        result = ec2_resource.create_security_group(
            Description='Quarantine Security Group. No ingress or egress rules should be attached.',
            GroupName='quarantine',
            VpcId=vpc_id )
        text_output = "Quarantine SG created %s \n" % result.id
        quarantine_sg_id = [result.id]
    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'InvalidGroup.Duplicate':
            text_output = "Quarantine SG already exists\n"
            # Get the SG id of the existing SG
            try:  
                result = ec2_client.describe_security_groups(
                    Filters=[
                            {
                                'Name': 'group-name',
                                'Values': [
                                    'quarantine',
                                ]
                            },
                        ]
                    )
                quarantine_sg_id = [result['SecurityGroups'][0]['GroupId']]

                text_output = text_output + "Existing quarantine sg_id: %s \n" % quarantine_sg_id
            except ClientError as e:
                text_output = text_output + "Unexpected error: %s \n" % e
        else:
            text_output = "Unexpected error: %s \n" % e

    text_output = text_output + "Updating the instance SG attachments to only contain the quarantine SG\n"

    try:
        result = ec2_resource.Instance(instance_id).modify_attribute(Groups=quarantine_sg_id)  
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "Instance quarantined: %s \n" % instance_id

    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output 
