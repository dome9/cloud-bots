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

    timestamp = "ReportTime: " + message['reportTime'] + "\n"
    text_output_array.append(timestamp)

    text_output_array = handle_event(message,text_output_array)
    
    if SNS_TOPIC_ARN != '':
        sendEvent(text_output_array,SNS_TOPIC_ARN)
    else:
        print('NO SNS out was defined')
        print(text_output_array)
    return


