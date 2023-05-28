"""
## mark_for_stop_ec2_resource
What it does: Tags an ec2 resource with "marked_for_stop" and <current epoch time>.
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
"""

import time
import re

from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    instance = entity['id']

    print(f'{__file__} - mark_for_stop_ec2_resource.py - Start execute Instance mark for stope for instance - {instance}')

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
        raise Exception("Mark for stop time not properly formatted in input params. Please check and try again\n"
                        "Usage: AUTO: mark_for_stop_ec2_resource <time><unit(m,h,d)>\n"
                        "Example: AUTO: mark_for_stop_ec2_resource 3h\n")

    ec2_client = boto_session.client('ec2')
    try:
        result = ec2_client.create_tags(
            Resources=[instance],
            Tags=[
                {
                    'Key': "marked_for_stop",
                    'Value': str(mark_for_stop_time)
                }
            ]
        )

        response_code = result['ResponseMetadata']['HTTPStatusCode']
        if response_code >= 400:
            raise Exception("Unexpected error: %s \n" % str(result))
        else:
            text_output = "Instance tagged: %s \nKey: %s | Value: %s \n" % (instance, "marked_for_stop", str(mark_for_stop_time))

        return text_output
    except ClientError as e:
        if 'InvalidId' in e.response['Error']['Code']:
            raise Exception('The provided instance id is not valid')
        else:
            raise e




