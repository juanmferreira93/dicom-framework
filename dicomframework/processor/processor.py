from processor.tables import fact_cols, patient_cols
import gc
import os

import pandas as pd
from pydicom import dcmread


def print_dicom():
    for file in os.listdir('data/dicom_files'):
        ds = dcmread(f'data/dicom_files/{file}')
        breakpoint()
        print(ds)


def to_csv():
    # All columns for which we want to collect information
    # Still need to define how we will work with sequences
    fact_table_cols = fact_cols()
    patient_table_cols = patient_cols()

    # Initialize dictionary to collect the metadata
    fact_table_dict = {col: [] for col in fact_table_cols}
    patient_table_dict = {col: [] for col in patient_table_cols}

    # Get dicoms from files
    dicom_files = os.listdir('data/dicom_files/')

    for dicom in dicom_files:
        print(f'Reading dicom_file: {dicom}')
        dicom_object = dcmread(f'data/dicom_files/{dicom}')

        create_table2(dicom_object, fact_table_cols,
                      fact_table_dict, patient_table_cols, patient_table_dict)

    # Store all information in a DataFrame and run garbage collector
    fact_table_df = pd.DataFrame(fact_table_dict)
    patient_table_df = pd.DataFrame(patient_table_dict)

    del fact_table_dict
    del patient_table_dict
    gc.collect()

    # Save to CSV
    fact_table_df.to_csv('data/csv_files/fact_table.csv', index=False)
    patient_table_df.to_csv('data/csv_files/patient_table.csv', index=False)


def create_table2(dicom_object, table_cols, table_dict, patient_table_cols, child_dict):
    for col in table_cols:
        try:
            if col == 'PatientID':
                id = len(table_dict[col]) + 1
                table_dict[col].append(str(id))
                create_child_table(
                    id, dicom_object, patient_table_cols, child_dict)
            else:
                table_dict[col].append(str(getattr(dicom_object, col)))
        except:
            table_dict[col].append('-')
            print(f'Error importing fields')


def create_child_table(id, dicom_object, child_cols, child_dict):
    for col in child_cols:
        try:
            if col == 'id':
                child_dict[col].append(str(id))
            else:
                child_dict[col].append(str(getattr(dicom_object, col)))
        except:
            child_dict[col].append('-')
            print(f'Error importing CHILD fields')


def create_table(dicom_object, table_cols, table_dict):
    for col in table_cols:
        try:
            table_dict[col].append(str(getattr(dicom_object, col)))
        except:
            table_dict[col].append('-')
            print(f'Error importing fields')
