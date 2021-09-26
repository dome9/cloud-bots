'''
## iam_role_clone_with_non_enumerable_name
What it does: Clones the IAM role and gives it a non-enumerable name. The new name is the original name +  20 length non-enumerable string, Example: MyRole -> MyRole-XaTrEiuNyHsRAqqC_rBW.
Usage: AUTO: iam_role_clone_non_enumerable_name
Limitations: The bot doesn't delete the original role, in order to avoid misconfigurations. After the role will be cloned, it's under your responsibility to delete the original role, after
validating it (For example, it's important to make sure that you do not have any Amazon EC2 instances running with the role). If you're using the bot via CSPM, the rule will keep failing
until the original role (with the enumerable name) will be deleted. In the response message of the bot, you'll get the information about the old and the new (cloned) role.
For more information see:
https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_delete.html
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#replace-iam-role
'''

import json
from botocore.exceptions import ClientError
import string
import secrets

LENGTH = 13
allowed_characters = string.ascii_letters + string.digits + '+=,.@-_'  # AWS allow role names only with those characters
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'


def generate_non_enumerable_name(orig_role_name):
    random_str = ''.join(secrets.choice(allowed_characters) for x in range(LENGTH))
    new_role_name = f"{orig_role_name}-{random_str}"
    return new_role_name


def get_original_role(iam_client, orig_role_name):
    orig_role = iam_client.get_role(RoleName=orig_role_name)
    responseCode = orig_role['ResponseMetadata']['HTTPStatusCode']
    return orig_role, responseCode


def get_inline_policies(iam_client, orig_role_name, marker=None):
    if marker:
        response = iam_client.list_role_policies(RoleName=orig_role_name, Marker=marker)
    else:
        response = iam_client.list_role_policies(RoleName=orig_role_name)
    inline_policy_names = response['PolicyNames']
    if response['IsTruncated']:
        inline_policy_names = inline_policy_names + get_inline_policies(iam_client, orig_role_name, response['Marker'])
    responseCode = response['ResponseMetadata']['HTTPStatusCode']
    return inline_policy_names, responseCode


def get_managed_policies(iam_client, orig_role_name, marker=None):
    if marker:
        response = iam_client.list_attached_role_policies(RoleName=orig_role_name, Marker=marker)
    else:
        response = iam_client.list_attached_role_policies(RoleName=orig_role_name)
    managed_policies = response['AttachedPolicies']
    if response['IsTruncated']:
        managed_policy_names = managed_policies + get_inline_policies(iam_client, orig_role_name, response['Marker'])
    responseCode = response['ResponseMetadata']['HTTPStatusCode']
    return managed_policies, responseCode


def create_role_copy(iam_client, orig_role, new_role_name, inline_policies, managed_policies):
    if 'PermissionsBoundary' in orig_role['Role']:
        new_role = iam_client.create_role(
            Path=orig_role['Role']['Path'],
            RoleName=new_role_name,
            AssumeRolePolicyDocument=json.dumps(orig_role['Role']['AssumeRolePolicyDocument']),
            Description=orig_role['Role']['Description'],
            MaxSessionDuration=orig_role['Role']['MaxSessionDuration'],
            PermissionsBoundary=orig_role['Role']['PermissionsBoundary'],
        )
    else:
        new_role = iam_client.create_role(
            Path=orig_role['Role']['Path'],
            RoleName=new_role_name,
            AssumeRolePolicyDocument=json.dumps(orig_role['Role']['AssumeRolePolicyDocument']),
            Description=orig_role['Role']['Description'],
            MaxSessionDuration=orig_role['Role']['MaxSessionDuration']
        )
    responseCode = new_role['ResponseMetadata']['HTTPStatusCode']
    if 'Tags' in orig_role['Role']:
        tag_response = iam_client.tag_role(
            RoleName=new_role_name,
            Tags=orig_role['Role']['Tags']
        )
        tag_response_code = tag_response['ResponseMetadata']['HTTPStatusCode']
        return new_role, responseCode, tag_response_code
    return new_role, responseCode, 0


