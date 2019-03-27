import boto3
from botocore.exceptions import ClientError
import json
import os


# Post the event. Currently this goes to SNS but this can be generalized if needed
def sendEvent(output, SNS_TOPIC_ARN):
    output_type = os.getenv('OUTPUT_TYPE', '')
    sns = boto3.client('sns')
    text_output_str = ''
    if output_type == 'json':
        text_output_str = json.dumps(output)
    else:
        text_output_str = json.dumps(output).replace('"', '').replace('{', '').replace('}', '').replace(',', '\n')

    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=text_output_str,
        Subject='RemediationLog',
        MessageStructure='string')
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code > 400:
        print("SNS message failed to send!")
        print(str(response))
    else:
        print("SNS message posted successfully")
