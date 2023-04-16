import json
import requests
import base64
from botocore.exceptions import ClientError
from datetime import datetime

def send_logs_api_gateway(message):
    url = message.get('logsHttpEndpoint')
    apiKey = message.get('logsHttpEndpointKey')
    streamName = message.get('logsHttpEndpointStreamName')
    streamPartitionKey = message.get('logsHttpEndpointStreamPartitionKey')

    if ((url is not None) and (apiKey is not None) and (streamName is not None) and (streamPartitionKey is not None)):
        findingKey = message.get('findingKey')
        execution_time = datetime.now()
        dome9AccountId = message.get('dome9AccountId')
        vendor = message.get('vendor')
        accountId = message.get('Account id')
        executionId = message.get('executionId')

        for bot in message.get('Rules violations found', []):

            if "Execution status" in bot:
                bot["ExecutionStatus"] = bot.pop("Execution status")

            if "Bot message" in bot:
                bot["BotMessage"] = bot.pop("Bot message")

            logMessage = {
                "logType": "feedback",
                "dome9AccountId": dome9AccountId,
                "vendor": vendor,
                "findingKey": findingKey,
                "envCloudAccountId": accountId,
                "executionId": executionId,
                "remediationInfo": bot,
                "executionTime": str(execution_time)
            }
            json_bytes = (json.dumps(logMessage) + '\n').encode('utf-8')
            # Encode the JSON bytes as base64
            base64_bytes = base64.b64encode(json_bytes)
            # Convert the base64-encoded bytes to a string
            base64_string = base64_bytes.decode('utf-8')

            headers = {"Content-Type": "application/json", "x-api-key": apiKey}

            data = {"Data": base64_string,
                    "PartitionKey": streamPartitionKey,
                    "StreamName": streamName}
            try:
                response = requests.post(url, json=data, headers=headers)
            except ClientError as e:
                print(f'bot feedback Failed set post request-' + e)

            if (response.status_code == 200 and "SequenceNumber" in response.text and "ShardId" in response.text):
                print(f'{findingKey} - bot feedback was reported successfully')
            else:
                print(f'{findingKey} bot feedback Failed {response.text}')
