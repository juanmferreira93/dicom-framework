import os

from awsservice.s3 import download
from consolemenu import *
from consolemenu.items import *
from dicom_generator.generator import to_csv
from transformations.t1 import run


def main():
    menu = ConsoleMenu("DICOM Framework Processor", "Select your choice")

    download_dicom_files_function = FunctionItem("Download DICOM files", download)
    generate_dw_function = FunctionItem("Process DICOM files", to_csv)

    menu.append_item(download_dicom_files_function)
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
            test_function = FunctionItem(f"{file}", run)
            sub_menu.append_item(test_function)

    sub_menu_item = SubmenuItem("Trasnformations", submenu=sub_menu)
    sub_menu_item.set_menu(menu)

    menu.append_item(sub_menu_item)
    menu.show()


if __name__ == "__main__":
    main()
