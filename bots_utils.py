"""
Bots Utilities File
"""

# imports
import re
import ipaddress
from datetime import datetime, timedelta
import json

PORT_TO = 'portTo'
PORT_FROM = 'port'
PROTOCOL = 'protocol'
SCOPE = 'scope'
ALL_TRAFFIC_PORT = 0
ALL_TRAFFIC_PROTOCOL = '-1'
DEFAULT_CLOUDTRAIL_LOOKUP_TIME_DIFF = 0.5

"""
#################################
Security Groups relates functions :
#################################
"""

"""
returns a string of rule's id by scope,port,direction,etc.
Example rule: {'protocol': 'TCP', 'port': 22, 'portTo': 22, 'scope': '0.0.0.0/0', 'scopeMetaData': 'null', 'serviceType': 'CIDR'}
"""


def stringify_rule(rule):
    return 'rule_id: ' + rule[PROTOCOL].lower() + ' ' + rule[SCOPE] + ' port_range: ' + str(
        rule[PORT_FROM]) + '->' + str(rule[PORT_TO]) + ' '


"""
checks for ip validity as cidr, fix it to be right otherwise
Example rule: {'protocol': 'TCP', 'port': 22, 'portTo': 22, 'scope': '0.0.0.0/0', 'scopeMetaData': 'null', 'serviceType': 'CIDR'}
"""


def verify_scope_is_cidr(rule):
    ip = re.split('/|\.', str(rule[SCOPE]))  # break ip to blocks
    rule[SCOPE] = ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + ip[3] + '/' + ip[4]
    pass


"""
Check if two scopes intersect , if it does returns true 
"""


def is_two_scopes_overlap_ipv4(scope1, scope2):
    n1 = ipaddress.IPv4Network(scope1)
    n2 = ipaddress.IPv4Network(scope2)
    intersect = n2.overlaps(n1)
    if intersect:
        return True
    else:
        return False # cidr if out of scope bounds


"""
Check if cider is completely inside scope(other cidr), if it does returns true  
"""


def is_scope_contained_by_other_ipv4(scope, other):
    n1 = ipaddress.IPv4Network(scope)
    n2 = ipaddress.IPv4Network(other)
    scope_len = n1.prefixlen
    other_len = n2.prefixlen
    return scope_len >= other_len and n1.supernet(scope_len - other_len) == n2


"""
Check if cider is completely inside scope, if it does returns true 
"""


def is_scope_contained_by_other_ipv6(scope, other):
    n1 = ipaddress.IPv6Network(scope)
    n2 = ipaddress.IPv6Network(other)
    scope_len = n1.prefixlen
    other_len = n2.prefixlen
    return scope_len >= other_len and n1.supernet(scope_len - other_len) == n2


"""
removes the specified rule from a security group 
"""


def delete_sg(sg, sg_id, rule, direction, text_output):
    # make sure that scope is in CIDR notation for example, 203.0.113.0/24
    verify_scope_is_cidr(rule)

    if direction == 'inbound':
        try:
            sg.revoke_ingress(
                CidrIp=rule[SCOPE],
                FromPort=rule[PORT_FROM],
                ToPort=rule[PORT_TO],
                GroupId=sg_id,
                IpProtocol=rule[PROTOCOL].lower()
            )
            text_output = text_output + stringify_rule(rule) + 'deleted successfully from sg : ' + str(sg_id) + '; '

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'

    elif direction == 'outbound':
        try:
            sg.revoke_egress(
                IpPermissions=[  # only IpPermissions supported with this func !
                    {
                        'FromPort': rule[PORT_FROM],
                        'IpProtocol': rule[PROTOCOL].lower(),
                        'IpRanges': [
                            {
                                'CidrIp': rule[SCOPE]
                            },
                        ],
                        'ToPort': rule[PORT_TO]
                    },
                ]
            )
            text_output = text_output + stringify_rule(rule) + ' deleted successfully from sg : ' + str(sg_id) + '; '

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'

    else:
        text_output = text_output + f'Error unknown direction ; \n'

    return text_output


