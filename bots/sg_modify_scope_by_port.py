"""
##sg_modify_scope_by_port
# What it does: modify Security Group's rules scope by a given port , new and old scope(optional).
# Direction can be : inbound or outbound
# Usage: sg_modify_scope_by_port <port> <change_scope_from|*> <change_scope_to> <direction>
       - When '*' set for replacing any rule with the specific port
# Examples:
        sg_modify_scope_by_port 22 0.0.0.0/0 10.0.0.0/24 inbound
        sg_modify_scope_by_port 22 * 10.0.0.0/24 inbound
#Notes:
    -  if the port is in a rule's port range, the bot will change the rule's ip to desire ip , to avoid that
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

"""
returns a string of rule's id by scope,port,direction,etc.
"""


def stringify_rule(rule):
    return 'rule: ' + rule[SCOPE] + ',' + str(rule[PORT_FROM]) + ',' + str(rule[PORT_TO]) + ',' + \
       rule[PROTOCOL].lower() + ' '


"""
compare the 2 forms of representation for security group rules and find if a rule exists in ip permissions 
"""


def find_rule_in_ip_permissions(perm,rule,direction,scope):
    if perm['FromPort'] == rule[PORT_FROM] and perm['ToPort'] == rule[PORT_TO] and perm['IpProtocol'] == rule[PROTOCOL].lower():
        for ip in perm['IpRanges']:
            if ip['CidrIp'] == scope:  # found same rule exists already
                return True
    return False




def is_rule_exists_in_sg(sg, rule, direction, scope):

    if direction.lower() == 'inbound':
        for perm in sg.ip_permissions:
            return find_rule_in_ip_permissions(perm, rule, direction, scope)

    if direction.lower() == 'outbound':
        for perm in sg.ip_permissions_egress:
            return find_rule_in_ip_permissions(perm, rule, direction, scope)

    return False


"""
checks for ip validity , fix it to be right
"""


def verify_scope_is_cidr(rule):
    ip = re.split('/|\.', str(rule[SCOPE]))  # break ip to blocks
    rule[SCOPE] = ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + ip[3] + '/' + ip[4]
    pass


"""
creates & removes the specified rules from a security group 
"""


def update_sg(sg, sg_id, rule, scope, direction, text_output):
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
            text_output = text_output + stringify_rule(rule) + ' deleted successfully from sg : ' + str(sg_id) + '; '

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'
            return text_output

        # check if one is existing first ! avoid duplicates and exception
        found = is_rule_exists_in_sg(sg, rule, direction, scope)
        if found:
            return text_output
        try:

            sg.authorize_ingress(
                CidrIp=scope,
                FromPort=rule[PORT_FROM],
                ToPort=rule[PORT_TO],
                GroupId=sg_id,
                IpProtocol=rule[PROTOCOL].lower()
            )
            text_output = text_output + stringify_rule(rule) + ' created successfully in sg : ' + str(sg_id) + '; '

        except Exception as e:
            text_output = text_output + f'Error while trying to create security group. Error: {e}'
            return text_output

    elif direction == 'outbound':
        ip_perm = [
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
        try:
            sg.revoke_egress(
                IpPermissions=ip_perm  # only IpPermissions supported with this func !
            )
            text_output = text_output + stringify_rule(rule) + ' deleted successfully from sg : ' + str(sg_id) + '; '

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'
            return text_output

        # check if one is existing first ! avoid duplicates and exception
        found = is_rule_exists_in_sg(sg, rule, direction, scope)
        if found:
            return text_output
        try:
            ip_perm[0]['IpRanges'][0]['CidrIp'] = scope  # ip permissions to create of a new rule
            # must have user's scope
            sg.authorize_egress(
                IpPermissions=ip_perm  # only IpPermissions supported with this func !
            )
            text_output = text_output + stringify_rule(rule) + ' created successfully in sg : ' + str(sg_id) + '; '

        except Exception as e:
            text_output = text_output + f'Error while trying to create security group. Error: {e}'
            return text_output
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
        text_output = text_output + 'Params handling error. Please check parameters and try again. \n ' + e + '\n'
        + 'Usage: sg_modify_scope_by_port <port> <change_scope_from|*> <change_scope_to> <direction>'
        raise Exception(text_output)

    ec2_resource = boto_session.resource('ec2')
    sg = ec2_resource.SecurityGroup(sg_id)

    for rule in entity[f'{direction}Rules']:
        if rule[PORT_FROM] <= int(port) <= rule[PORT_TO]:
            if change_from_scope == rule[SCOPE] or change_from_scope == '*':
                if rule[PROTOCOL] == 'ALL':
                    rule[PROTOCOL] = ALL_TRAFFIC_PROTOCOL  # '-1'
                text_output = text_output + ' rule was found in security group with port in range ;'
                text_output = text_output + update_sg(sg, sg_id, rule, change_to_scope, direction, text_output)

        else:
            continue

    return text_output
