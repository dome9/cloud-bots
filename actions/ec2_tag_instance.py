import boto3
import json
import os
import re
from botocore.exceptions import ClientError

### Add Tags to EC2 ###
#Tag format: AUTO: EC2_tag_instance (key:value)"
def run_action(message,event_log):
	#House keeping - set up variables	
	instance = message['Entity']['Id']
	region = message['Entity']['Region']
	region = region.replace("_","-")
	compliance_tags = message['Rule']['ComplianceTags'].split("|")

	#initialize ec2
	ec2 = boto3.client('ec2', region_name=region)

	for tag in compliance_tags:
		tag = tag.strip() #Sometimes the tags come through with trailing or leading spaces. 
		remediate_tag = re.match(r'AUTO:\sec2_tag_instance\s\((?P<key>.+):(?P<value>.+)\)', tag) #we just want the tag that matches "AUTO: ec2_tag_instance (key:value)"

		if remediate_tag:
			key = remediate_tag.group(1)
			value = remediate_tag.group(2)

			try:	
				#Apply the tags
				tag_instance = ec2.create_tags(
				    Resources=[instance],
				    Tags=[
				        {
				            'Key': key,
				            'Value': value
				        }
				    ]
				)
				
				responseCode = tag_instance['ResponseMetadata']['HTTPStatusCode']

				if responseCode >= 400:
					event_log.append("Unexpected error:" + tag_instance + "\n")
				else:
					event_log.append("Instance tagged: " + instance + "\nKey: " + key + " | Value: " + value + " \n")

			except (ClientError, AttributeError) as e:
				event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)


