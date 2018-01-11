import boto3
import json
import os
from botocore.exceptions import ClientError

### DeleteS3BucketPermissions ###
def main(message,event_log):
	# Create an S3 client
	s3 = boto3.client('s3')

	bucket = message['Entity']['Id']

	try:
		#sendEvent out the S3 permissions first so we can reference them later
		bucket_policy = s3.get_bucket_policy(Bucket=bucket)['Policy']
		str_bucket_policy = "Bucket policy that will be deleted: \n " + str(bucket_policy) + "\n"
		event_log.append(str_bucket_policy)
		
		#Call S3 to delete the bucket policy for the given bucket
		bucket_policy_delete_output = s3.delete_bucket_policy(Bucket=bucket)
		
		responseCode = bucket_policy_delete_output['ResponseMetadata']['HTTPStatusCode']
		if responseCode >= 400:
			event_log.append("Unexpected error: %s" % bucket_policy_delete_output + "\n")
		else:
			event_log.append("Bucket policy deleted: " + bucket + " \n")	

	except (ClientError, AttributeError) as e:
		error = e.response['Error']['Code']
		if error == 'NoSuchBucketPolicy':
	 		event_log.append("Bucket " + bucket + " does not have a bucket policy. Checking ACLs next.\n")
		else:
			event_log.append("Unexpected error: %s" % e + "\n")

	try:
		#list bucket ACLs
		bucket_acls = s3.get_bucket_acl(Bucket=bucket)['Grants']
		
		if len(bucket_acls) == 1:
			event_log.append("Only the CanonicalUser ACL found. Skipping.\n")
		else:
			str_bucket_acls = "ACLs that will be removed: \n " + str(bucket_acls) + "\n"
			event_log.append(str_bucket_acls)

			# Unset the bucket ACLs
			acl_delete_output = s3.put_bucket_acl(Bucket=bucket,ACL='private')
		
			responseCode = acl_delete_output['ResponseMetadata']['HTTPStatusCode']
			if responseCode >= 400:
				event_log.append("Unexpected error: %s" % acl_delete_output + "\n")
			else:
				event_log.append("Bucket ACL deleted: " + bucket + " \n")	
	
	except (ClientError, AttributeError) as e:
		event_log.append("Unexpected error: %s" % e + "\n")

	return(event_log)
