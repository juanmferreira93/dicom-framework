import logging
from abc import ABC, abstractmethod

import pandas as pd

from dicomframework.awsservice.redshift import write
from dicomframework.awsservice.transformations import connect_query


class ImageTransformation(ABC):
    logger = logging.getLogger("dicomframework.ImageTransformations")

    def run(self):
        """
        Template method
        """

        images = self.get_images()
        new_images = self.transform(images)
        images_dict = self.generate_table(new_images)
        self.write_table(images_dict)

    def get_images(self):
        conn = connect_query()
        cur = conn.cursor()

        cur.execute("select * from public.image_table")

        # todo: ver bien como manejar esto, en teoria son
        # los resultados de la consulta que trae todas la imagenes.
        images = cur.fetchall()

        # por ejemplo, para recorrerlo:

        # for row in images:
        #   print "%s, %s" % (row["id"], row["image_path"])

        # esto hay qye ver si lo podemos cerrar y seguir usando lo que
        # quedo guardado en images afuera del metodo. Seria lo ideal.

        # cur.close()
        # conn.close()
        return images

    @abstractmethod
    def transform(self, images):
        # El codigo de la transformacion, lo define el usuario en la clase hija
        pass

    def generate_table(self, images):
        # Aca la logica de la generacion del a tabla y el data frame
        # itera sobre images
        # for row in images:
        #   print "%s, %s" % (row["id"], row["image_path"])
        # y va armando todo
        pass

    def write_table(self, images_dict):
        # Aca se deberia usar un metod (o el mismo importandolo) que se
        # usa para escribir en todos lados

        images_df = pd.DataFrame(self.images_dict)
        # el csv lo creamos para una eventual auditoria de la informacion
        images_df.to_csv(f"data/csv_files/{self.transformation_name}.csv", index=False)
        # no se si se lo tengo q pasar con o sin parentesis: self.transformation_name()
        write(images_df, self.transformation_name)
        pass

    @abstractmethod
    def transformation_name(self):
        # El nombre de la transformacion (con la q se van a crear las tablas y demas)
        # por ahora que la defina el usuario en la clase hija
        pass
