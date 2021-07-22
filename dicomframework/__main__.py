from processor.processor import to_csv


def generate_dw_data(write_on_redshift):
    # download() # keep this commented for now
    to_csv(write_on_redshift)
    # upload() # keep this commented for now
    # uploadImg() # keep this commented for now

generate_dw_data(True)
