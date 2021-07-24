from awsservice.transformations import execute
from transformations.transformation import Transformation


class T1(Transformation):
    def run(self):
        super().run()

        print("Executing T1")

        sql_statement = "select * from main_table"
        execute(sql_statement)

        print("Finish execution of T1")

    def execute(self, sql_statement):
        super().execute(sql_statement)
