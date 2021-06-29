from awsservice.s3 import connect, download, upload
from processor.processor import print_dicom, to_csv
from awsservice.redshift import  redShiftConnect, createTable

def generate_dw_data():
    connect()
    # download()
    # print_dicom()
    # to_csv()
    # upload()
    cur = redShiftConnect()
    createTable(cur)


generate_dw_data()
