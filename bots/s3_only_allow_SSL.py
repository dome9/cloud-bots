"""
## s3_only_allow_SSL
What it does: Ensure that S3 Buckets enforce encryption of data transfers using Secure Sockets Layer (SSL)
Usage: AUTO: s3_only_allow_SSL
Note: The bot looks at the bucket policy and adds to the current policy the missing actions(s3:GetObject and s3:PutObject)
      and the SSL statement.
      if no policy in the bucket an SSL policy will add to the bucket
Limitations: none
"""

import json
from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    # create a s3 sessions
    s3_client = boto_session.client('s3')

    bucket_name = entity['name']
    account_number = entity["accountNumber"]
    policy_bucket = entity['policy']

    try:
        if policy_bucket == "null":  # s3 does not have a bucket policy
            policy = json.dumps(make_new_policy(bucket_name, account_number))

        else:  # bucket has a policy
            res = get_correct_policy(policy_bucket)
            first_Effect, second_Effect = get_actions(bucket_name, account_number, res)
            if second_Effect is None:  # if there is only one Effect to add to the bucket policy
                policy_bucket['Statement'].append(first_Effect)
                policy = json.dumps(policy_bucket)
            else:
                policy_bucket['Statement'].append(first_Effect)
                policy_bucket['Statement'].append(second_Effect)
                policy = json.dumps(policy_bucket)
        print(policy)
        result = s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "SSL policy add to bucket: %s" % bucket_name

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


# This Function find witch actions in the bucket policy and return a list with the actions that relevant to the ssl
def get_correct_policy(policy_bucket):
    run = policy_bucket['Statement']
    res = []
    options = ["s3:GetObject", "s3:*", "s3:PutObject", "s3:Put*", "s3:Get*", "*"]

    for action in run:
        if action["Effect"] == "Allow":
            res = [ele for ele in action['Action'] if (ele in options)]

    return res


# The function find which actions should add to policy and return the missing Effects in a json format
def get_actions(bucket_name, account_number, options):
    if ("*" in options) or ("s3:*" in options) or ('s3:GetObject' in options and 's3:PutObject' in options) or (
            's3:Get*' in options and 's3:Put*' in options):
        Effect = {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::" + bucket_name + "/*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
        return Effect, None

    elif 's3:GetObject' in str(options) or "s3:Get*" in str(options):
        first_Effect = {
            "Effect": "Allow",
            "Principal": {
                "AWS": account_number
            },
            "Action":
                's3:PutObject',
            "Resource": "arn:aws:s3:::" + bucket_name + "/*"
        }
        second_Effect = {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::" + bucket_name + "/*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
        return first_Effect, second_Effect
    elif 's3:PutObject' in str(options) or "s3:Put*" in str(options):
        first_Effect = {
            "Effect": "Allow",
            "Principal": {
                "AWS": account_number
            },
            "Action":
                's3:GetObject',
            "Resource": "arn:aws:s3:::" + bucket_name + "/*"
        }
        second_Effect = {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::" + bucket_name + "/*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
        return first_Effect, second_Effect
    else: # need to add both s3:PutObject and s3:GutObject
        first_Effect = {
            "Effect": "Allow",
            "Principal": {
                "AWS": account_number
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::" + bucket_name + "/*",
        }
        second_Effect = {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::" + bucket_name + "/*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
        return first_Effect, second_Effect


# The Function return the SSL policy if the bucket does not have a bucket policy
def make_new_policy(bucket_name, account_number):
    ssl_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": account_number
                },
                "Action": "s3:*",
                "Resource": "arn:aws:s3:::" + bucket_name + "/*",
            },
            {
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": "arn:aws:s3:::" + bucket_name + "/*",
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
            }
        ]
    }
    return ssl_policy
