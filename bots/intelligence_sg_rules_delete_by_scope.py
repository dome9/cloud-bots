"""
## intelligence_sg_rules_delete_by_scope
What it does: Deletes all rules on a security group with a scope(cidr) containing or equal to a given scope,
             port and protocol are optional

Usage: intelligence_sg_rules_delete_by_scope <scope> <direction> <port|*> <protocol|*>

Parameters:
    scope: a.b.c.d/e
    direction: inbound/ outbound
    port: number/ *
    protocol: TCP/ UDP/ *
-When '*' is any value of the parameter

Examples:
    intelligence_sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 tcp

    all rules with 1.0.0.0/16 scope will be deleted for any port and protocol:
    intelligence_sg_rules_delete_by_scope 1.0.0.0/16 inbound * *

    all rules with 0.0.0.0/0 scope will be deleted for port 22 and any protocol:
    intelligence_sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 *

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


def run_action(boto_session, rule, entity, params):
    text_output = 'Run Bot sg_rules_delete_by_scope. '
    # Get SecurityGroup id
    sg_id = entity['id']
    # Param retrieving
    try:
        scope, direction, port, protocol = params[0,4]  # get params

    except Exception as e:
        text_output = text_output + f'Params handling error. Please check parameters and try again. Error: {e}'
        raise Exception(text_output)

    try:
        ec2_client = boto_session.client('ec2')
        sg_rules = ec2_client.describe_security_group_rules(Filters=[
            {
                'Name': 'group-id',
                'Values': [sg_id]
            }
        ])
    except Exception as e:
        text_output += f'Could not fetch security group rule! Error: {e}'
        raise Exception(text_output)

    port = str(port)
    rules_to_delete = []
    for rule in sg_rules['SecurityGroupRules']:
        if not is_direction_matches(direction, rule):
            continue

        if not utils.is_scope_contained_by_other_ipv4(scope, rule['CidrIpv4']):
            continue

        if not (port == '*' or int(port) == rule['FromPort'] == rule['ToPort']):
            continue

        rules_to_delete.append(rule['SecurityGroupRuleId'])

    if not rules_to_delete:
        text_output += 'No violating rules weer found'
    else:
        try:
            delete_sg_rules(ec2_client, sg_id, rules_to_delete, direction, text_output)
        except Exception as e:
            text_output += f'Could not delete security group rules! Error: {e}'
            raise Exception(text_output)

    return text_output


def is_direction_matches(direction, rule):
    return (direction == 'inbound' and rule['IsEgress'] == False) or \
           (direction == 'outbound' and rule['IsEgress'] == True)


def delete_sg_rules(ec2_client, sg_id, rules_to_delete, direction, text_output):
    if direction == 'inbound':
        ec2_client.revoke_security_group_ingress(GroupId=sg_id, SecurityGroupRuleIds=rules_to_delete)

    elif direction == 'outbound':
        ec2_client.revoke_security_group_egress(GroupId=sg_id, SecurityGroupRuleIds=rules_to_delete)

    return text_output
