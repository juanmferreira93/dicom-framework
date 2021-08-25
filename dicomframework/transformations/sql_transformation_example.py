from dicomframework.transformations.transformation import Transformation


class SqlTransformationExample(Transformation):
    def sql_query(self):
        sql_query = (
            "select * from public.main_table "
            "JOIN public.image_table "
            "ON public.main_table.image_paths = public.image_table.id "
            "JOIN public.patient_table "
            "ON public.main_table.patientid = public.patient_table.id "
        )

        return sql_query

    def view_name(self):
        return "sql_transformation_example"
