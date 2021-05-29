import boto3
from decouple import config


def connect():
    region_name = config('AWS_DEFAULT_REGION')
    access_key = config('AWS_ACCESS_KEY_ID')
    master_key = config('AWS_SECRET_ACCESS_KEY')

    s3 = boto3.resource(
        service_name='s3',
        region_name=region_name,
        aws_access_key_id=access_key,
        aws_secret_access_key=master_key
    )

    for bucket in s3.buckets.all():
        print(f'You are connected to the following buckets: {bucket.name}')

    return s3
