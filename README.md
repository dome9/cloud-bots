# lambda_remediations
Auto remediation actions

This is meant to be used in conjunction with Dome9's Continuous Compliance to remediate issues that are uncovered. 

## Setup Steps

### Create a bundle that you want to use for auto remediation. 
A sample bundle is in sample_bundle.json

### For all rules that you want to add remediation to, add the remediation tag to the "Compliance Section" of the rule.

Current remediation functions/tags are:
```
"AUTO: DeleteBucket"
"AUTO: DeleteBucketPermissions"
"AUTO: DeleteSecurityGroup"
"AUTO: DeleteSecurityGroupRules"
"AUTO: EC2_tag_instance (key:value)"
"AUTO: EC2_stop_instance"
"AUTO: EC2_terminate_instance"
"AUTO: Quarantine_user"
"AUTO: Quarantine_role"
```

### Test this bundle. 
Make sure you're getting the results you want and expect

### Create 2 new SNS topics
One topic will be for Dome9 to send events to, and the second will be for remediation outputs.
1. Go to SNS and create a new topic. Call it whatever you want (I went with d9-events and remediation-output).

For the D9-events topic:
2. Go into the topic you created and edit the Topic Policy
3. "Allow these users to publish messages to this topic" - select "Only these AWS users" and put in 634729597623 in the text box.
4. Copy down the topic ARNs as we'll use them later

### Create a new IAM policy
Use this policy document.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "lambdaRemediationPermissions",
            "Action": [
				"logs:CreateLogGroup",
				"logs:CreateLogStream",
		                "logs:PutLogEvents",
				"sns:Publish",
				"sts:GetCallerIdentity",
				"iam:CreatePolicy",
				"iam:GetPolicy",
				"iam:CreateGroup",
				"iam:GetGroup",
				"iam:AttachGroupPolicy",
				"iam:AttachRolePolicy",
				"iam:AddUserToGroup",
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
Name it "remediation_actions" and set the SNS topic from the Continuous Compliance step to be the trigger. 
Set the runtime as Python 3.6

### Create a trigger for your function
Set the d9-events SNS topic as the trigger and make sure it's enabled

### Create an environment variable in your function called "SNS_TOPIC_ARN"
Paste in the ARN from the topic we just created in the last step

### Set the handler
Change it from "lambda_function.lambda_handler" to "index.lambda_handler"

### Zip the all_remediations folder and upload it to your function
```
cd all_remediations 
rm function.zip
zip -r -X function.zip *
aws lambda update-function-code --function-name remediation_actions --zip-file fileb://function.zip
```

### Set the Dome9 compliance bundle to run via continuous compliance. 
Currently there needs to be a 1 Continuous Compliance bundle per account
Set the topic as the d9-events one we set up
Set the format to be JSON - Basic Entity

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
## To-do
- Refactor 'filtering_events' to be an object instead of a bunch of IFs

- Refactor quarantine_user and _role. Currently it works but isn't following best practices


## How does it work?
- Dome9 will scan the accounts on an ongoing basis and send failing rules to SNS
- In the rules, if we want to add remediation, we can add in a "remediation flag" into the compliance section so that the SNS event is tagged with what we want to do. 
- In lambda, once the event comes in, we need to read the message and see if there's anything we need to do. Filter messages will take the event and loop through all of the compliance tags on the rule. 
- If any of those tags match a remediation that we have built out, it'll call that function
- All of the methods are sending their events to an array called event_log. Once the function is finished working, this array is turned into a string and posted to SNS
