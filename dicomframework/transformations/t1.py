from awsservice.transformations import connect_query
from transformations.transformation import Transformation


class T1(Transformation):
    def run(self):
        print("Executing T1")

        self.execute("select * from main_table")

        print("Finish execution of T1")

        input("Press ENTER to continue \n")

    def execute(self, sql_statement):
        conn = connect_query()
        cur = conn.cursor()
        cur.execute(sql_statement)

        # todo: improve this and make more logic
        start_query = f"create or replace view public.{type(self).__name__}_view"
        sql_query = (
            f"{start_query} as select * from public.main_table with no schema binding;"
        )
        cur.execute(sql_query)

        conn.commit()

        cur.close()
        conn.close()
