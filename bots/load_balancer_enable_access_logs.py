'''
## load_balancer_enable_access_logs
What it does: enables access logging for a load balancer (elb, alb)
Usage: AUTO: load_balancer_enable_access_logs
Limitations: None
'''

import json
from botocore.exceptions import ClientError
import string
import secrets

LENGTH = 6
allowed_characters = string.ascii_lowercase + string.digits
permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'
elb_id_table = {'us-east-1': '127311923021', 'us-east-2': '033677994240', 'us-west-1': '027434742980',
                'us-west-2': '797873946194', 'af-south-1': '098369216593', 'ca-central-1': '985666609251',
                'eu-central-1': '054676820928', 'eu-west-1': '156460612806', 'eu-west-2': '652711504416',
                'eu-south-1': '635631232127', 'eu-west-3': '009996457667', 'eu-north-1': '897822967062',
                'ap-east-1': '754344448648', 'ap-northeast-1': '582318560864', 'ap-northeast-2': '600734575887',
                'ap-northeast-3': '383597477331', 'ap-southeast-1': '114774131450',
                'ap-southeast-2': '783225319266', 'ap-south-1': '718504428378', 'me-south-1': '076674570225',
                'sa-east-1': '507241528517', 'us-gov-west-1': '048591011584', 'us-gov-east-1': '190560391635',
                'cn-north-1': '638102146993', 'cn-northwest-1': '037604701340'}


def elb_handler(boto_session, elb_name, bucket_name):
    client = boto_session.client('elb')
    try:
        print(f'{__file__} - Trying to enable access logs... \n')
        result = client.modify_load_balancer_attributes(
            LoadBalancerName=elb_name,
            LoadBalancerAttributes={
                'AccessLog': {
                    'Enabled': True,
                    'S3BucketName': bucket_name,
                    'EmitInterval': 60,
                }
            }
        )
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            return 0, f"Unexpected error: {str(result)} \n"

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
        return 0, text_output

    print(f'{__file__} - Done. \n')
    return 1, f'Successfully enabled access logs for: {elb_name}. Target bucket: {bucket_name}.'


def alb_handler(boto_session, alb_id, bucket_name):
    client = boto_session.client('elbv2')
    try:
        print(f'{__file__} - Trying to enable access logs... \n')
        result = client.modify_load_balancer_attributes(
            LoadBalancerArn=alb_id,
            Attributes=[
                {
                    'Key': 'access_logs.s3.enabled',
                    'Value': 'true'
                },
                {
                    'Key': 'access_logs.s3.bucket',
                    'Value': bucket_name
                }
            ]
        )
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            return 0, f"Unexpected error: {str(result)} \n"

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
        return 0, text_output

    print(f'{__file__} - Done. \n')
    return 1, f'Successfully enabled access logs for: {alb_id}. Target bucket: {bucket_name}'


def generate_random_str(entity):
    random_str = ''.join(secrets.choice(allowed_characters) for x in range(LENGTH))
    lb_name = entity['name'].lower()
    lb_type = entity['type'].replace('ApplicationLoadBalancer', 'ALB').lower()
    region = entity['region'].replace("_", "-")
    bucket_name = f"{lb_type}-access-logs-{lb_name}-{region}-{random_str}"
    return bucket_name


def create_bucket(boto_session, entity):
    s3_client = boto_session.client('s3')
    bucket_name = generate_random_str(entity)
    print(f'{__file__} - Target bucket name: {bucket_name} \n')
    try:
        print(f'{__file__} - Checks whether the bucket with this name is already exists... \n')
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError:
        print(f'{__file__} - Bucket doesnt exist. Creating bucket... \n')
        # Creates the bucket:
        try:
            region = entity['region'].replace("_", "-")
            if region == 'us-east-1':
                result = s3_client.create_bucket(
                    Bucket=bucket_name
                )
            elif region == 'eu-west-1':
                result = s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': 'EU',
                    },
                )
            else:
                result = s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': entity['region'].replace("_", "-"),
                    },
                )
            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                return 0, f"Unexpected error: {str(result)} \n"
        except ClientError as e:
            text_output = f"Unexpected client error: {e} \n"
            if 'AccessDenied' in e.response['Error']['Code']:
                text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
            return 0, text_output

    print(f'{__file__} - Done. Target bucket for the access logs: {bucket_name}. \n')
    return 1, bucket_name


def put_relevant_permissions(bucket_name, elb_account_id, aws_account_id, boto_session):
    s3_client = boto_session.client('s3')
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{elb_account_id}:root"
                },
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{aws_account_id}/*"
            },
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "delivery.logs.amazonaws.com"
                },
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{aws_account_id}/*",
                "Condition": {
                    "StringEquals": {
                        "s3:x-amz-acl": "bucket-owner-full-control"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "delivery.logs.amazonaws.com"
                },
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            }
        ]
    }
    try:
        print(f'{__file__} - Attaching relevant policy to: {bucket_name}... \n')
        print(f'{__file__} - Full policy: {policy} \n')
        result = s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(policy),
        )
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            return 0, f"Unexpected error: {str(result)} \n"

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"
        return 0, text_output

    print(f'{__file__} - Successfully attached policy. \n')
    return 1, ""


def run_action(boto_session, rule, entity, params):
    text_output = ''
    s3_client = boto_session.client('s3')
    success, msg = create_bucket(boto_session, entity)
    if success:
        bucket_name = msg
    else:
        return msg

    elb_account_id = elb_id_table[entity['region'].replace("_", "-")]
    success, msg = put_relevant_permissions(bucket_name, elb_account_id, entity['accountNumber'], boto_session)
    if not success:
        return msg

    if entity['type'] == 'ELB':
        success, msg = elb_handler(boto_session, entity['name'], bucket_name)
        if success:
            text_output += msg
        else:
            return msg
    elif entity['type'] == 'ApplicationLoadBalancer':
        success, msg = alb_handler(boto_session, entity['id'], bucket_name)
        if success:
            text_output += msg
        else:
            return msg

    return text_output
