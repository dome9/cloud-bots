"""
## s3_only_allow_ssl
What it does: Ensure that S3 Buckets enforce encryption of data transfers using Secure Sockets Layer (SSL)
Usage: AUTO: s3_only_allow_ssl
Note: The bot looks at the bucket policy and adds to the current policy the missing actions(s3:GetObject and s3:PutObject)
      and the SSL statement.
      if no policy in the bucket, an SSL policy will add to the bucket
Limitations: none
"""

import json
from botocore.exceptions import ClientError

BUCKET_POLICY = {
    "Version": "2012-10-17",
    "Statement": [

    ]
}

GETPUT_STAT = {
    "Effect": "Allow",
    "Principal": {
        "AWS": "account_number"
    },
    "Action": 'action',
    "Resource": "arn:aws:s3:::bucketName/*",
}

SSL_STAT = {
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": "arn:aws:s3:::bucketName/*",
    "Condition": {
        "Bool": {
            "aws:SecureTransport": "false"
        }
    }
}


def run_action(boto_session, rule, entity, params):
    # create a s3 sessions
    s3_client = boto_session.client('s3')

    bucket_name = entity['id']
    account_number = entity["accountNumber"]
    policy_bucket = entity['policy']

    try:
        if policy_bucket == "null" or policy_bucket is None:  # s3 does not have a bucket policy

            GETPUT_STAT["Resource"] = GETPUT_STAT.get("Resource").replace("bucketName", bucket_name)
            GETPUT_STAT["Principal"]["AWS"] = account_number
            GETPUT_STAT["Action"] = "s3*"
            SSL_STAT["Resource"] = SSL_STAT.get("Resource").replace("bucketName", bucket_name)

            BUCKET_POLICY.get('Statement').append(GETPUT_STAT)
            BUCKET_POLICY.get('Statement').append(SSL_STAT)

            policy_bucket = BUCKET_POLICY

        else:  # bucket has a policy but need to add the missing actions

            current_actions = check_for_get_put_action(policy_bucket)
            first_effect, second_effect = get_missing_statements(bucket_name, account_number, current_actions)

            if second_effect is None:  # if there is only one Statement(ssl Statement) to add to the bucket policy
                policy_bucket['Statement'].append(first_effect)

            else:
                policy_bucket['Statement'].append(first_effect)
                policy_bucket['Statement'].append(second_effect)

        policy = json.dumps(policy_bucket)

        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy
        )

        text_output = "SSL policy added to bucket: %s" % bucket_name

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


# This Function find which actions in the bucket policy that relevant to the SSL(options list)
def check_for_get_put_action(policy_bucket):
    Statements = policy_bucket['Statement']
    getPut_action = []
    options = ["s3:GetObject", "s3:*", "s3:PutObject", "s3:Put*", "s3:Get*", "*"]

    for Statement in Statements:
        if Statement["Effect"] == "Allow":

            if isinstance(Statement['Action'], list):  # if action is a list of actions
                getPut_action = [action for action in Statement['Action'] if (action in options)]

            elif Statement['Action'] in options:  # if action is a string (one action)
                getPut_action.append(Statement['Action'])

    return getPut_action


# The function add to the missing actions the relevant information and return the Statements based
# of the missing actions
def get_missing_statements(bucket_name, account_number, options):

    missing_action = find_missing_action(options)

    if missing_action == 'ssl':  # need to add only ssl action

        SSL_STAT["Resource"] = SSL_STAT.get("Resource").replace("bucketName", bucket_name)
        return SSL_STAT, None

    elif missing_action == 'Get':  # need to add only 's3:PutObject' action

        GETPUT_STAT["Resource"] = GETPUT_STAT.get("Resource").replace("bucketName", bucket_name)
        GETPUT_STAT["Principal"]["AWS"] = account_number
        GETPUT_STAT["Action"] = "s3:PutObject"
        SSL_STAT["Resource"] = SSL_STAT.get("Resource").replace("bucketName", bucket_name)

    elif missing_action == 'Put':  # need to add only 's3:GetObject' action

        GETPUT_STAT["Resource"] = GETPUT_STAT.get("Resource").replace("bucketName", bucket_name)
        GETPUT_STAT["Principal"]["AWS"] = account_number
        GETPUT_STAT["Action"] = "s3:GetObject"
        SSL_STAT["Resource"] = SSL_STAT.get("Resource").replace("bucketName", bucket_name)

    else:  # need to add both s3:PutObject and s3:GutObject

        GETPUT_STAT["Resource"] = GETPUT_STAT.get("Resource").replace("bucketName", bucket_name)
        GETPUT_STAT["Principal"]["AWS"] = account_number
        GETPUT_STAT["Action"] = "s3*"
        SSL_STAT["Resource"] = SSL_STAT.get("Resource").replace("bucketName", bucket_name)

    return GETPUT_STAT, SSL_STAT


# The function find which action is missing from the option so it will add to the SSL policy
def find_missing_action(options):
    missing_action = ''

    if ("*" in options) or ("s3:*" in options) or ('s3:GetObject' in options and 's3:PutObject' in options) or \
            ('s3:Get*' in options and 's3:Put*' in options) or ('s3:GetObject' in options and 's3:Put*' in options) or \
            ('s3:Get*' in options and 's3:PutObject' in options):
        missing_action = 'ssl'

    elif 's3:GetObject' in str(options) or "s3:Get*" in str(options):
        missing_action = 'Get'

    elif 's3:PutObject' in str(options) or "s3:Put*" in str(options):
        missing_action = 'Put'

    return missing_action
