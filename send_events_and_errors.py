import boto3
from botocore.exceptions import ClientError


#Post the event. Currently this goes to SNS but this can be generalized if needed
def sendEvent(full_event_to_send,SNS_TOPIC_ARN): 
	full_event_to_send.append("-------------------------\n")
	#turn it from an array to a string
	full_event_to_send = ''.join(full_event_to_send)

	sns = boto3.client('sns')

	response = sns.publish(
		TopicArn=SNS_TOPIC_ARN,
		Message=full_event_to_send,
		Subject='RemediationLog',
		MessageStructure='string'
	)
	#To do - Add more error handling in here if >200
	status_code = response['ResponseMetadata']['HTTPStatusCode']
	if status_code > 400:
		print("SNS message failed to send!")
		print(str(response))
	else:
		print("SNS message posted successfully")


	
			
