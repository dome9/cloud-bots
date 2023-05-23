"""
## ec2_attach_instance_role
What it does: Attaches an instance role to an EC2 instance. This role needs be passed in through the params.
Usage: AUTO: ec2_attach_instance_role role_arn=<role_arn>

If you have a role that is the same across accounts, and don't want to pass in an account specific ARN,
add '$ACCOUNT_ID' to the role ARN and the function will automatically pull in the current account ID of the finding.
Example: AUTO: ec2_attach_instance_role role_arn=arn:aws:iam::$ACCOUNT_ID:instance-profile/ec2SSM
Sample GSL: Instance should have roles
"""

from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    instance_id = entity['id']
    text_output = ''

    ec2_client = boto_session.client('ec2')   

    # Set up params. We need a role ARN to come through in the params.
    usage = 'Usage: AUTO: ec2_attach_instance_role role_arn=<role_arn>\n ' \
            'Example: AUTO: ec2_attach_instance_role role_arn=arn:aws:iam::621958466464:role/ec2Alexa\n'
    if len(params) == 1:
        try:
            if '=' in params[0]:
                key, value = params[0].split('=')
            else:
                key = 'role_arn'
                value = params[0]
            if key == 'role_arn':     
                # Look for '$ACCOUNT_ID' and replace it with the current account number
                account_id = entity['accountNumber']
                role_arn = value.replace('$ACCOUNT_ID', account_id)
                text_output = text_output + 'Role ARN that we are attaching to the instance: %s \n' % role_arn
            else:
                raise Exception('ERROR! Params do not match expected values. Exiting.')
        except Exception:
            raise Exception('ERROR! Params handling error. Please check params and try again.\n' + usage)
    else:
        raise Exception('ERROR! Wrong amount of params inputs detected. Exiting.\n' + usage)

    # If the instance has an instance profile, try to update the role to have the new policy attached.
    # If it's already attached, it'll still return a 200 so no need to worry about too much error handling.
    if len(entity['roles']) == 0:
        try:
            result = ec2_client.associate_iam_instance_profile(
                IamInstanceProfile={
                    'Arn': role_arn,
                    'Name': role_arn.split('/')[1]
                },
                InstanceId=instance_id
            )

            response_code = result['ResponseMetadata']['HTTPStatusCode']
            if response_code >= 400:
                text_output = text_output + 'Unexpected error: %s \n' % str(result)
                raise Exception('ERROR!' + text_output)
            else:
                text_output = text_output + 'Role successfully attached to instance\n'

        except ClientError as e:
            text_output = text_output + 'Unexpected error: %s \n' % e
            raise Exception('ERROR!' + text_output)

    else:
        raise Exception('ERROR! Instance already has an instance role attached.\nExiting\n')

    return text_output
