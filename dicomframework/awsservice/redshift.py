from decouple import config
import psycopg2


def connect():
    dsn_database = config('DSN_DATABASE')
    dsn_hostname = config('DSN_HOSTNAME')
    dsn_port = config('DSN_PORT')
    dsn_uid = config('DSN_UID')
    dsn_pwd = config('DSN_PWD')

    conn = psycopg2.connect(dbname=dsn_database, host=dsn_hostname,
                            port=dsn_port, user=dsn_uid, password=dsn_pwd)
    cur = conn.cursor()

    print('Connected to Redshift')

    return cur


def write(dataFrame):
    cur = connect()
    # cur.execute("begin;")
    # cur.execute("copy dev.public.idmodality from 's3://metadata-test-csv/csv_files/patient_table.csv' credentials 'aws_access_key_id=AKIARTYB5ILZCGHXHMXG;aws_secret_access_key=HBzeRTgIhpI9AWCN6WZBqr8jlydDn6/5RUSt7Cmf' csv;")
    # # Commit your transaction
    # cur.execute("commit;")
    # print("Copy executed fine!")
