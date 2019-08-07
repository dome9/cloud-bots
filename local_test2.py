
from index import *

message = r'''{
   "status": "Failed",
   "policy": {
       "name": "CLOUDBOTS-PCI",
       "description": "AUTO REMEDIATION FOR AWS PCI"
   },
   "findingKey": "xxLIMNdo/LbKSMgLQyE7bw",
   "bundle": {
       "name": "cloudbots PCI test",
       "description": "Automated Validation of Payment Card Industry (PCI) Data Security Standard Version 3.2 - April 2016.\nFor additional reference: https://s3.amazonaws.com/quickstart-reference/enterprise-accelerator/pci/latest/assets/PCI-DSS-Security-Controls-Mapping.xlsx"
   },
   "reportTime": "2019-08-07T18:19:01.89Z",
   "rule": {
       "name": "Ensure a log metric filter and alarm exist for IAM policy changes",
       "ruleId": "D9.AWS.MON.04",
       "description": "Real-time monitoring of API calls can be achieved by directing CloudTrail Logs to CloudWatch Logs and establishing corresponding metric filters and alarms. It is recommended that a metric filter and alarm be established changes made to Identity and Access Management (IAM) policies.\nMonitoring changes to IAM policies will help ensure authentication and authorization controls remain intact.",
       "remediation": "Perform the following to setup the metric filter, alarm, SNS topic, and subscription:\n1. Create a metric filter based on filter pattern relevant for this check. For More details, refer to CIS Amazon Web Services Foundations Benchmark v1.1.2\nhttps://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf\n2. Create an SNS topic that the alarm will notify Note: you can execute this command once and then re-use the same topic for all monitoring alarms.\n3. Create an SNS subscription to the topic created in step 2 Note: you can execute this command once and then re-use the SNS subscription for all monitoring alarms.\n4. Create an alarm that is associated with the CloudWatch Logs Metric Filter created in step 1 and an SNS topic created in step 2\n\nAdditional Reference:\nCIS Amazon Web Services Foundations Benchmark v1.1.2\nhttps://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf",
       "complianceTags": "10.5|10.6|AUTO: cloudwatch_create_metric_filter adgupta@checkpoint.com IamPolicyChanges",
       "severity": "Medium"
   },
   "account": {
       "id": "514129783023",
       "name": "Dome9-Connect-Raji",
       "vendor": "AWS"
   },
   "entity": {},
   "remediationActions": []
}'''



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

SNS_TOPIC_ARN = "arn:aws:sns:us-west-2:905007184296:eventsToSlack"



lambda_handler(sns_event, context)