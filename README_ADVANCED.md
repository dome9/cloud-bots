# Supporting docs for initial setup




## CS2 Setup without using the CFT Launch Button

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

