"""
Bots Utilities File
"""

# imports
import re
import ipaddress

PORT_TO = 'portTo'
PORT_FROM = 'port'
PROTOCOL = 'protocol'
SCOPE = 'scope'
ALL_TRAFFIC_PORT = 0
ALL_TRAFFIC_PROTOCOL = '-1'

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

    inside = n2.supernet_of(n1)
    if inside:
        return True
    else:
        return False # cidr if out of scope bounds


"""
Check if cider is completely inside scope, if it does returns true 
"""


def is_scope_contained_by_other_ipv6(scope, other):
    n1 = ipaddress.IPv6Network(scope)
    n2 = ipaddress.IPv6Network(other)
    inside = n2.supernet_of(n1)
    if inside:
        return True
    else:
        return False  # cidr if out of scope bounds

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
