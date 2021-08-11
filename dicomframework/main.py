import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, flash, redirect, render_template, url_for

from dicomframework.awsservice.s3 import download
from dicomframework.dicom_generator.generator import to_csv
from dicomframework.transformations.t1 import T1

executor = ThreadPoolExecutor(1)

app = Flask(__name__)
app.secret_key = "app-secret-key"

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

logging.basicConfig(
    filename="logs.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def auto_create_folders():
    if not os.path.exists("data/csv_files"):
        os.makedirs("data/csv_files")
        app.logger.info("Folder data/csv_files was created")

    if not os.path.exists("data/dicom_files"):
        os.makedirs("data/dicom_files")
        app.logger.info("Folder data/dicom_files was created")

    if not os.path.exists("data/image_files"):
        os.makedirs("data/image_files")
        app.logger.info("Folder data/image_files was created")


@app.route("/")
def index():
    auto_create_folders()

    return render_template("home.html")


@app.route("/process_dicom", methods=["POST"])
def process_dicom():
    executor.submit(to_csv)
    app.logger.info("Processor start runing on background")

    flash("DICOM Process started in background")

    return redirect(url_for("index"))
