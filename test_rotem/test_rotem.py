import boto3
from botocore.exceptions import ClientError


def get_aws_region_code(region):
    ec2 = boto3.client('ec2')
    ssm_client = boto3.client('ssm', region_name='us-east-1')
    regions = ec2.describe_regions()

    region_names = [region['RegionName'] for region in regions['Regions']]

    if region in region_names:
        return region
    else:
        for region_id in region_names:
            ssm_name = '/aws/service/global-infrastructure/regions/%s/longName' % region_id
            ssm_response = ssm_client.get_parameter(Name=ssm_name)
            if region.lower() in ssm_response['Parameter']['Value'].lower():
                return region_id
        raise Exception('not valid region:' + region)


def rotem_test(region):
    print('ok')
    boto_session = boto3.Session(region_name=region)
    iam_client = boto_session.client('iam')
    response = iam_client.get_role(RoleName='rotem-test-role-20240220')
    print('ok')


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


def run_action(session, entity):
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


get_aws_region_code('test_region')
# rotem_test('ttt')


#boto_session = boto3.Session(region_name='tttttttttttt')
#run_action(boto_session, {'arn': 'arn:aws:iam::125223212618:policy/rotemtest'})
