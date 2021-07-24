# Here we have to add all the key field tag for each new child table
def child_id_cols():
    return ["00100020", "0020000d"]


# Here we have to specify for each key value, the table to be created on Redshift
def child_mapping_table():
    return {"00100020": "patient", "0020000d": "study"}


def main_cols():
    return [
        {"number": "00080005", "name": "SpecificCharacterSet"},
        {"number": "00080008", "name": "ImageType"},
        {"number": "00080016", "name": "SOPClassUID"},
        {"number": "00080018", "name": "SOPInstanceUID"},
        {"number": "00080020", "name": "StudyDate"},
        {"number": "00080030", "name": "StudyTime"},
        {"number": "00080050", "name": "AccessionNumber"},
        {"number": "00080060", "name": "Modality"},
        {"number": "00080070", "name": "Manufacturer"},
        {"number": "00080080", "name": "InstitutionName"},
        {"number": "00080081", "name": "InstitutionAddress"},
        {"number": "00080090", "name": "ReferringPhysicianName"},
        {"number": "00081030", "name": "StudyDescription"},
        {"number": "00081050", "name": "PerformingPhysicianName"},
        {"number": "00081140", "name": "ReferencedImageSequence"},
        {"number": "00082110", "name": "LossyImageCompression"},
        {"number": "00082112", "name": "SourceImageSequence"},
        {"number": "00090010", "name": "PrivateCreator"},
        {"number": "00100020", "name": "PatientID"},
        {"number": "00100060", "name": "KVP"},
        {"number": "00181063", "name": "FrameTime"},
        {"number": "00181152", "name": "Exposure"},
        {"number": "00181155", "name": "RadiationSetting"},
        {"number": "00181500", "name": "PositionerMotion"},
        {"number": "00181510", "name": "PositionerPrimaryAngle"},
        {"number": "00181511", "name": "PositionerSecondaryAngle"},
        {"number": "00191030", "name": "[MaximumFrameSize]"},
        {"number": "0020000d", "name": "StudyInstanceUID"},
        {"number": "00211013", "name": "[ImageSequenceNumber]"},
        {"number": "00280002", "name": "SamplesperPixel"},
        {"number": "00280004", "name": "PhotometricInterpretation"},
        {"number": "00280008", "name": "NumberofFrames"},
        {"number": "00280009", "name": "FrameIncrementPointer"},
        {"number": "00280010", "name": "Rows"},
        {"number": "00280011", "name": "Columns"},
        {"number": "00280100", "name": "BitsAllocated"},
        {"number": "00280101", "name": "BitsStored"},
        {"number": "00280102", "name": "HighBit"},
        {"number": "00280103", "name": "PixelRepresentation"},
        {"number": "00281040", "name": "PixelIntensityRelationship"},
        {"number": "00281090", "name": "RecommendedViewingMode"},
        {"number": "00286040", "name": "RWavePointer"},
        {"number": "00286100", "name": "MaskSubtractionSequence"},
        {"number": "00291000", "name": "Privatetagdata"},
        # {"number": "50000005", "name": "CurveDimensions"},
        # {"number": "50000010", "name": "NumberofPoints"},
        # {"number": "50000020", "name": "TypeofData"},
        # {"number": "50000030", "name": "AxisUnits"},
        # {"number": "50000103", "name": "DataValueRepresentation"},
        # {"number": "50000104", "name": "MinimumCoordinateValue"},
        # {"number": "50000105", "name": "MaximumCoordinateValue"},
        # {"number": "50000106", "name": "CurveRange"},
        # {"number": "50000110", "name": "CurveDataDescriptor"},
        # {"number": "50000112", "name": "CoordinateStartValue"},
        # {"number": "50000114", "name": "CoordinateStepValue"},
        # {"number": "50003000", "name": "CurveData"},
        #    {'number': '7fe00010', 'name': 'PixelData'}
    ]


# For each new table, we have to specify the columns and a 'id' field as below
def patient_cols():
    return [
        {"number": "id", "name": "id"},
        {"number": "00100020", "name": "PatientID"},
        {"number": "00100010", "name": "PatientName"},
        {"number": "00100030", "name": "PatientBirthDate"},
        {"number": "00100040", "name": "PatientSex"},
    ]


def study_cols():
    return [
        {"number": "id", "name": "id"},
        {"number": "0020000d", "name": "StudyInstanceUID"},
        {"number": "0020000e", "name": "SeriesInstanceUID"},
        {"number": "00200010", "name": "StudyID"},
        {"number": "00200011", "name": "SeriesNumber"},
        {"number": "00200013", "name": "InstanceNumber"},
        {"number": "00200020", "name": "PatientOrientation"},
    ]
