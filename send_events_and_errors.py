import boto3
from botocore.exceptions import ClientError


#Post the event. Currently this goes to SNS but this can be generalized if needed
def sendEvent(text_output_array,SNS_TOPIC_ARN,post_to_sns): 
	text_output_array.append("-------------------------\n")
	#turn it from an array to a string
	text_output_str = ''.join(text_output_array)

	if post_to_sns:
		sns = boto3.client('sns')

		response = sns.publish(
			TopicArn=SNS_TOPIC_ARN,
			Message=text_output_str,
			Subject='RemediationLog',
			MessageStructure='string'
		)

		status_code = response['ResponseMetadata']['HTTPStatusCode']
		if status_code > 400:
			print("SNS message failed to send!")
			print(str(response))
		else:
			print("SNS message posted successfully")


		#print it for the logs too
	print(text_output_str)
			
