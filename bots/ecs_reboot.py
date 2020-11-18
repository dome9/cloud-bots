'''
## ecs_reboot
What it does: stops an ecs task and the service (which started the task) will create it again and run it.
Usage: AUTO: ecs_reboot

Sample GSL: ecs should have tasks running
'''

import boto3
from botocore.exceptions import ClientError
import boto3.session


def stop_task(ecs_client, cluster, task):

    text_output = ''
    try:
        result = ecs_client.stop_task(cluster=cluster, task=task, reason='Privileged task is dangerous and unnecessary')
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = 'Unexpected error: %s \n' % str(result)
        else:
            text_output = 'Task %s successfully stopped \n' % str(task)

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output


def run_action(boto_session,rule,entity,params):
    role_arn = entity['id']
    ecs_client = boto_session.client('ecs')

    text_output = ''

    # check if client has active clusters.
    clusters = ecs_client.list_clusters()['clusterArns']
    if len(clusters) == 0:
        text_output = '0 clusters exist for user. No tasks running!\n'
        return text_output

    for cluster in clusters:

        tasks = ecs_client.list_tasks(cluster=cluster, desiredStatus='RUNNING')['taskArns']

        # check if client has running tasks.
        if len(tasks) != 0:

            for task in tasks:
                described = ecs_client.describe_tasks(cluster=cluster, tasks=[task, ])['tasks'][0]
                task_defenition = described['taskDefinitionArn']

                # check if task defenition of running tasks is secure and if not than task is stopped.
                defenition = ecs_client.describe_task_definition(taskDefinition=task_defenition)['taskDefinition']

                if defenition['executionRoleArn'] == role_arn:

                    text_output = stop_task(ecs_client, cluster, task)
                    if text_output.find('error') != -1:
                        return text_output

                    print(text_output)

    if text_output == '':
        text_output = 'Running tasks do not exist.\nExiting\n'

    return text_output
    session = boto3.Session(
        aws_access_key_id='AKIA6BANX7CAHHWPALPD',
        aws_secret_access_key='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',
        region_name='us-east-2'
    )

    text = run_action(session, '', {'role':'arn:aws:iam::964248991872:role/ecsTaskExecutionRole'},
                      ['role_arn=arn:aws:iam::964248991872:instance-profile/admin-ec2'])
    print(text)