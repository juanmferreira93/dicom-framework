from awsservice.s3 import connect, download, upload
from processor.processor import print_dicom, to_csv, redshift


def generate_dw_data():
    # download()
    # print_dicom()
    # to_csv()
    # upload()
    redshift()

generate_dw_data()
