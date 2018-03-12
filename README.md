```
                                                                                    
,---.|                  |    ,---.                          o                   ,--.
|    |    ,---..   .,---|    `---..   .,---.,---.,---..    ,.,---.,---.,---.    ,--'
|    |    |   ||   ||   |        ||   ||   ||---'|     \  / |`---.|   ||        |   
`---'`---'`---'`---'`---'    `---'`---'|---'`---'`      `'  ``---'`---'`        `--'
                                       |                                            
```

# Cloud-Supervisor v2 (CS2)
Auto remediation actions for AWS.

This solution is meant to be used in conjunction with Dome9's Continuous Compliance Engine to remediate issues that are uncovered. 


Table of Contents
=================

* [Overview](#overview)
  * [What is this ?](#what-is-this-)
  * [Why and when would I need it ?](#why-and-when-would-i-need-it-)
  * [How does it work ?](#how-does-it-work-)
* [Setup Steps](#setup-steps)
  * [Outside of Dome9](#outside-of-dome9)
    * [Clone this GitHub project](#clone-this-github-project)
    * [Zip the function](#zip-the-function)
    * [Get the name of a S3 bucket to load the zip into](#Get-the-name=of-a-S3-bucket-to-load-the-zip-into)
    * [Deploy the fucnction via CloudFormation template](#deploy-the-fucnction-via-cloudformation-template)
    * [Get the outputs from the new stack](#get-the-outputs-from-the-new-stack)
    * [OPTIONAL: Set up a subscriber to the SNS output topic](#optional-set-up-a-subscriber-to-the-sns-output-topic)
  * [In Dome9](#in-dome9)
    * [Create a bundle that you want to use for auto remediation\.](#create-a-bundle-that-you-want-to-use-for-auto-remediation)
    * [For all rules that you want to add remediation to, add the remediation tag to the "Compliance Section" of the rule\.](#for-all-rules-that-you-want-to-add-remediation-to-add-the-remediation-tag-to-the-compliance-section-of-the-rule)
      * [Tag Syntax: AUTO: &lt;action\_name&gt;](#tag-syntax-auto-action_name-)
    * [Test this compliance bundle\.](#test-this-compliance-bundle)
    * [Set the Dome9 compliance bundle to run via continuous compliance\.](#set-the-dome9-compliance-bundle-to-run-via-continuous-compliance)
* [Sample Setup Example](#sample-setup-example)
  * [Outside of Dome9](#outside-of-dome9-1)
  * [In Dome9](#in-dome9-1)
* [Actions Reference](#actions-reference)
  * [ec2\_stop\_instance](#ec2_stop_instance)
  * [ec2\_tag\_instance](#ec2_tag_instance)
  * [ec2\_terminate\_instance](#ec2_terminate_instance)
  * [iam\_quarantine\_role](#iam_quarantine_role)
  * [iam\_quarantine\_user](#iam_quarantine_user)
  * [iam\_turn\_on\_password\_policy](#iam_turn_on_password_policy)
  * [s3\_delete\_bucket](#s3_delete_bucket)
  * [s3\_delete\_permissions](#s3_delete_permissions)
  * [sg\_delete](#sg_delete)
  * [sg\_rules\_delete](#sg_rules_delete)
  * [vpc\_turn\_on\_flow\_logs](#vpc_turn_on_flow_logs)
  * [cloudtrail\_enable](#cloudtrail_enable)
  * [s3\_enable\_versioning](#s3_enable_versioning)
  * [ec2\_enable\_detailed\_monitoring](#ec2_enable_detailed_monitoring)

* [Examples](#examples)
  * [Sample output from the remediation function](#sample-output-from-the-remediation-function)
  * [Sample event output from Dome9](#sample-event-output-from-dome9)
* [Adding new actions](#adding-new-actions)
* [Questions / Comments](#questions--comments)




# Overview
## What is this ?
Cloud-Supervisor 2 is an **automatic remediation solution for AWS** built on top of Dome9's Continuous Compliance capabilities

## Why and when would I need it ?
Dome9 Compliance Engine continuously scans the relevant cloud account (AWS,Azure,GCP) for policy violations, and then alert and report.<br/>
For some organizations that is enough. However, at a certain scale and cloud matureness level- organizations prefer to move towards automatic-remediation approach, in which the system takes specific automated remediation actions in regards to specific violations.</br>
This approach could reduce the load from the security operators and drastically reduce the time to resolve security issues.

## How does it work ?
![Data Flow](./pictures/data-flow.png?raw=true "Title")



- Dome9 will scan the accounts on an ongoing basis and send failing rules to SNS
- In the rules, if we want to add remediation, we can add in a "remediation flag" into the compliance section so that the SNS event is tagged with what we want to do. 
- Each remediation action that is tagged correlates to a file in the actions folder of the remediation function. 
- Lambda reads the message tags and looks for a tag that matches AUTO: <anything>
- If any of those AUTO tags match a remediation that we have built out, it'll call that action.
- All of the methods are sending their events to an array called text_output. Once the function is finished working, this array is turned into a string and posted to SNS


# Setup Steps

## Outside of Dome9

### Clone this GitHub project
```bash 
git clone git@github.com:Dome9/cloud-supervisor2.git 
```

### Zip the function
```bash
cd cloud-supervisor2
zip -r -X remediation-function.zip actions/ handle_event.py index.py send_events_and_errors.py 
```

### Get the name of a S3 bucket to load the zip into
The zip will be automicatically uploaded to your S3 bucket before deployment. If you have an S3 bucket already, skip this step and put the bucket name in the command on the next step. 

If you need to create a new bucket:

```bash
aws s3 mb s3://<NEW_BUCKET_NAME>
```

### Deploy the fucnction via CloudFormation template
For YOUR_BUCKET_NAME, put in the name of a bucket that remediation-function.zip can be uploaded to. 
```bash
aws cloudformation package    \
--template-file ./deployment_cft.yaml    \
--output-template-file serverless-output.yaml    \
--s3-bucket <YOUR_BUCKET_NAME>

