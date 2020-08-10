"""
## sg_rules_delete_by_scope
What it does: Deletes all rules on a security group with a specific scope, port and protocol are optional
Usage: sg_rules_delete_by_scope <scope> <direction> <port|*> <protocol|*>

Parameters:
    scope: a.b.c.d/e
    direction: inbound/ outbound
    port: number/ *
    protocol: TCP/ UDP/ *
-When '*' is any value of the parameter

Examples:
    sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 tcp

    all rules with 1.0.0.0/16 scope will be deleted for any port and protocol:
    sg_rules_delete_by_scope 1.0.0.0/16 inbound * *

    all rules with 0.0.0.0/0 scope will be deleted for port 22 and any protocol:
    sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 *

Notes :
    - the bot deletes the rule without splitting ports ( do not create new rules without the deleted port)
      for deleting rule with split use - sg_single_rule_delete bot .
    -  before running this bot, ensure that your applications will work correctly without those rules
    - if a port is in a port range the rule wont be deleted ! use * on port parameter to delete the rule for any port
Limitations: IPv6 is not supported

"""

import bots_utils as utils

PORT_TO = 'portTo'
PORT_FROM = 'port'
PROTOCOL = 'protocol'
SCOPE = 'scope'
ALL_TRAFFIC_PORT = 0
ALL_TRAFFIC_PROTOCOL = '-1'




"""
creates & removes the specified rules from a security group 
"""


def delete_sg(sg, sg_id, rule, direction, text_output):
    # make sure that scope is in CIDR notation for example, 203.0.113.0/24
    utils.verify_scope_is_cidr(rule)

    if direction == 'inbound':
        try:
            sg.revoke_ingress(
                CidrIp=rule[SCOPE],
                FromPort=rule[PORT_FROM],
                ToPort=rule[PORT_TO],
                GroupId=sg_id,
                IpProtocol=rule[PROTOCOL].lower()
            )
            text_output = text_output + utils.stringify_rule(rule) + 'deleted successfully from sg : ' + str(sg_id) + '; '

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


def run_action(boto_session, rule, entity, params):
    text_output = 'Run Bot sg_rules_delete_by_scope. '
    sg_id = entity['id']
    # Param retrieving
    try:
        scope, direction, port, protocol = params  # get params
    except Exception as e:
        text_output = text_output + f'Params handling error. Please check parameters and try again. Error: {e}'
        raise Exception(text_output)

    ec2_resource = boto_session.resource('ec2')
    sg = ec2_resource.SecurityGroup(sg_id)
    port = str(port)
    for rule in entity[f'{direction}Rules']:
        if scope == rule[SCOPE]:
            if port == '*' or int(port) == rule[PORT_FROM] == rule[PORT_TO]:
                if protocol.lower() == rule[PROTOCOL].lower() or protocol == '*':
                    if rule[PROTOCOL] == 'ALL':
                        rule[PROTOCOL] = ALL_TRAFFIC_PROTOCOL  # '-1'
                    text_output = text_output + stringify_rule(rule) + 'rule was found in security group with port in range; '
                    text_output = delete_sg(sg, sg_id, rule, direction, text_output)

        else:
            continue

    return text_output
