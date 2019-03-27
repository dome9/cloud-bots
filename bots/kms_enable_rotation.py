


'''
## kms_enable_rotation
What it does: Enables rotation on a KMS key
Usage: AUTO: kms_enable_rotation
Sample GSL: KMS where isCustomerManaged=true should have rotationStatus=true  
Limitations: Edits can not be made to AWS maged keys. Only customer managed keys can be edited.   
'''

import boto3

def run_action(boto_session,rule,entity,params):
    key = entity['id']
    kms_client = boto_session.client('kms')
    
    result = kms_client.enable_key_rotation(
        KeyId=key
    )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s " % str(result)
    else:
        text_output = "Key rotation enabled for key: %s " % entity['name']

    return text_output 


