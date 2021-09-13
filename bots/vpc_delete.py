"""
## vpc_delete
What it does: deletes vpc
Usage: AUTO: vpc_delete
"""
import boto3
from botocore.exceptions import ClientError


def run_action(session, rule, entity, params):
    ec2 = boto3.resource('ec2')
    vpc_id = entity['id']

    # create vpc resource
    vpc = ec2.Vpc(vpc_id)
    try:
        vpc.delete()
        return f"Deleted vpc {entity['name']}."

    except ClientError as e:
        return f"Unexpected error: {e}"