aws cloudformation deploy \
--template-file ./serverless-output.yaml \
--stack-name lambda-remediations \
--capabilities CAPABILITY_IAM
```

### Get the outputs from the new stack
```bash
aws cloudformation describe-stacks \
--stack-name lambda-remediations \
--query 'Stacks[0].Outputs' \
--output text
```

The output will look like this:
```
ARN for the export logs topic   OutputTopicARN  arn:aws:sns:us-west-2:726853184812:remediationOutput
ARN that Dome9 sends events to  InputTopicARN   arn:aws:sns:us-west-2:726853184812:d9-findings
```
Save these ARNs for the next step and the Dome9 Continuous Compliance setup

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




## In Dome9
See [this section](#in-dome9-1) for sample screenshots of the setup

### Create a bundle that you want to use for auto remediation. 
It's recommended but not required to break remediation actions into their own bundles. 
There is a sample bundle (sample_bundle.json) that can be used as a starting point.
The rule in the sample bundle will remove rules from the default security group if the SG is empty. 

### For all rules that you want to add remediation to, add the remediation tag to the "Compliance Section" of the rule. 

All available remediation actions are in the actions folder. 

#### Tag Syntax: AUTO: <action_name> <params>
    Ex: AUTO: ec2_stop_instance

### Test this compliance bundle. 
Make sure you're getting the results you want and expect

### Set the Dome9 compliance bundle to run via continuous compliance. 
Currently there needs to be a 1 Continuous Compliance bundle per account
Set the output topic as the ARN from the InputTopicARN one we set up
Set the format to be JSON - Full Entity

If you have a subscriber set up for the remediationOutput topic, you'll see this message when you send the SNS test message during setup:
```
-------------------------
ReportTime: 2018-02-04T01:38:05.5899299+00:00
Error: This finding was found in account id 123456789123. The Lambda function is running in account id: 794306781643. Remediations need to be ran from the account there is the issue in.
-------------------------
```
This is alright and means that everything is working properly. 


### NOTE: 
Currently Continuous Compliance sends a 'diff' for the SNS notifications. Because of this, if you have ran the bundle before, only new issues will be sent to SNS. 
If you want to have the first auto-remediation run to include all pre-existing issues, you'll need to clone the bundle and set the new never-ran bundle as the thing that is being tested in the CC config. This works because if it's never ran, then every existing issue is considered 'new' and will be sent to SNS. 
This will be changed in future releases and is being currently worked on. 


### From here, you should be good to go!


# Sample Setup Example
## Outside of Dome9
```
# Clone this GitHub project
[~]$git clone git@github.com:Dome9/cloud-supervisor2.git 
Cloning into 'cloud-supervisor2'...
remote: Counting objects: 390, done.
remote: Compressing objects: 100% (52/52), done.
remote: Total 390 (delta 42), reused 55 (delta 22), pack-reused 315
Receiving objects: 100% (390/390), 640.04 KiB | 0 bytes/s, done.
Resolving deltas: 100% (247/247), done.


