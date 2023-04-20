"""
## sg_delete_not_matching_cidr
What it does: Deletes all rules on a security group , that have the given port and have a scope outside the given cidr
        * following GSL - SecurityGroup should not have inboundRules contain [ port<=x and portTo>=x and scope!= y  ]

Usage: sg_delete_not_matching_cidr <port> <cidr> <direction>

Parameters:
    port: number
    scope: a.b.c.d/e
    direction: inbound/ outbound


Example:

    sg_delete_not_matching_cidr 22 10.163.0.0/16 inbound

    *all the sg's rules with port 22 that have scope with range outside of 10.163.0.0/16 scope ,  will be deleted

Notes :

    -  before running this bot, ensure that your applications will work correctly without those rules
    - if a port is in a port range and there is a mismatch in cidr the rule will be deleted ( with all the other port in range )

Limitations: IPv6 is not supported yet

"""

import bots_utils as utils

PORT_TO = 'portTo'
PORT_FROM = 'port'
PROTOCOL = 'protocol'
SCOPE = 'scope'
ALL_TRAFFIC_PORT = 0
ALL_TRAFFIC_PROTOCOL = '-1'


def run_action(boto_session, rule, entity, params):
    text_output = 'Run Bot sg_delete_not_matching_cidr. '
    sg_id = entity['id']

    # param retrieving
    try:
        port, scope, direction, = params[0,3]  # get params
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
            if not utils.is_scope_contained_by_other_ipv4(rule[SCOPE], scope):
                # rule scope is outside of the scope given , hence need to be deleted
                text_output = text_output + utils.stringify_rule(
                    rule) + 'rule was found in security group with port in range; '
                text_output = utils.delete_sg(sg, sg_id, rule, direction, text_output)

        else:
            continue

    return text_output
