'''
## ecs_stop
What it does: stops an ecs tasks and ec2 instances which contain the tasks
Usage: AUTO: ecs_stop

Sample GSL: ecs should have tasks running
'''

import boto3
from botocore.exceptions import ClientError


def stop_instance(ecs_client, cluster, instance):
    #function will stop an instance by changing it's state to 'Draining'
    text_output = ''
    try:
        result = ecs_client.update_container_instances_state(cluster=cluster, containerInstances=[instance,], status='DRAINING')
        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = 'Unexpected error: %s \n' % str(result)
        else:
            text_output = 'Instance %s successfully stopped \n' % str(instance)

    except ClientError as e:
        text_output = 'Unexpected error: %s \n' % e

    return text_output

def stop_task(ecs_client, cluster, task):
    #function will stop task
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

    id = entity['id']
    role_arn = id[:id.find(',')]
    ecs_client = boto_session.client('ecs')
    
    text_output = ''
    
    #check if client has active clusters.
    clusters = ecs_client.list_clusters()['clusterArns']
    if len(clusters) == 0:
        text_output = '0 clusters exist for user. No tasks running!\n'
        return text_output

    for cluster in clusters:
        
        tasks = ecs_client.list_tasks(cluster=cluster, desiredStatus='RUNNING')['taskArns']
       
        #check if client has running tasks.
        if len(tasks) != 0:
            
            for task in tasks:
                described = ecs_client.describe_tasks(cluster=cluster, tasks=[task,])['tasks'][0]
                task_defenition = described['taskDefinitionArn']
                
                #check if task defenition of running tasks is secure and if not than task is stopped.
                defenition = ecs_client.describe_task_definition(taskDefinition=task_defenition)['taskDefinition']
                
                
                if defenition['executionRoleArn'] == role_arn:
                    
                    text_output = stop_task(ecs_client, cluster, task)
                    if text_output.find('error') != -1:
                        return text_output
    
                    print(text_output)
                    #if task runs on an instance, instance needs to be stopped so more tasks like that wont be created.
                    if 'EC2' in defenition['compatibilities']:
                        text_output = stop_instance(ecs_client, cluster, described['containerInstanceArn'])
                        #cant stop instance if more tasks run on it, first all running tasks supposed to be stopped
                        #in case of any other error the programme will stop.
                        if text_output.find('error') != -1 and text_output.find('Found running tasks on the instance') == -1:
                            return text_output
                    print(text_output)

    
    if text_output == '':
        text_output = 'Running tasks do not exist.\nExiting\n' 
            
    return text_output