import os

import boto3
from decouple import config
from tqdm import tqdm


def connect():
    region_name = config("AWS_DEFAULT_REGION")
    access_key = config("AWS_ACCESS_KEY_ID")
    master_key = config("AWS_SECRET_ACCESS_KEY")

    s3 = boto3.resource(
        service_name="s3",
        region_name=region_name,
        aws_access_key_id=access_key,
        aws_secret_access_key=master_key,
    )

    # print("Conneced to s3")
    return s3


def upload():
    s3 = connect()
    bucket_name = config("BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    for file in os.listdir("data/csv_files"):
        if file.split(".")[1] == "csv":
            # print(f"Uploading csv_file: {file}")
            bucket.upload_file(
                Filename=f"data/csv_files/{file}", Key=f"csv_files/{file}"
            )


def uploadImg():
    s3 = connect()
    bucket_name = config("BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    for file in os.listdir("data/image_files"):
        if file.split(".")[2] == "png":
            # print(f"Uploading img_file: {file}")
            bucket.upload_file(
                Filename=f"data/image_files/{file}", Key=f"image_files/{file}"
            )


def uploadImgToS3(image):
    s3 = connect()
    bucket_name = config("BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    # print(f"Uploading img_file: {image}")

    bucket.upload_file(Filename=f"data/image_files/{image}", Key=f"image_files/{image}")
    # todo: need to return the image url


def download():
    s3 = connect()
    bucket_name = config("BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    for obj in tqdm(bucket.objects.filter(Prefix="dicom_files/")):
        file_name = obj.key.split("/")[-1]

        # print(f"Downloading dicom_file: {file_name}")
        bucket.download_file(obj.key, f"data/dicom_files/{file_name}")
