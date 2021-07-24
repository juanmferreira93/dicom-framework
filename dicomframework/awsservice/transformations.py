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


def execute(sql_statement):
    conn = connect_query()

    cur = conn.cursor()
    cur.execute(sql_statement)

    cur.close()
    conn.close()
