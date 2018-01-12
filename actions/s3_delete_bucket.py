import boto3
from botocore.exceptions import ClientError

### DeleteS3Bucket ###
def run_action(rule,entity,params):
    # Create an S3 client
    s3 = boto3.client('s3')

    bucket = entity['Id']
    
    try:
        # Call S3 to delete the given bucket
        output = s3.delete_bucket(Bucket=bucket)
        text_output = "Bucket successfully deleted %s \n" % bucket

    except (ClientError, AttributeError) as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchBucket':
            text_output = "Bucket %s doesn't exist. Skipping" % bucket
        else:
            text_output = "Unexpected error: %s \n" % e

    return text_output