def add_inline_policies(iam_client, new_role_name, inline_policies):
    for policy in inline_policies:
        response = iam_client.put_role_policy(
            RoleName=new_role_name,
            PolicyName=policy['Name'],
            PolicyDocument=json.dumps(policy['PolicyDocument'])
        )
        if response['ResponseMetadata']['HTTPStatusCode'] >= 400:
            return False, response
    return True, {}


def add_managed_policies(iam_client, new_role_name, managed_policies):
    for policy in managed_policies:
        response = iam_client.attach_role_policy(
            RoleName=new_role_name,
            PolicyArn=policy['PolicyArn'],
        )
        if response['ResponseMetadata']['HTTPStatusCode'] >= 400:
            return False, response
    return True, {}


def run_action(boto_session, rule, entity, params):
    orig_role_name = entity['name']
    print(f'{__file__} - The following role will be cloned: {orig_role_name}. \n')
    new_role_name = generate_non_enumerable_name(orig_role_name)
    print(f'{__file__} - Generated new name: {new_role_name} \n')
    iam_client = boto_session.client('iam')
    text_output = ''
    try:
        print(f'{__file__} - Fetching role... \n')
        orig_role, responseCode = get_original_role(iam_client, orig_role_name)
        if responseCode >= 400:
            text_output += f"Failed to fetch role {orig_role_name}. Unexpected error: %s \n" % str(orig_role)
            return text_output
        print(f'{__file__} - Successfully Fetched Role. \n')
        print(f'{__file__} - Fetching inline policies... \n')
        inline_policies, responseCode = get_inline_policies(iam_client, orig_role_name)
        if responseCode >= 400:
            text_output += "Failed to fetch the inline policies. Unexpected error: %s \n" % str(inline_policies)
            return text_output
        print(f'{__file__} - Successfully fetched inline policies. \n')
        print(f'{__file__} - Fetching managed policies... \n')
        managed_policies, responseCode = get_managed_policies(iam_client, orig_role_name)
        if responseCode >= 400:
            text_output += "Failed to fetch the managed policies. Unexpected error: %s \n" % str(inline_policies)
            return text_output
        print(f'{__file__} - Successfully fetched managed policies. \n')
        print(f'{__file__} - Creating the new role... \n')
        new_role, responseCode, tag_response_code = create_role_copy(iam_client, orig_role, new_role_name,
                                                                     inline_policies, managed_policies)
        if responseCode >= 400:
            text_output += "Failed to create the new role. Unexpected error: %s \n" % str(new_role)
            return text_output
        print(f'{__file__} - Successfully created a new role with name: {new_role_name}. \n')
        if tag_response_code >= 400:
            print(f'{__file__} Failed to add tags to the new role. Continuing. Please try to add them manually \n')
            text_output += "Failed to add tags to the new role. Please try to add them manually. \n"
        if len(inline_policies) > 0:
            print(f'{__file__} - Attaching inline policies... \n')
            success, response = add_inline_policies(iam_client, new_role_name, inline_policies)
            if not success:
                text_output += "Failed to attach inline policies. Unexpected error: %s \n" % str(response)
                return text_output
            print(f'{__file__} - Successfully attached {len(inline_policies)} inline policies. \n')
        if len(managed_policies) > 0:
            print(f'{__file__} - Attaching managed policies... \n')
            success, response = add_managed_policies(iam_client, new_role_name, managed_policies)
            if not success:
                text_output += "Failed to attach managed policies. Unexpected error: %s \n" % str(response)
                return text_output
            print(f'{__file__} - Successfully attached {len(managed_policies)} managed policies. \n')
        print(f'{__file__} - Done cloning. \n')
        text_output += f'Successfully created a copy of role {orig_role_name} with non-enumerable name: {new_role_name}. Please note the original role didnt delete and you should validate and then delete it by yourself. \n'

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
    except Exception as e:
        text_output = f"Unexpected error: {e}. For more details please see the CloudWatch logs. \n"

    print(f'{__file__} - {text_output} \n')
    return text_output
