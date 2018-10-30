# Bots

## ami_set_to_private
What it does: Sets an AMI to be private instead of public  
Usage: AUTO: ami_set_to_private  
Sample GSL: AMI should have isPublic=false  
Limitations: none  

## cloudtrail_enable
What it does: Creates a new S3 bucket and turns on a multi-region trail that logs to it.  
Pre-set Settings:  
Default bucket name: acct<account_id>cloudtraillogs  
IsMultiRegionTrail: True (CIS for AWS V 1.1.0 Section 2.1)  
IncludeGlobalServiceEvents: True  
EnableLogFileValidation: True (CIS for AWS V 1.1.0 Section 2.2)   

Usage: AUTO: cloudtrail_enable trail_name=<trail_name> bucket_name=<bucket_name>  
Note: Trail_name and bucket_name are optional and don't need to be set.   
Limitations: none   

## cloudtrail_send_to_cloudwatch
What it does: Makes CloudTrail output logs to CloudWatchLogs. If the log group doesn't exist alredy, it'll reate a new one. 
Usage: AUTO: cloudtrail_send_to_cloudwatch <log_group_name>    
Limitations: none    
Defaults: 
    If no log group name is set, it'll default to CloudTrail/DefaultLogGroup  
    Role name: CloudTrail_CloudWatchLogs_Role  
    Log delivery policy name: CloudWatchLogsAllowDelivery  
 
## cloudwatch_create_metric_filter
What it does: Creates CloudWatch Metric Filters to match the CIS Benchmark. A metric alarm and SNS subscripion is created as well  
Usage: AUTO: cloudwatch_create_metric_filter <email_address> <filter1> <filter2> ....   
Limitations: Cloudtrail needs to be set up to send the logs to a CloudWatchLogs group first.     
Default: SNS topic name is CloudTrailMetricFilterAlerts  
Available filters are: UnauthorizedApiCalls, NoMfaConsoleLogins, RootAccountLogins, IamPolicyChanges, CloudTrailConfigurationChanges, FailedConsoleLogins, DisabledOrDeletedCmks, S3BucketPolicyChanges, AwsConfigChanges, SecurityGroupChanges, NetworkAccessControlListChanges, NetworkGatewayChanges, RouteTableChanges, VpcChanges  

## config_enable
What it does: Enables AWS Config. This DOES NOT create config rules. It only turns on the configuration recorders. 
Usage: AUTO: config_enable bucket_name=mybucketlogs bucket_region=us-west-1 include_global_resource_types_region=us-west-1
Limitations: none  
Variables (and their defaults): 
    bucket_name = accountNumber + "awsconfiglogs"
    bucket_region = us-west-1
    allSupported = True
    includeGlobalResourceTypes = True (if you want to change this, use the variable include_global_resource_types_region=<desired_region>)  

Defaults (not changable currently via variable):
    file deliveryFrequency(to S3) is set to One_Hour
    config_name = default  

## ec2_attach_instance_role
What it does: Attaches an instance role to an EC2 instance. This role needs be passed in through the params.    
Usage: AUTO: ec2_attach_instance_role role_arn=<role_arn>  

If you have a role that is the same across accounts, and don't want to pass in an account specific ARN, add "$ACCOUNT_ID" to the role ARN and the function will automatically pull in the current account ID of the finding.   
Example: AUTO: ec2_attach_instance_role role_arn=arn:aws:iam::$ACCOUNT_ID:instance-profile/ec2SSM  
Sample GSL: Instance should have roles

## ec2_create_snapshot  
What it does: Snapshots the EBS volumes on an instance  
Usage: AUTO: ec2_create_snapshot  
Notes: The snapshot description will show that it was created by CloudBots and the rule that failed that triggered the bot. Also, the snapshot will be tagged with a key of "source_instance_id" and a value with the instance id from the source instance.   
Limitations: This will not work on Instance Store volumes. Only EBS  

## ec2_release_eips  
What it does: Disassociates and releases all EIPs on an instance  
Usage: AUTO: ec2_release_eips  
Limitations: none  

## ec2_quarantine_instance
What it does: Attaches the instance a SG with no rules so it can't communicate with the outside world  
Usage: AUTO: ec2_quarantine_instance  
Limitations: None  

## ec2_stop_instance
What it does: Stops an ec2 instance    
Usage: AUTO: ec2_stop_instance   
Limitations: none  

## ec2_terminate_instance
What it does: Terminates an ec2 instance  
Usage: AUTO: ec2_terminate_instance  
Limitations: none  

