import pandas as pd
import gc
import os
import pydicom
import numpy as np
import cv2
from processor.column_mapping import main_cols, patient_cols, child_id_cols, child_mapping_table
from awsservice.redshift import write
from PIL import ImageTk, Image
from pydicom import dcmread

class Processor:
    def __init__(self):
        # Get cols for each table
        self.main_cols = main_cols()
        self.child_ids = child_id_cols()

        ##### Child tables #####
        self.patient_cols = patient_cols()
        # self.xxx_cols = xxx_cols()
        ##### Finish cols section #####

        # Initialize one dict for each table
        self.main_dict = {col['name']: []
                          for col in self.main_cols}

        ##### Child dicts #####
        self.patient_dict = {col['name']: []
                             for col in self.patient_cols}
        # self.xxx._dict = {col['name']: [] for col in self.xxx_cols}
        ##### Finish dict initialization #####

    # Replace this method with awsservice.redshift.write method
    def create_csv(self):
        main_df = pd.DataFrame(self.main_dict)
        main_df.to_csv('data/csv_files/main.csv', index=False)
        write(main_df, 'main_table')

        ##### Child CSVs #####
        patient_df = pd.DataFrame(self.patient_dict)
        patient_df.to_csv(
            'data/csv_files/patient.csv', index=False)
        write(patient_df, 'patient_table')
        ##### Finish CSV creations #####

    def clean(self):
        # This code deletes dicts
        del self.main_dict

        ##### Child dicts #####
        del self.patient_dict
        gc.collect()
        ##### Finish dict deletion #####


def to_csv():   
    processor = Processor()
    dicom_files = os.listdir('data/dicom_files/')
    for dicom in dicom_files:
        dicom_object = dcmread(f'data/dicom_files/{dicom}')
        try:
            print(f'Reading dicom_file: {dicom}')
            try:
                secuence = dicom_object[0x00280008].value
            except:
                secuence = 0
            i=0
            if ( int(secuence) > 2):
        
                for listaDePixcel in dicom_object.pixel_array:
                    i+=1
                    im =listaDePixcel.astype(float)
                    rescaled_image = (np.maximum(im,0)/im.max())*255 # float pixels
                    final_image = np.uint8(rescaled_image) # integers pixels           
                    final_image = Image.fromarray(final_image)    
                    # final_image.save('data/images/'+dicom+'.jpg') # Save the image as JPG
                    final_image.save('data/images/'+dicom+ str(i)+'.png') # Save the image as PNG
            else:
                im =dicom_object.pixel_array.astype(float)
                rescaled_image = (np.maximum(im,0)/im.max())*255 # float pixels
                final_image = np.uint8(rescaled_image) # integers pixels       
                final_image = Image.fromarray(final_image)          
                # final_image.save('data/images/'+dicom+'.jpg') # Save the image as JPG
                final_image.save('data/images/'+dicom+ str(i)+'.png') # Save the image as PNG

        except:
            print(f'Could not convert:  {dicom}')

        create_csv(processor, dicom_object)
       
    processor.create_csv()
    processor.clean()


def create_csv(processor, dicom_object):
    for col in processor.main_cols:
        try:
            data = decode(dicom_object.get_item(f"0x{col['number']}").value)

            if col['number'] in processor.child_ids:
                table = child_mapping(col['number'])

                if data in eval(f'processor.{table}_dict')[col['name']]:
                    id = eval(f'processor.{table}_dict')[
                        col['name']].index(data) + 1
                    processor.main_dict[col['name']].append(str(id))
                else:
                    id = len(processor.main_dict[col['name']]) + 1
                    processor.main_dict[col['name']].append(str(id))

                    create_csv_from_child_table(
                        processor, table, id, dicom_object)
            else:
                processor.main_dict[col['name']].append(data)
        except:
            processor.main_dict[col['name']].append('-')
            filename = dicom_object.filename.split('/')[2]
            print(f'Error importing Main: {col} from {filename}')


def create_csv_from_child_table(processor, table, id, dicom_object):
    for col in eval(f'processor.{table}_cols'):
        try:
            if col['name'] == 'id':
                eval(f'processor.{table}_dict')[col['name']].append(str(id))
            else:
                eval(f'processor.{table}_dict')[col['name']].append(
                    decode(dicom_object.get_item(f"0x{col['number']}").value)
                )
        except:
            eval(f'processor.{table}_dict')[col['name']].append('-')
            filename = dicom_object.filename.split('/')[2]
            print(f'Error importing Patient: {col} from {filename}')


def decode(string):
    encoding = 'utf-8'
    errors = 'replace'

    try:
        return string.decode(encoding, errors).replace("\x00", '')
    except:
        return str(string)


def child_mapping(number):
    return child_mapping_table()[number]
