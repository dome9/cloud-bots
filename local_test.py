
from index import *

"""
    This is a local test file to test and debug your bots execution in your local environment
    The way to use it is by filling the message variable with the relevant Dome9 notification record that should trigger your bot 
    You can use some notification samples from sample_compliance_notification folder 
    Or sample it from the output sns that Dome9 send it to 
"""

message = r'''
{
  "status": "Failed",
  "policy": {
    "name": "Logic-Default-Console-Notification",
    "description": ""
  },
  "findingKey": "C3ZlwCS9gKJd2H9Tx5yRNw",
  "findingId": "C3ZlwCS9gKJd2H9Tx5yRNw",
  "cloudGuardAccountId": "39801",
  "origin": "CIEM",
  "bundle": {
    "name": "Entitlement Management",
    "id": 802
  },
  "reportTime": "2023-01-29T11:54:43Z",
  "rule": {
    "name": "Overprivileged IamRole",
    "description": "Excessive permissions were granted to IamRole:AwsAcmCertificate-metric-role-qa.\nSetting excessive permissions increases your attack surface.\nPlease take suggested remediation steps to ensure only necessary privileges are assigned.",
    "remediation": "After reviewing the suggested changes, replace your current policy with suggested policy.",
    "logicHash": "1B2M2Y8AsgTpgAmY7PhCfg",
    "severity": "Medium"
  },
  "account": {
    "id": "941298424820",
    "name": "D9-SB-PREQA",
    "vendor": "AWS",
    "dome9CloudAccountId": "90c256e3-5b10-4e92-b5e1-551590b5ed21",
    "organizationalUnitId": "00000000-0000-0000-0000-000000000000",
    "organizationalUnitPath": ""
  },
  "region": "",
  "entity": {
    "type": "Default",
    "id": "arn:aws:iam::941298424820:role/AwsAcmCertificate-metric-role-qa",
    "name": "AwsAcmCertificate-metric-role-qa",
    "accountNumber": "39801",
    "region": ""
  },
  "remediationActions": [
    "{\"RedundantPermissions\":[{\"Policy\":\"arn:aws:iam::941298424820:policy/AwsAcmCertificate-sqs-Policy-qa\",\"Suggestions\":[{\"Original\":{\"action\":\"sqs:*\",\"resource\":\"arn:aws:sqs:us-west-2:941298424820:AwsAcmCertificate-CloudAccountRegion-qa\"},\"Suggested\":[{\"action\":[\"sqs:SendMessage\",\"sqs:ReceiveMessage\",\"sqs:ListQueues\",\"sqs:ListQueueTags\",\"sqs:ListDeadLetterSourceQueues\",\"sqs:GetQueueUrl\",\"sqs:GetQueueAttributes\",\"sqs:DeleteMessage\",\"sqs:ChangeMessageVisibility\"],\"resource\":\"arn:aws:sqs:us-west-2:941298424820:AwsAcmCertificate-CloudAccountRegion-qa\"}]},{\"Original\":{\"action\":\"sqs:*\",\"resource\":\"arn:aws:sqs:us-west-2:941298424820:AwsAcmCertificate-CloudAccount-qa\"},\"Suggested\":[{\"action\":[\"sqs:SendMessage\",\"sqs:ReceiveMessage\",\"sqs:ListQueues\",\"sqs:ListQueueTags\",\"sqs:ListDeadLetterSourceQueues\",\"sqs:GetQueueUrl\",\"sqs:GetQueueAttributes\",\"sqs:DeleteMessage\",\"sqs:ChangeMessageVisibility\"],\"resource\":\"arn:aws:sqs:us-west-2:941298424820:AwsAcmCertificate-CloudAccount-qa\"}]}]}]}",
    "{\"Link\":\"https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_delete.html\",\"SuggestedRole\":\"{\\\"Version\\\":\\\"2012-10-17\\\",\\\"Statement\\\":[{\\\"Action\\\":[\\\"sqs:GetQueueAttributes\\\",\\\"sqs:GetQueueUrl\\\",\\\"sqs:ListDeadLetterSourceQueues\\\",\\\"sqs:ListQueues\\\"],\\\"Resource\\\":[\\\"*\\\"],\\\"Effect\\\":\\\"Allow\\\",\\\"Sid\\\":\\\"CloudGuardGenerated0\\\"},{\\\"Action\\\":[\\\"cloudwatch:PutMetricData\\\"],\\\"Resource\\\":[\\\"*\\\"],\\\"Effect\\\":\\\"Allow\\\",\\\"Sid\\\":\\\"CloudGuardGenerated1\\\"},{\\\"Action\\\":[\\\"sqs:SendMessage\\\",\\\"sqs:ReceiveMessage\\\",\\\"sqs:ListQueues\\\",\\\"sqs:ListQueueTags\\\",\\\"sqs:ListDeadLetterSourceQueues\\\",\\\"sqs:GetQueueUrl\\\",\\\"sqs:GetQueueAttributes\\\",\\\"sqs:DeleteMessage\\\",\\\"sqs:ChangeMessageVisibility\\\"],\\\"Resource\\\":[\\\"arn:aws:sqs:us-west-2:941298424820:AwsAcmCertificate-CloudAccountRegion-qa\\\",\\\"arn:aws:sqs:us-west-2:941298424820:AwsAcmCertificate-CloudAccount-qa\\\"],\\\"Effect\\\":\\\"Allow\\\",\\\"Sid\\\":\\\"CloudGuardGenerated2\\\"}]}\",\"Info\":\"Excessive permissions were granted to IamRole:AwsAcmCertificate-metric-role-qa.\\nSetting excessive permissions increases your attack surface.\\nPlease take suggested remediation steps to ensure only necessary privileges are assigned.\"}",
    "iam_entity_create_and_attach_permission_boundary dryRun"
  ],
  "action": "Detect"
}
'''



sns_event = {
    'Records': [{
        'EventSource': 'aws:sns',
        'EventVersion': '1.0',
        'EventSubscriptionArn': 'arn:aws:sns:us-west-2:905007184296:eventsToSlack:0cf0e80c-1fef-4421-9cc0-b3c102ac7836',
        'Sns': {
            'Type': 'Notification',
            'MessageId': 'd59748d6-f529-532f-bf13-1a1e438fde5c',
            'TopicArn': 'arn:aws:sns:us-west-2:905007184296:eventsToSlack',
            'Subject': 'Dome9 Continuous compliance: Entity status change detected',
            'Message': message,
            'Timestamp': '2018-01-04T23:10:30.652Z',
            'SignatureVersion': '1',
            'Signature': 'fKnhCGtvNIKIKslbL54A2ZjIiGc/NPw==',
            'SigningCertUrl': 'https://sns.us-west-2.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem',
            'UnsubscribeUrl': 'https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:905007184296:eventsToSlack:0cf0e80c-1fef-4421-9cc0-b3c102ac7836',
            'MessageAttributes': {}
        }
    }]
}




context =""


lambda_handler(sns_event, context)