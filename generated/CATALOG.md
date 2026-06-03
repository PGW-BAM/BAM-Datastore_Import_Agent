# bam-masterdata CATALOG

Generated: 2026-06-02T00:00:00Z
bam-masterdata SHA: 39c0c77dd209b8b5951eb5e2275c78eab9fab400
bam-masterdata commit date: 2026-06-01 10:10:07 +0200
Source: C:/Users/pgerards/repos/bam-masterdata/bam_masterdata/datamodel/

This catalog enumerates every existing entity type (ObjectType, ExperimentalStep, VocabularyType, CollectionType, DatasetType) discovered by recursive scan of `bam_masterdata/datamodel/**/*.py` (excluding files whose basename starts with `_`). Every row carries a real `file:line` citation. The Welding subpackage is broken out into its own section because it underpins the FB7.2 welded fatigue workflow.

---

## ObjectTypes

Source file: `bam_masterdata/datamodel/object_types.py` unless noted otherwise.

| Class | openBIS code | File | Line |
|---|---|---|---|
| SearchQuery | SEARCH_QUERY | bam_masterdata/datamodel/object_types.py | 5 |
| GeneralElnSettings | GENERAL_ELN_SETTINGS | bam_masterdata/datamodel/object_types.py | 49 |
| Entry | ENTRY | bam_masterdata/datamodel/object_types.py | 66 |
| GeneralProtocol | GENERAL_PROTOCOL | bam_masterdata/datamodel/object_types.py | 110 |
| ExperimentalStep | EXPERIMENTAL_STEP | bam_masterdata/datamodel/object_types.py | 235 |
| Storage | STORAGE | bam_masterdata/datamodel/object_types.py | 371 |
| StoragePosition | STORAGE_POSITION | bam_masterdata/datamodel/object_types.py | 461 |
| Supplier | SUPPLIER | bam_masterdata/datamodel/object_types.py | 551 |
| Product | PRODUCT | bam_masterdata/datamodel/object_types.py | 696 |
| Request | REQUEST | bam_masterdata/datamodel/object_types.py | 813 |
| Order | ORDER | bam_masterdata/datamodel/object_types.py | 876 |
| Publication | PUBLICATION | bam_masterdata/datamodel/object_types.py | 984 |
| Calibration | CALIBRATION | bam_masterdata/datamodel/object_types.py | 1073 |
| AuxiliaryMaterial | AUXILIARY_MATERIAL | bam_masterdata/datamodel/object_types.py | 1173 |
| Instrument | INSTRUMENT | bam_masterdata/datamodel/object_types.py | 1254 |
| **TestingMachine** | **TESTING_MACHINE** | bam_masterdata/datamodel/object_types.py | **1488** |
| Document | DOCUMENT | bam_masterdata/datamodel/object_types.py | 1769 |
| GasBottle | GAS_BOTTLE | bam_masterdata/datamodel/object_types.py | 1850 |
| TestObject | TEST_OBJECT | bam_masterdata/datamodel/object_types.py | 2082 |
| Project | PROJECT | bam_masterdata/datamodel/object_types.py | 2270 |
| Person | PERSON | bam_masterdata/datamodel/object_types.py | 2463 |
| Control | CONTROL | bam_masterdata/datamodel/object_types.py | 2552 |
| Task | TASK | bam_masterdata/datamodel/object_types.py | 2615 |
| SpecificPersonInfo | SPECIFIC_PERSON_INFO | bam_masterdata/datamodel/object_types.py | 2706 |
| Sop | SOP | bam_masterdata/datamodel/object_types.py | 2761 |
| Sample | SAMPLE | bam_masterdata/datamodel/object_types.py | 2898 |
| Chemical | CHEMICAL | bam_masterdata/datamodel/object_types.py | 3086 |
| Organism | ORGANISM | bam_masterdata/datamodel/object_types.py | 3354 |
| BamGentechFacility | BAM_GENTECH_FACILITY | bam_masterdata/datamodel/object_types.py | 3473 |
| GlassWare | GLASS_WARE | bam_masterdata/datamodel/object_types.py | 3625 |
| StorageConnector | STORAGE_CONNECTOR | bam_masterdata/datamodel/object_types.py | 3792 |
| Action | ACTION | bam_masterdata/datamodel/object_types.py | 3836 |
| RawMaterialCode | RAW_MATERIAL_CODE | bam_masterdata/datamodel/object_types.py | 3890 |
| ParameterSet | PARAMETER_SET | bam_masterdata/datamodel/object_types.py | 3979 |
| EnvironmentalConditions | ENVIRONMENTAL_CONDITIONS | bam_masterdata/datamodel/object_types.py | 4041 |
| SampleNdt | SAMPLE_NDT | bam_masterdata/datamodel/object_types.py | 4103 |
| SampleHolder | SAMPLE_HOLDER | bam_masterdata/datamodel/object_types.py | 4174 |
| SamplePretreatment | SAMPLE_PRETREATMENT | bam_masterdata/datamodel/object_types.py | 4255 |
| InstrumentAccessory | INSTRUMENT_ACCESSORY | bam_masterdata/datamodel/object_types.py | 4299 |
| ComputationalAnalysis | COMPUTATIONAL_ANALYSIS | bam_masterdata/datamodel/object_types.py | 4352 |
| CondaEnvironment | CONDA_ENVIRONMENT | bam_masterdata/datamodel/object_types.py | 4414 |
| Hpc | HPC | bam_masterdata/datamodel/object_types.py | 4485 |
| InteratomicPotential | INTERATOMIC_POTENTIAL | bam_masterdata/datamodel/object_types.py | 4641 |
| JupyterNotebook | JUPYTER_NOTEBOOK | bam_masterdata/datamodel/object_types.py | 4740 |
| Pseudopotential | PSEUDOPOTENTIAL | bam_masterdata/datamodel/object_types.py | 4820 |
| PyironJob | PYIRON_JOB | bam_masterdata/datamodel/object_types.py | 4947 |
| SoftwareCode | SOFTWARE_CODE | bam_masterdata/datamodel/object_types.py | 5108 |
| WorkflowReference | WORKFLOW_REFERENCE | bam_masterdata/datamodel/object_types.py | 5206 |
| MaterialV1 | MATERIAL_V1 | bam_masterdata/datamodel/object_types.py | 5268 |
| MatSimStructure | MAT_SIM_STRUCTURE | bam_masterdata/datamodel/object_types.py | 5358 |
| **Fcg** (FCG specimen — closest peer to a "WeldedFatigueSpecimen") | **SPECIMEN.FCG** | bam_masterdata/datamodel/object_types.py | **6156** |
| Steel | RAW_MATERIAL.STEEL | bam_masterdata/datamodel/object_types.py | 6295 |
| Aluminium | RAW_MATERIAL.ALUMINIUM | bam_masterdata/datamodel/object_types.py | 6634 |
| Test | SETUP.TEST | bam_masterdata/datamodel/object_types.py | 7537 |

