
"""
## s3_block_all_public_access
What it does: turn on S3 Bucket's Block all Public Access : Block public access to buckets and objects granted
through Future New AND Existing public ACLs and Bucket Policies.

Usage:  s3_block_public_all_access

Limitations: none

Notes:
    -  before running this bot, ensure that your applications will work correctly without public access
"""

import boto3
from botocore.exceptions import ClientError

text_output = ''


def run_action(boto_session, rule, entity, params):
    # Create an S3 client
    s3 = boto_session.client('s3')
    # get bucket id from entity
    bucket_id = entity['id']
    global text_output

    # -----------------------  Block public access ----------------------------------#
    try:
        # -------call S3 to block all public access --------#
        result = s3.put_public_access_block(
            Bucket=bucket_id,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        text_output = text_output + "Bucket's Public Access Block enabled: %s" % bucket_id + ', ' \
                                    'NEW and OLD public ACLs and Bucket Policies are Blocked now. '

    except ClientError as e:
        text_output = text_output + "Unexpected error: %s \n" % e

    return text_output


