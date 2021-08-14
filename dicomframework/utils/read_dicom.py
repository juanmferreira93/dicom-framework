import os

from pydicom import dcmread


def read_dicom():
    file_name = os.listdir("data/dicom_files")[0]
    ds = dcmread(f"data/dicom_files/{file_name}")
    breakpoint()
    print(ds)


read_dicom()
