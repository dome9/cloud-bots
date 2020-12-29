'''
## lambda_detach_external_layer
Log.ic bot only
What it does: Detaches a layer version from a lambda function if it was added from an external account.
Usage: AUTO: lambda_detach_external_layer
Limitations: The bot will stop running if the proper 'UpdateFunctionConfiguration20150331v2' event is not found.
'''

import boto3
import bots_utils
import botocore.exceptions
import json

LAYER_NAME_PLACEMENT = 6
EVENT_NAME = 'UpdateFunctionConfiguration20150331v2'


def run_action(boto_session, rule, entity, params):
    text_output = ''
    lambda_function_name = entity.get('name')

    # Search for event in cloudtrail
    event = bots_utils.cloudtrail_event_lookup(boto_session, entity, EVENT_NAME,
                                               resource_name_to_filter=lambda_function_name)

    if not event:
        # If no cloud trail event found - do not run bot
        text_output = f'Error: No matching \'{EVENT_NAME}\' events were found in cloud trail. Bot wasn\'t executed'

    else:
        try:
            # Event found - get layer name
            layer_name = get_details_from_event(event)
        except:
            text_output = f'Error while parsing {EVENT_NAME} event. bot wasn\'t executed.'
        else:
            # If event was parsed successfully - detach the layer from the lambda function
            text_output = detach_layer_from_lambda(boto_session, lambda_function_name, layer_name)

    return text_output


def detach_layer_from_lambda(boto_session, lambda_function_name, layer_name_to_delete):
    lambda_client = boto_session.client('lambda')
    # Getting lambda's current layers
    try:
        current_layers = lambda_client.get_function(FunctionName=lambda_function_name)['Configuration']['Layers']
    except KeyError:
        return f'Error: the lambda function ({lambda_function_name}) has no layers attached to it'
    except botocore.exceptions.ClientError as e:
        return f'Client error: {e}'

    # Remove the layer specified in the event from the layers list
    try:
        layer_item_to_delete = next((layer for layer in current_layers if layer_name_to_delete in layer.get('Arn')))
    except StopIteration:
        return 'Error: Layer to detach doesn\'t exist or was already detached'
    else:
        current_layers.remove(layer_item_to_delete)

    # Creating list of updated layers in the correct format
    updated_layers = [layer.get('Arn') for layer in current_layers]

    # Updating function's layers list
    try:
        lambda_client.update_function_configuration(FunctionName=lambda_function_name,
                                                    Layers=updated_layers)
    except botocore.exceptions.ClientError as e:
        return f'Client error: {e}'

    return f'Success: Layer ({layer_name_to_delete}) was successfully' \
           f' detached from lambda function ({lambda_function_name})'


def get_details_from_event(event):
    layer_arn = json.loads(event['CloudTrailEvent'])['requestParameters']['layers'][-1]
    # Parse layer arn to get layer name
    return layer_arn.split(sep=':')[LAYER_NAME_PLACEMENT]
