from awsservice.s3 import download, upload
from processor.processor import to_csv


def generate_dw_data(write_on_redshift):
    # download() # keep this commented for now
    to_csv(write_on_redshift)

generate_dw_data(True)
