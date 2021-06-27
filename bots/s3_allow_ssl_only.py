"""
## s3_enforce_ssl_data_encryption
What it does: force s3 bucket to accept only ssl requests
Usage: AUTO: s3_enforce_ssl_data_encryption
Limitations: none
"""

import boto3
from botocore.exceptions import ClientError
import json

UPDATE = 1
CREATE = 2

### work flow
    # check if the bucket has policy
    # edit or add policy that denny data not encrypted with ssl

def create_statement_block(bucket_arn):
    statement_block = [
        {
            "Sid": "AllowSSLRequestsOnly",
            "Action": "s3:*",
            "Effect": "Deny",
            "Resource": [
                f"{bucket_arn}",
                f"{bucket_arn}/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            },
            "Principal": "*"
        }
    ]

    return statement_block

def check_bucket_policy(bucket_policy):
    """
    return if we need to edit or create policy
    """
    # if this fails 3 times this means that the bucket has no policy
    for attempt in range(3):
        try:
            # try to access the bucket policy
            bucket_policy.policy
            return UPDATE
        except:
            # tries another time
            pass

    return CREATE

def update_policy(bucket_arn, bucket_policy):
    bucket_policy_document = json.loads(bucket_policy.policy)

    statement_block = create_statement_block(bucket_arn)[0]

    # append the statement block to the policy document
    bucket_policy_document['Statement'].append(statement_block)

    return json.dumps(bucket_policy_document)


def create_policy(bucket_arn, bucket_policy):
    policy_document = {
        "Id" : 'ssl-requests-only',
        "Version": "2012-10-17",
        "Statement": create_statement_block(bucket_arn)}

    return json.dumps(policy_document)

def run_action(session, rule, entity, params):
    s3_resource = session.resource('s3')

    # get bucket properties
    bucket_arn = entity['arn']
    bucket_name = entity['name']

    bucket_policy = s3_resource.BucketPolicy(bucket_name)

    switch_case = {UPDATE : update_policy, CREATE : create_policy}

    policy_document = switch_case[check_bucket_policy(bucket_policy)](bucket_arn, bucket_policy)

    output_text = ''
    try:
        response = bucket_policy.put(
            ConfirmRemoveSelfBucketAccess=True,
            Policy=policy_document,)
        output_text = f'Updated policy to bucket: {bucket_arn}'
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return output_text
