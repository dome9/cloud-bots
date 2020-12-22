"""
## delete_image_from_ecs_repo
What it does: delete an image from  ECS repository
Usage: AUTH: delete_image_from_ecs_repo
Limitations: none
"""

import boto3
from botocore.exceptions import ClientError
import datetime
from dateutil.tz import tzlocal
import json
import bots_utils

EVENT_NAME = 'DescribeImageScanFindings'

def run_action(boto_session, rule, entity, params, report_time):
    # creating ecr client
    ecr_client = boto_session.client('ecr')

    # looking for the event
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)

    # taking all the image details that we need to delete the malicious image
    registry_id = event['responseElements']['registryId']
    repository_name = event['responseElements']['repositoryName']
    image_name =  event['responseElements']['imageId']['imageTag']
    image_digest = event['responseElements']['imageId']['imageDigest']

    ecr_client.batch_delete_image(registryId=registry_id,
                                  repositoryName= repository_name,
                                  imageIds=[
                                      {
                                          'imageDigest' : image_digest,
                                          'imageTag' : image_name
                                      }
                                  ])

def format_time(report_time):
    # format the time from string to datetime object
    # 2020-11-11T14:03:43.123Z
    report_time = datetime.datetime.strptime(report_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    return report_time

def find_event(boto_session, report_time):
    # create CloudTrail client
    client = boto_session.client('cloudtrail')

    # converting the time from utc to Israel time zone
    report_time = report_time.replace(tzinfo=tzlocal())
    # taking 20 minutes before the alert popped in logic
    start_time = report_time + datetime.timedelta(minutes=-20)



    # get the event details
    response = client.lookup_events(LookupAttributes=[{'AttributeKey' : 'EventName', 'AttributeValue' : EVENT_NAME}],
                                    StartTime=start_time,
                                    EndTime=report_time)

    return response['Events'][0]['CloudTrailEvent']  if len(response['Events']) == 1 else None
