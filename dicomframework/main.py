import logging
import os

from flask import Flask, redirect, render_template, request

from dicomframework.awsservice.s3 import download
from dicomframework.dicom_generator.generator import to_csv
from dicomframework.transformations.t1 import T1

app = Flask("DICOM-Processor")
logging.basicConfig(
    filename="logs.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


@app.route("/")
def index():
    auto_create_folders()
    return render_template("home.html")


@app.route("/process_dicom", methods=["POST"])
def process_dicom():
    to_csv()
    return redirect(request.url)


def auto_create_folders():
    if not os.path.exists("data/csv_files"):
        os.makedirs("data/csv_files")

    if not os.path.exists("data/dicom_files"):
        os.makedirs("data/dicom_files")

    if not os.path.exists("data/image_files"):
        os.makedirs("data/image_files")
