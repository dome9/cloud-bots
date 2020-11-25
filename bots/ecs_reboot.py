'''
## ecs_reboot
What it does: stops an ecs task and the service (which started the task) will create it again and run it.
Usage: AUTO: ecs_reboot

Sample GSL: ecs should have tasks running
'''

import boto3
from botocore.exceptions import ClientError


def stop_task(ecs_client, cluster, task):

    # function will stop task

    text_output = ''
    try:
        ecs_client.stop_task(cluster=cluster, task=task, reason='Privileged task is dangerous and unnecessary')
        text_output = f'Task {task} successfully stopped \n'

    except ClientError as e:

        text_output = f'Unexpected error: {e}\n'
        if 'ResponseMetadata' in e.response and 'HTTPStatusCode' in e.response['ResponseMetadata']:
            text_output += f"error code: {e.response['ResponseMetadata']['HTTPStatusCode']}\n"

    return text_output


def run_action(boto_session, rule, entity, params):

    role_arn = entity.get('id')
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
                task_definition = described.get('taskDefinitionArn')

                # check if task definition of running tasks is secure and if not than task is stopped.
                definition = ecs_client.describe_task_definition(taskDefinition=task_definition)['taskDefinition']

                if definition.get('executionRoleArn') == role_arn:

                    text_output = stop_task(ecs_client, cluster, task)
                    if text_output.find('error') != -1:
                        return text_output
                    print(text_output)

    if text_output == '':
        text_output = 'Running tasks do not exist.\nExiting\n'

    return text_output
