from pydicom import dcmread
import os
import pandas as pd
from tqdm import tqdm
import gc


def read():
    for file in os.listdir('data/dicom_files'):
        ds = dcmread(f'data/dicom_files/{file}')
        print(ds)
        # df = pd.read_json(ds.to_json())
        # df.to_csv(f'data/csv_files/{file}.csv', index=False, header=True)
        # print(f'Reading dicom_file: {file}')
        # print(ds.Modality)


def to_csv():
    # All columns for which we want to collect information
    # Still need to define how we will work with sequences
    meta_cols = ['ImageType', 'SOPClassUID', 'SOPInstanceUID', 'StudyDate', 'StudyTime', 'AccessionNumber', 'Modality', 'Manufacturer',
                 'InstitutionName', 'InstitutionAddress', 'StudyDescription', 'SourceImageSequence']

    # Initialize dictionary to collect the metadata
    col_dict_test = {col: [] for col in meta_cols}

    # Get values from files
    dicom_files = os.listdir('data/dicom_files/')
    for dicom in tqdm(dicom_files):
        print(f'Reading dicom_file: {dicom}')
        dicom_object = dcmread(f'data/dicom_files/{dicom}')
        for col in meta_cols:
            col_dict_test[col].append(str(getattr(dicom_object, col)))

    # Store all information in a DataFrame and run garbage collector
    meta_df_test = pd.DataFrame(col_dict_test)
    del col_dict_test
    gc.collect()

    # Specify numeric columns
    # num_cols = ['BitsAllocated', 'BitsStored', 'Columns', 'HighBit', 'Rows',
    #             'PixelRepresentation', 'SamplesPerPixel']

    # Split to get proper PatientIDs
    # meta_df_test['PatientID'] = meta_df_test['PatientID'].str.split(
    #     "_", n=3, expand=True)[1]

    # Convert all numeric cols to floats
    # for col in num_cols:
    #     meta_df_test[col] = meta_df_test[col].fillna(-9999).astype(float)

    # Save to CSV
    meta_df_test.to_csv('data/csv_files/test.csv', index=False)
