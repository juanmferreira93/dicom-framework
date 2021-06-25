from awsservice.s3 import download, upload
from processor.processor import to_csv


def generate_dw_data():
    download()
    to_csv()
    upload()


generate_dw_data()
