import os

import psycopg2


def connect_query():
    conn = psycopg2.connect(
        dbname=os.environ.get("AWS_DATABASE"),
        host=os.environ.get("AWS_HOSTNAME"),
        port=os.environ.get("AWS_PORT"),
        user=os.environ.get("AWS_UID"),
        password=os.environ.get("AWS_PASSWORD"),
    )

    return conn
