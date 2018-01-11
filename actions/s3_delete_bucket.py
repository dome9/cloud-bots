import boto3
import json
import os
from botocore.exceptions import ClientError

### DeleteS3Bucket ###
def main(message,event_log):
	# Create an S3 client
	s3 = boto3.client('s3')

	bucket = message['Entity']['Id']
	
	try:
		# Call S3 to delete the given bucket
		output = s3.delete_bucket(Bucket=bucket)
		event_log.append("Bucket successfully deleted" + bucket + "\n")

	except (ClientError, AttributeError) as e:
		error = e.response['Error']['Code']
		if error == 'NoSuchBucket':
	 		event_log.append("Bucket " + bucket + " doesn't exist. Skipping")
	 	else:
			event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)