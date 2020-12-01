'''
## ec2_enable_metadata_v2
What it does: Enables ec2 metadata
Usage: AUTO: ec2_enable_metadata_v2
Sample GSL: cloudtrail where event.name = 'ModifyInstanceMetadataOptions'
Limitations: None
'''
import botocore.exceptions
from datetime import datetime, timedelta
import json
from botocore.exceptions import ClientError

TIME_DIFF = 3
EVENT_NAME = 'ModifyInstanceMetadataOptions'

### Enable EC2 metadata V2 ###
def run_action(boto_session, rule, entity, params, message):
    #Get the instance id
    instance_id = entity.get('id')

    get_event_from_cloudtrail(boto_session, message, "Test")

    try:
        # Enable the metadata
        ec2_client = boto_session.client('ec2')
        result = ec2_client.modify_instance_metadata_options(InstanceId=instance_id, HttpEndpoint='enabled')
        text_output = f"Instance {instance_id} metadata is enabled.\n"

    except ClientError as e:
        text_output = f"Client error: {e}.\n"

    return text_output

def get_event_from_cloudtrail(boto_session, message, user_name):
    # Get event from cloudtrail
    cloudtrail_client = boto_session.client('cloudtrail')

    # Get event time from message - to find it in cloudtrail
    alert_time = datetime.strptime(json.loads(message['additionalFields'][0]['value'])['alertWindowStartTime'],
                                   '%Y-%m-%dT%H:%M:%SZ')
    # Adjust time format for the event search
    start_time = alert_time - timedelta(minutes=TIME_DIFF)
    end_time = alert_time + timedelta(minutes=TIME_DIFF)
    # Look up events in cloudtrail
    try:
        events = cloudtrail_client.lookup_events(LookupAttributes=[
            {'AttributeKey': 'EventName', 'AttributeValue': EVENT_NAME}],
            StartTime=start_time, EndTime=end_time)

    except botocore.exceptions.ClientError as e:
        return 'Client error: %s \n' % e
    # Filter the result events to find the most relevant one
    return filter_events(events['Events'], alert_time, user_name)


def filter_events(cloudtrail_events, alert_time, user_name):
    # Make list of events related to the relevant user
    events = [event for event in cloudtrail_events if user_name in event['Resources'][0]['ResourceName']]

    # If list contains only 1 event - return it
    if len(events) == 1:
        return events[0]
    # If there are more than 1 event - find the event that occurred in the nearest time to the alert time
    try:
        return min(events, key=lambda event: abs(
            alert_time - datetime.strptime(json.loads(event['CloudTrailEvent'])['eventTime'], '%Y-%m-%dT%H:%M:%SZ')))
        # No events found
    except ValueError:
        return None


def get_details_from_event(event):
    return json.loads(event['CloudTrailEvent'])['requestParameters']['groupName']
