'''
## s3_limit_access
What it does: Removes policies for the following actions for principals '*':
s3:Delete*, s3:Get*, s3:List*, s3:Put*, s3:RestoreObject and s3:*.
Usage: AUTO: s3_limit_aceess
Notes: The bot Removes these actions from the policy. if this is the only action, the whole policy will be removed.
If necessary, modify the policy after the deletation, to limit the access to specific principals.
Limitations: The bot removes the policies for *all* the mentioned actions, if exist.
'''

from botocore.exceptions import ClientError
import re
import json
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'

def check_match(action):
    return re.match('^s3:Delete', action) or re.match('^s3:Get', action) or re.match('^s3:List', action) or re.match('^s3:Put', action) or re.match('s3:RestoreObject', action) or re.match('s3:*', action) or action == '*'


def handle_object(policy_statement, obj, action, text_output):
    # Removes the action from the policy statement.
    # if there is a list of action, will remove only the desired one.
    # if there is only one action, the object will be completely removed.
    if type(obj['Action']) is str:
        try:
            policy_statement.remove(obj)
            text_output = text_output + f'Object with Action {action} will be completely removed. \n'
        except Exception as e:
            text_output = text_output + f'Couldnt remove object with action {action}. Error: {e} \n'
    elif type(obj['Action']) is list:
        try:
            obj['Action'].remove(action)
            text_output = text_output + f'Action {action} will be removed from the actions list. \n'
            if len(obj['Action']) == 0:  # if this is the only action left, we can remove the whole object
                policy_statement.remove(obj)
                text_output = text_output + f'All actions will be removed from the object. deleting the object from the statement. \n'
        except Exception as e:
            text_output = text_output + f'Couldnt remove action {action}. Error: {e} \n'

    return policy_statement, text_output


def update_policy_statement(policy_statement, text_output):
    allow_all_objects = [obj for obj in policy_statement if obj['Effect'] == 'Allow' and (obj['Principal'] == '*' or obj['Principal']['AWS'] == '*')]

    for obj in allow_all_objects:
        if obj['Action'] is None:
            continue
        elif type(obj['Action']) is str:  # one action
            actions = [obj['Action']]
        elif type(obj['Action']) is list:  # list of actions
            actions = obj['Action']

        for action in actions:
            match = check_match(action)
            if match:
                policy_statement, text_output = handle_object(policy_statement, obj, action, text_output)
            else:
                continue

    return policy_statement, text_output


def run_action(boto_session, rule, entity, params):
    # Create an S3 client
    s3_client = boto_session.client('s3')
    bucket = entity['name']
    text_output = ''

    try:

        # Get bucket's policy (TYPE: DICTIONARY)
        policy = s3_client.get_bucket_policy(Bucket=bucket)['Policy']
        policy = json.loads(policy)
        # Get bucket's policy statement (TYPE: ARRAY, each object is dictionary)
        policy_statement = policy['Statement']

        new_policy_statement, text_output = update_policy_statement(policy_statement, text_output)
        policy['Statement'] = new_policy_statement

        if len(policy['Statement']) == 0:
            # all objects removed, delete all policy:
            result = s3_client.delete_bucket_policy(
                Bucket=bucket,
            )
            text_output = text_output + f"All the objects in the policy were risky and removed, the policy is now empty. \n"

        else:
            # Serializing json
            final_policy = json.dumps(policy)

            result = s3_client.put_bucket_policy(
                Bucket=bucket,
                Policy=final_policy
            )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "Bucket policy updated for: %s \nYou may want to update the policy manually for specific principals." % bucket


    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output

