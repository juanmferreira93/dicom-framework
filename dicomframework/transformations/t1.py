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
        end_query = "with no schema binding;"
        sql_query = (
            f"{start_query} AS "
            f"select * from public.main_table "
            "JOIN public.image_table "
            "ON public.main_table.image_paths = public.image_table.id "
            "JOIN public.patient_table "
            "ON public.main_table.patientid = public.patient_table.id "
            f"{end_query}"
        )

        print(f"Executing query: {sql_query}")
        cur.execute(sql_query)
        print("Commiting")
        conn.commit()

        cur.close()
        conn.close()
