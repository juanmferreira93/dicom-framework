import os

from awsservice.s3 import download
from consolemenu import *
from consolemenu.items import *
from dicom_generator.generator import to_csv
from transformations.t1 import T1


def main():
    menu = ConsoleMenu("DICOM Framework Processor", "Select your choice")
    generate_dw_function = FunctionItem("Process DICOM files", to_csv)

    menu.append_item(generate_dw_function)

    sub_menu = MultiSelectMenu(
        "Transformations Menu",
        "This is a Multi-Select Menu",
        epilogue_text=(
            "Please select one or more entries separated by commas, and/or a range "
            "of numbers. For example:  1,2,3   or   1-4   or   1,3-4"
        ),
        exit_option_text="Return",
    )

    for file in os.listdir("dicomframework/transformations/"):
        if not file in ["__init__.py", "transformation.py"]:
            file_name = file.split(".")[0] + "()"
            function = FunctionItem(f"{file}", eval(file_name.capitalize()).run)
            sub_menu.append_item(function)

    sub_menu_item = SubmenuItem("Transformations", submenu=sub_menu)
    sub_menu_item.set_menu(menu)

    menu.append_item(sub_menu_item)
    menu.show()


def auto_create_folders():
    if not os.path.exists("data/csv_files"):
        os.makedirs("data/csv_files")

    if not os.path.exists("data/dicom_files"):
        os.makedirs("data/dicom_files")

    if not os.path.exists("data/image_files"):
        os.makedirs("data/image_files")


if __name__ == "__main__":
    auto_create_folders()
    main()
