from awsservice.redshift import connect


def execute(sql_statement):
    conn = connect()
    cur = conn.cursor()

    cur.execute(sql_statement)

    cur.fetchall()

    cur.close()
    conn.close()
