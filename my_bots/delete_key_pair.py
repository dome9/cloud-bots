'''
## delete_key_pair
What it does: Deletes a key pair
Usage: AUTO: delete_key_pair
Limitations: none
'''
import boto3

### Delete EC2 Key Pair ###
def run_action(boto_session,rule,entity,params):
    #Get the key name and delete the keypair
    keypair = entity['id']
    ec2_client = boto_session.client('ec2')
    result = ec2_client.delete_key_pair(KeyName=keypair)

    #Check if the keypair was deleted
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Keypair deleted: %s \n" % keypair

    return responseCode