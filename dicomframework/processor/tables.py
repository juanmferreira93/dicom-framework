def child_id_cols():
    return['PatitntID']


def header_cols():
    return ['FileMetaInformationGroupLength',
            'FileMetaInformationVersion',
            'MediaStorageSOPClassUID',
            'MediaStorageSOPInstanceUID',
            'TransferSyntaxUID',
            'ImplementationClassUID',
            'SourceApplicationEntityTitle']


def fact_cols():
    return['SpecificCharacterSet',
           'ImageType',
           'SOPClassUID',
           'SOPInstanceUID',
           'StudyDate',
           'StudyTime',
           'AccessionNumber',
           'Modality',
           'Manufacturer',
           'InstitutionName',
           'InstitutionAddress',
           'ReferringPhysicianName',
           'StudyDescription',
           'PerformingPhysicianName',
           'ReferencedImageSequence',
           'LossyImageCompression',
           'SourceImageSequence',
           'PrivateCreator',
           'PatientID',
           'KVP',
           'FrameTime',
           'Exposure',
           'RadiationSetting',
           'PositionerMotion',
           'PositionerPrimaryAngle',
           'Positioner Secondary Angle',
           '[Maximum Frame Size]',
           'StudyInstanceUID',
           'SeriesInstanceUID',
           'StudyID',
           'SeriesNumber',
           'InstanceNumber',
           'PatientOrientation',
           '[Image Sequence Number]',
           'SamplesperPixel',
           'PhotometricInterpretation',
           'NumberofFrames',
           'FrameIncrementPointer',
           'Rows',
           'Columns',
           'BitsAllocated',
           'BitsStored',
           'HighBit',
           'PixelRepresentation',
           'PixelIntensityRelationship',
           'RecommendedViewingMode',
           'RWavePointer',
           'MaskSubtractionSequence',
           'Privatetagdata',
           'CurveDimensions',
           'NumberofPoints',
           'TypeofData',
           'AxisUnits',
           'DataValueRepresentation',
           'MinimumCoordinateValue',
           'MaximumCoordinateValue',
           'CurveRange',
           'CurveDataDescriptor',
           'CoordinateStartValue',
           'CoordinateStepValue',
           'CurveData',
           'PixelData'
           ]


def patient_cols():
    return ['id',
            'PatientName',
            'PatientID',
            'PatientBirthDate',
            'PatientSex']