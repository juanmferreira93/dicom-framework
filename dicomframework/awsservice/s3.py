import os

import boto3


def connect():
    region_name = os.environ.get("AWS_DEFAULT_REGION")
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    master_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    s3 = boto3.resource(
        service_name="s3",
        region_name=region_name,
        aws_access_key_id=access_key,
        aws_secret_access_key=master_key,
    )

    return s3


def uploadImgToS3(image, image_folder="image_files"):
    s3 = connect()
    bucket_name = os.environ.get("AWS_BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)
    region_name = os.environ.get("AWS_DEFAULT_REGION")

    bucket.upload_file(
        Filename=f"data/{image_folder}/{image}", Key=f"{image_folder}/{image}"
    )

    image_path = f"{bucket_name}.s3.{region_name}.amazonaws.com/{image_folder}/{image}"
    return image_path


def download():
    s3 = connect()
    bucket_name = os.environ.get("AWS_BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix="dicom_files/"):
        file_name = obj.key.split("/")[-1]

        if not file_name == "":
            bucket.download_file(obj.key, f"data/dicom_files/{file_name}")


def save_image(folder_name, image_name):
    s3 = connect()
    bucket_name = os.environ.get("AWS_BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    if not os.path.exists(f"data/{folder_name}"):
        os.makedirs(f"data/{folder_name}")

    image_name_s3 = image_name.split("+")[-1]
    bucket.download_file(
        f"image_files/{image_name_s3}", f"data/{folder_name}/{image_name}"
    )
