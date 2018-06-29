'''
## ec2_release_eips
What it does: Disassociates and releases all EIPs on an instance
Usage: AUTO: ec2_release_eips
Limitations: none  
'''

import boto3

def run_action(boto_session,rule,entity,params):
    text_output = ""
    instance = entity['id']
    ec2_client = boto_session.client('ec2')
    
    # Get the allocation id(s) from the instance
    describe_response = ec2_client.describe_addresses(
        Filters=[
            {
                'Name': 'instance-id',
                'Values': [instance]
            }
        ]
    )

   
    addresses = describe_response['Addresses']
    print(addresses) #for debugging

    if len(addresses) > 0:
        for address in addresses:
            allocation_id = address['AllocationId']

            result = ec2_client.release_address(AllocationId=allocation_id)

            text_output = text_output + "Released EIP: %s \n" % address['PublicIp']

    else:
        text_output = "No EIPs found. Nothing to release.\n"
        return text_output 

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = text_output + "Unexpected error: %s \n" % str(result)

    return text_output 


