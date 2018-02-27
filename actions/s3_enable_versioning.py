import boto3

##### YOU HAVE TO BE THE BUCKET OWNER FOR THIS TO WORK ####

## Turn on S3 bucket versioning
def run_action(rule,entity,params):
    bucket_name = entity['id']
    s3 = boto3.resource('s3')
    bucket_versioning = s3.BucketVersioning(bucket_name)
    result = bucket_versioning.enable()

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Bucket versioning enabled: %s \n" % bucket_name

    return text_output 
