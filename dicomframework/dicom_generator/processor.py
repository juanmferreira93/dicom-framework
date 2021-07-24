import gc

import pandas as pd
from awsservice.redshift import write
from dicom_generator.column_mapping import *


class Processor:
    def __init__(self):
        # Supported modalities
        self.supported_modalities = ["XA"]

        # Get cols for each table
        self.main_cols = main_cols()
        self.child_ids = child_id_cols()

        ##### Child tables #####
        self.patient_cols = patient_cols()
        self.study_cols = study_cols()
        # self.xxx_cols = xxx_cols()
        ##### Finish cols section #####

        # Initialize one dict for each table
        self.main_dict = {col["name"]: [] for col in self.main_cols}

        ##### Child dicts #####
        self.patient_dict = {col["name"]: [] for col in self.patient_cols}
        self.study_dict = {col["name"]: [] for col in self.study_cols}
        # self.xxx._dict = {col['name']: [] for col in self.xxx_cols}
        ##### Finish dict initialization #####

    # Replace this method with awsservice.redshift.write method
    def create_csv(self):
        main_df = pd.DataFrame(self.main_dict)
        main_df.to_csv("data/csv_files/main.csv", index=False)

        ##### Child CSVs #####
        patient_df = pd.DataFrame(self.patient_dict)
        patient_df.to_csv("data/csv_files/patient.csv", index=False)

        study_df = pd.DataFrame(self.study_dict)
        study_df.to_csv("data/csv_files/study.csv", index=False)
        ##### Finish CSV creations #####

        write(main_df, "main_table")
        write(patient_df, "patient_table")
        write(study_df, "study_table")

    def clean(self):
        # This code deletes dicts
        del self.main_dict

        ##### Child dicts #####
        del self.patient_dict
        del self.study_dict
        gc.collect()
        ##### Finish dict deletion #####