Subtotal ObjectTypes (main `object_types.py`): 52

## ExperimentalSteps

ExperimentalStep base lives in `object_types.py:235`. The following ExperimentalStep subclasses live in `object_types.py`:

| Class | openBIS code | File | Line |
|---|---|---|---|
| Dcpd | EXPERIMENTAL_STEP.DCPD | bam_masterdata/datamodel/object_types.py | 5474 |
| **FcgTest** (closest peer to a welded-fatigue test step) | **EXPERIMENTAL_STEP.FCG_TEST** | bam_masterdata/datamodel/object_types.py | **5591** |
| RazorbladeNotching | EXPERIMENTAL_STEP.RAZORBLADE_NOTCHING | bam_masterdata/datamodel/object_types.py | 5680 |
| **FcgStep** | **EXPERIMENTAL_STEP.FCG_STEP** | bam_masterdata/datamodel/object_types.py | **5724** |
| MicroscopyFcgFractureSurfaceCracklength | EXPERIMENTAL_STEP.MICROSCOPY_FCG_FRACTURE_SURFACE_CRACKLENGTH | bam_masterdata/datamodel/object_types.py | 6101 |
| FcgEvaluation | EXPERIMENTAL_STEP.FCG_EVALUATION | bam_masterdata/datamodel/object_types.py | 6137 |
| ImageSeries | EXPERIMENTAL_STEP.IMAGE_SERIES | bam_masterdata/datamodel/object_types.py | 7762 |
| ProfileScan | EXPERIMENTAL_STEP.PROFILE_SCAN | bam_masterdata/datamodel/object_types.py | 7806 |
| VideoRecording | EXPERIMENTAL_STEP.VIDEO_RECORDING | bam_masterdata/datamodel/object_types.py | 7841 |
| Ftir | EXPERIMENTAL_STEP.FTIR | bam_masterdata/datamodel/object_types.py | 8215 |
| Sem | EXPERIMENTAL_STEP.SEM | bam_masterdata/datamodel/object_types.py | 8287 |
| Nmr | EXPERIMENTAL_STEP.NMR | bam_masterdata/datamodel/object_types.py | 8394 |
| Tem | EXPERIMENTAL_STEP.TEM | bam_masterdata/datamodel/object_types.py | 8523 |
| Dls | EXPERIMENTAL_STEP.DLS | bam_masterdata/datamodel/object_types.py | 8693 |
| MsBatch | EXPERIMENTAL_STEP.MS_BATCH | bam_masterdata/datamodel/object_types.py | 9142 |
| RmEthanol | EXPERIMENTAL_STEP.RM_ETHANOL | bam_masterdata/datamodel/object_types.py | 9791 |
| ThermographicMeasurement | EXPERIMENTAL_STEP.THERMOGRAPHIC_MEASUREMENT | bam_masterdata/datamodel/object_types.py | 10347 |
| SaxsMeasurement | EXPERIMENTAL_STEP.SAXS_MEASUREMENT | bam_masterdata/datamodel/object_types.py | 10457 |
| MeasurementSession | EXPERIMENTAL_STEP.MEASUREMENT_SESSION | bam_masterdata/datamodel/object_types.py | 11430 |
| LaserDiffPSDMeasurement | EXPERIMENTAL_STEP.LASER_DIFF_PSD_MEASUREMENT | bam_masterdata/datamodel/object_types.py | 11501 |
| PowderXRDMeasurement | EXPERIMENTAL_STEP.PXRD_MEASUREMENT | bam_masterdata/datamodel/object_types.py | 11685 |

