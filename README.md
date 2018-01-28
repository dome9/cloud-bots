# Cloud-Supervisor v2
Auto remediation actions

This is meant to be used in conjunction with Dome9's Continuous Compliance to remediate issues that are uncovered. 

## Setup Steps

### Create a bundle that you want to use for auto remediation. 
It's recommended but not required to break remediation actions into their own bundles. 

### For all rules that you want to add remediation to, add the remediation tag to the "Compliance Section" of the rule. 

All available remediation actions are in the actions folder. 

#### Tag Syntax: AUTO: <action_name> <params>
    Ex: AUTO: ec2_stop_instance

### Test this compliance bundle. 
Make sure you're getting the results you want and expect

### Create 2 new SNS topics
One topic will be for Dome9 to send events to, and the second will be for remediation outputs.
1. Go to SNS and create two new topics. Call it whatever you want (I went with d9-events and remediation-output).

For the d9-events topic:
2. Go into the topic and edit the Topic Policy
3. "Allow these users to publish messages to this topic" - select "Only these AWS users" and put in 634729597623 in the text box.

For both topics: Copy down the topic ARNs as we'll use them later

### Create a new IAM policy
Use this policy document.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "lambdaRemediationPermissions",
            "Action": [
				"sns:Publish",
				"sts:GetCallerIdentity",
				"ec2:TerminateInstances",
				"ec2:StopInstances",
				"ec2:CreateTags",
				"ec2:DeleteSecurityGroup",
				"ec2:DescribeSecurityGroups",
				"ec2:RevokeSecurityGroupEgress",
				"ec2:RevokeSecurityGroupIngress",
				"s3:DeleteBucket",
				"s3:GetBucketPolicy",
				"s3:DeleteBucketPolicy",
				"s3:GetBucketAcl",
				"s3:PutBucketAcl"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```


### Create a new role
And attach the policy from the previous step to it
Call it something like "lambda-d9-remediations"

### Create a new lambda function. 
Name it "remediation_actions" and set the runtime as Python 3.6

### Create a trigger for your function
Set the d9-events SNS topic as the trigger and make sure it's enabled

### Create an environment variable in your function called "SNS_TOPIC_ARN"
Paste in the remediation-output ARN from the topic we just created in the last step

### Set the handler
Change it from "lambda_function.lambda_handler" to "index.lambda_handler"

### Zip the all_remediations folder and upload it to your function
```
zip -r -X remediation_function.zip *
aws lambda update-function-code --function-name remediation_actions --zip-file fileb://remediation_function.zip
```

### Set the Dome9 compliance bundle to run via continuous compliance. 
Currently there needs to be a 1 Continuous Compliance bundle per account
Set the output topic as the d9-events one we set up
Set the format to be JSON - Full Entity

### Recommended:
Set up a separate function to send the events to Slack
https://github.com/alpalwal/D9SnsToSlack

From SNS you can send the events wherever you want, but we have found that Slack works great for collaboration as well as troubleshooting. 

### Sample output from Slack:
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



## How does it work?
- Dome9 will scan the accounts on an ongoing basis and send failing rules to SNS
- In the rules, if we want to add remediation, we can add in a "remediation flag" into the compliance section so that the SNS event is tagged with what we want to do. 
- Each remediation action that is tagged correlates to a file in the actions folder. 
- Lambda reads the message tags and looks for a tag that matches AUTO: <anything>
- If any of those AUTO tags match a remediation that we have built out, it'll call that function
- All of the methods are sending their events to an array called text_output. Once the function is finished working, this array is turned into a string and posted to SNS


## Adding new actions
Any new action that is added just needs to follow the format of the other actions and be put in the action folder. 

Here is a sample from sg_delete. The rule and entity variables that are passed through come from the source SNS message. Params are only passed through if there are any in the tag (ex: AUTO: ec2_tag_instance owner unknown)
```
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



## Sample event output from Dome9
```
JSON - Full Entity

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
        "description": "a",
        "inboundRules": [],
        "outboundRules": [{
            "protocol": "ALL",
            "port": 0,
            "portTo": 0,
            "scope": "0.0.0.0/0",
            "scopeMetaData": null
        }],
        "networkAssetsStats": [{
            "type": "ELBs",
            "count": 0
        }, {
            "type": "instances",
            "count": 0
        },  {
            "type": "ElastiCacheClusters",
            "count": 0
        }],
        "isProtected": false,
        "vpc": {
            "cloudAccountId": "89ff48fc-9c8b-4292-a169-d6e938af2dd2",
            "cidr": "10.0.0.0/16",
            "region": 5,
            "id": "vpc-c037c1b9",
            "accountNumber": "621958466464",
            "vpnGateways": [],
            "internetGateways": [{
                "externalId": "igw-e49a6d82",
                "vpcAttachments": [{
                    "state": "available",
                    "vpcId": "vpc-c037c1b9"
                }],
                "name": ""
            }],
            "dhcpOptionsId": "dopt-b18786d5",
            "instanceTenancy": "default",
            "isDefault": false,
            "state": "available",
            "tags": {},
            "name": "testDeleteMe",
            "source": 1
        },
        "id": "sg-d03158ac",
        "type": "SecurityGroup",
        "name": "myTestSG",
        "dome9Id": "2375649",
        "accountNumber": "621958466464",
        "region": "us_west_2",
        "source": "db",
        "tags": []
    }
}
```