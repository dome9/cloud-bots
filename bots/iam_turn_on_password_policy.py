"""
## iam_turn_on_password_policy
What it does: Sets all settings in an account password policy
Usage: AUTO: iam_turn_on_password_policy MinimumPasswordLength:<int> RequireSymbols:<True/False> RequireNumbers:<True/False> RequireUppercaseCharacters:<True/False>  RequireLowercaseCharacters:<True/False> AllowUsersToChangePassword:<True/False>  MaxPasswordAge:<int> PasswordReusePrevention:<int> HardExpiry:<True/False>
Limitations: ALL variables need to be set at the same time

Sample PasswordPolicy:
{
   MinimumPasswordLength=int - any number from 6 to 128,
   RequireSymbols=True|False,
   RequireNumbers=True|False,
   RequireUppercaseCharacters=True|False,
   RequireLowercaseCharacters=True|False,
   AllowUsersToChangePassword=True|False,
   MaxPasswordAge=int,
   PasswordReusePrevention=int - any number from 1 to 24, inclusive,
   HardExpiry=True|False
}
more information - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html
Sample tag: AUTO: iam_turn_on_password_policy MinimumPasswordLength:15 RequireSymbols:True RequireNumbers:True RequireUppercaseCharacters:True RequireLowercaseCharacters:True AllowUsersToChangePassword:True MaxPasswordAge:5 PasswordReusePrevention:5 HardExpiry:True
"""
from botocore.exceptions import ClientError

PROPERTIES = ['MinimumPasswordLength', 'RequireSymbols', 'RequireNumbers', 'RequireUppercaseCharacters',
              'RequireLowercaseCharacters', 'AllowUsersToChangePassword', 'MaxPasswordAge', 'PasswordReusePrevention',
              'HardExpiry']


def run_action(boto_session, rule, entity, params):
    # Create IAM client
    iam_client = boto_session.client('iam')

    if len(params) != 9:  # We need to make sure we have the exact amount of values for all of these properties.
        text_output = "Array length is not equal to 9. Are you sure ALL password policy properties were set? \n " \
                      "MinimumPasswordLength=int, \n RequireSymbols=True|False, \n RequireNumbers=True|False, " \
                      "\n RequireUppercaseCharacters=True|False, \n RequireLowercaseCharacters=True|False, " \
                      "\n AllowUsersToChangePassword=True|False, \n MaxPasswordAge=int, \n PasswordReusePrevention=int, " \
                      "\n HardExpiry=True|False \n "
        return text_output

    password_config = {}

    try:
        # Parse all the values from the params and match them to their values
        for index, policy_config in enumerate(params):
            property_to_update = PROPERTIES[index]
            if ':' in policy_config:  # if params if from auto
                value = policy_config.split(":")[1]
            else:
                value = policy_config
            password_config[property_to_update] = string_to_value(property_to_update, value)

        iam_client.update_account_password_policy(
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

        text_output = "Account Password Policy updated successfully \n"

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


def string_to_value(property_to_update, value):
    # classify the values into int or bool depending on what is needed.
    if property_to_update in ("MinimumPasswordLength", "MaxPasswordAge", "PasswordReusePrevention"):
        value = int(value)
    else:
        if value == 'True' or 'true':
            value = True
        elif value == 'False' or 'true':
            value = False
    return value
