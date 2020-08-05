"""
## sg_delete_not_matching_cidr
What it does: Deletes all rules on a security group with a certian port when the cidr is not matching input
Usage: sg_delete_not_matching_cidr <port> <scope> <direction>

Parameters:
    port: integer
    scope: a.b.c.d/e
    direction: inbound/ outbound


Example:
    sg_rules_delete_by_scope 22 1.0.0.0/16 inbound

    *all the sg's rules with port 22 that doesn't have 1.0.0.0/16 cidr will be deleted

Notes :

    -  before running this bot, ensure that your applications will work correctly without those rules
    - if a port is in a port range and there is  a mismatch in cidr the rule will be deleted

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
            text_output = text_output + utils.stringify_rule(rule) + 'deleted successfully from sg : %s; ' % str(sg_id)

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
            text_output = text_output + utils.stringify_rule(rule) + ' deleted successfully from sg : %s; ' % str(sg_id)

        except Exception as e:
            text_output = text_output + f'Error while trying to delete security group. Error: {e}'

    else:
        text_output = text_output + f'Error unknown direction ; \n'

    return text_output


def run_action(boto_session, rule, entity, params):
    text_output = 'Run Bot sg_delete_not_matching_cidr. '
    sg_id = entity['id']

    # param retrieving
    try:
        port, scope, direction, = params  # get params
    except Exception as e:
        text_output = text_output + f'Params handling error. Please check parameters and try again. Error: {e}'
        raise Exception(text_output)

    # Create an EC2 resource
    ec2_resource = boto_session.resource('ec2')
    # get sg by sg_id of the entity
    sg = ec2_resource.SecurityGroup(sg_id)
    port = str(port)

    # going through all the user's sg and check for mismatch
    for rule in entity[f'{direction}Rules']:
        if rule[PORT_FROM] <= int(port) <= rule[PORT_TO]:
            # port found , if the scope doesn't match , rule will be deleted
            if rule[SCOPE] != scope:
                text_output = text_output + utils.stringify_rule(
                    rule) + 'rule was found in security group with port in range; '
                text_output = delete_sg(sg, sg_id, rule, direction, text_output)

        else:
            continue

    return text_output
