'''
## sg_rules_delete
What it does: Deletes all ingress and egress rules from a SG  
Usage: AUTO: sg_rules_delete  
Limitations: none  
'''

import boto3
from botocore.exceptions import ClientError

### DeleteSecurityGroupRules ###
def run_action(rule,entity,params):

    sg_id = entity['id']
    region = entity['region']
    region = region.replace("_","-")

    ec2_client = boto3.client('ec2', region_name=region)
    #Get the SG info
    sgInformation = ec2_client.describe_security_groups(GroupIds=[sg_id])

    #Save the inbound/outbound rules for logging/forensics
    egressRules = sgInformation['SecurityGroups'][0]['IpPermissionsEgress']
    
    text_output = "Egress rules to be deleted: " + str(egressRules) + "\n"

    ingressRules = sgInformation['SecurityGroups'][0]['IpPermissions']
    text_output = text_output + "Ingress rules to be deleted: " + str(ingressRules) + "\n"

    #New client for making changes
    ec2_resource = boto3.resource('ec2', region_name=region)
    sg = ec2_resource.SecurityGroup(sg_id)

    #Try to delete inbound rules if they exist
    if ingressRules:
        #An IP permission may contain a group name or a group ID, but not both. This removes the group name from the rules to we just have the ID
        for i, v in enumerate(ingressRules):
            try:
                del ingressRules[i]['UserIdGroupPairs'][0]['GroupName']
            except Exception as e: 
                        print("No groupName to clean up - deleting rules")
        result = sg.revoke_ingress(IpPermissions=ingressRules)

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "Security Group ingress rules successfully deleted\n"
    else:
        text_output = text_output + "Security Group does not have any inbound rules. Checking outbound next.\n"   

    #Try to delete outbound rules if they exist
    if egressRules:
        #An IP permission may contain a group name or a group ID, but not both. This removes the group name from the rules to we just have the ID
        for i, v in enumerate(egressRules):
            try:
                del egressRules[i]['UserIdGroupPairs'][0]['GroupName']
            except Exception as e: 
                        print("No groupName to clean up - deleting rules")
        result = sg.revoke_egress(IpPermissions=egressRules)
        
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "Security Group egress rules successfully deleted\n"

    else:
        text_output = text_output + "Security Group does not have any outbound rules.\n"   

    return text_output
