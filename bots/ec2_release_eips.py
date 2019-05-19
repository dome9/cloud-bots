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
    print("Dome9 Cloud bots - ec2_release_eips.py - {}".format(addresses)) #for debugging

    if len(addresses) > 0:
        for address in addresses:
            #Instances not in the default VPC need to be disassociated before they can be released
            association_id = address['AssociationId']
            disassociate_result = ec2_client.disassociate_address(AssociationId=association_id)

            responseCode = disassociate_result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = "Unexpected error: %s \n" % str(disassociate_result)
                return text_output 
            else:
                text_output = text_output + "Disassociated EIP: %s \n" % address['PublicIp']


            allocation_id = address['AllocationId']
            release_result = ec2_client.release_address(AllocationId=allocation_id)

            responseCode = release_result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = "Unexpected error: %s \n" % str(release_result)
                return text_output 
            else:
                text_output = text_output + "Released EIP: %s \n" % address['PublicIp']

    else:
        text_output = "No EIPs found. Nothing to release.\n"

    return text_output 



