import logging
import os
import shutil
from abc import ABC, abstractmethod

import pandas as pd
from PIL import Image

from dicomframework.awsservice.redshift import write
from dicomframework.awsservice.s3 import save_image, uploadImgToS3
from dicomframework.awsservice.transformation import connect_query


class ImageTransformation(ABC):
    logger = logging.getLogger("dicomframework.ImageTransformations")

    def run(self):
        """
        Template method
        """

        transformation_name = self.transformation_name()

        self.download_images(transformation_name)

        for image_name in os.listdir(f"data/{transformation_name}"):
            image = Image.open(f"data/{transformation_name}/{image_name}")
            image = self.transform(image)
            image.save(f"data/{transformation_name}/{image_name}")

            uploadImgToS3(image_name, transformation_name)

        images_dict = self.generate_table(transformation_name)

        try:
            shutil.rmtree(f"data/{transformation_name}")
        except:
            self.logger.warning(f"Could not delete folder: data/{transformation_name}")

        self.write_table(images_dict, transformation_name)
        self.logger.info(f"Transformation: {transformation_name} execution finished")

    def download_images(self, transformation_name):
        conn = connect_query()
        cur = conn.cursor()

        cur.execute("select * from public.image_table")
        images = cur.fetchall()

        for row in images:
            dicom_id = row[0]
            image_name = dicom_id + "+" + row[1].split("/")[-1]
            self.logger.info(f"Getting image: {image_name}")
            save_image(transformation_name, image_name)

        cur.close()
        conn.close()

        return images

    def generate_table(self, transformation_name):
        image_dict = {col: [] for col in ["id", "image_path"]}

        for image_name in os.listdir(f"data/{transformation_name}"):
            dicom_id = image_name.split("+")[0]
            image_dict["id"].append(dicom_id)

            bucket_name = os.environ.get("AWS_BUCKET_NAME")
            region_name = os.environ.get("AWS_DEFAULT_REGION")

            image_path = f"{bucket_name}.s3.{region_name}.amazonaws.com/{transformation_name}/{image_name}"
            image_dict["image_path"].append(image_path)

        return image_dict

    def write_table(self, images_dict, transformation_name):
        self.logger.info(f"Writing new table: {transformation_name} on Redshift")
        images_df = pd.DataFrame(images_dict)
        write(images_df, transformation_name)

    @abstractmethod
    def transform(self, transformation_name):
        # El codigo de la transformacion, lo define el usuario en la clase hija
        pass

    @abstractmethod
    def transformation_name(self):
        # El nombre de la transformacion (con la q se van a crear las tablas y demas)
        # por ahora que la defina el usuario en la clase hija
        pass
