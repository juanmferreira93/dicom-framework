import os

from awsservice.s3 import download
from consolemenu import *
from consolemenu.items import *
from processor.processor import to_csv
from transformations.t1 import run


def main():
    menu = ConsoleMenu("DICOM Framework Processor", "Select your choice")

    download_dicom_files_function = FunctionItem(
        "Download DICOM files", download_dicom_files
    )
    generate_dw_function = FunctionItem("Process DICOM files", generate_dw)

    menu.append_item(download_dicom_files_function)
    menu.append_item(generate_dw_function)

    for file in os.listdir("dicomframework/transformations/"):
        if not file in ["__init__.py", "transformation.py"]:
            test_function = FunctionItem(f"{file}", run_t1)
            menu.append_item(test_function)

    menu.show()


def generate_dw():
    generate_dw_data(True)


def generate_dw_data(write_on_redshift):
    to_csv(write_on_redshift)


def download_dicom_files():
    download()


def run_t1():
    run()


if __name__ == "__main__":
    main()
