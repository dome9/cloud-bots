'''
## iam_turn_on_password_policy
What it does: Sets all settings in an account password policy  
Usage: AUTO: iam_turn_on_password_policy MinimumPasswordLength:<int> RequireSymbols:<True/False> RequireNumbers:<True/False>  RequireUppercaseCharacters:<True/False>  RequireLowercaseCharacters:<True/False>  AllowUsersToChangePassword:<True/False>  MaxPasswordAge:<int> PasswordReusePrevention:<int> HardExpiry:<True/False>   
Limitations: ALL variables need to be set at the same time  

Sample PasswordPolicy:
{
   MinimumPasswordLength=int,
   RequireSymbols=True|False,
   RequireNumbers=True|False,
   RequireUppercaseCharacters=True|False,
   RequireLowercaseCharacters=True|False,
   AllowUsersToChangePassword=True|False,
   MaxPasswordAge=int,
   PasswordReusePrevention=int,
   HardExpiry=True|False
}

Sample tag: AUTO: iam_turn_on_password_policy MinimumPasswordLength:15 RequireSymbols:True RequireNumbers:True RequireUppercaseCharacters:True RequireLowercaseCharacters:True AllowUsersToChangePassword:True MaxPasswordAge:5 PasswordReusePrevention:5 HardExpiry:True
'''

import boto3

def run_action(rule,entity,params):
    # Create IAM client
    iam = boto3.client('iam')

    if len(params) != 9: #We need to make sure we have the exact amount of values for all of these properties.
        text_output = "Array length is not equal to 9. Are you sure ALL passwort policy properties were set?\n MinimumPasswordLength=int, \nRequireSymbols=True|False, \nRequireNumbers=True|False, \nRequireUppercaseCharacters=True|False, \nRequireLowercaseCharacters=True|False, \nAllowUsersToChangePassword=True|False, \nMaxPasswordAge=int, \nPasswordReusePrevention=int, \nHardExpiry=True|False \n"
        return text_output

    password_config = {}

    #Parse all the values from the params and match them to their values
    for policy_config in params:
        key_value = policy_config.split(":") 
        property_to_update = key_value[0]
        value = key_value[1]

        #classify the values into int or bool depending on what is needed.
        if property_to_update in ("MinimumPasswordLength", "MaxPasswordAge", "PasswordReusePrevention"):
            value = int(value)
        else:
            if value == 'True':
                value = True
            elif value == 'False':
                value = False

        password_config[property_to_update] = value


    result = iam.update_account_password_policy(
        MinimumPasswordLength=password_config["MinimumPasswordLength"],
        RequireSymbols=password_config["RequireSymbols"],
        RequireNumbers=password_config["RequireNumbers"],
        RequireUppercaseCharacters=password_config["RequireUppercaseCharacters"],
        RequireLowercaseCharacters=password_config["RequireLowercaseCharacters"],
        AllowUsersToChangePassword=password_config["AllowUsersToChangePassword"],
        MaxPasswordAge=password_config["MaxPasswordAge"],
        PasswordReusePrevention=password_config["PasswordReusePrevention"],
        HardExpiry=password_config["HardExpiry"]
    )

    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        text_output = "Unexpected error:" + str(result) + "\n"
    else:
        text_output = "Account Password Policy updated successfully \n" 

    return text_output
