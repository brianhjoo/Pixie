import os
import boto3
from botocore.exceptions import ClientError


BUCKET = os.environ.get('BUCKET')

S3 = boto3.client(
    's3',
    'us-west-1',
    aws_access_key_id=os.environ.get('ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('SECRET_ACCESS_KEY')
)


def upload_file(
        file_name,
        folder_name,
        bucket=BUCKET,
        object_name=None):
    ''' Upload a file to a s3 bucket. '''

    # If s3 object_name was not specified, use file_name
    if object_name is None:
        object_name = f'{folder_name}/{os.path.basename(file_name)}'

    # Upload the file
    s3_client = S3

    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError:
        return False

    return True


def download_file(
        file_name,
        folder_name,
        bucket=BUCKET,
        object_name=None):
    ''' Download a file from s3 bucket. '''

    if object_name is None:
        object_name = f'{folder_name}/{os.path.basename(file_name)}'

    s3_client = S3

    try:
        s3_client.download_file(bucket, object_name,
                                f'image_holding/{file_name}')
    except ClientError:
        return False

    return True


def list_user_files(folder_name, bucket=BUCKET):
    ''' Get a list files in a folder. '''

    s3_client = S3

    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder_name)
    except ClientError:
        return False

    if 'Contents' in response:
        files = [content['Key'].split('/')[1]
                 for content in response['Contents']]

        return files
    else:
        return []


def delete_file(
        file_name,
        folder_name,
        bucket=BUCKET,
        object_name=None):
    ''' Delete a file from s3 bucket. '''

    s3_client = S3

    if object_name is None:
        object_name = f'{folder_name}/{file_name}'

    try:
        s3_client.delete_object(
            Bucket=bucket,
            Key=object_name,
        )
    except ClientError:
        return False

    return True
