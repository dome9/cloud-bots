
from index import *

"""
    This is a local test file to test and debug your bots execution in your local environment
    The way to use it is by filling the message variable with the relevant Dome9 notification record that should trigger your bot 
    You can use some notification samples from sample_compliance_notification folder 
    Or sample it from the output sns that Dome9 send it to 
"""

message = r'''
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