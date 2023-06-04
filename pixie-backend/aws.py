import os
import boto3
from botocore.exceptions import ClientError


BUCKET = os.environ.get('BUCKET')

S3 = boto3.client(
    's3',
    'us-west-1',
    aws_access_key_id = os.environ.get('ACCESS_KEY_ID'),
    aws_secret_access_key = os.environ.get('SECRET_ACCESS_KEY')
)


def upload_file(file_name, bucket=BUCKET, object_name=None):
    ''' Upload a file to a s3 bucket. '''

    # If s3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = S3

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError:
        return False

    return True

