from decouple import config
from sqlalchemy import NVARCHAR, create_engine


def connect():
    dsn_database = config("DSN_DATABASE")
    dsn_hostname = config("DSN_HOSTNAME")
    dsn_port = config("DSN_PORT")
    dsn_uid = config("DSN_UID")
    dsn_pwd = config("DSN_PWD")

    conn = create_engine(
        f"postgresql://{dsn_uid}:{dsn_pwd}@{dsn_hostname}:{dsn_port}/{dsn_database}"
    )

    print("Connected to Redshift")

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

    print(f"Table: {table_name} created/charged fine!")
