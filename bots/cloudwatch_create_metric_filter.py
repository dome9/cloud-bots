'''
## cloudwatch_create_metric_filter
What it does: Creates CloudWatch Metric Filters to match the CIS Benchmark. A metric alarm and SNS subscripion is created as well
Usage: AUTO: cloudwatch_create_metric_filter <email_address> <filter1> <filter2> .... 
Limitations: Cloudtrail needs to be set up to send the logs to a CloudWatchLogs group first.   
Default: SNS topic name is CloudTrailMetricFilterAlerts
Available filters are: UnauthorizedApiCalls, NoMfaConsoleLogins, RootAccountLogins, IamPolicyChanges, CloudTrailConfigurationChanges, FailedConsoleLogins, DisabledOrDeletedCmks, S3BucketPolicyChanges, AwsConfigChanges, SecurityGroupChanges, NetworkAccessControlListChanges, NetworkGatewayChanges, RouteTableChanges, VpcChanges
'''

import boto3
import json
import re
from botocore.exceptions import ClientError

def create_filter(boto_session,log_group,filter_name,filter_pattern,metric_name,metric_value):
  cloudwatchlogs_client = boto_session.client('logs')

  try:
    #Give the config somewhere to go
    result = cloudwatchlogs_client.put_metric_filter(
        logGroupName=log_group,
        filterName=filter_name,
        filterPattern=filter_pattern,
        metricTransformations=[
            {
                'metricName': metric_name,
                'metricNamespace': 'CISBenchmark',
                'metricValue': metric_value
            },
        ]
    )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s " % str(result)
    else:
        text_output = "Metric filter created for filter: %s " % filter_name  

  except ClientError as e:
      text_output = "Unexpected error: %s " % e

  return text_output

def create_topic(boto_session,topic_name):
    sns_client = boto_session.client('sns')

    try:
        #Give the config somewhere to go
        result = sns_client.create_topic(Name=topic_name)
 
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s " % str(result)
        else:
            text_output = "SNS topic created (or already existed): %s " % topic_name

    except ClientError as e:
        text_output = "Unexpected error: %s " % e

    return text_output


def create_subscription(boto_session,topic_arn,email_address):
    sns_client = boto_session.client('sns')

    try: # Check if there's already a subscription. If it's already there and we re-add it then they get another confirmation email which can be annoying.
        result = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)

        for subscription in result['Subscriptions']:
            if subscription['Endpoint'] == email_address:
                text_output = "Email address %s already has a subscription to this topic %s. Skipping" % (email_address,topic_arn)
                return text_output

    except ClientError as e:
            text_output = "Unexpected error: %s " % e

    try:
        #Give the config somewhere to go
        result = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s " % str(result)
        else:
            text_output = "SNS subscription created for: %s " % email_address

    except ClientError as e:
        text_output = "Unexpected error: %s " % e

    return text_output 


def create_alarm(boto_session,filter_name,topic_arn):
    cloudwatch_client = boto_session.client('cloudwatch')

    try:
      #Give the config somewhere to go
      alarm_name = filter_name + ' Alarm'
      result = cloudwatch_client.put_metric_alarm(
          AlarmName=alarm_name, 
          AlarmDescription='Metric alarm for CloudTrail Metrics', 
          ActionsEnabled=True,
          AlarmActions=[topic_arn],
          MetricName=filter_name,
          Namespace='CISBenchmark',
          Statistic='Sum',
          Period=300,
          EvaluationPeriods=1,
          Threshold=1,
          ComparisonOperator='GreaterThanOrEqualToThreshold'
      )

      
      responseCode = result['ResponseMetadata']['HTTPStatusCode']
      if responseCode >= 400:
          text_output = "Unexpected error: %s " % str(result)
      else:
          text_output = "CloudWatch alarm created: \"%s\" " % alarm_name

    except ClientError as e:
        text_output = "Unexpected error: %s " % e

    return text_output 



