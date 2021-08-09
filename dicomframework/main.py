import logging
import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, flash, redirect, render_template, url_for

from dicomframework.awsservice.s3 import download
from dicomframework.dicom_generator.generator import to_csv
from dicomframework.transformations.t1 import T1

executor = ThreadPoolExecutor(1)

app = Flask("DICOM-Processor")
app.secret_key = "app-secret-key"

logging.basicConfig(
    filename="logs.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

def auto_create_folders():
    if not os.path.exists("data/csv_files"):
        os.makedirs("data/csv_files")

    if not os.path.exists("data/dicom_files"):
        os.makedirs("data/dicom_files")

    if not os.path.exists("data/image_files"):
        os.makedirs("data/image_files")

@app.route("/")
def index():
    auto_create_folders()
    return render_template("home.html")


@app.route("/process_dicom", methods=["POST"])
def process_dicom():
    executor.submit(to_csv)
    flash("DICOM Process started in background")
    return redirect(url_for("index"))
