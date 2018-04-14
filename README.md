<link rel="shortcut icon" type="image/x-icon" href="docs/pictures/favicon.ico">

```   
     |                  |   |         |         
,---.|    ,---..   .,---|   |---.,---.|--- ,---.
|    |    |   ||   ||   |---|   ||   ||    `---.
`---'`---'`---'`---'`---'   `---'`---'`---'`---'                                                
```

# Cloud-Bots
Auto remediation & automation bots for AWS.

This solution is meant to be used in conjunction with Dome9's Continuous Compliance Engine to remediate issues that are uncovered. 


Table of Contents
=================
* [Overview](#overview)
  * [What is this ?](#what-is-this-)
  * [Why and when would I need it ?](#why-and-when-would-i-need-it-)
  * [How does it work ?](#how-does-it-work-)
* [Setup Steps](#setup-steps)
  * [Decide on deployment mode](#decide-on-deployment-mode)
  * [Outside of Dome9 Easy mode](#outside-of-dome9)
  * [Outside of Dome9](#outside-of-dome9)
  * [In Dome9](#in-dome9)
* [Sample Setup Example](#sample-setup-example)


## For more technical information, please see README_ADVANCED.md

# Overview
## What is this ?
Cloud-Supervisor 2 is an **automatic remediation solution for AWS** built on top of Dome9's Continuous Compliance capabilities

## Why and when would I need it ?
Dome9 Compliance Engine continuously scans the relevant cloud account (AWS,Azure,GCP) for policy violations, and then alert and report.<br/>
For some organizations that is enough. However, at a certain scale and cloud matureness level- organizations prefer to move towards automatic-remediation approach, in which the system takes specific automated remediation bots in regards to specific violations.</br>
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

Click the link and click Next > Next > Next.


On the 4th page, you'll need to check the 2 boxes that allow this template to create IAM resources with custom names (This is for the role that is created for Lambda to perform the bots).

Next, click on the 'Create Change Set' button at the bottom of the page. Then click 'Execute' 

From here, the stack will deploy. If there are no errors, go to the 'Outputs' tab and grab the two ARNs that were output. You'll need them later. 


### OPTIONAL: Set up a subscriber to the SNS output topic
Since the Lambda output is exported to SNS, you can send it from there to wherever you please. 

- If you want to send the events to Slack, please follow this guide: https://github.com/alpalwal/D9SnsToSlack

- To get email alerts instead, you can do it from the CLI:
```bash
aws sns subscribe \
--topic-arn <OUTPUT_TOPIC_ARN> \
--protocol email \
--notification-endpoint <your email>
```




## Decide on deployment mode

### Single vs Multi

#### Single
In single account mode, the Lambda function will only remediate issues found within the account it's running in. If the event is from another account, it'll be skipped.

This is the default mode. Nothing needs to be changed. 


#### Multi
In multi account mode, the function will run in the local account but will also try to assume a role into another account if the event was from a different account than the one the function is running in. Each account that will have remediation bots will need a cross-account role to the master account. 

#### Setup for Multi-account mode in AWS:
In the dome9AutoRemediations lambda function:
- Update the ACCOUNT_MODE environment variable from 'single' to 'multi'
- By default, the cross account roles will all need to be named "dome9-auto-remediations". If you want a different name, add a new variable called "CROSS_ACCOUNT_ROLE_NAME" and set the value to the new name for the role. 


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
--role-name dome9-auto-remediations \
--assume-role-policy-document file://trust_policy.json \
--profile <aws_account_profile>                                      
```

#### Create the IAM policy for the role
```bash
aws iam create-policy \
--policy-name CloudSupervisorRemediations \
--policy-document file://remediation_policy.json \
--query 'Policy.Arn' \
--profile <aws_account_profile>                   
```

#### Link the new policy and role
Take ARN from create-policy for the next command           
```bash
aws iam attach-role-policy \
--role-name dome9-auto-remediations \
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

#### Tag Syntax: AUTO: <bot_name> <params>
    Ex: AUTO: ec2_stop_instance

### Test this compliance bundle. 
Make sure you're getting the results you want and expect

### Set the Dome9 compliance bundle to run via continuous compliance. 
If you're in single account mode, there needs to be a 1 Continuous Compliance bundle per account. If not, select all the accounts that you set up cross-account roles in. 
Set the output topic as the ARN from the InputTopicARN one we set up
Set the format to be JSON - Full Entity


### ********* NOTE: ********** 
Currently Continuous Compliance sends a 'diff' for the SNS notifications. Because of this, if you have ran the bundle before, only new issues will be sent to SNS. 
If you want to have the first auto-remediation run to include all pre-existing issues, you'll need to clone the bundle and set the new (never-ran) bundle as the thing that is being tested in the CC config. This works because if it's never ran, then every existing issue is considered 'new' and will be sent to SNS. 
This will be changed in future releases and is being currently worked on. 


### From here, you should be good to go!

## In Dome9

- Create a bundle that you want to use for auto remediation. 
![Sample Bundle](./docs/pictures/sample_bundle.png?raw=true "Title")

- Edit the bundle (Edit JSON). 
![Sample Bundle](./docs/pictures/edit_bundle.png?raw=true "Title")

- Paste in the text from sample_bundle.json. 
![Sample Bundle](./docs/pictures/edit_json.png?raw=true "Title")

- For any other rules that you want to create and add remediation to, add the remediation tag to the "Compliance Section" of the rule. 
![Rule Tagging](./docs/pictures/tagging_a_rule.png?raw=true "Title")

- Test this compliance bundle. 
![Sample Report](./docs/pictures/sample_report.png?raw=true "Title")
![Sample Results](./docs/pictures/sample_findings.png?raw=true "Title")

- Set the Dome9 compliance bundle to run via continuous compliance. 
![CC Setup1](./docs/pictures/cc_setup1.png?raw=true "Title")
![CC Setup2](./docs/pictures/cc_setup2.png?raw=true "Title")








## Questions / Comments
Contact: Alex Corstorphine (alex@dome9.com)



