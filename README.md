# Cloud-Supervisor v2 (CS2)
Auto remediation actions

This is meant to be used in conjunction with Dome9's Continuous Compliance to remediate issues that are uncovered. 

## Setup Steps

## AWS

### Clone this GitHub project
``` 
git clone git@github.com:Dome9/cloud-supervisor2.git 
```

### Zip the folder and copy it to S3
```
cd cloud-supervisor2
zip -r -X remediation-function.zip *
aws s3 cp remediation-function.zip s3://<YOUR-BUCKET-NAME>/

```

### Update the deployment_cft.yaml file with your file name
Change this line to the path for your bucket/file
```
CodeUri: s3://<YOUR-BUCKET-NAME>/remediation-function.zip
```

### Deploy the template via CloudFormation
```
aws cloudformation package    \
--template-file ./deployment_cft.yaml    \
--output-template-file serverless-output.yaml    \
--s3-bucket <YOUR-BUCKET-NAME>

aws cloudformation deploy \
--template-file ./serverless-output.yaml \
--stack-name lambda-remediations \
--capabilities CAPABILITY_IAM
```

### Get the outputs from the new stack
```
aws cloudformation describe-stacks --stack-name lambda-remediations --query 'Stacks[0].Outputs' --output text
```

### Recommended:
Set up a separate function to send the events to Slack
https://github.com/alpalwal/D9SnsToSlack

From SNS you can send the events wherever you want, but we have found that Slack works great for collaboration as well as troubleshooting. 


## Dome9

### Create a bundle that you want to use for auto remediation. 
It's recommended but not required to break remediation actions into their own bundles. 

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

### NOTE: 
Currently Continuous Compliance sends a 'diff' for the SNS notifications. Because of this, if you have ran the bundle before, only new issues will be sent to SNS. 
If you want to have the first auto-remediation run to include all pre-existing issues, you'll need to clone the bundle and set the new never-ran bundle as the thing that is being tested in the CC config. This works because if it's never ran, then every existing issue is considered 'new' and will be sent to SNS. 
This will be changed in future releases and is being currently worked on. 



## Examples
 
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
