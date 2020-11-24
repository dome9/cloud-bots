'''
## delete_key_pair
What it does: Deletes a key pair
Usage: AUTO: delete_key_pair
Limitations: none
'''
import boto3
from botocore.exceptions import ClientError

### Delete EC2 Key Pair ###
def run_action(boto_session, rule, entity, params):
    #Get the key name
    keypair = entity.get('id')

    try:
        #Delete the keypair
        ec2_client = boto_session.client('ec2')
        result = ec2_client.delete_key_pair(KeyName=keypair)

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e
        return text_output

    #Check if the keypair was deleted
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Keypair %s was deleted successfully\n" % keypair

    return text_output