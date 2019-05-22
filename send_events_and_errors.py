import boto3
import json
import os


def parse_rule_violations(rule_violations):
    rule_violations_text = ''
    for rule in rule_violations:
        bot_message = rule.get('Bot message')
        del rule['Bot message']
        rule_violations_text = ''.join([rule_violations_text,
                json.dumps(rule).replace('"', '').replace('{', '').replace('}', '').replace(',', '\n').replace("'", '') , '\nBot message: ' , bot_message])
    return rule_violations_text


# Post the event. Currently this goes to SNS but this can be generalized if needed
def sendEvent(output_message, SNS_TOPIC_ARN):
    output_type = os.getenv('OUTPUT_TYPE', '')
    print(f'{__file__} - output type: {output_type} - TopicArn: {SNS_TOPIC_ARN}')

    if output_type == 'JSON':
        text_output = json.dumps(output_message)
    else:
        bots_messages = parse_rule_violations(
            output_message.get('Rules violations found', ['N.A']))
        del output_message['Rules violations found']
        text_output = ''.join([json.dumps(output_message).replace('"', '').replace('{', '').replace('}', '').replace(',', '\n').replace(
            "'", ''), '\nRule violations found:\n', bots_messages])

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