Subtotal ExperimentalSteps (main file): 21 (excluding the `ExperimentalStep` base at line 235, which is itself defined as an ObjectType subclass).

## VocabularyTypes

Source file: `bam_masterdata/datamodel/vocabulary_types.py` unless noted otherwise.

| Class | Code | File | Line |
|---|---|---|---|
| DefaultCollectionViews | $DEFAULT_COLLECTION_VIEWS | bam_masterdata/datamodel/vocabulary_types.py | 5 |
| StorageFormat | $STORAGE_FORMAT | bam_masterdata/datamodel/vocabulary_types.py | 24 |
| AccuracyClassVde0410 | ACCURACY_CLASS_VDE0410 | bam_masterdata/datamodel/vocabulary_types.py | 43 |
| AtomisticCalcType | ATOMISTIC_CALC_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 92 |
| AtomKpointType | ATOM_KPOINT_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 129 |
| AtomPotentialStyle | ATOM_POTENTIAL_STYLE | bam_masterdata/datamodel/vocabulary_types.py | 154 |
| AtomXcFunctional | ATOM_XC_FUNCTIONAL | bam_masterdata/datamodel/vocabulary_types.py | 203 |
| AuxiliaryMaterialType | AUXILIARY_MATERIAL_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 252 |
| BamFieldOfActivity | BAM_FIELD_OF_ACTIVITY | bam_masterdata/datamodel/vocabulary_types.py | 319 |
| BamFocusArea | BAM_FOCUS_AREA | bam_masterdata/datamodel/vocabulary_types.py | 506 |
| BravaisLattice | BRAVAIS_LATTICE | bam_masterdata/datamodel/vocabulary_types.py | 543 |
| BuildingMaterialType | BUILDING_MATERIAL_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 640 |
| CalibrationProvider | CALIBRATION_PROVIDER | bam_masterdata/datamodel/vocabulary_types.py | 671 |
| CameraShutterMode | CAMERA_SHUTTER_MODE | bam_masterdata/datamodel/vocabulary_types.py | 690 |
| ChemicalProductCategory | CHEMICAL_PRODUCT_CATEGORY | bam_masterdata/datamodel/vocabulary_types.py | 709 |
| DcpdPotCal | DCPD_POT_CAL | bam_masterdata/datamodel/vocabulary_types.py | 956 |
| DfgDeviceCode | DFG_DEVICE_CODE | bam_masterdata/datamodel/vocabulary_types.py | 975 |
| DocumentType | DOCUMENT_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 27550 |
| ElectronicSmearing | ELECTRONIC_SMEARING | bam_masterdata/datamodel/vocabulary_types.py | 27701 |
| EvaluationFileType | EVALUATION_FILE_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 27744 |
| FcgStepType | FCG_STEP_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 27781 |
| FlashLampShape | FLASH_LAMP_SHAPE | bam_masterdata/datamodel/vocabulary_types.py | 27836 |
| FtirAccessories | FTIR_ACCESSORIES | bam_masterdata/datamodel/vocabulary_types.py | 27861 |
| GentechSafetyLevel | GENTECH_SAFETY_LEVEL | bam_masterdata/datamodel/vocabulary_types.py | 27892 |
| HeatingAreaDesc | HEATING_AREA_DESC | bam_masterdata/datamodel/vocabulary_types.py | 27923 |
| HeatingPrinciple | HEATING_PRINCIPLE | bam_masterdata/datamodel/vocabulary_types.py | 27948 |
| InstrumentStatus | INSTRUMENT_STATUS | bam_masterdata/datamodel/vocabulary_types.py | 27985 |
| LaserType | LASER_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 28022 |
| LoadFrameOrientation | LOAD_FRAME_ORIENTATION | bam_masterdata/datamodel/vocabulary_types.py | 28095 |
| MassSpecType | MASS_SPEC_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 28114 |
| MaterialUsageTechnikum | MATERIAL_USAGE_TECHNIKUM | bam_masterdata/datamodel/vocabulary_types.py | 28163 |
| MatScale | MAT_SCALE | bam_masterdata/datamodel/vocabulary_types.py | 28194 |
| MatStructure | MAT_STRUCTURE | bam_masterdata/datamodel/vocabulary_types.py | 28243 |
| MeasuringAmplifierType | MEASURING_AMPLIFIER_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 28268 |
| MicroscopyFcgCracklengthType | MICROSCOPY_FCG_CRACKLENGTH_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 28287 |
| MinimizationAlgo | MINIMIZATION_ALGO | bam_masterdata/datamodel/vocabulary_types.py | 28312 |
| MurnEqnOfState | MURN_EQN_OF_STATE | bam_masterdata/datamodel/vocabulary_types.py | 28391 |
| NmrExperimentTypes | NMR_EXPERIMENT_TYPES | bam_masterdata/datamodel/vocabulary_types.py | 28422 |
| NmrNuclei | NMR_NUCLEI | bam_masterdata/datamodel/vocabulary_types.py | 28507 |
| NmrSolvents | NMR_SOLVENTS | bam_masterdata/datamodel/vocabulary_types.py | 28610 |
| NotchTypeFcg | NOTCH_TYPE_FCG | bam_masterdata/datamodel/vocabulary_types.py | 28695 |
| NucPerformed | NUC_PERFORMED | bam_masterdata/datamodel/vocabulary_types.py | 28720 |
| OperatingSystem | OPERATING_SYSTEM | bam_masterdata/datamodel/vocabulary_types.py | 28745 |
| OpticalSpectrometerType | OPTICAL_SPECTROMETER_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 28794 |
| OrganismFootnoteZkbs | ORGANISM_FOOTNOTE_ZKBS | bam_masterdata/datamodel/vocabulary_types.py | 28825 |
| OrganismGroup | ORGANISM_GROUP | bam_masterdata/datamodel/vocabulary_types.py | 28880 |
| OrganismRiskGroup | ORGANISM_RISK_GROUP | bam_masterdata/datamodel/vocabulary_types.py | 28947 |
| PhysicalState | PHYSICAL_STATE | bam_masterdata/datamodel/vocabulary_types.py | 28984 |
| PlasmidBacterialAntibioticResistance | PLASMID_BACTERIAL_ANTIBIOTIC_RESISTANCE | bam_masterdata/datamodel/vocabulary_types.py | 29009 |
| PlasmidOri | PLASMID_ORI | bam_masterdata/datamodel/vocabulary_types.py | 29076 |
| PositionerType | POSITIONER_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 29119 |
| ProjectStatus | PROJECT_STATUS | bam_masterdata/datamodel/vocabulary_types.py | 29156 |
| PseudopotFunctional | PSEUDOPOT_FUNCTIONAL | bam_masterdata/datamodel/vocabulary_types.py | 29187 |
| PseudopotType | PSEUDOPOT_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 29212 |
| PublicationStatus | PUBLICATION_STATUS | bam_masterdata/datamodel/vocabulary_types.py | 29243 |
| PublicationType | PUBLICATION_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 29292 |
| QueuingSystem | QUEUING_SYSTEM | bam_masterdata/datamodel/vocabulary_types.py | 29329 |
| RawMatForm | RAW_MAT_FORM | bam_masterdata/datamodel/vocabulary_types.py | 29366 |
| RawMatTreatmentAlu | RAW_MAT_TREATMENT_ALU | bam_masterdata/datamodel/vocabulary_types.py | 29409 |
| RawMatTreatmentSteel | RAW_MAT_TREATMENT_STEEL | bam_masterdata/datamodel/vocabulary_types.py | 29494 |
| RobotType | ROBOT_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 29597 |
| RtdAccuracyClass | RTD_ACCURACY_CLASS | bam_masterdata/datamodel/vocabulary_types.py | 29628 |
| RtdConnectionType | RTD_CONNECTION_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 29665 |
| RtdInsulationMaterial | RTD_INSULATION_MATERIAL | bam_masterdata/datamodel/vocabulary_types.py | 29690 |
| RtdType | RTD_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 29721 |
| SampleHolderMaterial | SAMPLE_HOLDER_MATERIAL | bam_masterdata/datamodel/vocabulary_types.py | 29806 |
| ShortRngOrd | SHORT_RNG_ORD | bam_masterdata/datamodel/vocabulary_types.py | 29855 |
| SpaceGroup | SPACE_GROUP | bam_masterdata/datamodel/vocabulary_types.py | 29880 |
| **SpecimenStatus** | **SPECIMEN_STATUS** | bam_masterdata/datamodel/vocabulary_types.py | **31267** |
| **SpecimenTypeFcgTest** | **SPECIMEN_TYPE_FCG_TEST** | bam_masterdata/datamodel/vocabulary_types.py | **31304** |
| SubframeType | SUBFRAME_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 31341 |
| TemporalHeatingStructure | TEMPORAL_HEATING_STRUCTURE | bam_masterdata/datamodel/vocabulary_types.py | 31372 |
| TestingMachineDriveType | TESTING_MACHINE_DRIVE_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 31409 |
| TestingMachineLoadType | TESTING_MACHINE_LOAD_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 31452 |
| TestFileType | TEST_FILE_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 31483 |
| TestObjectStatus | TEST_OBJECT_STATUS | bam_masterdata/datamodel/vocabulary_types.py | 31532 |
| TestProgramType | TEST_PROGRAM_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 31551 |
| TestSetupType | TEST_SETUP_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 31588 |
| TestSoftware | TEST_SOFTWARE | bam_masterdata/datamodel/vocabulary_types.py | 31607 |
| ThermocoupleType | THERMOCOUPLE_TYPE | bam_masterdata/datamodel/vocabulary_types.py | 31650 |
| ThermodynEnsemble | THERMODYN_ENSEMBLE | bam_masterdata/datamodel/vocabulary_types.py | 31717 |
| ThermographicSetupConfig | THERMOGRAPHIC_SETUP_CONFIG | bam_masterdata/datamodel/vocabulary_types.py | 31760 |
| ThermographicSetupHsOrient | THERMOGRAPHIC_SETUP_HS_ORIENT | bam_masterdata/datamodel/vocabulary_types.py | 31785 |
| UnitMass | UNIT_MASS | bam_masterdata/datamodel/vocabulary_types.py | 31810 |
| WeatherCondition | WEATHER_CONDITION | bam_masterdata/datamodel/vocabulary_types.py | 31853 |
| WindDirection | WIND_DIRECTION | bam_masterdata/datamodel/vocabulary_types.py | 31896 |
| OrderStatus | $ORDER.ORDER_STATUS | bam_masterdata/datamodel/vocabulary_types.py | 31952 |
| Currency | $PRODUCT.CURRENCY | bam_masterdata/datamodel/vocabulary_types.py | 31984 |
| StorageValidationLevel | $STORAGE.STORAGE_VALIDATION_LEVEL | bam_masterdata/datamodel/vocabulary_types.py | 32010 |
| StorageBoxSize | $STORAGE_POSITION.STORAGE_BOX_SIZE | bam_masterdata/datamodel/vocabulary_types.py | 32036 |
| Language | $SUPPLIER.LANGUAGE | bam_masterdata/datamodel/vocabulary_types.py | 32086 |
| PreferredOrderMethod | $SUPPLIER.PREFERRED_ORDER_METHOD | bam_masterdata/datamodel/vocabulary_types.py | 32106 |
| ColorEncodedAnnotations | $WELL.COLOR_ENCODED_ANNOTATIONS | bam_masterdata/datamodel/vocabulary_types.py | 32132 |
| TriggerSetting | IR_CAMERA.TRIGGER_SETTING | bam_masterdata/datamodel/vocabulary_types.py | 32152 |
| ScatteringModelPSDLD | SCATTERING_MODEL_PSD_LD | bam_masterdata/datamodel/vocabulary_types.py | 32183 |

