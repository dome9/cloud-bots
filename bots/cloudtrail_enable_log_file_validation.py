"""
## cloudtrail_enable_log_file_validation
What it does: Enable log file validation in cloudTrail
Usage: AUTO: cloudtrail_enable_log_file_validation.py
Limitations: None
Defaults:
"""
from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    # create a cloudTrail session
    cloudTrail_client = boto_session.client('cloudtrail')

    cloudTrail_name = entity['name']

    try:
        result = cloudTrail_client.update_trail(
            Name=cloudTrail_name,
            EnableLogFileValidation=True,
        )
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = "enable log File validation in CloudTrail: %s  \n" % cloudTrail_name

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output
