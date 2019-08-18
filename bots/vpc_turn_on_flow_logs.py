'''
## vpc_turn_on_flow_logs
What it does: Turns on flow logs for a VPC
Settings: 
Log Group Name: vpcFlowLogs
If traffic type to be logged isn't specified, it defaults to all.
Usage: AUTO: vpc_turn_on_flow_logs traffic_type=<all|accept|reject> destination=<logs|s3> s3_arn=arn:aws:s3:::my-bucket/my-logs/
Example: AUTO: vpc_turn_on_flow_logs traffic_type=all destination=logs
Example: AUTO: vpc_turn_on_flow_logs traffic_type=all destination=s3 s3_arn=arn:aws:s3:::my-bucket/my-logs/

Limitations: none 
Sample GSL: VPC should have hasFlowLogs=true

To specify a subfolder in the bucket, use the following ARN format: bucket_ARN/subfolder_name/ . 
For example, to specify a subfolder named my-logs in a bucket named my-bucket , use the following ARN: arn:aws:s3:::my-bucket/my-logs/

log delivery policy name is set as: vpcFlowLogDelivery
log delivery role is set as: vpcFlowLogDelivery
'''

DESTINATION_INDEX = 0
TRAFFIC_TYPE_INDEX = 1
S3_ARN_INDEX = 2

import boto3
import json
import re
from botocore.exceptions import ClientError


def create_log_delivery_policy(boto_session):
    # Create IAM client
    iam_client = boto_session.client('iam')

    print(f'{__file__} - Creating log delivery policy')

    try:
        # Create a policy
        delivery_policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': [
                        'logs:CreateLogGroup',
                        'logs:CreateLogStream',
                        'logs:DescribeLogGroups',
                        'logs:DescribeLogStreams',
                        'logs:PutLogEvents'
                    ],
                    'Effect': 'Allow',
                    'Resource': '*'
                }
            ]
        }

        create_policy_response = iam_client.create_policy(
            PolicyName='vpcFlowLogDelivery',
            PolicyDocument=json.dumps(delivery_policy)
        )

        responseCode = create_policy_response['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = 'Unexpected error: %s \n' % create_policy_response
        else:
            text_output = 'vpcFlowLogDelivery policy successfully created.\n'

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output


# Poll the account and check if the log delivery IAM policy exists. If not - make it
def check_for_log_delivery_policy(boto_session, policy_arn):
    # Create IAM client
    iam_client = boto_session.client('iam')
    print(f'{__file__} - Checking for log delivery policy')

    try:
        # Check to see if the deny policy exists in the account currently
        get_policy_response = iam_client.get_policy(PolicyArn=policy_arn)

        if get_policy_response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output = 'IAM vpcFlowLogDelivery policy exists in this account.\n'

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'NoSuchEntity':
            # If the policy isn't there - add it into the account
            text_output = create_log_delivery_policy(boto_session)
        else:
            text_output = 'Unexpected error: %s \n' % e

    return text_output


# Try to create the role
def create_role(boto_session, policy_arn):
    iam_client = boto_session.client('iam')
    print(f'{__file__} - Creating role')

    trust_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': '',
                'Effect': 'Allow',
                'Principal': {
                    'Service': 'vpc-flow-logs.amazonaws.com'
                },
                'Action': 'sts:AssumeRole'
            }
        ]
    }

    try:
        response = iam_client.create_role(
            RoleName='vpcFlowLogDelivery',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Created by Dome9 remediation function. This is to allow flow logs to be delivered to CloudWatch'
        )

        if response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output = 'vpcFlowLogDelivery role successfully created.\n'

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'EntityAlreadyExists':
            # If the policy isn't there - add it into the account
            text_output = 'vpcFlowLogDelivery role already exists in this account.\n'
        else:
            text_output = 'Unexpected error: %s \n' % e

    return text_output


def add_policy_to_role(boto_session, policy_arn):
    # Create IAM client
    iam_client = boto_session.client('iam')
    print(f'{__file__} - adding policy to new role')

    try:
        attach_policy_response = iam_client.attach_role_policy(
            RoleName='vpcFlowLogDelivery',
            PolicyArn=policy_arn
        )
        text_output = 'Flow log delivery policy attached to role.\n'

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output


