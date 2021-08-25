import logging
import os
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import RotatingFileHandler

from flask import Flask, flash, redirect, render_template, url_for

from dicomframework.dicom_generator.generator import to_csv
from dicomframework.transformations.sql_transformation_example import (
    SqlTransformationExample,
)
from dicomframework.transformations.transformation import Transformation

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


@app.route("/")
def index():
    auto_create_folders()

    return render_template("home.html")


@app.route("/process_dicom", methods=["POST"])
def process_dicom():
    executor.submit(to_csv)
    logger.info("Processor start runing on background")

    flash("DICOM Process started in background")

    return redirect(url_for("index"))


@app.route("/sql_transformation_example", methods=["POST"])
def sql_transformation_example():
    logger.info("SqlTransformationExample start runing on background")

    executor.submit(client_call(SqlTransformationExample()))

    flash("Transformation: SqlTransformationExample started in background")

    return redirect(url_for("index"))


def client_call(transformation: Transformation):
    transformation.run()
