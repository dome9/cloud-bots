'''
## ec2_delete_key_pair
What it does: Deletes a key pair
Usage: AUTO: ec2_delete_key_pair
Sample GSL: cloudtrail where event.name='CreateKeyPair'
Limitations: None
'''
from botocore.exceptions import ClientError

### Delete EC2 Key Pair ###
def run_action(boto_session, rule, entity, params):
    #Get the key name
    keypair = entity.get('id')

    try:
        #Delete the keypair
        ec2_client = boto_session.client('ec2')
        result = ec2_client.delete_key_pair(KeyName=keypair)
        text_output = f"Keypair {keypair} was deleted successfully.\n"

    except ClientError as e:
        text_output = f"Client error: {e}.\n"

    return text_output