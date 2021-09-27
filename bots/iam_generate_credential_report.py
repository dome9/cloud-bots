"""
## iam_generate_credential_report
What it does: Generates a credential report for the account.
Usage: AUTO iam_generate_credential_report
"""

from botocore.exceptions import ClientError
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'

def run_action(boto_session, rule, entity, params):

    iam_client = boto_session.client('iam')
    text_output = ''
    complete = False

    try:
        print(f'{__file__} - Trying to generate the credential report... \n')
        while not complete:
            result = iam_client.generate_credential_report()
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s \n" % str(result)
                return text_output
            complete = result['State'] == 'COMPLETE'

        print(f'{__file__} - Done. \n')
        text_output = text_output + f'Successfully generated a credential report. \n'

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output
