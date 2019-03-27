import boto3
from botocore.exceptions import ClientError
import json
import os

#Post the event. Currently this goes to SNS but this can be generalized if needed
def sendEvent(output,SNS_TOPIC_ARN):
	output_type = os.getenv('OUTPUT_TYPE', '')

	if output_type == 'json':
		text_output_str = json.dumps(output)
		sns = boto3.client('sns')
		response = sns.publish(
		TopicArn=SNS_TOPIC_ARN,
		Message=text_output_str,
		Subject='RemediationLog',
		MessageStructure='string')
	else:
		text_output_str = json.dumps(output).replace('"', '').replace('{', '').replace('}', '').replace(',', '')
		sns = boto3.client('sns')
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
