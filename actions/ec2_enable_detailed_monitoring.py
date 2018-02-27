import boto3

## Turn on EC2 detailed monitoring
def run_action(rule,entity,params):
    instance = entity['id']
    ec2 = boto3.client('ec2')
    result = ec2.monitor_instances(InstanceIds=[instance])

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Detailed monitoring enabled for instance: %s \n" % instance

    return text_output 
