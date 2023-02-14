'''
## iam_entity_remove_permission_boundary
What it does: Removes an attached permissions boundary from iam entity (Role/User).
Usage: iam_entity_remove_permission_boundary entity_arn=<name|all> [cloud_account_id=<123456789>] [--dryRun]
Limitations: None.
Examples:  
    iam_entity_remove_permission_boundary entity_arn=all -> Will remove permission boundary from all IAM entities in the bot account.
    iam_entity_remove_permission_boundary entity_arn=name -> WIll remove permission boundary from specific iam entity.
    iam_entity_remove_permission_boundary entity_arn=all cloud_account_id=123456789 -> Will remove permission boundary from all IAM entities in account 123456789
'''

import boto3
from botocore.exceptions import ClientError

LIST_MAX_ITEMS = 1000


# Attach permission boundary to user
def remove_user_permission_boundary(iam_client, name):
    try:
        remove_boundary_policy = iam_client.delete_user_permissions_boundary(
            UserName=name
        )
        text = 'Permission boundary removed from user: \' %s \'\n' % name

    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchEntity':
            text = 'Unexpected error: %s \n' % e
        else:
            text = 'No permission boundary for %s.' % name
            pass

    return text


def remove_role_permission_boundary(iam_client, name):
    try:
        remove_boundary_policy = iam_client.delete_role_permissions_boundary(
            RoleName=name
        )
        text = 'Permission boundary removed from role: \' %s \'\n' % name

    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchEntity':
            text = 'Unexpected error: %s \n' % e
        else:
            text = 'No permission boundary for %s.' % name
            pass

    return text


def list_iam_roles(iam_client, arn_list):
    keep_searching = True
    marker = None
    while keep_searching:
        if marker:
            response = iam_client.list_roles(MaxItems=LIST_MAX_ITEMS, Marker=marker)
        else:
            response = iam_client.list_roles(MaxItems=LIST_MAX_ITEMS)
        keep_searching = response['IsTruncated']
        if keep_searching:
            marker = response['Marker']

        build_iam_entities_arn_list(response, arn_list)


def list_iam_users(iam_client, arn_list):
    keep_searching = True
    marker = None
    while keep_searching:
        if marker:
            response = iam_client.list_users(MaxItems=LIST_MAX_ITEMS, Marker=marker)
        else:
            response = iam_client.list_users(MaxItems=LIST_MAX_ITEMS)
        keep_searching = response['IsTruncated']
        if keep_searching:
            marker = response['Marker']

        build_iam_entities_arn_list(response, arn_list)


def build_iam_entities_arn_list(response, name_list):
    if 'Roles' not in response and 'Users' not in response:
        return
    if 'Roles' not in response:
        response_type = 'Users'
    else:
        response_type = 'Roles'
    for entity in response[response_type]:
        name = entity['Arn'].rsplit(':', 1)[-1]
        name = name.rsplit('/')[-1]
        name_list.append(name)


def get_all_iam_entities_arns(iam_client, iam_entities_names):
    list_iam_users(iam_client, iam_entities_names['Users'])
    list_iam_roles(iam_client, iam_entities_names['Roles'])
    return iam_entities_names

def get_iam_entity_type(entity_arn):
    name = entity_arn.rsplit(':', 1)[-1]
    type_name = name.split('/')

    return type_name[0], type_name[1]

def get_bot_specific_configuration(params):
    entity_name = None
    cloud_account_id = None
    dry_run = None
    for idx, param in enumerate(params):
        if 'entity_arn' in param:
            _, entity_name = param.split('entity_arn=')
        elif '--dryRun' in param:
            dry_run = True
        elif 'cloud_account_id=' in param:
            _, cloud_account_id = param.split('cloud_account_id=')

    return dry_run, entity_name, cloud_account_id


def describe_functionality(entity_name, cloud_account_id):
    text = 'The bot configuration is set to dry run once enabled the next actions will be conducted:\n'
    account_id = ' in %s' % cloud_account_id
    if entity_name == 'all':
        text = text + '1. List all IAM entities%s.\n' % account_id
        text = text + '2. Remove permission boundary from all listed entities.\n'
    else:
        text = text + '1. Will remove permission boundary from %s.\n' % entity_name
    return text


def run_action(boto_session, rule, entity, params):
    text_output = ''
    iam_entities_names = {'Roles': [], 'Users': []}
    dry_run = False

    iam_client = boto_session.client('iam')

    dry_run, entity_arn, cloud_account_id = get_bot_specific_configuration(params)

    if dry_run:
        return describe_functionality(entity_arn, cloud_account_id)

    try:
        if cloud_account_id is not None and entity_arn == 'all':
            iam_entities = get_all_iam_entities_arns(iam_client, iam_entities_names)
            text_output = text_output + 'Listed all iam entities of cloud account %s.\n' % cloud_account_id
            for role in iam_entities['Roles']:
                remove_role_permission_boundary(iam_client, role)
            for user in iam_entities['Users']:
                remove_user_permission_boundary(iam_client, user)
            text_output = text_output + 'Removed all iam entities permission boundary.\n'
        elif entity_arn == 'all':
            text_output = text_output + 'Remove all permissions boundary must have cloud account id parameter supplied\n'
        else:
            entity_type, name = get_iam_entity_type(entity_arn)
            if entity_type == 'role':
                remove_role_permission_boundary(iam_client, name)
                text_output = text_output + 'Removed role:%s permission boundary.\n' % entity_arn
            elif entity_type == 'user':
                remove_user_permission_boundary(iam_client, name)
                text_output = text_output + 'Removed user:%s permission boundary.\n' % entity_arn
            else:
                text_output = text_output + 'Unsupported entity: %s, skipping.\n' % entity_arn
    except ClientError as e:
        text_output = text_output + 'Unexpected error: %s \n' % e

    return text_output
