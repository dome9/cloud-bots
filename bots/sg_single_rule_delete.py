'''
## sg_single_rule_delete
What it does: Deletes a single rule on a security group
Usage: AUTO: sg_single_rule_delete split=<true|false> protocol=<TCP|UDP> scope=<a.b.c.d/e> direction=<inbound|outbound> port=<number>

Example: AUTO: sg_single_rule_delete split=false protocol=TCP scope=0.0.0.0/0 direction=inbound port=22
Sample GSL: SecurityGroup should not have inboundRules with [scope = '0.0.0.0/0' and port<=22 and portTo>=22]

Conditions and caveats: Deleting a single rule on a security group can be difficult because the problematic port can be nested within a wider range of ports. If SSH is open because a SG has all of TCP open, do you want to delete the whole rule or would you break up the SG into the same scope but port 0-21 and a second rule for 23-end of TCP port range?
Currently the way this is being addressed is using the 'split' parameter. If it's set as false, CloudBots will only look for the specific port in question. If it's nested within a larger port scope, it'll be skipped.
If you set split to true, then the whole rule that the problematic port is nested in will be removed and 2 split rules will be added in its place (ex: if port 1-30 is open and you want to remove SSH, the new rules will be for port 1-21 and port 23-30).

If you want to delete a rule that is open on any ports:
Put Port 0 as the port to be deleted and the bot will remove the rule

If you want to delete a rule that is open to ALL protocol:
Put protocol=ALL and the bot will remove the open rule that configured with ALL as protocol

Set Split to True
AUTO: sg_single_rule_delete split=true protocol=TCP scope=8.8.8.8/32 direction=inbound port=0


Limitations: IPv6 is not supported

'''

import boto3
import re
import sys, traceback
from botocore.exceptions import ClientError

text_output = ''


PROTOCOL_INDEX = 1
SPLIT_INDEX = 0
SCOPE_INDEX = 2
DIRECTION_INDEX = 3
PORT_INDEX = 4

usage = 'AUTO: sg_single_rule_delete split=<true|false> protocol=<TCP|UDP> scope=<a.b.c.d/e> direction=<inbound|outbound> port=<number>\n'