Subtotal VocabularyTypes (main `vocabulary_types.py`): 96

## CollectionTypes

| Class | Code | File | Line |
|---|---|---|---|
| Collection | COLLECTION | bam_masterdata/datamodel/collection_types.py | 8 |
| DefaultExperiment | DEFAULT_EXPERIMENT | bam_masterdata/datamodel/collection_types.py | 46 |

Subtotal CollectionTypes: 2

## DatasetTypes

| Class | Code | File | Line |
|---|---|---|---|
| ElnPreview | ELN_PREVIEW | bam_masterdata/datamodel/dataset_types.py | 5 |
| RawData | RAW_DATA | bam_masterdata/datamodel/dataset_types.py | 42 |
| ProcessedData | PROCESSED_DATA | bam_masterdata/datamodel/dataset_types.py | 79 |
| AnalyzedData | ANALYZED_DATA | bam_masterdata/datamodel/dataset_types.py | 116 |
| Attachment | ATTACHMENT | bam_masterdata/datamodel/dataset_types.py | 153 |
| OtherData | OTHER_DATA | bam_masterdata/datamodel/dataset_types.py | 190 |
| SourceCode | SOURCE_CODE | bam_masterdata/datamodel/dataset_types.py | 227 |
| AnalysisNotebook | ANALYSIS_NOTEBOOK | bam_masterdata/datamodel/dataset_types.py | 264 |
| PublicationData | PUBLICATION_DATA | bam_masterdata/datamodel/dataset_types.py | 311 |
| Document | DOCUMENT | bam_masterdata/datamodel/dataset_types.py | 348 |
| TestFile | TEST_FILE | bam_masterdata/datamodel/dataset_types.py | 426 |
| LogFile | LOG_FILE | bam_masterdata/datamodel/dataset_types.py | 504 |
| MeasurementProtocolFile | MEASUREMENT_PROTOCOL_FILE | bam_masterdata/datamodel/dataset_types.py | 541 |
| Norm | NORM | bam_masterdata/datamodel/dataset_types.py | 598 |
| CompEnv | COMP_ENV | bam_masterdata/datamodel/dataset_types.py | 736 |
| MatModel | MAT_MODEL | bam_masterdata/datamodel/dataset_types.py | 793 |
| PyironJob | PYIRON_JOB | bam_masterdata/datamodel/dataset_types.py | 881 |
| SourceCodeWorkflow | SOURCE_CODE_WORKFLOW | bam_masterdata/datamodel/dataset_types.py | 968 |
| Figure | FIGURE | bam_masterdata/datamodel/dataset_types.py | 1045 |
| MatSimStructure | MAT_SIM_STRUCTURE | bam_masterdata/datamodel/dataset_types.py | 1172 |

