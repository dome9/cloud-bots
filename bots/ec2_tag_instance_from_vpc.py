import boto3

### If an instance is missing a specific tag, try to pull it from the VPC. 
# Tag format: AUTO: ec2_tag_instance_from_vpc <Key>

def run_action(boto_session,rule,entity, params):
    instance = entity['id']
    vpc_tags = entity['vpc']['tags']
    vpc_id = entity['vpc']['id']

    ec2_client = boto_session.client('ec2')

    try:
        key = params[0]
    except:
        text_output = "USAGE: AUTO: ec2_tag_instance_from_vpc <Key>\nNo key was found. Skipping.\n"
        return text_output

    instance_tagged = False

    text_output = "Checking instance VPC tags for \"%s\" tag\n" % key

    for tag in vpc_tags:
        vpc_key = tag['key']
        vpc_value = tag['value']

        if key == vpc_key:
            result = ec2_client.create_tags(
                Resources=[instance],
                Tags=[
                    {
                        'Key': vpc_key,
                        'Value': vpc_value
                    }
                ]
            )
        
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s \n" % str(result)
            else:
                text_output = text_output + "Instance tagged: %s \nKey: %s | Value: %s \n" % (instance,vpc_key,vpc_value)
                instance_tagged = True

    if not instance_tagged:
        text_output = text_output + "Did not find the \"%s\" key in the VPC tags. Please check the VPC and try again.\n" % key

    return text_output