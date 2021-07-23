import os

import numpy as np
from awsservice.s3 import uploadImgToS3
from dicom_generator.column_mapping import child_mapping_table
from dicom_generator.processor import Processor
from PIL import Image
from pydicom import dcmread
from tqdm import tqdm


def to_csv():
    processor = Processor()
    dicom_files = os.listdir("data/dicom_files/")
    for dicom in dicom_files:
        print(f"Processing dicom: {dicom}")
        dicom_object = dcmread(f"data/dicom_files/{dicom}")
        create_csv(processor, dicom_object, dicom)

    processor.create_csv()
    processor.clean()


def create_csv(processor, dicom_object, dicom_name):
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
            processor.main_dict[col["name"]].append("-")
            filename = dicom_object.filename.split("/")[2]

    generate_image(dicom_object, dicom_name)


def generate_image(dicom_object, dicom_name):
    try:
        try:
            secuence = dicom_object[0x00280008].value
        except:
            secuence = 0

        i = 0

        if int(secuence) > 2:

            for pixel_array in tqdm(dicom_object.pixel_array):
                i += 1
                generate_png_from_pixel(pixel_array, dicom_name, i)
        else:
            generate_png_from_dicom(dicom_object, dicom_name, i)
    except:
        print(f"Could not convert:  {dicom_object}")


def generate_png_from_pixel(pixel_array, dicom_name, index):
    image = pixel_array.astype(float)

    paths = image_helper(image, index, dicom_name)

    uploadImgToS3(paths[0])

    delete_image(paths[1])


def generate_png_from_dicom(dicom_object, dicom_name, index):
    image = dicom_object.pixel_array.astype(float)

    paths = image_helper(image, index, dicom_name)

    uploadImgToS3(paths[0])

    delete_image(paths[1])


def delete_image(image):
    os.remove(image)


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


def decode(string):
    encoding = "utf-8"
    errors = "replace"

    try:
        return string.decode(encoding, errors).replace("\x00", "")
    except:
        return str(string)


def child_mapping(number):
    return child_mapping_table()[number]
