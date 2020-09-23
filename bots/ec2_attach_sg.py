'''
## ec2_attach_sg
What it does: Replaces any existing security groups with
 the specified security group to an EC2 instance.
Usage: 'AUTO: ec2_atach_sg name_of_sg_to_attach
Limitations: None
stuartg@checkpoint.com 23/9/20
'''

import boto3
from botocore.exceptions import ClientError

def run_action(boto_session,rule,entity,params):
    instance_id = entity['id']
    vpc_id = entity['vpc']['id']
    ec2_resource = boto_session.resource('ec2')
    ec2_client = boto_session.client('ec2')
    
    # Retrieve params, throw exception if not present
    try:
        param_group = params[0]
    except Exception as e:
        return (e)

    #Check the specified SG name exists
    try:    
        result = ec2_client.describe_security_groups(
            Filters=[
                    {
                        'Name': 'group-name',
                        'Values': [param_group]
                    },
                    {
                        'Name': 'vpc-id',
                        'Values': [vpc_id]
                    }
                ]
            )
        if result['SecurityGroups']: 
            sg_group_id = result['SecurityGroups'][0]['GroupId']
            text_output = "Existing security group ID: %s \n" % sg_group_id

        else:
            text_output = text_output + "ERROR: Security group '" + param_group + "' does not exist!" 
            return text_output

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    text_output = text_output + "Updating the instance SG attachments to contain the noted SG\n"

    #Attach the specified security group to the instance, remove others.
    try:
        result = ec2_resource.Instance(instance_id).modify_attribute(Groups=[sg_group_id])  
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "SG attached: %s \n" % instance_id

    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output 
