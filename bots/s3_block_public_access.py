"""
## s3_block_public_access
What it does: turn on S3 Bucket Block public access

Usage:  s3_block_public_access <BlockNewPublicAcls> <BlockNewPublicPolicy>
Example: AUTO: s3_block_public_access <true|false|-> <true|false|->
When - set for ignore the specific attribute if its optional so usage will be
Limitations: none
Notes:
    -  before running this bot, ensure that your applications will work correctly without public access
    - works with JSON - Full / Basic entity findings
Examples:

    Block public access to buckets and objects granted through new public ACLs and Bucket Policies:
    AUTO: s3_block_public_access BlockPublicAcls_NewPUTRequests=true  BlockPublicPolicy_NewPUTRequests=true

    Block public access to buckets and objects granted through any existing ACLs and Bucket Policies
    ( granted through new public ACLs and Bucket Policies Configuration Stays Unchanged ):
    AUTO: s3_block_public_access - -

    Block public access to buckets and objects granted through any existing ACLs and Bucket Policies BUT NOT for
    new public ACLs and Bucket Policies added/created:
    AUTO: s3_block_public_access false false

     Block public access to buckets and objects granted through any existing ACLs and Bucket Policies
     BUT NOT for new public ACLs ,   new Bucket Policies Configuration Stays Unchanged :
    AUTO: s3_block_public_access false -

"""

import boto3
from botocore.exceptions import ClientError

usage = 'AUTO: s3_block_public_access <true|false|-> <true|false|-> \n '

text_output = ''

OUTPUT_DIC = {
    'BlockPublicAcls': ' set to true - certain PUT requests includes a public ACL will fail \n ',
    'BlockPublicPolicy': 'set to true -  S3 will reject calls to PUT Bucket policy if the specified bucket policy '
                         'allow public access. \n ',
    'IgnorePublicAcls': ' set to true -  S3 will ignore all public ACLs on this bucket and objects in this bucket \n ',

    'RestrictPublicBuckets': 'set to true -  access to this bucket restricted to only AWS services and authorized '
                             'users within this account if the bucket has a public policy. \n '
}

CONFIG_PARAMS_DIC = {  # key: param index val : config name
    0: 'BlockPublicAcls',
    1: 'BlockPublicPolicy'
}


def run_action(boto_session, rule, entity, params):
    # Create an S3 client
    s3 = boto3.client('s3')
    bucket_id = entity['id']

    # keep current config
    current_acces_block_config = s3.get_public_access_block(Bucket=bucket_id)['PublicAccessBlockConfiguration']
    global text_output, usage

    # Param retrieving
    try:
        params_dic = get_params(params, current_acces_block_config)
    except Exception as e:
        return e

    # -----------------------  Block public access of the bucket ----------------------------------#

    try:
        # -------call S3 to block public access --------#

        # define changes in acl
        for key in params_dic:
            if params_dic[key]:
                text_output = text_output + key + ' ' + OUTPUT_DIC[key]

        result = s3.put_public_access_block(
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

            key = CONFIG_PARAMS_DIC[index]  # get config key name
            user_value = param
            val = True
            if user_value.lower() == 'true':
                params_dic[key] = val
            elif user_value.lower() == 'false':
                val = False
                params_dic[key] = val
            elif user_value == '-':
                params_dic[key] = curr_config[key]  # keeps curr config
                continue
            else:
                text_output = text_output + key + ' parameter value does not match true or false or - . Defaulting is' \
                                                  ' to ignore - configuration stays as is \n '
        return params_dic

    except:
        text_output = text_output + 'Params handling error. Please check parameters and try again.\n ' + usage
        raise Exception(text_output)