## ec2_update_instance_role  
What it does: Updates an EXISTING EC2 instance role by attaching another policy to the role. This policy needs be passed in through the params.  
Usage: AUTO: ec2_update_instance_role policy_arn=<policy_arn>  
Example: AUTO: ec2_update_instance_role policy_arn=arn:aws:iam::aws:policy/AlexaForBusinessDeviceSetup  
Sample GSL: Instance where roles should have roles with [ managedPolicies contain [ name='AmazonEC2RoleforSSM' ] ]  

## iam_quarantine_role
What it does: Adds an explicit deny all policy to IAM and directly attaches it to a role  
Usage: AUTO: iam_quarantine_role  
Limitations: none  

## iam_quarantine_user
What it does: Adds an explicit deny all policy to IAM and directly attaches it to a user  
Usage: AUTO: iam_quarantine_user  
Limitations: none  

## iam_turn_on_password_policy
What it does: Sets all settings in an account password policy  
Usage: AUTO: iam_turn_on_password_policy MinimumPasswordLength:<int> RequireSymbols:<True/False> RequireNumbers:<True/False>  RequireUppercaseCharacters:<True/False>  RequireLowercaseCharacters:<True/False>  AllowUsersToChangePassword:<True/False>  MaxPasswordAge:<int> PasswordReusePrevention:<int> HardExpiry:<True/False>   
Limitations: ALL variables need to be set at the same time  

Sample tag: AUTO: iam_turn_on_password_policy MinimumPasswordLength:15 RequireSymbols:True RequireNumbers:True RequireUppercaseCharacters:True RequireLowercaseCharacters:True AllowUsersToChangePassword:True MaxPasswordAge:5 PasswordReusePrevention:5 HardExpiry:True  

## iam_user_force_password_change
What it does: Updates the setting for an IAM user so that they need to change their console password the next time they log in.  
Usage: AUTO: iam_user_force_password_change  
Limitations: none  

## igw_delete
What it does: Turns off ec2 instances with public IPs, detaches an IGW from a VPC, and then deletes it.  
Limitations: VPCs have lots of interconnected services. This is currently just focused on EC2 but future enhancements will need to be made to turn off RDS, Redshift, etc.  

## kms_enable_rotation
What it does: Enables rotation on a KMS key  
Usage: AUTO: kms_enable_rotation  
Sample GSL: KMS where isCustomerManaged=true should have rotationStatus=true  
Limitations: Edits can not be made to AWS maged keys. Only customer managed keys can be edited.  
 
## mark_for_stop_ec2_resource
What it does: Tags an ec2 resource with "marked_for_stop" and <current epoch time>     
Usage: AUTO: mark_for_stop_ec2_resource <time><unit(m,h,d)>  
Example: AUTO: mark_for_stop_ec2_resource 3h  
Note: This is meant to be used in conjunction with a more aggressive action like stopping or termanating an instance. The first step will be to tag an instance with the time that we want to tigger the remediation bot.  
From there, a rule like "Instance should not have tags with [ key='marked_for_stop' and value before(1, 'minutes') ]" can be ran to check how long an instance has had the 'mark for stop' tag. 
Limitations: none  

THIS WORKS ACROSS ALL EC2 RELATED SERVICES:  
- Image  
- Instance  
- InternetGateway  
- NetworkAcl  
- NetworkInterface  
- PlacementGroup  
- RouteTable  
- SecurityGroup  
- Snapshot  
- Subnet  
- Volume  
- Vpc  
- VpcPeeringConnection  


