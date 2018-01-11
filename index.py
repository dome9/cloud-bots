import boto3
import json
import os
import time
from botocore.exceptions import ClientError

from filter_events import * 
from send_events_and_errors import * 

#Feed in the SNS Topic from an env. variable
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

#Bring the data in and parse the SNS message
def lambda_handler(event, context):

	text_output_array = ["-------------------------\n"]

	raw_message = event['Records'][0]['Sns']['Message']
	message = json.loads(raw_message)

	timestamp = "ReportTime: " + message['ReportTime'] + "\n"
	text_output_array.append(timestamp)

	text_output_array = filter_events(message,text_output_array)
	sendEvent(text_output_array,SNS_TOPIC_ARN)
	return



## LOCAL TESTING

#sample event
event = {
    'Records': [{
        'EventSource': 'aws:sns',
        'EventVersion': '1.0',
        'EventSubscriptionArn': 'arn:aws:sns:us-west-2:621958466464:eventsToSlack:0cf0e80c-1fef-4421-9cc0-b3c102ac7836',
        'Sns': {
            'Type': 'Notification',
            'MessageId': 'd59748d6-f529-532f-bf13-1a1e438fde5c',
            'TopicArn': 'arn:aws:sns:us-west-2:621958466464:eventsToSlack',
            'Subject': 'Dome9 Continuous compliance: Entity status change detected',
            'Message': '{"Policy":{"Name":"*remediationv3","Description":""},"Bundle":{"Name":"* Remediation bundle v2","Description":""},"ReportTime":"2018-01-04T23:10:27.612Z","Rule":{"Name":"Remove Unused Security Groups","Description":"a security group with no attached protected assets. PCI-DSS Section 1.1.6, 1.1.7 Removing Unused Security Groups is the expected outcome of a 6 months firewall review and proper justification for used rules.","Remediation":"Delete Unused Security Groups detected by the Dome9 Report.","ComplianceTags":"PCI-DSS Section 1.1.6| PCI-DSS Section 1.1.7| AUTO: ec2_tag_instance (thisimykey:thisismyvalue)","Severity":"High"},"Status":"Failed","Account":{"Id":"621958466464","Vendor":"Aws"},"Region":"Oregon","Entity":{"description":"dellleettteeme","inboundRules":[],"outboundRules":[{"protocol":"ALL","port":0,"portTo":0,"scope":"0.0.0.0/0","scopeMetaData":null}],"networkAssetsStats":[{"type":"ELBs","count":0},{"type":"instances","count":0},{"type":"RDSs","count":0},{"type":"LambdaFunctions","count":0},{"type":"Redshifts","count":0},{"type":"ApplicationLoadBalancers","count":0},{"type":"EFSs","count":0},{"type":"ElastiCacheClusters","count":0}],"isProtected":false,"vpc":{"cloudAccountId":"89ff48fc-9c8b-4292-a169-d6e938af2dd2","cidr":"10.0.0.0/16","Region":5,"Id":"vpc-c037c1b9","AccountNumber":"621958466464","vpnGateways":[],"internetGateways":[{"externalId":"igw-e49a6d82","vpcAttachments":[{"state":"available","vpcId":"vpc-c037c1b9"}],"name":""}],"dhcpOptionsId":"dopt-b18786d5","instanceTenancy":"default","isDefault":false,"state":"available","tags":{},"name":"testDeleteMe","source":1},"Id":"i-0579293b8a3aeafb9","Type":"SecurityGroup","Name":"test2222","Dome9Id":"2398817","AccountNumber":"621958466464","Region":"us_west_2","source":"db","tags":[]}}',
            'Timestamp': '2018-01-04T23:10:30.652Z',
            'SignatureVersion': '1',
            'Signature': 'f+5JYT19akaX0zwG7P9wW88cvZEGnnGzFCpUgREMrJEw1jg7wGRv45dL7xXwKGaMCvC/nbryu7nxzMW99KnhCGtvNIKIKslbL54A2ZjIseyQdqIWaSMWek7PRlapvCKbJb2wMbpjyJR7AvnPSv20oAGE5/f2Xaf8jPxiVtSVZVL4BwdAXP87tO2WYjDg+j14fan0Rqqg8Rzh38VMwhXXKbu9Vf+jCmfrOqXHp8IRm5+mCxhMsY3CrG4FgX3w3Al5Wp5OPYMq4623Ks58jb2tHE74QwrD35N+Pulv9ijQrJOUtGhWO3mEZFdtW40ZLzIzwhalMCkVaazjUAeiGc/NPw==',
            'SigningCertUrl': 'https://sns.us-west-2.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem',
            'UnsubscribeUrl': 'https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:621958466464:eventsToSlack:0cf0e80c-1fef-4421-9cc0-b3c102ac7836',
            'MessageAttributes': {}
        }
    }]
}


#export SNS_TOPIC_ARN="arn:aws:sns:us-west-2:621958466464:eventsToSlack"
SNS_TOPIC_ARN = "arn:aws:sns:us-west-2:621958466464:eventsToSlack"

context = ""
lambda_handler(event,context)