"""
## s3_block_public_access
What it does: turn on S3 Bucket Block public access
Usage: AUTO: s3_block_public_access BlockPublicAcls_NewPUTRequests=<true|false>  BlockPublicPolicy_NewPUTRequests=<true|false>
Limitations: none
Notes:
    -  before running this bot, ensure that your applications will work correctly without public access
    - works with JSON - Full / Basic entity findings
Examples:

    Block public access to buckets and objects granted through new public ACLs and Bucket Policies:
    AUTO: s3_block_public_access BlockPublicAcls_NewPUTRequests=true  BlockPublicPolicy_NewPUTRequests=true

    Block public access to buckets and objects granted through any existing ACLs and Bucket Policies
    ( granted through new public ACLs and Bucket Policies Configuration Stays the same ):
    AUTO: s3_block_public_access

    Block public access to buckets and objects granted through any existing ACLs and Bucket Policies But not for
    new public ACLs and Bucket Policies:
    AUTO: s3_block_public_access BlockPublicAcls_NewPUTRequests=false  BlockPublicPolicy_NewPUTRequests=false

"""

import boto3
from botocore.exceptions import ClientError

usage = 'AUTO: s3_block_public_access BlockPublicAcls_NewPUTRequests=<true|false>  BlockPublicPolicy_NewPUTRequests=<true|false> \n '

text_output = ''

TEXT_OUTPUT_DIC = {
    'BlockPublicAcls': ' set to true - certain PUT requests includes a public ACL will fail \n ',
    'IgnorePublicAcls': ' set to true -  S3 will ignore all public ACLs on this bucket and objects in this bucket \n ',
    'BlockPublicPolicy': 'set to true -  S3 will reject calls to PUT Bucket policy if the specified bucket policy '
                         'allow public access. \n ',
    'RestrictPublicBuckets': 'set to true -  access to this bucket restricted to only AWS services and authorized users '
                             'within this account if the bucket has a public policy. \n '
}


def run_action(boto_session, rule, entity, params):
    # Create an S3 client
    s3 = boto3.client('s3')
    bucket_id = entity['id']

    # For basic findings use  - entity region is not specified
    region = s3.get_bucket_location(Bucket=bucket_id)['LocationConstraint']
    s3_client = boto_session.client('s3', region_name=region)
    current_acces_block_config = s3_client.get_public_access_block(Bucket=bucket_id)['PublicAccessBlockConfiguration']
    global text_output, usage
    # Param retrieving
    try:
        params_dic = get_params(params, current_acces_block_config)
    except Exception as e:
        return (e)

    print(params_dic)

    # -----------------------  Block public access of the bucket ----------------------------------#

    try:
        # -------call S3 to block public access --------#

        # define changes in acl
        for key in params_dic:
            if params_dic[key]:
                text_output = text_output + key + ' ' + TEXT_OUTPUT_DIC[key]

        result = s3_client.put_public_access_block(
            Bucket=bucket_id,
            PublicAccessBlockConfiguration=params_dic
        )

        responseCode = result['ResponseMetadata']['HTTPStatusCode']
        if responseCode >= 400:
            text_output = "Unexpected error: %s \n" % str(result)
        else:
            text_output = text_output + "Bucket's Public Access Block enabled: %s \n" % bucket_id

    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output


def get_params(params, curr_config):
    global text_output

    params_dic = curr_config  # keep part of the user config if he doesnt want to change it

    # turn on block existing acls and policies any way
    params_dic['IgnorePublicAcls'] = True
    params_dic['RestrictPublicBuckets'] = True

    if len(params) == 1:
        return params_dic
    try:
        for index, param in enumerate(params):
            if '=' in param:
                key, value = param.split('=')
                key = key.rsplit('_NewPUTRequests', 1)[0]
            else:
                continue

            if key == 'BlockPublicAcls' or key == 'BlockPublicPolicy':
                val = True
                if value.lower() == 'true':
                    params_dic[key] = val
                elif value.lower() == 'false':
                    val = False
                    params_dic[key] = val
                else:
                    text_output = text_output + key + ' parameter value does not match true or false. Defaulting is to ' \
                                                      'ignore - configuration stays as is \n '
            else:
                text_output = text_output + key + ' parameter name does not match any Public Access Block ' \
                                                  'Configuration parameters - Ignored try again.\n ' + usage
        return params_dic

    except:
        text_output = text_output + 'Params handling error. Please check parameters and try again.\n ' + usage
        raise Exception(text_output)
