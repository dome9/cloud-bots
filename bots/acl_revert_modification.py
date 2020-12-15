'''
## acl_revert_modification
What it does: returns an acl to it's previous form.
Usage: AUTO: acl_revert_modification

Sample GSL: cloudtrail where event.name in ('ReplaceNetworkAclEntry', 'DeleteNetworkAclEntry', 'CreateNetworkAclEntry')
Limitation: None
Note: Logic only bot
'''

import boto3
from botocore.exceptions import ClientError
import json
from bots_utils import cloudtrail_event_lookup

def replace_entry(boto_session, params):
    '''
    function will be called if event is: ReplaceNetworkAclEntry.
    it will recreate the deleted entry.
    To get all the params to get the entry before it get replaced, function will search for the creation of the entry.

    In this function params are not used in function create_entry because they lack information needed to create an entry.
    '''

    text_output = ''
    acl_id = params.get('networkAclId')
    # Trying to get entry creation event
    print('here')
    event_name, event_params = find_event(boto_session, acl_id)

    # Exiting if creation event can not be found
    if event_name != 'CreateNetworkAclEntry':
        text_output = f"Can not recreate replaced rule {params.get('ruleNumber')}.\nExiting"
        return text_output

    ec2_resource = boto_session.resource('ec2')
    network_acl = ec2_resource.NetworkAcl(acl_id)

    # change dict keys to upper case if they have value
    try:
        network_acl.replace_entry(
            CidrBlock=event_params.get('cidrBlock'),
            DryRun=False,
            Egress=event_params.get('egress'),
            IcmpTypeCode=event_params.get('icmpTypeCode'),
            PortRange=event_params.get('portRange'),
            Protocol=event_params.get('aclProtocol'),
            RuleAction=event_params.get('ruleAction'),
            RuleNumber=event_params.get('ruleNumber'))

        text_output = f"Rule number {params.get('ruleNumber')} successfully replaced \n"

    except ClientError as e:
        text_output = f'Unexpected error: {e}\n'


    return text_output


def create_entry(boto_session, params):
    '''
    function will be called if event is: DeleteNetworkAclEntry.
    it will recreate the deleted entry.
    To get all the params to create a new entry function will search for the creation of the deleted entry.

    In this function params are not used in function create_entry because they lack information needed to create an entry.
    '''

    text_output = ''
    acl_id = params.get('networkAclId')
    # Trying to get entry creation event
    event_name, event_params = find_event(boto_session, acl_id)

    # Exiting if creation event can not be found
    if event_name != 'CreateNetworkAclEntry':
        text_output = f'Can not recreate deleted rule {params.get("ruleNumber")}.\nExiting'
        return text_output

    ec2_resource = boto_session.resource('ec2')
    network_acl = ec2_resource.NetworkAcl(acl_id)

    try:
        network_acl.create_entry(
            CidrBlock=event_params.get('cidrBlock'),
            DryRun=False,
            Egress=event_params.get('egress'),
            IcmpTypeCode=event_params.get('icmpTypeCode'),
            PortRange=event_params.get('portRange'),
            Protocol=event_params.get('aclProtocol'),
            RuleAction=event_params.get('ruleAction'),
            RuleNumber=event_params.get('ruleNumber'))

        text_output = f"Rule number {params.get('ruleNumber')} successfully created \n"

    except ClientError as e:

        text_output = f'Unexpected error: {e}\n'


    return text_output


def delete_entry(boto_session, params):
    '''
    function will be called if event is: CreateNetworkAclEntry
    it will delete the new created entry.
    '''

    text_output = ''
    ec2_resource = boto_session.resource('ec2')
    network_acl = ec2_resource.NetworkAcl(params.get('networkAclId'))

    try:
        network_acl.delete_entry(
            DryRun=False,
            Egress=params.get('egress'),
            RuleNumber=params.get('ruleNumber'))
        text_output = f"Rule number {params.get('ruleNumber')} successfully deleted \n"

    except ClientError as e:

        text_output = f'Unexpected error: {e}\n'


    return text_output


def find_event(boto_session, attribute_value, entity={}):
    '''
    function will get event related to given attribute_value
    In this case attribute_value is the acl which was modified.
    '''

    # create CloudTrail client
    client = boto_session.client('cloudtrail')
    response = dict()
    if entity:
        # set the start time to search in cloudtrail
        # get the event details
        response = cloudtrail_event_lookup(boto_session, entity, attribute_value, 'ResourceName')

    else:
        # in case time is not set, function will look for all events related to attribute_value
        tmp_response = client.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName', 'AttributeValue': attribute_value}])
        print(tmp_response)
        for event in tmp_response['Events']:
            if event['EventName'] == 'CreateNetworkAclEntry':
                # get index of create entry event
                print(event)
                response = event
                break

    if not response:
        return 'No event found!', None
        
    # gets dictionary from cloudtrail string
    print(response)
    cloud_trail = json.loads(response.get('CloudTrailEvent'))
    event_params = cloud_trail.get('requestParameters')
    
    # Capitalizing key names to use event_params in create and replace entry functions.
    # Function wont work if keys not capitalized.
    if 'portRange' in event_params and event_params['portRange']:
        event_params['portRange']['From'] = event_params['portRange'].pop('from')
        event_params['portRange']['To'] = event_params['portRange'].pop('to')

    if 'icmpTypeCode' in event_params and event_params['icmpTypeCode']:
        event_params['icmpTypeCode']['Code'] = event_params['icmpTypeCode'].pop('code')
        event_params['icmpTypeCode']['Type'] = event_params['icmpTypeCode'].pop('type')

    return cloud_trail.get('eventName'), event_params


def run_action(boto_session, rule, entity, params):
    text_output = ''
    acl_id = entity.get('id')

    # There are 3 possible events. Each has it's own solution. This is a dict to help assign a function to each case.
    functions = {'ReplaceNetworkAclEntry': replace_entry, 'DeleteNetworkAclEntry': create_entry, 'CreateNetworkAclEntry': delete_entry}

    # getting alert time from additional params in message. and turning value string into dictionary
    
    event_name, event_params = find_event(boto_session, acl_id, entity)

    # use functions dictionary to get function for event.
    if event_name in functions.keys():
        text_output = functions.get(event_name)(boto_session, event_params)

    return text_output
