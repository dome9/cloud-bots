'''
## ec2_detach_instance_role
What it does: Detach an instance role from an EC2 instance.
Usage: AUTO: ec2_detach_instance_role

Sample GSL: cloudtrail where event.name='AddRoleToInstanceProfile' and event.status='Success'
Limitations: none
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
            text_output = f'The {role_name} role is not attached to instance.\nExiting\n'
            return text_output

        iam.remove_role_from_instance_profile(
            InstanceProfileName=response[0]['InstanceProfileName'],
            RoleName=role_name
        )

        text_output = f'The {role_name} role successfully detached from instance\nExiting'

    except ClientError as e:

        text_output = f'Unexpected error: {e}\n'
        

    return text_output
