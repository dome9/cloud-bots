"""
## sns_set_topic_private
# What it does: set sns topic to private
# Usage:sns_set_topic_private policy<class str>policy
# Examples:
"""
import boto3
import json
from botocore.exceptions import ClientError


def check_policy(policy_string):
    policy_string = policy_string.strip()
    try:
        # check if the policy in json format.
        # if it's not in valid json format it will throw error.
        policy = json.loads(policy_string)

        for statement in policy['Statement']:
            # check if statement has Effect='Allow' and Principal='*'.
            statement_str = json.dumps(statement).replace(' ', '')
            if '"Effect":"Allow"' in statement_str and '"Principal":{"AWS":"*"}' in statement_str:
                return f"Invalid Statement, can't use Effect='Allow' and Principal='*'\n{statement}"

            # check if policy Statement has Condition block.
            if "Condition" not in statement.keys():
                return f"Invalid policy, has no Condition block\n{statement}"

        # pass al checks
        return True

    except:
        return "invalid Json format"


def run_action(session, rule, entity, params):
    topic_arn = entity['topicArn']
    client = session.client('sns')

    if 'policy' in params.keys():
        policy_string = params['policy']
    elif 'Policy' in params.keys():
        policy_string = params['Policy']
    else:
        return "Error, no policy was given to the bot." \
               "Usage: sns_set_topic_private policy=<class str>policy"

    text_output = check_policy(policy_string)
    if text_output is True:
        try:
            client.set_topic_attributes(
                TopicArn=topic_arn,
                AttributeName='Policy',
                AttributeValue=params['policy']
            )
            text_output = f"Updated topic policy {topic_arn}"

        except ClientError as error:
            text_output = f"Unexpected error, {error}"

    return text_output