# Zip the function
[~]$cd cloud-supervisor2
[cloud-supervisor2]$zip -r -X remediation-function.zip actions/ handle_event.py index.py send_events_and_errors.py 
  adding: actions/ (stored 0%)
  adding: actions/__init__.py (stored 0%)
  adding: actions/ec2_stop_instance.py (deflated 46%)
  adding: actions/ec2_tag_instance.py (deflated 49%)
  adding: actions/ec2_terminate_instance.py (deflated 46%)
  adding: actions/iam_quarantine_role.py (deflated 67%)
  adding: actions/iam_quarantine_user.py (deflated 67%)
  adding: actions/iam_turn_on_password_policy.py (deflated 66%)
  adding: actions/s3_delete_bucket.py (deflated 42%)
  adding: actions/s3_delete_permissions.py (deflated 68%)
  adding: actions/sg_delete.py (deflated 47%)
  adding: actions/sg_rules_delete.py (deflated 71%)
  adding: handle_event.py (deflated 64%)
  adding: index.py (deflated 52%)
  adding: send_events_and_errors.py (deflated 44%)


# Deploy the fucnction via CloudFormation template
[cloud-supervisor2]$aws cloudformation package    \
> --template-file ./deployment_cft.yaml    \
> --output-template-file serverless-output.yaml    \
> --s3-bucket remediationuploadsdome 

Uploading to 87666a89b6af585e6726fd3d2e472a52  9851 / 9851.0  (100.00%)
Successfully packaged artifacts and wrote output template to file serverless-output.yaml.
Execute the following command to deploy the packaged template
aws cloudformation deploy --template-file /Users/ale/cloud-supervisor2/serverless-output.yaml --stack-name <YOUR STACK NAME>


[cloud-supervisor2]$aws cloudformation deploy \
> --template-file ./serverless-output.yaml \
> --stack-name lambda-remediations \
> --capabilities CAPABILITY_IAM 
Waiting for changeset to be created..
Waiting for stack create/update to complete
Successfully created/updated stack - lambda-remediations


# Get the outputs from the new stack
[cloud-supervisor2]$aws cloudformation describe-stacks --stack-name lambda-remediations --query 'Stacks[0].Outputs' --output text 
ARN for the export logs topic   OutputTopicARN  arn:aws:sns:us-west-2:726853184812:remediationOutput
ARN that Dome9 sends events to  InputTopicARN   arn:aws:sns:us-west-2:726853184812:d9-findings


# OPTIONAL: Set up a subscriber to the SNS output topic
[cloud-supervisor2]$aws sns subscribe --topic-arn arn:aws:sns:us-west-2:726853184812:remediationOutput --protocol email --notification-endpoint alex@dome9.com 