def run_action(boto_session,rule,entity,params):
    text_output = ""
    region = entity['region']
    region = region.replace("_","-")
    accountNumber = entity['accountNumber']

    topic_name = "CloudTrailMetricFilterAlerts" + region
    topic_arn = 'arn:aws:sns:' + region + ':' + accountNumber + ':' + topic_name
    log_group = entity['cloudWatchLogsLogGroupArn']

    #Validate the rule was set up properly
    if not re.match(r"[^@]+@[^@]+\.[^@]+", params[0]):
      text_output = "No email found as the first parameterUsage: AUTO: cloudwatch_create_metric_filter <email_address> <filter1> <filter2> .... "
      return text_output
    else:
      email_address = params[0]

    if log_group == None or log_group == "":
        text_output = "Cloudtrail is not set up to send to a CloudWatchLogs group. Please update and try again"
        return text_output

    else:
    # strip out just the group from the ARN
        try:
            pattern = re.compile('arn:aws:logs:\S+:\d+:log-group:(?P<group_name>.+):.+')
            log_group_regex = re.findall(pattern, log_group)
            log_group = log_group_regex[0]

        except IndexError as e:
            text_output = "The cloudWatchLogsLogGroupArn does not match the capture group. Can't parse / exiting"
            return text_output
    
    filters = {
      'UnauthorizedApiCalls': {
        'metric_value': '1',
        'filter_pattern': '{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }'
      },
      'NoMfaConsoleLogins': {
        'metric_value': '1',
        'filter_pattern': '{ $.userIdentity.sessionContext.attributes.mfaAuthenticated != "true" && $.userIdentity.invokedBy = "signin.amazonaws.com" }'
      },
      'RootAccountLogins': {
        'metric_value': '1',
        'filter_pattern': '{ $.userIdentity.type = "Root" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != "AwsServiceEvent" }'
      },
      'IamPolicyChanges': {
        'metric_value': '1',
        'filter_pattern': '{($.eventName=DeleteGroupPolicy)||($.eventName=DeleteRolePolicy)||($.eventName=DeleteUserPolicy)||($.eventName=PutGroupPolicy)||($.eventName=PutRolePolicy)||($.eventName=PutUserPolicy)||($.eventName=CreatePolicy)||($.eventName=DeletePolicy)||($.eventName=CreatePolicyVersion)||($.eventName=DeletePolicyVersion)||($.eventName=AttachRolePolicy)||($.eventName=DetachRolePolicy)||($.eventName=AttachUserPolicy)||($.eventName=DetachUserPolicy)||($.eventName=AttachGroupPolicy)||($.eventName=DetachGroupPolicy)}'
      },
      'CloudTrailConfigurationChanges': {
        'metric_value': '1',
        'filter_pattern': '{ ($.eventName = CreateTrail) ||($.eventName = UpdateTrail) || ($.eventName = DeleteTrail) || ($.eventName = StartLogging) || ($.eventName = StopLogging) }'
      },
      'FailedConsoleLogins': {
        'metric_value': '2',
        'filter_pattern': '{ ($.eventName = ConsoleLogin) && ($.errorMessage = "Failed authentication") }'
      },
      'DisabledOrDeletedCmks': {
        'metric_value': '2',
        'filter_pattern': '{($.eventSource = kms.amazonaws.com) && (($.eventName=DisableKey)||($.eventName=ScheduleKeyDeletion))}'
      },
      'S3BucketPolicyChanges': {
        'metric_value': '1',
        'filter_pattern': '{ ($.eventSource = s3.amazonaws.com) && (($.eventName = PutBucketAcl) || ($.eventName = PutBucketPolicy) || ($.eventName = PutBucketCors) || ($.eventName = PutBucketLifecycle) || ($.eventName = PutBucketReplication) || ($.eventName = DeleteBucketPolicy) || ($.eventName = DeleteBucketCors) || ($.eventName = DeleteBucketLifecycle) || ($.eventName = DeleteBucketReplication)) }'
      },
      'AwsConfigChanges': {
        'metric_value': '2',
        'filter_pattern': '{($.eventSource = config.amazonaws.com) && (($.eventName=StopConfigurationRecorder)||($.eventName=DeleteDeliveryChannel)||($.eventName=PutDeliveryChannel)||($.eventName=PutConfigurationRecorder))}'
      },
      'SecurityGroupChanges': {
        'metric_value': '2',
        'filter_pattern': '{ ($.eventName = AuthorizeSecurityGroupIngress) || ($.eventName = AuthorizeSecurityGroupEgress) || ($.eventName = RevokeSecurityGroupIngress) || ($.eventName = RevokeSecurityGroupEgress) || ($.eventName = CreateSecurityGroup) || ($.eventName = DeleteSecurityGroup)}'
      },
      'NetworkAccessControlListChanges': {
        'metric_value': '2',
        'filter_pattern': '{ ($.eventName = CreateNetworkAcl) || ($.eventName = CreateNetworkAclEntry) || ($.eventName = DeleteNetworkAcl) || ($.eventName = DeleteNetworkAclEntry) || ($.eventName = ReplaceNetworkAclEntry) || ($.eventName = ReplaceNetworkAclAssociation) }'
      },
      'NetworkGatewayChanges': {
        'metric_value': '1',
        'filter_pattern': '{ ($.eventName = CreateCustomerGateway) || ($.eventName = DeleteCustomerGateway) || ($.eventName = AttachInternetGateway) || ($.eventName = CreateInternetGateway) || ($.eventName = DeleteInternetGateway) || ($.eventName = DetachInternetGateway) }'
      },
      'RouteTableChanges': {
        'metric_value': '1',
        'filter_pattern': '{ ($.eventName = CreateRoute) || ($.eventName = CreateRouteTable) || ($.eventName = ReplaceRoute) || ($.eventName = ReplaceRouteTableAssociation) || ($.eventName = DeleteRouteTable) || ($.eventName = DeleteRoute) || ($.eventName = DisassociateRouteTable) }'
      },
      'VpcChanges': {
        'metric_value': '1',
        'filter_pattern': '{ ($.eventName = CreateVpc) || ($.eventName = DeleteVpc) || ($.eventName = ModifyVpcAttribute) || ($.eventName = AcceptVpcPeeringConnection) || ($.eventName = CreateVpcPeeringConnection) || ($.eventName = DeleteVpcPeeringConnection) || ($.eventName = RejectVpcPeeringConnection) || ($.eventName = AttachClassicLinkVpc) || ($.eventName = DetachClassicLinkVpc) || ($.eventName = DisableVpcClassicLink) || ($.eventName = EnableVpcClassicLink) }'
      }
    }


    # Loop through the params
    # For each filter, if matching, update variables and set filter
    for filter_name in params[1:]: 
        # Check to make sure we know the filter that we're trying to add
        try:
            metric_name = filter_name
            filter_pattern = filters[filter_name]['filter_pattern']
            metric_value = filters[filter_name]['metric_value']
        except KeyError as e:
            text_output = text_output + "Metric filter %s not found. Please check spelling and try again.Available filters are: UnauthorizedApiCalls, NoMfaConsoleLogins, RootAccountLogins, IamPolicyChanges, CloudTrailConfigurationChanges, FailedConsoleLogins, DisabledOrDeletedCmks, S3BucketPolicyChanges, AwsConfigChanges, SecurityGroupChanges, NetworkAccessControlListChanges, NetworkGatewayChanges, RouteTableChanges, VpcChanges " % filter_name
            continue

        #Do work
        try:
          text_output = text_output + create_filter(boto_session,log_group,filter_name,filter_pattern,metric_name,metric_value)
          text_output = text_output + create_topic(boto_session,topic_name)
          text_output = text_output + create_alarm(boto_session,filter_name,topic_arn)
        except ClientError as e:
          text_output = text_output + "Unexpected error: %s " % e  

    #We only want to run this once so we'll do it at the end
    try:
      text_output = text_output + create_subscription(boto_session,topic_arn,email_address)
    except ClientError as e:
      text_output = text_output + "Unexpected error: %s " % e  

    return text_output 

