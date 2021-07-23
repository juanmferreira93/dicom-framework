from awsservice.transformations import execute


def run():
    print("Executing T1")
    sql_statement = "select * from main_table"
    execute(sql_statement)
    print("Finish execution of T1")
