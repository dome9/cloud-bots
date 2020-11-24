'''
## ec2_detach_instance_role
What it does: Detach an instance role from an EC2 instance.
Usage: AUTO: ec2_detach_instance_role

Sample GSL: Instance should have roles
'''

import boto3
from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    text_output = ''

    role_name = entity.get('name')

    iam = boto_session.client('iam')
    try:
        response = iam.list_instance_profiles_for_role(RoleName=role_name)['InstanceProfiles']
        if len(response) == 0:
            text_output = f'The {role_name} role is not attached to an instance.\nExiting'
            return text_output

        iam.remove_role_from_instance_profile(
            InstanceProfileName=response[0]['InstanceProfileName'],
            RoleName=role_name
        )
        text_output = text_output + 'Role successfully detached from instance\n'

    except ClientError as e:
        text_output = 'Unexpected error: %s , error code: %s\n' % e % e.response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        text_output = 'Unexpected error: %s\n' % e
    return text_output
