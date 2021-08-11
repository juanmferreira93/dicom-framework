import logging

from dicomframework.awsservice.transformations import connect_query
from dicomframework.transformations.transformation import Transformation

logger = logging.getLogger(__name__)

class T1(Transformation):
    def run(self):
        logger.info("Executing T1")

        self.execute("")  # todo: need to improve this

        logger.info("Finish execution of T1")

    def execute(self, sql_statement):
        conn = connect_query()
        cur = conn.cursor()

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

        logger.info(f"Executing query: {sql_query}")
        cur.execute(sql_query)

        logger.info("Commiting")
        conn.commit()

        cur.close()
        conn.close()
