"""
## ecs_service_role_detach_inline_policy
What it does: removes all inline policies from the role of the ECS
Usage: ecs_service_role_detach_inline_policy
Limitations: None
"""

from botocore.exceptions import ClientError

permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'


def run_action(boto_session, rule, entity, params):
    role_name = entity['role']['name']
    text_output = ''
    iam_client = boto_session.client('iam')

    try:
        print(f'{__file__} - Fetching inline policies from the following role: {role_name}\n')
        result = iam_client.list_role_policies(RoleName=role_name)
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
            return text_output
        else:
            inline_policies = result['PolicyNames']
            print(f'{__file__} - Done. {len(inline_policies)} inline policies will be deleted from {role_name}.\n')
    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
        return text_output

    inline_policies_list = []
    for policy in inline_policies:
        try:
            print(f'{__file__} - Trying to remove the policy: {policy}\n')
            result = iam_client.delete_role_policy(
                RoleName=role_name,
                PolicyName=policy
            )

            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s \n" % str(result)
                return text_output
            else:
                print(f'{__file__} - Done. \n')
                inline_policies_list.append(policy)

        except ClientError as e:
            text_output = f"Unexpected client error: {e} \n"
            if 'AccessDenied' in e.response['Error']['Code']:
                text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
                return text_output

    if len(inline_policies_list) > 0:
        policies_string = ', '.join(inline_policies_list)
        text_output = text_output + f'Successfully detached inline policies from the role: {role_name}. The following policies removed: {policies_string}. You may want to convert them to managed policies. \n'

    return text_output