Subtotal DatasetTypes: 20

---

## Welding subpackage (`bam_masterdata/datamodel/welding/`)

This subpackage is the primary reuse target for the FB7.2 welded fatigue PRD. All ObjectType / ExperimentalStep / VocabularyType classes contributed by the welding subpackage are listed below. Note: the welding ObjectTypes inherit either `ObjectType`, `Instrument` (in `WeldingEquipment`), or each other (e.g., `WeldingEquipment` -> `GmawTorch`); `Weldment` inherits from `ExperimentalStep`. They are all reachable through the standard discovery rule (recursive glob of `datamodel/**/*.py`).

### ObjectTypes (welding)

| Class | Parent | openBIS code | File | Line |
|---|---|---|---|---|
| Welding | ObjectType | CONSUMABLE.WELDING | bam_masterdata/datamodel/welding/object_types.py | 7 |
| WeldingEquipment | Instrument | INSTRUMENT.WELDING_EQUIPMENT | bam_masterdata/datamodel/welding/object_types.py | 149 |
| GmawTorch | WeldingEquipment | INSTRUMENT.WELDING_EQUIPMENT.GMAW_TORCH | bam_masterdata/datamodel/welding/object_types.py | 166 |
| GmawWeldingPowerSource | WeldingEquipment | INSTRUMENT.WELDING_EQUIPMENT.GMAW_WELDING_POWER_SOURCE | bam_masterdata/datamodel/welding/object_types.py | 184 |
| Positioner | WeldingEquipment | INSTRUMENT.WELDING_EQUIPMENT.POSITIONER | bam_masterdata/datamodel/welding/object_types.py | 228 |
| RobotController | WeldingEquipment | INSTRUMENT.WELDING_EQUIPMENT.ROBOT_CONTROLLER | bam_masterdata/datamodel/welding/object_types.py | 264 |
| Robot | WeldingEquipment | INSTRUMENT.WELDING_EQUIPMENT.ROBOT | bam_masterdata/datamodel/welding/object_types.py | 299 |
| StationLayout | WeldingEquipment | INSTRUMENT.WELDING_EQUIPMENT.STATION_LAYOUT | bam_masterdata/datamodel/welding/object_types.py | 344 |
| WireSolid | Welding | CONSUMABLE.WELDING.WIRE_SOLID | bam_masterdata/datamodel/welding/object_types.py | 958 |

