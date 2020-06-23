"""
## lambda_detach_blanket_permissions
What it does: For lambda that failed, it check all the policies that grant blanket permissions ('*') to resources and
              detach it from the lambda role
Usage: AUTO: lambda_detach_blanket_permissions
Note: The bot will detach the policies that have admin privileges from the lambda role so you will need to configure the specific
      policies to grant positive permissions to specific AWS services or actions
Limitations:None
"""

from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    text_output = ""

    # Create an iam client
    iam_client = boto_session.client('iam')

    policy = entity.get('executionRole')
    role_name = policy.get('name')

    try:
        arn_list = get_admin_policies(policy)

        for arn in arn_list:
            try:
                iam_client.detach_role_policy(
                    RoleName=role_name,
                    PolicyArn=arn
                )

                policy_name = arn.split('/')[-1]
                text_output = text_output + ' detach policy: %s from lambda role: %s' % (policy_name, role_name)

            except ClientError as e:
                text_output = "Unexpected error: %s \n" % e

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


# The function find all the polices that grant blanket permissions ('*') to resource and return
# the polices arn in a list
def get_admin_policies(policy):

    arn_list = []

    try:
        for policy_name in policy['combinedPolicies']:  # for any policy
            for Statement in policy_name['policyDocument']['Statement']:  # check the Statement of the policy
                if Statement['Effect'] == "Allow" and 'Resource' in Statement and "*" in str(Statement['Resource']):
                    arn_list.append(policy_name['id'])

        arn_list = list(dict.fromkeys(arn_list))  # remove duplicate in the list

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e
        return text_output

    return arn_list
