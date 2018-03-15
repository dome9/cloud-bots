'''
## rds_quarantine_instance
What it does: Attaches the RDS instance a SG with no rules so it can't communicate with the outside world
Usage: AUTO: rds_quarantine_instance
Limitations: Instance needs to be "Available" in order to update. If it's in "backing up" state, this will fail
'''

import boto3
from botocore.exceptions import ClientError

def run_action(rule,entity,params):
    db_name = entity['name']
    region = entity['region']
    region = region.replace("_","-")
    vpc_id = entity['vpc']['id']

    ec2_resource = boto3.resource('ec2', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)
    rds_client = boto3.client('rds', region_name=region)

    #Check or create the Quarantine SG
    try:    
        result = ec2_client.describe_security_groups(
            Filters=[
                    {
                        'Name': 'group-name',
                        'Values': ['quarantine']
                    },
                    {
                        'Name': 'vpc-id',
                        'Values': [vpc_id]
                    }
                ]
            )
        if result['SecurityGroups']: 
            quarantine_sg_id = [result['SecurityGroups'][0]['GroupId']]
            text_output = "Existing quarantine sg_id: %s \n" % quarantine_sg_id

        else:
            result = ec2_resource.create_security_group(
                    Description='Quarantine Security Group. No ingress or egress rules should be attached.',
                    GroupName='quarantine',
                    VpcId=vpc_id )
            text_output = "Quarantine SG created %s \n" % result.id
            quarantine_sg_id = [result.id]
        
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    text_output = text_output + "Updating the instance SG attachments to only contain the quarantine SG\n"

    #Attach the RDS instance to only the quarantine SG
    try:
        result = rds_client.modify_db_instance(
            DBInstanceIdentifier=db_name,
            VpcSecurityGroupIds=quarantine_sg_id,
            ApplyImmediately=True
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "RDS instance quarantined: %s \n" % db_name

    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output 

