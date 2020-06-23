"""
## cloudtrail_enable_log_file_validation
What it does: Enable log file validation in cloudTrail
Usage: AUTO: cloudtrail_enable_log_file_validation
Limitations: None
"""

from botocore.exceptions import ClientError


def run_action(boto_session, rule, entity, params):
    # create a cloudTrail session
    cloudTrail_client = boto_session.client('cloudtrail')

    cloudTrail = entity['id']

    try:
        cloudTrail_client.update_trail(
            Name=cloudTrail,
            EnableLogFileValidation=True,
        )
        text_output = "Enable log File validation in CloudTrail: %s" % cloudTrail.split('/')[-1]

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output
