'''
## vpc_remove_inet_gw
What it does: Remove the Internet Gateway from a VPC and deletes it
Usage: AUTO: vpc_remove_inet_gw
'''

import boto3
from botocore.exceptions import ClientError


# Main function
def run_action(boto_session,rule,entity,params): 
    text_output = "";

    try:
        # Setup variables
        vpc_id = entity['id']
        inet_gw_id = entity['internetGateways'][0]['externalId']
        text_output += "VPC: %s Gateway: %s\n" % (vpc_id, inet_gw_id)
        
        client = boto3.client('ec2')
        client.detach_internet_gateway(InternetGatewayId = inet_gw_id, VpcId = vpc_id)
        client.delete_internet_gateway(InternetGatewayId = inet_gw_id)

    except Exception as e:
        text_output += "\n Error: %s \n" % e
    
    return text_output


