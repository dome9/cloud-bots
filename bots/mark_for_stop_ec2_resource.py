'''
## mark_for_stop_ec2_resource
Description: Tags an ec2 resource with "marked_for_stop" and <current epoch time>.
Required Permissions: ec2:CreateTags
Usage: AUTO: mark_for_stop_ec2_resource <time><unit(m,h,d)>
Example: AUTO: mark_for_stop_ec2_resource 3h
Note: This is meant to be used in conjunction with a more aggressive action like stopping or termanating an instance. The first step will be to tag an instance with the time that we want to tigger the remediation bot. 
From there, a rule like "Instance should not have tags with [ key='marked_for_stop' and value before(1, 'minutes') ]" can be ran to check how long an instance has had the 'mark for stop' tag. 
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
import re

def run_action(boto_session,rule,entity,params):
    instance = entity['id']

    print("Start execute Instance mark for stope for instance - %s" % instance)

    # Take in the params and find the epoch time to mark for stop
    try:
        matches = re.findall('(\d+)([mMhHdD])', params[0])
        number = int(matches[0][0]) # The 1 in 1h for example
        unit = matches[0][1].lower() # days hours or minutes

        if unit == "m":
            seconds = 60
        elif unit == "h":
            seconds = 3600
        elif unit == "d":
            seconds = 86400

        total_seconds = seconds * number
        current_time = int(time.time())

        mark_for_stop_time = current_time + total_seconds

    except IndexError:
        text_output = "Mark for stop time not properly formatted in input params. Please check and try again\nUsage: AUTO: mark_for_stop_ec2_resource <time><unit(m,h,d)>\nExample: AUTO: mark_for_stop_ec2_resource 3h\n"
        return text_output


    ec2_client = boto_session.client('ec2')
    result = ec2_client.create_tags(
        Resources=[instance],
        Tags=[
            {
                'Key': "marked_for_stop",
                'Value': str(mark_for_stop_time)
            }
        ]
    )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance tagged: %s \nKey: %s | Value: %s \n" % (instance,"marked_for_stop",str(mark_for_stop_time))

    return text_output




