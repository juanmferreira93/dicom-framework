from processor.tables import main_cols, patient_cols, child_id_cols
import gc
import os

import pandas as pd
from pydicom import dcmread

main_table_cols = main_cols()
child_ids = child_id_cols()
# Child tables. Each new child table must be declared here.
# todo: Improve this.
patient_table_cols = patient_cols()

main_table_dict = {col: [] for col in main_table_cols}
# Child tables. For each new child table user must declare a dict for it.
# todo: Improve this.
patient_table_dict = {col: [] for col in patient_table_cols}


def to_csv():
    global main_table_dict
    # Child tables. For each new child table user must require the dict here.
    # todo: Improve this.
    global patient_table_dict

    dicom_files = os.listdir('data/dicom_files/')

    for dicom in dicom_files:
        print(f'Reading dicom_file: {dicom}')
        dicom_object = dcmread(f'data/dicom_files/{dicom}')

        create_csv(dicom_object)

    main_table_df = pd.DataFrame(main_table_dict)
    # Child tables. For each new child table user must declare a df for it.
    # todo: Improve this.
    patient_table_df = pd.DataFrame(patient_table_dict)

    del main_table_dict
    # Child tables. For each new child table user must delete the dict here.
    # todo: Improve this.
    del patient_table_dict
    gc.collect()

    main_table_df.to_csv('data/csv_files/main_table.csv', index=False)
    patient_table_df.to_csv('data/csv_files/patient_table.csv', index=False)


def create_csv(dicom_object):
    global main_table_cols
    global main_table_dict
    global child_ids

    for col in main_table_cols:
        try:
            value = str(getattr(dicom_object, col))

            if col in child_ids:
                if value in patient_table_dict[col]:
                    id = patient_table_dict[col].index(value) + 1
                    main_table_dict[col].append(str(id))
                else:
                    id = len(main_table_dict[col]) + 1
                    main_table_dict[col].append(str(id))

                    create_patient_csv(id, dicom_object)
            else:
                main_table_dict[col].append(value)
        except:
            main_table_dict[col].append('-')
            filename = dicom_object.filename.split('/')[2]
            # print(f'Error importing Main: {col} from {filename}')


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
            # print(f'Error importing Patient: {col} from {filename}')
