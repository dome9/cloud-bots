'''
## sg_single_rule_delete
What it does: Deletes a single rule on a security group
Usage: AUTO: sg_single_rule_delete strict=<true|false> protocol=<TCP|UDP|ALL> scope=<a.b.c.d/e> direction=<inbound|outbound> port=<number>

Example: AUTO: sg_single_rule_delete strict=false protocol=TCP scope=0.0.0.0/0 direction=inbound port=22
Sample GSL: SecurityGroup should not have inboundRules with [scope = '0.0.0.0/0' and port<=22 and portTo>=22]

Conditions and caveats: Deleting a single rule on a security group can be difficult because the problematic port can be nested within a wider range of ports. If SSH is open because a SG has all of TCP open, do you want to delete the whole rule or would you break up the SG into the same scope but port 0-21 and a second rule for 23-end of TCP port range?
Currently the way this is being addressed is using the 'strict' parameter. If it's set as true, CloudBots will only look for the specific port in question. If it's nested within a larger port scopem, it'll be skipped. 
If you set strict to false, then the whole rule that the problematic port is nested in will be removed. 
'''

import boto3
import re
from botocore.exceptions import ClientError

### DeleteSecurityGroupRules ###
def run_action(boto_session,rule,entity,params):
    ## Set up params. We need a role ARN to come through in the params.
    text_output = ""
    usage = "AUTO: sg_single_rule_delete strict=<true|false> protocol=<TCP|UDP> scope=<a.b.c.d/e> direction=<inbound|outbound> port=<number>\n"
    
    if len(params) == 5:
        try:
            for param in params:
                key_value = param.split("=")
                key = key_value[0]
                value = key_value[1]

                if key == "strict":     
                    if value.lower() == "true":
                        strict = True
                        text_output = text_output + "Strict matching for the port to be remediated is set to True\n"
                    elif value.lower() == "false":
                        strict = False
                        text_output = text_output + "Strict matching for the port to be remediated is set to False\n"
                    else: 
                        text_output = text_output + "Strict value doesn't match true or false. Defaulting to true\n"
                
                if key == "protocol":     
                    if value.lower() == "tcp":
                        protocol = "TCP"
                        text_output = text_output + "The protocol to be removed is TCP\n"
                    elif value.lower() == "udp":
                        protocol = "UDP"
                        text_output = text_output + "The protocol to be removed is UDP\n"
                    elif value.lower() == "all":
                        protocol = "ALL"
                        text_output = text_output + "The protocol to be removed is \"ALL\"\n"
                    else: 
                        text_output = text_output + "Protocol not set to TCP, UDP, or ALL. Those are the only three currently supported protocols. Skipping\n" + usage
                        return text_output

                if key == "scope":     
                    scope = value
                    scope_pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$")
                    if scope_pattern.match(scope):
                        text_output = text_output + "Scope to be removed found: %s \n" % scope
                    else:
                        text_output = text_output + "Scope doesn't match expected value (a.b.c.d/e). Skipping.\n" + usage   

                if key == "direction":     
                    if value.lower() == "inbound":
                        direction = "inbound"
                        text_output = text_output + "The rule to be removed is going to be for inbound traffic\n"
                    elif value.lower() == "outbound":
                        direction = "outbound"
                        text_output = text_output + "The rule to be removed is going to be for outbound traffic\n"
                    else: 
                        text_output = text_output + "Traffic direction doesn't match inbound or outbound. Skipping.\n" + usage
                        return text_output

                if key == "port":     
                    try: 
                        port = int(value)
                        text_output = text_output + "Port to be removed: %s \n" % port
                    except ValueError:
                        text_output = text_output + "Port number was not a valid integer. Skipping.\n" + usage
                        return text_output

        except:
            text_output = text_output + "Params handling error. Please check params and try again.\n" + usage
            return text_output

    else:
        text_output = "Wrong amount of params inputs detected. Exiting.\n" + usage
        return text_output

    rule_direction = direction + "Rules" ## The objects are nested in entity['inboundRules'] or outboundRules but we want to heave the direction variable alone for logging later. 
    found_rule = False
    for rule in entity[rule_direction]:
        if scope == rule['scope'] and protocol == rule['protocol']: 
            # 2/3 of the conditions are good. Check for scope now. 
            if strict == True and port == rule['port'] and port == rule['portTo']:
                rule_to_delete = rule
                break

            if strict == False and rule['port'] <= port and rule['portTo'] >= port:
                rule_to_delete = rule
                break

    if rule_to_delete:
        text_output = text_output + "Matching rule found that is going to be deleted. Protocol:%s Direction:%s Port:%s Scope:%s \n" % (protocol, direction, port, scope)
    else:
        text_output = text_output + "No SG rule was found that matches the defined parameters. Skipping\n"
        return text_output


    ###### After deciding what rule to remove - remove it

    # Client for making changes / set up parameters
    sg_id = entity['id']
    portTo = rule['portTo']
    ec2_resource = boto_session.resource('ec2')
    sg = ec2_resource.SecurityGroup(sg_id)

    if protocol == "ALL":
        protocol = "-1" # This is what AWS calls the protocol for "all"

    if direction == "inbound":
        result = sg.revoke_ingress(
            CidrIp=scope,
            FromPort=port,
            GroupId=sg_id,
            IpProtocol=protocol,
            ToPort=portTo
        )

    if direction == "outbound":
        result = sg.revoke_egress(
            IpPermissions=[
                {
                    'FromPort': port,
                    'ToPort': portTo,
                    'IpProtocol': protocol,
                    'IpRanges': [
                        {
                            'CidrIp': scope
                        }
                    ]   
                }
            ]
        )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = text_output + "Security Group rule successfully deleted\n"
    
    return text_output


