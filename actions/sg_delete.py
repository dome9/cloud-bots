import boto3
import json
import os
from botocore.exceptions import ClientError

### DeleteSecurityGroup ###
def main(message,event_log):
	region = message['Entity']['Region']
	region = region.replace("_","-")

	sg_id = message['Entity']['Id']
	ec2 = boto3.resource('ec2', region_name=region)

	try:
		delete_sg = ec2.SecurityGroup(sg_id).delete()
		event_log.append("Security Group " + sg_id + " successfully deleted\n")
		
	except (ClientError, AttributeError) as e:
		error = e.response['Error']['Code']
		if error == 'DependencyViolation':
			event_log.append("Security group (id: " + sg_id + ") Still has assets attahced to it. Can't delete / Skipping.\n")
		else:	
			event_log.append("Unexpected error: %s" % e + "\n")
		#Add in "SG is in use error. Dump current attachments"

	return(event_log)