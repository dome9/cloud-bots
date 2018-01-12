import boto3
import json
import os
from botocore.exceptions import ClientError

### DeleteSecurityGroupRules ###
def run_action(message):
    sg_id = message['Entity']['Id']
    region = message['Entity']['Region']
    region = region.replace("_","-")

    try:
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
        try:
            deleteIngress = sg.revoke_ingress(IpPermissions=sg.ip_permissions)
            deleteIngressMsg = "Security Group " + sg_id + " ingress rules successfully deleted\n"
            text_output = text_output + deleteIngressMsg

        except (ClientError, AttributeError) as e:
            error = e.response['Error']['Code']
            if error == 'MissingParameter':
                 text_output = text_output + "Security Group " + sg_id + " does not have any inbound rules. Checking outbound next.\n"
            else:
                text_output = text_output + "Unexpected error: %s" % e + "\n")

        #Try to delete outbound rules if they exist
        try:
            deleteEgress = sg.revoke_egress(IpPermissions=sg.ip_permissions_egress)
            #deleteEgressMsg = "Security Group " + sg_id + " egress rules successfully deleted\n"
            text_output = text_output + "Security Group " + sg_id + " egress rules successfully deleted\n"
        except (ClientError, AttributeError) as e:
            error = e.response['Error']['Code']
            if error == 'MissingParameter':
                 text_output = text_output + "Security Group " + sg_id + " does not have any outbound rules. Skipping.\n"
            else:
                text_output = text_output + "Unexpected error: %s" % e + "\n"

    except (ClientError, AttributeError) as e:
        text_output = "Unexpected error: %s" % e + "\n"

    return text_output
