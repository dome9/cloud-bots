import boto3
import json
import os
from botocore.exceptions import ClientError

### DeleteS3Bucket ###
def run_action(message):
	# Create an S3 client
	s3 = boto3.client('s3')

	bucket = message['Entity']['Id']
	
	try:
		# Call S3 to delete the given bucket
		output = s3.delete_bucket(Bucket=bucket)
		text_output = ("Bucket successfully deleted" + bucket + "\n")

	except (ClientError, AttributeError) as e:
		error = e.response['Error']['Code']
		if error == 'NoSuchBucket':
	 		text_output = ("Bucket " + bucket + " doesn't exist. Skipping")
	 	else:
			text_output = ("Unexpected error: %s" % e + "\n")

	return text_output