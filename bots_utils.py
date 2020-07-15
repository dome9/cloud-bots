"""
Bots Utilities File
"""

# imports
import re

PORT_TO = 'portTo'
PORT_FROM = 'port'
PROTOCOL = 'protocol'
SCOPE = 'scope'
ALL_TRAFFIC_PORT = 0
ALL_TRAFFIC_PROTOCOL = '-1'

"""
#################################
Security Groups relates functions :
#################################
"""

"""
returns a string of rule's id by scope,port,direction,etc.
"""


def stringify_rule(rule):
    return 'rule_id: ' + rule[SCOPE] + ', ' + str(rule[PORT_FROM]) + ', ' + str(rule[PORT_TO]) + ', ' + \
           rule[PROTOCOL].lower() + '; '


"""
checks for ip validity as cidr, fix it to be right otherwise
"""


def verify_scope_is_cidr(rule):
    ip = re.split('/|\.', str(rule[SCOPE]))  # break ip to blocks
    rule[SCOPE] = ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + ip[3] + '/' + ip[4]
    pass
