'''
## sg_delete
What it does: Deletes a security group  
Usage: AUTO: sg_delete  
Limitations: This will fail if there is something still attached to the SG.  
'''

import boto3

def run_action(boto_session,rule,entity,params):
    text_output = str(entity)
    sg_id = entity['id']
    
    ec2_resource = boto_session.resource('ec2')
    result = ec2_resource.SecurityGroup(sg_id).delete()

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Security Group %s successfully deleted\n" % sg_id

    return text_output 