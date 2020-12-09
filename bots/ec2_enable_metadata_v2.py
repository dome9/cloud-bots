'''
## ec2_enable_metadata_v2
What it does: Enables ec2 metadata
Usage: AUTO: ec2_enable_metadata_v2
Sample GSL: cloudtrail where event.name = 'ModifyInstanceMetadataOptions'
Limitations: None
'''
import json
from botocore.exceptions import ClientError
import bots_utils

TIME_DIFF = 3
EVENT_NAME = 'ModifyInstanceMetadataOptions'

### Enable EC2 metadata V2 ###
def run_action(boto_session, rule, entity, params):
    #Get the instance id
    events = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)
    instance_id = get_details_from_event(events)

    try:
        # Enable the metadata
        ec2_client = boto_session.client('ec2')
        result = ec2_client.modify_instance_metadata_options(InstanceId=instance_id, HttpEndpoint='enabled')
        text_output = f"Instance {instance_id} metadata is enabled.\n"

    except ClientError as e:
        text_output = f"Client error: {e}.\n"

    return text_output


## Get the instance ID from the cloudtrail event"
def get_details_from_event(event):
    return json.loads(event['CloudTrailEvent'])['requestParameters']['ModifyInstanceMetadataOptionsRequest']['InstanceId']