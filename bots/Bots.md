# Bots
  - [acl\_delete](#acl_delete)
  - [acl\_revert\_modification](#acl_revert_modification)
  - [acm\_delete\_certificate](#acm_delete_certificate)
  - [ami\_set\_to\_private](#ami_set_to_private)
  - [cloudtrail\_enable](#cloudtrail_enable)
  - [cloudtrail\_enable\_log\_file\_validation](#cloudtrail_enable_log_file_validation)
  - [cloudtrail\_encrypt\_log\_files\_using\_existing\_key](#cloudtrail_encrypt_log_files_using_existing_key)
  - [cloudtrail\_encrypt\_log\_files\_using\_new\_key\_creation](#cloudtrail_encrypt_log_files_using_new_key_creation)
  - [cloudtrail\_send\_to\_cloudwatch](#cloudtrail_send_to_cloudwatch)
  - [cloudwatch\_create\_metric\_filter](#cloudwatch_create_metric_filter)
  - [config\_enable](#config_enable)
  - [ec2\_attach\_instance\_role](#ec2_attach_instance_role)
  - [ec2\_create\_snapshot](#ec2_create_snapshot)
  - [ec2\_detach\_instance\_role](#ec2_detach_instance_role)
  - [ec2\_release\_eips](#ec2_release_eips)
  - [ec2\_quarantine\_instance](#ec2_quarantine_instance)
  - [ec2\_stop\_instance](#ec2_stop_instance)
  - [ec2\_terminate\_instance](#ec2_terminate_instance)
  - [ec2\_update\_instance\_role](#ec2_update_instance_role)
  - [ecs\_reboot](#ecs_reboot)
  - [ecs\_service\_role\_detach\_inline\_policy](#ecs_service_role_detach_inline_policy)  
  - [ecs\_stop](#ecs_stop)
  - [ecs\_delete\_repository\_image](#ecs_delete_repository_image)
  - [iam\_detach\_policy](#iam_detach_policy)
  - [iam\_generate\_credential\_report](#iam_generate_credential_report)  
  - [iam\_delete\_access\_key](#iam_delete_access_key)
  - [iam\_delete\_default\_policy\_version](#iam_delete_default_policy_version)
  - [iam\_group\_delete\_inline\_policy](#iam_group_delete_inline_policy)
  - [iam\_role\_attach\_policy](#iam_role_attach_policy)
  - [iam\_role\_clone\_with\_non\_enumerable\_name](#iam_role_clone_with_non_enumerable_name)
  - [iam\_revoke\_access\_key](#iam_revoke_access_key)
  - [iam\_user\_attach\_policy](#iam_user_attach_policy)
  - [iam\_user\_detach](#iam_user_detach)
  - [iam\_quarantine\_role](#iam_quarantine_role)
  - [iam\_quarantine\_user](#iam_quarantine_user)
  - [iam\_turn\_on\_password\_policy](#iam_turn_on_password_policy)
  - [iam\_user\_deactivate\_unused\_access\_key](#iam_user_deactivate_unused_access_key)
  - [iam\_user\_delete\_inline\_policies](#iam_user_delete_inline_policies)
  - [iam\_user\_force\_password\_change](#iam_user_force_password_change)
  - [igw\_delete](#igw_delete)
  - [kms\_cmk\_enable\_key](#kms_cmk_enable_key)  
  - [kms\_enable\_rotation](#kms_enable_rotation)
  - [lambda\_detach\_blanket\_permissions](#lambda_detach_blanket_permissions)
  - [lambda\_disable](#lambda_disable)
  - [lambda\_enable\_active\_tracing](#lambda_enable_active_tracing)
  - [lambda\_tag](#lambda_tag)
  - [load\_balancer\_enable\_access\_logs](#load_balancer_enable_access_logs)
  - [mark\_for\_stop\_ec2\_resource](#mark_for_stop_ec2_resource)
  - [network\_firewall\_enable\_logging](#network_firewall_enable_logging)
  - [rds\_quarantine\_instance](#rds_quarantine_instance)
  - [route53domain\_enable\_auto\_renew](#route53domain_enable_auto_renew)  
  - [route53domain\_enable\_transfer\_lock](#route53domain_enable_transfer_lock)  
  - [sns\_set\_topic\_private](sns_set_topic_private)
  - [sns\_topic\_delete](sns_topic_delete)
  - [ssm\_document\_set\_private](#ssm_document_set_private)
  - [s3\_allow\_ssl\_only](#s3_allow_ssl_only)
  - [s3\_block\_all\_public\_access](#s3_block_all_public_access)
  - [s3\_delete\_acls](#s3_delete_acls)
  - [s3\_delete\_permissions](#s3_delete_permissions)
  - [s3\_disable\_static\_website\_hosting](#s3_disable_static_website_hosting)
  - [s3\_enable\_encryption](#s3_enable_encryption)
  - [s3\_enable\_logging](#s3_enable_logging)
  - [s3\_enable\_versioning](#s3_enable_versioning)
  - [s3\_limit\_access](#s3_limit_access)
  - [s3\_only\_allow\_ssl](#s3_only_allow_ssl)
  - [secretsmanager\_enable\_encryption](#secretsmanager_enable_encryption)
  - [sg\_clear\_rules\_for\_any\_scope](#sg_clear_rules_for_any_scope)
  - [sg\_delete](#sg_delete)
  - [sg\_delete\_not\_matching\_cidr](#sg_delete_not_matching_cidr)
  - [sg\_modify\_scope\_by\_port](#sg_modify_scope_by_port)
  - [sg\_rules\_delete](#sg_rules_delete)
  - [sg\_single\_rule\_delete](#sg_single_rule_delete)
  - [sns\_topic\_delete](#sns_topic_delete)
  - [sns\_enforce\_sse](#sns_enforce_sse)
  - [sqs\_configure\_dlq](#sqs_configure_dlq)
  - [sqs\_enforce\_sse](#sqs_enforce_sse)  
  - [tag\_ec2\_resource](#tag_ec2_resource)
  - [vpc\_delete](#vpc_delete)
  - [vpc\_isolate](#vpc_isolate)
  - [vpc\_turn\_on\_flow\_logs](#vpc_turn_on_flow_logs)
  - [sg\_rules\_delete\_by\_scope](#sg_rules_delete_by_scope)
    
  
  
###[Optional Bots](#optional-bots)
- [ec2\_tag\_instance\_from\_vpc](#ec2_tag_instance_from_vpc)
- [s3\_delete\_bucket](#s3_delete_bucket)

## acl\_delete

What it does: deletes created network acl.  
Usage: AUTO: acl_delete

Sample GSL: cloudtrail where event.name='CreateNetworkAcl'  
Limitation: None  
Note: Logic only bot

## acl\_revert\_modification

What it does: returns an acl to it's previous form.  
Usage: AUTO: acl_revert_modification   

Sample GSL: cloudtrail where event.name in ('ReplaceNetworkAclEntry', 'DeleteNetworkAclEntry', 'CreateNetworkAclEntry')  
Limitation: None  
Note: Logic only bot

##acm\_delete\_certificate
What it does: Deletes ACM certificate
Usage: AUTO: acm_delete_certificate
Limitations: none

## ami\_set\_to\_private

What it does: Sets an AMI to be private instead of public  
Usage:  ami\_set\_to\_private  
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

Usage:  cloudtrail\_enable trail\_name=\<trail\_name\>
bucket\_name=\<bucket\_name\>  
Note: Trail\_name and bucket\_name are optional and don't need to be
set.  
Limitations: none

## cloudtrail\_enable\_log\_file\_validation
What it does: Enable log file validation in cloudTrail
Usage:  cloudtrail_enable_log_file_validation
Limitations: None

## cloudtrail\_encrypt\_log\_files\_using\_existing\_key
What it does: Encrypt log file in the cloudTrial with a customer key that user pass as parameter.
Usage: AUTO: cloudtrail_encrypt_log_files_using_existing_key <key_id>
Note: - The key must have the correct policy for enable CloudTrail to encrypt, users to decrypt log files and user
            to describe key.
            For more information https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-kms-key-policy-for-cloudtrail.html
      - The key the user pass can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key,
        or a globally unique identifier
            Examples:
                * alias/MyAliasName
                * arn:aws:kms:us-east-2:123456789012:alias/MyAliasName
                * arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
                * 12345678-1234-1234-1234-123456789012
Limitations:None

## cloudtrail\_encrypt\_log\_files\_using\_new\_key\_creation
What it does: Create new customer key with the correct policy for encrypt log file in the cloudTrial.
Usage: AUTO: cloudtrail_encrypt_log_files_using_new_key_creation
Note: - The bot create a new customer key
Limitations:None


## cloudtrail\_send\_to\_cloudwatch

What it does: Makes CloudTrail output logs to CloudWatchLogs. If the log
group doesn't exist alredy, it'll reate a new one. Usage: 
cloudtrail\_send\_to\_cloudwatch \<log\_group\_name\>  
Limitations: none  
Defaults: If no log group name is set, it'll default to
CloudTrail/DefaultLogGroup  
Role name: CloudTrail\_CloudWatchLogs\_Role  
Log delivery policy name: CloudWatchLogsAllowDelivery

## cloudwatch\_create\_metric\_filter

What it does: Creates CloudWatch Metric Filters to match the CIS
Benchmark. A metric alarm and SNS subscripion is created as well  
Usage:  cloudwatch\_create\_metric\_filter \<email\_address\>
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
only turns on the configuration recorders. Usage:  config\_enable
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
Usage:  ec2\_attach\_instance\_role role\_arn=\<role\_arn\>

If you have a role that is the same across accounts, and don't want to
pass in an account specific ARN, add "$ACCOUNT\_ID" to the role ARN and
the function will automatically pull in the current account ID of the
finding.  
Example:  ec2\_attach\_instance\_role
role\_arn=arn:aws:iam::$ACCOUNT\_ID:instance-profile/ec2SSM  
Sample GSL: Instance should have roles

## ec2\_create\_snapshot

What it does: Snapshots the EBS volumes on an instance  
Usage:  ec2\_create\_snapshot  
Notes: The snapshot description will show that it was created by
CloudBots and the rule that failed that triggered the bot. Also, the
snapshot will be tagged with a key of "source\_instance\_id" and a value
with the instance id from the source instance.  
Limitations: This will not work on Instance Store volumes. Only EBS

## ec2\_detach\_instance\_role

What it does: Detach an instance role from an EC2 instance.  
Usage: AUTO: ec2_detach_instance_role  
Sample GSL: cloudtrail where event.name='AddRoleToInstanceProfile' and event.status='Success'  
Limitations: none

## ec2\_release\_eips

What it does: Disassociates and releases all EIPs on an instance  
Usage:  ec2\_release\_eips  
Limitations: none

## ec2\_quarantine\_instance

What it does: Attaches the instance a SG with no rules so it can't
communicate with the outside world  
Usage:  ec2\_quarantine\_instance  
Limitations: None

## ec2\_stop\_instance

What it does: Stops an ec2 instance  
Usage:  ec2\_stop\_instance  
Limitations: none

## ec2\_terminate\_instance

What it does: Terminates an ec2 instance  
Usage:  ec2\_terminate\_instance  
Limitations: none

## ec2\_update\_instance\_role

What it does: Updates an EXISTING EC2 instance role by attaching another
policy to the role. This policy needs be passed in through the params.  
Usage:  ec2\_update\_instance\_role policy\_arn=\<policy\_arn\>  
Example:  ec2\_update\_instance\_role
policy\_arn=arn:aws:iam::aws:policy/AlexaForBusinessDeviceSetup  
Sample GSL: Instance where roles should have roles with \[
managedPolicies contain \[ name='AmazonEC2RoleforSSM' \] \]

## ecs\_reboot

What it does: stops an ecs task and the service (which started the task) will create it again and run it.  
Usage: AUTO: ecs_reboot  
Sample GSL: cloudtrail where event.name='RegisterTaskDefinition' and event.status='Success'  
Limitations: none  

## ecs\_service\_role\_detach\_inline\_policy
What it does: removes all inline policies from the role of the ECS <br>
Usage: ecs_service_role_detach_inline_policy <br>
Limitations: None

## ecs\_stop

What it does: stops an ecs tasks and ec2 instances which contain the tasks  
Usage: AUTO: ecs_stop  
Sample GSL: cloudtrail where event.name='RegisterTaskDefinition' and event.status='Success'  
Limitations: none  

##  ecs\_delete\_repository\_image

What it does: Delete an image from  ECS repository
Usage:   ecs\_delete\_repository\_image

if an malicious image was Pushed to a ECS Repository
this function will delete the image from the repository.

Sample GSL: cloudtrail where event.name='DescribeImageScanFindings' and event.status = 'Success'

##iam\_detach\_policy
What it does: detach all entities that attached to policy
Usage: iam_detach_policy
Limitations: none

## iam\_delete\_access\_key

What it does: Deleting an IAM user AccessKey
Usage:  iam\_delete\_access\_key

if the root user create an access key or a user that dont need one 
this function will delete the AccessKey

Example:  iam\_delete\_access\_key
Sample GSL: cloudtrail where event.name='CreateAccessKey' and identity.type='Root'


## iam\_delete\_default\_policy\_version 
What it does: Delete the default policy version and set the latest instead.  
Usage: iam_delete_default_policy_version  
Limitations: Most be at least more than one version to the policy.  

## iam_generate_credential_report
What it does: Generates a credential report for the account. <br>
Usage: AUTO iam_generate_credential_report

## iam\_group\_delete\_inline\_policy
What it does: Deletes a inline policy attached to iam group
Usage: AUTO: iam_group_delete_inline_group
Limitations: none

## iam\_role\_attach\_policy

What it does: Attaches a policy (passed in as a variable) to the role  
Usage:  iam\_role\_attach\_policy policy\_arn=\<policy\_arn\>  
Limitations: none  
Examples:  
 iam\_role\_attach\_policy
policy\_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccess  
 iam\_role\_attach\_policy
policy\_arn=arn:aws:iam::621958466464:policy/sumo\_collection  
 iam\_role\_attach\_policy
policy\_arn=arn:aws:iam::$ACCOUNT\_ID:policy/sumo\_collection

## iam\_role\_clone\_with\_non\_enumerable\_name
What it does: Clones the IAM role and gives it a non-enumerable name. The new name is the original name +  20 length non-enumerable string, Example: MyRole -> MyRole-XaTrEiuNyHsRAqqC_rBW. </br>
Usage: AUTO: iam_role_clone_non_enumerable_name </br>
Limitations: The bot doesn't delete the original role, in order to avoid misconfigurations. After the role will be cloned, it's under your responsibility to delete the original role, after
validating it (For example, it's important to make sure that you do not have any Amazon EC2 instances running with the role). If you're using the bot via CSPM, the rule will keep failing
until the original role (with the enumerable name) will be deleted. In the response message of the bot, you'll get the information about the old and the new (cloned) role. </br>
For more information see:
https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_delete.html
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#replace-iam-role

## iam\_user\_attach\_policy

What it does: Attaches a policy (passed in as a variable) to the user  
Usage:  iam\_user\_attach\_policy policy\_arn=\<policy\_arn\>  
Limitations: none  
Examples:  
 iam\_user\_attach\_policy
policy\_arn=arn:aws:iam::aws:policy/AlexaForBusinessFullAccess  
 iam\_user\_attach\_policy
policy\_arn=arn:aws:iam::621958466464:policy/sumo\_collection  
 iam\_user\_attach\_policy
policy\_arn=arn:aws:iam::$ACCOUNT\_ID:policy/sumo\_collection

## iam\_user\_detach

Log.ic bot only  
What it does: Detaches an IAM user from an IAM group.  
Usage: AUTO: iam\_user\_detach  
Limitations: The bot will stop running if the proper 'AddUserToGroup' event is not found  
             The bot will not notify if the IAM user is already detached or was not attached to the group in the  
                 first place.
                 
## iam\_quarantine\_role

What it does: Adds an explicit deny all policy to IAM and directly
attaches it to a role  
Usage:  iam\_quarantine\_role  
Limitations: none

## iam\_quarantine\_user

What it does: Adds an explicit deny all policy to IAM and directly
attaches it to a user  
Usage:  iam\_quarantine\_user  
Limitations: none

## iam\_turn\_on\_password\_policy

What it does: Sets all settings in an account password policy  
Usage:  iam\_turn\_on\_password\_policy MinimumPasswordLength:<int>
RequireSymbols:\<True/False\> RequireNumbers:\<True/False\>
RequireUppercaseCharacters:\<True/False\>
RequireLowercaseCharacters:\<True/False\>
AllowUsersToChangePassword:\<True/False\> MaxPasswordAge:<int>
PasswordReusePrevention:<int> HardExpiry:\<True/False\>  
Limitations: ALL variables need to be set at the same time

Sample tag:  iam\_turn\_on\_password\_policy
MinimumPasswordLength:15 RequireSymbols:True RequireNumbers:True
RequireUppercaseCharacters:True RequireLowercaseCharacters:True
AllowUsersToChangePassword:True MaxPasswordAge:5
PasswordReusePrevention:5 HardExpiry:True

## iam_user_disable_console_password

What it does:  disable console password for IAM user.

Usage: iam_user_disable_console_password

Limitations: Deleting a user's password does not prevent a user from accessing AWS through the command line interface or
the API. To prevent all user access, you must also either make any access keys inactive or delete them.


## iam\_user\_deactivate\_unused\_access\_key
What it does: deactivate unused access key that haven't been in use for some time

Usage: iam_user_deactivate_unused_access_key <number of days>

Example: iam_user_inactivate_unused_access_key 90

Limitations: default time is 90 days, if there are more then 200 access keys for user should increase maxItems

## iam_user_delete_inline_policies
What it does: deleted all iam user inline policies and attach new maneged policies if pass as an argument

Usage: AUTH: iam_user_delete_inline_policies (option)maneged_policies=policy1_arn,policy2_arn


## iam\_user\_force\_password\_change

What it does: Updates the setting for an IAM user so that they need to
change their console password the next time they log in.  
Usage:  iam\_user\_force\_password\_change  
Limitations: none

## igw\_delete

What it does: Turns off ec2 instances with public IPs, detaches an IGW
from a VPC, and then deletes it.  
Limitations: VPCs have lots of interconnected services. This is
currently just focused on EC2 but future enhancements will need to be
made to turn off RDS, Redshift, etc.

## kms_cmk_enable_key
What it does: Enables a kms cmk (customer managed key) <br>
Usage: kms_cmk_enable_key

## kms\_enable\_rotation

What it does: Enables rotation on a KMS key  
Usage:  kms\_enable\_rotation  
Sample GSL: KMS where isCustomerManaged=true and deletionDate\!=0 should
have rotationStatus=true Limitations: Edits can not be made to AWS maged
keys. Only customer managed keys can be edited.

## lambda\_detach\_blanket\_permissions
What it does: For lambda that failed, it check all the policies that grant blanket permissions ('*') to resources and
              detach it from the lambda role
Usage:  lambda_detach_blanket_permissions
Note: The bot will detach the policies that have admin privileges from the lambda role so you will need to configure the specific
      policies to grant positive permissions to specific AWS services or actions
Limitations:None

## lambda\_disable  
What it does:  Disable lambda function (by put function concurrency = 0).  
Sample GSL:  cloudtrail where event.name like 'UpdateFunctionCode%' and issuer.type='Role'  
Usage:  AUTO: lambda_disable  
Limitations: none  

## lambda\_enable\_active\_tracing
What it does: Enable lambda active tracing
Usage: lambda_enable_active_tracing
Limitations: none

## lambda\_tag
What it does: Tags a lambda function </br>
Usage: AUTO: lambda_tag &lt;key> &lt;value> </br>
Notes:
value is an optional parameter. you can pass only key, without value. Usage: lambda_tag &lt;key> </br>
Limitations: Tags/values with spaces are currently not supported. it will be added in the future.

## load\_balancer\_enable\_access\_logs
What it does: enables access logging for a load balancer (elb, alb) <br>
Usage: AUTO: load_balancer_enable_access_logs <br>
Limitations: None 

## mark\_for\_stop\_ec2\_resource

What it does: Tags an ec2 resource with "marked\_for\_stop" and
<current epoch time>  
Usage:  mark\_for\_stop\_ec2\_resource <time>\<unit(m,h,d)\>  
Example:  mark\_for\_stop\_ec2\_resource 3h  
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

## network_firewall_enable_logging
What it does: Enable logging (Flow Logs or Alert) for a network firewall. The log destination type must be specified, the options are: S3, CloudWatchLogs, KinesisDataFirehose. <br>
For S3 and CloudWatchLogs, the bot can create the log destination, by adding 'create' as a third parameter. For KinesisDataFirehose, the name of the delivery stream MUST be provided
as a parameter. <br>
Usage: AUTO network_firewall_enable_logging &lt;LoggingType> &lt;LogDestinationType> &lt;LogDestination> <br>
&lt;LoggingType> can be: FLOW, ALERT <br>
&lt;LogDestinationType> can be: S3, CloudWatchLogs, KinesisDataFirehose (Case-Sensitive!) <br>
Examples: <br>
network_firewall_enable_logging FLOW S3 create (the bot will create the bucket) <br>
network_firewall_enable_logging ALERT CloudWatchLogs create (the bot will create the log group) <br>
network_firewall_enable_logging FLOW S3 my-bucket (logs will be sent to my-bucket. if there is a prefix, please provide it like this: my-bucket/prefix) <br>
network_firewall_enable_logging FLOW CloudWatchLogs my-log-group (logs will be sent to my-log-group) <br>
network_firewall_enable_logging FLOW KinesisDataFirehose my-delivery-stream (logs will be sent to my-delivery-stream) <br>
Limitations: None

## rds\_quarantine\_instance

What it does: Attaches the RDS instance a SG with no rules so it can't
communicate with the outside world  
Usage:  rds\_quarantine\_instance  
Limitations: Instance needs to be "Available" in order to update. If
it's in "backing up" state, this will fail  
(Might not work with Aurora since it's in a cluster)

## route53domain_enable_auto_renew
What it does: Configures Amazon Route 53 to automatically renew the specified domain before the domain registration expires. <br>
Usage: AUTO route53domain_enable_auto_renew <br>
Permissions: route53domains:EnableDomainAutoRenew

## route53domain_enable_transfer_lock
What it does: Sets the transfer lock on the domain. The bot will return the operation ID of the request, which can be used in order to track the operation status
by the GetOperationDetail. For more details: https://docs.aws.amazon.com/Route53/latest/APIReference/API_domains_GetOperationDetail.html <br>
Usage: AUTO route53domain_enable_transfer_lock <br>
Permissions: route53domains:EnableDomainTransferLock


## sns\_set\_topic\_private
What it does: set sns topic to private <br>
Usage: sns_set_topic_private policy&lt;class str>policy


## ssm\_document\_set\_private
What it does: removes all aws account that can access the file except of the one that pass as a param.
Note that the account ID's should be separated by column.
Usage: ssm_document_set_private AccountIdToAdd=<account_id_1>,<account_id_2>
Example: ssm_document_set_private
Limitations: None

##s3\_allow\_ssl\_only
What it does: force s3 bucket to accept only ssl requests
Usage: AUTO: s3_enforce_ssl_data_encryption
Limitations: none

## s3\_block\_all\_public\_access
What it does: turn on S3 Bucket Block public access : Block public access to buckets and objects granted
through Future New AND Existing public ACLs and Bucket Policies.

Usage:  s3_block_public_all_access

Limitations: none

Notes:
    -  before running this bot, ensure that your applications will work correctly without public access

## iam\_revoke\_access\_key

What it does: Revoking an IAM user AccessKey
Usage:  iam\_revoke\_access\_key

if the root user create an access key or a user that dont need one 
this function will revoke the AccessKey

Example:  iam\_revoke\_access\_key
Sample GSL: cloudtrail where event.name='CreateAccessKey' and identity.type='Root'


## s3\_delete\_acls

What it does: Deletes all ACLs from a bucket. If there is a bucket
policy, it'll be left alone.  
Usage:  s3\_delete\_acls  
Limitations: none

## s3\_delete\_permissions

What it does: Deletes all ACLs and bucket policies from a bucket  
Usage:  s3\_delete\_permissions  
Limitations: none

## s3\_disable\_static\_website\_hosting
What it does: deletes ant s3 static website hosting
Usage: s3_disable_website_static_hosting
Limitations: None
 
## s3\_enable\_encryption

What it does: Turns on encryption on the target bucket. <br>
Usage: AUTO: s3_enable_encryption &lt;encryption_type> &lt;kms-key-arn> (&lt;kms-key-arn> should be provided only if &lt;encryption_type> is KMS) <br>
Note: &lt;encryption_type> can be one of the following: <br>
1. s3 (for s3-managed keys) <br>
2. kms (for customer managed keys - RECOMMENDED) - for kms you MUST provide the &lt;kms-key-arn>. <br>
EXAMPLES: <br>
s3_enable_encryption s3 <br>
s3_enable_encryption kms arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab

 ## s3\_enable\_logging

What it does: Turns on server access logging. The target bucket needs to
be in the same region as the remediation bucket or it'll throw a
CrossLocationLoggingProhibitted error. This bot will create a bucket to
log to as well. Usage:  s3\_enable\_logging  
Limitations: none

## s3\_enable\_versioning

What it does: Turns on versioning for an S3 bucket  
Usage:  s3\_enable\_versioning  
Limitations: none

## s3\_limit\_access

What it does: Removes policies for the following actions for principals '*':
s3:Delete*, s3:Get*, s3:List*, s3:Put*, s3:RestoreObject and s3:*. </br>
Usage:  s3\_limit\_access </br>
Notes: The bot Removes these actions from the policy. if this is the only action, the whole policy will be removed.
If necessary, modify the policy after the deletation, to limit the access to specific principals. </br>
Limitations: The bot removes the policies for *all* the mentioned actions, if exist.

## s3\_only\_allow\_ssl
What it does: Ensure that S3 Buckets enforce encryption of data transfers using Secure Sockets Layer (SSL)
Usage:  s3_only_allow_ssl
Note: The bot looks at the bucket policy and adds to the current policy the missing actions(s3:GetObject and s3:PutObject)
      and the SSL statement.
      if no policy in the bucket, an SSL policy will add to the bucket
Limitations: none

## secretsmanager_enable_encryption
What it does: Enables data-at-rest encryption using KMS CMK (Customer Master Key). <br>
Usage: AUTO secretsmanager_enable_encryption <kms-key-id> <br>
EXAMPLE: secretsmanager_enable_encryption aaaaaaaa-bbbb-cccc-dddd-eeeeeeee <br>
Notes: <br>
secretsmanagers can be encrypted by a symmetric key only. <br> 
As a security best practice, we recommend to encrypt it with CMK. The bot will throw an error for aws-managed keys. <br>
The provided key must be in the same region as the secret. <br>
Required permissions: "secretsmanager:UpdateSecret", "kms:GenerateDataKey", "kms:Decrypt".

## sg_clear_rules_for_any_scope
What it does: Removes rules from a security group by port, protocol and direction only (for any scope).<br>
Usage: sg_clear_rules_for_any_scope <port> <protocol> <direction> <white-list> (<white-list> is not mandatory). <br>
Please provide the cidrs of the white list seperated by a comma, without spaces. for example: 10.0.0.1/32,10.0.0.2/32 <br>
Permissions:
- ec2:RevokeSecurityGroupEgress
- ec2:RevokeSecurityGroupIngress
- ec2:DescribeSecurityGroups

## sg\_delete

What it does: Deletes a security group  
Usage:  sg\_delete  
Limitations: This will fail if there is something still attached to the
SG.

##sg\_modify\_scope\_by\_port

What it does: modify Security Group's rules scope by a given port , new and old scope(optional).
Direction can be : inbound or outbound

Usage: sg_modify_scope_by_port <port> <change_scope_from|*> <change_scope_to> <direction>
 - When '*' set for replacing any rule with the specific port

Examples:
        
        sg_modify_scope_by_port 22 0.0.0.0/0 10.0.0.0/24 inbound
        sg_modify_scope_by_port 22 * 10.0.0.0/24 inbound
Notes:

    -  if the port is in a rule's port range, the bot will change the rule's ip to desire ip , to avoid that
      specify existing rule's scope instead of using '*'
    - to split the rule around the port you can use the bot : #sg_single_rule_delete

Limitations: IPv6 is not supported yet

## sg\_rules\_delete

What it does: Deletes all ingress and egress rules from a SG  
Usage:  sg\_rules\_delete  
Limitations: none


## sg_delete_not_matching_cidr
What it does: Deletes all rules on a security group , that have the given port and have a scope outside the given cidr
        * following GSL - SecurityGroup should not have inboundRules contain [ port<=x and portTo>=x and scope!= y  ]

Usage: sg_delete_not_matching_cidr <port> <cidr> <direction>

Parameters:
    port: number
    scope: a.b.c.d/e
    direction: inbound/ outbound


Example:

    sg_delete_not_matching_cidr 22 10.163.0.0/16 inbound

    *all the sg's rules with port 22 that have scope with range outside of 10.163.0.0/16 scope ,  will be deleted

Notes :

    -  before running this bot, ensure that your applications will work correctly without those rules
    - if a port is in a port range and there is a mismatch in cidr the rule will be deleted ( with all the other port in range )

Limitations: IPv6 is not supported yet



## sg_rules_delete_by_scope
What it does: Deletes all rules on a security group with a scope(cidr) containing or equal to a given scope,
             port and protocol are optional

Usage: sg_rules_delete_by_scope <scope> <direction> <port|*> <protocol|*>

Parameters:
   
    scope: a.b.c.d/e
    direction: inbound/ outbound
    port: number/ *
    protocol: TCP/ UDP/ *
    -When '*' is any value of the parameter

Examples:
    
    sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 tcp

    all rules with 1.0.0.0/16 scope will be deleted for any port and protocol:
    sg_rules_delete_by_scope 1.0.0.0/16 inbound * *

    all rules with 0.0.0.0/0 scope will be deleted for port 22 and any protocol:
    sg_rules_delete_by_scope 0.0.0.0/0 inbound 22 *

Notes :
    
    - the bot deletes the rule without splitting ports ( do not create new rules without the deleted port)
      for deleting rule with split use - sg_single_rule_delete bot .
    -  before running this bot, ensure that your applications will work correctly without those rules
    - if a port is in a port range the rule wont be deleted ! use * on port parameter to delete the rule for any port
Limitations: IPv6 is not supported

## sg\_single\_rule\_delete

What it does: Deletes a single rule on a security group Usage: 
sg\_single\_rule\_delete split=\<true|false\> protocol=\<TCP|UDP\>
scope=\<a.b.c.d/e\> direction=\<inbound|outbound\> port=<number>

Example:  sg\_single\_rule\_delete split=false protocol=TCP
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
 sg_single_rule_delete split=true protocol=TCP scope=8.8.8.8/32 direction=inbound port=0   

Limitations: IPv6 is not supported

## sns_enforce_sse
What it does: makes sns topic use server side encryption (sse) </br>
Usage:  sns_enforce_sse kmsKeyId=aaaaaaaa-bbbb-cccc-dddd-eeeeeeee </br>
Limitations: none


## sqs_enforce_sse
What it does: Configures server-side encryption (SSE) for a queue </br>
Usage:  sqs_enforce_sse <kmsKeyId> <kmsRegion> (<kmsRegion> is not required - provide it if the kms key is in a different region than the SQS). </br>
Examples:
sqs_enforce_sse aaaaaaaa-bbbb-cccc-dddd-eeeeeeee </br>
sqs_enforce_sse aaaaaaaa-bbbb-cccc-dddd-eeeeeeee us-east-2 </br>
sqs_enforce_sse mrk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (for multi-region key) </br>
sqs_enforce_sse mrk-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (for multi-region key, if it's in a different region) </br>
Limitations: The KMS key MUST be in the same AWS account as the SQS.

## sqs_configure_dlq
What it does: Configures a Dead-Letter Queue (DLQ) for a source queue. <br>
Usage: AUTO sqs_configure_dlq <br>
Notes: A dead-Letter Queue is also a queue. The bot doesn't create a DLQ if the queue is a DLQ itself. <br>
Limitations: None

## sns_topic_delete
What it does: Deletes sns topic and all its subscriptions. </br>
Usage: AUTO: sns_topic_delete </br>
Limitations: None


## tag\_ec2\_resource

What it does: Tags an ec2 instance  
Usage:  tag\_ec2\_resource "key" "value"  
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

## vpc_delete
What it does: deletes vpc 

Usage: AUTO: vpc_delete

## vpc\_isolate

What it does: turn off dns resource,    
              change network acl to new empty one with deny all,  
              add iam policy, to all users in the account, which limits vpc use: ec2 and sg use in the vpc  

Usage: AUTO: vpc_isolate  
Limitation: None

## vpc\_turn\_on\_flow\_logs

What it does: Turns on flow logs for a VPC Settings: Log Group Name:
vpcFlowLogs If traffic type to be logged isn't specified, it defaults to
all. Usage:  vpc\_turn\_on\_flow\_logs
traffic\_type=\<all|accept|reject\> destination=\<logs|s3\>
s3\_arn=arn:aws:s3:::my-bucket/my-logs/ Example: 
vpc\_turn\_on\_flow\_logs traffic\_type=all destination=logs Example:
 vpc\_turn\_on\_flow\_logs traffic\_type=all destination=s3
s3\_arn=arn:aws:s3:::my-bucket/my-logs/

Limitations: none Sample GSL: VPC should have hasFlowLogs=true

To specify a subfolder in the bucket, use the following ARN format:
bucket\_ARN/subfolder\_name/ . For example, to specify a subfolder named
my-logs in a bucket named my-bucket , use the following ARN:
arn:aws:s3:::my-bucket/my-logs/

log delivery policy name is set as: vpcFlowLogDelivery log delivery role
is set as: vpcFlowLogDelivery


# Optional Bots

These bots are not packaged with the core Lambda function because
they're extremely impactful or edge-case bots that won't be normally
used.  
If you want to use these bots, they will need to be manually added to
the function. All of the code is in the optional\_bots directory.

## ec2\_tag\_instance\_from\_vpc

### This bot was created for a customer and most likely won't be used outside of that edge case

What it does: If an instance is missing a specific tag, try to pull it
from the VPC. Usage:  ec2\_tag\_instance\_from\_vpc <Key>  
Limitations: none

## s3\_delete\_bucket

What it does: Deletes an S3 bucket  
Usage:  s3\_delete\_bucket  
Limitations: none
