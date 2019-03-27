'''
## rds_quarantine_instance
What it does: Attaches the RDS instance a SG with no rules so it can't communicate with the outside world
Usage: AUTO: rds_quarantine_instance
Limitations: Instance needs to be "Available" in order to update. If it's in "backing up" state, this will fail
    Might not work with Aurora since it's in a cluster
'''

import boto3
from botocore.exceptions import ClientError

def run_action(boto_session,rule,entity,params):
    db_name = entity['name']
    vpc_id = entity['vpc']['id']

    ec2_resource = boto_session.resource('ec2')
    ec2_client = boto_session.client('ec2')
    rds_client = boto_session.client('rds')

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
            quarantine_sg_id = result['SecurityGroups'][0]['GroupId']
            text_output = "Existing quarantine sg_id: %s " % quarantine_sg_id

        else:
            result = ec2_client.create_security_group(
                    Description='Quarantine Security Group. No ingress or egress rules should be attached.',
                    GroupName='quarantine',
                    VpcId=vpc_id 
                    )

            #When a SG is created, AWS automatically adds in an outbound rule we need to delete
            security_group = ec2_resource.SecurityGroup(result['GroupId'])
            delete_outbound_result = security_group.revoke_egress(GroupId=result['GroupId'],IpPermissions=[{'IpProtocol':'-1','IpRanges': [{'CidrIp':'0.0.0.0/0'}]}])


            text_output = "Quarantine SG created %s " % result['GroupId']
            quarantine_sg_id = result['GroupId']
        
    except ClientError as e:
        text_output = "Unexpected error: %s " % e

    text_output = text_output + "Updating the instance SG attachments to only contain the quarantine SG"

    #Attach the RDS instance to only the quarantine SG
    try:
        result = rds_client.modify_db_instance(
            DBInstanceIdentifier=db_name,
            VpcSecurityGroupIds=[quarantine_sg_id],
            ApplyImmediately=True
            )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s " % str(result)
        else:
            text_output = text_output + "RDS instance quarantined: %s " % db_name

    except ClientError as e:
        text_output = text_output + "Unexpected error: %s " % e

    return text_output 

