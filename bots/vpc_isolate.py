'''
##vpc-isolate
What it does: turn off dns resource
              change network acl to new empty one with deny all
              add iam policy, to all users in the account, which limits vpc use: ec2 and sg use in the vpc

Usage: AUTO: vpc_isolate
Limitation: None
'''

import boto3
from botocore.exceptions import ClientError
import json

text_output = str()


def create_acl(ec2_client, vpc_id):

    # An array which will contain all vpc subnets
    association_ids = []

    try:
        # getting all acls within the vpc, to get the subnet associations from them
        network_acl_iterator = ec2_client.describe_network_acls(
            Filters=[{
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]},
            ],)

        # Going through all each acl and checking for associated subnets
        for acl in network_acl_iterator.get('NetworkAcls'):

            associations = acl.get('Associations')
            if associations:
                # gets all subnets from the acl in an array and adding it to association_ids array
                association_ids += [association.get('NetworkAclAssociationId') for association in associations]

        # checking if there any subnets to associate with the new acl
        if association_ids:

            # creating new acl with deny all rules
            network_acl = ec2_client.create_network_acl(VpcId=vpc_id)

            # associating each subnet with the new acl
            for id in association_ids:
                ec2_client.replace_network_acl_association(
                    AssociationId=id,
                    DryRun=False,
                    NetworkAclId=network_acl.get('NetworkAclId')
                )

    except ClientError as e:
        global text_output
        text_output = f'Unexpected error: {e}\n'

    return text_output


def attach_policy_to_all_users(boto_session, policy_arn):

    global text_output
    iam_client = boto_session.client('iam')

    # getting all users in the account
    users = iam_client.list_users()['Users']

    try:

        # attaching isolate policy to each user
        for user in users:
            iam_client.attach_user_policy(
                UserName=user.get('UserName'),
                PolicyArn=policy_arn
            )
        text_output = 'Vpc isolated successfully!'

    except ClientError as e:
        text_output = f'Unexpected error: {e}\n'

    return text_output


def create_deny_policy(boto_session, region, vpc_id):

    # Create IAM client
    iam_client = boto_session.client('iam')

    # Policy to deny user use of ec2 and security groups in the specified vpc
    # user can create an instance with existing sg if this resource is not in deny.
    deny_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "ec2:*",
                "Effect": "Deny",
                "Resource": [
                    f"arn:aws:ec2:{region}:*:vpc/{vpc_id}",
                    f"arn:aws:ec2:{region}:*:security-group/*"
                ],
                "Condition": {
                    "ArnEquals": {
                        f"ec2:Vpc": f"arn:aws:ec2:{region}:*:vpc/{vpc_id}"
                    }
                }
            }
        ]
    }
    try:
        # Create a policy
        iam_client.create_policy(
            PolicyName=f'isolate_deny_{vpc_id}_access_policy',
            PolicyDocument=json.dumps(deny_policy)
        )

    except ClientError as e:
        global text_output
        text_output = f'Unexpected error: {e}\n'
    return text_output


# Pull the account and check if the policy exists. If not - make it
def check_for_policy(boto_session, policy_arn):
    # Create IAM client
    iam_client = boto_session.client('iam')

    try:
        # Check to see if the deny policy exists in the account currently
        iam_client.get_policy(PolicyArn=policy_arn)

    except ClientError as e:
        error = e.response['Error']['Code']

        if error == 'NoSuchEntity':
            # If the policy isn't there - add it into the account
            return False
        else:
            return f'Unexpected error: {e}\n'

    return True


def run_action(boto_session, rule, entity, params):

    # getting parameters needed for all functions
    vpc_id = entity.get('id')
    region = entity.get('region')
    global text_output
    
    try:

        # getting the vpc from ec2 recourse
        ec2_client = boto_session.client('ec2')
        vpc = ec2_client.describe_vpcs(VpcIds=[vpc_id,],).get('Vpcs')[0]

        account_id = vpc.get('OwnerId')
        policy_arn = f"arn:aws:iam::{account_id}:policy/isolate_deny_{vpc_id}_access_policy"


        # disabling vpc's DNS
        ec2_client.modify_vpc_attribute(EnableDnsSupport={
            'Value': False
        }, VpcId=vpc_id)

      
        # creating a new acl with deny all rules
        text_output = create_acl(ec2_client, vpc_id)

        # checking if there was an error and if policy that limits all users in the account exist
        if text_output == '' and not check_for_policy(boto_session, policy_arn):
            # if policy doesn't exist , create it
            text_output = create_deny_policy(boto_session, region, vpc_id)
            if 'error' in text_output:
                return text_output

        # attaching policy to all users in the account
        text_output = attach_policy_to_all_users(boto_session, policy_arn)

    except ClientError as e:
        text_output = f'Unexpected error: {e}\n'

    return text_output