### DeleteSecurityGroupRules ###
def run_action(boto_session, rule, entity, params):
    ## Set up params. We need a role ARN to come through in the params.

    global text_output, usage, portTo

    result = {}
    protocol_to_remove = ''
    # Param retrieving
    try:
        params_dic = get_params(params)
    except Exception as e:
        return (e)

    protocol = params_dic['protocol']
    scope = params_dic['scope']
    port = params_dic['port']
    split = params_dic['split']
    direction = params_dic['direction']

    print(params_dic)

    if not (len(params_dic) == 5 or (
            len(params_dic) == 4 and 'protocol' in params_dic and params_dic['protocol'] == 'ALL')):
        text_output = 'Wrong amount of params inputs detected. Exiting.\n' + usage
        return text_output

    rule_direction = direction + 'Rules'  ## The objects are nested in entity['inboundRules'] or outboundRules but we want to heave the direction variable alone for logging later.
    found_rule = False
    rule_to_delete = False
    lower_port_number = 0
    upper_port_number_to = 0

    # Iterate over the rules and look for one to be deleted
    for rule in entity[rule_direction]:
        if scope == rule['scope'] and (
                protocol == rule['protocol']):  # Scope and protocol match - now check the ports that are open

            protocol = rule['protocol']

            # In case we want to delete the SG with protocol = 'All'  traffic
            if (protocol == 'ALL'):
                if (split == True):
                    rule['port'] = 0
                    rule['portTo'] = 65535
                    protocol_to_remove = '-1'  # -1 specify protocol = All
                    protocol = 'tcp'
                else:
                    port = -1
                    portTo = -1
                    protocol = '-1'
                    split = False
                    rule_to_delete = rule
                    break

            # 2/3 of the conditions are good. Check for scope now.
            if port == rule['port'] and port == rule[
                'portTo']:  # The port to delete is the only one open for the rule and will be deleted
                split = False  # We can just do the normal port delete if there's only 1 port defined in the SG rule. No need to try to split it.
                rule_to_delete = rule
                break

            if split == True and port == 0:
                # If port 0 was defined, we want to delete the rule that is open on ALL ports.
                rule_to_delete = rule
                lower_port_number = rule['port']
                upper_port_number_to = rule['portTo']
                break

            # The port to delete is within a range of ports and will need to be extracted.
            if split == True and rule['port'] <= port <= rule['portTo']:
                rule_to_delete = rule
                # If port 22 is the issue, and the rule in question defines port 20-30:
                # lower_port_number = 20
                # lower_port_number_to = 21
                # upper_port_number = 23
                # upper_port_number_to = 30
                lower_port_number = rule['port']
                upper_port_number_to = rule['portTo']
                break

    if rule_to_delete:
        str_protocol = 'All' if protocol == -1 else protocol
        text_output = text_output + f'Matching rule found that is going to be deleted. Protocol:{str_protocol} Direction:{direction} Port:{port} Scope:{scope}\n'
    else:
        text_output = text_output + 'No SG rule was found that matches the defined parameters. Skipping\n'
        return text_output

    ###### After deciding what rule to remove - remove it

    # Client for making changes / set up parameters
    sg_id = entity['id']
    portTo = rule_to_delete['portTo']

    ec2_resource = boto_session.resource('ec2')
    sg = ec2_resource.SecurityGroup(sg_id)

    # With or without split, we'll need to first remove the old rule before adding in the split one.
    if split == False:

        responseCode = touch_sg(sg, direction, 'revoke', port, portTo, sg_id, scope, protocol)

        if responseCode >= 400:
            text_output = 'Unexpected error: %s \n' % str(result)
        else:
            str_pot = 0 if port == -1 else port
            text_output = text_output + f'Security Group rule from port {str_pot} to port {portTo} successfully removed\n'

    # If split is enabled, we'll need to re-add back in the rest of the ports that were deleted. Two calls are
    # needed. One for the lower section and one for the upper.
    if split == True and port != 0:
        lower_port_number_to = port - 1
        upper_port_number = port + 1

        # In case that the port to revoke was the start of the range
        if lower_port_number == port:
            lower_port_number = lower_port_number + 1

            responseCode = touch_sg(sg, direction, 'authorize', lower_port_number, upper_port_number_to, sg_id, scope,
                                    protocol)

            if responseCode >= 400:
                text_output = 'Unexpected error: %s \n' % str(result)
            else:
                text_output = text_output + 'Security Group ingress rule from port %s to port %s successfully added\n' % (
                    lower_port_number, upper_port_number_to)
                lower_port_number = lower_port_number - 1

        else:
            # In case that the port to revoke was the end of the range
            if upper_port_number_to == port:
                upper_port_number_to = upper_port_number_to - 1

                responseCode = touch_sg(sg, direction, 'authorize', lower_port_number, upper_port_number_to, sg_id,
                                        scope, protocol)

                if responseCode >= 400:
                    text_output = 'Unexpected error: %s \n' % str(result)
                else:
                    text_output = text_output + 'Security Group ingress rule from port %s to port %s successfully added\n' % (
                        lower_port_number, upper_port_number_to)
                    upper_port_number_to = upper_port_number_to + 1


            # in case that the revoked port was in the range
            else:
                responseCode = touch_sg(sg, direction, 'authorize', lower_port_number, lower_port_number_to, sg_id,
                                        scope, protocol)

                if responseCode >= 400:
                    text_output = 'Unexpected error: %s \n' % str(result)
                else:
                    text_output = text_output + 'Security Group ingress rule from port %s to port %s successfully added\n' % (
                        lower_port_number, lower_port_number_to)

                responseCode = touch_sg(sg, direction, 'authorize', upper_port_number, upper_port_number_to, sg_id,
                                        scope, protocol)

                if responseCode >= 400:
                    text_output = 'Unexpected error: %s \n' % str(result)
                else:
                    text_output = text_output + 'Security Group ingress rule from port %s to port %s successfully added\n' % (
                        upper_port_number, upper_port_number_to)

    if split:
        if protocol_to_remove == '-1':  # -1 specify all protocols - bug fixed : '-1' cannot use as boolean
            lower_port_number = 0
            upper_port_number_to = -1
            protocol = protocol_to_remove

        responseCode = touch_sg(sg, direction, 'revoke', lower_port_number, upper_port_number_to, sg_id, scope,
                                protocol)

        if responseCode >= 400:
            text_output = 'Unexpected error: %s \n' % str(result)
        else:
            text_output = text_output + 'Security Group rule from port %s to port %s successfully removed\n' % (
                lower_port_number, upper_port_number_to)

    return text_output


