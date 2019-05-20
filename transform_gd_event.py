'''
Sample required minimum event structure that we're formatting the event to:

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
    "region": "us_west_2",
    "vpc": {
        "id": "vpc-1234"
    }
  }
}
'''
import json
import os

def transform_gd_event(unformatted_message):
    found_action = False
    formatted_message = ""
    text_output = ""
    #Check the OS variables to get the list of what we want to do for the different GD actions
    try:
        gd_actions = json.loads(os.environ['GD_ACTIONS'])

        for gd_finding_type, action in gd_actions.items():
            if unformatted_message["detail"]["type"] == gd_finding_type and "AUTO:" in action:
                text_output = "Found a defined rule for GD finding %s. Continuing\n" % gd_finding_type
                found_action = True
                break    

    except Exception as e:
        text_output = "Unexpected error %s \n Please check the formatting of the GD_ACTIONS env variable in Lambda\n Exiting\n Event:\n %s \n" % (e,unformatted_message["detail"])
        return found_action, text_output, formatted_message
    
    if not found_action:
        print("GuardDuty event found but no bots were defined for the event %s. Skipping.\n Event:\n %s \n" % (unformatted_message["detail"]["type"],unformatted_message["detail"]))
        return found_action, text_output, formatted_message

    try:
        # Make the main structure of the formatted message
        formatted_message = {
            "reportTime": unformatted_message["detail"]["createdAt"],
            "rule": {
                "name": action,
                "complianceTags": action
            },
            "status": "Failed",
            "account": {
                "id": unformatted_message["detail"]["accountId"],
                "vendor": "AWS"
            },
            "entity": {
                "region": unformatted_message["detail"]["region"]
            }
        }

        # Guard Duty has 2 types of resource events - instance and accesskey. We'll conditionally format the message based on the message type
        # Sample resource information is at the bottom of the file

        # Instance type
        if unformatted_message["detail"]["resource"]["resourceType"] == "Instance":
            instance_id = unformatted_message["detail"]["resource"]["instanceDetails"]["instanceId"]
            formatted_message["entity"]["id"] = instance_id

            # Stop trying to parse event/run bot if it's from GD's "Generate Sample Findings"
            if instance_id == "i-99999999":
              text_output = "Guard Duty sample event found. Instance ID from the finding is i-99999999. Skipping\n"
              found_action = False
              return found_action, text_output, formatted_message


            try:
                formatted_message["entity"]["vpc"] = {"id": unformatted_message["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["vpcId"]}
            except:
                print("Instance doesn't have any network interfaces. VPC ID didn't come through in the event so it's not being added.")

            for tag in unformatted_message["detail"]["resource"]["instanceDetails"]["tags"]:
                if tag["key"] == "Name":
                    formatted_message["entity"]["name"] = tag["value"]
                    break                 
            if "name" not in formatted_message["entity"]:
                formatted_message["entity"]["name"] = ""

        # Access Key type
        elif unformatted_message["detail"]["resource"]["resourceType"] == "AccessKey":
            access_key_id = unformatted_message["detail"]["resource"]["accessKeyDetails"]["accessKeyId"]
            formatted_message["entity"]["id"] = access_key_id

            formatted_message["entity"]["name"] = unformatted_message["detail"]["resource"]["accessKeyDetails"]["userName"]

            # Stop trying to parse event/run bot if it's from GD's "Generate Sample Findings"
            if access_key_id == "GeneratedFindingAccessKeyId":
              text_output = "Guard Duty sample event found. Access Key ID from the finding is \"GeneratedFindingAccessKeyId\". Skipping\n"
              found_action = False
              return found_action, text_output, formatted_message


            
        else:
            text_output = "Unknown resource type found: %s. Current known resources are AccessKeys and Instance. Skipping.\n" % unformatted_message["detail"]["resource"]["resourceType"]
            found_action = False
            return found_action, text_output, formatted_message

        text_output = text_output + "Successfully formatted GuardDuty finding and found a corresponding bot\n" 
    except Exception as e:
        text_output = text_output + "Unexpected error: %s. Exiting\n" % e

    return found_action, text_output, formatted_message



'''
Sample available resource properties for Instance:
"resource": {
    "Records": [
      {
        "EventVersion": "1.0",
        "EventSubscriptionArn": "arn:aws:sns:EXAMPLE",
        "EventSource": "aws:sns",
        "Sns": {
          "SignatureVersion": "1",
          "Timestamp": "1970-01-01T00:00:00.000Z",
          "Signature": "EXAMPLE",
          "SigningCertUrl": "EXAMPLE",
          "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
          "Message": {
            "version": "0",
            "id": "f183081b-5200-9f19-96f5-b9d1a6571d68",
            "detail-type": "GuardDuty Finding",
            "source": "aws.guardduty",
            "account": "936643054293",
            "time": "2018-08-06T23:00:00Z",
            "region": "eu-central-1",
            "resources": [],
            "detail": {
              "schemaVersion": "2.0",
              "accountId": "936643054293",
              "region": "eu-central-1",
              "partition": "aws",
              "id": "96b288bbb2e1ce22761022abb085098e",
              "arn": "arn:aws:guardduty:eu-central-1:936643054293:detector/9ab288b99e41606bca925c2b0f576164/finding/96b288bbb2e1ce22761022abb085098e",
              "type": "UnauthorizedAccess:EC2/RDPBruteForce",
              "resource": {
                "resourceType": "Instance",
                "instanceDetails": {
                  "instanceId": "i-028012aee68c13984",
                  "instanceType": "m4.large",
                  "launchTime": "2018-08-06T21:55:57Z",
                  "platform": "windows",
                  "productCodes": [],
                  "iamInstanceProfile": null,
                  "networkInterfaces": [
                    {
                      "ipv6Addresses": [],
                      "networkInterfaceId": "eni-01654d81e52c8ebe2",
                      "privateDnsName": "ip-172-16-0-30.eu-central-1.compute.internal",
                      "privateIpAddress": "172.16.0.30",
                      "privateIpAddresses": [
                        {
                          "privateDnsName": "ip-172-16-0-30.eu-central-1.compute.internal",
                          "privateIpAddress": "172.16.0.30"
                        }
                      ],
                      "subnetId": "subnet-00a157a847f4a305a",
                      "vpcId": "vpc-0ab9824c1455a0272",
                      "securityGroups": [
                        {
                          "groupName": "gdEventGenerator-BasicWindowsSecurityGroup-N6U27Q3D215B",
                          "groupId": "sg-0542d03ff92ddfe72"
                        }
                      ]
                    }
                  ],
                  "tags": [
                    {
                      "key": "aws:cloudformation:stack-id",
                      "value": "arn:aws:cloudformation:eu-central-1:936643054293:stack/gdEventGenerator/615b0e70-99c3-11e8-ab39-503f2ad2e59a"
                    },
                    {
                      "key": "aws:cloudformation:stack-name",
                      "value": "gdEventGenerator"
                    },
                    {
                      "key": "aws:cloudformation:logical-id",
                      "value": "BasicWindowsTarget"
                    },
                    {
                      "key": "Name",
                      "value": "BasicWindowsTarget"
                    }
                  ],
                  "instanceState": "running",
                  "availabilityZone": "eu-central-1a",
                  "imageId": "ami-3204995d",
                  "imageDescription": "Microsoft Windows Server 2012 R2 RTM 64-bit Locale English AMI provided by Amazon"
                }
              },
              "service": {
                "serviceName": "guardduty",
                "detectorId": "9ab288b99e41606bca925c2b0f576164",
                "action": {
                  "actionType": "NETWORK_CONNECTION",
                  "networkConnectionAction": {
                    "connectionDirection": "INBOUND",
                    "remoteIpDetails": {
                      "ipAddressV4": "172.16.0.27",
                      "organization": {
                        "asn": "0",
                        "asnOrg": "",
                        "isp": "",
                        "org": ""
                      },
                      "country": {
                        "countryName": null
                      },
                      "city": {
                        "cityName": ""
                      },
                      "geoLocation": {
                        "lat": 0,
                        "lon": 0
                      }
                    },
                    "remotePortDetails": {
                      "port": 33900,
                      "portName": "Unknown"
                    },
                    "localPortDetails": {
                      "port": 3389,
                      "portName": "RDP"
                    },
                    "protocol": "TCP",
                    "blocked": false
                  }
                },
                "resourceRole": "TARGET",
                "additionalInfo": {},
                "eventFirstSeen": "2018-08-06T22:49:57Z",
                "eventLastSeen": "2018-08-06T22:55:49Z",
                "archived": false,
                "count": 1
              },
              "severity": 2,
              "createdAt": "2018-08-06T22:59:22.179Z",
              "updatedAt": "2018-08-06T22:59:22.179Z",
              "title": "172.16.0.27 is performing RDP brute force attacks against i-028012aee68c13984.",
              "description": "172.16.0.27 is performing RDP brute force attacks against i-028012aee68c13984. Brute force attacks are used to gain unauthorized access to your instance by guessing the RDP password."
            }
          },
            "TestBinary": {
              "Type": "Binary",
              "Value": "TestBinary"
            }
          },
          "Type": "Notification",
          "UnsubscribeUrl": "EXAMPLE",
          "TopicArn": "arn:aws:sns:EXAMPLE",
          "Subject": "TestInvoke"
        }
    ]
  }



///// NEED TO RECONFIRM THIS
Sample resource properties for AccessKey:
    "resource": {
    "resourceType": "AccessKey",
    "accessKeyDetails": {
        "accessKeyId": "GeneratedFindingAccessKeyId",
        "principalId": "GeneratedFindingPrincipalId",
        "userType": "IAMUser",
        "userName": "GeneratedFindingUserName"
    }
'''