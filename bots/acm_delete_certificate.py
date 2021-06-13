import boto3
from botocore.exceptions import ClientError

def run_action(session, rule, entity, params):
    acm_client = session.client("acn")

    certificate_arn = ''
    try:
        acm_res = acm_client.delete_certificate(CertificateArn=certificate_arn)
        text_output = f"Deleted certificate: {certificate_arn}"
    except ClientError as e:
        text_output = "Unexpected error: %s \n" % e

    return text_output