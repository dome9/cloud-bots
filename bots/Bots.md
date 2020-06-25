# Bots
  - [ami\_set\_to\_private](#ami_set_to_private)
  - [cloudtrail\_enable](#cloudtrail_enable)
  - [cloudtrail\_enable\_log\_file\_validation](#cloudtrail_enable_log_file_validation)
  - [cloudtrail\_send\_to\_cloudwatch](#cloudtrail_send_to_cloudwatch)
  - [cloudwatch\_create\_metric\_filter](#cloudwatch_create_metric_filter)
  - [config\_enable](#config_enable)
  - [ec2\_attach\_instance\_role](#ec2_attach_instance_role)
  - [ec2\_create\_snapshot](#ec2_create_snapshot)
  - [ec2\_release\_eips](#ec2_release_eips)
  - [ec2\_quarantine\_instance](#ec2_quarantine_instance)
  - [ec2\_stop\_instance](#ec2_stop_instance)
  - [ec2\_terminate\_instance](#ec2_terminate_instance)
  - [ec2\_update\_instance\_role](#ec2_update_instance_role)
  - [iam\_role\_attach\_policy](#iam_role_attach_policy)
  - [iam\_user\_attach\_policy](#iam_user_attach_policy)
  - [iam\_quarantine\_role](#iam_quarantine_role)
  - [iam\_quarantine\_user](#iam_quarantine_user)
  - [iam\_turn\_on\_password\_policy](#iam_turn_on_password_policy)
  - [iam\_user\_force\_password\_change](#iam_user_force_password_change)
  - [igw\_delete](#igw_delete)
  - [kms\_enable\_rotation](#kms_enable_rotation)
  - [lambda\_detach\_blanket\_permissions](#lambda_detach_blanket_permissions)
  - [mark\_for\_stop\_ec2\_resource](#mark_for_stop_ec2_resource)
  - [rds\_quarantine\_instance](#rds_quarantine_instance)
  - [s3\_delete\_acls](#s3_delete_acls)
  - [s3\_delete\_permissions](#s3_delete_permissions)
  - [s3\_enable\_encryption](#s3_enable_encryption)
  - [s3\_enable\_logging](#s3_enable_logging)
  - [s3\_enable\_versioning](#s3_enable_versioning)
  - [s3\_only\_allow\_ssl](#s3_only_allow_ssl)
  - [sg\_delete](#sg_delete)
  - [sg\_rules\_delete](#sg_rules_delete)
  - [sg\_single\_rule\_delete](#sg_single_rule_delete)
  - [tag\_ec2\_resource](#tag_ec2_resource)
  - [vpc\_turn\_on\_flow\_logs](#vpc_turn_on_flow_logs)
  - [s3\_block\_all\_public\_access](#s3_block_all_public_access)
  
###[Optional Bots](#optional-bots)
- [ec2\_tag\_instance\_from\_vpc](#ec2_tag_instance_from_vpc)
- [s3\_delete\_bucket](#s3_delete_bucket)


## ami\_set\_to\_private

What it does: Sets an AMI to be private instead of public  
Usage: AUTO: ami\_set\_to\_private  
Sample GSL: AMI should have isPublic=false  
Limitations: none


## cloudtrail\_enable

What it does: Creates a new S3 bucket and turns on a multi-region trail
that logs to it.  
Pre-set Settings:  
Default bucket name: acct\<account\_id\>cloudtraillogs  
IsMultiRegionTrail: True (CIS for AWS V 1.1.0 Section 2.1)  
IncludeGlobalServiceEvents: True  
EnableLogFileValidation: True (CIS for AWS V 1.1.0 Section 2.2)

Usage: AUTO: cloudtrail\_enable trail\_name=\<trail\_name\>
bucket\_name=\<bucket\_name\>  
Note: Trail\_name and bucket\_name are optional and don't need to be
set.  
Limitations: none

## cloudtrail\_enable\_log\_file\_validation
What it does: Enable log file validation in cloudTrail
Usage: AUTO: cloudtrail_enable_log_file_validation
Limitations: None


## cloudtrail\_send\_to\_cloudwatch

What it does: Makes CloudTrail output logs to CloudWatchLogs. If the log
group doesn't exist alredy, it'll reate a new one. Usage: AUTO:
cloudtrail\_send\_to\_cloudwatch \<log\_group\_name\>  
Limitations: none  
Defaults: If no log group name is set, it'll default to
CloudTrail/DefaultLogGroup  
Role name: CloudTrail\_CloudWatchLogs\_Role  
Log delivery policy name: CloudWatchLogsAllowDelivery

## cloudwatch\_create\_metric\_filter

What it does: Creates CloudWatch Metric Filters to match the CIS
Benchmark. A metric alarm and SNS subscripion is created as well  
Usage: AUTO: cloudwatch\_create\_metric\_filter \<email\_address\>
<filter1> <filter2> ....  
Limitations: Cloudtrail needs to be set up to send the logs to a
CloudWatchLogs group first.  
Default: SNS topic name is CloudTrailMetricFilterAlerts  
Available filters are: UnauthorizedApiCalls, NoMfaConsoleLogins,
RootAccountLogins, IamPolicyChanges, CloudTrailConfigurationChanges,
FailedConsoleLogins, DisabledOrDeletedCmks, S3BucketPolicyChanges,
AwsConfigChanges, SecurityGroupChanges, NetworkAccessControlListChanges,
NetworkGatewayChanges, RouteTableChanges, VpcChanges

## config\_enable

What it does: Enables AWS Config. This DOES NOT create config rules. It
only turns on the configuration recorders. Usage: AUTO: config\_enable
bucket\_name=mybucketlogs bucket\_region=us-west-1
include\_global\_resource\_types\_region=us-west-1 Limitations: none  
Variables (and their defaults): bucket\_name = accountNumber +
"awsconfiglogs" bucket\_region = us-west-1 allSupported = True
includeGlobalResourceTypes = True (if you want to change this, use the
variable include\_global\_resource\_types\_region=\<desired\_region\>)

Defaults (not changable currently via variable): file
deliveryFrequency(to S3) is set to One\_Hour config\_name = default

## ec2\_attach\_instance\_role

What it does: Attaches an instance role to an EC2 instance. This role
needs be passed in through the params.  
Usage: AUTO: ec2\_attach\_instance\_role role\_arn=\<role\_arn\>

If you have a role that is the same across accounts, and don't want to
pass in an account specific ARN, add "$ACCOUNT\_ID" to the role ARN and
the function will automatically pull in the current account ID of the
finding.  
Example: AUTO: ec2\_attach\_instance\_role
role\_arn=arn:aws:iam::$ACCOUNT\_ID:instance-profile/ec2SSM  
Sample GSL: Instance should have roles

## ec2\_create\_snapshot

What it does: Snapshots the EBS volumes on an instance  
Usage: AUTO: ec2\_create\_snapshot  
Notes: The snapshot description will show that it was created by
CloudBots and the rule that failed that triggered the bot. Also, the
snapshot will be tagged with a key of "source\_instance\_id" and a value
with the instance id from the source instance.  
Limitations: This will not work on Instance Store volumes. Only EBS

## ec2\_release\_eips

What it does: Disassociates and releases all EIPs on an instance  
Usage: AUTO: ec2\_release\_eips  
Limitations: none

## ec2\_quarantine\_instance

What it does: Attaches the instance a SG with no rules so it can't
communicate with the outside world  
Usage: AUTO: ec2\_quarantine\_instance  
Limitations: None

## ec2\_stop\_instance

What it does: Stops an ec2 instance  
Usage: AUTO: ec2\_stop\_instance  
Limitations: none

## ec2\_terminate\_instance

What it does: Terminates an ec2 instance  
Usage: AUTO: ec2\_terminate\_instance  
Limitations: none

## ec2\_update\_instance\_role

What it does: Updates an EXISTING EC2 instance role by attaching another
policy to the role. This policy needs be passed in through the params.  
Usage: AUTO: ec2\_update\_instance\_role policy\_arn=\<policy\_arn\>  
Example: AUTO: ec2\_update\_instance\_role
policy\_arn=arn:aws:iam::aws:policy/AlexaForBusinessDeviceSetup  
Sample GSL: Instance where roles should have roles with \[
managedPolicies contain \[ name='AmazonEC2RoleforSSM' \] \]

## iam\_role\_attach\_policy

What it does: Attaches a policy (passed in as a variable) to the role  
Usage: AUTO: iam\_role\_attach\_policy policy\_arn=\<policy\_arn\>  
Limitations: none  
Examples:  
AUTO: iam\_role\_attach\_policy
policy\_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccess  
AUTO: iam\_role\_attach\_policy
policy\_arn=arn:aws:iam::621958466464:policy/sumo\_collection  
AUTO: iam\_role\_attach\_policy
policy\_arn=arn:aws:iam::$ACCOUNT\_ID:policy/sumo\_collection

## iam\_user\_attach\_policy

What it does: Attaches a policy (passed in as a variable) to the user  
Usage: AUTO: iam\_user\_attach\_policy policy\_arn=\<policy\_arn\>  
Limitations: none  
Examples:  
AUTO: iam\_user\_attach\_policy
policy\_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccess  
AUTO: iam\_user\_attach\_policy
policy\_arn=arn:aws:iam::621958466464:policy/sumo\_collection  
AUTO: iam\_user\_attach\_policy
policy\_arn=arn:aws:iam::$ACCOUNT\_ID:policy/sumo\_collection

## iam\_quarantine\_role

What it does: Adds an explicit deny all policy to IAM and directly
attaches it to a role  
Usage: AUTO: iam\_quarantine\_role  
Limitations: none

## iam\_quarantine\_user

What it does: Adds an explicit deny all policy to IAM and directly
attaches it to a user  
Usage: AUTO: iam\_quarantine\_user  
Limitations: none

## iam\_turn\_on\_password\_policy

What it does: Sets all settings in an account password policy  
Usage: AUTO: iam\_turn\_on\_password\_policy MinimumPasswordLength:<int>
RequireSymbols:\<True/False\> RequireNumbers:\<True/False\>
RequireUppercaseCharacters:\<True/False\>
RequireLowercaseCharacters:\<True/False\>
AllowUsersToChangePassword:\<True/False\> MaxPasswordAge:<int>
PasswordReusePrevention:<int> HardExpiry:\<True/False\>  
Limitations: ALL variables need to be set at the same time

Sample tag: AUTO: iam\_turn\_on\_password\_policy
MinimumPasswordLength:15 RequireSymbols:True RequireNumbers:True
RequireUppercaseCharacters:True RequireLowercaseCharacters:True
AllowUsersToChangePassword:True MaxPasswordAge:5
PasswordReusePrevention:5 HardExpiry:True

## iam\_user\_force\_password\_change

What it does: Updates the setting for an IAM user so that they need to
change their console password the next time they log in.  
Usage: AUTO: iam\_user\_force\_password\_change  
Limitations: none

## igw\_delete

What it does: Turns off ec2 instances with public IPs, detaches an IGW
from a VPC, and then deletes it.  
Limitations: VPCs have lots of interconnected services. This is
currently just focused on EC2 but future enhancements will need to be
made to turn off RDS, Redshift, etc.

## kms\_enable\_rotation

What it does: Enables rotation on a KMS key  
Usage: AUTO: kms\_enable\_rotation  
Sample GSL: KMS where isCustomerManaged=true and deletionDate\!=0 should
have rotationStatus=true Limitations: Edits can not be made to AWS maged
keys. Only customer managed keys can be edited.

## lambda\_detach\_blanket\_permissions
What it does: For lambda that failed, it check all the policies that grant blanket permissions ('*') to resources and
              detach it from the lambda role
Usage: AUTO: lambda_detach_blanket_permissions
Note: The bot will detach the policies that have admin privileges from the lambda role so you will need to configure the specific
      policies to grant positive permissions to specific AWS services or actions
Limitations:None

## mark\_for\_stop\_ec2\_resource

What it does: Tags an ec2 resource with "marked\_for\_stop" and
<current epoch time>  
Usage: AUTO: mark\_for\_stop\_ec2\_resource <time>\<unit(m,h,d)\>  
Example: AUTO: mark\_for\_stop\_ec2\_resource 3h  
Note: This is meant to be used in conjunction with a more aggressive
action like stopping or termanating an instance. The first step will be
to tag an instance with the time that we want to trigger the remediation
bot.  
From there, a rule like "Instance should not have tags with \[
key='marked\_for\_stop' and value before(1, 'minutes') \]" can be ran to
check how long an instance has had the 'mark for stop' tag. Limitations:
none

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

## rds\_quarantine\_instance

What it does: Attaches the RDS instance a SG with no rules so it can't
communicate with the outside world  
Usage: AUTO: rds\_quarantine\_instance  
Limitations: Instance needs to be "Available" in order to update. If
it's in "backing up" state, this will fail  
(Might not work with Aurora since it's in a cluster)

## s3\_delete\_acls

What it does: Deletes all ACLs from a bucket. If there is a bucket
policy, it'll be left alone.  
Usage: AUTO: s3\_delete\_acls  
Limitations: none

## s3\_delete\_permissions

What it does: Deletes all ACLs and bucket policies from a bucket  
Usage: AUTO: s3\_delete\_permissions  
Limitations: none

## s3\_enable\_encryption

What it does: Turns on AES-256 encryption on the target bucket  
Usage: AUTO: s3\_enable\_encryption  
Limitations: none

## s3\_enable\_logging

What it does: Turns on server access logging. The target bucket needs to
be in the same region as the remediation bucket or it'll throw a
CrossLocationLoggingProhibitted error. This bot will create a bucket to
log to as well. Usage: AUTO: s3\_enable\_logging  
Limitations: none

## s3\_enable\_versioning

What it does: Turns on versioning for an S3 bucket  
Usage: AUTO: s3\_enable\_versioning  
Limitations: none


## s3\_only\_allow\_ssl
What it does: Ensure that S3 Buckets enforce encryption of data transfers using Secure Sockets Layer (SSL)
Usage: AUTO: s3_only_allow_ssl
Note: The bot looks at the bucket policy and adds to the current policy the missing actions(s3:GetObject and s3:PutObject)
      and the SSL statement.
      if no policy in the bucket, an SSL policy will add to the bucket
Limitations: none

## sg\_delete

What it does: Deletes a security group  
Usage: AUTO: sg\_delete  
Limitations: This will fail if there is something still attached to the
SG.

## sg\_rules\_delete

What it does: Deletes all ingress and egress rules from a SG  
Usage: AUTO: sg\_rules\_delete  
Limitations: none

## sg\_single\_rule\_delete

What it does: Deletes a single rule on a security group Usage: AUTO:
sg\_single\_rule\_delete split=\<true|false\> protocol=\<TCP|UDP\>
scope=\<a.b.c.d/e\> direction=\<inbound|outbound\> port=<number>

Example: AUTO: sg\_single\_rule\_delete split=false protocol=TCP
scope=0.0.0.0/0 direction=inbound port=22 Sample GSL: SecurityGroup
should not have inboundRules with \[scope = '0.0.0.0/0' and port\<=22
and portTo\>=22\]

Conditions and caveats: Deleting a single rule on a security group can
be difficult because the problematic port can be nested within a wider
range of ports. If SSH is open because a SG has all of TCP open, do you
want to delete the whole rule or would you break up the SG into the same
scope but port 0-21 and a second rule for 23-end of TCP port range?
Currently the way this is being addressed is using the 'split'
parameter. If it's set as false, CloudBots will only look for the
specific port in question. If it's nested within a larger port scope,
it'll be skipped. If you set split to true, then the whole rule that the
problematic port is nested in will be removed and 2 split rules will be
added in its place (ex: if port 1-30 is open and you want to remove SSH,
the new rules will be for port 1-21 and port 23-30).

If you want to delete a rule that is open on ALL ports:
Put Port 0 as the port to be deleted and the bot will remove the rule.
If you want to delete a rule that is open to ALL :
Put protocol=ALL and the bot will remove the open rule that configured with ALL as protocol
If you want to delete a rule that is open no matter to the configured protocol 
Put protocol=* and the bot will remove the open rule  
Set Split to True
AUTO: sg_single_rule_delete split=true protocol=TCP scope=8.8.8.8/32 direction=inbound port=0   

Limitations: IPv6 is not supported

## tag\_ec2\_resource

What it does: Tags an ec2 instance  
Usage: AUTO: tag\_ec2\_resource "key" "value"  
Note: Tags with spaces can be added if they are surrounded by quotes:
ex: tag\_ec2\_resource "this is my key" "this is a value"  
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

## vpc\_turn\_on\_flow\_logs

What it does: Turns on flow logs for a VPC Settings: Log Group Name:
vpcFlowLogs If traffic type to be logged isn't specified, it defaults to
all. Usage: AUTO: vpc\_turn\_on\_flow\_logs
traffic\_type=\<all|accept|reject\> destination=\<logs|s3\>
s3\_arn=arn:aws:s3:::my-bucket/my-logs/ Example: AUTO:
vpc\_turn\_on\_flow\_logs traffic\_type=all destination=logs Example:
AUTO: vpc\_turn\_on\_flow\_logs traffic\_type=all destination=s3
s3\_arn=arn:aws:s3:::my-bucket/my-logs/

Limitations: none Sample GSL: VPC should have hasFlowLogs=true

To specify a subfolder in the bucket, use the following ARN format:
bucket\_ARN/subfolder\_name/ . For example, to specify a subfolder named
my-logs in a bucket named my-bucket , use the following ARN:
arn:aws:s3:::my-bucket/my-logs/

log delivery policy name is set as: vpcFlowLogDelivery log delivery role
is set as: vpcFlowLogDelivery

## s3\_block\_all\_public\_access
What it does: turn on S3 Bucket Block public access : Block public access to buckets and objects granted
through Future New AND Existing public ACLs and Bucket Policies.

Usage:  s3_block_public_all_access

Limitations: none

Notes:
    -  before running this bot, ensure that your applications will work correctly without public access

# Optional Bots

These bots are not packaged with the core Lambda function because
they're extremely impactful or edge-case bots that won't be normally
used.  
If you want to use these bots, they will need to be manually added to
the function. All of the code is in the optional\_bots directory.

## ec2\_tag\_instance\_from\_vpc

### This bot was created for a customer and most likely won't be used outside of that edge case

What it does: If an instance is missing a specific tag, try to pull it
from the VPC. Usage: AUTO: ec2\_tag\_instance\_from\_vpc <Key>  
Limitations: none

## s3\_delete\_bucket

What it does: Deletes an S3 bucket  
Usage: AUTO: s3\_delete\_bucket  
Limitations: none