{
    "SubscriptionArn": "pending confirmation"
}
```

## In Dome9

- Create a bundle that you want to use for auto remediation. 
![Sample Bundle](./pictures/sample_bundle.png?raw=true "Title")

- Edit the bundle (Edit JSON). 
![Sample Bundle](./pictures/edit_bundle.png?raw=true "Title")

- Paste in the text from sample_bundle.json. 
![Sample Bundle](./pictures/edit_json.png?raw=true "Title")

- For any other rules that you want to create and add remediation to, add the remediation tag to the "Compliance Section" of the rule. 
![Rule Tagging](./pictures/tagging_a_rule.png?raw=true "Title")

- Test this compliance bundle. 
![Sample Report](./pictures/sample_report.png?raw=true "Title")
![Sample Results](./pictures/sample_findings.png?raw=true "Title")

- Set the Dome9 compliance bundle to run via continuous compliance. 
![CC Setup1](./pictures/cc_setup1.png?raw=true "Title")
![CC Setup2](./pictures/cc_setup2.png?raw=true "Title")







# Actions Reference

## All action descriptions have been moved to the action files to ensure that documentation stays up to date


# Examples
 
## Sample output from the remediation function
```
-------------------------
Rule violation found: Remove Unused Security Groups
ID: sg-cbd89fb7 | Name: deletmeSG
Remediation Action: AUTO: DeleteSecurityGroup
Security Group sg-cbd89fb7 successfully deleted
-------------------------

-------------------------
Rule violation found: 'default' Security Groups should not have network policies
ID: sg-32930e4e | Name: default
Remediation Action: AUTO: DeleteSecurityGroupRules
Egress rules to be deleted: []
Ingress rules to be deleted: [{'FromPort': 3
 'IpProtocol': 'tcp'
 'IpRanges': [{'CidrIp': '3.0.0.0/32'}]
 'Ipv6Ranges': []
 'PrefixListIds': []
 'ToPort': 3
 'UserIdGroupPairs': []}]
Security Group sg-32930e4e ingress rules successfully deleted
Security group (id: sg-32930e4e) does not have any outbound rules. Skipping.
-------------------------

-------------------------
Rule violation found: Role should not have permissve policies
ID: AROAIVBJXL6XZI677IDZQ | Name: testremediationrole4
Remediation Action: AUTO: Quarantine_role
IAM deny-all policy exists in this account.
Deny policy attached to role: "testremediationrole4"
-------------------------
```


## Sample event output from Dome9
JSON - Full Entity
```javascript
{
    "Policy": {
        "Name": "Remediation-compliance - full entity",
        "Description": ""
    },
    "Bundle": {
        "Name": "* Remediation bundle",
        "Description": ""
    },
    "ReportTime": "2017-12-23T07:12:16.449Z",
    "Rule": {
        "Name": "Remove Unused Security Groups",
        "Description": "a security group with no attached protected assets. PCI-DSS Section 1.1.6, 1.1.7 Removing Unused Security Groups is the expected outcome of a 6 months firewall review and proper justification for used rules.",
        "Remediation": "Delete Unused Security Groups detected by the Dome9 Report.",
        "ComplianceTags": "PCI-DSS Section 1.1.6| PCI-DSS Section 1.1.7| AUTO: sg_delete",
        "Severity": "High"
    },
    "Status": "Failed",
    "Account": {
        "Id": "621958466464",
        "Vendor": "Aws"
    },
    "Region": "Oregon",
    "Entity": {
        "description": "my description",
        "inboundRules": [],
        ... REDACTED ...
        "id": "sg-d03158ac",
        "type": "SecurityGroup",
        "name": "myTestSG",
        "dome9Id": "2375649",
        "accountNumber": "621958466464",
        "region": "us_west_2",
        "source": "db",
        "tags": []
}
```





# Adding new actions
Any new action that is added just needs to follow the format of the other actions and be put in the action folder. 

Here is a sample from sg_delete. The rule and entity variables that are passed through come from the source SNS message. Params are only passed through if there are any in the tag (ex: AUTO: ec2_tag_instance owner unknown)
```python
import boto3

def run_action(rule,entity,params):
    text_output = str(entity)
    region = entity['region']
    region = region.replace("_","-")
    sg_id = entity['id']
    
    ec2 = boto3.resource('ec2', region_name=region)
    result = ec2.SecurityGroup(sg_id).delete()

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Security Group %s successfully deleted\n" % sg_id

    return text_output 
```


## Questions / Comments
Contact: Alex Corstorphine (alex@dome9.com)
