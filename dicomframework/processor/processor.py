from processor.tables import fact_cols, patient_cols, child_id_cols
import gc
import os

import pandas as pd
from pydicom import dcmread

# All columns for which we want to collect information
# Still need to define how we will work with sequences
fact_table_cols = fact_cols()
patient_table_cols = patient_cols()
# child_ids = child_id_cols()

# Initialize dictionary to collect the metadata
fact_table_dict = {col: [] for col in fact_table_cols}
patient_table_dict = {col: [] for col in patient_table_cols}

# Get dicoms from files
dicom_files = os.listdir('data/dicom_files/')


def print_dicom():
    for file in os.listdir('data/dicom_files'):
        ds = dcmread(f'data/dicom_files/{file}')
        breakpoint()
        print(ds)


def to_csv():
    global dicom_files
    global fact_table_dict
    global patient_table_dict

    for dicom in dicom_files:
        print(f'Reading dicom_file: {dicom}')
        dicom_object = dcmread(f'data/dicom_files/{dicom}')

        create_csv(dicom_object)

    # Store all information in a DataFrame and run garbage collector
    fact_table_df = pd.DataFrame(fact_table_dict)
    patient_table_df = pd.DataFrame(patient_table_dict)

    del fact_table_dict
    del patient_table_dict
    gc.collect()

    # Save to CSV
    fact_table_df.to_csv('data/csv_files/fact_table.csv', index=False)
    patient_table_df.to_csv('data/csv_files/patient_table.csv', index=False)


def create_csv(dicom_object):
    global fact_table_cols
    global fact_table_dict
    # global child_ids

    for col in fact_table_cols:
        try:
            value = str(getattr(dicom_object, col))

            if col == 'PatientID':
                if value in patient_table_dict['PatientID']:
                    id = patient_table_dict['PatientID'].index(value) + 1
                    fact_table_dict[col].append(str(id))
                else:
                    id = len(fact_table_dict[col]) + 1
                    fact_table_dict[col].append(str(id))

                    create_patient_csv(id, dicom_object)
            else:
                fact_table_dict[col].append(value)
        except:
            fact_table_dict[col].append('-')
            filename = dicom_object.filename.split('/')[2]
            print(f'Error importing Fact: {col} from {filename}')


def create_patient_csv(id, dicom_object):
    global patient_table_cols
    global patient_table_dict

    for col in patient_table_cols:
        try:
            if col == 'id':
                patient_table_dict[col].append(str(id))
            else:
                patient_table_dict[col].append(str(getattr(dicom_object, col)))
        except:
            patient_table_dict[col].append('-')
            filename = dicom_object.filename.split('/')[2]
            print(f'Error importing Patient: {col} from {filename}')