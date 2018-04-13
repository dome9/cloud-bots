'''
## tag_ec2_resource
What it does: Tags an ec2 instance  
Usage: AUTO: tag_ec2_resource <key> <value>  
Note: Tags with spaces can be added if they are surrounded by quotes: ex: tag_ec2_resource "this is my key" "this is a value"
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
import re

#Tags with spaces can be added if they are surrounded by quotes: ex: ec2_tag_instance "this is my key" "this is a value"
def run_action(boto_session,rule,entity,params):
    instance = entity['id']

    if len(params) == 2: #Standard key value formatting
        key = params[0]
        value = params[1]

    else:
        #Bring the params together to parse and look for quotes
        both_tags = " ".join(params)

        if "\"" not in both_tags: 
            text_output = ("Tag \"%s\" does not follow formatting - skipping\n" % both_tags) # String is formatted wrong. Fail/exit
            return text_output

        #Capture text blocks in quotes or standalones
        pattern = re.compile("[(A-Za-z0-9_\.,\s-]*")

        matched_tags = re.findall(pattern, both_tags)
        both_tags_no_spaces = [x.strip(' ') for x in matched_tags] # Remove empty spaces in array
        both_tags_no_spaces[:] = [x for x in both_tags_no_spaces if x != ''] # Remove empty array elements
        
        key = both_tags_no_spaces[0]
        value = both_tags_no_spaces[1]

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




