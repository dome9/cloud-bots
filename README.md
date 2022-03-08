<p align="center">
<a href="https://cloudbots.dome9.com">
<img width="150" src="cloudbotslogo.svg"> </a>
</p>

<div align="center">
    <h1><a target="_blank" href="https://cloudbots.dome9.com">CloudBots</a> is an automatic remediation solution for public cloud platforms (AWS, <a href="https://github.com/Dome9/cloud-bots-azure" targe="_blank">Azure</a> and <a href="https://github.com/Dome9/cloud-bots-gcp" targe="_blank">GCP</a>)</h1>

</div>

  - [Overview](#overview)
      - [What are CloudGuard CloudBots?](#what-are-dome9-cloudbots)
      - [What does it do?](#what-does-it-do)
      - [How does it work?](#how-does-it-work)
      - [The Bots](#the-bots)
      - [Deployment modes](#deployment-modes)
          - [Single account mode](#single-account-mode)
          - [Multi mode](#multi-mode)
  - [Deploy CloudBots to your AWS
    accounts](#deploy-cloudbots-to-your-aws-accounts)
      - [Setup your AWS account(s) for
        CloudBots](#setup-your-aws-accounts-for-cloudbots)
      - [Deploy for Multi mode](#deploy-for-multi-mode)
      - [Setup your CloudGuard account](#setup-your-dome9-account)
          - [Configure remediations](#configure-remediations)
          - [Configure a Cloudguard Continuous Compliance
            policy](#configure-a-dome9-continuous-compliance-policy)
      - [Use the CloudBots without a CloudGuard
        account](#use-the-cloudbots-without-a-dome9-account)
  - [Log Collection for
    Troubleshooting](#log-collection-for-troubleshooting)
	
# Overview

## What are CloudGuard CloudBots?

Cloud-Bots is an autoremediation solution for AWS, built on top of 
CloudGuard Continuous Compliance capabilities.

They can also be used standalone, without CloudGuard, to remedy issues in AWS
accounts. Details are included how to configure and trigger them.

## What does it do?

You can configure CloudGuard Continuous Compliance to assess your cloud
accounts with rulesets, to continuously check the compliance of your
accounts, and issue reports and findings in near real-time for issues
that are found.

CloudBots extends this by adding an option to trigger an immediate
remediation action on the problematic cloud entity in your account,
directly from the compliance rule that fails. The rule triggers a bot
that runs in your account, that provides a remedy to the issue that
failed the rule.

For example, a rule that checks whether a customer-managed KMS has
rotation enabled, could trigger the bot *kms\_enable\_rotation*, to
enable rotation. Similarly, a rule that checks whether CloudTrail is
enabled could trigger the bot *cloud\_trailenable*, to create and enable
a CloudTrail.

You can also use the CloudBots without CloudGuard, using the same triggers,
but sourced from your application (details for configuring this
included).

## How does it work?

To use CloudGuard cloudbots, you deploy a CFT stack in your AWS account (or
one of your accounts). This stack has the bots, and an AWS Lambda
function that runs the bots.

You also create an SNS in your AWS account, which is triggers the Lambda
function. Finally, to connect a specific compliance rule in a ruleset
with a bot, you add a remediation flag in the rule. If this rule fails
during a compliance assessment, the CloudGuard Compliance Engine will send an
event message to the SNS, with details about the bot to be triggered
(and any parameters that are needed when it is run). This will trigger
the Lambda function, which runs the specified bot on the entity in
question.

The remedial action is triggered in near real-time after the rule fails.
The next time the rule is run the issue should already be remedied, and
the rule should pass.

## The Bots

Refer to [this](bots/Bots.md) file for a list of the bots, what each one
does, and an example of a rule that could be used to trigger it.

## Deployment modes

You can deploy the CloudBots in a single AWS account, or across multiple
AWS accounts.

### Single account mode

The default mode is ‘single’ account. Remediations will be applied to
entities in a single account. It follows this workflow:

![single mode](docs/pictures/data-flow.png)

### Multi mode

In multi-mode, remediations are applied for more than one account. The
lambda function is deployed in only one account, but uses cross-account
roles to run bots in other accounts. It follows this workflow:

![multi mode](docs/pictures/cs2_multi_acct_workflow.png)

# Deploy CloudBots to your AWS accounts

To use the CloudBots, you have to set up your AWS account(s) and, if are
using CloudGuard, your CloudGuard account.

## Setup your AWS account(s) for CloudBots

Follow these steps for each region in your account in which you want to
deploy the bots.

1.  Click
    [<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=dome9CloudBots&templateURL=https://dome9cloudbotsemplatesuseast1.s3.amazonaws.com/template.yml),
    and select the region in which to deploy the stack. This
    will run a script in the CFT console to deploy the cloudbot stack in
    the selected region.
2.  In the **Select Template**, click **Next** (no need to make a
    selection)
3.  In the **Parameters** section select the deployment mode, *single*
    or *multi* mode. Enter an email address for SNS notifications in the
    EmailAddress field (optional),then click **Next**
4.  In the **Options** page, click **Next** (no need to make any
    selections)
5.  In the **Review** page, select the options:

`I acknowledge that AWS CloudFormation might create IAM resources`

`I acknowledge that AWS CloudFormation might create IAM resources with
custom names.`

6.  Click **Create Change Set**, then **Execute**. The stack will be
    created in your AWS account. It will appear as *dome9CloudBots* in
    the list of stacks in the CloudFormation console.
7.  Select the stack, and then select the **Outputs** section.
8.  Copy the two ARNs there, *OutputTopicARN* and *InputTopicARN* and
    save them; they will be used to setup the SNS to trigger the bots,
    and the output reporting channel.

## Deploy for Multi mode

For multi-mode, you will setup one account as above for the single mode,
and then set up cross account roles in each additional account.

On the AWS CFT console, for your account, perform these steps:

1.  Set the ACCOUNT\_MODE environment variable to *multi*.
2.  Edit the *trust\_policy.json* file (in the
    *cross\_account\_role\_configs* folder),to add the account id of the
    additional account. Then, run the following commands:

<!-- end list -->

    cd cross_account_role_configs
    ./create_role.sh <aws profile>

This script will create the IAM role and policy and the cross-account
role for the additional account.

## Setup your CloudGuard account

On CloudGuard you define remediations, which will apply to selected rules in
rulesets, and, optionally, for selected cloud accounts.

### Configure remediations

You can add a remediation for a specific rule in a ruleset or for all rules in a ruleset. You limit a remediation to specific environments, entities, or environments and entities.

<b> To add a remediation for a specific rule: </b>

1. Navigate to the Rulesets page in the Posture Management menu.

2. Open the ruleset that contains the rule to which you want to apply a remediation.

3. Use the Filter and Search toolbar to find the rule.

4. Click Add to add a predefined CloudBot recommended by CloudGuard. If no recommendation exists, click Add CloudBot to create a new custom CloudBot and add it.
The Edit Remediation window opens with the selected rule and ruleset.

5. Select the remediation parameters. You can combine the options, so the remediation applies to the combination of all the selected options.

	a. Environment that applies the remediation to rules in the selected ruleset only when the ruleset is applied to the selected environments.

	b. Entity, by its entity ID (optional, if missing, all entities are implied); this selects all rules that contain the selected entities

6. For rules with a recommended remediation, the CloudBot appears in the field. For rules without recommendations, select the CloudBot from the list. If the CloudBot is not in the list, select Custom, and then add the name of the CloudBot, along with the runtime arguments. The CloudBot must be deployed in the selected environment, in the same folder as the other bots.

7. Add a comment (mandatory field) and click Save.

<b> To add a remediation for all rules in a ruleset: </b>

1. Navigate to the Remediation page in the Posture Management menu.

2. Click Create New Remediation, in the upper right.

3. Select the rules for which the remediation applies, from the given options. You can combine the options, so the remediation applies to the combination of all the selected options.

	a. a Ruleset (mandatory)

	b. a specific Rule in the ruleset (optional, if missing, all rules are implied)

	c. a specific Environment that applies the remediation to rules in the selected ruleset only when the ruleset is applied to the selected environments.

	d. a specific Entity, by its entity ID (optional, if missing, all entities are implied); this selects all rules involving the selected entities

4. Select the CloudBot, from the list. If the CloudBot is not in the list, select Custom, and then add the name of the CloudBot, along with the runtime arguments. The CloudBot must be deployed in the selected environment, in the same folder as the other bots.

5. Add a comment (mandatory) and click Save.


### Configure a CloudGuard Continuous Compliance policy

Once the rules in the ruleset have been tagged for remediation, set up a
Continuous Compliance policy to run the ruleset, and send findings to
the SNS.

1.  Navigate to the **Compliance Policies** page in the **Posture
    Management** menu.
2.  Click **ADD POLICY** (on the right).
3.  Select the account from the list, then click **NEXT**. For ‘single’
    mode, this will be the one account in which the bots are deployed.
    For ‘multi’ mode, select the accounts (they must be configured with
    cross-account roles).
4.  Select the ruleset from the list, then click **NEXT**.
5.  Click **ADD NOTIFICATION**.
6.  Select *SNS notification for each new finding as soon as it is
    discovered*, and enter the ARN for the SNS (*InputTopicARN*, created
    above). Select option *JSON - Full entity*, and then click **SAVE**.

**Note:** CloudGuard will send event messages to the SNS for new findings. To
send events for previous findings, follow these steps:

1.  Navigate to the **Compliance Policies** page.
2.  Find the ruleset and account in the list, and hover over the right
    of the row, then click on the *Send All Alerts* icon.
    ![](docs/pictures/send_all_events_button.png)
3.  Select the *SNS* Notification Type option, and the Notification
    Policy (the one created above), then click **SEND**. CloudGuard will send
    event messages to the SNS for findings.

## Use the CloudBots without a CloudGuard account

You can use the CloudBots without a CloudGuard account. In this case you must
send messages to the SNS for each event that requires remediation. The
message should have the following format:

    {
      "reportTime": "2018-03-20T05:40:42.043Z",
      "rule": {
        "name": "<name for rule>"
      },
      "status": "Failed",
      "account": {
        "id": "************"
      },
      "entity": {
        "accountNumber": "************",
        "id": "*****************",
        "name": "************",
        "region": "us_west_2",
      }
      "remediationActions":[<bot-name> <param1> <param2>]
    }

where:

*account: id* and *accountNumber* are your AWS account number (from AWS)

*status* is marked *Failed*

*entity: id* is the id (arn) for the entity that failed the rule

NOTE: If the bot requires other properties of the entity, add them to the entity section.

# Update CloudBots

The CloudBots set of bots is continually being updated with new bots. To update your deployment, re-launch the CFT stack.

Via AWS console: Go to CloudFormation and choose the dome9CloudBots stack -> Update stack -> Replace current template -> Enter the following s3 url: https://dome9cloudbotsemplatesuseast1.s3.amazonaws.com/template.yml

Or click 
    [<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/update?stackName=dome9CloudBots&templateURL=https://dome9cloudbotsemplatesuseast1.s3.amazonaws.com/template.yml),
    and select the region in which the stack is currently deployed.

This link will update your existing stack with the most new cloudbots and the cloudbots remediation role.

# Log Collection for Troubleshooting

The CloudBots send log information to CloudGuard, that is used for
troubleshooting. By default, this is enabled for all bots. You can
disable this in your AWS account. Select the Lambda function created by
the CFT stack, and set the environment variable SEND\_LOGS to False.
This will apply to all bots in the account.

Each account is controlled by the variable for the Lambda function
configured in that account.
