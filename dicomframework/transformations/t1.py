import logging

from dicomframework.awsservice.transformations import connect_query
from dicomframework.transformations.transformation import Transformation

logger = logging.getLogger("dicomframework.t1")

# todo: we need to improve transformations
class T1(Transformation):
    def run():
        logger.info("Executing T1")

        conn = connect_query()
        cur = conn.cursor()

        # todo: improve this and make more logic
        start_query = f"create or replace view public.t1_view"
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

        logger.info("Finish execution of T1")
