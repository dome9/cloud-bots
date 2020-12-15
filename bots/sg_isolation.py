'''
## sg_isolation
What it does: isolate the inbound/outbound traffic rules
Usage: AUTO: sg_isolation
Limitation: most get entity which contain security group id.
Note: can trigger the sg_revert_modification bot.
'''

import boto3
from botocore.exceptions import ClientError

# isolate the traffic of the sg - remove all the traffic rules (cancel any inbound/outbound traffic of the sg)
def isolate_security_group_traffic(security_group, type):
    revoke_function = {'inbound': security_group.revoke_ingress, 'outbound': security_group.revoke_egress}
    # get the inbound/outbound rules for remove.
    if type == 'inbound':
        rules = security_group.ip_permissions
    else: # type == outbound
        rules = security_group.ip_permissions_egress

    # if there is inbound/outbound rules - remove them.
    if rules != []:
        # take care to the client response (write to him which rules has been removed from the sg)
        text_output = f"{type} rules that has been removed by sg_isolation action: {rules} \n"

        # remove the inbound/outbound rules of the sg:
        response = revoke_function[type](GroupId=security_group.group_id, IpPermissions=rules)

        # check if rules removed successfully
        if (response.get('UnknownIpPermissions') == []):
            text_output += f"all {type} rules removed successfully"
        else:
            text_output += f"Problematic {type} rules: \n {response.get('UnknownIpPermissions')}. they didn't removed (didn't found in {security_group.group_id})"
    else:
        text_output = f"there are no {type} rules for remove \n"

    return text_output

# get the entity (security group) id and check it's really sg id(template of "sg-"*).
def get_security_id_for_isolation(entity):
    if entity.get('id') != None and entity.get('id')[:3] == 'sg-':
        return entity.get('id')
    elif entity.get('name') != None and entity.get('name')[:3] == 'sg-': # sometimes the sg_name its the sg id
        return entity.get('name')
    else:
        return None


### isolate security group -- core method
def run_action(boto_session, rule, entity, params):
    text_output = ''

    # getting the parameters needed for all functions
    sg_id = get_security_id_for_isolation(entity)
    if sg_id == None:
        return f"isolation failed, entity most contain the security group id. entity name recevied: {entity.get('name')}, entity id recevied: {entity.get('id')}"

    # getting the sg (for isolation) from ec2 recourse
    ec2 = boto_session.resource('ec2')
    security_group = ec2.SecurityGroup(sg_id)

    try:
        # isolate the sg traffic:
        text_output += isolate_security_group_traffic(security_group, "inbound")
        text_output += isolate_security_group_traffic(security_group, "outbound")

    except ClientError as e:
        text_output += f'Unexpected error: {e}\n'

    return text_output
