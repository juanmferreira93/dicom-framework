from awsservice.s3 import connect, download, upload
from processor.processor import print_dicom, to_csv


def generate_dw_data():
    download()
    # print_dicom()
    to_csv()
    # upload()


generate_dw_data()