def create_logs(boto_session, role_id, vpc_id, traffic_type, destination, bucket_arn):
    ec2_client = boto_session.client('ec2')

    print(f'{__file__} - creating vpc flow logging')

    # Resource IDs need to be in a list - not string
    vpc_ids = []
    vpc_ids.append(vpc_id)

    try:
        if destination == 'logs':
            response = ec2_client.create_flow_logs(
                DeliverLogsPermissionArn=role_id,
                LogGroupName='vpcFlowLogs',
                ResourceIds=vpc_ids,
                ResourceType='VPC',
                TrafficType=traffic_type,
                LogDestinationType='cloud-watch-logs'
            )

        elif destination == 's3' and bucket_arn != None:
            response = ec2_client.create_flow_logs(
                DeliverLogsPermissionArn=role_id,
                ResourceIds=vpc_ids,
                ResourceType='VPC',
                TrafficType=traffic_type,
                LogDestinationType='s3',
                LogDestination=bucket_arn
            )

        if response['ResponseMetadata']['HTTPStatusCode'] < 400:
            text_output = 'VPC Flow Logs successfully created. The destination is %s \n' % destination
        else:
            text_output = 'Unexpected error: %s \n'

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'FlowLogAlreadyExists':
            # If the policy isn't there - add it into the account
            text_output = 'There is an existing Flow Log in this VPC with the same configuration and log group. Skipping.\n'
        else:
            text_output = 'Unexpected error: %s \n' % e

    return text_output


# Main function
def run_action(boto_session, rule, entity, params):
    # Setup variables
    vpc_id = entity['id']
    account_id = entity['accountNumber']
    bucket_arn = False
    policy_arn = 'arn:aws:iam::' + account_id + ':policy/vpcFlowLogDelivery'
    role_id = 'arn:aws:iam::' + account_id + ':role/vpcFlowLogDelivery'

    ## Set up params. We need a role ARN to come through in the params.
    text_output = ''
    usage = 'Usage: AUTO: vpc_turn_on_flow_logs traffic_type=<all|accept|reject> destination=<logs|s3> s3_arn=arn:aws:s3:::my-bucket/my-logs/\nExample: AUTO: vpc_turn_on_flow_logs traffic_type=all destination=logs\nExample: AUTO: vpc_turn_on_flow_logs traffic_type=all destination=s3 s3_arn=arn:aws:s3:::my-bucket/my-logs/\n'

    if len(params) > 1:
        try:
            for index, param in enumerate(params):
                if '=' in param:
                    key, value = param.split('=')
                else:
                    value = param
                    if index == DESTINATION_INDEX:
                        key = 'destination'
                    elif index == TRAFFIC_TYPE_INDEX:
                        key = 'traffic_type'
                    elif index == S3_ARN_INDEX:
                        key = 's3_arn'

                if key == 'destination':
                    if value.lower() == 'logs':
                        destination = 'logs'
                        text_output = text_output + 'Flow logs will be sent to CW Logs\n'
                    elif value.lower() == 's3':
                        destination = 's3'
                        text_output = text_output + 'Flow logs will be sent to S3\n'
                    else:
                        destination = 'logs'
                        text_output = text_output + 'Destination value does not match logs or S3. Defaulting to logs\n'

                elif key == 'traffic_type':
                    if value.upper() == 'ALL':
                        traffic_type = 'ALL'
                        text_output = text_output + 'The traffic_type to be logged is ALL\n'
                    elif value.upper() == 'ACCEPT':
                        traffic_type = 'ACCEPT'
                        text_output = text_output + 'The traffic_type to be logged is ACCEPT\n'
                    elif value.upper() == 'REJECT':
                        traffic_type = 'REJECT'
                        text_output = text_output + 'The traffic_type to be logged is REJECT\n'
                    else:
                        text_output = text_output + 'Traffic_type not set to ALL, ACCEPT, or REJECT. Those are the only three supported traffic_types. Skipping\n' + usage
                        return text_output

                elif key == 's3_arn':
                    arn_pattern = re.compile('^arn:aws:s3:::')
                    if arn_pattern.match(value):
                        bucket_arn = value
                        text_output = text_output + 'Bucket destination: %s \n' % bucket_arn
                    else:
                        text_output = text_output + 's3_arn does not match expected pattern arn:aws:s3:::my-bucket/my-logs/. Skipping.\n' + usage

        except:
            text_output = text_output + 'Params handling error. Please check params and try again.\n' + usage
            return text_output

    try:
        text_output = text_output + check_for_log_delivery_policy(boto_session,
                                                                  policy_arn)  # Check for the policy to deliver logs from VPC to CloudWatch
        text_output = text_output + create_role(boto_session,
                                                policy_arn)  # Check for role / create it if it does not exist
        text_output = text_output + add_policy_to_role(boto_session, policy_arn)
        text_output = text_output + create_logs(boto_session, role_id, vpc_id, traffic_type, destination,
                                                bucket_arn)  # Create the flow logs

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output
