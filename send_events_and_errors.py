import boto3
import json
import os


# Post the event. Currently this goes to SNS but this can be generalized if needed
def sendEvent(output_message, SNS_TOPIC_ARN):
    output_type = os.getenv('OUTPUT_TYPE', '')
    print(f'{__file__} - output type: {output_type} - TopicArn: {SNS_TOPIC_ARN}')

    if output_type == 'JSON':
        text_output = json.dumps(output_message)
    else:
        bots_messages = ''.join([str(v) for v in output_message.get('Rules violations found', ['N.A'])])
        del output_message['Rules violations found']
        text_output = json.dumps(output_message).replace('"', '').replace('{', '').replace('}', '').replace(',',
                                                                                                            '\n').replace(
            "'", '') + bots_messages

    print(f'{__file__} - text_output: {text_output}')
    sns = boto3.client('sns')

    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=text_output,
        Subject='RemediationLog',
        MessageStructure='string'
    )

    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code > 400:
        print(f'{__file__} - SNS message failed to send!')
        print(f'{__file__} - {str(response)}')
    else:
        print(f'{__file__} - SNS message posted successfully')
