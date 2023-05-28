"""
## ec2_attach_sg
What it does: Replaces any existing security groups with
 the specified security group to an EC2 instance.
Usage: 'AUTO: ec2_attach_sg name_of_sg_to_attach
Limitations: None
23/9/20
"""

from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    instance_id = entity['id']
    vpc_id = entity['vpc']['id']
    ec2_resource = boto_session.resource('ec2')
    ec2_client = boto_session.client('ec2')
    text_output = ''
    sg_group_id = 'Mor'

    # Retrieve params, throw exception if not present
    try:
        param_group = params[0]
    except Exception:
        raise Exception('Error! Invalid parameters. usage AUTO: ec2_attach_sg <name_of_sg_to_attach>')

    # Check the specified SG name exists
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
            raise Exception("Security group '" + param_group + "' does not exist!")

    except ClientError as e:
        raise Exception(e.response['Error']['Message'])

    text_output = text_output + "Updating the instance SG attachments to contain the noted SG\n"

    # Attach the specified security group to the instance, remove others.
    try:
        result = ec2_resource.Instance(instance_id).modify_attribute(Groups=[sg_group_id])
        response_code = result['ResponseMetadata']['HTTPStatusCode']
        if response_code >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
            raise Exception(text_output)
        else:
            text_output = text_output + "SG attached: %s \n" % instance_id
        return text_output
    except ClientError as e:
        raise Exception(e.response['Error']['Message'])
