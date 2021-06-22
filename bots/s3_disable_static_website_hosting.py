"""
## s3_disable_website_static_hosting
What it does: deletes ant s3 static website hosting
Usage: s3_disable_website_static_hosting
Example: s3_disable_website_static_hosting
Limitations: None
"""

import boto3
from botocore.exceptions import ClientError

def run_action(boto_session, rule, entity, params):
    s3_resource = boto_session.resource('s3')

    bucket_name = entity['name']
    bucket_website = s3_resource.BucketWebsite(bucket_name)

    text_output = ''
    try:
        bucket_website.delete()
        text_output = f'Disabled static website hosting from Bucket : {bucket_name}'
    except ClientError as e:
        text_output = text_output + f'Unexpected error: {e}.'

    return text_output
