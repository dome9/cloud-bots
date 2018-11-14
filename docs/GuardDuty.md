# GuardDuty
Setup Steps

* [Setup Steps](#setup-steps)
  * [Lambda Deployment](#lambda-deployment)
  * [GuardDuty Configuration](#guard-duty-configuration)
  * [Multi Account](#multi-account)
  * [Testing](#testing)
  * [Troubleshooting](#troubleshooting)
* [Sample Setup Example](#sample-setup-example)

![Data Flow](https://github.com/Dome9/cloud-bots/blob/master/docs/pictures/cloudbots_with_GD.png?raw=true "With GuardDuty")


## Lambda Deployment

You can deploy this stack via the link below. Pick the region that you would like it deployed in.   

| Region        | Launch        | 
| ------------- |:-------------:| 
|us-east-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3.amazonaws.com/dome9cftemplatesuseast1/cloudbots_cftemplate.yaml)|
|us-east-2|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-us-east-2.amazonaws.com/dome9cftemplatesuseast2/cloudbots_cftemplate.yaml)|
|us-west-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-us-west-1.amazonaws.com/dome9cftemplatesuswest1/cloudbots_cftemplate.yaml)|
|us-west-2|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-us-west-2.amazonaws.com/dome9cftemplatesuswest2/cloudbots_cftemplate.yaml)|
|ca-central-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ca-central-1.amazonaws.com/dome9cftemplatescacentral1/cloudbots_cftemplate.yaml)|
|eu-central-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-central-1.amazonaws.com/dome9cftemplateseucentral1/cloudbots_cftemplate.yaml)|
|eu-west-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-west-1.amazonaws.com/dome9cftemplateseuwest1/cloudbots_cftemplate.yaml)|
|eu-west-2|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-west-2.amazonaws.com/dome9cftemplateseuwest2/cloudbots_cftemplate.yaml)|
|eu-west-3|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-eu-west-3.amazonaws.com/dome9cftemplateseuwest3/cloudbots_cftemplate.yaml)|
|ap-northeast-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-northeast-1.amazonaws.com/dome9cftemplatesapnortheast1/cloudbots_cftemplate.yaml)|
|ap-northeast-2|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-northeast-2.amazonaws.com/dome9cftemplatesapnortheast2/cloudbots_cftemplate.yaml)|
|ap-southeast-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-southeast-1.amazonaws.com/dome9cftemplatesapsoutheast1/cloudbots_cftemplate.yaml)|
|ap-southeast-2|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-southeast-2.amazonaws.com/dome9cftemplatesapsoutheast2/cloudbots_cftemplate.yaml)|
|ap-south-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-ap-south-1.amazonaws.com/dome9cftemplatesapsouth1/cloudbots_cftemplate.yaml)|
|sa-east-1|[<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3-sa-east-1.amazonaws.com/dome9cftemplatessaeast1/cloudbots_cftemplate.yaml)|


<br>
<br>

**Click the link and click Next** 

In the parameters section leave it in single account mode since this currently only supports 1 account

If you would like to set up an SNS subscriber for the output topic (recommended) then put an email in the EmailAddress field. 
<br> 
<br> 

### In the GuardDutyRules section
Add in the mapping (in JSON format) for the different GuardDuty findings you want to auto-rememdiate and what actions you want to run when the event occurs.

If you don't want to auto-remediate a particular event or finding, just leave it out of the object or leave the bot syntax empty. 

Syntax:
```javascript
{
    "<guardduty event>": "<bot syntax>",
    "<guardduty event>": "<bot syntax>"
}
```

