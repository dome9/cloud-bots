'''
## cloudwatch_create_metric_filter
What it does: Creates CloudWatch Metric Filters to match the CIS Benchmark
Usage: cloudwatch_create_metric_filter <filter1> <filter2> .... 
Limitations: Cloudtrail needs to be set up to send the logs to a CloudWatchLogs group first.   
'''

import boto3
import json
import re
from botocore.exceptions import ClientError

def run_action(boto_session,rule,entity,params):
    text_output = ""

    log_group = entity['cloudWatchLogsLogGroupArn']

    if log_group == None or log_group == "":
        text_output = "Cloudtrail is not set up to send to a CloudWatchLogs group. Please update and try again\n"
        return text_output

    else:
    # strip out just the group from the ARN
        try:
            pattern = re.compile('arn:aws:logs:\S+:\d+:log-group:(?P<group_name>.+):.+')
            log_group_regex = re.findall(pattern, log_group)
            log_group = log_group_regex[0]

        except IndexError as e:
            text_output = "The cloudWatchLogsLogGroupArn does not match the capture group. Can't parse / exiting\n"
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

    cloudwatchlogs_client = boto_session.client('logs')

    # Loop through the params
    # For each filter, if matching, update variables and set filter
    for filter_name in params:
        
        # Check to make sure we know the filter that we're trying to add
        try:
            metric_name = filter_name
            filter_pattern = filters[filter_name]['filter_pattern']
            metric_value = filters[filter_name]['metric_value']
        except KeyError as e:
            text_output = text_output + "Metric filter %s not found. Please check spelling and try again.\nAvailable filters are: UnauthorizedApiCalls, NoMfaConsoleLogins, RootAccountLogins, IamPolicyChanges, CloudTrailConfigurationChanges, FailedConsoleLogins, DisabledOrDeletedCmks, S3BucketPolicyChanges, AwsConfigChanges, SecurityGroupChanges, NetworkAccessControlListChanges, NetworkGatewayChanges, RouteTableChanges, VpcChanges \n" % filter_name
            continue

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
                text_output = text_output + "Unexpected error: %s \n" % str(result)
            else:
                text_output = text_output + "Metric filter created for filter: %s \n" % filter_name

        except ClientError as e:
            text_output = text_output + "Unexpected error: %s \n" % e

    return text_output 