Subtotal welding ObjectTypes: 9

### ExperimentalSteps (welding)

| Class | Parent | openBIS code | File | Line |
|---|---|---|---|---|
| **Weldment** | ExperimentalStep | **EXPERIMENTAL_STEP.WELDMENT** | bam_masterdata/datamodel/welding/object_types.py | **357** |
| GmawBase | Weldment | EXPERIMENTAL_STEP.WELDMENT.GMAW_BASE | bam_masterdata/datamodel/welding/object_types.py | 420 |
| LaserHybridMagnet | Weldment | EXPERIMENTAL_STEP.WELDMENT.LASER_HYBRID_MAGNET | bam_masterdata/datamodel/welding/object_types.py | 509 |
| LaserMagnet | Weldment | EXPERIMENTAL_STEP.WELDMENT.LASER_MAGNET | bam_masterdata/datamodel/welding/object_types.py | 670 |

Subtotal welding ExperimentalSteps: 4

### VocabularyTypes (welding)

| Class | Code | Terms (count + values) | File | Line |
|---|---|---|---|---|
| GmawTorchType | WELDING.GMAW_TORCH_TYPE | 4 (WELDING_GMAW_TORCH_TYPE_NGW_ROT, WELDING_GMAW_TORCH_TYPE_NGW_SWING, WELDING_GMAW_TORCH_TYPE_SINGLE, WELDING_GMAW_TORCH_TYPE_TANDEM) | bam_masterdata/datamodel/welding/vocabularies.py | 6 |
| **WeldType** | **WELDING.WELD_TYPE** | **6 (WELDING_FILLET_WELD, WELDING_GROOVE_WELD, WELDING_PLUG_WELD, WELDING_SPOT_WELD, WELDING_SURFACING_WELD, WELDING_TACK_WELD)** | bam_masterdata/datamodel/welding/vocabularies.py | **38** |

