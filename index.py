import json
from handle_event import * 
from send_events_and_errors import * 

#Feed in the SNS Topic from an env. variable
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN','')

#Bring the data in and parse the SNS message
def lambda_handler(event, context):
    output_message = {}
    print("Dome9 Cloud bots - index.py - Start running")
    if event['Records'] and len(event['Records']) and event['Records'][0] and event['Records'][0]['Sns'] and event['Records'][0]['Sns']['Message']:
        raw_message = event['Records'][0]['Sns']['Message']
    print("Dome9 Cloud bots - index.py - Raw message - {}".format(raw_message))

    try: 
        try: # Normally the event comes through as json
            source_message = json.loads(raw_message)
        except: # If the event comes through as a dict, take it as it comes (this is usually when testing locally)
            source_message = raw_message
    except: 
        print("Dome9 Cloud bots - index.py - Unexpected error. Exiting.")
        return

    print("Dome9 Cloud bots - index.py - Source message - {}".format(source_message))

    if(source_message.get('reportTime')):
        output_message['ReportTime'] = str(source_message['reportTime'])

    if(source_message.get('account') and source_message.get('account').get('id')):
        output_message['Account id'] = source_message['account']['id']

    if source_message.get('findingKey'):
        output_message['Finding key'] = source_message['findingKey']
    else:
        output_message['Finding key'] = 'N.A'

    try:
       post_to_sns = handle_event(source_message,output_message)
    except Exception as e: 
        post_to_sns = True
        output_message['Handle event failed'] = str(e)

    print("Dome9 Cloud bots - index.py - output message - {}".format(output_message))
    sendEvent(output_message, SNS_TOPIC_ARN)

    # After the bot is called, post it to SNS for output logging
    if SNS_TOPIC_ARN != '' and post_to_sns:
        sendEvent(output_message,SNS_TOPIC_ARN)

    if not SNS_TOPIC_ARN:
        print("Dome9 Cloud bots - index.py - SNS topic out was not defined!")

    return