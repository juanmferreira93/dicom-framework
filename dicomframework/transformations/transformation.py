import logging
from abc import ABC, abstractmethod

from dicomframework.awsservice.transformations import connect_query


class Transformation(ABC):
    logger = logging.getLogger("dicomframework.Transformations")

    def run(self):
        """
        Template method
        """

        "Required"
        view_name = self.view_name()
        sql_query = self.sql_query()

        "Non required"
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
