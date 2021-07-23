from transformation import execute


def run(sql_statement):
    execute(sql_statement)


run("select * from main_table")
