import boto3

### DeleteS3Bucket ###
def run_action(rule,entity,params):
    bucket = entity['Id']
    
    s3 = boto3.client('s3')
    result = s3.delete_bucket(Bucket=bucket)

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Bucket deleted. Id: %s \n" % (bucket)

    return text_output