## rds_quarantine_instance
What it does: Attaches the RDS instance a SG with no rules so it can't communicate with the outside world  
Usage: AUTO: rds_quarantine_instance  
Limitations: Instance needs to be "Available" in order to update. If it's in "backing up" state, this will fail  
(Might not work with Aurora since it's in a cluster)  

## s3_delete_acls
What it does: Deletes all ACLs from a bucket. If there is a bucket policy, it'll be left alone.  
Usage: AUTO: s3_delete_acls  
Limitations: none  

## s3_delete_permissions
What it does: Deletes all ACLs and bucket policies from a bucket  
Usage: AUTO: s3_delete_permissions  
Limitations: none  

## s3_enable_encryption
What it does: Turns on AES-256 encryption on the target bucket  
Usage: AUTO: s3_enable_encryption  
Limitations: none  

## s3_enable_logging
What it does: Turns on server access logging. The target bucket needs to be in the same region as the remediation bucket or it'll throw a CrossLocationLoggingProhibitted error. This bot will create a bucket to log to as well.
Usage: AUTO: s3_enable_logging  
Limitations: none  

## s3_enable_versioning
What it does: Turns on versioning for an S3 bucket  
Usage: AUTO: s3_enable_versioning  
Limitations: none  

## sg_delete
What it does: Deletes a security group  
Usage: AUTO: sg_delete  
Limitations: This will fail if there is something still attached to the SG.  

## sg_rules_delete
What it does: Deletes all ingress and egress rules from a SG  
Usage: AUTO: sg_rules_delete  
Limitations: none  

## sg_single_rule_delete
What it does: Deletes a single rule on a security group
Usage: AUTO: sg_single_rule_delete split=<true|false> protocol=<TCP|UDP> scope=<a.b.c.d/e> direction=<inbound|outbound> port=<number>

Example: AUTO: sg_single_rule_delete split=false protocol=TCP scope=0.0.0.0/0 direction=inbound port=22
Sample GSL: SecurityGroup should not have inboundRules with [scope = '0.0.0.0/0' and port<=22 and portTo>=22]

Conditions and caveats: Deleting a single rule on a security group can be difficult because the problematic port can be nested within a wider range of ports. If SSH is open because a SG has all of TCP open, do you want to delete the whole rule or would you break up the SG into the same scope but port 0-21 and a second rule for 23-end of TCP port range?
Currently the way this is being addressed is using the 'split' parameter. If it's set as false, CloudBots will only look for the specific port in question. If it's nested within a larger port scope, it'll be skipped. 
If you set split to true, then the whole rule that the problematic port is nested in will be removed and 2 split rules will be added in its place (ex: if port 1-30 is open and you want to remove SSH, the new rules will be for port 1-21 and port 23-30). 

If you want to delete a rule that is open on ALL ports:  
Put Port 0 as the port to be deleted and the bot will remove the rule.  
Set Split to True  
AUTO: sg_single_rule_delete split=true protocol=TCP scope=8.8.8.8/32 direction=inbound port=0  

## tag_ec2_resource
What it does: Tags an ec2 instance  
Usage: AUTO: tag_ec2_resource "key" "value"  
Note: Tags with spaces can be added if they are surrounded by quotes: ex: tag_ec2_resource "this is my key" "this is a value"  
Limitations: none  

THIS WORKS ACROSS ALL EC2 RELATED SERVICES:
* Image
* Instance
* InternetGateway
* NetworkAcl
* NetworkInterface
* PlacementGroup
* RouteTable
* SecurityGroup
* Snapshot
* Subnet
* Volume
* Vpc
* VpcPeeringConnection

## vpc_turn_on_flow_logs
What it does: Turns on flow logs for a VPC
Settings: 
Log Group Name: vpcFlowLogs
If traffic type to be logged isn't specified, it defaults to all.
Usage: AUTO: vpc_turn_on_flow_logs traffic_type=<all|accept|reject> destination=<logs|s3> s3_arn=arn:aws:s3:::my-bucket/my-logs/
Example: AUTO: vpc_turn_on_flow_logs traffic_type=all destination=logs
Example: AUTO: vpc_turn_on_flow_logs traffic_type=all destination=s3 s3_arn=arn:aws:s3:::my-bucket/my-logs/

Limitations: none 
Sample GSL: VPC should have hasFlowLogs=true

To specify a subfolder in the bucket, use the following ARN format: bucket_ARN/subfolder_name/ . 
For example, to specify a subfolder named my-logs in a bucket named my-bucket , use the following ARN: arn:aws:s3:::my-bucket/my-logs/

log delivery policy name is set as: vpcFlowLogDelivery
log delivery role is set as: vpcFlowLogDelivery


# Optional Bots

These bots are not packaged with the core Lambda function because they're extremely impactful or edge-case bots that won't be normally used.  
If you want to use these bots, they will need to be manually added to the function. All of the code is in the optional_bots directory.  


## ec2_tag_instance_from_vpc
### This bot was created for a customer and most likely won't be used outside of that edge case
What it does: If an instance is missing a specific tag, try to pull it from the VPC. 
Usage: AUTO: ec2_tag_instance_from_vpc <Key>  
Limitations: none  

## s3_delete_bucket
What it does: Deletes an S3 bucket  
Usage: AUTO: s3_delete_bucket  
Limitations: none  

