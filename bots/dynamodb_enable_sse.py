"""
## dynamodb_enable_sse
What it does: enables dynamodb sse (Server Side Encryption)
Usage: dynamodb_enable_sse KMSMasterKeyId=<kms_key_id>
Example: dynamodb_enable_sse KMSMasterKeyId=11223344-4444-5555-6666-777788889999
Limitations: none
"""

from botocore.exceptions import ClientError

def run_action(session, rule, entity, params):
    dynamo_client = session.client('dynamodb')

    table_name = entity['name']
    kms_key_id = params.get('KMSMasterKeyId')

    text_output = ''
    try:
        response = dynamo_client.update_table(
            TableName=table_name,
            SSESpecification={
                'Enabled': True,
                'SSEType': 'KMS',
                'KMSMasterKeyId': kms_key_id}
        )
        text_output = f'Table {table_name} enable sse (Server Side Encryption)'
    except ClientError as e:
        text_output = f"Unexpected error: {e}"

    return text_output