"""
## route53domain_enable_auto_renew
What it does: Configures Amazon Route 53 to automatically renew the specified domain before the domain registration expires.
Usage: AUTO route53domain_enable_auto_renew
Permissions: route53domains:EnableDomainAutoRenew
"""


def run_action(boto_session, rule, entity, params):
    domain = entity['name']
    client = boto_session.client('route53domains', region_name='us-east-1')

    print(f'{__file__} - Trying to enable auto renew for {domain}... \n')
    result = client.enable_domain_auto_renew(DomainName=domain)
    responseCode = result['ResponseMetadata']['HTTPStatusCode']
    if responseCode >= 400:
        raise ValueError("Unexpected error: %s \n" % str(result))
    else:
        print(f'{__file__} - Done. \n')
        text_output = f'Successfully enabled auto-renew for the domain: {domain} \n'

    return text_output
