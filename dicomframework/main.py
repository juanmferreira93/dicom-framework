import logging
import os
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import RotatingFileHandler

from flask import Flask, flash, redirect, render_template, request, url_for

from dicomframework.awsservice.redshift import connect as connect_redshift
from dicomframework.awsservice.s3 import connect as connect_s3
from dicomframework.awsservice.transformation import connect_query
from dicomframework.dicom_generator.generator import to_dict
from dicomframework.transformations.image_transformation import ImageTransformation
from dicomframework.transformations.image_transformation_example import (
    ImageTransformationExample,
)
from dicomframework.transformations.sql_transformation import SqlTransformation
from dicomframework.transformations.sql_transformation_example import (
    SqlTransformationExample,
)

executor = ThreadPoolExecutor(1)

app = Flask("dicomframework")
app.secret_key = "app-secret-key"

file_handler = RotatingFileHandler("production.log", maxBytes=2000)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
logger = app.logger


def auto_create_folders():
    if not os.path.exists("data/csv_files"):
        os.makedirs("data/csv_files")
        logger.info("Folder data/csv_files was created")

    if not os.path.exists("data/dicom_files"):
        os.makedirs("data/dicom_files")
        logger.info("Folder data/dicom_files was created")

    if not os.path.exists("data/image_files"):
        os.makedirs("data/image_files")
        logger.info("Folder data/image_files was created")


@app.before_request
def check_startup_configuration():
    if not request.path == "/":
        try:
            # Redshift
            logger.info("Testing Reshift connection")
            conn = connect_redshift()
            conn.execute("select * from main_table limit 1")

            # S3
            logger.info("Testing S3 connection")
            conn = connect_s3()
            bucket = conn.Bucket(os.environ.get("AWS_BUCKET_NAME"))
            for obj in bucket.objects.filter(Prefix="dicom_files/"):
                obj.key

            # Transformations
            logger.info("Testing Transformation connection")
            conn = connect_query()
            cur = conn.cursor()
            cur.execute("select * from main_table limit 1")

            logger.info("All connections are good")
        except:
            logger.error("Please check your credentials before continue.")
            flash("Something went wrong, please check your credentials.")

            return redirect(url_for("index"))


@app.route("/")
def index():
    auto_create_folders()

    return render_template("home.html")


@app.route("/process_dicom", methods=["POST"])
def process_dicom():
    executor.submit(to_dict)
    logger.info("Processor start runing on background")

    flash("DICOM Process started in background")

    return redirect(url_for("index"))


@app.route("/sql_transformation_example", methods=["POST"])
def sql_transformation_example():
    logger.info("SqlTransformationExample start runing on background")
    executor.submit(call_sql_transformation(SqlTransformationExample()))
    flash("SqlTransformation: SqlTransformationExample started in background")

    return redirect(url_for("index"))


@app.route("/image_transformation_example", methods=["POST"])
def image_transformation_example():
    logger.info("ImageTransformationExample start runing on background")
    executor.submit(call_image_transformation(ImageTransformationExample()))
    flash("ImageTransformation: ImageTransformationExample started in background")

    return redirect(url_for("index"))


def call_sql_transformation(sql_transformation: SqlTransformation):
    sql_transformation.run()


def call_image_transformation(image_transformation: ImageTransformation):
    image_transformation.run()
