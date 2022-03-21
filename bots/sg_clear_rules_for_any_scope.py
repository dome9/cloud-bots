"""
## sg_clear_rules_for_any_scope
What it does:
Usage: sg_clear_rules_for_any_scope <port> <protocol> <direction> <white-list> (<white-list> is not mandatory).
Permissions:
- ec2:RevokeSecurityGroupEgress
- ec2:RevokeSecurityGroupIngress
- ec2:DescribeSecurityGroups
"""


def update_permissions(sg, port, protocol, direction, white_list):
    if direction == 'inbound':
        ip_permissions_to_delete = sg.ip_permissions
    if direction == 'outbound':
        ip_permissions_to_delete = sg.ip_permissions_egress
    i = 0
    cidr_list = []
    for rule in ip_permissions_to_delete:
        if rule.get('IpProtocol') == protocol and rule.get('FromPort') == port and rule.get('ToPort') == port:
            cidr_list = rule.get('IpRanges')
            break
        i += 1
    if i == len(ip_permissions_to_delete):
        return -1
    cidrs_to_remove = []
    for cidr in cidr_list:
        if cidr.get('CidrIp') in white_list:  # if the cidr not in the white list, we don't want to delete it
            cidrs_to_remove.append(cidr)
    for cidr in cidrs_to_remove:
        (ip_permissions_to_delete[i]['IpRanges']).remove(cidr)

    if len(ip_permissions_to_delete[i]['IpRanges']) == 0:
        return -1

    return ip_permissions_to_delete[i]


def run_action(boto_session, rule, entity, params):
    if not 3 <= len(params) <= 4:
        raise ValueError(f"Error: Wrong use of the sg_clear_rules_for_any_scope bot. Usage: "
                         f"sg_clear_rules_for_any_scope <port> <protocol> <direction> <white-list> (<white-list> is "
                         f"not mandatory).\n")

    ec2 = boto_session.resource('ec2')
    sg_id = entity['id']
    sg = ec2.SecurityGroup(sg_id)
    port = int(params[0])
    protocol = params[1]
    direction = (params[2]).lower()
    text_output = ''

    white_list = {'44.229.44.249/32', '44.229.40.33/32', '44.231.221.27/32'}
    ### GET THE WHITE LIST
    print(f'{__file__} - Cloudbot will remove {direction} rules from security group with id: {sg_id}\n')
    print(f'{__file__} - port = {port}, protocol = {protocol}\n')
    print(f'{__file__} - rules with the following cidrs were configured in the white list and will be ignored: {white_list}')

    ip_permissions_to_delete = update_permissions(sg, port, protocol, direction, white_list)
    if ip_permissions_to_delete == -1:
        raise ValueError(f"No {direction} rules in port {port} and protocol {protocol} were found on {sg_id}, or found but exist in the white list. Bot didnt execute.\n")

    print(f'{__file__} - Trying to remove rules... \n')
    if direction == 'inbound':
        result = sg.revoke_ingress(IpPermissions=[ip_permissions_to_delete])
    if direction == 'outbound':
        result = sg.revoke_egress(IpPermissions=[ip_permissions_to_delete])

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        raise ValueError("Unexpected error: %s \n" % str(result))
    else:
        print(f'{__file__} - Done. \n')
        text_output = text_output + f'Successfully removed rules from the specified security group.\n'

    return text_output
