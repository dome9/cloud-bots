"""
## iam_detach_policy
What it does: detach all entities that attached to policy
Usage: iam_detach_policy
Limitations: none
"""
import boto3
from botocore.exceptions import ClientError

def detach_policy_from_entity(iterator, policy_arn):
    """
    iterates throw list of entities and detach the policy
    """
    text_output = ''
    for entity in iterator:
        try:
            entity.detach_policy(PolicyArn=policy_arn)
        except ClientError as e:
            text_output = "Unexpected error: %s \n" % e

    return text_output

def run_action(session,rule,entity,params):
    iam_resource = session.resource('iam')
    policy_arn = entity['arn']
    iam_policy = iam_resource.Policy(policy_arn)

    # check if the policy attached to any entity
    if iam_policy.attachment_count <= 0:
        return f"The policy {policy_arn} is not attached to an entity"

    # detach the policy from evey entity
    text_output = ''
    text_output += detach_policy_from_entity(iam_policy.attached_groups.all(), policy_arn)
    text_output += detach_policy_from_entity(iam_policy.attached_roles.all(), policy_arn)
    text_output += detach_policy_from_entity(iam_policy.attached_users.all(), policy_arn)

    return text_output