Subtotal welding VocabularyTypes: 2

### WeldType term details (FB7.2-relevant)

WeldType (`WELDING.WELD_TYPE`) — defined at `bam_masterdata/datamodel/welding/vocabularies.py:38` — currently exposes the following six terms:

| Term code | Label | File | Line |
|---|---|---|---|
| WELDING_FILLET_WELD | fillet weld | bam_masterdata/datamodel/welding/vocabularies.py | 44 |
| WELDING_GROOVE_WELD | groove weld | bam_masterdata/datamodel/welding/vocabularies.py | 50 |
| WELDING_PLUG_WELD | plug weld | bam_masterdata/datamodel/welding/vocabularies.py | 56 |
| WELDING_SPOT_WELD | spot weld | bam_masterdata/datamodel/welding/vocabularies.py | 62 |
| WELDING_SURFACING_WELD | surfacing weld | bam_masterdata/datamodel/welding/vocabularies.py | 68 |
| WELDING_TACK_WELD | tack weld | bam_masterdata/datamodel/welding/vocabularies.py | 74 |

---

## FB7.2 quick-reference (welded fatigue PRD focus areas)

These are the existing closest-peer entities that should be the REUSE / EXTEND targets for a future `WeldedFatigueSpecimen` workflow:

- **TestingMachine** (`TESTING_MACHINE`) — `bam_masterdata/datamodel/object_types.py:1488`
- **Fcg** specimen (`SPECIMEN.FCG`) — `bam_masterdata/datamodel/object_types.py:6156` (closest existing peer to a "WeldedFatigueSpecimen")
- **FcgTest** ExperimentalStep (`EXPERIMENTAL_STEP.FCG_TEST`) — `bam_masterdata/datamodel/object_types.py:5591`
- **FcgStep** ExperimentalStep (`EXPERIMENTAL_STEP.FCG_STEP`) — `bam_masterdata/datamodel/object_types.py:5724`
- **FcgEvaluation** ExperimentalStep (`EXPERIMENTAL_STEP.FCG_EVALUATION`) — `bam_masterdata/datamodel/object_types.py:6137`
- **Weldment** ExperimentalStep (`EXPERIMENTAL_STEP.WELDMENT`) — `bam_masterdata/datamodel/welding/object_types.py:357`
- **WeldType** VocabularyType (`WELDING.WELD_TYPE`) — `bam_masterdata/datamodel/welding/vocabularies.py:38`
- **SpecimenStatus** VocabularyType (`SPECIMEN_STATUS`) — `bam_masterdata/datamodel/vocabulary_types.py:31267`
- **SpecimenTypeFcgTest** VocabularyType (`SPECIMEN_TYPE_FCG_TEST`) — `bam_masterdata/datamodel/vocabulary_types.py:31304`
- **NotchTypeFcg** VocabularyType (`NOTCH_TYPE_FCG`) — `bam_masterdata/datamodel/vocabulary_types.py:28695`
- **TestingMachineDriveType** (`TESTING_MACHINE_DRIVE_TYPE`) — `bam_masterdata/datamodel/vocabulary_types.py:31409`
- **TestingMachineLoadType** (`TESTING_MACHINE_LOAD_TYPE`) — `bam_masterdata/datamodel/vocabulary_types.py:31452`

---

## Totals

| Entity kind | Count |
|---|---|
| ObjectTypes (main `object_types.py`) | 52 |
| ExperimentalSteps (main `object_types.py`) | 21 |
| VocabularyTypes (main `vocabulary_types.py`) | 96 |
| CollectionTypes | 2 |
| DatasetTypes | 20 |
| Welding ObjectTypes | 9 |
| Welding ExperimentalSteps | 4 |
| Welding VocabularyTypes | 2 |
| **GRAND TOTAL ObjectTypes (incl. welding)** | **61** |
| **GRAND TOTAL ExperimentalSteps (incl. welding)** | **25** |
| **GRAND TOTAL VocabularyTypes (incl. welding)** | **98** |
| **GRAND TOTAL CollectionTypes** | **2** |
| **GRAND TOTAL DatasetTypes** | **20** |
