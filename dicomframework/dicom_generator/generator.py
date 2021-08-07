import os

import numpy as np
from awsservice.s3 import connect, uploadImgToS3
from decouple import config
from dicom_generator.column_mapping import child_mapping_table
from dicom_generator.processor import Processor
from logger.logger import Logger
from PIL import Image
from pydicom import dcmread
from tqdm import tqdm

logger = Logger()


def to_csv():
    processor = Processor()

    s3 = connect()
    bucket_name = config("BUCKET_NAME")
    bucket = s3.Bucket(bucket_name)

    i = 0

    for obj in bucket.objects.filter(Prefix="dicom_files/"):
        file_name = obj.key.split("/")[-1]
        logger.log("info", f"Downloading file: {file_name}")

        if not file_name == "":
            bucket.download_file(obj.key, f"data/dicom_files/{file_name}")

            dicom_object = dcmread(f"data/dicom_files/{file_name}")
            logger.log("info", f"Processing dicom: {file_name}")

            modality = dicom_object.Modality
            if modality in processor.supported_modalities:
                i += 1
                create_csv(i, processor, dicom_object, file_name)

            delete_file(f"data/dicom_files/{file_name}")

    processor.create_csv()
    processor.clean()

    input("Press ENTER to continue \n")


def delete_file(file):
    os.remove(file)


def create_csv(dicom_index, processor, dicom_object, dicom_name):
    for col in processor.main_cols:
        try:
            data = decode(dicom_object.get_item(f"0x{col['number']}").value)

            if col["number"] in processor.child_ids:
                table = child_mapping(col["number"])

                if data in eval(f"processor.{table}_dict")[col["name"]]:
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
                filename = dicom_object.filename.split("/")[2]

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
            for pixel_array in tqdm(dicom_object.pixel_array):
                i += 1
                image_path = generate_png_from_pixel(pixel_array, dicom_name, i)
                image_paths.append(image_path)
        else:
            image_path = generate_png_from_dicom(dicom_object, dicom_name, i)
            image_paths.append(image_path)

        return image_paths
    except:
        logger.log("error", f"Could not convert:  {dicom_object}")


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
    rescaled_image = (np.maximum(image, 0) / image.max()) * 255  # float pixels
    final_image = np.uint8(rescaled_image)  # integers pixels
    final_image = Image.fromarray(final_image)

    index_string = str(index)
    image_path = f"{dicom_name}{index_string}.png"
    image_full_path = f"data/image_files/{image_path}"
    final_image.save(image_full_path)  # Save the image as PNG

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


def decode(string):
    encoding = "utf-8"
    errors = "replace"

    try:
        return string.decode(encoding, errors).replace("\x00", "")
    except:
        return str(string)


def child_mapping(number):
    return child_mapping_table()[number]
