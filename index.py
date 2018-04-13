import boto3
import json
import os
from botocore.exceptions import ClientError

from handle_event import * 
from send_events_and_errors import * 

#Feed in the SNS Topic from an env. variable
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN','')

#Bring the data in and parse the SNS message
def lambda_handler(event, context):

    text_output_array = ["-------------------------\n"]

    raw_message = event['Records'][0]['Sns']['Message']
    message = json.loads(raw_message)

    timestamp = "ReportTime: " + str(message['reportTime']) + "\n"

    text_output_array.append(timestamp)

    event_account = "Account id:" + message['account']['id'] + "\n"
    text_output_array.append(event_account)

    try:
        text_output_array, post_to_sns = handle_event(message,text_output_array)
    except Exception as e: 
        post_to_sns = True
        text_output_array.append("Handle_event failed\n")
        text_output_array.append(str(e))

    
    if SNS_TOPIC_ARN != '' and post_to_sns:
        sendEvent(text_output_array,SNS_TOPIC_ARN)

    if not SNS_TOPIC_ARN:
        print("SNS topic out was not defined!")

    print(text_output_array)
    return


