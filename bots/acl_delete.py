'''
## acl_delete
What it does: deletes created network acl.
Usage: AUTO: acl_delete

Sample GSL: cloudtrail where event.name='CreateNetworkAcl'
Limitation: Bot will not delete default vpc's network acl
            Bot only for logic
'''

import boto3
from botocore.exceptions import ClientError
import json
from bots_utils import cloudtrail_event_lookup


def find_event_and_get_acl(boto_session, entity):
    '''
    function will get event related to given attribute_value
    In this case attribute_value is the network acl which was created.
    '''
    try:
        response = cloudtrail_event_lookup(boto_session, entity, 'CreateNetworkAcl')
        print(response)
        # gets dictionary from cloudtrail string
        cloud_trail = json.loads(response['CloudTrailEvent'])

        return cloud_trail.get("responseElements")['networkAcl']

    except ClientError as e:
        return f'Unexpected error: {e}\n'


def run_action(boto_session, rule, entity, params):

    text_output = ''
    ec2_resource = boto_session.resource('ec2')
    try:
        # getting the network acl from cloud trail event
        acl_description = find_event_and_get_acl(boto_session, entity)

        acl_id = acl_description.get('networkAclId')

        network_acl = ec2_resource.NetworkAcl(acl_id)
        # checking if acl was not created as default vpc's network acl
        if not network_acl.is_default:
            network_acl.delete()
            text_output = 'Network acl deleted successfully\n'

    except ClientError as e:
        text_output = f'Unexpected error: {e}\n'

    return text_output
