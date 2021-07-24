import psycopg2
from decouple import config


def connect_query():
    conn = psycopg2.connect(
        dbname=config("DSN_DATABASE"),
        host=config("DSN_HOSTNAME"),
        port=config("DSN_PORT"),
        user=config("DSN_UID"),
        password=config("DSN_PWD"),
    )

    return conn