"""
The function looks up for events in cloud trail based on alert time and event name / resource name.
  boto_session (boto_session object)
  entity (entity dictionary)
  attribute_key (string): name of attribute key (as it appears in boto documentation). Default lookup - by event name.
  attribute_value (string): name of the event / resource (according to attribute_key), as it appears in cloudtrail. 
  is_return_single_event (bool): flag. True - returns only one event. Returns the event that occurred at the time closest to alert_time
                                       False - return all the events found in the time period
  time_diff (int/float): the amount of time (in minutes) to add before and after the alert time in the lookup proccess. 
  resource_name_to_filter (string): string with resource name that helps to filter the events found.
                                    For example: If multiple 'UpdateFunctionConfiguration' events found, you can pass your lambda function name in
                                                 resource_name_to_filter field. That way, the events that are related to other lambdas will be filltered out.
"""


def cloudtrail_event_lookup(boto_session, entity, attribute_value, attribute_key='EventName', is_return_single_event=True, time_diff=DEFAULT_CLOUDTRAIL_LOOKUP_TIME_DIFF, resource_name_to_filter=''):
    # Create Cloudtrail client
    cloudtrail_client = boto_session.client('cloudtrail')
    alert_time = datetime
    
    # check if event time was given
    if entity.get('eventTime'):
        #  Parse given event time
        try:
            alert_time = datetime.strptime(entity.get('eventTime'), '%Y-%m-%dT%H:%M:%SZ')
        except Exception as e:
            print(f'Warning - Error while parsing Log.ic event time: {e} ')
            return None

        # Adjust start and end time the event search
        start_time = alert_time - timedelta(minutes=time_diff)
        end_time = alert_time + timedelta(minutes=time_diff)

        # Look up events in cloudtrail
        try:
            events = cloudtrail_client.lookup_events(LookupAttributes=[
                {'AttributeKey': attribute_key, 'AttributeValue': attribute_value}],
                StartTime=start_time, EndTime=end_time)

        except Exception as e:
            print('Unexpected error while querying cloudtrail: %s \n' % e)
            return None

    else:
        # Look up events in cloudtrail without time
        try:
            events = cloudtrail_client.lookup_events(LookupAttributes=[
                {'AttributeKey': attribute_key, 'AttributeValue': attribute_value}])

        except Exception as e:
            print('Unexpected error while querying cloudtrail: %s \n' % e)
            return None

    if not events.get('Events'):
        print('Warning - No matching events were found in cloudtrail lookup')
        return None
    
    if is_return_single_event:
        # Return only one event - which is the closest to alert time
        return filter_events(events.get('Events'), alert_time, resource_name_to_filter)
    else:
        # Return all events found
        return events.get('Events')


"""
The function filter cloudtrail events list by additional_details given and returns 
the event closest to the given alert_time
  cluodtrail_events (list): list of events found in cloudtrail
  alert_time (datetime object): the time at which the event occurred. 
  resource_name_to_filter (String): string with resource name that helps to filter the events found.
"""


def filter_events(cloudtrail_events, alert_time, resource_name_to_filter=''):
    # Make list of events related to the relevant resource, if additional resource_name_to_filter is given
    if resource_name_to_filter != '':
        events = [event for event in cloudtrail_events if resource_name_to_filter in json.dumps(event['Resources'])]
    else:
        events = cloudtrail_events

    # Find the event that occurred in the nearest time to the alert time
    try:
        return min(events, key=lambda event: abs(
            alert_time - datetime.strptime(json.loads(event['CloudTrailEvent'])['eventTime'], '%Y-%m-%dT%H:%M:%SZ')))
    # No events found or json loads failed
    except:
        print('Warning - No matching events were found in cloudtrail lookup')
        return None
