'''
## ecs_stop
What it does: stops an ecs tasks and ec2 instances which contain the tasks
Usage: AUTO: ecs_stop
Sample GSL: cloudtrail where event.name='RegisterTaskDefinition' and event.status='Success'
Limitations: none

Bot doesn't change services fields, number of required tasks field as well.
Since some tasks can be activated without a service.
Draining the instances related to the tasks prevents the service from creating tasks even if field of required tasks not set to 0.
'''

import boto3
from botocore.exceptions import ClientError


def stop_instance(ecs_client, cluster, instance):
    
    # function will stop an instance by changing it's state to 'Draining'
    
    text_output = ''
    try:
        ecs_client.update_container_instances_state(cluster=cluster, containerInstances=[instance,], status='DRAINING')
        
        text_output = f'Instance {instance} successfully stopped'

    except ClientError as e:

        text_output = f'Unexpected error: {e}\n'
        

    return text_output


def stop_task(ecs_client, cluster, task):

    # function will stop task

    text_output = ''
    try:
        ecs_client.stop_task(cluster=cluster, task=task, reason='Privileged task is dangerous and unnecessary')
        text_output = f'Task {task} successfully stopped'

    except ClientError as e:

        text_output = f'Unexpected error: {e}\n'
        

    return text_output


def run_action(boto_session, rule, entity, params):

    ecs_client = boto_session.client('ecs')
    
    text_output = ''
    
    try:
        role_arn = entity.get('id').split(",")[0]
        
        # check if client has active clusters.
        clusters = ecs_client.list_clusters()['clusterArns']
        
    except ClientError as e:
        return f'Unexpected error: {e}'
    
    if len(clusters) == 0:
        text_output = '0 clusters exist for user. No tasks running!\n'
        return text_output

    for cluster in clusters:
        
        try:
            tasks = ecs_client.list_tasks(cluster=cluster, desiredStatus='RUNNING')['taskArns']

        except ClientError as e:
            return f'Unexpected error: {e}'
       
        # check if client has running tasks.
        if len(tasks) != 0:
            
            for task in tasks:
                described = ecs_client.describe_tasks(cluster=cluster, tasks=[task,])['tasks'][0]
                
                task_definition = described.get('taskDefinitionArn')
                
                # check if task definition of running tasks is secure and if not than task is stopped.
                definition = ecs_client.describe_task_definition(taskDefinition=task_definition)['taskDefinition']
                
                #task defenition considered unsecure if it has privileged permissions role
                if definition.get('executionRoleArn') == role_arn:
                    
                    # if task runs on an instance, instance needs to be stopped so more tasks like that wont be created.
                    if 'EC2' in described.get('launchType'):
                        text_output = stop_instance(ecs_client, cluster, described.get('containerInstanceArn'))

                        if 'error' in text_output:
                            return text_output
                        
                    text_output += stop_task(ecs_client, cluster, task)
                    if 'error' in text_output:
                        return text_output
 

    if text_output == '':
        text_output = 'Running tasks do not exist. Exiting' 
            
    return text_output
