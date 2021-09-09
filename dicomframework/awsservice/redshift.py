import os

from sqlalchemy import NVARCHAR, create_engine


def connect():
    database = os.environ.get("AWS_DATABASE")
    hostname = os.environ.get("AWS_HOSTNAME")
    port = os.environ.get("AWS_PORT")
    uid = os.environ.get("AWS_UID")
    pwd = os.environ.get("AWS_PASSWORD")

    conn = create_engine(f"postgresql://{uid}:{pwd}@{hostname}:{port}/{database}")

    return conn


def write(dataFrame, table_name):
    conn = connect()

    dataFrame.to_sql(
        table_name,
        conn,
        index=False,
        if_exists="replace",
        dtype={
            col_name: NVARCHAR(65535) for col_name in dataFrame
        },  # todo: need to work on that
    )
