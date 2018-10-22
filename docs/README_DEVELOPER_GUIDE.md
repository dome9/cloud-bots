# Developer Guide
The goal of this is to provide a guide for understanding how CloudBots works from a code perspective and what is needed to add your own bots

# How it works

## High level
- Dome9 will scan the accounts on an ongoing basis and send failing rules to SNS
- In the rules, if we want to add remediation, we can add in a "remediation flag" into the compliance section so that the SNS event is tagged with what we want to do. 
- Each remediation bot that is tagged correlates to a file in the bots folder of the remediation function. 
- Lambda reads the message tags and looks for a tag that matches AUTO: <anything>
- If any of those AUTO tags match a remediation that we have built out, it'll call that bot.
- All of the methods are sending their events to an array called text_output. Once the function is finished working, this array is turned into a string and posted to SNS

## Data flow:
Index > handle_event > bot/<action> > handle_event > index > send_events_and_errors

## Index
text_output is a log of the events that are occurring during the function run. Throughout all the files, it's an array that is appended to. At the end of the function run, the array is turned into a string and sent to SNS for logging. 

## Handle_event
Handle_event is the cornerstone of CloudBots because it takes the events in from Dome9 and routes the events to the right function. 

If the event is "passing" or there's no remediation tag, it skips the event. 

If the event occurs in a different account than the one that the function is running in, it'll take care of the assume_role to the other account (if the deployment mode is set to multi)

If the event contains a bot that we want to call, it will look for the corresponding file in the bots/ folder and invoke the bot.

## Bots

### Sample event
```javascript
{
  "policy": {
    "name": "unknown user testing",
    "description": ""
  },
  "bundle": {
    "name": "6",
    "description": ""
  },
  "reportTime": "2018-03-20T05:40:42.043Z",
  "rule": {
    "name": "Instance should fail",
    "description": "",
    "remediation": "",
    "complianceTags": "AUTO: tag_ec2_resource myKey myValue",
    "severity": "High"
  },
  "status": "Failed",
  "account": {
    "id": "621958466464",
    "vendor": "Aws"
  },
  "region": "Oregon",
  "entity": {
    "image": "ami-d874e0a0",
    "kernelId": null,
    "platform": "linux",
    "launchTime": 1521238615,
    "isPublic": false,
    "instanceType": "t2.micro",
    "isRunning": false,
    "id": "i-0028f9751d334c93a",
    "type": "Instance",
    "name": "",
    "dome9Id": "",
    "accountNumber": "621958466464",
    "region": "us_west_2",
    "source": "db",
    "tags": []
  }
}
```

### Required event structure
Here is the minimum information that CloudBots needs to run:
```javascript
{
  "reportTime": "2018-03-20T05:40:42.043Z",
  "rule": {
    "name": "Instance should fail",
    "complianceTags": "AUTO: tag_ec2_resource myKey myValue"
  },
  "status": "Failed",
  "account": {
    "id": "621958466464"
  },
  "entity": {
    "id": "i-0028f9751d334c93a",
    "name": "TestInstance",
    "region": "us_west_2"
  }
}
```

### Sample bot
```python
import boto3 #Required

### Turn off EC2 instance ###
def run_action(boto_session,rule,entity,params): 
# run_action is the main function that handle_event will trigger
# boto_session contains the session credentials and region (set in handle_event). 
# rule is from the rule object above
# entity is from the entity object above
# params is from rule > Compliance tags and is the remaining text after AUTO: <bot>. 
#   Example: "AUTO: tag_ec2_resource myKey myValue"
#   Params would be ["myKey", "myValue"]

    instance = entity['id']
    ec2_client = boto_session.client('ec2')
    # boto_session comes from handle_event
    
    result = ec2_client.stop_instances(InstanceIds=[instance])

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error: %s \n" % str(result)
    else:
        text_output = "Instance stopped: %s \n" % instance

    # text_output is a string of the function log output. If multiple logs need to be added, append it to the end of the string with a newline.
    # Example:
    # text_output = "myfirstlogline\n"
    # text_output = text_output + "mysecondlogline\n"

    return text_output 
```

### Calling the new bot
Once you create the new bot, put the file in the bots directory. Handle_event will automatically pick it up and try to call it if the bot is defined in the event. 