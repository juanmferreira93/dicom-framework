import logging
import os

import numpy as np
from decouple import config
from PIL import Image
from pydicom import dcmread

from dicomframework.awsservice.s3 import connect, uploadImgToS3
from dicomframework.dicom_generator.column_mapping import child_mapping_table
from dicomframework.dicom_generator.encode_mapping import decode
from dicomframework.dicom_generator.processor import Processor

logger = logging.getLogger("dicomframework.generator")


def to_csv():
    processor = Processor()

    s3 = connect()
    bucket_name = config("BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    i = 0

    for obj in bucket.objects.filter(Prefix="dicom_files/"):
        file_name = obj.key.split("/")[-1]

        if not file_name == "":
            bucket.download_file(obj.key, f"data/dicom_files/{file_name}")

            dicom_object = dcmread(f"data/dicom_files/{file_name}")
            logger.info(f"Processing dicom: {file_name}")

            modality = dicom_object.Modality
            if modality in processor.supported_modalities:
                i += 1
                create_csv(i, processor, dicom_object, file_name)

            delete_file(f"data/dicom_files/{file_name}")

    processor.crate_records()
    processor.clean()

    logger.info("Process finished")


def delete_file(file):
    os.remove(file)


def create_csv(dicom_index, processor, dicom_object, dicom_name):
    for col in processor.main_cols:
        try:
            data = decode(dicom_object.get_item(f"0x{col['number']}").value)

            if col["number"] in processor.child_ids:
                table = child_mapping(col["number"])

                if data in eval(f"processor.{table}_dict")[col["name"]]:
                    # todo: this line add a extra value when repeated patient appear
                    id = eval(f"processor.{table}_dict")[col["name"]].index(data) + 1
                    processor.main_dict[col["name"]].append(str(id))
                else:
                    id = len(processor.main_dict[col["name"]]) + 1
                    processor.main_dict[col["name"]].append(str(id))

                    create_csv_from_child_table(processor, table, id, dicom_object)
            else:
                processor.main_dict[col["name"]].append(data)

        except:
            if col["name"] != "image_paths":
                processor.main_dict[col["name"]].append("-")

    image_paths = generate_image(dicom_object, dicom_name)
    create_csv_from_image_paths(processor, dicom_index, image_paths)


def generate_image(dicom_object, dicom_name):
    try:
        try:
            secuence = dicom_object[0x00280008].value
        except:
            secuence = 0

        i = 0

        image_paths = []
        if int(secuence) > 2:
            images_count = len(dicom_object.pixel_array)
            for pixel_array in dicom_object.pixel_array:
                i += 1
                logger.info(f"Processing image {i}/{images_count} from {dicom_name}")
                image_path = generate_png_from_pixel(pixel_array, dicom_name, i)
                image_paths.append(image_path)
        else:
            image_path = generate_png_from_dicom(dicom_object, dicom_name, i)
            image_paths.append(image_path)

        return image_paths
    except:
        logger.warning(f"Could not convert: {dicom_object}")


def generate_png_from_pixel(pixel_array, dicom_name, index):
    image = pixel_array.astype(float)
    paths = image_helper(image, index, dicom_name)
    image_path = uploadImgToS3(paths[0])
    delete_file(paths[1])

    return image_path


def generate_png_from_dicom(dicom_object, dicom_name, index):
    image = dicom_object.pixel_array.astype(float)
    paths = image_helper(image, index, dicom_name)
    image_path = uploadImgToS3(paths[0])
    delete_file(paths[1])

    return image_path


def image_helper(image, index, dicom_name):
    rescaled_image = (np.maximum(image, 0) / image.max()) * 255
    final_image = np.uint8(rescaled_image)
    final_image = Image.fromarray(final_image)

    index_string = str(index)
    dicom_name = dicom_name.split(".")[0]
    image_path = f"{dicom_name}-{index_string}.png"
    image_full_path = f"data/image_files/{image_path}"
    final_image.save(image_full_path)

    return [image_path, image_full_path]


def create_csv_from_child_table(processor, table, id, dicom_object):
    for col in eval(f"processor.{table}_cols"):
        try:
            if col["name"] == "id":
                eval(f"processor.{table}_dict")[col["name"]].append(str(id))
            else:
                eval(f"processor.{table}_dict")[col["name"]].append(
                    decode(dicom_object.get_item(f"0x{col['number']}").value)
                )
        except:
            eval(f"processor.{table}_dict")[col["name"]].append("-")
            filename = dicom_object.filename.split("/")[2]


def create_csv_from_image_paths(processor, dicom_index, image_paths):
    processor.main_dict["image_paths"].append(dicom_index)
    for image_path in image_paths:
        processor.image_dict["id"].append(dicom_index)
        processor.image_dict["image_path"].append(image_path)


def child_mapping(number):
    return child_mapping_table()[number]
