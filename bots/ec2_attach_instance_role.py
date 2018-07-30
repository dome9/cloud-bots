'''
ec2_attach_instance_role
What it does: Attaches an instance role to an EC2 instance. This role needs be passed in through the params. 
Usage: AUTO: ec2_update_instance_role role_arn=<role_arn>

If you have a role that is the same across accounts, and don't want to pass in an account specific ARN, add "$ACCOUNT_ID" to the role ARN and the function will automatically pull in the current account ID of the finding. 
Example: AUTO: ec2_update_instance_role role_arn=arn:aws:iam::$ACCOUNT_ID:instance-profile/ec2SSM
'''

import boto38
from botocore.exceptions import ClientError
 
def run_action(boto_session,rule,entity,params):
    instance_id = entity['id']
    text_output = ""

    ec2_client = boto_session.client('ec2')   

    ## Set up params. We need a role ARN to come through in the params.
    usage = "Usage: AUTO: ec2_update_instance_role role_arn=<role_arn>\n Example: AUTO: ec2_update_instance_role role_arn=arn:aws:iam::621958466464:role/ec2Alexa\n"
    if len(params) == 1:
        try:
            key_value = params[0].split("=")
            key = key_value[0]
            value = key_value[1]

            if key == "role_arn":     
                # Look for "$ACCOUNT_ID" and replace it with the current account number
                account_id = entity['accountNumber']
                role_arn = value.replace("$ACCOUNT_ID", account_id)
                text_output = text_output + "Role ARN that we're attaching to the instance: %s \n" % role_arn

            else:
                text_output = text_output + "Params don't match expected values. Exiting.\n" + usage
                return text_output  

        except:
            text_output = text_output + "Params handling error. Please check params and try again.\n" + usage
            return text_output

    else:
        text_output = "Wrong amount of params inputs detected. Exiting.\n" + usage
        return text_output

    # If the instance has an instance profile, try to update the role to have the new policy attached. It it's already attached, it'll still return a 200 so no need to worry about too much error handling. 
    if len(entity['roles']) == 0 :  
        try:
            result = ec2_client.associate_iam_instance_profile(
                IamInstanceProfile={
                    'Arn': role_arn,
                    'Name': role_arn.split("/")[1]
                },
                InstanceId=instance_id
            )

            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                text_output = text_output + "Unexpected error: %s \n" % str(result)
            else:
                text_output = text_output + "Role successfully attached to instance\n"

        except ClientError as e:
            text_output = text_output + "Unexpected error: %s \n" % e

    else:
        text_output = "Instance already has an instance role attached.\nExiting\n"

    return text_output


