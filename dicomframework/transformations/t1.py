from awsservice.redshift import execute


def run():
    sql_statement = "select * from main_table"
    execute(sql_statement)
