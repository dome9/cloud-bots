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

    try:
        ecr_client.batch_delete_image(registryId=registry_id,
                                  repositoryName= repository_name,
                                  imageIds=[
                                      {
                                          'imageDigest' : image_digest,
                                          'imageTag' : image_name
                                      }
                                  ])
    except ClientError as e:
        return f"Unexpected error: {e} \n"
