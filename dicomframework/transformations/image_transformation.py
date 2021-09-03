import logging
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
from abc import ABC, abstractmethod
from dicomframework.awsservice.redshift import write
from dicomframework.awsservice.transformations import connect_query
from dicomframework.awsservice.s3 import downloadImg, uploadImgToS3OnT1
from dicomframework.dicom_generator.generator import delete_file

class ImageTransformation(ABC):
    logger = logging.getLogger("dicomframework.ImageTransformations")

    def run(self):
        """
        Template method
        """
        print ("111")
        images = self.get_images()

        

    def convert_image(image_path):
        image_full_path = f"data/image_files/{image_path}"
        image = Image.open(image_full_path)
        factor=2
        image = ImageEnhance.Contrast(image).enhance(factor)
        final_image = np.uint8(image)
        final_image = Image.fromarray(final_image)
        image_path_Save = 'transform'+image_path
        image_full_path = f"data/image_files/{image_path_Save}"
        final_image.save(image_full_path)
       

    def get_images(self):
        conn = connect_query()
        cur = conn.cursor()

        cur.execute("select * from public.image_table")

        # todo: ver bien como manejar esto, en teoria son
        # los resultados de la consulta que trae todas la imagenes.
        images = cur.fetchall()
        # por ejemplo, para recorrerlo:
        # esto hay qye ver si lo podemos cerrar y seguir usando lo que
        # quedo guardado en images afuera del metodo. Seria lo ideal.

        for row in images: 
            name = row[1]
            name2= name.split("/")
            name3=name2[1]+"/"+name2[2]
            print("entra a descargar : "+name3)
            downloadImg(name3)
            print("descarg0 : "+name3)
            #convert_image(name3), como no pude llamar al convert lo tire pa aca
            image_full_path = f"data/{name3}"
            image = Image.open(image_full_path)
            factor=2
            image = ImageEnhance.Contrast(image).enhance(factor)
            final_image = np.uint8(image)
            final_image = Image.fromarray(final_image)
            image_path_Save = 'transform'+name2[2]
            image_full_path = f"data/image_files/{image_path_Save}"
            
            final_image.save(image_full_path)
            uploadImgToS3OnT1(image_path_Save)
            delete_file(f"data/{name3}")
            
           

        cur.close()
        conn.close()
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
