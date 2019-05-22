# CloudBots

# Overview

## What are D9 cloudbots?

Cloud-Bots is an autoremediation solution for AWS, built on top of the CloudGuard Dome9 Continuous Compliance capabilities.

They can also be used standalone, without Dome9, to remedy issues in AWS accounts. Details are included how to configure and trigger them. 

## What does it do?

If you have configured Dome9 Continuous Compliance rulesets for your cloud account, the Dome9 Compliance Engine continuously scans  your cloud account (AWS,Azure,GCP) for rule violations, and issues alerts and reports for issues that are found.

CloudBots provide autoremediation for these issues, in which you configure your cloud account to  trigger  specific remedial actions, using cloudbots, in response to specific compliance violations. The actions use the  cloudbots included here. They are  typically  scripts, which perform actions on your cloud account.

You can use the cloudbots without Dome9, using the same triggers, but sourced from your application (details for configuring this included).

## How does it work?

Dome9 continuously  scans your cloud accounts (using compliance rulesets)  and can be configured to send findings for  failed rules to an AWS SNS.

To add a remediation step, the rule is modified to include  a "remediation flag" in the compliance section so that the SNS event is tagged with what we want to do.
Each remediation bot that is tagged corresponds to a file in the bots folder of the remediation function.

When you deploy the cloudbots in your account, a Lambda function is deployed. This Lambda function picks up the event messages from the SNS, reads the message tags, and looks for a tag that matches AUTO:
If any of those AUTO tags match a remediation bot it will call that bot.
All of the methods are sending their events to an array called text_output. Once the function is finished working, this array is turned into a string and posted to SNS.

## Deployment modes

You can deploy the cloudbots in a single AWS account, or across multiple accounts.

### Single account mode

The default mode is 'single' account. Remediations will be applied to entities in a single account. It follows this workflow:

![single mode](docs/pictures/data-flow.png)


### Multi mode

In multi-mode, remediations are applied for more than one account. The lambda function is deployed in only one account, but used cross-account roles to run bots in other accounts. It follows this workflow:

![multi mode](docs/pictures/cs2_multi_acct_workflow.jpg)


# Onboarding

## Setup your AWS account(s) for cloudbots
Follow these steps for each region in your account in which you want to deploy the bots.

1. Select the region (deployment links), click  [<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://s3.amazonaws.com/dome9cftemplatesuseast1/cloudbots_cftemplate.yaml). 
This will launch a script in the AWS CloudFormation console, for your AWS account, to setup cloud-bots in the selected region.
1. In the **Select Template**, click **Next** (no need to make a selection)
1. In the **Parameters** section select the deployment mode, *single* or *multi* mode. Enter an email address for SNS notifications in the EmailAddress field (optional),then click **Next**
1. In the **Options** page, click **Next** (no need to make any selections)
1. In the **Review** page, select the options:

``` I acknowledge that AWS CloudFormation might create IAM resources```

``` I acknowledge that AWS CloudFormation might create IAM resources with custom names.```

6. Click **Create Change Set**, then **Execute**. The stack will be created in your AWS account. It will appear as *dome9CloudBots* in the list of stacks in the CloudFormation console.
1. Select the stack, and then select the **Outputs** section.
1. Copy the two ARNs there, *OutputTopicARN* and *InputTopicARN* and save them; they will be used to setup the SNS to trigger the bots, and the output reporting channel.

## Onboarding for Multi mode

For multi-mode, you will setup one account as above for the single mode, and then set up cross account roles in each additional account.

On the AWS console, for your account, perform these steps:

1. Set the ACCOUNT_MODE environment variable to *multi*.
1. Edit the *trust_policy.json* file (in the *cross_account_role_configs* folder),to add the account id of the additional account. Then, run the following commands:
```
cd cross_account_role_configs
./create_role.sh <aws profile>
```

This script will create the IAM role and policy and the cross-account role for the additional account.

# Setup your Dome9 account

## Configure the rules
Follow these steps in your Dome9 account to tag the compliance rules & rulesets to use bots as a remediation step.

1. In the Dome9 console, navigate to the Rulesets page in the Compliance & Governance menu.
1. Select the rules for which you want to add a remediation step.
1. In the Compliance Section add a row with the following string:
``` AUTO: <bot-name> <params> ```
   where *bot-name* is the name of the bot, and *params* is a list of arguments for the bot (if any).
   
   For example,  ``` AUTO: ec2_stop_instance ``` will run the bot to stop an EC2 instance.

### Test the rule

## Configure the Continuous Compliance policy

Once the rules in the ruleset have been tagged for remediation, set up a Continuous Compliance policy to run the ruleset, and send findings to the SNS.

1. Navigate to the **Policies** page in the Compliance & Governance menu.
1. Click **ADD POLICY** (on the right).
1. Select the account from the list, then click **NEXT**.
1. Select the ruleset from the list, then click **NEXT**.
1. Click **ADD NOTIFICATION**.
1. Select *SNS notification for each new finding as soon as it is discovered*, and enter the ARN for the SNS (*InputTopicARN*, created above). Select option *JSON - Full entity*, and then click **SAVE**.

**Note:** Dome9 will  send event messages to the SNS for new findings. To send events for previous findings, follow these steps:
1. Navigate to the **Policies** page.
1. Find the ruleset and account in the list, and hover over the right of the row, then click on the *Send All Alerts* icon.
![](docs/pictures/send_all_events_button.png)
1. Select the *SNS* Notification Type option, and the Notification Policy (the one created above), then click **SEND**. Dome9 will send event messages to the SNS for findings.

# Use the cloudbots without Dome9

You can use the cloudbots without a Dome9 account. In this case you must send messages to the SNS for each event that requires remediation. The message should have the following format:

```
{
  "reportTime": "2018-03-20T05:40:42.043Z",
  "rule": {
    "name": "<name for rule>",
    "complianceTags": "AUTO: <bot-name>"
  },
  "status": "Failed",
  "account": {
    "id": "************"
  },
  "entity": {
    "accountNumber": "************",
    "id": "i-*****************",
    "name": "************",
    "region": "us_west_2",
  }
}
```
where 
 *account: id* and *accountNumber* is your AWS account number (from AWS)
 
 *status* is marked *Failed*
 
 *entity: id* is the id for the entity that failed the rule
 

