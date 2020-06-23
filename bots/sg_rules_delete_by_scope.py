"""
## sg_rules_delete_by_scope
What it does: Deletes all rules on a security group with a specific scope, port and protocol are optional
Usage: AUTO: sg_rules_delete_by_scope <scope> <direction> <port|*> <protocol|*>

Example: AUTO: sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 tcp
Parameters:
    scope: a.b.c.d/e
    direction: inbound/ outbound
    port: number/ *
    protocol: TCP/ UDP/ *
-When '*' is any value of the parameter

Other Examples:
    all rules with 1.0.0.0/16 scope will be deleted for any port and protocol:
    sg_rules_delete_by_scope 1.0.0.0/16 inbound * *

    all rules with 0.0.0.0/0 scope will be deleted for port 22 and any protocol:
    sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 *
Notes :
    - make sure
Limitations: IPv6 is not supported

"""

import re

PORT_TO = 'portTo'
PORT_FROM = 'port'
PROTOCOL = 'protocol'
SCOPE = 'scope'
ALL_TRAFFIC_PORT = 0
ALL_TRAFFIC_PROTOCOL = '-1'

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


def delete_sg(sg, sg_id, rule,direction, text_output):
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
            text_output = text_output + ' rule : ' + rule[SCOPE] + ',' + str(rule[PORT_FROM]) + ',' + str(
                rule[PORT_TO]) + ',' + str(sg_id) + ',' + rule[PROTOCOL].lower() + ' deleted successfully ;'

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'

    else:
        text_output = text_output + f'Error unknown direction ; \n'

    return text_output


def run_action(boto_session, rule, entity, params):
    text_output = 'Run bot sg_rules_delete_by_scope.'
    sg_id = entity['id']
    # Param retrieving
    try:
        scope, direction, port, protocol = params  # get params
    except Exception as e:
        return e

    ec2_resource = boto_session.resource('ec2')
    sg = ec2_resource.SecurityGroup(sg_id)
    port = str(port)
    for rule in entity[f'{direction}Rules']:
        if scope == rule[SCOPE]:
            if port == '*' or int(port) == rule[PORT_FROM] == rule[PORT_TO]:
                if protocol == rule[PROTOCOL] or protocol == '*':
                    if rule[PROTOCOL] == 'ALL':
                        rule[PROTOCOL] = ALL_TRAFFIC_PROTOCOL  # '-1'
                    text_output = text_output + ' rule was found in security group with port in range ;'
                    text_output = delete_sg(sg, sg_id, rule,  direction, text_output)

        else:
            continue

    return text_output
