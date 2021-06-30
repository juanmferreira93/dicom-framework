from awsservice.s3 import download, upload
from processor.processor import to_csv


def generate_dw_data():
    # download() keep this commented for now
    to_csv()
    # upload() keep this commented for now


generate_dw_data()
