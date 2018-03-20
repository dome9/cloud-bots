import boto3

### Take tags from VPC and add them as tags to EC2 ### 
# Tag format: AUTO: ec2_tag_instance_from_vpc

def run_action(rule,entity, params):
    instance = entity['id']
    region = entity['region']
    region = region.replace("_","-")
    tags = entity['vpc']['tags']
    vpc_id = entity['vpc']['id']
    
    text_output = "Tagging instance with tags from VPC (id: %s)\n" % vpc_id

    for tag in tags:
        key = tag['key']
        value = tag['value']

        if not value:
            text_output = text_output + "Key \"%s\" has an empty value. Skipping\n" % key
            continue

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
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "Instance tagged: %s \nKey: %s | Value: %s \n" % (instance,key,value)

    return text_output

