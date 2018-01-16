import boto3

### DeleteSecurityGroup ###
def run_action(rule,entity,params):
    region = entity['Region']
    region = region.replace("_","-")
    sg_id = entity['Id']
    
    ec2 = boto3.resource('ec2', region_name=region)
    result = ec2.SecurityGroup(sg_id).delete()

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Security Group %s successfully deleted\n" % sg_id

    return text_output 