import boto3
import os
from decouple import config

BUCKET_NAME = 'metadata-test-csv'


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

    print('Conneced to s3')
    return s3


def upload():
    s3 = connect()
    bucket = s3.Bucket(BUCKET_NAME)

    for file in os.listdir('data/csv_files'):
        print(f'Uploading csv_file: {file}')
        bucket.upload_file(
            Filename=f'data/csv_files/{file}', Key=f'csv_files/{file}')


def download():
    s3 = connect()
    bucket = s3.Bucket(BUCKET_NAME)

    for obj in bucket.objects.filter(Prefix='dicom_files/'):
        file_name = obj.key.split('/')[-1]

        print(f'Downloading dicom_file: {file_name}')
        bucket.download_file(obj.key, f'data/dicom_files/{file_name}')
