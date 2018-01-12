import boto3
from botocore.exceptions import ClientError

### Add Tags to EC2 ### 
# Tag format: AUTO: ec2_tag_instance key value"
def run_action(rule,entity, params):
    instance = entity['Id']
    region = entity['Region']
    region = region.replace("_","-")
    key = params[0]
    value = params[1]
    print("tagging:", key,value)

    ec2 = boto3.client('ec2', region_name=region)
    result = ec2.create_tags(
        Resources=[instance],
        Tags=[
            {
                'Key': key,
                'Value': value
            }
        ]
    )
    
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % tag_instance
    else:
        text_output = "Instance tagged: %s \nKey: %s | Value: %s \n" % (instance,key,value)

    return text_output