For a full list of GuardDuty findings, please check [gd_sample_actions.json](https://github.com/Dome9/cloud-bots/blob/master/gd_sample_actions.json)

Sample:
```javascript
{
    "Backdoor:EC2/XORDDOS": "AUTO: ec2_stop_instance",
    "Backdoor:EC2/Spambot": "AUTO: ec2_quarantine_instance"
}
```

**Click Next > Next**

**On the 4th page, you'll need to check the 2 boxes that allow this template to create IAM resources with custom names** (This is for the role that is created for Lambda to perform the bots)

**Next, click on the 'Create Change Set' button** at the bottom of the page. Then click 'Execute' 

From here, the stack will deploy. If there are no errors, go to the 'Outputs' tab and grab the two ARNs that were output. You'll need them later. 

**If you set up an SNS Subscriber**
Go to your email and confirm the subscription. SNS seems to have some odd behaviors if you leave the subscription for a while before confirming. 

<br>
<br>

## GuardDuty Configuration

### Run ./enable_guard_duty.sh

Usage: ./enable_guard_duty.sh <lambda_arn> <aws_profile_name>  
Example: ./enable_guard_duty.sh arn:aws:lambda:us-west-2:936643454293:function:Dome9CloudBots sandbox

If no profile name is included, it defaults to 'default'.

This shell script will configure GuardDuty and let the data be sent to the correct lambda function.  
This runs as a shell script since CloudFormation runs per-region and this would be a hassle to manually put in each region. 

If you don't want to enable GD in a certain region, remove the region name from line 3 of the script. 

For each region defined it will:
- Enable GD
- Create a SNS topic
- Create a CW events rule to catch GD events and send it to SNS
- Update the SNS policy to allow delivery from CW
- Set up a target lambda function as a SNS subscriber 
- Update the lambda function invocation policy to allow SNS to trigger it


## Multi Account

Setting up multiple accounts to work with a single deployment of CloudBots is very straightforward because GD easily sends events across accounts.  

At a high level, GuardDuty events from other accounts still have the same structure as standard GD events, but it's tagged with the source ID from the account the event occurred in. CloudBots will see that the event occurred in an account outside of the one that it's running in and will then assume a role via cross-account role to run the remediation. 


### Steps to set up multi-account GuardDuty

This repo from AWS can be used to link multiple accounts together for GuardDuty findings.  
https://github.com/aws-samples/amazon-guardduty-multiaccount-scripts  

If you don't use this, you can manually invite accounts to each other, but this needs to be done for each region you're using GD in, and for every account. The script is going to be the faster way for anything over a couple accounts.  


### Steps to set up CloudBots to run in multi-account mode

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
              
                  
               


             
              




## Testing

Testing with GuardDuty can be a pain. There are two ways you can test this to make sure it's working.

### Generate Sample Events

In AWS, go to the GuardDuty console > Settings and click on "Generate Sample Findings".  
This will create some sample findings that will trigger the lambda function. You will get emails with this line:  
"GuardDuty sample event found. Instance ID from the finding is i-99999999. Skipping"  

CloudBots is configured to skip the sample findings so it doesn't hammer your inbox with sample events. You can see if the events were properly handled by checking out the CloudWatch Logs for the CloudBots function


### Generate Real Events

AWS has a project up on their GitHub page that can be used to generate GuardDuty findings:  
https://github.com/awslabs/amazon-guardduty-tester

It takes ~10 minutes to create the CloudFormation stack for this and then another 5 or so to log in and generate the findings. This is the best way to be sure that the events will trigger and auto-remediate though. 


## Troubleshooting

If things aren't working as expected, try troubleshooting in this order:
- Make sure the CloudBots CloudFormation stack created without errors
- Pick a random region and check to see that GuardDuty is enabled
- Check that there is a CloudWatch Events rule called "GuardDutyFindings" and that it has an SNS topic as a target
- Go to the SNS topic and verify that it has a lambda function as a subscriber
- Add another subscriber to the topic that sends emails to your inbox. This can help verify if events are making it from GD all the way to SNS or if the issue is down stream in the function
- Take a look at the lambda function's logs - Are there any recent logs? 
- Look through the most recent invocation logs for further information and troubleshooting leads


## Questions / Comments
Contact: Alex Corstorphine (alex@dome9.com)