def get_params(params):
    global text_output
    params_dic = {}
    try:
        for index, param in enumerate(params):
            if '=' in param:
                key, value = param.split('=')
            else:
                value = param
                if index == SPLIT_INDEX:
                    key = 'split'
                elif index == PROTOCOL_INDEX:
                    key = 'protocol'
                elif index == SCOPE_INDEX:
                    key = 'scope'
                elif index == DIRECTION_INDEX:
                    key = 'direction'
                elif index == PORT_INDEX:
                    key = 'port'
            if key == 'split':
                split = True
                if value.lower() == 'true':
                    text_output = text_output + 'Split matching for the port to be remediated is set to True\n'
                elif value.lower() == 'false':
                    split = False
                    text_output = text_output + 'Split matching for the port to be remediated is set to False. If the port is contained within a larger scope, it will be skipped.\n'
                else:
                    text_output = text_output + 'Split value does not match true or false. Defaulting to True\n'
                params_dic[key] = split

            elif key == 'protocol':
                if value.lower() == 'tcp':
                    protocol = 'TCP'
                    text_output = text_output + 'The protocol to be removed is TCP\n'
                elif value.lower() == 'udp':
                    protocol = 'UDP'
                    text_output = text_output + 'The protocol to be removed is UDP\n'
                elif value.lower() == 'all':
                    protocol = 'ALL'
                    text_output = text_output + 'The protocol to be removed is ALL protocols\n'
                else:
                    text_output = text_output + 'Unsupported Protocol - currently the only supported options are - TCP,UDP,ALL'
                    raise Exception(text_output)
                params_dic[key] = protocol

            elif key == 'scope':
                scope = value
                # TODO - SUPPORT IPV6 SCOPE AS WELL
                scope_pattern = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$')
                if scope_pattern.match(scope):
                    text_output = text_output + f'Scope to be removed found: {scope} \n'
                else:
                    text_output = text_output + 'Scope does not match expected value (a.b.c.d/e). Skipping.\n' + usage
                    raise Exception(text_output)
                params_dic[key] = scope

            elif key == 'direction':
                if value.lower() == 'inbound':
                    direction = 'inbound'
                    text_output = text_output + 'The rule to be removed is going to be for inbound traffic\n'
                elif value.lower() == 'outbound':
                    direction = 'outbound'
                    text_output = text_output + 'The rule to be removed is going to be for outbound traffic\n'
                else:
                    text_output = text_output + 'Traffic direction does not match inbound or outbound. Skipping.\n' + usage
                    raise Exception(text_output)
                params_dic[key] = direction

            elif key == 'port':
                try:
                    port = int(value)
                    text_output = text_output + f'Port to be removed: {port} \n'
                    params_dic[key] = port
                except ValueError:
                    text_output = text_output + 'Port number was not a valid integer. Skipping.\n' + usage
                    raise Exception(text_output)

        return params_dic

    except:
        text_output = text_output + 'Params handling error. Please check params and try again.\n' + usage
        raise Exception(text_output)


def touch_sg(sg, direction, touch_type, lower_port, uper_port, sg_id, scope, protocol):
    result = {}
    try:
        if touch_type == 'authorize':

            if direction == 'inbound':
                result = sg.authorize_ingress(
                    CidrIp=scope,
                    FromPort=lower_port,
                    ToPort=uper_port,
                    GroupId=sg_id,
                    IpProtocol=protocol
                )
            else:
                result = sg.authorize_egress(
                    IpPermissions=[
                        {
                            'FromPort': lower_port,
                            'ToPort': uper_port,
                            'IpProtocol': protocol,
                            'IpRanges': [
                                {
                                    'CidrIp': scope
                                }
                            ]
                        }
                    ]
                )
        else:
            if direction == 'inbound':
                result = sg.revoke_ingress(
                    CidrIp=scope,
                    FromPort=lower_port,
                    ToPort=uper_port,
                    GroupId=sg_id,
                    IpProtocol=protocol
                )
            else:
                result = sg.revoke_egress(
                    IpPermissions=[
                        {
                            'FromPort': lower_port,
                            'ToPort': uper_port,
                            'IpProtocol': protocol,
                            'IpRanges': [
                                {
                                    'CidrIp': scope
                                }
                            ]
                        }
                    ]
                )
    except Exception as e:
        traceback.print_exc(file=sys.stdout)

    return result['ResponseMetadata']['HTTPStatusCode']
