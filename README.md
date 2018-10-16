```   
     |                  ||         |         
,---.|    ,---..   .,---||---.,---.|--- ,---.
|    |    |   ||   ||   ||   ||   ||    `---.
`---'`---'`---'`---'`---'`---'`---'`---'`---'                                                
```


# CloudBots
Auto remediation & automation bots for AWS.

This solution is meant to be used in conjunction with Dome9's Continuous Compliance Engine or AWS GuardDuty to remediate issues that are uncovered. 


Table of Contents
=================
* [Overview](#overview)
  * [What is this ?](#what-is-this-)
  * [Why and when would I need it ?](#why-and-when-would-i-need-it-)
  * [How does it work ?](#how-does-it-work-)
  * [FAQ](#faq)
* [Setup Steps](#setup-steps)
  * [Decide on deployment mode](#decide-on-deployment-mode)
  * [Outside of Dome9 Easy mode](#outside-of-dome9)
  * [Outside of Dome9](#outside-of-dome9)
  * [In Dome9](#in-dome9)
  * [Updating the stack](#updating-the-stack)
* [Sample Setup Example](#sample-setup-example)
* [Actions](#actions)
* [Release Notes](#release-notes)

## For a GuardDuty quickstart doc, please see [README_GUARDDUTY.md](https://github.com/Dome9/cloud-bots/blob/master/README_GUARDDUTY.md)

## For a condensed quickstart doc, please see [README_QUICKSTART.md](https://github.com/Dome9/cloud-bots/blob/master/README_QUICKSTART.md)

## For more technical information, please see [README_ADVANCED.md](https://github.com/Dome9/cloud-bots/blob/master/README_ADVANCED.md)

## For more information on creating your own bots, please see [README_DEVELOPER_GUIDE.md](https://github.com/Dome9/cloud-bots/blob/master/README_DEVELOPER_GUIDE.md)

# Overview
## What is this ?
Cloud-Bots is an **automatic remediation solution for AWS** built on top of Dome9's Continuous Compliance capabilities

## Why and when would I need it ?
Dome9 Compliance Engine continuously scans the relevant cloud account (AWS,Azure,GCP) for policy violations, and then alert and report.<br/>
For some organizations that is enough. However, at a certain scale and cloud matureness level- organizations prefer to move towards automatic-remediation approach, in which the system takes specific automated remediation bots in regards to specific violations.<br/>
This approach could reduce the load from the security operators and drastically reduce the time to resolve security issues.

## How does it work ?

### Single account mode:
![Data Flow](./docs/pictures/data-flow.png?raw=true "Single account mode")



### Multi account mode:
![Data Flow](./docs/pictures/cs2_multi_acct_workflow.jpg?raw=true "Multi account mode")



- Dome9 will scan the accounts on an ongoing basis and send failing rules to SNS
- In the rules, if we want to add remediation, we can add in a "remediation flag" into the compliance section so that the SNS event is tagged with what we want to do. 
- Each remediation bot that is tagged correlates to a file in the bots folder of the remediation function. 
- Lambda reads the message tags and looks for a tag that matches AUTO: <anything>
- If any of those AUTO tags match a remediation that we have built out, it'll call that bot.
- All of the methods are sending their events to an array called text_output. Once the function is finished working, this array is turned into a string and posted to SNS

## FAQ

### Where can I see this in action? 
Here are two videos on CloudBots:  
- [Initial Setup](https://www.youtube.com/watch?v=HTRAq8g6dnk)
- [Remediating an exposed S3 bucket](https://www.youtube.com/watch?v=Fb3gjFlxXjA)


### Where does the function live?
The function can exist in any region you want in your account. Only one is needed per account though. 

### How many do I need?
In multi-account mode, only one function is required.
In single account mode, one function is required per account.

In either mode, there's no need for one function per region or antyhing like that. The max is one function per account.  

Every cloud-bot lives in the same function. There aren't multiple functions for the different bots.  


### Does this use the original Dome9 role?
No. The Dome9-connect role is only for Dome9 to collect data from your AWS accounts. The CloudBots function needs its own execution role to run the remediation actions, but it's completely separate from the Dome9 role. 

### Where does the AUTO: <bot> syntax come from? 
AUTO: is used to signal to CloudBots that a remediation action needs to be triggered. The bot name correlates to a file name in the bots/ folder. 

### Why isn't it in the remediation field of the rule? 
By putting the bot syntax in the "Compliance Section" field, multiple actions can be triggered from one rule since the Compliance Section is passed through the event as an array.  

### How do I add on new "bots"?
Any new bot needs to go into the bots folder in the function. From there, you call it with the AUTO: syntax.  
For example, a delete user bot would be named delete_user.py and put in the bots folder.  
It would be triggered with "AUTO: delete_user"  

### What languages are supported?
Currently only python is supported  

### How are the permissions segregated between Dome9 and CloudBots?
Dome9's cross account role is completely separate from the CloudBots permissions and cross account roles. Dome9 permissions are in yellow, while the CloudBots permissions are in bold.  This is done so that the most sensitive permissions stay within the customer environments and are never given to a third party. 

![Permissions model](./docs/pictures/cloudbots_permissions.png?raw=true "Permissions model")


# Setup Steps

## Outside of Dome9

You can deploy this stack via the link below. Pick the region that you would like it deployed in.   

| Region        | Launch        | 
| ------------- |:-------------:| 
|us-east-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3.amazonaws.com/dome9cftemplatesuseast1/cloudbots_cftemplate.yaml)|
|us-east-2|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-us-east-2.amazonaws.com/dome9cftemplatesuseast2/cloudbots_cftemplate.yaml)|
|us-west-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-us-west-1.amazonaws.com/dome9cftemplatesuswest1/cloudbots_cftemplate.yaml)|
|us-west-2|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-us-west-2.amazonaws.com/dome9cftemplatesuswest2/cloudbots_cftemplate.yaml)|
|ca-central-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ca-central-1.amazonaws.com/dome9cftemplatescacentral1/cloudbots_cftemplate.yaml)|
|eu-central-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-central-1.amazonaws.com/dome9cftemplateseucentral1/cloudbots_cftemplate.yaml)|
|eu-west-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-west-1.amazonaws.com/dome9cftemplateseuwest1/cloudbots_cftemplate.yaml)|
|eu-west-2|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-west-2.amazonaws.com/dome9cftemplateseuwest2/cloudbots_cftemplate.yaml)|
|eu-west-3|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-west-3.amazonaws.com/dome9cftemplateseuwest3/cloudbots_cftemplate.yaml)|
|ap-northeast-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-northeast-1.amazonaws.com/dome9cftemplatesapnortheast1/cloudbots_cftemplate.yaml)|
|ap-northeast-2|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-northeast-2.amazonaws.com/dome9cftemplatesapnortheast2/cloudbots_cftemplate.yaml)|
|ap-southeast-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-southeast-1.amazonaws.com/dome9cftemplatesapsoutheast1/cloudbots_cftemplate.yaml)|
|ap-southeast-2|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-southeast-2.amazonaws.com/dome9cftemplatesapsoutheast2/cloudbots_cftemplate.yaml)|
|ap-south-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-south-1.amazonaws.com/dome9cftemplatesapsouth1/cloudbots_cftemplate.yaml)|
|sa-east-1|[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-sa-east-1.amazonaws.com/dome9cftemplatessaeast1/cloudbots_cftemplate.yaml)|

**If you want to deploy this via CLI, please see README_ADVANCED.md**

* Click the link and click Next

* In the parameters section, set the Deployment Mode as single or multi depending on if this will be run across multiple accounts or not. (you can change this later if needed)

* In the email address field, put in one of the subscriber emails we saved in step 1. 

* Click on Next > Next.

* On the 4th page, you'll need to check the 2 boxes that allow this template to create IAM resources with custom names (This is for the role that is created for Lambda to perform the bots).

* Next, click on the 'Create Change Set' button at the bottom of the page. Then click 'Execute' 

* From here, the stack will deploy. If there are no errors, go to the 'Outputs' tab and grab the two ARNs that were output. You'll need them later. 



## Decide on deployment mode

### Single vs Multi

#### Single
In single account mode, the Lambda function will only remediate issues found within the account it's running in. If the event is from another account, it'll be skipped.

This is the default mode. Nothing needs to be changed. 


#### Multi
In multi account mode, the function will run in the local account but will also try to assume a role into another account if the event was from a different account than the one the function is running in. Each account that will have remediation bots will need a cross-account role to the master account. 

#### Setup for Multi-account mode in AWS:
In the Dome9CloudBots lambda function:
- Update the ACCOUNT_MODE environment variable from 'single' to 'multi'
- By default, the cross account roles will all need to be named "Dome9CloudBots". If you want a different name, add a new variable called "CROSS_ACCOUNT_ROLE_NAME" and set the value to the new name for the role. 


#### Set up cross account roles for EACH account that will be remediated

```bash
cd cross_account_role_configs
```

Role creation needs to be done via something other than CloudFormation because CFTs don't output consistent role names

#### Update trust_policy.json with the account ID where the main function will live

#### There is a small bash script in this directory that you can run (create_role.sh) to create these roles. 
```bash 
./create_role.sh <aws profile>
```


#### Manual Setup:

#### Create the cross-account role
```bash
aws iam create-role \
--role-name Dome9CloudBots \
--assume-role-policy-document file://trust_policy.json \
--profile <aws_account_profile>                                        
```

#### Create the IAM policy for the role
```bash
aws iam create-policy \
--policy-name Dome9CloudBots \
--policy-document file://remediation_policy.json \
--query 'Policy.Arn' \
--profile <aws_account_profile>                      
```

#### Take the ARN from this for the next command           
```bash
aws iam create-role \
--role-name Dome9CloudBots \
--assume-role-policy-document file://trust_policy.json \
--profile <aws_account_profile>     
```

#### Link the new policy and role
Take ARN from create-policy for the next command           
```bash
aws iam attach-role-policy \
--role-name Dome9CloudBots \
--policy-arn <ARN FROM LAST COMMAND> \
--profile <aws_account_profile>                     
```              
              
                  
               


             
              




## In Dome9
See [this section](#in-dome9-1) for sample screenshots of the setup

### Create a bundle that you want to use for auto remediation. 
It's recommended but not required to break remediation bots into their own bundles. 
There is a sample bundle (sample_bundle.json) that can be used as a starting point.
The rule in the sample bundle will remove rules from the default security group if the SG is empty. 

### For all rules that you want to add remediation to, add the remediation tag to the "Compliance Section" of the rule. 

All available remediation bots are in the bots folder. 

#### Tag Syntax: `AUTO: <bot_name> <optional space delimeted params>`
    Ex: AUTO: ec2_stop_instance

### Test this compliance bundle. 
Make sure you're getting the results you want and expect

### Set the Dome9 compliance bundle to run via continuous compliance. 
If you're in single account mode, there needs to be a 1 Continuous Compliance bundle per account. If not, select all the accounts that you set up cross-account roles in. 
Set the output topic as the ARN from the InputTopicARN one we set up
Set the format to be JSON - Full Entity


### ********* NOTE: ********** 
Currently Continuous Compliance sends a 'diff' for the SNS notifications. Because of this, if you have ran the bundle before, only new issues will be sent to SNS. 
If you want to have the first auto-remediation run to include all pre-existing issues, you'll need to use the "send all events" button to force a re-send. 

For the compliance policy you have set up, look for a button on the right hand side with an arrow pointing up.  
![Send all events button](./docs/pictures/send_all_events_button.png?raw=true "Send all events button")

In this page, select SNS as the delivery method and your notification policy as the place to send the events.  
This can also be useful for rolling out new bots and/or testing since you can re-send the same event more than once.  
![Send all events page](./docs/pictures/send_all_events_page.png?raw=true "Send all events page")



### From here, you should be good to go!

## In Dome9

- Create a bundle that you want to use for auto remediation. 
![Sample Bundle](./docs/pictures/sample_bundle.png?raw=true)

- Edit the bundle (Edit JSON). 
![Sample Bundle](./docs/pictures/edit_bundle.png?raw=true)

- Paste in the text from sample_bundle.json. 
![Sample Bundle](./docs/pictures/edit_json.png?raw=true)

- For any other rules that you want to create and add remediation to, add the remediation tag to the "Compliance Section" of the rule. 
![Rule Tagging](./docs/pictures/tagging_a_rule.png?raw=true)

- Test this compliance bundle. 
![Sample Report](./docs/pictures/sample_report.png?raw=true)
![Sample Results](./docs/pictures/sample_findings.png?raw=true)

- Set the Dome9 compliance bundle to run via continuous compliance. 
![CC Setup1](./docs/pictures/cc_setup1.png?raw=true)
![CC Setup2](./docs/pictures/cc_setup2.png?raw=true)

# Updating the stack

Updating your current CloudBots stack is very straightforward. In the UI, navigate to CloudFormation for the region that CloudBots is set up in. 

* Select the dome9CloudBots stack and then select Actions > Update Stack
* Select "Specify an Amazon S3 template URL" and copy the link from the table below that corresponds to the region you're in. 
* Click next/update all the way through and it'll deploy the new version of the template.

| Region        | CFT Link        | 
| ------------- |:-------------:| 
|us-east-1|https://s3.amazonaws.com/dome9cftemplatesuseast1/cloudbots_cftemplate.yaml|
|us-east-2|https://s3-us-east-2.amazonaws.com/dome9cftemplatesuseast2/cloudbots_cftemplate.yaml|
|us-west-1|https://s3-us-west-1.amazonaws.com/dome9cftemplatesuswest1/cloudbots_cftemplate.yaml|
|us-west-2|https://s3-us-west-2.amazonaws.com/dome9cftemplatesuswest2/cloudbots_cftemplate.yaml|
|ca-central-1|https://s3-ca-central-1.amazonaws.com/dome9cftemplatescacentral1/cloudbots_cftemplate.yaml|
|eu-central-1|https://s3-eu-central-1.amazonaws.com/dome9cftemplateseucentral1/cloudbots_cftemplate.yaml|
|eu-west-1|https://s3-eu-west-1.amazonaws.com/dome9cftemplateseuwest1/cloudbots_cftemplate.yaml|
|eu-west-2|https://s3-eu-west-2.amazonaws.com/dome9cftemplateseuwest2/cloudbots_cftemplate.yaml|
|eu-west-3|https://s3-eu-west-3.amazonaws.com/dome9cftemplateseuwest3/cloudbots_cftemplate.yaml|
|ap-northeast-1|https://s3-ap-northeast-1.amazonaws.com/dome9cftemplatesapnortheast1/cloudbots_cftemplate.yaml|
|ap-northeast-2|https://s3-ap-northeast-2.amazonaws.com/dome9cftemplatesapnortheast2/cloudbots_cftemplate.yaml|
|ap-southeast-1|https://s3-ap-southeast-1.amazonaws.com/dome9cftemplatesapsoutheast1/cloudbots_cftemplate.yaml|
|ap-southeast-2|https://s3-ap-southeast-2.amazonaws.com/dome9cftemplatesapsoutheast2/cloudbots_cftemplate.yaml|
|ap-south-1|https://s3-ap-south-1.amazonaws.com/dome9cftemplatesapsouth1/cloudbots_cftemplate.yaml|
|sa-east-1|https://s3-sa-east-1.amazonaws.com/dome9cftemplatessaeast1/cloudbots_cftemplate.yaml|



# Actions

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

## mark_for_stop_ec2_resource
What it does: Tags an ec2 resource with "marked_for_stop" and <current epoch time>     
Usage: AUTO: mark_for_stop_ec2_resource <time><unit(m,h,d)>  
Example: AUTO: mark_for_stop_ec2_resource 3h  
Note: This is meant to be used in conjunction with a more aggressive action like stopping or termanating an instance. The first step will be to tag an instance with the time that we want to tigger the remediation bot.  
From there, a rule like "Instance should not have tags with [ key='marked_for_stop' and value before(1, 'minutes') ]" can be ran to check how long an instance has had the 'mark for stop' tag. 
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


## rds_quarantine_instance
What it does: Attaches the RDS instance a SG with no rules so it can't communicate with the outside world  
Usage: AUTO: rds_quarantine_instance  
Limitations: Instance needs to be "Available" in order to update. If it's in "backing up" state, this will fail  
(Might not work with Aurora since it's in a cluster)  

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


## Release Notes

#### 10/1/18
Updated sg_single_rule_delete to support deleting just a single port from a wider scope of rules (ex: deleting just port 22 from ports 10-30).  
2 new permissions are required to support this bot:  
ec2:AuthorizeSecurityGroupEgress  
ec2:AuthorizeSecurityGroupIngress   

Updated vpc_turn_on_flow_logs to support sending logs to S3 instead of CloudWatch logs

#### 10/2/18
Created a new folder called optional_bots. This will not be packaged with the standard Lambda function and will need to be added in manually as required.  
Bots that are extremely impactful (s3_delete_bucket, etc.) will live here as well as edge case bots that were made for specific customers (ec2_tag_instance_from_vpc).  



## Questions / Comments
Contact: Alex Corstorphine (alex@dome9.com)



