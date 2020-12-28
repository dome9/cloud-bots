"""
## ecs_delete_repository_image
What it does: delete an image from  ECS repository
Usage: AUTH: ecs_delete_repository_image
Limitations: none

This bot is relevant to logic only and it's Running Following the DescribeImageScanFindings event
"""

import boto3
from botocore.exceptions import ClientError
import bots_utils

EVENT_NAME = 'DescribeImageScanFindings'

def run_action(boto_session, rule, entity, params, report_time):
    # creating ecr client
    ecr_client = boto3.client('ecr')

    # looking for the event
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME)

    if event is None:
        return "Error when looking for the DescribeImageScanFindings event, 0 events returned"

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

