import boto3
from botocore.exceptions import ClientError

### DeleteSecurityGroup ###
def run_action(rule,entity,params):
    region = entity['Region']
    region = region.replace("_","-")

    sg_id = message['Entity']['Id']
    ec2 = boto3.resource('ec2', region_name=region)

    try:
        delete_sg = ec2.SecurityGroup(sg_id).delete()
        text_output = "Security Group %s successfully deleted\n" % sg_id
        
    except (ClientError, AttributeError) as e:
        error = e.response['Error']['Code']
        if error == 'DependencyViolation':
            text_output = "Security group (id: %s) Still has assets attahced to it. Can't delete / Skipping.\n" % sg_id
        else:   
            text_output = "Unexpected error: %s \n" % e
        #Add in "SG is in use error. Dump current attachments"

    return text_output 