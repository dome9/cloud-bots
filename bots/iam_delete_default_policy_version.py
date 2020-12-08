'''
## iam_delete_default_policy_version
What it does:
    Delete the default policy version and put the newest before it.
Usage:
    AUTO: iam_delete_default_policy_version
Limitations:
    None
'''

import boto3
from botocore.exceptions import ClientError


# get the version id of the default version (that we need to delete)
def get_default_version_id(iam_client, policy_arn, text_output):
    version_id = iam_client.get_policy(PolicyArn=policy_arn) ['Policy']['DefaultVersionId']
    text_output += f'default policy version to remove is version: {version_id} from policy: {policy_arn} \n'
    return version_id, text_output

# find the newest version before the default version which will replace the default.
def get_new_default_version(versions):
    if (versions[0]['IsDefaultVersion'] == False): # if the newest version isn't the default version, send it.
        return versions[0]['VersionId']
    else: # the newest version is the default version (probably), send the newest before it.
        return versions[1]['VersionId']

# swap the default version to another version
def swap_default_version(iam_client, policy_arn, new_default_version_id):
    response = iam_client.set_default_policy_version(
        PolicyArn=policy_arn,
        VersionId=new_default_version_id
    )
    return f'New default policy version is : {new_default_version_id} \n'

# delete version by its version id (can't delete version that set to default)
def remove_policy_version(iam_client, policy_arn, version_id):
    response = iam_client.delete_policy_version(
        PolicyArn=policy_arn,
        VersionId=version_id
    )
    return f'policy version {version_id} has been removed successfully. \n'



### Update policy - core method
def run_action(boto_session, rule, entity, params):
    text_output = ''
    policy_arn = entity['id']
    iam_client = boto_session.client('iam')

    try:
        # get the version id of the default version (that we need to delete)
        default_version_id, text_output = get_default_version_id(iam_client, policy_arn, text_output)

        # get list of all the version of the policy
        # https://docs.aws.amazon.com/cli/latest/reference/iam/list-policy-versions.html
        versions = iam_client.list_policy_versions(PolicyArn=policy_arn) ["Versions"]

        # if the default version isn't the only version
        if len(versions) > 1:
            # find the newest version before the default version which will replace the default
            new_default_version_id = get_new_default_version(versions)

            # swap the default version to another version (the newest version before it that we just found)
            text_output += swap_default_version(iam_client, policy_arn, new_default_version_id)

            # delete the previous default version from the policy (now we can because it's no longer the default version)
            text_output += remove_policy_version(iam_client, policy_arn, default_version_id)

        else:
            text_output += f'version: {default_version_id} is the only version of the policy {policy_arn}. Therefore we can\'t remove it.'

    except ClientError as e:
        text_output += 'Unexpected error: %s \n' % e

    return text_output