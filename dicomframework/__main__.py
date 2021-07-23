import os

from awsservice.s3 import download
from consolemenu import *
from consolemenu.items import *
from processor.processor import to_csv


def main():
    menu = ConsoleMenu("DICOM Framework Processor", "Select your choice")

    download_dicom_files_function = FunctionItem(
        "Download DICOM files", download_dicom_files
    )
    generate_dw_function = FunctionItem("Process DICOM files", generate_dw)

    transformations = []
    for file in os.listdir("dicomframework/transformations/"):
        if not file in ["__init__.py", "transformation.py"]:
            transformations.append(f"{file}")

    selection_menu = SelectionMenu(transformations)
    submenu_item = SubmenuItem("Execute transformations", selection_menu, menu)

    menu.append_item(download_dicom_files_function)
    menu.append_item(generate_dw_function)
    menu.append_item(submenu_item)

    menu.show()


if __name__ == "__main__":
    main()


def generate_dw():
    generate_dw_data(True)


def generate_dw_data(write_on_redshift):
    to_csv(write_on_redshift)


def download_dicom_files():
    download()
