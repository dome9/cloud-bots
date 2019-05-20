import boto3
import json
import os


#Post the event. Currently this goes to SNS but this can be generalized if needed
def sendEvent(output_message,SNS_TOPIC_ARN):
	output_type = os.getenv('OUTPUT_TYPE', '')
	print("Dome9 Cloud bots - send_events_and_errors.py - output type: {} - TopicArn: {}".format(output_type, SNS_TOPIC_ARN))

	if output_type == 'JSON':
		text_output = json.dumps(output_message)
	else:
		bot_message = "\nBot message :" + output_message.get('Bot message')
		del output_message['Bot message']
		text_output = json.dumps(output_message).replace('"', '').replace('{', '').replace('}', '').replace(',', '\n').replace("'",'') + bot_message

	print("Dome9 Cloud bots - send_events_and_errors.py - text_output: {}".format(text_output))
	sns = boto3.client('sns')

	response = sns.publish(
		TopicArn=SNS_TOPIC_ARN,
		Message=text_output,
		Subject='RemediationLog',
		MessageStructure='string'
	)

	status_code = response['ResponseMetadata']['HTTPStatusCode']
	if status_code > 400:
		print("Dome9 Cloud bots - send_events_and_errors.py - SNS message failed to send!")
		print("Dome9 Cloud bots - send_events_and_errors.py - {}".format(str(response)))
	else:
		print("Dome9 Cloud bots - send_events_and_errors.py - SNS message posted successfully")
