import logging
from abc import ABC, abstractmethod

from dicomframework.awsservice.transformation import connect_query


class SqlTransformation(ABC):
    logger = logging.getLogger("dicomframework.SqlTransformations")

    def run(self):
        """
        Template method
        """

        view_name = self.view_name()
        sql_query = self.sql_query()
        final_query = self.generate_sql_statement(sql_query, view_name)
        self.execute_query(final_query)

    @abstractmethod
    def sql_query(self):
        pass

    @abstractmethod
    def view_name(self):
        pass

    def generate_sql_statement(self, query, view_name):
        start_query = f"create or replace view public.{view_name} AS "
        end_query = "with no schema binding;"

        return f"{start_query} {query} {end_query}"

    def execute_query(self, query):
        self.logger.info(f"Executing query: {query}")

        conn = connect_query()
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()

        cur.close()
        conn.close()

        self.logger.info(f"Execution finished")
