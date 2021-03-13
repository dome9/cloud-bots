'''
## ecs_deregister_task_definition
What it does: Deregister an ecs task definition revision
Usage: AUTO: ecs_deregister_task_definition
Sample GSL: cloudtrail where event.name='registerTaskDefinition' and event.status='Success'
Limitations: none

Used when overly permissive container definitions created
Example: Logic rule - Unsecured Task Definition Created - Privileged Container
'''

import bots_utils
import ast

EVENT_NAME = 'RegisterTaskDefinition'


def run_action(boto_session, rule, entity, params):
    # look for event in cloudtrail
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME, time_diff=360)
    if event is None:
        print("Could not find any 'Register task definition' event.")

    # Convert event logs from string to dict (json)
    cloud_trail_event = ast.literal_eval(event['CloudTrailEvent'].replace('true', 'True').replace('false', 'False'))
    # retrieve the arn of the new task definition revision
    target = cloud_trail_event['responseElements']['taskDefinition']['taskDefinitionArn']
    # retrieve the privileges of the container definition
    is_priv = cloud_trail_event['responseElements']['taskDefinition']['containerDefinitions'][0]['privileged']

    # check that the task definition has privileged container definition.
    if target and is_priv:
        ecs = boto_session.client('ecs')
        try:
            # deregister the new task definition revision, and make sure the new state in not active
            if ecs.deregister_task_definition(taskDefinition=target).get('taskDefinition').get(
                    'status').lower() != 'active':
                return f'Task definition: {target} was successfully deregistered. You should edit the privileges and then create a new revision.'
            else:
                return 'Task definition revision is still active. Could not deregister the task definition. Try again.'
        except ecs.exceptions.ServerException as e:
            return 'Server Exception, try again. Error is:', str(e)
        except ecs.exceptions.ClientError as e:
            return 'Client Error, try again. Error is:', str(e)
        except Exception as e:
            return 'Unexpected exception: ' + str(e)
    else:
        return 'Task definition does not have privileged container defined.'
