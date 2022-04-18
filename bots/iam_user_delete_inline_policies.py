"""
## iam_user_delete_inline_policies
What it does: deleted all iam user inline policies and attach new managed policies if passed as an argument
Usage: iam_user_delete_inline_policies <managed_policies_arn> (<managed_policies_arn> is optional. For more than one policy, use a comma as a separator).
- iam_user_delete_inline_policies (only deletes)
- iam_user_delete_inline_policies policy1_arn,policy2_arn
"""

from botocore.exceptions import ClientError


def attach_policies(params, iam_resource, user_name) -> str:
    policies_arn = params[0].replace(" ", '').split(',')
    iam_user = iam_resource.User('name', user_name)

    text_output = ''
    for policy_arn in policies_arn:
        try:
            iam_user.attach_policy(PolicyArn=policy_arn)
            text_output += f"Attached policy {policy_arn}"
        except ClientError as e:
            raise ValueError(f"Error {e} while attaching policy {policy_arn}\n")

    return text_output


def run_action(session, rule, entity, params):
    iam_resource = session.resource('iam')
    user_name = entity['name']
    inline_policies = entity['inlinePolicies']

    text_output = ''
    for policy in inline_policies:
        policy_name = policy['name']
        try:
            user_policy = iam_resource.UserPolicy(user_name, policy_name)
            user_policy.delete()
            text_output += f"Deleted policy: {policy_name}\n"
        except ClientError as e:
            raise ValueError(f"Error {e} while deleting policy {policy_name}\n")

    if len(params) > 0:
        text_output += attach_policies(params, iam_resource, user_name)
    return text_output
