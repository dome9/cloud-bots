"""
## kms_cmk_enable_key
What it does: Enables a kms cmk (customer managed key),
Usage: kms_cmk_enable_key
"""

from botocore.exceptions import ClientError
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'

def run_action(boto_session, rule, entity, params):

    key_arn = entity['arn']
    key_state = entity['keyState']
    client = boto_session.client('kms')
    text_output = ''

    print(f'{__file__} - Key arn: {key_arn} \n Current State: {key_state}. \n')

    if key_state == 'PendingDeletion':
        try:
            print(f'{__file__} - Trying to cancel key deletion... \n')
            result = client.cancel_key_deletion(KeyId=key_arn)
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s \n" % str(result)
                return text_output
            else:
                print(f'{__file__} - Done. Current key state is Disabled. \n')

        except ClientError as e:
            text_output = f"Unexpected client error: {e} \n"
            if 'AccessDenied' in e.response['Error']['Code']:
                text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
            return text_output
    try:
        print(f'{__file__} - Trying to enable key... \n')
        result = client.enable_key(KeyId=key_arn)
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            print(f'{__file__} - Done. Current key state is Enabled. \n')
            text_output = text_output + f'Successfully set the key state to enabled. Key arn: {key_arn} \n'

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output

