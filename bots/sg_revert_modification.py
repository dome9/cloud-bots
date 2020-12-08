'''
## sg_revert_modification ***LOG.IC Bot***
What it does:
    revert modification action on security group.
    modification actions = ('AuthorizeSecurityGroupEgress', 'AuthorizeSecurityGroupIngress', 'RevokeSecurityGroupEgress', 'RevokeSecurityGroupIngress')
Sample GSL:
    cloudtrail where event.name in ('AuthorizeSecurityGroupEgress', 'AuthorizeSecurityGroupIngress', 'RevokeSecurityGroupEgress', 'RevokeSecurityGroupIngress') and event.status='Success'
Usage:
    AUTO: sg_revert_modification
Limitations: none
'''

import json
from botocore.exceptions import ClientError
import bots_utils

EVENT_NAMES = ('AuthorizeSecurityGroupEgress', 'AuthorizeSecurityGroupIngress', 'RevokeSecurityGroupEgress', 'RevokeSecurityGroupIngress')


# Make list of events related to the relevant security modification actions
def filter_events(cloudtrail_events):
    return [event for event in cloudtrail_events if event['EventName'] in EVENT_NAMES]

# normalize the IpPermissions that got in the event to IpPermissions parameter for the revert action
# Reference: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_IpPermission.html
def normalize_IpPermissions(IpPermissions_items):
    normalizedIpPermissions = []
    for rule in IpPermissions_items:
        normalized_rule = {}
        for element in rule.keys():
            normalized_element = element[0].upper() + element[1:]
            if element == 'groups':
                normalized_element = 'UserIdGroupPairs'

            if isinstance(rule[element], dict) and rule[element].get('items') != None:
                normalized_rule[normalized_element] = normalize_IpPermissions(rule.get(element).get('items'))
            elif rule[element] != {}:
                normalized_rule[normalized_element] = rule[element]

        normalizedIpPermissions.append(normalized_rule)
    return normalizedIpPermissions

# revert a modification action on security group -- core method
def run_action(boto_session, rule, entity, params):
    text_output = ''
    sg_id = entity.get('id')

    ec2_client = boto_session.client('ec2')

    revert_functions = {
        'AuthorizeSecurityGroupEgress': ec2_client.revoke_security_group_egress,
        'AuthorizeSecurityGroupIngress': ec2_client.revoke_security_group_ingress,
        'RevokeSecurityGroupEgress': ec2_client.authorize_security_group_egress,
        'RevokeSecurityGroupIngress': ec2_client.authorize_security_group_ingress
    }

    try:
        # lookup for the relevant events to revert by bot_utils function of cloudtrail events lookup + my function of filtering.
        events_to_revert = filter_events(bots_utils.cloudtrail_event_lookup(boto_session,entity,sg_id,'ResourceName',False))

        if events_to_revert != None:
            for event in events_to_revert: # do revert on any relevant event that we found in the alert time window (usually one)
                event_name = event.get('EventName')

                # get the rules who has been modified the rules we need to revert (the sg acls rules = ipPermissions):
                relevant_event_json = json.loads(event.get('CloudTrailEvent'))
                relevant_revert_arguments = relevant_event_json.get('requestParameters')
                relevant_rules_to_revert = normalize_IpPermissions(relevant_revert_arguments.get('ipPermissions').get('items'))

                # do the revert action:
                if relevant_revert_arguments.get('groupId'):
                    if relevant_revert_arguments.get('groupName'):
                        response = revert_functions[event_name](GroupId=relevant_revert_arguments.get('groupId'), GroupName= relevant_revert_arguments.get('groupName'), IpPermissions=relevant_rules_to_revert)
                    else:
                        response = revert_functions[event_name](GroupId=relevant_revert_arguments.get('groupId'), IpPermissions=relevant_rules_to_revert)
                else:
                    response = revert_functions[event_name](GroupName=relevant_revert_arguments.get('groupName'), IpPermissions=relevant_rules_to_revert)

                # take care to the client response:
                sg_action_to_revert = event_name.split('SecurityGroup')[0]
                sg_acl = event_name.split('SecurityGroup')[1]
                text_output = f"revert to the action of {sg_action_to_revert} in the {sg_acl} acl of the SecurityGroup - {sg_id}: relevant_rules_to_revert: {relevant_rules_to_revert}"

                # if we just did revoke as a revert, we need to check that the rules has been removed successfully
                if sg_action_to_revert == 'Authorize':
                    if not (response.get('UnknownIpPermissions') == []):
                        text_output += f"Problematic rules: \n {response.get('UnknownIpPermissions')}. they didn't removed (didn't found in the {sg_acl} acl of {sg_id})"
                    else:
                        text_output += "revert done successfully!!!"

        else:
            text_output = f"can't find the modification event of {sg_id} to revert"

    except ClientError as e:
        text_output = f"Unexpected error: {e} \n"

    return text_output
