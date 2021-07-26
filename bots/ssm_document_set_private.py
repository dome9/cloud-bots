"""
## ssm_document_set_private
What it does: removes all aws account that can access the file except of the one that pass as a param.
Note that the account ID's should be separated by column.
Usage: ssm_document_set_private AccountIdToAdd=<account_id_1>,<account_id_2>
Example: ssm_document_set_private
Limitations: None
"""

from botocore.exceptions import ClientError


PARAM_NAME = "AccountIdToAdd"


def run_action(boto_session, rule, entity, params):
    client = boto_session.client('ssm')
    document_name = entity['name']

    # check if there is any accountId to add..
    # If there is no account id then return empty list.
    account_to_add = params[PARAM_NAME].split(',') if PARAM_NAME in params.keys() else []

    text_output = ''
    try:
        response = client.modify_document_permission(
            Name=document_name,
            PermissionType='Share',
            AccountIdsToAdd=account_to_add,  # add the account that passes as a param.
            AccountIdsToRemove=['All']  # removes all account id (sets the document to private).
        )

        text_output = f'Removed all account id access except from: {account_to_add}' \
            if response['ResponseMetadata']['HTTPStatusCode'] == 200 else 'Unexpected error'
    except ClientError as error:
        text_output = f'Unexpected error: {error}'

    return text_output
