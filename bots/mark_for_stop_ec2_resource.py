'''
## mark_for_stop_ec2_resource
What it does: Tags an ec2 resource with "marked_for_stop" and <current epoch time>.   
Usage: AUTO: mark_for_stop_ec2_resource
Note: This is meant to be used in conjunction with a more aggressive action like stopping or termanating an instance. The first step will be to tag an instance with the time that the failure was found. 
From there, a rule like "Instance should not have tags with [ key='marked_for_stop' and value before(-7, 'days') ]" can be ran to check how long an instance has had the 'mark for stop' tag. 
Limitations: none

## THIS WORKS ACROSS ALL EC2 RELATED SERVICES:
* Image
* Instance
* InternetGateway
* NetworkAcl
* NetworkInterface
* PlacementGroup
* RouteTable
* SecurityGroup
* Snapshot
* Subnet
* Volume
* Vpc
* VpcPeeringConnection
'''

import boto3
import time

def run_action(boto_session,rule,entity,params):
    instance = entity['id']

    value = str(int(time.time()))
    key = "marked_for_stop"

    ec2_client = boto_session.client('ec2')
    result = ec2_client.create_tags(
        Resources=[instance],
        Tags=[
            {
                'Key': key,
                'Value': value
            }
        ]
    )
    
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance tagged: %s \nKey: %s | Value: %s \n" % (instance,key,value)

    return text_output




