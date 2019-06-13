import json
from handle_event import *
from send_events_and_errors import *
from send_logs import *
import time


# Feed in the SNS Topic from an env. variable
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN', '')

# Bring the data in and parse the SNS message
def lambda_handler(event, context):
    start_time = time.time()
    output_message = {}
    print(f'{__file__} - Start running')
    if event['Records'][0]['Sns']['Message']:
        raw_message = event['Records'][0]['Sns']['Message']
    print(f'{__file__}- Raw message - {raw_message}')

    try:  # Normally the event comes through as json
        source_message = json.loads(raw_message)
    except:  # If the event comes through as a dict, take it as it comes (this is usually when testing locally)
        source_message = raw_message

    print(f'{__file__} - Source message - {source_message}')

    output_message['ReportTime'] = source_message.get('reportTime', 'N.A')

    if (source_message.get('account')):
        output_message['Account id'] = source_message['account'].get('id', 'N.A')

    output_message['findingKey'] = source_message.get('findingKey', 'N.A')
    try:
        post_to_sns = handle_event(source_message, output_message)
    except Exception as e:
        post_to_sns = True
        output_message['Handle event failed'] = str(e)

    print(f'{__file__} - output message - {output_message}')

    # After the bot is called, post it to SNS for output logging
    if SNS_TOPIC_ARN != '' and post_to_sns:
        sendEvent(output_message, SNS_TOPIC_ARN)

    if not SNS_TOPIC_ARN:
        print(f'{__file__} - SNS topic out was not defined!')

    send_logs_to_dome9 = os.getenv('SEND_LOGS_TO_DOME9', '')
    if(send_logs_to_dome9 == 'True'):
        send_logs(output_message, start_time, source_message.get('account').get('vendor'))
    return
