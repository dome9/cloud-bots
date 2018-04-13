### Delete IGW
# From the boto3 docs: The VPC must not contain any running instances with Elastic IP addresses or public IPv4 addresses.
# Because of this, all instances with a public IP will be turned off in the VPC before the IGW can be detached

# Limitations: 
# VPCs have lots of interconnected services. This is currently just focused on EC2 but future enhancements will need to be made to turn off RDS, Redshift, etc. 

import boto3  
from time import sleep
from botocore.exceptions import ClientError


def run_action(boto_session,rule,entity,params):
    vpc_id = entity['id']
    igw_id = entity['internetGateways'][0]['externalId']

    ec2_resource = boto_session.resource('ec2')    
    ec2_client = boto_session.client('ec2')

    try:
        #Check the region for instances in the VPC that was specified
        text_output = "Checking the VPC for instances with public IPs. These need to be turned off before the IGW is detached.\n"
        result = ec2_client.describe_instances(
            Filters=[{
                    'Name': 'vpc-id',
                    'Values':[vpc_id]
                }]
            )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)

        # Look through all the reservations for the instances with public IPs. Put all the instance IDs into an array
        instances_to_turn_off=[]
        for reservation in result["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance['InstanceId']
                for interface in instance['NetworkInterfaces']:
                    for ips in interface['PrivateIpAddresses']:
                        try:
                            print(ips['Association']['PublicIp'])
                            print(instance_id)
                            instances_to_turn_off.append(instance_id)
                        except:
                            continue

        if instances_to_turn_off:
            print("turning instances off")
            result = ec2_client.stop_instances(InstanceIds=instances_to_turn_off)

            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s \n" % str(result)
                return text_output
            else:
                instances = ' '.join(instances_to_turn_off)
                text_output = text_output + "Instances that are being stopped: %s \n" % instances
        
                instance = ec2_resource.Instance(instances_to_turn_off[0])
                while instance.state['Name'] not in 'stopped':
                    print("Sleeping while waiting for instances to turn off (usually about 45 seconds)")
                    sleep(5)
                    instance.load()
                print("Instances are fully shut down. Continuing")

        else:
            text_output = text_output + "No instances in this VPC that have public IPs. Trying to remove the IGW next.\n"

        #Detach the IGW
        response = ec2_client.detach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
            )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
            return text_output
        else:
            text_output = text_output + "IGW detached on VPC %s \n" % vpc_id


        #Delete the IGW
        response = ec2_client.delete_internet_gateway(InternetGatewayId=igw_id)

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = text_output + "Unexpected error: %s \n" % str(result)
            return text_output
        else:
            text_output = text_output + "IGW deleted %s \n" % igw_id


    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output 