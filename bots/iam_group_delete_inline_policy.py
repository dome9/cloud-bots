"""
## iam_group_delete_inline_group
What it does: Deletes a inline policy attached to iam group
Usage: AUTO: iam_group_delete_inline_group
Limitations: none
"""

import boto3
from botocore.exceptions import ClientError

def run_action(session, rule, entity, params):
    iam_resource = session.resource('iam')
    iam_group = iam_resource.Group(entity['name'])

    # take te names of the policies that we need to delete
    inline_policies = [policy['name'] for policy in entity['inlinePolicies']]

    try:
        text_output = ""
        # iterates over the policies and delete the inline policies
        for policy in iam_group.policies.all():
                if policy.name in inline_policies:
                    policy.delete()
                    text_output += f"Deleted inline policy '{policy.name}'\n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output