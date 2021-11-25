"""
## route53domain_enable_transfer_lock
What it does: Sets the transfer lock on the domain. The bot will return the operation ID of the request, which can be used in order to track the operation status
by the GetOperationDetail. For more details: https://docs.aws.amazon.com/Route53/latest/APIReference/API_domains_GetOperationDetail.html
Usage: AUTO route53domain_enable_transfer_lock
Permissions: route53domains:EnableDomainTransferLock
"""


def run_action(boto_session, rule, entity, params):
    domain = entity['name']
    client = boto_session.client('route53domains', region_name='us-east-1')

    print(f'{__file__} - Trying to set transfer lock for {domain}... \n')
    result = client.enable_domain_transfer_lock(DomainName=domain)
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        raise ValueError("Unexpected error: %s \n" % str(result))
    else:
        print(f'{__file__} - Done. \n')
        operation_id = result['OperationId']
        text_output = f'Successfully enabled transfer-lock for the domain: {domain}. You can use the following operation id: {operation_id} to track the progress' \
                      f' and completion of the action.\n'

    return text_output
