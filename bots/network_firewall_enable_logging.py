"""
## network_firewall_enable_logging
What it does: Enable logging (Flow Logs or Alert) for a network firewall. The log destination type must be specified, the options are: S3, CloudWatchLogs, KinesisDataFirehose.
For S3 and CloudWatchLogs, the bot can create the log destination, by adding 'create' as a third parameter. For KinesisDataFirehose, the name of the delivery stream MUST be provided
as a parameter.
Usage: AUTO network_firewall_enable_logging <LoggingType> <LogDestinationType> <LogDestination>
<LoggingType> can be: FLOW, ALERT
<LogDestinationType> can be: S3, CloudWatchLogs, KinesisDataFirehose (Case-Sensitive!)
Examples:
network_firewall_enable_logging FLOW S3 create (the bot will create the bucket)
network_firewall_enable_logging ALERT CloudWatchLogs create (the bot will create the log group)
network_firewall_enable_logging FLOW S3 my-bucket (logs will be sent to my-bucket. if there is a prefix, please provide it like this: my-bucket/prefix)
network_firewall_enable_logging FLOW CloudWatchLogs my-log-group (logs will be sent to my-log-group)
network_firewall_enable_logging FLOW KinesisDataFirehose my-delivery-stream (logs will be sent to my-delivery-stream)
Limitations: None
"""

import json
from botocore.exceptions import ClientError
import bots_utils as utils

permissions_link = 'https://github.com/dome9/cloud-bots/blob/master/template.yml'
relaunch_stack = 'https://github.com/dome9/cloud-bots#update-cloudbots'


def run_action(boto_session, rule, entity, params):
    if len(params) != 3:
        return f"Error: Wrong use of the network_firewall_enable_logging bot. Usage: network_firewall_enable_logging <LoggingType> <LogDestinationType> <LogDestination>. <LoggingType> can be one of the following: flow, alert. <LogDestinationType> can be one of the following: S3, CloudWatchLogs, KinesisDataFirehose. \n"
    if params[0].upper() not in ['FLOW','ALERT']:
        return f"Error: Wrong use of the network_firewall_enable_logging bot. Usage: network_firewall_enable_logging <LoggingType> <LogDestinationType> <LogDestination>. <LoggingType> can be one of the following: flow, alert. \n"
    if params[1] not in ['S3', 'CloudWatchLogs', 'KinesisDataFirehose']:
        return f"Error: Wrong use of the network_firewall_enable_logging bot. Usage: Usage: network_firewall_enable_logging <LoggingType> <LogDestinationType> <LogDestination>. <LogDestinationType> can be one of the following (Case Sensitive): S3, CloudWatchLogs, KinesisDataFirehose. \n"
    logging_type = params[0].upper()
    dest_type = params[1]
    dest = params[2]

    if dest.lower() == 'create' and dest_type not in ['S3', 'CloudWatchLogs']:
        return f"Error: Wrong use of the network_firewall_enable_logging bot. The destination can be created by the bot only for S3 or CloudWatchLogs. \n"
    print(f'{__file__} - Logs destination type: {dest_type} \n')
    if dest.lower() == 'create':
        account = entity['accountNumber']
        region = entity['region'].replace("_","-")
        if dest_type.lower() == 's3':
            bucket_name = f'{account}-s3-network-firewall-{logging_type.lower()}-logs-{region}'
            success, msg = utils.create_bucket(boto_session, entity, bucket_name)
            if success:
                dest = msg
            else:
                return msg
        if dest_type == 'CloudWatchLogs':
            log_group_name = f'{account}-cloudwatch-network-firewall-{logging_type.lower()}-logs-{region}'
            success, msg = utils.create_log_group(boto_session, entity, log_group_name)
            if success:
                dest = msg
            else:
                return msg

    client = boto_session.client('network-firewall')
    text_output = ''

    if dest_type == 'S3':
        bucket_and_prefix = dest.split("/")
        if len(bucket_and_prefix) == 1:
            log_dest_dict = {"bucketName": dest}
        else:
            log_dest_dict = {"bucketName": bucket_and_prefix[0], "prefix": bucket_and_prefix[1]}
    elif dest_type == 'CloudWatchLogs':
        log_dest_dict = {"logGroup": dest}
    elif dest_type == 'KinesisDataFirehose':
        log_dest_dict = {"deliveryStream": dest}
    print(f'{__file__} - Logs destination is: {log_dest_dict} \n')

    try:
        entity_name = entity['name']
        print(f'{__file__} - Updating logging configuration... \n')
        result = client.update_logging_configuration(
            FirewallArn=entity['id'],
            LoggingConfiguration={
                'LogDestinationConfigs': [
                    {
                        'LogType': logging_type,
                        'LogDestinationType': dest_type,
                        'LogDestination': log_dest_dict
                    },
                ]
            }
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
        else:
            print(f'{__file__} - Done. \n')
            text_output = text_output + f'Successfully enabled {logging_type.lower()} logging for network firewall named {entity_name}. Logs will be sent to {dest_type}. Details: {log_dest_dict} \n'

    except ClientError as e:
        text_output = f"Unexpected client error: {e} \n"
        if 'AccessDenied' in e.response['Error']['Code']:
            text_output = text_output + f"Make sure your dome9CloudBots-RemediationFunctionRole is updated with the relevant permissions. The permissions can be found here: {permissions_link}. You can update them manually or relaunch the CFT stack as described here: {relaunch_stack} \n"

    return text_output
