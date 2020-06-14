"""
# What it does: Security group rule modify scope by a given port and scope.
# Direction can be : inbound or outbound
# Usage: AUTO: sg_modify_scope_by_port <port> <change_scope_from|*> <change_scope_to> <direction>
        When '*' set for replacing any rule with the specific port
# Examples:
        AUTO: sg_modify_security_group_scope_by_port 22 0.0.0.0/0 10.0.0.0/24 inbound
        AUTO: sg_modify_security_group_scope_by_port 22 * 10.0.0.0/24 inbound
#Notes:
    -  if the port is in a rule's port range the bot will change the rule's ip to desire ip , to avoid that
      specify existing rule's scope instead of using '*'
    - to split the rule around the port you can use the bot : #sg_single_rule_delete

#Limitations: IPv6 is not supported yet

"""
import re

PORT_TO = 'portTo'
PORT_FROM = 'port'
PROTOCOL = 'protocol'
SCOPE = 'scope'
ALL_TRAFFIC_PORT = 0
ALL_TRAFFIC_PROTOCOL = '-1'

"""
checks if a rule exists in a security group , returns false/true 
"""


def rule_exists(sg, rule, direction, scope):
    if direction.lower() == 'inbound':
        for perm in sg.ip_permissions:
            if perm['FromPort'] == rule[PORT_FROM] and perm['ToPort'] == rule[PORT_TO] and \
                    perm['IpProtocol'] == rule[PROTOCOL].lower():
                for ip in perm['IpRanges']:
                    if ip['CidrIp'] == scope:  # found same rule exists
                        return True;
        return False
    if direction.lower() == 'outbound':
        for perm in sg.ip_permissions_egress:
            if perm['FromPort'] == rule[PORT_FROM] and perm['ToPort'] == rule[PORT_TO] and \
                    perm['IpProtocol'] == rule[PROTOCOL].lower():
                for ip in perm['IpRanges']:
                    if ip['CidrIp'] == scope:  # found same rule exists
                        return True;
        return False


"""
checks for ip validity , fix it to be right
"""


def fix_malformed(rule):
    ip = re.split('/|\.', str(rule[SCOPE]))  # break ip to blocks
    rule[SCOPE] = ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + ip[3] + '/' + ip[4]
    pass


"""
creates & removes the specified rules from a security group 
"""


def update_sg(sg, sg_id, rule, scope, direction, text_output):
    # make sure that scope is in CIDR notation for example, 203.0.113.0/24
    fix_malformed(rule)

    if direction == 'inbound':
        try:
            sg.revoke_ingress(
                CidrIp=rule[SCOPE],
                FromPort=rule[PORT_FROM],
                ToPort=rule[PORT_TO],
                GroupId=sg_id,
                IpProtocol=rule[PROTOCOL].lower()
            )
            text_output = text_output + ' rule : ' + rule[SCOPE] + ',' + str(rule[PORT_FROM]) + ',' + str(
                rule[PORT_TO]) + ',' + \
                          str(sg_id) + ',' + rule[PROTOCOL].lower() + ' deleted successfully ;'

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'

        try:
            # check if one is existing first ! avoid duplicates and exception
            if rule_exists(sg, rule, direction, scope):
                return text_output

            sg.authorize_ingress(
                CidrIp=scope,
                FromPort=rule[PORT_FROM],
                ToPort=rule[PORT_TO],
                GroupId=sg_id,
                IpProtocol=rule[PROTOCOL].lower()
            )
            text_output = text_output + ' rule : ' + scope + ',' + str(rule[PORT_FROM]) + ',' + str(
                rule[PORT_TO]) + ',' + \
                          str(sg_id) + ',' + rule[PROTOCOL].lower() + ' created successfully ;'

        except Exception as e:
            text_output = text_output + f'Error while trying to create security group. Error: {e}'
    elif direction == 'outbound':
        try:
            sg.revoke_egress(
                IpPermissions=[ # only IpPermissions supported with this func !
                    {
                        'FromPort': rule[PORT_FROM],
                        'IpProtocol': rule[PROTOCOL].lower(),
                        'IpRanges': [
                            {
                                'CidrIp': rule[SCOPE]
                            },
                        ],
                        # 'Ipv6Ranges': [ # future work
                        #     {
                        #         'CidrIpv6': 'string',
                        #         'Description': 'string'
                        #     },
                        # ],
                        'ToPort': rule[PORT_TO]
                    },
                ]
            )
            text_output = text_output + ' rule : ' + rule[SCOPE] + ',' + str(rule[PORT_FROM]) + ',' + str(
                rule[PORT_TO]) + ',' + str(sg_id) + ',' + rule[PROTOCOL].lower() + ' deleted successfully ;'

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'

        try:
            # check if one is existing first ! avoid duplicates and exception
            if rule_exists(sg, rule, direction, scope):
                return text_output

            sg.authorize_egress(
                IpPermissions=[  # only IpPermissions supported with this func !
                    {
                        'FromPort': rule[PORT_FROM],
                        'IpProtocol': rule[PROTOCOL].lower(),
                        'IpRanges': [
                            {
                                'CidrIp': scope
                            },
                        ],
                        # 'Ipv6Ranges': [ # future work
                        #     {
                        #         'CidrIpv6': 'string',
                        #         'Description': 'string'
                        #     },
                        # ],
                        'ToPort': rule[PORT_TO]
                    },
                ]

            )
            text_output = text_output + ' rule : ' + scope + ',' + str(rule[PORT_FROM]) + ',' + str(
                rule[PORT_TO]) + ',' + str(sg_id) + ',' + rule[PROTOCOL].lower() + ' created successfully ;'

        except Exception as e:
            text_output = text_output + f'Error while trying to create security group. Error: {e}'
    else:
        text_output = text_output + f'Error unknown direction ; \n'

    return text_output


def run_action(boto_session, rule, entity, params):
    text_output = 'Run bot sg_modify_scope_by_port.'
    sg_id = entity['id']
    # Param retrieving
    try:
        port, change_from_scope, change_to_scope, direction = params
    except Exception as e:
        text_output = text_output + 'Params handling error. Please check parameters and try again.\n ' + e + '\n' \
                      + 'Usage: AUTO: sg_modify_scope_by_port <port> <change_scope_from|*> <change_scope_to> ' \
                        '<direction> '
        raise Exception(text_output)

    ec2_resource = boto_session.resource('ec2')
    sg = ec2_resource.SecurityGroup(sg_id)

    for rule in entity[f'{direction}Rules']:
        if rule[PORT_FROM] <= int(port) <= rule[PORT_TO] and change_to_scope != rule[SCOPE]:
            if change_from_scope == rule[SCOPE] or change_from_scope == '*':
                if rule[PROTOCOL] == 'ALL':
                    rule[PROTOCOL] = ALL_TRAFFIC_PROTOCOL  # '-1'
                text_output = text_output + ' rule was found in security group with port in range ;'
                text_output = text_output + update_sg(sg, sg_id, rule, change_to_scope, direction, text_output)

        else:
            continue

    return text_output
