<p align="center">
    <a href="https://cloudbots.dome9.com">
      <img width="150" src="cloudbotslogo.svg">
    </a>
</p>

<div align="center">
    <h1><a target="_blank" href="https://cloudbots.dome9.com">CloudBots</a> is an automatic remediation solution for public cloud platforms (AWS, <a href="https://github.com/Dome9/cloud-bots-azure" targe="_blank">Azure</a> and <a href="https://github.com/Dome9/cloud-bots-gcp" targe="_blank">GCP</a>)</h1>
</div>

  - [Overview](#overview)
      - [What are Dome9 CloudBots?](#what-are-dome9-cloudbots)
      - [What does it do?](#what-does-it-do)
      - [How does it work?](#how-does-it-work)
      - [The Bots](#the-bots)
      - [Deployment modes](#deployment-modes)
  - [Onboarding](#onboarding)
      - [Setup your AWS account(s) for
        CloudBots](#setup-your-aws-accounts-for-cloudbots)
      - [Onboarding for Multi mode](#onboarding-for-multi-mode)
  - [Setup your Dome9 account](#setup-your-dome9-account)
      - [Configure the rules](#configure-the-rules)
      - [Configure the Continuous Compliance
        policy](#configure-the-continuous-compliance-policy)
  - [Use the CloudBots without Dome9](#use-the-cloudbots-without-dome9)
  - [Log Collection for Troubleshooting](#log-collection-for-troubleshooting)


# Overview

## What are Dome9 Cloud Bots?

As it's name suggests Dome9 Cloud Bots are a collection of cloud-based software bots that are built on top of the [CloudGuard Dome9](https://dome9.com/) Continuous Compliance capabilities. They can be used both with CloudGuard Dome9 or on their own to identify and fix compliance issues with cloud platforms. 

This document is limited to providing instructions for getting them to work with the [AWS Cloud platform](https://aws.amazon.com/). There are separate instructions for [Google](https://github.com/Dome9/cloud-bots-gcp) and [Azure](https://github.com/Dome9/cloud-bots-azure) cloud platforms. 

## What does it do?

You can configure [Dome9 Continuous Compliance](https://www.checkpoint.com/products/public-cloud-compliance-governance/) to assess your cloud accounts against predefined rulesets, continually checking their compliance. Findings are reported in the form of near real-time reports.

Cloud Bots compliments this reporting function by providing the ability to trigger a remedial action on the cloud object triggering the violation from within the failed compliance rule itself. 

For example, when a rule that checks for rotation being enabled on a [customer-managed KMS](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#master_keys) fails, it can trigger the *kms\_enable\_rotation* bot to fix the issue by enable rotation. Similarly a rule that checks for CloudTrail being enabled could trigger the *cloud\_trailenable*  bot to create and enable a CloudTrail. Both failures and fix actions are logged to the report. 

Most importantly, Cloud Bots can be used without Dome9 by using same triggers sourced from your application. Details on this are in sections to follow.

## How does it work?

Using Dome9 Cloud Bots are deployed to your AWS account as a [CloudFormation stack](https://docs.aws.amazon.com/en_pv/AWSCloudFormation/latest/UserGuide/stacks.html). The stack contains
* a AWS Lambda function that run the bots
* a set of bots

Individual rules within Compliance rulesets have a remedial tag that needs to be set in order to indicate that a remedial bot needs to be triggered for fixing the violation. When the Dome9 compliance engine detects a rule failure during compliance assessment, it will use remedial tag on the rule to decide whether or not to generate a SNS event along with the necessary details of the failed object. 

The Cloud Bot Lambda function is triggered in response to this message. Its execution will run an instance of the remedial bot on the AWS object that has the failure has been reported on. As result, the remedial action is triggered in near real-time after the rule has failed. 

After the bot has fixed the issue, the rule passes in the next run.

## The Bots

Refer to [this](bots/Bots.md) file for a list of the bots. It includes a description of what each one does along with an example of a rule that could be used to trigger it.

## Deployment modes

Cloud Bots can be deployed in a single AWS account or across multiple ones.

### Single-account mode

The default mode is 'single' account. Remediations will be applied to entities in a single account. It follows this workflow:

![single mode](docs/pictures/data-flow.png)

### Multi-account mode

In a multi-account mode, remediations are applied across more than one accounts. Though the Lambda function is deployed in only one account, it uses [cross-account roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html) to run bots in other accounts. It follows this workflow:

![multi mode](docs/pictures/cs2_multi_acct_workflow.png)

# Deployment

## Single-account mode 

Follow these steps for each region in your account in which you want to deploy the bots.

1.  Click [<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://dome9cloudbotsemplatesuseast1.s3.amazonaws.com/template.yml)
    and select the region in which you wish to deploy the stack. This will run a script in the CFT console to deploy the cloud bot stack in the selected region.
2.  In the **Select Template**, click **Next** (no need to make a
    selection)
3.  In the **Parameters** section select the deployment mode, *single*
    or *multi* mode. Enter an email address for SNS notifications in the
    EmailAddress field (optional),then click **Next**
4.  In the **Options** page, click **Next** (no need to make any
    selections)
5.  In the **Review** page, select the options:

`  I acknowledge that AWS CloudFormation might create IAM resources `

`  I acknowledge that AWS CloudFormation might create IAM resources with
custom names. `

6.  Click **Create Change Set**, then **Execute**. The stack will be
    created in your AWS account. It will appear as *dome9CloudBots* in the list of stacks in the CloudFormation console.
7.  Select the stack, and then select the **Outputs** section.
8.  Copy the two ARNs there, *OutputTopicARN* and *InputTopicARN* and
    save them; they will be used to setup the SNS to trigger the bots,
    and the output reporting channel.

## Multi-account mode

For this mode, execute the steps described in the previous section to deploy the bots to only one of your accounts. Then following the steps below in each additional account, to set up the the cross-account roles. 

1. Open a AWS CFT console for the account and execute the steps below
2. On the AWS CFT console for the account, set the ACCOUNT\_MODE environment variable to *multi*.
3. Edit the *trust\_policy.json* file (in the *cross\_account\_role\_configs* folder),to add the account id of the additional account. Then, run the following commands to create the IAM role and policy and a cross-account role in that AWS account:
```
<!-- end list -->
cd cross_account_role_configs
./create_role.sh <aws profile>
```

# Set up your Dome9 account

On Dome9 add remediation tags to rules in a compliance ruleset

## Configure the rules

Follow these steps in your Dome9 account to tag the compliance rules & rulesets to use bots as a remediation step.

1.  In the Dome9 console, navigate to the Rulesets page in the
    Compliance & Governance menu.
2.  Select the rules for which you want to add a remediation step.
3.  In the Compliance Section add a row with the following string:
    `AUTO: <bot-name> <params>` 
    where *bot-name* is the name of the bot, and *params* is a list of arguments for the bot (if any).
    
    For example, `AUTO: ec2_stop_instance` will run the bot to stop an     EC2 instance.

## Configure the Continuous Compliance policy

Once the rules in the ruleset have been tagged for remediation, set up a Continuous Compliance policy to run the ruleset, and send findings to the SNS.

1.  Navigate to the **Policies** page in the Compliance & Governance     menu.
2.  Click **ADD POLICY** (on the right).
3.  Select the account from the list, then click **NEXT**. For 'single' mode, this will be the one account in which 
    the bots are deployed.
    For 'multi' mode, select the accounts (they must be configured with cross-account roles).
4.  Select the ruleset from the list, then click **NEXT**.
5.  Click **ADD NOTIFICATION**.
6.  Select *SNS notification for each new finding as soon as it is discovered*, and enter the ARN for the SNS 
    (*InputTopicARN*, created above). Select option *JSON - Full entity*, and then click **SAVE**.

**Note:** Dome9 will send event messages to the SNS for new findings. To send events for previous findings, follow these steps:

1.  Navigate to the **Policies** page.
2.  Find the ruleset and account in the list, and hover over the right
    of the row, then click on the *Send All Alerts* icon.
    ![](docs/pictures/send_all_events_button.png)
3.  Select the *SNS* Notification Type option, and the Notification
    Policy (the one created above), then click **SEND**. Dome9 will send
    event messages to the SNS for findings.

# Using the Cloud Bots without Dome9 (or in standalone mode)

To use the Cloud Bots without a Dome9 account, you must send messages to the SNS for each event that requires remediation. The message should have the following format:

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

where 
* *account: id* and *accountNumber* is your AWS account number (from AWS)
* *status* is marked *Failed*
* *entity: id* is the id for the entity that failed the rule

# Log Collection for Troubleshooting

Logging is enabled by default for all Cloud Bots. Each bot will send log data to Dome9 for use in troubleshooting. Following the steps below for every AWS account you need to disable logging for

1. Locate and select the Lambda function created by the CFT stack in your AWS account
2. set the environment variable SEND_LOGS to False. 

Note: Each account is controlled by the variable for the Lambda function configured in that account.
