# bam-masterdata CATALOG

bam-masterdata SHA: 3cc15ca71348af09f222924ff01f8e1ac6d1b734
bam-masterdata commit date: 2026-11-02 18:07:39 +0100
Generator: `tools/build_catalog.py` (AST, full inheritance resolution — deterministic)

Every row cites `file:line`. `Parent` is the direct base class; inherited
properties are listed in `generated/catalog.json`.

## ObjectTypes (149)

| Class | Code | Parent | Own props | File:Line |
|---|---|---|---|---|
| BuildingMaterialsSpecimen | SAMPLE.BUILDING_MATERIALS_SPECIMEN | Sample | 15 | bam_masterdata/datamodel/v0/building_materials/object_types.py:5 |
| ConcreteMixture | SAMPLE.CONCRETE_MIXTURE | Sample | 9 | bam_masterdata/datamodel/v0/building_materials/object_types.py:154 |
| CreepTestMaterialHistoryAndCondition | CREEP_TEST_MATERIAL_HISTORY_AND_CONDITION | ObjectType | 46 | bam_masterdata/datamodel/v0/creep_test/object_types.py:374 |
| CreepTestChemicalCompositionNominal | CREEP_TEST_CHEMICAL_COMPOSITION_NOMINAL | ObjectType | 4 | bam_masterdata/datamodel/v0/creep_test/object_types.py:787 |
| CreepTestChemicalCompositionMeasured | CREEP_TEST_CHEMICAL_COMPOSITION_MEASURED | ObjectType | 4 | bam_masterdata/datamodel/v0/creep_test/object_types.py:829 |
| CreepTestMaterialHistoryNDTResults | CREEP_TEST_MATERIAL_HISTORY_NDT_RESULTS | ObjectType | 2 | bam_masterdata/datamodel/v0/creep_test/object_types.py:871 |
| CreepTestMaterialHistoryMechanicalTestsResults | CREEP_TEST_MATERIAL_HISTORY_MECHANICAL_TESTS_RESULTS | ObjectType | 3 | bam_masterdata/datamodel/v0/creep_test/object_types.py:896 |
| CreepTestTestPiece | SAMPLE.CREEP_TEST_TEST_PIECE | Sample | 10 | bam_masterdata/datamodel/v0/creep_test/object_types.py:931 |
| CreepTestTestMachine | TESTING_MACHINE.CREEP_TEST_TEST_MACHINE | TestingMachine | 11 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1023 |
| CreepTestTestMachineHeatingSystem | INSTRUMENT.CREEP_TEST_TEST_MACHINE_HEATING_SYSTEM | Instrument | 1 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1129 |
| CreepTestTestPieceHolderSystem | INSTRUMENT_ACCESSORY.CREEP_TEST_TEST_PIECE_HOLDER_SYSTEM | InstrumentAccessory | 1 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1146 |
| CreepTestTestMachineLoadingSystem | INSTRUMENT.CREEP_TEST_TEST_MACHINE_LOADING_SYSTEM | Instrument | 9 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1163 |
| CreepTestTestMachineDataAcquisition | INSTRUMENT.CREEP_TEST_TEST_MACHINE_DATA_ACQUISITION | Instrument | 5 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1246 |
| CreepTestLoadSensor | INSTRUMENT.CREEP_TEST_LOAD_SENSOR | Instrument | 8 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1295 |
| CreepTestLoadDataAcquisition | CREEP_TEST_LOAD_DATA_ACQUISITION | ObjectType | 1 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1370 |
| CreepTestLaboratoryConditions | ENVIRONMENTAL_CONDITIONS.CREEP_TEST_LABORATORY_CONDITIONS | EnvironmentalConditions | 2 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1386 |
| CreepTestTemperatureMeasuringSystem | INSTRUMENT.CREEP_TEST_TEMPERATURE_MEASURING_SYSTEM | Instrument | 2 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1410 |
| CreepTestTemperatureSensor | INSTRUMENT.CREEP_TEST_TEMPERATURE_SENSOR | Instrument | 16 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1436 |
| CreepTestTemperatureDataAcquisition | INSTRUMENT.CREEP_TEST_TEMPERATURE_DATA_ACQUISITION | Instrument | 9 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1584 |
| CreepTestExtensometerSystem | INSTRUMENT.CREEP_TEST_EXTENSOMETER_SYSTEM | Instrument | 3 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1670 |
| CreepTestExtensionValuesContactingExtensometer | INSTRUMENT.CREEP_TEST_EXTENSION_VALUES_CONTACTING_EXTENSOMETER | Instrument | 18 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1706 |
| CreepTestElongationValuesAndCrossSectionalDimensions | INSTRUMENT.CREEP_TEST_ELONGATION_VALUES_AND_CROSS_SECTIONAL_DIMENSIONS | Instrument | 13 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1867 |
| CreepTestDataProcessingProcedures | COMPUTATIONAL_ANALYSIS.CREEP_TEST_DATA_PROCESSING_PROCEDURES | ComputationalAnalysis | 6 | bam_masterdata/datamodel/v0/creep_test/object_types.py:1985 |
| CreepTestPrimaryValuesRecordedAtTestStart | CREEP_TEST_PRIMARY_VALUES_RECORDED_AT_TEST_START | ObjectType | 9 | bam_masterdata/datamodel/v0/creep_test/object_types.py:2042 |
| CreepTestValuesRecordedDuringTestRunBase | CREEP_TEST_VALUES_RECORDED_DURING_TEST_RUN_BASE | ObjectType | 4 | bam_masterdata/datamodel/v0/creep_test/object_types.py:2132 |
| CreepTestPrimaryValuesRecordedDuringTestRun | CREEP_TEST_VALUES_RECORDED_DURING_TEST_RUN_BASE.CREEP_TEST_PRIMARY_VALUES_RECORDED_DURING_TEST_RUN | CreepTestValuesRecordedDuringTestRunBase | 3 | bam_masterdata/datamodel/v0/creep_test/object_types.py:2177 |
| CreepTestPrimaryValuesRecordedAfterEndOfTest | CREEP_TEST_PRIMARY_VALUES_RECORDED_AFTER_END_OF_TEST | ObjectType | 3 | bam_masterdata/datamodel/v0/creep_test/object_types.py:2214 |
| CreepTestSecondaryValuesRecordedDuringTestRun | CREEP_TEST_VALUES_RECORDED_DURING_TEST_RUN_BASE.CREEP_TEST_SECONDARY_VALUES_RECORDED_DURING_TEST_RUN | CreepTestValuesRecordedDuringTestRunBase | 5 | bam_masterdata/datamodel/v0/creep_test/object_types.py:2250 |
| CreepTestSecondaryElongationValues | CREEP_TEST_SECONDARY_ELONGATION_VALUES | ObjectType | 3 | bam_masterdata/datamodel/v0/creep_test/object_types.py:2306 |
| CreepTestSecondaryExtensionValues | CREEP_TEST_SECONDARY_EXTENSION_VALUES | ObjectType | 6 | bam_masterdata/datamodel/v0/creep_test/object_types.py:2342 |
| Ellipsometer | INSTRUMENT.ELLIPSOMETER | Instrument | 21 | bam_masterdata/datamodel/v0/ellipsometry/object_types.py:6 |
| ForceTransducer | INSTRUMENT.FORCE_TRANSDUCER | Instrument | 5 | bam_masterdata/datamodel/v0/instruments.py:5 |
| HydraulicCylinder | INSTRUMENT.HYDRAULIC_CYLINDER | Instrument | 5 | bam_masterdata/datamodel/v0/instruments.py:58 |
| HydraulicMisc | INSTRUMENT.HYDRAULIC_MISC | Instrument | 2 | bam_masterdata/datamodel/v0/instruments.py:111 |
| Servovalve | INSTRUMENT.SERVOVALVE | Instrument | 6 | bam_masterdata/datamodel/v0/instruments.py:137 |
| LoadFrame | INSTRUMENT.LOAD_FRAME | Instrument | 6 | bam_masterdata/datamodel/v0/instruments.py:199 |
| AlignmentFixture | INSTRUMENT.ALIGNMENT_FIXTURE | Instrument | 2 | bam_masterdata/datamodel/v0/instruments.py:262 |
| Thermocouple | INSTRUMENT.THERMOCOUPLE | Instrument | 6 | bam_masterdata/datamodel/v0/instruments.py:288 |
| Rtd | INSTRUMENT.RTD | Instrument | 9 | bam_masterdata/datamodel/v0/instruments.py:351 |
| Nanovoltmeter | INSTRUMENT.NANOVOLTMETER | Instrument | 12 | bam_masterdata/datamodel/v0/instruments.py:444 |
| PowerSupply | INSTRUMENT.POWER_SUPPLY | Instrument | 7 | bam_masterdata/datamodel/v0/instruments.py:560 |
| MeasuringAmplifier | INSTRUMENT.MEASURING_AMPLIFIER | Instrument | 14 | bam_masterdata/datamodel/v0/instruments.py:631 |
| LaserLineScanner | INSTRUMENT.LASER_LINE_SCANNER | Instrument | 9 | bam_masterdata/datamodel/v0/instruments.py:766 |
| Centrifuge | INSTRUMENT.CENTRIFUGE | Instrument | 8 | bam_masterdata/datamodel/v0/instruments.py:855 |
| CentrifugeRotor | INSTRUMENT.CENTRIFUGE_ROTOR | Instrument | 5 | bam_masterdata/datamodel/v0/instruments.py:935 |
| Freezer2 | INSTRUMENT.FREEZER | Instrument | 2 | bam_masterdata/datamodel/v0/instruments.py:989 |
| Scale | INSTRUMENT.SCALE | Instrument | 4 | bam_masterdata/datamodel/v0/instruments.py:1015 |
| SpectrometerOptical | INSTRUMENT.SPECTROMETER_OPTICAL | Instrument | 3 | bam_masterdata/datamodel/v0/instruments.py:1060 |
| LaserGeneral | INSTRUMENT.LASER_GENERAL | Instrument | 6 | bam_masterdata/datamodel/v0/instruments.py:1096 |
| FlashLamp | INSTRUMENT.FLASH_LAMP | Instrument | 2 | bam_masterdata/datamodel/v0/instruments.py:1159 |
| ObjectiveSpacer | INSTRUMENT.OBJECTIVE_SPACER | Instrument | 1 | bam_masterdata/datamodel/v0/instruments.py:1186 |
| LocalWorkstation | INSTRUMENT.LOCAL_WORKSTATION | Instrument | 1 | bam_masterdata/datamodel/v0/instruments.py:1203 |
| Camera | INSTRUMENT.CAMERA | Instrument | 8 | bam_masterdata/datamodel/v0/instruments.py:1221 |
| Lens | INSTRUMENT.CAMERA.LENS | Camera | 4 | bam_masterdata/datamodel/v0/instruments.py:1301 |
| MassSpec | INSTRUMENT.MASS_SPEC | Instrument | 4 | bam_masterdata/datamodel/v0/mass_spectrometry/object_types.py:73 |
| LcSystem | INSTRUMENT.LC_SYSTEM | Instrument | 2 | bam_masterdata/datamodel/v0/mass_spectrometry/object_types.py:121 |
| GcSystem | INSTRUMENT.GC_SYSTEM | Instrument | 2 | bam_masterdata/datamodel/v0/mass_spectrometry/object_types.py:149 |
| SearchQuery | SEARCH_QUERY | ObjectType | 4 | bam_masterdata/datamodel/v0/object_types.py:5 |
| GeneralElnSettings | GENERAL_ELN_SETTINGS | ObjectType | 1 | bam_masterdata/datamodel/v0/object_types.py:49 |
| Entry | ENTRY | ObjectType | 4 | bam_masterdata/datamodel/v0/object_types.py:66 |
| TestMethod | TEST_METHOD | ObjectType | 2 | bam_masterdata/datamodel/v0/object_types.py:110 |
| GeneralProtocol | GENERAL_PROTOCOL | ObjectType | 13 | bam_masterdata/datamodel/v0/object_types.py:137 |
| Storage | STORAGE | ObjectType | 9 | bam_masterdata/datamodel/v0/object_types.py:400 |
| StoragePosition | STORAGE_POSITION | ObjectType | 9 | bam_masterdata/datamodel/v0/object_types.py:490 |
| Supplier | SUPPLIER | ObjectType | 15 | bam_masterdata/datamodel/v0/object_types.py:580 |
| Product | PRODUCT | ObjectType | 12 | bam_masterdata/datamodel/v0/object_types.py:725 |
| Request | REQUEST | ObjectType | 6 | bam_masterdata/datamodel/v0/object_types.py:842 |
| Order | ORDER | ObjectType | 11 | bam_masterdata/datamodel/v0/object_types.py:905 |
| Publication | PUBLICATION | ObjectType | 9 | bam_masterdata/datamodel/v0/object_types.py:1013 |
| Calibration | CALIBRATION | ObjectType | 10 | bam_masterdata/datamodel/v0/object_types.py:1102 |
| AuxiliaryMaterial | AUXILIARY_MATERIAL | ObjectType | 8 | bam_masterdata/datamodel/v0/object_types.py:1202 |
| Tool | TOOL | ObjectType | 11 | bam_masterdata/datamodel/v0/object_types.py:1283 |
| Instrument | INSTRUMENT | ObjectType | 24 | bam_masterdata/datamodel/v0/object_types.py:1397 |
| MeasuringInstrument | MEASURING_INSTRUMENT | ObjectType | 11 | bam_masterdata/datamodel/v0/object_types.py:1631 |
| TestingMachine | TESTING_MACHINE | ObjectType | 29 | bam_masterdata/datamodel/v0/object_types.py:1744 |
| TestingEquipment | TESTING_EQUIPMENT | ObjectType | 10 | bam_masterdata/datamodel/v0/object_types.py:2025 |
| Document | DOCUMENT | ObjectType | 11 | bam_masterdata/datamodel/v0/object_types.py:2128 |
| DataTransferPackage | DATA_TRANSFER_PACKAGE | ObjectType | 7 | bam_masterdata/datamodel/v0/object_types.py:2237 |
| GasBottle | GAS_BOTTLE | ObjectType | 24 | bam_masterdata/datamodel/v0/object_types.py:2310 |
| TestObject | TEST_OBJECT | ObjectType | 19 | bam_masterdata/datamodel/v0/object_types.py:2542 |
| TestObjectBAM | TEST_OBJECT_BAM | TestObject | 5 | bam_masterdata/datamodel/v0/object_types.py:2731 |
| TestObjectExternal | TEST_OBJECT_EXTERNAL | ObjectType | 13 | bam_masterdata/datamodel/v0/object_types.py:2785 |
| Project | PROJECT | ObjectType | 20 | bam_masterdata/datamodel/v0/object_types.py:2915 |
| Person | PERSON | ObjectType | 8 | bam_masterdata/datamodel/v0/object_types.py:3108 |
| Control | CONTROL | ObjectType | 6 | bam_masterdata/datamodel/v0/object_types.py:3188 |
| DataTransfer | DATA_TRANSFER | ObjectType | 6 | bam_masterdata/datamodel/v0/object_types.py:3251 |
| Task | TASK | ObjectType | 9 | bam_masterdata/datamodel/v0/object_types.py:3315 |
| SpecificPersonInfo | SPECIFIC_PERSON_INFO | ObjectType | 5 | bam_masterdata/datamodel/v0/object_types.py:3406 |
| Sop | SOP | ObjectType | 14 | bam_masterdata/datamodel/v0/object_types.py:3461 |
| Sample | SAMPLE | ObjectType | 19 | bam_masterdata/datamodel/v0/object_types.py:3598 |
| Chemical | CHEMICAL | ObjectType | 28 | bam_masterdata/datamodel/v0/object_types.py:3790 |
| Organism | ORGANISM | ObjectType | 12 | bam_masterdata/datamodel/v0/object_types.py:4058 |
| BamGentechFacility | BAM_GENTECH_FACILITY | ObjectType | 15 | bam_masterdata/datamodel/v0/object_types.py:4177 |
| GlassWare | GLASS_WARE | ObjectType | 17 | bam_masterdata/datamodel/v0/object_types.py:4329 |
| StorageConnector | STORAGE_CONNECTOR | ObjectType | 4 | bam_masterdata/datamodel/v0/object_types.py:4496 |
| Action | ACTION | ObjectType | 5 | bam_masterdata/datamodel/v0/object_types.py:4540 |
| RawMaterialCode | RAW_MATERIAL_CODE | ObjectType | 9 | bam_masterdata/datamodel/v0/object_types.py:4594 |
| ParameterSet | PARAMETER_SET | ObjectType | 6 | bam_masterdata/datamodel/v0/object_types.py:4683 |
| EnvironmentalConditions | ENVIRONMENTAL_CONDITIONS | ObjectType | 6 | bam_masterdata/datamodel/v0/object_types.py:4745 |
| Measurement | MEASUREMENT | ObjectType | 2 | bam_masterdata/datamodel/v0/object_types.py:4807 |
| SampleNdt | SAMPLE_NDT | ObjectType | 7 | bam_masterdata/datamodel/v0/object_types.py:4833 |
| SampleHolder | SAMPLE_HOLDER | ObjectType | 8 | bam_masterdata/datamodel/v0/object_types.py:4904 |
| SamplePretreatment | SAMPLE_PRETREATMENT | ObjectType | 4 | bam_masterdata/datamodel/v0/object_types.py:4985 |
| InstrumentAccessory | INSTRUMENT_ACCESSORY | ObjectType | 5 | bam_masterdata/datamodel/v0/object_types.py:5029 |
| ComputationalAnalysis | COMPUTATIONAL_ANALYSIS | ObjectType | 6 | bam_masterdata/datamodel/v0/object_types.py:5082 |
| CondaEnvironment | CONDA_ENVIRONMENT | ObjectType | 7 | bam_masterdata/datamodel/v0/object_types.py:5144 |
| Hpc | HPC | ObjectType | 16 | bam_masterdata/datamodel/v0/object_types.py:5215 |
| InteratomicPotential | INTERATOMIC_POTENTIAL | ObjectType | 10 | bam_masterdata/datamodel/v0/object_types.py:5371 |
| JupyterNotebook | JUPYTER_NOTEBOOK | ObjectType | 8 | bam_masterdata/datamodel/v0/object_types.py:5470 |
| Pseudopotential | PSEUDOPOTENTIAL | ObjectType | 13 | bam_masterdata/datamodel/v0/object_types.py:5550 |
| PyironJob | PYIRON_JOB | ObjectType | 17 | bam_masterdata/datamodel/v0/object_types.py:5677 |
| SoftwareCode | SOFTWARE_CODE | ObjectType | 10 | bam_masterdata/datamodel/v0/object_types.py:5838 |
| WorkflowReference | WORKFLOW_REFERENCE | ObjectType | 6 | bam_masterdata/datamodel/v0/object_types.py:5936 |
| MaterialV1 | MATERIAL_V1 | ObjectType | 9 | bam_masterdata/datamodel/v0/object_types.py:5998 |
| MatSimStructure | MAT_SIM_STRUCTURE | ObjectType | 12 | bam_masterdata/datamodel/v0/object_types.py:6088 |
| Fcg | SPECIMEN.FCG | ObjectType | 14 | bam_masterdata/datamodel/v0/object_types.py:6205 |
| Steel | RAW_MATERIAL.STEEL | ObjectType | 36 | bam_masterdata/datamodel/v0/object_types.py:6344 |
| Aluminium | RAW_MATERIAL.ALUMINIUM | ObjectType | 35 | bam_masterdata/datamodel/v0/object_types.py:6683 |
| Test | SETUP.TEST | ObjectType | 9 | bam_masterdata/datamodel/v0/object_types.py:7013 |
| Bam | PERSON.BAM | Person | 4 | bam_masterdata/datamodel/v0/object_types.py:7103 |
| Freezer1 | CONTROL.FREEZER | Control | 2 | bam_masterdata/datamodel/v0/object_types.py:7149 |
| MsCenter | PROJECT.MS_CENTER | Project | 8 | bam_masterdata/datamodel/v0/object_types.py:7175 |
| Technikum | SAMPLE.TECHNIKUM | Sample | 3 | bam_masterdata/datamodel/v0/object_types.py:7256 |
| GmoDonor | SAMPLE.GMO_DONOR | Sample | 3 | bam_masterdata/datamodel/v0/object_types.py:7292 |
| GmoRecipient | SAMPLE.GMO_RECIPIENT | Sample | 4 | bam_masterdata/datamodel/v0/object_types.py:7330 |
| Plasmid | SAMPLE.PLASMID | Sample | 5 | bam_masterdata/datamodel/v0/object_types.py:7378 |
| Gmo | SAMPLE.GMO | Sample | 10 | bam_masterdata/datamodel/v0/object_types.py:7434 |
| DeviceTraining | ACTION.DEVICE_TRAINING | Action | 1 | bam_masterdata/datamodel/v0/object_types.py:7537 |
| DeviceUsage | ACTION.DEVICE_USAGE | Action | 2 | bam_masterdata/datamodel/v0/object_types.py:7555 |
| IrCameraAcquisition | PARAMETER_SET.IR_CAMERA_ACQUISITION | ParameterSet | 16 | bam_masterdata/datamodel/v0/object_types.py:7581 |
| ThermographySetup | PARAMETER_SET.THERMOGRAPHY_SETUP | ParameterSet | 5 | bam_masterdata/datamodel/v0/object_types.py:7736 |
| ThermographyHeating | PARAMETER_SET.THERMOGRAPHY_HEATING | ParameterSet | 10 | bam_masterdata/datamodel/v0/object_types.py:7791 |
| BamLaboratory | ENVIRONMENTAL_CONDITIONS.BAM_LABORATORY | EnvironmentalConditions | 5 | bam_masterdata/datamodel/v0/object_types.py:7892 |
| Outdoor | ENVIRONMENTAL_CONDITIONS.OUTDOOR | EnvironmentalConditions | 7 | bam_masterdata/datamodel/v0/object_types.py:7950 |
| Named | SAMPLE_NDT.NAMED | SampleNdt | 9 | bam_masterdata/datamodel/v0/object_types.py:8023 |
| Lammps | PYIRON_JOB.LAMMPS | PyironJob | 31 | bam_masterdata/datamodel/v0/object_types.py:8115 |
| Murnaghan | PYIRON_JOB.MURNAGHAN | PyironJob | 8 | bam_masterdata/datamodel/v0/object_types.py:8405 |
| Vasp | PYIRON_JOB.VASP | PyironJob | 32 | bam_masterdata/datamodel/v0/object_types.py:8486 |
| Amorphous | MAT_SIM_STRUCTURE.AMORPHOUS | MatSimStructure | 4 | bam_masterdata/datamodel/v0/object_types.py:8788 |
| Crystal | MAT_SIM_STRUCTURE.CRYSTAL | MatSimStructure | 12 | bam_masterdata/datamodel/v0/object_types.py:8833 |
| Welding | CONSUMABLE.WELDING | ObjectType | 14 | bam_masterdata/datamodel/v0/welding/object_types.py:7 |
| WeldingEquipment | INSTRUMENT.WELDING_EQUIPMENT | Instrument | 1 | bam_masterdata/datamodel/v0/welding/object_types.py:149 |
| GmawTorch | INSTRUMENT.WELDING_EQUIPMENT.GMAW_TORCH | WeldingEquipment | 1 | bam_masterdata/datamodel/v0/welding/object_types.py:166 |
| GmawWeldingPowerSource | INSTRUMENT.WELDING_EQUIPMENT.GMAW_WELDING_POWER_SOURCE | WeldingEquipment | 4 | bam_masterdata/datamodel/v0/welding/object_types.py:184 |
| Positioner | INSTRUMENT.WELDING_EQUIPMENT.POSITIONER | WeldingEquipment | 3 | bam_masterdata/datamodel/v0/welding/object_types.py:228 |
| RobotController | INSTRUMENT.WELDING_EQUIPMENT.ROBOT_CONTROLLER | WeldingEquipment | 3 | bam_masterdata/datamodel/v0/welding/object_types.py:264 |
| Robot | INSTRUMENT.WELDING_EQUIPMENT.ROBOT | WeldingEquipment | 4 | bam_masterdata/datamodel/v0/welding/object_types.py:299 |
| StationLayout | INSTRUMENT.WELDING_EQUIPMENT.STATION_LAYOUT | WeldingEquipment | 0 | bam_masterdata/datamodel/v0/welding/object_types.py:344 |
| WireSolid | CONSUMABLE.WELDING.WIRE_SOLID | Welding | 6 | bam_masterdata/datamodel/v0/welding/object_types.py:958 |

## ExperimentalSteps (35)

| Class | Code | Parent | Own props | File:Line |
|---|---|---|---|---|
| Dcpd | EXPERIMENTAL_STEP.DCPD | ExperimentalStep | 12 | bam_masterdata/datamodel/v0/activities.py:5 |
| FcgTest | EXPERIMENTAL_STEP.FCG_TEST | ExperimentalStep | 9 | bam_masterdata/datamodel/v0/activities.py:122 |
| RazorbladeNotching | EXPERIMENTAL_STEP.RAZORBLADE_NOTCHING | ExperimentalStep | 4 | bam_masterdata/datamodel/v0/activities.py:211 |
| FcgStep | EXPERIMENTAL_STEP.FCG_STEP | ExperimentalStep | 35 | bam_masterdata/datamodel/v0/activities.py:255 |
| MicroscopyFcgFractureSurfaceCracklength | EXPERIMENTAL_STEP.MICROSCOPY_FCG_FRACTURE_SURFACE_CRACKLENGTH | ExperimentalStep | 3 | bam_masterdata/datamodel/v0/activities.py:579 |
| FcgEvaluation | EXPERIMENTAL_STEP.FCG_EVALUATION | ExperimentalStep | 1 | bam_masterdata/datamodel/v0/activities.py:615 |
| ImageSeries | EXPERIMENTAL_STEP.IMAGE_SERIES | ExperimentalStep | 4 | bam_masterdata/datamodel/v0/activities.py:633 |
| ProfileScan | EXPERIMENTAL_STEP.PROFILE_SCAN | ExperimentalStep | 3 | bam_masterdata/datamodel/v0/activities.py:677 |
| VideoRecording | EXPERIMENTAL_STEP.VIDEO_RECORDING | ExperimentalStep | 7 | bam_masterdata/datamodel/v0/activities.py:712 |
| Ftir | EXPERIMENTAL_STEP.FTIR | ExperimentalStep | 7 | bam_masterdata/datamodel/v0/activities.py:784 |
| Sem | EXPERIMENTAL_STEP.SEM | ExperimentalStep | 11 | bam_masterdata/datamodel/v0/activities.py:856 |
| Nmr | EXPERIMENTAL_STEP.NMR | ExperimentalStep | 13 | bam_masterdata/datamodel/v0/activities.py:963 |
| Tem | EXPERIMENTAL_STEP.TEM | ExperimentalStep | 18 | bam_masterdata/datamodel/v0/activities.py:1092 |
| Dls | EXPERIMENTAL_STEP.DLS | ExperimentalStep | 49 | bam_masterdata/datamodel/v0/activities.py:1262 |
| RmEthanol | EXPERIMENTAL_STEP.RM_ETHANOL | ExperimentalStep | 2 | bam_masterdata/datamodel/v0/activities.py:1711 |
| ThermographicMeasurement | EXPERIMENTAL_STEP.THERMOGRAPHIC_MEASUREMENT | ExperimentalStep | 1 | bam_masterdata/datamodel/v0/activities.py:1737 |
| SaxsMeasurement | EXPERIMENTAL_STEP.SAXS_MEASUREMENT | ExperimentalStep | 5 | bam_masterdata/datamodel/v0/activities.py:1755 |
| MeasurementSession | EXPERIMENTAL_STEP.MEASUREMENT_SESSION | ExperimentalStep | 2 | bam_masterdata/datamodel/v0/activities.py:1808 |
| LaserDiffPSDMeasurement | EXPERIMENTAL_STEP.LASER_DIFF_PSD_MEASUREMENT | ExperimentalStep | 18 | bam_masterdata/datamodel/v0/activities.py:1835 |
| PowderXRDMeasurement | EXPERIMENTAL_STEP.PXRD_MEASUREMENT | ExperimentalStep | 11 | bam_masterdata/datamodel/v0/activities.py:2008 |
| MouseMeasurement | EXPERIMENTAL_STEP.SAXS_MEASUREMENT.MOUSE_MEASUREMENT | SaxsMeasurement | 6 | bam_masterdata/datamodel/v0/activities.py:2132 |
| MechanicalTest | EXPERIMENTAL_STEP.MECHANICAL_TEST | ExperimentalStep | 0 | bam_masterdata/datamodel/v0/activities.py:2196 |
| CreepTest | EXPERIMENTAL_STEP.MECHANICAL_TEST.CREEP_TEST | MechanicalTest | 37 | bam_masterdata/datamodel/v0/creep_test/object_types.py:14 |
| Ellipsometry | EXPERIMENTAL_STEP.ELLIPSOMETRY | ExperimentalStep | 10 | bam_masterdata/datamodel/v0/ellipsometry/object_types.py:237 |
| EllipsometryInSitu | EXPERIMENTAL_STEP.ELLIPSOMETRY.ELLIPSOMETRY_IN_SITU | Ellipsometry | 3 | bam_masterdata/datamodel/v0/ellipsometry/object_types.py:363 |
| EllipsometryInSituTemperature | EXPERIMENTAL_STEP.ELLIPSOMETRY.ELLIPSOMETRY_IN_SITU.ELLIPSOMETRY_IN_SITU_TEMPERATURE | EllipsometryInSitu | 8 | bam_masterdata/datamodel/v0/ellipsometry/object_types.py:411 |
| EllipsometryMapping | EXPERIMENTAL_STEP.ELLIPSOMETRY_MAPPING | Ellipsometry | 2 | bam_masterdata/datamodel/v0/ellipsometry/object_types.py:527 |
| EllipsometryImaging | EXPERIMENTAL_STEP.ELLIPSOMETRY_IMAGING | Ellipsometry | 10 | bam_masterdata/datamodel/v0/ellipsometry/object_types.py:560 |
| MsBatch | EXPERIMENTAL_STEP.MS_BATCH | ExperimentalStep | 6 | bam_masterdata/datamodel/v0/mass_spectrometry/object_types.py:6 |
| SIMS | EXPERIMENTAL_STEP.SIMS | ExperimentalStep | 20 | bam_masterdata/datamodel/v0/mass_spectrometry/object_types.py:177 |
| ExperimentalStep | EXPERIMENTAL_STEP | ObjectType | 14 | bam_masterdata/datamodel/v0/object_types.py:262 |
| Weldment | EXPERIMENTAL_STEP.WELDMENT | ExperimentalStep | 6 | bam_masterdata/datamodel/v0/welding/object_types.py:357 |
| GmawBase | EXPERIMENTAL_STEP.WELDMENT.GMAW_BASE | Weldment | 9 | bam_masterdata/datamodel/v0/welding/object_types.py:420 |
| LaserHybridMagnet | EXPERIMENTAL_STEP.WELDMENT.LASER_HYBRID_MAGNET | Weldment | 17 | bam_masterdata/datamodel/v0/welding/object_types.py:509 |
| LaserMagnet | EXPERIMENTAL_STEP.WELDMENT.LASER_MAGNET | Weldment | 29 | bam_masterdata/datamodel/v0/welding/object_types.py:670 |

## VocabularyTypes (152)

| Class | Code | Terms | File:Line |
|---|---|---|---|
| BuildingMaterialType | BUILDING_MATERIAL_TYPE | 9: BITUMINOUS, MINERAL, PLASTIC, WOOD, CONCRETE, CLAY, NATURAL_STONE, OTHER, METAL | bam_masterdata/datamodel/v0/building_materials/vocabularies.py:5 |
| BuildingMaterialsTestMachine | BUILDING_MATERIALS_TEST_MACHINE | 5: 10MN, 5MN, 1MN, SEIDNER, TONI | bam_masterdata/datamodel/v0/building_materials/vocabularies.py:66 |
| CreepTestStandard | CREEP_TEST_STANDARD | 3: DIN_EN_ISO_204, ASTM_E139, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:5 |
| TypeOfLoading | CREEP_TEST_TYPE_OF_LOADING | 3: TENSION, COMPRESSION, BENDING | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:30 |
| LoadControlType | CREEP_TEST_LOAD_CONTROL_TYPE | 2: CONSTANT_FORCE, CONSTANT_STRESS | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:55 |
| CreepTestType | CREEP_TEST_TYPE | 3: UNINTERRUPTED_CREEP_TESTS_CONTINUOUS_EXTENSION, INTERRUPTED_CREEP_TESTS_PERIODIC_ELONGATION, STRESS_RUPTURE_TESTS_TIME_TO_FRACTURE_MEASURED | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:74 |
| EndOfTestCriterium | CREEP_TEST_END_OF_TEST_CRITERIUM | 4: TEST_PIECE_BREAK, TIME_LIMIT, EXTENSION_LIMIT, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:99 |
| InterruptionCourse | CREEP_TEST_INTERRUPTION_COURSE | 2: UNLOADING_BEFORE_COOLING, UNLOADING_AFTER_COOLING | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:130 |
| Solidification | CREEP_TEST_SOLIDIFICATION | 2: SINGLE_CRYSTAL, POLYCRYSTAL | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:149 |
| Condition | CREEP_TEST_CONDITION | 2: HEAT_TREATED, AS_MANUFACTURED | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:168 |
| HeatTreatmentState | CREEP_TEST_HEAT_TREATMENT_STATE | 4: NONE, ANNEALED, HARDENED, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:187 |
| MicrostructureFeature | CREEP_TEST_MICROSTRUCTURE_FEATURE | 9: MATRIX, PHASE, GRAIN_BOUNDARY, DENDRITE, PRECIPITATE, INCLUSION, GRAIN, SEGREGATION, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:218 |
| GrainSizeDeterminationMethod | CREEP_TEST_GRAIN_SIZE_DETERMINATION_METHOD | 3: LINE_INTERCEPT, CIRCULAR_INTERCEPT, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:279 |
| MeasuredCondition | CREEP_TEST_MEASURED_CONDITION | 4: AS_MANUFACTURED, HEAT_TREATED, AS_TESTED, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:304 |
| TestPieceTypeI | CREEP_TEST_TEST_PIECE_TYPE_I | 2: MINIATURIZED_SPECIMEN, SPECIMEN_ACCORDING_TO_STANDARD | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:335 |
| TestPieceTypeII | CREEP_TEST_TEST_PIECE_TYPE_II | 2: ROUND_CROSS_SECTION, RECTANGULAR_SECTION | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:354 |
| TestPieceTypeIII | CREEP_TEST_TEST_PIECE_TYPE_III | 4: SMOOTH_TEST_PIECE, NOTCHED_TEST_PIECE, COMBINED_TEST_PIECE, OTHER_TYPE_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:373 |
| CreepTestMachineType | CREEP_TEST_MACHINE_TYPE | 3: LEVER_ARM, ELECTROMECHANICAL_DRIVE, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:404 |
| CreepTestFurnaceType | CREEP_TEST_FURNACE_TYPE | 3: SPLIT_TUBE_FURNACE_WITH_TWO_ZONES, SPLIT_TUBE_FURNACE_WITH_THREE_ZONES, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:429 |
| CreepTestFixingTechnique | CREEP_TEST_FIXING_TECHNIQUE | 3: THREADED, BUTTON_HEAD, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:454 |
| CreepTestLoadSystemCalibrationStandard | CREEP_TEST_LOAD_SYSTEM_CALIBRATION_STANDARD | 2: DIN_EN_ISO_7500_2, OTHERS_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:479 |
| TemperatureSignal | CREEP_TEST_TEMPERATURE_SIGNAL | 3: ON_TEST_PIECE, VIA_FURNACE, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:498 |
| CreepTestSensorType | CREEP_TEST_SENSOR_TYPE | 2: THERMOCOUPLE, THERMOCAMERA | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:523 |
| CreepTestThermocoupleCalibrationMethod | CREEP_TEST_THERMOCOUPLE_CALIBRATION_METHOD | 2: COMPARISON_METHOD, FIX_POINT_METHOD | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:542 |
| CreepTestThermocoupleCalibrationStandard | CREEP_TEST_THERMOCOUPLE_CALIBRATION_STANDARD | 4: ASTM_E220, EURAMET_CG_08, GUIDELINE_DKD_R_5_3, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:561 |
| CreepTestThermocoupleContactMethod | CREEP_TEST_THERMOCOUPLE_CONTACT_METHOD | 5: WELDED, ATTACHED, PRESSED, GLUED, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:592 |
| CreepTestThermocoupleLocation | CREEP_TEST_THERMOCOUPLE_LOCATION | 2: INSIDE, OUTSIDE | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:629 |
| CreepTestReferenceJunction | CREEP_TEST_REFERENCE_JUNCTION | 2: INTERNAL, EXTERNAL | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:648 |
| CreepTestDataAcquisitionCalibrationStandard | CREEP_TEST_DATA_ACQUISITION_CALIBRATION_STANDARD | 2: EURAMET_CG_11, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:667 |
| CreepTestDisplacementMeasuringMethod | CREEP_TEST_DISPLACEMENT_MEASURING_METHOD | 2: CONTACTING_METHOD, NON_CONTACTING_METHOD | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:686 |
| CreepTestSensorTypeContactingMethod | CREEP_TEST_SENSOR_TYPE_CONTACTING_METHOD | 4: LVDT_WITH_EXTENSION_LEGS, CLIP_ON_EXTENSOMETER, ANALOG_DIAL_GAUGES, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:705 |
| CreepTestSensorTypeNonContactingMethod | CREEP_TEST_SENSOR_TYPE_NON_CONTACTING_METHOD | 3: LASEREXTENSOMETER, DIGITAL_IMAGE_CORRELATION_TECHNIQUE, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:736 |
| CreepTestMeasurementSetup | CREEP_TEST_MEASUREMENT_SETUP | 2: ONE_SIDED, TWO_SIDED | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:761 |
| CreepTestMeasurementDirection | CREEP_TEST_EXTENSION_MEASUREMENT_DIRECTION | 2: AXIAL_ACTION, DIAMETRICAL_ACTION | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:780 |
| CreepTestMountingType | CREEP_TEST_EXTENSOMETER_MOUNTING_TYPE | 3: AT_TEST_PIECE_IN_PARALLEL_LENGTH, AT_COLLARS, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:799 |
| ExtensometerLegMaterial | CREEP_TEST_EXTENSOMETER_LEG_MATERIAL | 2: CERAMIC_LEGS, METALLIC_LEGS | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:824 |
| MeasuringEquipment | CREEP_TEST_MEASURING_EQUIPMENT | 4: CALIPER_GAUGE, MEASURING_MICROSCOPE, MICROMETER_SCREW_GAUGE, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:843 |
| MeasuringEquipmentType | CREEP_TEST_MEASURING_EQUIPMENT_TYPE | 3: DIGITAL, ANALOG, OTHER_SPECIFY | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:874 |
| CreepTestDeterminationOfReferenceLength | CREEP_TEST_DETERMINATION_OF_REFERENCE_LENGTH | 2: CASE_1, CASE_2 | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:899 |
| CreepTestFracturePosition | CREEP_TEST_FRACTURE_POSITION | 9: CENTERED, WITHIN_THE_GAUGE_LENGTH, WITHIN_THE_GAUGE_LENGTH_AND_THE_PARALLEL_LENGTH, AT_THE_EDGE_OF_THE_UPPER_EXTENSOMETER_GAUGE_LENGTH, AT_THE_EDGE_OF_THE_LO... | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:921 |
| CreepTestCalibrationStatus | CREEP_TEST_CALIBRATION_STATUS | 5: CALIBRATED, NOT_CALIBRATED, EXPIRED, UNKNOWN, NOT_APPLICABLE | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:982 |
| CreepTestNumberOfThermocouples | CREEP_TEST_NUMBER_OF_THERMOCOUPLES | 3: ONE, TWO, THREE | bam_masterdata/datamodel/v0/creep_test/vocabularies.py:1046 |
| IonizationType | IONIZATION_TYPE | 4: ESI, EI, CI, APCI | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:5 |
| ChromatographyType | CHROMATOGRAPHY_TYPE | 7: LC, HPLC, UPLC, GC, SFC, IC, NONE | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:36 |
| DetectorType | DETECTOR_TYPE | 11: FID, ECD, MSMS, DAD, UV, QTOF, Q, QQQ, QTOF_ALT, TOF, FLD | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:85 |
| MsAcquisitionMode | MS_ACQUISITION_MODE | 5: FULL_SCAN, IDA, SWATH, MRM, SIM | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:158 |
| MsIonPolarity | MS_ION_POLARITY | 3: POSITIVE, NEGATIVE, POSITIVENEGATIVE | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:195 |
| MassSpecType | MASS_SPEC_TYPE | 7: ICP, MALDI, Q, QQQ, QTOF, TOF, TRAP | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:220 |
| SIMSPrimaryIon | SIMS_PRIMARY_ION | 11: BI1, BI2, BI3, BI4, BI5, BI6, BI7, BI1PP, BI3PP, BI5PP, BI7PP | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:269 |
| SIMSSputterSource | SIMS_SPUTTER_SOURCE | 2: OXYGEN, CESIUM | bam_masterdata/datamodel/v0/mass_spectrometry/vocabularies.py:342 |
| DefaultCollectionViews | $DEFAULT_COLLECTION_VIEWS | 2: FORM_VIEW, LIST_VIEW | bam_masterdata/datamodel/v0/vocabulary_types.py:5 |
| MeasurementQuantity | MEASUREMENT_QUANTITY | 5: TEMPERATURE, MOISTURE, WEIGHT, LENGTH, PRESSURE | bam_masterdata/datamodel/v0/vocabulary_types.py:24 |
| MeasuringInstrumentClassification | MEASURING_INSTRUMENT_CLASSIFICATION | 5: MECHANICAL, ELECTROMAGNETIC, ELECTROCHEMICAL, MAGNETIC, SPECTROSCOPIC | bam_masterdata/datamodel/v0/vocabulary_types.py:61 |
| StorageFormat | $STORAGE_FORMAT | 2: BDS_DIRECTORY, PROPRIETARY | bam_masterdata/datamodel/v0/vocabulary_types.py:98 |
| AccuracyClassVde0410 | ACCURACY_CLASS_VDE0410 | 7: ACCURACY_0.1, ACCURACY_0.2, ACCURACY_0.5, ACCURACY_1, ACCURACY_1.5, ACCURACY_2.5, ACCURACY_5 | bam_masterdata/datamodel/v0/vocabulary_types.py:117 |
| AtomisticCalcType | ATOMISTIC_CALC_TYPE | 5: ATOM_CALC_MC, ATOM_CALC_MD, ATOM_CALC_NEB, ATOM_CALC_SC, ATOM_CALC_STRUC_OPT | bam_masterdata/datamodel/v0/vocabulary_types.py:166 |
| AtomKpointType | ATOM_KPOINT_TYPE | 3: KPOINTS_KSPACING, KPOINTS_MANUAL, KPOINTS_MP | bam_masterdata/datamodel/v0/vocabulary_types.py:203 |
| AtomPotentialStyle | ATOM_POTENTIAL_STYLE | 7: POT_STYLE_EAM, POT_STYLE_FF, POT_STYLE_LJ, POT_STYLE_MEAM, POT_STYLE_MLIP, POT_STYLE_SW, POT_STYLE_UMLIP | bam_masterdata/datamodel/v0/vocabulary_types.py:228 |
| AtomXcFunctional | ATOM_XC_FUNCTIONAL | 7: XC_FUNC_B3LYP, XC_FUNC_HSE03, XC_FUNC_HSE06, XC_FUNC_LDA, XC_FUNC_PBE, XC_FUNC_PBE_SOL, XC_FUNC_SCAN0 | bam_masterdata/datamodel/v0/vocabulary_types.py:277 |
| AuxiliaryMaterialType | AUXILIARY_MATERIAL_TYPE | 10: ABRASIVE, ADHESIVE, CLEANER, FLUX, LUBRICANT, POLISHING_AGENT, RAZORBLADE, SOLDER, SOLVANT, WELDING_ADDITIVE | bam_masterdata/datamodel/v0/vocabulary_types.py:326 |
| BamFieldOfActivity | BAM_FIELD_OF_ACTIVITY | 30: ANAL_SCI_CHEMICAL_COMPOSITION_AND_TRACE_ANALYSIS, ANAL_SCI_NON_DESTRUCTIVE_TESTING_AND_SPECTROSCOPY, ANAL_SCI_QUALITY_ASSURANCE_AND_DATA_SCIENCE, ANAL_SCI_SE... | bam_masterdata/datamodel/v0/vocabulary_types.py:393 |
| BamFocusArea | BAM_FOCUS_AREA | 5: CHEMISTRY_AND_PROCESS_ENGINEERING, ENERGY, ENVIRONMENT, INFRASTRUCTURE, MATERIALS | bam_masterdata/datamodel/v0/vocabulary_types.py:580 |
| BravaisLattice | BRAVAIS_LATTICE | 15: BASE_MONOCLINIC, BASE_ORTHORMB, BODY_CENTER_CUBIC, BODY_CENTER_TETRA, BODY_ORTHORMB, FACE_CENTER_CUBIC, FACE_ORTHORMB, HEXAGONAL, HEX_CLOSE_PACK, RHOMBOHEDRA... | bam_masterdata/datamodel/v0/vocabulary_types.py:617 |
| CalibrationProvider | CALIBRATION_PROVIDER | 2: BAM_FB8_1, MPA_KALIBRIERDIENST_GMBH | bam_masterdata/datamodel/v0/vocabulary_types.py:714 |
| CameraShutterMode | CAMERA_SHUTTER_MODE | 2: CAMERA_SHUTTER_GLOBAL, CAMERA_SHUTTER_ROLLING | bam_masterdata/datamodel/v0/vocabulary_types.py:733 |
| ChemicalProductCategory | CHEMICAL_PRODUCT_CATEGORY | 40: PC0, PC1, PC2, PC3, PC4, PC7, PC8, PC9A, PC9B, PC9C, PC11, PC12, PC13, PC14, PC15, PC16, PC17, PC18, PC20, PC21, PC23, PC24, PC25, PC26, PC27, PC28, PC29, PC... | bam_masterdata/datamodel/v0/vocabulary_types.py:752 |
| DcpdPotCal | DCPD_POT_CAL | 2: FEM_FIT, JOHNSON | bam_masterdata/datamodel/v0/vocabulary_types.py:999 |
| DfgDeviceCode | DFG_DEVICE_CODE | 4428: DFG_0000_1, DFG_0005_1, DFG_0010_1, DFG_0010_2, DFG_0010_3, DFG_0020_1, DFG_0020_2, DFG_0020_3, DFG_0020_4, DFG_0020_5, DFG_0020_6, DFG_0020_7, DFG_0020_8, D... | bam_masterdata/datamodel/v0/vocabulary_types.py:1018 |
| DataPackageKind | DATA_PACKAGE_KIND | 2: RAW, PROCESSED | bam_masterdata/datamodel/v0/vocabulary_types.py:27593 |
| DocumentType | DOCUMENT_TYPE | 30: ACCEPTANCE_CERTIFICATE, CALIBRATION_CERTIFICATE, CATALOG, DATASHEET, DATASHEET_MSDS, DATASHEET_TECHNICAL, DELIVERY_NOTE, DIAGRAM, FABRICATION_ORDER, INSPECTI... | bam_masterdata/datamodel/v0/vocabulary_types.py:27612 |
| ElectronicSmearing | ELECTRONIC_SMEARING | 6: ELEC_SMEAR_FERMI, ELEC_SMEAR_FILE, ELEC_SMEAR_GAUSS, ELEC_SMEAR_MP, ELEC_SMEAR_TET, ELEC_SMEAR_TET_BL | bam_masterdata/datamodel/v0/vocabulary_types.py:27799 |
| EvaluationFileType | EVALUATION_FILE_TYPE | 5: EXCEL, JUPYTER, MATLAB, ORIGIN, PYTHON | bam_masterdata/datamodel/v0/vocabulary_types.py:27842 |
| FcgStepType | FCG_STEP_TYPE | 8: DELTA_F_CONST, DELTA_K_CONST, DELTA_K_DECR_KMAX_CONST, DELTA_K_DECR_KMEAN_CONST, DELTA_K_DECR_R_CONST, DELTA_K_INCR_KMAX_CONST, DELTA_K_INCR_KMEAN_CONST, DEL... | bam_masterdata/datamodel/v0/vocabulary_types.py:27879 |
| FlashLampShape | FLASH_LAMP_SHAPE | 3: ELONGATED, RING, ROUND | bam_masterdata/datamodel/v0/vocabulary_types.py:27934 |
| FtirAccessories | FTIR_ACCESSORIES | 4: FTIR_ACCESSORY_GE_DISC, FTIR_ACCESSORY_GOLDEN_GATE, FTIR_ACCESSORY_NONE, FTIR_ACCESSORY_OTHER | bam_masterdata/datamodel/v0/vocabulary_types.py:27959 |
| GentechSafetyLevel | GENTECH_SAFETY_LEVEL | 4: S1, S2, S3, S4 | bam_masterdata/datamodel/v0/vocabulary_types.py:27990 |
| HeatingAreaDesc | HEATING_AREA_DESC | 3: FULL_BODY, FULL_FACE, ROI | bam_masterdata/datamodel/v0/vocabulary_types.py:28021 |
| HeatingPrinciple | HEATING_PRINCIPLE | 5: HOT_AIR, INDUCTION, OPTICAL, OVEN, VIBRATION | bam_masterdata/datamodel/v0/vocabulary_types.py:28046 |
| InstrumentStatus | INSTRUMENT_STATUS | 5: IN_REPAIR, IN_STORAGE, IN_USE, IS_DEFECT, IS_DISCARDED | bam_masterdata/datamodel/v0/vocabulary_types.py:28083 |
| LaserType | LASER_TYPE | 11: DIODE_MONO, DIODE_PUMPED_CW, DIODE_PUMPED_PULSED, DIODE_TUNABLE, DYE_CW, DYE_PULSED, FLASH_PUMPED, GAS, OPO, OTHER, QCL | bam_masterdata/datamodel/v0/vocabulary_types.py:28120 |
| LoadFrameOrientation | LOAD_FRAME_ORIENTATION | 2: HOR, VERT | bam_masterdata/datamodel/v0/vocabulary_types.py:28193 |
| MaterialUsageTechnikum | MATERIAL_USAGE_TECHNIKUM | 4: CT, OA, QT, RM | bam_masterdata/datamodel/v0/vocabulary_types.py:28212 |
| MatScale | MAT_SCALE | 7: MAT_SCALE_ATOMISTIC, MAT_SCALE_ATOMISTIC_CG, MAT_SCALE_ELEC, MAT_SCALE_MACRO, MAT_SCALE_MESO, MAT_SCALE_MICRO, MAT_SCALE_MULTI | bam_masterdata/datamodel/v0/vocabulary_types.py:28243 |
| MatStructure | MAT_STRUCTURE | 3: AMORPHOUS, CRYSTALLINE, SEMI_CRYSTALLINE | bam_masterdata/datamodel/v0/vocabulary_types.py:28292 |
| MeasuringAmplifierType | MEASURING_AMPLIFIER_TYPE | 2: CARRIER_FREQUENCY, DC | bam_masterdata/datamodel/v0/vocabulary_types.py:28317 |
| MicroscopyFcgCracklengthType | MICROSCOPY_FCG_CRACKLENGTH_TYPE | 3: BEACHMARK, FINAL, NOTCH | bam_masterdata/datamodel/v0/vocabulary_types.py:28336 |
| MinimizationAlgo | MINIMIZATION_ALGO | 12: MIN_ALGO_BLOCK_DVD, MIN_ALGO_CG, MIN_ALGO_DAMPED_MD, MIN_ALGO_EXCT_DIAG, MIN_ALGO_FIRE, MIN_ALGO_HFTN, MIN_ALGO_LBFGS, MIN_ALGO_PREC_CG, MIN_ALGO_QUICKMIN, M... | bam_masterdata/datamodel/v0/vocabulary_types.py:28361 |
| MurnEqnOfState | MURN_EQN_OF_STATE | 4: EOS_BIRCH_MURNAGHAN, EOS_MURNAGHAN, EOS_POLYNOMIAL, EOS_VINET | bam_masterdata/datamodel/v0/vocabulary_types.py:28440 |
| NmrExperimentTypes | NMR_EXPERIMENT_TYPES | 13: NMR_EXP_COSY, NMR_EXP_CP_MAS, NMR_EXP_DEPT, NMR_EXP_HMBC, NMR_EXP_HMQC, NMR_EXP_HSQC, NMR_EXP_IR, NMR_EXP_NOESY, NMR_EXP_OTHER, NMR_EXP_ROESY, NMR_EXP_SPIN_E... | bam_masterdata/datamodel/v0/vocabulary_types.py:28471 |
| NmrNuclei | NMR_NUCLEI | 16: NMR_NUC_1H, NMR_NUC_11B, NMR_NUC_13C, NMR_NUC_14N, NMR_NUC_15N, NMR_NUC_17O, NMR_NUC_19F, NMR_NUC_27AL, NMR_NUC_29SI, NMR_NUC_31P, NMR_NUC_33S, NMR_NUC_35CL,... | bam_masterdata/datamodel/v0/vocabulary_types.py:28556 |
| NmrSolvents | NMR_SOLVENTS | 13: NMR_SOL_ACETONE_D6, NMR_SOL_C6D5CL, NMR_SOL_C6D6, NMR_SOL_CD2CL2, NMR_SOL_CD3CN, NMR_SOL_CD3OD, NMR_SOL_CDCL3, NMR_SOL_D2O, NMR_SOL_DMSO_D6, NMR_SOL_OTHER, N... | bam_masterdata/datamodel/v0/vocabulary_types.py:28659 |
| NotchTypeFcg | NOTCH_TYPE_FCG | 3: CHEVRON_EDM, STRAIGHT_EDM, STRAIGHT_RAZOR | bam_masterdata/datamodel/v0/vocabulary_types.py:28744 |
| NucPerformed | NUC_PERFORMED | 3: BEFORE_ACQUISITION, INITIAL, RESTORE_SAVED | bam_masterdata/datamodel/v0/vocabulary_types.py:28769 |
| OperatingSystem | OPERATING_SYSTEM | 7: DEBIAN_11_BULLSEYE, DEBIAN_12_BOOKWORM, RHEL_8_10_OOTPA, RHEL_9_3_PLOW, SUSE_SLES_15_SP5, UBUNTU_22_04_4, WINDOWS_11_ENT | bam_masterdata/datamodel/v0/vocabulary_types.py:28794 |
| OpticalSpectrometerType | OPTICAL_SPECTROMETER_TYPE | 4: CZERNY_TURNER, ECHELLE, INTERFEROMETRIC, OTHER | bam_masterdata/datamodel/v0/vocabulary_types.py:28843 |
| OrganismFootnoteZkbs | ORGANISM_FOOTNOTE_ZKBS | 8: FN_AR, FN_AR_STRIKETHROUGH, FN_D, FN_E, FN_EXCLAMATION_MARK, FN_P, FN_STAR, FN_VA | bam_masterdata/datamodel/v0/vocabulary_types.py:28874 |
| OrganismGroup | ORGANISM_GROUP | 10: ARCHAEA, BACTERIA, EUKARYOTIC_MICROORGANISMS, FUNGI, MOTHS, OTHER, TERMITES, TSE-AGENTS, VIROID, VIRUS | bam_masterdata/datamodel/v0/vocabulary_types.py:28929 |
| OrganismRiskGroup | ORGANISM_RISK_GROUP | 5: RISK_GROUP_0, RISK_GROUP_1, RISK_GROUP_2, RISK_GROUP_3, RISK_GROUP_4 | bam_masterdata/datamodel/v0/vocabulary_types.py:28996 |
| PhysicalState | PHYSICAL_STATE | 3: GASEOUS, LIQUID, SOLID | bam_masterdata/datamodel/v0/vocabulary_types.py:29033 |
| PlasmidBacterialAntibioticResistance | PLASMID_BACTERIAL_ANTIBIOTIC_RESISTANCE | 10: 5-ALA, AMP, CAM, KAN, NIT, NONE, OTHER, SPEC, STR, TET | bam_masterdata/datamodel/v0/vocabulary_types.py:29058 |
| PlasmidOri | PLASMID_ORI | 6: HIGH, LOW, PBR322, PMB1, PUC, VERY_LOW | bam_masterdata/datamodel/v0/vocabulary_types.py:29125 |
| PositionerType | POSITIONER_TYPE | 5: POSITIONER_TYPE_FIXED, POSITIONER_TYPE_LINEAR, POSITIONER_TYPE_ROTARY_TILT_TABLE, POSITIONER_TYPE_TURNTABLE, POSITIONER_TYPE_WELD_TABLE | bam_masterdata/datamodel/v0/vocabulary_types.py:29168 |
| ProjectStatus | PROJECT_STATUS | 4: APPLICATION, COMPLETED, IN_PREPARATION, IN_PROGRESS | bam_masterdata/datamodel/v0/vocabulary_types.py:29205 |
| PseudopotFunctional | PSEUDOPOT_FUNCTIONAL | 3: PSEUDOPOT_GGA, PSEUDOPOT_HYBRID, PSEUDOPOT_LDA | bam_masterdata/datamodel/v0/vocabulary_types.py:29236 |
| PseudopotType | PSEUDOPOT_TYPE | 4: PSEUDOPOT_AE, PSEUDOPOT_NC, PSEUDOPOT_PAW, PSEUDOPOT_ULTRASOFT | bam_masterdata/datamodel/v0/vocabulary_types.py:29261 |
| PublicationStatus | PUBLICATION_STATUS | 7: ACCEPTED, CORRECTION, DRAFT, FINALISED, PUBLISHED, REVIEW, WRITING | bam_masterdata/datamodel/v0/vocabulary_types.py:29292 |
| PublicationType | PUBLICATION_TYPE | 5: CONFERENCE_PAPER, JOURNAL_PAPER, POSTER, PRESENTATION, TEST_REPORT | bam_masterdata/datamodel/v0/vocabulary_types.py:29341 |
| QueuingSystem | QUEUING_SYSTEM | 5: OPEN_PBS, ORACLE_GE, PBS_PRO, SLURM, TORQUE | bam_masterdata/datamodel/v0/vocabulary_types.py:29378 |
| RawMatForm | RAW_MAT_FORM | 6: COMPONENT, FLAT_BAR, PIPE, PLATE_METAL, ROUND_BAR, SHEET_METAL | bam_masterdata/datamodel/v0/vocabulary_types.py:29415 |
| RawMatTreatmentAlu | RAW_MAT_TREATMENT_ALU | 13: H14, H16, H18, H19, H22, H24_H34, H26_H36, H111, O, T4, T6, T73, T76 | bam_masterdata/datamodel/v0/vocabulary_types.py:29458 |
| RawMatTreatmentSteel | RAW_MAT_TREATMENT_STEEL | 16: A, AC, AR, AT, BC, C, FP, H, HH, HL, M, N, NT, QT, SH, T | bam_masterdata/datamodel/v0/vocabulary_types.py:29543 |
| RobotType | ROBOT_TYPE | 4: ROBOT_TYPE_ARTICULATED, ROBOT_TYPE_CARTESIAN_COORDINATE, ROBOT_TYPE_DELTA, ROBOT_TYPE_SCARA | bam_masterdata/datamodel/v0/vocabulary_types.py:29646 |
| RtdAccuracyClass | RTD_ACCURACY_CLASS | 5: 1_3, A, AA, B, DIN_1_10 | bam_masterdata/datamodel/v0/vocabulary_types.py:29677 |
| RtdConnectionType | RTD_CONNECTION_TYPE | 3: 2_WIRE, 3_WIRE, 4_WIRE | bam_masterdata/datamodel/v0/vocabulary_types.py:29714 |
| RtdInsulationMaterial | RTD_INSULATION_MATERIAL | 4: GLAS_SILK, PFA, PTFE, SILICONE | bam_masterdata/datamodel/v0/vocabulary_types.py:29739 |
| RtdType | RTD_TYPE | 13: NI500, NI1000, NI1000TK5000, NTC1.8KOHM, NTC1KOHM, NTC5KOHM, NTC10KOHM, NTC20KOHM, NTC50KOHM, PT100, PT500, PT1000, PT2000 | bam_masterdata/datamodel/v0/vocabulary_types.py:29770 |
| SampleHolderMaterial | SAMPLE_HOLDER_MATERIAL | 7: SAM_HOL_MAT_GLASS, SAM_HOL_MAT_KAPTON, SAM_HOL_MAT_PC, SAM_HOL_MAT_PTFE, SAM_HOL_MAT_QUARTZ, SAM_HOL_MAT_SMT, SAM_HOL_MAT_NONE | bam_masterdata/datamodel/v0/vocabulary_types.py:29855 |
| ShortRngOrd | SHORT_RNG_ORD | 3: SHORT_RNG_ORD_CHAIN, SHORT_RNG_ORD_RING, SHORT_RNG_ORD_TETRA | bam_masterdata/datamodel/v0/vocabulary_types.py:29904 |
| SpaceGroup | SPACE_GROUP | 230: SPACE_GROUP.ABA2, SPACE_GROUP.ABM2, SPACE_GROUP.AMA2, SPACE_GROUP.AMM2, SPACE_GROUP.C2, SPACE_GROUP.C2_C, SPACE_GROUP.C2_M, SPACE_GROUP.C222, SPACE_GROUP.C22... | bam_masterdata/datamodel/v0/vocabulary_types.py:29929 |
| SpecimenStatus | SPECIMEN_STATUS | 5: DISPOSED, IN_PREPARATION, PREPARED, STORED, TESTED | bam_masterdata/datamodel/v0/vocabulary_types.py:31316 |
| SpecimenTypeFcgTest | SPECIMEN_TYPE_FCG_TEST | 5: CCT, CT, SENB3, SENB4, SENT | bam_masterdata/datamodel/v0/vocabulary_types.py:31353 |
| SubframeType | SUBFRAME_TYPE | 4: ARBITRARY, FULL_FRAME, HALF_FRAME, QUARTER_FRAME | bam_masterdata/datamodel/v0/vocabulary_types.py:31390 |
| TemporalHeatingStructure | TEMPORAL_HEATING_STRUCTURE | 5: ARBITRARY, CONTINUOUS, IMPULSE, RECTANGULAR_PULSE, SINUSOIDAL | bam_masterdata/datamodel/v0/vocabulary_types.py:31421 |
| TestingMachineDriveType | TESTING_MACHINE_DRIVE_TYPE | 6: ELECTRODYNAMIC, ELECTRODYNAMIC_RESONANCE, ELECTROMECHANIC, ELECTROMECHANIC_RESONANCE, SERVOHYDRAULIC, SERVOHYDRAULIC_RESONANCE | bam_masterdata/datamodel/v0/vocabulary_types.py:31458 |
| TestingMachineLoadType | TESTING_MACHINE_LOAD_TYPE | 4: AXIAL, COMBINED_AXAL_TORSION, ROTATING_BENDING, TORSION | bam_masterdata/datamodel/v0/vocabulary_types.py:31501 |
| TestFileType | TEST_FILE_TYPE | 7: TEST_DEFINITION_FILE, TEST_EVALUATION_FILE, TEST_FILE_OTHER, TEST_PROCESSED_DATA_FILE, TEST_PROTOCOL_FILE, TEST_RAWDATA_FILE, TEST_ZIP_ARCHIVE | bam_masterdata/datamodel/v0/vocabulary_types.py:31532 |
| TestMethodKind | TEST_METHOD_KIND | 11: RADAR, ULTRASONIC, REBOUND_HAMMER, IMPACT_ECHO, LIBS, NMR, TERAHERTZ, X_RAY, HALF_CELL_POTENTIAL, MAGNETIC_INDUCTIVE, OTHER | bam_masterdata/datamodel/v0/vocabulary_types.py:31581 |
| TestObjectStatus | TEST_OBJECT_STATUS | 2: AVAILABLE, DISPOSED | bam_masterdata/datamodel/v0/vocabulary_types.py:31654 |
| TestProgramType | TEST_PROGRAM_TYPE | 5: FCG, HCF, LCF_IST, LCF_SST, TENSILE | bam_masterdata/datamodel/v0/vocabulary_types.py:31673 |
| TestSetupType | TEST_SETUP_TYPE | 2: SETUP_TESTING_MACHINE, SETUP_TEST_INSTRUMENTS | bam_masterdata/datamodel/v0/vocabulary_types.py:31710 |
| TestSoftware | TEST_SOFTWARE | 6: INSTRON_SINGLE_AXIS_MAX, INSTRON_WAVEMAKER, MTS_BASIC_TESTWARE, MTS_MULTIPURPOSE_ELITE, MTS_MULTIPURPOSE_TESTWARE, RUMUL_TESTLAB | bam_masterdata/datamodel/v0/vocabulary_types.py:31729 |
| ThermocoupleType | THERMOCOUPLE_TYPE | 10: A, B, C, E, J, K, N, R, S, T | bam_masterdata/datamodel/v0/vocabulary_types.py:31772 |
| ThermodynEnsemble | THERMODYN_ENSEMBLE | 6: TD_ENSEMBLE_ATOM_ENS.NVT, TD_ENSEMBLE_GC, TD_ENSEMBLE_NPH, TD_ENSEMBLE_NPT, TD_ENSEMBLE_NVE, TD_ENSEMBLE_SGC | bam_masterdata/datamodel/v0/vocabulary_types.py:31839 |
| ThermographicSetupConfig | THERMOGRAPHIC_SETUP_CONFIG | 3: INDETERMINED, REFLECTION, TRANSMISSION | bam_masterdata/datamodel/v0/vocabulary_types.py:31882 |
| ThermographicSetupHsOrient | THERMOGRAPHIC_SETUP_HS_ORIENT | 3: OFF_AXIS, ON_AXIS, OTHER | bam_masterdata/datamodel/v0/vocabulary_types.py:31907 |
| UnitMass | UNIT_MASS | 6: GRAM, KILOGRAM, MICROGRAM, MILLIGRAM, NANOGRAM, TONNE | bam_masterdata/datamodel/v0/vocabulary_types.py:31932 |
| WeatherCondition | WEATHER_CONDITION | 6: CLEAR, CLOUDY, FOGGY, PARTIALLY_CLOUDY, RAINY, SNOWY | bam_masterdata/datamodel/v0/vocabulary_types.py:31975 |
| WindDirection | WIND_DIRECTION | 8: EAST, NORTH, NORTH_EAST, NORTH_WEST, SOUTH, SOUTH_EAST, SOUTH_WEST, WEST | bam_masterdata/datamodel/v0/vocabulary_types.py:32018 |
| OrderStatus | $ORDER.ORDER_STATUS | 4: DELIVERED, NOT_YET_ORDERED, ORDERED, PAID | bam_masterdata/datamodel/v0/vocabulary_types.py:32074 |
| Currency | $PRODUCT.CURRENCY | 3: CHF, EUR, USD | bam_masterdata/datamodel/v0/vocabulary_types.py:32106 |
| StorageValidationLevel | $STORAGE.STORAGE_VALIDATION_LEVEL | 3: BOX, BOX_POSITION, RACK | bam_masterdata/datamodel/v0/vocabulary_types.py:32132 |
| StorageBoxSize | $STORAGE_POSITION.STORAGE_BOX_SIZE | 7: 1X1, 4X4, 8X12, 9X9, 10X10, 16X24, 20X40 | bam_masterdata/datamodel/v0/vocabulary_types.py:32158 |
| Language | $SUPPLIER.LANGUAGE | 2: ENGLISH, GERMAN | bam_masterdata/datamodel/v0/vocabulary_types.py:32208 |
| PreferredOrderMethod | $SUPPLIER.PREFERRED_ORDER_METHOD | 3: EMAIL, FAX, MANUAL | bam_masterdata/datamodel/v0/vocabulary_types.py:32228 |
| ColorEncodedAnnotations | $WELL.COLOR_ENCODED_ANNOTATIONS | 2: DEFAULT, FAULTY | bam_masterdata/datamodel/v0/vocabulary_types.py:32254 |
| TriggerSetting | IR_CAMERA.TRIGGER_SETTING | 4: HARDWARE_INDIVIDUAL_FRAME, HARDWARE_START_ACQUISITION, SOFTWARE, TEMPERATURE | bam_masterdata/datamodel/v0/vocabulary_types.py:32274 |
| ScatteringModelPSDLD | SCATTERING_MODEL_PSD_LD | 2: MIE, FRAUNHOFER | bam_masterdata/datamodel/v0/vocabulary_types.py:32305 |
| SampleGeometry | SAMPLE_GEOMETRY | 4: CUBE, PRISM, CYLINDER, DRILL_CORE | bam_masterdata/datamodel/v0/vocabulary_types.py:32324 |
| SampleOrigin | SAMPLE_ORIGIN | 2: BAM_LAB, STRUCTURE | bam_masterdata/datamodel/v0/vocabulary_types.py:32355 |
| ToolPurpose | TOOL_PURPOSE | 3: CUT, DRILL, SCAN | bam_masterdata/datamodel/v0/vocabulary_types.py:32374 |
| GmawTorchType | WELDING.GMAW_TORCH_TYPE | 4: WELDING_GMAW_TORCH_TYPE_NGW_ROT, WELDING_GMAW_TORCH_TYPE_NGW_SWING, WELDING_GMAW_TORCH_TYPE_SINGLE, WELDING_GMAW_TORCH_TYPE_TANDEM | bam_masterdata/datamodel/v0/welding/vocabularies.py:6 |
| WeldType | WELDING.WELD_TYPE | 6: WELDING_FILLET_WELD, WELDING_GROOVE_WELD, WELDING_PLUG_WELD, WELDING_SPOT_WELD, WELDING_SURFACING_WELD, WELDING_TACK_WELD | bam_masterdata/datamodel/v0/welding/vocabularies.py:38 |

## CollectionTypes (2)

| Class | Code | Parent | Own props | File:Line |
|---|---|---|---|---|
| Collection | COLLECTION | CollectionType | 3 | bam_masterdata/datamodel/v0/collection_types.py:8 |
| DefaultExperiment | DEFAULT_EXPERIMENT | CollectionType | 14 | bam_masterdata/datamodel/v0/collection_types.py:46 |

## DatasetTypes (22)

| Class | Code | Parent | Own props | File:Line |
|---|---|---|---|---|
| ElnPreview | ELN_PREVIEW | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:5 |
| RawData | RAW_DATA | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:42 |
| ProcessedData | PROCESSED_DATA | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:79 |
| AnalyzedData | ANALYZED_DATA | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:116 |
| Attachment | ATTACHMENT | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:153 |
| OtherData | OTHER_DATA | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:190 |
| SourceCode | SOURCE_CODE | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:227 |
| AnalysisNotebook | ANALYSIS_NOTEBOOK | DatasetType | 4 | bam_masterdata/datamodel/v0/dataset_types.py:264 |
| PublicationData | PUBLICATION_DATA | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:311 |
| TestFile | TEST_FILE | DatasetType | 7 | bam_masterdata/datamodel/v0/dataset_types.py:426 |
| LogFile | LOG_FILE | DatasetType | 3 | bam_masterdata/datamodel/v0/dataset_types.py:504 |
| MeasurementProtocolFile | MEASUREMENT_PROTOCOL_FILE | DatasetType | 5 | bam_masterdata/datamodel/v0/dataset_types.py:541 |
| Norm | NORM | DatasetType | 13 | bam_masterdata/datamodel/v0/dataset_types.py:598 |
| CompEnv | COMP_ENV | DatasetType | 5 | bam_masterdata/datamodel/v0/dataset_types.py:736 |
| MatModel | MAT_MODEL | DatasetType | 8 | bam_masterdata/datamodel/v0/dataset_types.py:793 |
| SourceCodeWorkflow | SOURCE_CODE_WORKFLOW | DatasetType | 7 | bam_masterdata/datamodel/v0/dataset_types.py:968 |
| Figure | FIGURE | DatasetType | 12 | bam_masterdata/datamodel/v0/dataset_types.py:1045 |
| Pseudopot | MAT_MODEL.PSEUDOPOT | MatModel | 0 | bam_masterdata/datamodel/v0/dataset_types.py:1260 |
| IntPot | MAT_MODEL.INT_POT | MatModel | 0 | bam_masterdata/datamodel/v0/dataset_types.py:1267 |
| Plot | FIGURE.PLOT | Figure | 10 | bam_masterdata/datamodel/v0/dataset_types.py:1274 |
| Schematic | FIGURE.SCHEMATIC | Figure | 0 | bam_masterdata/datamodel/v0/dataset_types.py:1381 |
| SimVis | FIGURE.SIM_VIS | Figure | 11 | bam_masterdata/datamodel/v0/dataset_types.py:1388 |

## PropertyType index (1194 codes)

| Property code | Data type | Vocab/Object ref | Used by |
|---|---|---|---|
| $ANNOTATIONS_STATE | XML |  | Action, AuxiliaryMaterial, BamGentechFacility, Calibration, Chemical, CompEnv, ComputationalAnalysis, CondaEnvironmen... |
| $DEFAULT_COLLECTION_VIEW | CONTROLLEDVOCABULARY | $DEFAULT_COLLECTION_VIEWS | Collection |
| $DEFAULT_OBJECT_TYPE | VARCHAR |  | Collection, DefaultExperiment |
| $DOCUMENT | MULTILINE_VARCHAR |  | Entry |
| $ELN_SETTINGS | VARCHAR |  | GeneralElnSettings |
| $HISTORY_ID | VARCHAR |  | AnalysisNotebook |
| $NAME | VARCHAR |  | Action, Aluminium, AnalysisNotebook, AnalyzedData, Attachment, AuxiliaryMaterial, BamGentechFacility, Calibration, Ch... |
| $ORDER.ADDITIONAL_INFORMATION | VARCHAR |  | Order |
| $ORDER.BILL_TO | VARCHAR |  | Order |
| $ORDER.CONTACT_FAX | VARCHAR |  | Order |
| $ORDER.CONTACT_PHONE | VARCHAR |  | Order |
| $ORDER.ORDER_STATE | VARCHAR |  | Order |
| $ORDER.SHIP_ADDRESS | VARCHAR |  | Order |
| $ORDER.SHIP_TO | VARCHAR |  | Order |
| $ORDERING.ORDER_STATUS | CONTROLLEDVOCABULARY | $ORDER.ORDER_STATUS | Order, Request |
| $PRODUCT.CATALOG_NUM | VARCHAR |  | Product |
| $PRODUCT.CURRENCY | CONTROLLEDVOCABULARY | $PRODUCT.CURRENCY | Product |
| $PRODUCT.PRICE_PER_UNIT | REAL |  | Product |
| $PUBLICATION.DESCRIPTION | VARCHAR |  | Publication |
| $PUBLICATION.IDENTIFIER | VARCHAR |  | Publication |
| $PUBLICATION.OPENBIS_RELATED_IDENTIFIERS | VARCHAR |  | Publication |
| $PUBLICATION.ORGANIZATION | VARCHAR |  | Publication |
| $PUBLICATION.TYPE | VARCHAR |  | Publication |
| $PUBLICATION.URL | HYPERLINK |  | Publication |
| $SEARCH_QUERY.CUSTOM_DATA | XML |  | SearchQuery |
| $SEARCH_QUERY.FETCH_OPTIONS | XML |  | SearchQuery |
| $SEARCH_QUERY.SEARCH_CRITERIA | XML |  | SearchQuery |
| $SHOW_IN_PROJECT_OVERVIEW | BOOLEAN |  | DefaultExperiment, Entry, ExperimentalStep, Test |
| $STORAGE.BOX_NUM | INTEGER |  | Storage |
| $STORAGE.BOX_SPACE_WARNING | INTEGER |  | Storage |
| $STORAGE.COLUMN_NUM | INTEGER |  | Storage |
| $STORAGE.ROW_NUM | INTEGER |  | Storage |
| $STORAGE.STORAGE_SPACE_WARNING | INTEGER |  | Storage |
| $STORAGE.STORAGE_VALIDATION_LEVEL | CONTROLLEDVOCABULARY | $STORAGE.STORAGE_VALIDATION_LEVEL | Storage |
| $STORAGE_POSITION.STORAGE_BOX_NAME | VARCHAR |  | StoragePosition |
| $STORAGE_POSITION.STORAGE_BOX_POSITION | VARCHAR |  | StoragePosition |
| $STORAGE_POSITION.STORAGE_BOX_SIZE | CONTROLLEDVOCABULARY | $STORAGE_POSITION.STORAGE_BOX_SIZE | StoragePosition |
| $STORAGE_POSITION.STORAGE_CODE | VARCHAR |  | StoragePosition |
| $STORAGE_POSITION.STORAGE_RACK_COLUMN | INTEGER |  | StoragePosition |
| $STORAGE_POSITION.STORAGE_RACK_ROW | INTEGER |  | StoragePosition |
| $STORAGE_POSITION.STORAGE_USER | VARCHAR |  | StoragePosition |
| $SUPPLIER.COMPANY_ADDRESS_LINE_1 | VARCHAR |  | Supplier |
| $SUPPLIER.COMPANY_ADDRESS_LINE_2 | VARCHAR |  | Supplier |
| $SUPPLIER.COMPANY_EMAIL | VARCHAR |  | Supplier |
| $SUPPLIER.COMPANY_FAX | VARCHAR |  | Supplier |
| $SUPPLIER.COMPANY_LANGUAGE | CONTROLLEDVOCABULARY | $SUPPLIER.LANGUAGE | Supplier |
| $SUPPLIER.COMPANY_PHONE | VARCHAR |  | Supplier |
| $SUPPLIER.CUSTOMER_NUMBER | VARCHAR |  | Supplier |
| $XMLCOMMENTS | XML |  | Action, Aluminium, AnalysisNotebook, AnalyzedData, Attachment, AuxiliaryMaterial, BamGentechFacility, Calibration, Ch... |
| ABSOLUTE_DEVIATION | REAL |  | LaserDiffPSDMeasurement |
| ABSORPTION_COEFF_BLUE_SAMPLE | REAL |  | LaserDiffPSDMeasurement |
| ABSORPTION_COEFF_SAMPLE | REAL |  | LaserDiffPSDMeasurement |
| ABSTRACT | MULTILINE_VARCHAR |  | Project |
| ACCREDITATED_CALIBRATION_LAB | BOOLEAN |  | Calibration |
| ACCURACY_CLASS_VDE0410 | CONTROLLEDVOCABULARY | ACCURACY_CLASS_VDE0410 | MeasuringAmplifier |
| ACRONYM | VARCHAR |  | Project |
| ACTING_PERSON | OBJECT | PERSON.BAM | Action, Control, MsCenter |
| ACTION_DATE | DATE |  | Action |
| ACTION_END | TIMESTAMP |  | DeviceUsage |
| ACTION_START | TIMESTAMP |  | DeviceUsage |
| ADDITIVES | MULTILINE_VARCHAR |  | ConcreteMixture |
| ADDMIXTURES | MULTILINE_VARCHAR |  | ConcreteMixture |
| ADDRESS | MULTILINE_VARCHAR |  | Person |
| AD_CHANNEL_DESCRIPTION | MULTILINE_VARCHAR |  | IrCameraAcquisition |
| AFFILIATION | VARCHAR |  | Person |
| AGGREGATE | MULTILINE_VARCHAR |  | ConcreteMixture |
| AIR_REL_HUMIDITY_IN_PERCENT | REAL |  | EnvironmentalConditions |
| AIR_TEMPERATURE_IN_CELSIUS | REAL |  | EnvironmentalConditions |
| AIR_VOIDS_CONTENT | MULTILINE_VARCHAR |  | ConcreteMixture |
| ALIAS | VARCHAR |  | Aluminium, AuxiliaryMaterial, BamGentechFacility, Chemical, Document, Hpc, Instrument, Organism, Person, RawMaterialC... |
| ALU_TREATMENT_FIRST | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_ALU | Aluminium |
| ALU_TREATMENT_FOURTH | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_ALU | Aluminium |
| ALU_TREATMENT_SECOND | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_ALU | Aluminium |
| ALU_TREATMENT_THIRD | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_ALU | Aluminium |
| ANALOG_OUTPUT_VOLTAGE_MAX | REAL |  | MeasuringAmplifier, Nanovoltmeter |
| ANALOG_OUTPUT_VOLTAGE_MIN | REAL |  | MeasuringAmplifier, Nanovoltmeter |
| ARBITRARY_SUBFRAME_HEIGHT_IN_PIXEL | INTEGER |  | IrCameraAcquisition |
| ARBITRARY_SUBFRAME_START_HEIGHT_IN_PIXEL | INTEGER |  | IrCameraAcquisition |
| ARBITRARY_SUBFRAME_START_WIDTH_IN_PIXEL | INTEGER |  | IrCameraAcquisition |
| ARBITRARY_SUBFRAME_WIDTH_IN_PIXEL | INTEGER |  | IrCameraAcquisition |
| ARREST | BOOLEAN |  | FcgStep |
| ASSOCIATED_PROJECT | OBJECT | PROJECT | Named, ThermographicMeasurement |
| ATOMISTIC_CALC_TYPE | CONTROLLEDVOCABULARY | ATOMISTIC_CALC_TYPE | Lammps, Vasp |
| ATOMISTIC_IONIC_STEPS | INTEGER |  | Vasp |
| ATOMISTIC_KPT_FULL | MULTILINE_VARCHAR |  | Vasp |
| ATOMISTIC_KPT_SPACIN_IN_1_A | REAL |  | Vasp |
| ATOMISTIC_N_KPT_X | INTEGER |  | Vasp |
| ATOMISTIC_N_KPT_Y | INTEGER |  | Vasp |
| ATOMISTIC_N_KPT_Z | INTEGER |  | Vasp |
| ATOM_AVG_FNORM_IN_EV_A | REAL |  | Lammps |
| ATOM_AVG_POT_ENG_IN_EV | REAL |  | Lammps |
| ATOM_AVG_PRESS_IN_GPA | REAL |  | Lammps |
| ATOM_AVG_TOT_ENG_IN_EV | REAL |  | Lammps |
| ATOM_AVG_VOL_IN_A3 | REAL |  | Lammps |
| ATOM_CELL_SHP_RELAX | BOOLEAN |  | Lammps, Vasp |
| ATOM_CELL_VOL_RELAX | BOOLEAN |  | Lammps, Vasp |
| ATOM_CHGDENS_REUSE | BOOLEAN |  | Vasp |
| ATOM_ELEC_MIN_ALGO | CONTROLLEDVOCABULARY | MINIMIZATION_ALGO | Vasp |
| ATOM_EL_E_TOL_IN_EV | REAL |  | Vasp |
| ATOM_EQUIL_K_MOD_IN_GPA | REAL |  | Murnaghan |
| ATOM_EQUIL_TOTENG_IN_EV | REAL |  | Murnaghan |
| ATOM_EQUIL_VOL_IN_A3 | REAL |  | Murnaghan |
| ATOM_E_CUTOFF_IN_EV | REAL |  | Vasp |
| ATOM_E_TOL_ION_IN_EV | REAL |  | Lammps, Vasp |
| ATOM_FIN_FNORM_IN_EV_A | REAL |  | Lammps |
| ATOM_FIN_POT_ENG_IN_EV | REAL |  | Lammps, Vasp |
| ATOM_FIN_PRESS_IN_GPA | REAL |  | Vasp |
| ATOM_FIN_TOTMGMO_IN_MUB | VARCHAR |  | Vasp |
| ATOM_FIN_TOT_ENG_IN_EV | REAL |  | Lammps, Vasp |
| ATOM_FIN_VOL_IN_A3 | REAL |  | Lammps, Vasp |
| ATOM_FORCE_MAX_IN_EV_A | REAL |  | Lammps, Vasp |
| ATOM_F_TOL_IN_EV_A | REAL |  | Lammps, Vasp |
| ATOM_IONIC_MIN_ALGO | CONTROLLEDVOCABULARY | MINIMIZATION_ALGO | Lammps, Vasp |
| ATOM_IONIC_STEPS | INTEGER |  | Lammps |
| ATOM_KPOINT_TYPE | CONTROLLEDVOCABULARY | ATOM_KPOINT_TYPE | Vasp |
| ATOM_KPT_GAMMA_CENT | BOOLEAN |  | Vasp |
| ATOM_MD_AVG_TEMP_IN_K | REAL |  | Lammps |
| ATOM_MD_ENSEMBLE | CONTROLLEDVOCABULARY | THERMODYN_ENSEMBLE | Lammps |
| ATOM_MD_INIT_PRESS_IN_GPA | REAL |  | Lammps |
| ATOM_MD_INIT_TEMP_IN_K | REAL |  | Lammps |
| ATOM_MD_LANGEVIN | BOOLEAN |  | Lammps |
| ATOM_MD_TARG_TEMP_IN_K | REAL |  | Lammps |
| ATOM_MD_TIME_STP_IN_PS | REAL |  | Lammps |
| ATOM_NON_COLL_MAG | BOOLEAN |  | Vasp |
| ATOM_POS_RELAX | BOOLEAN |  | Lammps, Vasp |
| ATOM_POTENTIAL_STYLE | CONTROLLEDVOCABULARY | ATOM_POTENTIAL_STYLE | InteratomicPotential |
| ATOM_SAMPLE_TEMP_IN_K | REAL |  | Amorphous |
| ATOM_SHORT_RNG_ORD | CONTROLLEDVOCABULARY | SHORT_RNG_ORD | Amorphous |
| ATOM_SIGMA_IN_EV | REAL |  | Vasp |
| ATOM_SIM_TIME_PS_IN_PS | REAL |  | Lammps |
| ATOM_SPIN_POLARIZED | BOOLEAN |  | Vasp |
| ATOM_TARG_PRESS_IN_GPA | REAL |  | Lammps |
| ATOM_WAVEFUNC_REUSE | BOOLEAN |  | Vasp |
| ATOM_XC_FUNCTIONAL | CONTROLLEDVOCABULARY | ATOM_XC_FUNCTIONAL | Vasp |
| ATOM_XC_U_CORRECTION | BOOLEAN |  | Vasp |
| AUTHOR | VARCHAR |  | Document, Figure, MatModel, Sop, TestFile |
| AUTHOR_PERSON | OBJECT | PERSON.BAM | DataTransfer, DataTransferPackage, Document |
| AUXILIARY_MATERIAL_TYPE | CONTROLLEDVOCABULARY | AUXILIARY_MATERIAL_TYPE | AuxiliaryMaterial |
| BAM_DATA_STORE_USER_STATUS | BOOLEAN |  | Bam |
| BAM_FIELD_OF_ACTIVITY | CONTROLLEDVOCABULARY | BAM_FIELD_OF_ACTIVITY | Project |
| BAM_FLOOR | CONTROLLEDVOCABULARY | BAM_FLOOR | BamGentechFacility, BamLaboratory, Chemical, GasBottle, GlassWare, Instrument, Sample, TestObject, TestingMachine |
| BAM_FOCUS_AREA | CONTROLLEDVOCABULARY | BAM_FOCUS_AREA | Project |
| BAM_HOUSE | CONTROLLEDVOCABULARY | BAM_HOUSE | BamGentechFacility, BamLaboratory, Chemical, GasBottle, GlassWare, Instrument, Sample, TestObject, TestingMachine |
| BAM_INVENTORY_NUMBER | VARCHAR |  | MeasuringInstrument, TestingEquipment, Tool |
| BAM_LOCATION | CONTROLLEDVOCABULARY | BAM_LOCATION | BamGentechFacility, BamLaboratory, Chemical, GasBottle, GlassWare, Instrument, Sample, TestObject, TestingMachine |
| BAM_LOCATION_COMPLETE | CONTROLLEDVOCABULARY | BAM_LOCATION_COMPLETE | BamGentechFacility, BamLaboratory, Chemical, GasBottle, GlassWare, Instrument, MeasuringInstrument, Sample, TestObjec... |
| BAM_OE | CONTROLLEDVOCABULARY | BAM_OE | Bam, BamGentechFacility, Chemical, GasBottle, GlassWare, Instrument, MeasuringInstrument, Project, Sample, Sop, TestO... |
| BAM_PARTNER | VARCHAR |  | MeasurementSession, Project |
| BAM_ROOM | CONTROLLEDVOCABULARY | BAM_ROOM | BamGentechFacility, BamLaboratory, Chemical, GasBottle, GlassWare, Instrument, Sample, TestObject, TestingMachine |
| BAM_USERNAME | VARCHAR |  | Bam, PyironJob |
| BAM_USERPROFILE | HYPERLINK |  | Bam |
| BANDWIDTH | REAL |  | MeasuringAmplifier |
| BARCODE_EXTERNAL | VARCHAR |  | Chemical, GlassWare, Sample |
| BATCH_NUMBER | VARCHAR |  | Welding |
| BINDER | MULTILINE_VARCHAR |  | ConcreteMixture |
| BRAVAIS_LATTICE | CONTROLLEDVOCABULARY | BRAVAIS_LATTICE | Crystal |
| BUILDING_MATERIALS_TEST_ID | VARCHAR |  | BuildingMaterialsSpecimen |
| BUILDING_MATERIALS_TEST_MACHINE | CONTROLLEDVOCABULARY | BUILDING_MATERIALS_TEST_MACHINE | BuildingMaterialsSpecimen |
| BUILDING_MATERIALS_TEST_QUANTITY | VARCHAR |  | BuildingMaterialsSpecimen |
| BUILDING_MATERIALS_TEST_RESULT | REAL |  | BuildingMaterialsSpecimen |
| BUILDING_MATERIAL_DETAILS | MULTILINE_VARCHAR |  | BuildingMaterialsSpecimen |
| BUILDING_MATERIAL_TEST_STANDARD | VARCHAR |  | BuildingMaterialsSpecimen |
| BUILDING_MATERIAL_TYPE | CONTROLLEDVOCABULARY | BUILDING_MATERIAL_TYPE | BuildingMaterialsSpecimen |
| BUILDING_NAME | MULTILINE_VARCHAR |  | BuildingMaterialsSpecimen |
| BUILDING_NUMBER | VARCHAR |  | TestObjectExternal |
| BUILDING_YEAR | INTEGER |  | TestObjectExternal |
| CALIBRATION_CERTIFICATE_NUMBER | VARCHAR |  | Calibration, CreepTestElongationValuesAndCrossSectionalDimensions, CreepTestExtensionValuesContactingExtensometer, Cr... |
| CALIBRATION_DATE | DATE |  | Calibration, CreepTestElongationValuesAndCrossSectionalDimensions, CreepTestExtensionValuesContactingExtensometer, Cr... |
| CALIBRATION_INTERVAL | INTEGER |  | ForceTransducer, HydraulicCylinder, HydraulicMisc, MeasuringAmplifier, Servovalve |
| CALIBRATION_LAB_ACCREDITATION_NUMBER | VARCHAR |  | Calibration |
| CALIBRATION_PROVIDER | CONTROLLEDVOCABULARY | CALIBRATION_PROVIDER | Calibration |
| CAMERAS_SETUP | XML |  | LaserMagnet |
| CAMERA_DISTANCE_IN_MILLIMETER | REAL |  | ThermographySetup |
| CAMERA_SHUTTER_MODE | CONTROLLEDVOCABULARY | CAMERA_SHUTTER_MODE | VideoRecording |
| CAS_NUMBER | VARCHAR |  | Chemical |
| CELL_TEMPERATURE_IN_CELSIUS | REAL |  | SaxsMeasurement |
| CENTRIFUGE.COMPATIBLE_ROTORS | VARCHAR |  | Centrifuge |
| CENTRIFUGE.DATE_LAST_DGUV_CHECKING | DATE |  | Centrifuge |
| CENTRIFUGE.IS_TEMPERATURE_CONTROLLED | BOOLEAN |  | Centrifuge |
| CENTRIFUGE.MAXIMUM_SPEED_RCF | INTEGER |  | Centrifuge |
| CENTRIFUGE.MAXIMUM_SPEED_RPM | INTEGER |  | Centrifuge |
| CENTRIFUGE.MAXIMUM_TEMPERATURE | INTEGER |  | Centrifuge |
| CENTRIFUGE.MINIMUM_TEMPERATURE | INTEGER |  | Centrifuge |
| CENTRIFUGE.REQUIRES_DGUV_CHECKING | BOOLEAN |  | Centrifuge |
| CENTRIFUGE_ROTOR.COMPATIBLE_VIALS | VARCHAR |  | CentrifugeRotor |
| CENTRIFUGE_ROTOR.MAXIMUM_CAPACITY_VIALS | INTEGER |  | CentrifugeRotor |
| CENTRIFUGE_ROTOR.MAXIMUM_CAPACITY_VOLUME | INTEGER |  | CentrifugeRotor |
| CENTRIFUGE_ROTOR.MAXIMUM_SPEED_RCF | INTEGER |  | CentrifugeRotor |
| CENTRIFUGE_ROTOR.MAXIMUM_SPEED_RPM | INTEGER |  | CentrifugeRotor |
| CHARACTERISTICS | VARCHAR |  | RawMaterialCode |
| CHARGE_COMPENSATION | REAL |  | SIMS |
| CHECK_INTERVAL | INTEGER |  | Norm, Sop, Task |
| CHEM_SPECIES_ADDRESSED | VARCHAR |  | InteratomicPotential, Pseudopotential |
| CHEM_SPECIES_BY_COMP_IN_PCT | VARCHAR |  | CreepTestChemicalCompositionMeasured, CreepTestChemicalCompositionNominal, MaterialV1 |
| CHEM_SPECIES_BY_N_ATOMS | VARCHAR |  | Amorphous, Crystal |
| CHEM_SPECIES_BY_WT_IN_PCT | VARCHAR |  | MaterialV1 |
| CHROMATOGRAPHY_TYPE | CONTROLLEDVOCABULARY | CHROMATOGRAPHY_TYPE | MassSpec |
| COL_BLIND_ACCESS | BOOLEAN |  | Figure |
| COMPILATION_REQ | BOOLEAN |  | SourceCodeWorkflow |
| COMPILER | MULTILINE_VARCHAR |  | SourceCodeWorkflow |
| CONCENTRATION | REAL |  | Chemical |
| CONCEPTUAL_DICTIONARY | MULTILINE_VARCHAR |  | MatSimStructure, PyironJob |
| CONDA_CHANNELS | MULTILINE_VARCHAR |  | CondaEnvironment |
| CONDA_PIP | BOOLEAN |  | CondaEnvironment |
| CONDUCTIVITY_IN_MS | REAL |  | RmEthanol |
| CONSISTENCY | MULTILINE_VARCHAR |  | ConcreteMixture |
| CONSTRUCTION_TYPE | VARCHAR |  | TestObjectExternal |
| CO_RESPONSIBLE_PERSON | OBJECT | PERSON.BAM | GasBottle, Hpc, Instrument, Named, Sample, Sop, Task, TestingMachine, Welding |
| CPU_NODES_CONFIG | MULTILINE_VARCHAR |  | Hpc |
| CREEP_TEST_ADDITIONAL_INFORMATION_TEST_PIECE | VARCHAR |  | CreepTestTestPiece |
| CREEP_TEST_ANY_RELATED_ARTICLES | BOOLEAN |  | CreepTest |
| CREEP_TEST_CALIBRATION_CLASS | REAL |  | CreepTestExtensionValuesContactingExtensometer, CreepTestLoadSensor, CreepTestTestMachine, CreepTestTestMachineLoadin... |
| CREEP_TEST_CALIBRATION_RANGE | REAL |  | CreepTestElongationValuesAndCrossSectionalDimensions, CreepTestExtensionValuesContactingExtensometer, CreepTestLoadSe... |
| CREEP_TEST_CALIBRATION_RESULT | BOOLEAN |  | CreepTestElongationValuesAndCrossSectionalDimensions |
| CREEP_TEST_CALIBRATION_STATUS | CONTROLLEDVOCABULARY | CREEP_TEST_CALIBRATION_STATUS | CreepTestElongationValuesAndCrossSectionalDimensions, CreepTestTemperatureDataAcquisition, CreepTestTemperatureSensor |
| CREEP_TEST_CALIBRATION_VALIDITY_TIME_PERIOD | REAL |  | CreepTestElongationValuesAndCrossSectionalDimensions, CreepTestExtensionValuesContactingExtensometer, CreepTestLoadSe... |
| CREEP_TEST_CASTING_SPEED | REAL |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_CASTING_TEMPERATURE | REAL |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_CHARACTERIZATION_METHOD | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_CONDITION | CONTROLLEDVOCABULARY | CREEP_TEST_CONDITION | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_CONTACT_METHOD | CONTROLLEDVOCABULARY | CREEP_TEST_THERMOCOUPLE_CONTACT_METHOD | CreepTestTemperatureSensor |
| CREEP_TEST_COOLING_SPEED | REAL |  | CreepTestSecondaryValuesRecordedDuringTestRun |
| CREEP_TEST_CRACK_OR_DEFECT_INSPECTION_METHOD | VARCHAR |  | CreepTestMaterialHistoryNDTResults |
| CREEP_TEST_CRACK_OR_DEFECT_INSPECTION_RESULT | VARCHAR |  | CreepTestMaterialHistoryNDTResults |
| CREEP_TEST_CREEP_RUPTURE_TIME | REAL |  | CreepTestPrimaryValuesRecordedAfterEndOfTest |
| CREEP_TEST_DATA_ACQUISITION_DESCRIPTION | VARCHAR |  | CreepTestTestMachineDataAcquisition |
| CREEP_TEST_DATA_ACQUISITION_SOFTWARE_AND_VERSION | VARCHAR |  | CreepTestTestMachineDataAcquisition |
| CREEP_TEST_DATA_ACQUISITION_TIME_CHECK | BOOLEAN |  | CreepTestTestMachineDataAcquisition |
| CREEP_TEST_DATA_ACQUISITION_UNIT_ID | VARCHAR |  | CreepTestTestMachineDataAcquisition |
| CREEP_TEST_DATA_ACQUISITION_UNIT_MODEL_INFORMATION | VARCHAR |  | CreepTestTestMachineDataAcquisition |
| CREEP_TEST_DATA_ANALYSIS_PROCEDURES | VARCHAR |  | CreepTestDataProcessingProcedures |
| CREEP_TEST_DENDRITE_SPACINGS | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_DESCRIPTION_OF_THE_LOADING_SYSTEM | BOOLEAN |  | CreepTestTestMachineLoadingSystem |
| CREEP_TEST_DETERMINATION_OF_REFERENCE_LENGTH | CONTROLLEDVOCABULARY | CREEP_TEST_DETERMINATION_OF_REFERENCE_LENGTH | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_DISPLACEMENT_MEASURING_METHOD | CONTROLLEDVOCABULARY | CREEP_TEST_DISPLACEMENT_MEASURING_METHOD | CreepTestExtensometerSystem |
| CREEP_TEST_ELAPSED_TIME_FROM_END_OF_LOADING | REAL |  | CreepTestValuesRecordedDuringTestRunBase |
| CREEP_TEST_ELONGATION | REAL |  | CreepTestPrimaryValuesRecordedDuringTestRun |
| CREEP_TEST_ELONGATION_MEASURING_EQUIPMENT_CALIBRATION_STANDARD | VARCHAR |  | CreepTestElongationValuesAndCrossSectionalDimensions |
| CREEP_TEST_END_OF_TEST | VARCHAR |  | CreepTest |
| CREEP_TEST_END_OF_TEST_CRITERIUM | CONTROLLEDVOCABULARY | CREEP_TEST_END_OF_TEST_CRITERIUM | CreepTest |
| CREEP_TEST_EQUIPMENT_ID | VARCHAR |  | CreepTestElongationValuesAndCrossSectionalDimensions |
| CREEP_TEST_EXTENSION | REAL |  | CreepTestPrimaryValuesRecordedDuringTestRun |
| CREEP_TEST_EXTENSION_AVERAGING | BOOLEAN |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_EXTENSION_LIMIT | REAL |  | CreepTest |
| CREEP_TEST_EXTENSION_RANGE_LOWER_LIMIT | REAL |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_EXTENSION_RANGE_UPPER_LIMIT | REAL |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_EXTENSOMETER_CALIBRATION_STANDARD | VARCHAR |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_EXTENSOMETER_GAUGE_LENGTH | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_EXTENSOMETER_ID | VARCHAR |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_EXTENSOMETER_LEG_MATERIAL | CONTROLLEDVOCABULARY | CREEP_TEST_EXTENSOMETER_LEG_MATERIAL | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_EXTENSOMETER_MODEL_INFORMATION | VARCHAR |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_FINAL_GAUGE_LENGTH_AFTER_FRACTURE | REAL |  | CreepTestPrimaryValuesRecordedAfterEndOfTest |
| CREEP_TEST_FIXING_TECHNIQUE | CONTROLLEDVOCABULARY | CREEP_TEST_FIXING_TECHNIQUE | CreepTestTestPieceHolderSystem |
| CREEP_TEST_FORCE | REAL |  | CreepTestPrimaryValuesRecordedDuringTestRun |
| CREEP_TEST_FORCE_RECORDING | BOOLEAN |  | CreepTestLoadDataAcquisition |
| CREEP_TEST_FORM_OF_AS_MANUFACTURED_MATERIAL | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_FRACTURE_POSITION | CONTROLLEDVOCABULARY | CREEP_TEST_FRACTURE_POSITION | CreepTestPrimaryValuesRecordedAfterEndOfTest |
| CREEP_TEST_FURNACE_TYPE | CONTROLLEDVOCABULARY | CREEP_TEST_FURNACE_TYPE | CreepTestTestMachineHeatingSystem |
| CREEP_TEST_GAMMA_PRIME_PARTICLES_AVERAGE_SIZE | REAL |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GAMMA_PRIME_PARTICLES_MAXIMUM_SIZE | REAL |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GEOMETRY_SIZE_AS_MANUFACTURED_MATERIAL | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GEOMETRY_SIZE_AS_TESTED_MATERIAL | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GRAIN_ADDITIONAL_INFORMATION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GRAIN_SIZE | REAL |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GRAIN_SIZE_DETERMINATION_METHOD | CONTROLLEDVOCABULARY | CREEP_TEST_GRAIN_SIZE_DETERMINATION_METHOD | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GRAIN_SIZE_DISTRIBUTION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_GRAIN_SIZE_MEASURING_REGION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_HARDNESS | VARCHAR |  | CreepTestMaterialHistoryMechanicalTestsResults |
| CREEP_TEST_HEATING_SPEED | REAL |  | CreepTestSecondaryValuesRecordedDuringTestRun |
| CREEP_TEST_HEATING_TIME | REAL |  | CreepTestValuesRecordedDuringTestRunBase |
| CREEP_TEST_HEAT_TREATMENT_AGEING_DESCRIPTION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_HEAT_TREATMENT_ANNEALING_DESCRIPTION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_HEAT_TREATMENT_PROTOCOL | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_HEAT_TREATMENT_STATE | CONTROLLEDVOCABULARY | CREEP_TEST_HEAT_TREATMENT_STATE | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_ID | VARCHAR |  | CreepTest |
| CREEP_TEST_INITIAL_STRESS | REAL |  | CreepTest |
| CREEP_TEST_INTERRUPTION_COURSE | CONTROLLEDVOCABULARY | CREEP_TEST_INTERRUPTION_COURSE | CreepTest |
| CREEP_TEST_IS_THE_EXTENSOMETER_INCL_THE_DATA_ACQUISITION_CALIBRATED | BOOLEAN |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_K_VALUE | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_LAYOUT | VARCHAR |  | CreepTestTemperatureSensor |
| CREEP_TEST_LINK_CONTACTING_EXTENSOMETER | OBJECT | INSTRUMENT.CREEP_TEST_EXTENSION_VALUES_CONTACTING_EXTENSOMETER | CreepTest |
| CREEP_TEST_LINK_DATA_PROCESSING | OBJECT | COMPUTATIONAL_ANALYSIS.CREEP_TEST_DATA_PROCESSING_PROCEDURES | CreepTest |
| CREEP_TEST_LINK_ELONGATION_CROSS_SECTIONAL | OBJECT | INSTRUMENT.CREEP_TEST_ELONGATION_VALUES_AND_CROSS_SECTIONAL_DIMENSIONS | CreepTest |
| CREEP_TEST_LINK_EXTENSOMETER_SYSTEM | OBJECT | INSTRUMENT.CREEP_TEST_EXTENSOMETER_SYSTEM | CreepTest |
| CREEP_TEST_LINK_LABORATORY_CONDITIONS | OBJECT | ENVIRONMENTAL_CONDITIONS.CREEP_TEST_LABORATORY_CONDITIONS | CreepTest |
| CREEP_TEST_LINK_LOAD_MEASURING_DATA_ACQUISITION | OBJECT | CREEP_TEST_LOAD_DATA_ACQUISITION | CreepTest |
| CREEP_TEST_LINK_LOAD_SENSOR | OBJECT | INSTRUMENT.CREEP_TEST_LOAD_SENSOR | CreepTest |
| CREEP_TEST_LINK_MATERIAL_HISTORY_AND_CONDITION | OBJECT | CREEP_TEST_MATERIAL_HISTORY_AND_CONDITION | CreepTest |
| CREEP_TEST_LINK_PRIMARY_DATA_AFTER_END | OBJECT | CREEP_TEST_PRIMARY_VALUES_RECORDED_AFTER_END_OF_TEST | CreepTest |
| CREEP_TEST_LINK_PRIMARY_DATA_AT_START | OBJECT | CREEP_TEST_PRIMARY_VALUES_RECORDED_AT_TEST_START | CreepTest |
| CREEP_TEST_LINK_PRIMARY_DATA_DURING_RUN | OBJECT | CREEP_TEST_VALUES_RECORDED_DURING_TEST_RUN_BASE.CREEP_TEST_PRIMARY_VALUES_RECORDED_DURING_TEST_RUN | CreepTest |
| CREEP_TEST_LINK_PROJECT | OBJECT | PROJECT | CreepTest |
| CREEP_TEST_LINK_SECONDARY_DATA_DURING_RUN | OBJECT | CREEP_TEST_VALUES_RECORDED_DURING_TEST_RUN_BASE.CREEP_TEST_SECONDARY_VALUES_RECORDED_DURING_TEST_RUN | CreepTest |
| CREEP_TEST_LINK_SECONDARY_ELONGATION_VALUES | OBJECT | CREEP_TEST_SECONDARY_ELONGATION_VALUES | CreepTest |
| CREEP_TEST_LINK_SECONDARY_EXTENSION_VALUES | OBJECT | CREEP_TEST_SECONDARY_EXTENSION_VALUES | CreepTest |
| CREEP_TEST_LINK_TEMPERATURE_DAQ | OBJECT | INSTRUMENT.CREEP_TEST_TEMPERATURE_DATA_ACQUISITION | CreepTest |
| CREEP_TEST_LINK_TEMPERATURE_MEASURING_SYSTEM | OBJECT | INSTRUMENT.CREEP_TEST_TEMPERATURE_MEASURING_SYSTEM | CreepTest |
| CREEP_TEST_LINK_TEMPERATURE_SENSOR | OBJECT | INSTRUMENT.CREEP_TEST_TEMPERATURE_SENSOR | CreepTest |
| CREEP_TEST_LINK_TEST_MACHINE | OBJECT | TESTING_MACHINE.CREEP_TEST_TEST_MACHINE | CreepTest |
| CREEP_TEST_LINK_TEST_PIECE | OBJECT | SAMPLE.CREEP_TEST_TEST_PIECE | CreepTest |
| CREEP_TEST_LOADING_RATE | REAL |  | CreepTestSecondaryValuesRecordedDuringTestRun |
| CREEP_TEST_LOADING_SYSTEM_CALIBRATION_STANDARD | CONTROLLEDVOCABULARY | CREEP_TEST_LOAD_SYSTEM_CALIBRATION_STANDARD | CreepTestTestMachineLoadingSystem |
| CREEP_TEST_LOAD_CONTROL_TYPE | CONTROLLEDVOCABULARY | CREEP_TEST_LOAD_CONTROL_TYPE | CreepTest |
| CREEP_TEST_LOAD_SENSOR_CALIBRATION | BOOLEAN |  | CreepTestLoadSensor |
| CREEP_TEST_LOAD_SENSOR_CALIBRATION_STANDARD | CONTROLLEDVOCABULARY | CREEP_TEST_LOAD_SYSTEM_CALIBRATION_STANDARD | CreepTestLoadSensor |
| CREEP_TEST_LOAD_SENSOR_DURING_LOADING | BOOLEAN |  | CreepTestLoadSensor |
| CREEP_TEST_MANUFACTURING_PROCESS_DESCRIPTION_AS_MANUFACTURED_MATERIAL | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MANUFACTURING_PROCESS_DESCRIPTION_AS_TESTED_MATERIAL | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MATERIAL_IDENTIFIER | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MATERIAL_LINK_CHEMICAL_COMPOSITION_MEASURED | OBJECT | CREEP_TEST_CHEMICAL_COMPOSITION_MEASURED | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MATERIAL_LINK_CHEMICAL_COMPOSITION_NOMINAL | OBJECT | CREEP_TEST_CHEMICAL_COMPOSITION_NOMINAL | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MATERIAL_LINK_MECHANICAL_TESTS_RESULTS | OBJECT | CREEP_TEST_MATERIAL_HISTORY_MECHANICAL_TESTS_RESULTS | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MATERIAL_LINK_NDT_RESULTS | OBJECT | CREEP_TEST_MATERIAL_HISTORY_NDT_RESULTS | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MEASURED_CONDITION | CONTROLLEDVOCABULARY | CREEP_TEST_MEASURED_CONDITION | CreepTestChemicalCompositionMeasured, CreepTestChemicalCompositionNominal, CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MEASUREMENT_DIRECTION | CONTROLLEDVOCABULARY | CREEP_TEST_EXTENSION_MEASUREMENT_DIRECTION | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_MEASUREMENT_METHOD | VARCHAR |  | CreepTestChemicalCompositionMeasured, CreepTestChemicalCompositionNominal |
| CREEP_TEST_MEASUREMENT_SETUP | CONTROLLEDVOCABULARY | CREEP_TEST_MEASUREMENT_SETUP | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_MEASURING_AMPLIFIER_MODEL_INFORMATION | VARCHAR |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_MEASURING_EQUIPMENT | CONTROLLEDVOCABULARY | CREEP_TEST_MEASURING_EQUIPMENT | CreepTestElongationValuesAndCrossSectionalDimensions |
| CREEP_TEST_MEASURING_EQUIPMENTS_USAGE | VARCHAR |  | CreepTestElongationValuesAndCrossSectionalDimensions |
| CREEP_TEST_MEASURING_EQUIPMENT_TYPE | CONTROLLEDVOCABULARY | CREEP_TEST_MEASURING_EQUIPMENT_TYPE | CreepTestElongationValuesAndCrossSectionalDimensions |
| CREEP_TEST_MEASURING_POSITION | VARCHAR |  | CreepTestChemicalCompositionMeasured, CreepTestChemicalCompositionNominal, CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_METROLOGICAL_TRACEABILITY | BOOLEAN |  | CreepTestTemperatureMeasuringSystem |
| CREEP_TEST_MICROSTRUCTURE_FEATURE | CONTROLLEDVOCABULARY | CREEP_TEST_MICROSTRUCTURE_FEATURE | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MICROSTRUCTURE_FEATURE_INFORMATION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MICROSTRUCTURE_IMAGE | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MICROSTRUCTURE_REPORT | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MINIMUM_APPLICABLE_FORCE | REAL |  | CreepTestTestMachine |
| CREEP_TEST_MINIMUM_TEST_PIECE_DIAMETER_AT_ROOM_TEMPERATURE | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_MOUNTING_TYPE | CONTROLLEDVOCABULARY | CREEP_TEST_EXTENSOMETER_MOUNTING_TYPE | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_MULTISTAGE_AGEING | BOOLEAN |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_MULTISTAGE_ANNEALING | BOOLEAN |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_NOMINAL_GAUGE_LENGTH | REAL |  | CreepTestExtensionValuesContactingExtensometer |
| CREEP_TEST_NUMBER_OF_THERMOCOUPLES | INTEGER | CREEP_TEST_NUMBER_OF_THERMOCOUPLES | CreepTestTemperatureSensor |
| CREEP_TEST_ORIENTATION_DETERMINATION_ACCURACY | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_ORIGINAL_GAUGE_LENGTH | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_PARALLEL_LENGTH | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_PERCENTAGE_CREEP_EXTENSION | REAL |  | CreepTestSecondaryExtensionValues |
| CREEP_TEST_PERCENTAGE_ELASTIC_EXTENSION | REAL |  | CreepTestSecondaryExtensionValues |
| CREEP_TEST_PERCENTAGE_ELONGATION_AFTER_CREEP_FRACTURE | REAL |  | CreepTestSecondaryElongationValues |
| CREEP_TEST_PERCENTAGE_EXTENSION | REAL |  | CreepTestSecondaryValuesRecordedDuringTestRun |
| CREEP_TEST_PERCENTAGE_INITIAL_PLASTIC_EXTENSION | REAL |  | CreepTestSecondaryExtensionValues |
| CREEP_TEST_PERCENTAGE_INITIAL_TOTAL_EXTENSION | REAL |  | CreepTestSecondaryExtensionValues |
| CREEP_TEST_PERCENTAGE_PERMANENT_ELONGATION | REAL |  | CreepTestSecondaryElongationValues |
| CREEP_TEST_PERCENTAGE_PLASTIC_EXTENSION | REAL |  | CreepTestSecondaryExtensionValues |
| CREEP_TEST_PERCENTAGE_REDUCTION_OF_AREA_AFTER_CREEP_FRACTURE | REAL |  | CreepTestSecondaryElongationValues |
| CREEP_TEST_PERCENTAGE_TOTAL_EXTENSION | REAL |  | CreepTestSecondaryExtensionValues |
| CREEP_TEST_PHASE_TRANSFORMATION_DURING_TEST | BOOLEAN |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_POSSIBLE_PHASE_TRANSFORMATION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_PRELOAD | REAL |  | CreepTest |
| CREEP_TEST_PRIMARY_DATA_SERIES | VARCHAR |  | CreepTestDataProcessingProcedures |
| CREEP_TEST_PROCESSED_DATA_SERIES | VARCHAR |  | CreepTestDataProcessingProcedures |
| CREEP_TEST_PROOF_OF_SINGLE_CRYSTALLINITY | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_PROOF_STRENGTH_CREEP_TEST_TEMPERATURE | REAL |  | CreepTestMaterialHistoryMechanicalTestsResults |
| CREEP_TEST_PROOF_STRENGTH_ROOM_TEMPERATURE | REAL |  | CreepTestMaterialHistoryMechanicalTestsResults |
| CREEP_TEST_RATIO_REFERENCE_LENGTH_TO_DIAMETER | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_REFERENCE_JUNCTION | CONTROLLEDVOCABULARY | CREEP_TEST_REFERENCE_JUNCTION | CreepTestTemperatureDataAcquisition |
| CREEP_TEST_REFERENCE_LENGTH_TO_CALCULATE_PERCENTAGE_ELONGATIONS | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_REFERENCE_LENGTH_TO_CALCULATE_PERCENTAGE_EXTENSIONS | REAL |  | CreepTestPrimaryValuesRecordedAtTestStart |
| CREEP_TEST_RELATED_ARTICLE | MULTILINE_VARCHAR |  | CreepTest |
| CREEP_TEST_RELATED_PUBLICATIONS | MULTILINE_VARCHAR |  | CreepTestDataProcessingProcedures |
| CREEP_TEST_REPRECIPITATED_GAMMA_GAMMA_PRIME_REGIONS | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_RESOLUTION | INTEGER |  | CreepTestElongationValuesAndCrossSectionalDimensions |
| CREEP_TEST_ROOM_HUMIDITY | BOOLEAN |  | CreepTestLaboratoryConditions |
| CREEP_TEST_ROOM_TEMPERATURE | BOOLEAN |  | CreepTestLaboratoryConditions |
| CREEP_TEST_SENSOR_ID | VARCHAR |  | CreepTestTemperatureSensor |
| CREEP_TEST_SENSOR_TYPE | CONTROLLEDVOCABULARY | CREEP_TEST_SENSOR_TYPE | CreepTestTemperatureSensor |
| CREEP_TEST_SENSOR_TYPE_CONTACTING_METHOD | CONTROLLEDVOCABULARY | CREEP_TEST_SENSOR_TYPE_CONTACTING_METHOD | CreepTestExtensometerSystem |
| CREEP_TEST_SENSOR_TYPE_NON_CONTACTING_METHOD | CONTROLLEDVOCABULARY | CREEP_TEST_SENSOR_TYPE_NON_CONTACTING_METHOD | CreepTestExtensometerSystem |
| CREEP_TEST_SINGLE_CRYSTAL_ORIENTATION | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_SINGLE_CRYSTAL_ORIENTATION_DETERMINATION_METHOD | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_SINGLE_CRYSTAL_ORIENTATION_MEASURING_POINT | VARCHAR |  | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_SOAK_TIME | REAL |  | CreepTestValuesRecordedDuringTestRunBase |
| CREEP_TEST_SOFTWARE | VARCHAR |  | CreepTestDataProcessingProcedures |
| CREEP_TEST_SOLIDIFICATION | CONTROLLEDVOCABULARY | CREEP_TEST_SOLIDIFICATION | CreepTestMaterialHistoryAndCondition |
| CREEP_TEST_STANDARD | CONTROLLEDVOCABULARY | CREEP_TEST_STANDARD | CreepTest |
| CREEP_TEST_STANDARD_APPLIED | BOOLEAN |  | CreepTest |
| CREEP_TEST_TEMPERATURE_DAQ_CALIBRATION_METHOD | VARCHAR |  | CreepTestTemperatureDataAcquisition |
| CREEP_TEST_TEMPERATURE_DAQ_CALIBRATION_STANDARD | CONTROLLEDVOCABULARY | CREEP_TEST_DATA_ACQUISITION_CALIBRATION_STANDARD | CreepTestTemperatureDataAcquisition |
| CREEP_TEST_TEMPERATURE_DEVIATION | REAL |  | CreepTestTemperatureDataAcquisition, CreepTestTemperatureSensor |
| CREEP_TEST_TEMPERATURE_SENSOR_CALIBRATION_METHOD | CONTROLLEDVOCABULARY | CREEP_TEST_THERMOCOUPLE_CALIBRATION_METHOD | CreepTestTemperatureSensor |
| CREEP_TEST_TEMPERATURE_SENSOR_CALIBRATION_STANDARD | CONTROLLEDVOCABULARY | CREEP_TEST_THERMOCOUPLE_CALIBRATION_STANDARD | CreepTestTemperatureSensor |
| CREEP_TEST_TEMPERATURE_SIGNAL | CONTROLLEDVOCABULARY | CREEP_TEST_TEMPERATURE_SIGNAL | CreepTestTemperatureMeasuringSystem |
| CREEP_TEST_TEST_DURATION | REAL |  | CreepTestValuesRecordedDuringTestRunBase |
| CREEP_TEST_TEST_FORCE | REAL |  | CreepTest |
| CREEP_TEST_TEST_FRAME_AND_SPECIMEN_ALIGNMENT | BOOLEAN |  | CreepTestTestMachine |
| CREEP_TEST_TEST_FRAME_AND_SPECIMEN_ALIGNMENT_DESCRIPTION | VARCHAR |  | CreepTestTestMachine |
| CREEP_TEST_TEST_MACHINE_ID | VARCHAR |  | CreepTestTestMachine |
| CREEP_TEST_TEST_MACHINE_LINK_DATA_ACQUISITION | OBJECT | INSTRUMENT.CREEP_TEST_TEST_MACHINE_DATA_ACQUISITION | CreepTestTestMachine |
| CREEP_TEST_TEST_MACHINE_LINK_HEATING_SYSTEM | OBJECT | INSTRUMENT.CREEP_TEST_TEST_MACHINE_HEATING_SYSTEM | CreepTestTestMachine |
| CREEP_TEST_TEST_MACHINE_LINK_HOLDER_SYSTEM | OBJECT | INSTRUMENT_ACCESSORY.CREEP_TEST_TEST_PIECE_HOLDER_SYSTEM | CreepTestTestMachine |
| CREEP_TEST_TEST_MACHINE_LINK_LOADING_SYSTEM | OBJECT | INSTRUMENT.CREEP_TEST_TEST_MACHINE_LOADING_SYSTEM | CreepTestTestMachine |
| CREEP_TEST_TEST_MACHINE_TYPE | CONTROLLEDVOCABULARY | CREEP_TEST_MACHINE_TYPE | CreepTestTestMachine |
| CREEP_TEST_TEST_PIECE_HISTORY | VARCHAR |  | CreepTestTestPiece |
| CREEP_TEST_TEST_PIECE_ID | VARCHAR |  | CreepTestTestPiece |
| CREEP_TEST_TEST_PIECE_ORIENTATION_IN_TEST_MACHINE | VARCHAR |  | CreepTestTestPiece |
| CREEP_TEST_TEST_PIECE_ORIGIN_AND_ORIENTATION | VARCHAR |  | CreepTestTestPiece |
| CREEP_TEST_TEST_PIECE_TECHNICAL_DRAWING | VARCHAR |  | CreepTestTestPiece |
| CREEP_TEST_TEST_PIECE_TYPE_I | CONTROLLEDVOCABULARY | CREEP_TEST_TEST_PIECE_TYPE_I | CreepTestTestPiece |
| CREEP_TEST_TEST_PIECE_TYPE_II | CONTROLLEDVOCABULARY | CREEP_TEST_TEST_PIECE_TYPE_II | CreepTestTestPiece |
| CREEP_TEST_TEST_PIECE_TYPE_III | CONTROLLEDVOCABULARY | CREEP_TEST_TEST_PIECE_TYPE_III | CreepTestTestPiece |
| CREEP_TEST_THERMOCOUPLE_LOCATION | CONTROLLEDVOCABULARY | CREEP_TEST_THERMOCOUPLE_LOCATION | CreepTestTemperatureSensor |
| CREEP_TEST_THERMOCOUPLE_TYPE | CONTROLLEDVOCABULARY | THERMOCOUPLE_TYPE | CreepTestTemperatureSensor |
| CREEP_TEST_TIME_LIMIT | REAL |  | CreepTest |
| CREEP_TEST_TYPE | CONTROLLEDVOCABULARY | CREEP_TEST_TYPE | CreepTest |
| CREEP_TEST_TYPE_OF_LOADING | CONTROLLEDVOCABULARY | CREEP_TEST_TYPE_OF_LOADING | CreepTest |
| CREEP_TEST_UNLOADING_RATE | REAL |  | CreepTestSecondaryValuesRecordedDuringTestRun |
| CREEP_TEST_USE_OF_CALIBRATED_WEIGHTS | BOOLEAN |  | CreepTestTestMachineLoadingSystem |
| CREEP_TEST_VERIFICATION_OF_LOADING_SYSTEM | BOOLEAN |  | CreepTestTestMachineLoadingSystem |
| CREEP_TEST_WIRE_GAUGE | REAL |  | CreepTestTemperatureSensor |
| CREEP_TEST_WORKFLOW_USAGE | BOOLEAN |  | CreepTestDataProcessingProcedures |
| CRYSTAL_ORIENTATION | VARCHAR |  | MatSimStructure |
| CURRENT | REAL |  | PowderXRDMeasurement |
| CUSTOMER | VARCHAR |  | SIMS |
| CYLINDER_TYPE | VARCHAR |  | HydraulicCylinder |
| DATA_PACKAGE_DATE | DATE |  | DataTransferPackage |
| DATA_PACKAGE_KIND | CONTROLLEDVOCABULARY | DATA_PACKAGE_KIND | DataTransferPackage |
| DATE_BOTTLING | DATE |  | Chemical |
| DATE_EXPIRATION | DATE |  | Chemical |
| DATE_OF_PRODUCTION | DATE |  | BuildingMaterialsSpecimen |
| DATE_OPENING | DATE |  | Chemical |
| DATE_PUBLICATION | DATE |  | Norm |
| DCPD_AMPLIFICATION_FACTOR | REAL |  | Dcpd |
| DCPD_CURRENT | REAL |  | Dcpd |
| DCPD_INITIAL_CRACKLENGTH | REAL |  | Dcpd |
| DCPD_INITIAL_POTENTIAL_DROP | REAL |  | Dcpd |
| DCPD_INITIAL_TEMP | REAL |  | Dcpd |
| DCPD_LINEARISED_POTENTIAL | BOOLEAN |  | Dcpd |
| DCPD_POT_DROP_CAL | CONTROLLEDVOCABULARY | DCPD_POT_CAL | Dcpd |
| DCPD_PROPORTIONAL_POTENTIAL | BOOLEAN |  | Dcpd |
| DCPD_TEMP_COEFF | REAL |  | Dcpd |
| DCPD_TEMP_COMP | BOOLEAN |  | Dcpd |
| DCPD_YZERO_FITTED | REAL |  | Dcpd |
| DEFAULT_EXPERIMENT.EXPERIMENTAL_DESCRIPTION | MULTILINE_VARCHAR |  | DefaultExperiment |
| DEFAULT_EXPERIMENT.EXPERIMENTAL_GOALS | MULTILINE_VARCHAR |  | DefaultExperiment |
| DEFAULT_EXPERIMENT.EXPERIMENTAL_RESULTS | MULTILINE_VARCHAR |  | DefaultExperiment |
| DEFAULT_EXPERIMENT.GRANT | VARCHAR |  | DefaultExperiment |
| DEFECT_DESCRIPTION | MULTILINE_VARCHAR |  | Named |
| DELAYED_EXTRACTION | BOOLEAN |  | SIMS |
| DELTAK_EXPONENT | REAL |  | FcgStep |
| DELTA_A | REAL |  | FcgStep |
| DELTA_N | INTEGER |  | FcgStep |
| DENSITY_GRAM_PER_CUBIC_CM | REAL |  | Chemical |
| DENSITY_KG_PER_CUBIC_METER | REAL |  | BuildingMaterialsSpecimen |
| DESCRIPTION | MULTILINE_VARCHAR |  | BamGentechFacility, Chemical, ComputationalAnalysis, CondaEnvironment, DataTransfer, DataTransferPackage, GlassWare, ... |
| DETECTION_RANGE_MAX_IN_NM | REAL |  | SpectrometerOptical |
| DETECTION_RANGE_MIN_IN_NM | REAL |  | SpectrometerOptical |
| DETECTOR_TYPE | CONTROLLEDVOCABULARY | DETECTOR_TYPE | GcSystem, LcSystem, MassSpec |
| DETECTOR_TYPE_SECONDARY | CONTROLLEDVOCABULARY | DETECTOR_TYPE | GcSystem, LcSystem |
| DEVICE_MODEL_NAME | VARCHAR |  | CreepTestElongationValuesAndCrossSectionalDimensions, Instrument, MeasuringInstrument, TestingEquipment |
| DFG_DEVICE_CODE | CONTROLLEDVOCABULARY | DFG_DEVICE_CODE | Instrument, TestingMachine |
| DISPERSING_MEDIUM | VARCHAR |  | LaserDiffPSDMeasurement |
| DLS.ANALYSISMODEL | VARCHAR |  | Dls |
| DLS.ATTENUATOR | INTEGER |  | Dls |
| DLS.CELLDESCRIPTION | VARCHAR |  | Dls |
| DLS.COND | REAL |  | Dls |
| DLS.CUMULANTSFITERROR | REAL |  | Dls |
| DLS.DISPERSANT | VARCHAR |  | Dls |
| DLS.FKAMODEL | VARCHAR |  | Dls |
| DLS.INTERCEPT | REAL |  | Dls |
| DLS.MATERIAL | VARCHAR |  | Dls |
| DLS.MULTIMODALFITERROR | REAL |  | Dls |
| DLS.PDI | REAL |  | Dls |
| DLS.PK1INT | REAL |  | Dls |
| DLS.PK1INTPD | REAL |  | Dls |
| DLS.PK1INTWIDTH | REAL |  | Dls |
| DLS.PK1NUM | REAL |  | Dls |
| DLS.PK1NUMPD | REAL |  | Dls |
| DLS.PK1NUMWIDTH | REAL |  | Dls |
| DLS.PK1VOL | REAL |  | Dls |
| DLS.PK1VOLPD | REAL |  | Dls |
| DLS.PK1VOLWIDTH | REAL |  | Dls |
| DLS.PK1ZETA | REAL |  | Dls |
| DLS.PK1ZETAWIDTH | REAL |  | Dls |
| DLS.PK2INT | REAL |  | Dls |
| DLS.PK2INTPD | REAL |  | Dls |
| DLS.PK2INTWIDTH | REAL |  | Dls |
| DLS.PK2NUM | REAL |  | Dls |
| DLS.PK2NUMPD | REAL |  | Dls |
| DLS.PK2NUMWIDTH | REAL |  | Dls |
| DLS.PK2VOL | REAL |  | Dls |
| DLS.PK2VOLPD | REAL |  | Dls |
| DLS.PK2VOLWIDTH | REAL |  | Dls |
| DLS.PK2ZETA | REAL |  | Dls |
| DLS.PK2ZETAWIDTH | REAL |  | Dls |
| DLS.PK3INT | REAL |  | Dls |
| DLS.PK3INTPD | REAL |  | Dls |
| DLS.PK3INTWIDTH | REAL |  | Dls |
| DLS.PK3NUM | REAL |  | Dls |
| DLS.PK3NUMPD | REAL |  | Dls |
| DLS.PK3NUMWIDTH | REAL |  | Dls |
| DLS.PK3VOL | REAL |  | Dls |
| DLS.PK3VOLPD | REAL |  | Dls |
| DLS.PK3VOLWIDTH | REAL |  | Dls |
| DLS.PK3ZETA | REAL |  | Dls |
| DLS.PK3ZETAWIDTH | REAL |  | Dls |
| DLS.SIZEMERIT | REAL |  | Dls |
| DLS.TEMPERATURE | REAL |  | Dls |
| DLS.VOLT | REAL |  | Dls |
| DLS.ZAVG | REAL |  | Dls |
| DLS.ZETA | REAL |  | Dls |
| DOCUMENT_ID | VARCHAR |  | Document |
| DOCUMENT_LINK | HYPERLINK |  | Document |
| DOCUMENT_TYPE | CONTROLLEDVOCABULARY | DOCUMENT_TYPE | Document, TestFile |
| DONOR | OBJECT | ORGANISM | GmoDonor |
| DONOR_RISK_GROUP | CONTROLLEDVOCABULARY | ORGANISM_RISK_GROUP | GmoDonor |
| DURATION_IN_SECONDS | REAL |  | SamplePretreatment |
| D_10_IN_MICROMETERS | REAL |  | LaserDiffPSDMeasurement |
| D_50_IN_MICROMETERS | REAL |  | LaserDiffPSDMeasurement |
| D_90_IN_MICROMETERS | REAL |  | LaserDiffPSDMeasurement |
| ELECTRONIC_SMEARING | CONTROLLEDVOCABULARY | ELECTRONIC_SMEARING | Vasp |
| ELLIPSOMETRIC_ARRANGEMENT | VARCHAR |  | Ellipsometer |
| ELLIPSOMETRIC_CONFIGURATION | VARCHAR |  | Ellipsometer |
| ELLI_ACCESSORY | MULTILINE_VARCHAR |  | Ellipsometry |
| ELLI_AOI_HIGH | REAL |  | Ellipsometry |
| ELLI_AOI_LOW | REAL |  | Ellipsometry |
| ELLI_AOI_RANGE_LOWER | REAL |  | Ellipsometer |
| ELLI_AOI_RANGE_UPPER | REAL |  | Ellipsometer |
| ELLI_AUTO_ALIGN_OPTION | BOOLEAN |  | Ellipsometer |
| ELLI_AZIMUTH_ANGLE_OPTION | BOOLEAN |  | Ellipsometer |
| ELLI_FOCUSING | BOOLEAN |  | Ellipsometry |
| ELLI_FOCUSING_OPTION | BOOLEAN |  | Ellipsometer |
| ELLI_IMAGING_CAMERAS | MULTILINE_VARCHAR |  | Ellipsometer |
| ELLI_IMAGING_CAMERA_X | INTEGER |  | Ellipsometer |
| ELLI_IMAGING_CAMERA_Y | INTEGER |  | Ellipsometer |
| ELLI_IMAGING_ELLI_LENSES | MULTILINE_VARCHAR |  | Ellipsometer |
| ELLI_IMAGING_OPTION | BOOLEAN |  | Ellipsometer |
| ELLI_IMG_CAMERA_USED | VARCHAR |  | EllipsometryImaging |
| ELLI_IMG_DATASET_TYPE | VARCHAR |  | EllipsometryImaging |
| ELLI_IMG_DATA_OPTIMISATION | MULTILINE_VARCHAR |  | EllipsometryImaging |
| ELLI_IMG_FOCUSSCANNING | BOOLEAN |  | EllipsometryImaging |
| ELLI_IMG_LENS_USED | VARCHAR |  | EllipsometryImaging |
| ELLI_IMG_MULTI | BOOLEAN |  | EllipsometryImaging |
| ELLI_IMG_MULTI_N_IMAGES | INTEGER |  | EllipsometryImaging |
| ELLI_IMG_N_PIXELS_X | INTEGER |  | EllipsometryImaging |
| ELLI_IMG_N_PIXELS_Y | INTEGER |  | EllipsometryImaging |
| ELLI_IMG_N_ROIS | INTEGER |  | EllipsometryImaging |
| ELLI_INSITU_DESCR | MULTILINE_VARCHAR |  | EllipsometryInSitu |
| ELLI_INSITU_N_MEAS | INTEGER |  | EllipsometryInSitu |
| ELLI_INSITU_TIME | REAL |  | EllipsometryInSitu |
| ELLI_LIGHT_SOURCES | VARCHAR |  | Ellipsometer |
| ELLI_LIQUID_CELL_OPTION | BOOLEAN |  | Ellipsometer |
| ELLI_MAPPING_N_PTS | INTEGER |  | EllipsometryMapping |
| ELLI_MAPPING_OPTION | BOOLEAN |  | Ellipsometer |
| ELLI_MAPPING_RANGE | VARCHAR |  | Ellipsometer |
| ELLI_MAPPING_SIZE | VARCHAR |  | EllipsometryMapping |
| ELLI_N_AOI | INTEGER |  | Ellipsometry |
| ELLI_N_SPECTRAL_POINTS | INTEGER |  | Ellipsometry |
| ELLI_OTHER_ACCESSORY | MULTILINE_VARCHAR |  | Ellipsometer |
| ELLI_QUANTITY_TYPE | VARCHAR |  | Ellipsometry |
| ELLI_SPECTRAL_HIGH | REAL |  | Ellipsometry |
| ELLI_SPECTRAL_LOW | REAL |  | Ellipsometry |
| ELLI_SPECTRAL_RANGE_LOWER | REAL |  | Ellipsometer |
| ELLI_SPECTRAL_RANGE_UNITS | VARCHAR |  | Ellipsometer, Ellipsometry |
| ELLI_SPECTRAL_RANGE_UPPER | REAL |  | Ellipsometer |
| ELLI_TEMPERATURE_CONTROL_OPTION | BOOLEAN |  | Ellipsometer |
| ELLI_TEMP_CONTROL_R_COOL | REAL |  | EllipsometryInSituTemperature |
| ELLI_TEMP_CONTROL_R_HEAT | REAL |  | EllipsometryInSituTemperature |
| ELLI_TEMP_CONTROL_T_HIGH | REAL |  | EllipsometryInSituTemperature |
| ELLI_TEMP_CONTROL_T_LOW | REAL |  | EllipsometryInSituTemperature |
| ELLI_TEMP_COOLING | BOOLEAN |  | EllipsometryInSituTemperature |
| ELLI_TEMP_HEATING | BOOLEAN |  | EllipsometryInSituTemperature |
| ELLI_TEMP_T_CONST | REAL |  | EllipsometryInSituTemperature |
| ELLI_TEMP_VARIABLE | BOOLEAN |  | EllipsometryInSituTemperature |
| EMAIL | VARCHAR |  | Person |
| END_2THETA | REAL |  | PowderXRDMeasurement |
| END_DATE | TIMESTAMP |  | DefaultExperiment, ExperimentalStep, Project, Test |
| ENV_TOOL | VARCHAR |  | CompEnv |
| EQUIPMENT_STATUS | CONTROLLEDVOCABULARY | INSTRUMENT_STATUS | Tool |
| ETHERNET | BOOLEAN |  | MeasuringAmplifier, Nanovoltmeter, PowerSupply |
| EXPERIMENTAL_STEP.EXPERIMENTAL_DESCRIPTION | MULTILINE_VARCHAR |  | ExperimentalStep |
| EXPERIMENTAL_STEP.EXPERIMENTAL_GOALS | MULTILINE_VARCHAR |  | ExperimentalStep |
| EXPERIMENTAL_STEP.EXPERIMENTAL_RESULTS | MULTILINE_VARCHAR |  | ExperimentalStep |
| EXPERIMENTAL_STEP.SPREADSHEET | XML |  | ExperimentalStep |
| EXPERIMENTAL_STEP.WELDMENT.ARC_CURRENT | REAL |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.ARC_PROCESS | VARCHAR |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.ARC_VOLTAGE | REAL |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.CURRENT_TRANSFORMER | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.GROOVE_PREPARATION | VARCHAR |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.LASER_FOCUS | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.LASER_POWER | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.LASER_WIRE_OFFSET | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.MAGNET_CAPACITANCE | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.MAGNET_FREQUENCY | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.MAGNET_I_1 | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.MAGNET_U_1 | REAL |  | LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.SHIELDING_GAS_FLOW | REAL |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.WELD_TRAVEL_SPEED | REAL |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.WIRE_FEED_RATE | REAL |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.WIRE_STICKOUT_LENGTH | REAL |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT.WORKPIECE_THICKNESS | REAL |  | GmawBase, LaserHybridMagnet |
| EXPERIMENTAL_STEP.WELDMENT_TYPE | CONTROLLEDVOCABULARY | WELDING.WELD_TYPE | Weldment |
| EXPOSURE_TIME_IN_SECONDS | REAL |  | SaxsMeasurement |
| FAMILY_NAME | VARCHAR |  | Person |
| FCG_CYCLIC_R | BOOLEAN |  | FcgTest |
| FCG_NOMINAL_R | REAL |  | FcgTest |
| FCG_PARIS | BOOLEAN |  | FcgTest |
| FCG_RESULT_CYCLICR_A | REAL |  | FcgTest |
| FCG_RESULT_CYCLICR_B | REAL |  | FcgTest |
| FCG_RESULT_PARIS_C | REAL |  | FcgTest |
| FCG_RESULT_PARIS_M | REAL |  | FcgTest |
| FCG_RESULT_THRSHLD | REAL |  | FcgTest |
| FCG_STEP_PRECRACK | BOOLEAN |  | FcgStep |
| FCG_STEP_TYPE | CONTROLLEDVOCABULARY | FCG_STEP_TYPE | FcgStep |
| FCG_THRSHLD | BOOLEAN |  | FcgTest |
| FEM_FIT_EQ | VARCHAR |  | Dcpd |
| FIG_DPI | INTEGER |  | Figure |
| FILE_FORMAT | VARCHAR |  | DataTransfer, DataTransferPackage, Figure, MatModel |
| FILE_SYSTEM_CONFIG | MULTILINE_VARCHAR |  | Hpc |
| FINAL_CRACKLENGTH | REAL |  | FcgStep |
| FINAL_CYCLES | REAL |  | FcgStep |
| FINAL_DELTAF | REAL |  | FcgStep |
| FINAL_DELTAK | REAL |  | FcgStep |
| FINAL_FAMP | REAL |  | FcgStep |
| FINAL_FMAX | REAL |  | FcgStep |
| FINAL_FMEAN | REAL |  | FcgStep |
| FINAL_FMIN | REAL |  | FcgStep |
| FINAL_GEOMFUN | REAL |  | FcgStep |
| FINAL_R_RATIO | REAL |  | FcgStep |
| FINAL_SSY_RATIO | REAL |  | FcgStep |
| FINISHED_FLAG | BOOLEAN |  | DefaultExperiment, ExperimentalStep |
| FIRMWARE_VERSION | VARCHAR |  | Camera, GmawWeldingPowerSource, LaserLineScanner, RobotController |
| FLASH_LAMP_SHAPE | CONTROLLEDVOCABULARY | FLASH_LAMP_SHAPE | FlashLamp |
| FORCE_TRANSDUCER_TYPE | VARCHAR |  | ForceTransducer |
| FOR_WHAT | MULTILINE_VARCHAR |  | GeneralProtocol |
| FRAMERATE_IN_HERTZ | REAL |  | IrCameraAcquisition |
| FRAME_COUNT | INTEGER |  | SaxsMeasurement |
| FRESH_CONCRETE_DENSITY | MULTILINE_VARCHAR |  | ConcreteMixture |
| FRESH_CONCRETE_TEMPERATURE | MULTILINE_VARCHAR |  | ConcreteMixture |
| FTIR.ACCESSORY | CONTROLLEDVOCABULARY | FTIR_ACCESSORIES | Ftir |
| FTIR.END_WAVENUMBER | REAL |  | Ftir |
| FTIR.INSTRUMENT | VARCHAR |  | Ftir |
| FTIR.IS_FLUSHED | BOOLEAN |  | Ftir |
| FTIR.RESOLUTION | INTEGER |  | Ftir |
| FTIR.SCANS | INTEGER |  | Ftir |
| FTIR.START_WAVENUMBER | REAL |  | Ftir |
| FUNDING_GRANT_NO | VARCHAR |  | Project, TestObjectBAM |
| GAS_FLOODING | BOOLEAN |  | SIMS |
| GAS_PRESSURE_BAR | REAL |  | GasBottle |
| GAS_VOLUME | REAL |  | GasBottle |
| GENERAL_PROTOCOL.MATERIALS | MULTILINE_VARCHAR |  | GeneralProtocol |
| GENERAL_PROTOCOL.PROTOCOL_EVALUATION | MULTILINE_VARCHAR |  | GeneralProtocol |
| GENERAL_PROTOCOL.PROTOCOL_TYPE | MULTILINE_VARCHAR |  | GeneralProtocol |
| GENERAL_PROTOCOL.SPREADSHEET | XML |  | GeneralProtocol |
| GENERAL_PROTOCOL.TIME_REQUIREMENT | MULTILINE_VARCHAR |  | GeneralProtocol |
| GENETIC_MATERIAL | MULTILINE_VARCHAR |  | Gmo |
| GENETIC_MATERIAL_JUSTIFICATION | MULTILINE_VARCHAR |  | Gmo |
| GENETIC_MATERIAL_RISK_POTENTIAL | BOOLEAN |  | Gmo |
| GENTECH_BIOSAFETY_OFFICER | OBJECT | PERSON.BAM | BamGentechFacility |
| GENTECH_FACILITY | OBJECT | BAM_GENTECH_FACILITY | Gmo, GmoDonor, GmoRecipient, Plasmid |
| GENTECH_PROJECT_LEAD | OBJECT | PERSON.BAM | BamGentechFacility |
| GENTECH_SAFETY_LEVEL | CONTROLLEDVOCABULARY | GENTECH_SAFETY_LEVEL | BamGentechFacility |
| GIS_COORDINATES | VARCHAR |  | TestObjectExternal |
| GIVEN_NAME | VARCHAR |  | Person |
| GMO_DISPOSAL_DATE | DATE |  | Gmo |
| GMO_DONOR | OBJECT | SAMPLE.GMO_DONOR | Gmo |
| GMO_PRODUCTION_DATE | DATE |  | Gmo |
| GMO_RECIPIENT | OBJECT | SAMPLE.GMO_RECIPIENT | Gmo |
| GMO_RISK_GROUP | CONTROLLEDVOCABULARY | ORGANISM_RISK_GROUP | Gmo |
| GONIOMETER_TYPE | VARCHAR |  | PowderXRDMeasurement |
| GPIB | BOOLEAN |  | MeasuringAmplifier, Nanovoltmeter, PowerSupply |
| GPU_NODES_CONFIG | MULTILINE_VARCHAR |  | Hpc |
| HARDWARE_TRIGGER_INPUT | VARCHAR |  | IrCameraAcquisition |
| HAZARDOUS_SUBSTANCE | BOOLEAN |  | Chemical |
| HEATING_AREA_DESC | CONTROLLEDVOCABULARY | HEATING_AREA_DESC | ThermographyHeating |
| HEATING_DURATION_IN_SECONDS | REAL |  | ThermographyHeating |
| HEATING_FREQUENCY_IN_HERTZ | REAL |  | ThermographyHeating |
| HEATING_HEIGHT_IN_MILLIMETER | REAL |  | ThermographyHeating |
| HEATING_PRINCIPLE | CONTROLLEDVOCABULARY | HEATING_PRINCIPLE | ThermographyHeating |
| HEATING_TEMPERATURE_IN_CELSIUS | REAL |  | ThermographyHeating |
| HEATING_WIDTH_IN_MILLIMETER | REAL |  | ThermographyHeating |
| HEAT_SOURCE_DISTANCE_IN_MILLIMETER | REAL |  | ThermographySetup |
| HEAT_SOURCE_ORIENTATION | CONTROLLEDVOCABULARY | THERMOGRAPHIC_SETUP_HS_ORIENT | ThermographySetup |
| HOMEPAGE | HYPERLINK |  | Project |
| HPC_EXT_EMAIL_ADDRESS | VARCHAR |  | Hpc |
| HPC_EXT_PHYS_ADDRESS | VARCHAR |  | Hpc |
| HPC_JOB_ID | VARCHAR |  | PyironJob |
| HPC_JOB_QUEUE | VARCHAR |  | PyironJob |
| ID_EAKTE | VARCHAR |  | Sop |
| IMAGE_HORIZONTAL_RESOLUTION | INTEGER |  | Figure, ImageSeries, VideoRecording |
| IMAGE_SENSOR_FRAMERATE | REAL |  | Camera |
| IMAGE_SENSOR_NAME | VARCHAR |  | Camera |
| IMAGE_SENSOR_RESOLUTION_HORIZONTAL | INTEGER |  | Camera |
| IMAGE_SENSOR_RESOLUTION_VERTICAL | INTEGER |  | Camera |
| IMAGE_SENSOR_SIZE | VARCHAR |  | Camera |
| IMAGE_SERIES_COUNT | INTEGER |  | ImageSeries |
| IMAGE_VERTICAL_RESOLUTION | INTEGER |  | Figure, ImageSeries, VideoRecording |
| INCREMENT_DADN | REAL |  | FcgStep |
| INITIAL_CRACKLENGTH | REAL |  | FcgStep |
| INITIAL_CYCLES | INTEGER |  | FcgStep |
| INITIAL_DELTAF | REAL |  | FcgStep |
| INITIAL_DELTAK | REAL |  | FcgStep |
| INITIAL_FAMP | REAL |  | FcgStep |
| INITIAL_FMAX | REAL |  | FcgStep |
| INITIAL_FMEAN | REAL |  | FcgStep |
| INITIAL_FMIN | REAL |  | FcgStep |
| INITIAL_GEOMFUN | REAL |  | FcgStep |
| INITIAL_KAMP | REAL |  | FcgStep |
| INITIAL_KMAX | REAL |  | FcgStep |
| INITIAL_KMEAN | REAL |  | FcgStep |
| INITIAL_KMIN | REAL |  | FcgStep |
| INITIAL_R_RATIO | REAL |  | FcgStep |
| INITIAL_SSY_RATIO | REAL |  | FcgStep |
| INPUT_DATA_PACKAGE | OBJECT | DATA_TRANSFER_PACKAGE | DataTransfer |
| INSTRUMENT | OBJECT | (ALL) | Calibration |
| INSTRUMENT.LASER_SCANNER.LINE_RESOLUTION | INTEGER |  | LaserLineScanner |
| INSTRUMENT.LASER_SCANNER.X_MAX | REAL |  | LaserLineScanner |
| INSTRUMENT.LASER_SCANNER.X_MIN | REAL |  | LaserLineScanner |
| INSTRUMENT.LASER_SCANNER.Z_MAX | REAL |  | LaserLineScanner |
| INSTRUMENT.LASER_SCANNER.Z_MIN | REAL |  | LaserLineScanner |
| INSTRUMENT_CLASSIFICATION | CONTROLLEDVOCABULARY | MEASURING_INSTRUMENT_CLASSIFICATION | MeasuringInstrument |
| INSTRUMENT_STATUS | CONTROLLEDVOCABULARY | INSTRUMENT_STATUS | Instrument, MeasuringInstrument, TestingEquipment, TestingMachine |
| INTEGRATION_TIME_IN_MICROSECOND | REAL |  | IrCameraAcquisition |
| INVENTORY_NO | INTEGER |  | GasBottle, Instrument, TestingMachine, Welding |
| INVENTORY_NO_ADD | INTEGER |  | GasBottle, Instrument, TestingMachine, Welding |
| IONIZATION_TYPE | CONTROLLEDVOCABULARY | IONIZATION_TYPE | MassSpec |
| IR_CAMERA.TRIGGER_SETTING | CONTROLLEDVOCABULARY | IR_CAMERA.TRIGGER_SETTING | IrCameraAcquisition |
| IUPAC_NAME | VARCHAR |  | Chemical |
| JUPYTER_HEADERS | MULTILINE_VARCHAR |  | JupyterNotebook |
| JUPYTER_MODULES | MULTILINE_VARCHAR |  | JupyterNotebook |
| LASER_ANGLE | REAL |  | LaserMagnet |
| LASER_BEAM_DIAMETER_IN_MM | REAL |  | LaserGeneral |
| LASER_BEAM_PARAMETER_PROD | REAL |  | LaserMagnet |
| LASER_CLASS | VARCHAR |  | LaserLineScanner |
| LASER_FOCAL_DIAMETER | REAL |  | LaserMagnet |
| LASER_FOCAL_LENGTH | REAL |  | LaserMagnet |
| LASER_FOCAL_POSITION | REAL |  | LaserMagnet |
| LASER_M2 | REAL |  | LaserGeneral |
| LASER_OBSCURATION | REAL |  | LaserDiffPSDMeasurement |
| LASER_POWER | REAL |  | LaserMagnet |
| LASER_PULSE_ENERGY_NORMAL_IN_MJ | REAL |  | LaserGeneral |
| LASER_RAYLEIGH_LENGTH | REAL |  | LaserMagnet |
| LASER_REPETITION_RATE_IN_HZ | REAL |  | LaserGeneral |
| LASER_TRANSMISSION | REAL |  | LaserDiffPSDMeasurement |
| LASER_TYPE | CONTROLLEDVOCABULARY | LASER_TYPE | LaserGeneral |
| LASER_WAVELENGTH | VARCHAR |  | LaserLineScanner |
| LASER_WAVELENGTH_IN_NM | XML |  | LaserGeneral |
| LAST_CALIBRATION | DATE |  | Instrument, TestingMachine |
| LAST_CHECK | DATE |  | Norm, Sop, Task |
| LAST_SYSTEMCHECK | DATE |  | Camera, GasBottle, LaserLineScanner, Welding, WeldingEquipment |
| LATTICE_ANGALPHA_IN_DEG | REAL |  | Crystal |
| LATTICE_ANGBETA_IN_DEG | REAL |  | Crystal |
| LATTICE_ANGGAMMA_IN_DEG | REAL |  | Crystal |
| LATTICE_C_OVER_A | REAL |  | Crystal |
| LATTICE_PARAM_A_IN_A | REAL |  | Crystal |
| LATTICE_PARAM_B_IN_A | REAL |  | Crystal |
| LATTICE_PARAM_C_IN_A | REAL |  | Crystal |
| LATTICE_VOLUME_IN_A3 | REAL |  | Crystal |
| LENS_APERTURE_MAX | REAL |  | Lens |
| LENS_APERTURE_MIN | REAL |  | Lens |
| LENS_CONFOCAL | BOOLEAN |  | Lens |
| LENS_FOCALLENGTH | REAL |  | Lens |
| LENS_MOUNT_TYPE | VARCHAR |  | Camera |
| LICENSE | VARCHAR |  | Figure, Pseudopotential, SoftwareCode |
| LINK_EAKTE | HYPERLINK |  | Sop |
| LOAD_FRAME_ORIENTATION | CONTROLLEDVOCABULARY | LOAD_FRAME_ORIENTATION | LoadFrame |
| LOAD_FRAME_TYPE | VARCHAR |  | LoadFrame |
| LOCATION | VARCHAR |  | TestObjectExternal |
| LOCATION_ADDRESS | VARCHAR |  | Outdoor |
| LOCATION_LATITUDE_IN_DEGREES | REAL |  | Outdoor |
| LOCATION_LONGITUDE_IN_DEGREES | REAL |  | Outdoor |
| LOT_NUMBER | VARCHAR |  | Chemical, GlassWare |
| MAC_ADDRESS | VARCHAR |  | Instrument |
| MAGNET_FREQUENCY | REAL |  | LaserMagnet |
| MAGNET_MAX_FLUX_DENSITY | REAL |  | LaserMagnet |
| MAGNET_PRIMARY_CIRCUIT_CURRENT | REAL |  | LaserMagnet |
| MAGNET_PRIMARY_CIRCUIT_VOLTAGE | REAL |  | LaserMagnet |
| MANUFACTURER | VARCHAR |  | Aluminium, AuxiliaryMaterial, Chemical, GlassWare, Instrument, MeasuringInstrument, Sample, SampleHolder, Steel, Test... |
| MASS_MOLAR | REAL |  | Chemical |
| MASS_SPEC_TYPE | CONTROLLEDVOCABULARY | MASS_SPEC_TYPE | MassSpec |
| MATERIAL | VARCHAR |  | Named |
| MATERIAL_GROUP | VARCHAR |  | RawMaterialCode |
| MATERIAL_NUMBER | VARCHAR |  | RawMaterialCode |
| MAT_BONDING_TYPE | VARCHAR |  | MaterialV1 |
| MAT_CODE | OBJECT | RAW_MATERIAL_CODE | Aluminium, Steel |
| MAT_SCALE | CONTROLLEDVOCABULARY | MAT_SCALE | MatModel |
| MAT_STRUCTURE | CONTROLLEDVOCABULARY | MAT_STRUCTURE | MaterialV1 |
| MAXRANGE | REAL |  | Nanovoltmeter |
| MAXRANGE_RESOLUTION | REAL |  | Nanovoltmeter |
| MAX_COMMON_MODE_VOLTAGE | REAL |  | MeasuringAmplifier |
| MAX_DYNAMIC_FORCE | REAL |  | AlignmentFixture, ForceTransducer, HydraulicCylinder, LoadFrame |
| MAX_EXCITATION_VOLTAGE | REAL |  | ForceTransducer, HydraulicCylinder, MeasuringAmplifier |
| MAX_ITERS | INTEGER |  | Lammps |
| MAX_LOAD_DYNAMIC_PRIMARY | REAL |  | TestingMachine |
| MAX_LOAD_DYNAMIC_SECONDARY | REAL |  | TestingMachine |
| MAX_LOAD_STATIC_PRIMARY | REAL |  | TestingMachine |
| MAX_LOAD_STATIC_SECONDARY | REAL |  | TestingMachine |
| MAX_OUTPUT_CURRENT | REAL |  | PowerSupply |
| MAX_OUTPUT_VOLTAGE | REAL |  | PowerSupply |
| MAX_PRESSURE | REAL |  | Servovalve |
| MAX_PULSE_ENERGY_IN_JOULE | REAL |  | FlashLamp |
| MAX_SPACE_HOR | REAL |  | LoadFrame |
| MAX_SPACE_VERT | REAL |  | LoadFrame |
| MAX_STATIC_FORCE | REAL |  | AlignmentFixture, CreepTestTestMachine, ForceTransducer, HydraulicCylinder, LoadFrame |
| MAX_STROKE | REAL |  | TestingMachine |
| MEASUREMENT_DATE | DATE |  | SaxsMeasurement |
| MEASUREMENT_ID | INTEGER |  | LaserDiffPSDMeasurement, SaxsMeasurement |
| MEASUREMENT_MODE | VARCHAR |  | SIMS |
| MEASUREMENT_PROTOCOL_FILE | MULTILINE_VARCHAR |  | MouseMeasurement |
| MEASUREMENT_PROTOCOL_FILE.SOFTWARE_NAME | VARCHAR |  | MeasurementProtocolFile |
| MEASUREMENT_PROTOCOL_FILE.SOFTWARE_VERSION | VARCHAR |  | MeasurementProtocolFile |
| MEASUREMENT_PROTOCOL_OPTIONS | VARCHAR |  | MouseMeasurement |
| MEASUREMENT_QUANTITY | CONTROLLEDVOCABULARY | MEASUREMENT_QUANTITY | TestingEquipment |
| MEAS_MEDIUM_TEMPERATURE_IN_CELSIUS | REAL |  | LaserDiffPSDMeasurement |
| MIC_FCG_FRACSURF_CRACKLENGTH_CYCLES | INTEGER |  | MicroscopyFcgFractureSurfaceCracklength |
| MIC_FCG_FRACSURF_CRACKLENGTH_TYPE | CONTROLLEDVOCABULARY | MICROSCOPY_FCG_CRACKLENGTH_TYPE | MicroscopyFcgFractureSurfaceCracklength |
| MIC_FCG_FRACSURF_CRACKLENGTH_VALUE | REAL |  | MicroscopyFcgFractureSurfaceCracklength |
| MINRANGE | REAL |  | Nanovoltmeter |
| MINRANGE_RESOLUTION | REAL |  | Nanovoltmeter |
| MIN_EXCITATION_VOLTAGE | REAL |  | MeasuringAmplifier |
| MISC_HYD_COMP_TYPE | VARCHAR |  | HydraulicMisc |
| MODEL_NAME | VARCHAR |  | Tool |
| MODE_COUNT | INTEGER |  | LaserDiffPSDMeasurement |
| MONITORING_DATE | DATE |  | Control |
| MONITORING_VALUE | VARCHAR |  | Control |
| MS_ACQUISITION_MODE | CONTROLLEDVOCABULARY | MS_ACQUISITION_MODE | MsBatch |
| MS_INTENSITY_RANGE | VARCHAR |  | MsBatch |
| MS_ION_POLARITY | CONTROLLEDVOCABULARY | MS_ION_POLARITY | MsBatch |
| MS_MASS_RANGE | VARCHAR |  | MsBatch |
| MS_RESOLUTION | REAL |  | MsBatch |
| MS_SCAN_RATE | REAL |  | MsBatch |
| MURN_EQN_OF_STATE | CONTROLLEDVOCABULARY | MURN_EQN_OF_STATE | Murnaghan |
| MURN_FIT_EQN_ORDER | INTEGER |  | Murnaghan |
| MURN_N_DATA_POINTS | INTEGER |  | Murnaghan |
| MURN_STRAINVOL_RANGE | REAL |  | Murnaghan |
| MURN_STRAIN_AXES | VARCHAR |  | Murnaghan |
| NAME_OPTICAL_PARAMETERSET_SAMPLE | VARCHAR |  | LaserDiffPSDMeasurement |
| NCORES | INTEGER |  | PyironJob |
| NDT.MATERIAL | VARCHAR |  | SampleNdt |
| NDT.MATERIAL_NUMBER | VARCHAR |  | SampleNdt |
| NGPUS | INTEGER |  | PyironJob |
| NMR.ACQUISITION_TIME | REAL |  | Nmr |
| NMR.END_CHEMICAL_SHIFT | REAL |  | Nmr |
| NMR.EXPERIMENT | CONTROLLEDVOCABULARY | NMR_EXPERIMENT_TYPES | Nmr |
| NMR.FREQUENCY | REAL |  | Nmr |
| NMR.INSTRUMENT | VARCHAR |  | Nmr |
| NMR.INTERPULSE_DELAY | REAL |  | Nmr |
| NMR.IS_QNMR | BOOLEAN |  | Nmr |
| NMR.NUCLEUS_DIRECT | CONTROLLEDVOCABULARY | NMR_NUCLEI | Nmr |
| NMR.NUCLEUS_INDIRECT | CONTROLLEDVOCABULARY | NMR_NUCLEI | Nmr |
| NMR.PULSE_ANGLE | REAL |  | Nmr |
| NMR.SCANS | INTEGER |  | Nmr |
| NMR.SOLVENT | CONTROLLEDVOCABULARY | NMR_SOLVENTS | Nmr |
| NMR.START_CHEMICAL_SHIFT | REAL |  | Nmr |
| NORM_ANALYZED_MATRIX | VARCHAR |  | Norm |
| NORM_TITLE | VARCHAR |  | Norm |
| NORM_URL | HYPERLINK |  | Norm |
| NOTES | MULTILINE_VARCHAR |  | Aluminium, AnalysisNotebook, AnalyzedData, Attachment, AuxiliaryMaterial, BamGentechFacility, Calibration, Chemical, ... |
| NTHREADS | INTEGER |  | PyironJob |
| NUC_PERFORMED | CONTROLLEDVOCABULARY | NUC_PERFORMED | IrCameraAcquisition |
| NUMBER_CONSECUTIVE_ACQUISITONS | INTEGER |  | IrCameraAcquisition |
| NUMBER_OF_ANALOG_OUTPUTS | INTEGER |  | MeasuringAmplifier, Nanovoltmeter |
| NUMBER_OF_CHANNELS | INTEGER |  | Nanovoltmeter |
| NUMBER_OF_INPUTS | INTEGER |  | MeasuringAmplifier |
| NUMBER_OF_OUTPUTS | INTEGER |  | PowerSupply |
| NUMBER_PRETRIGGER_FRAMES | INTEGER |  | IrCameraAcquisition |
| NUMBER_RECORDED_FRAMES | INTEGER |  | IrCameraAcquisition |
| N_ATOMS_TOTAL | INTEGER |  | Amorphous, Crystal |
| OLD_DB_NAME | VARCHAR |  | TestObjectBAM |
| OPERATING_SYSTEM | CONTROLLEDVOCABULARY | OPERATING_SYSTEM | Hpc, LocalWorkstation |
| OPERATOR | VARCHAR |  | ExperimentalStep |
| ORDER.PRICE_PAID | REAL |  | Order |
| ORGANISM_FAMILY | VARCHAR |  | Organism |
| ORGANISM_FOOTNOTE | CONTROLLEDVOCABULARY | ORGANISM_FOOTNOTE_ZKBS | Organism |
| ORGANISM_GROUP | CONTROLLEDVOCABULARY | ORGANISM_GROUP | Organism |
| ORGANISM_RISK_GROUP | CONTROLLEDVOCABULARY | ORGANISM_RISK_GROUP | Organism |
| ORGANISM_ZKBS_STATEMENT | HYPERLINK |  | Organism |
| OWNER | VARCHAR |  | TestObjectExternal |
| PARAMETER_SET.SPREADSHEET | XML |  | ParameterSet |
| PARFIS_PROJECT_NO | VARCHAR |  | Project, TestObjectBAM |
| PERIODIC_BOUNDARY_X | BOOLEAN |  | Lammps |
| PERIODIC_BOUNDARY_Y | BOOLEAN |  | Lammps |
| PERIODIC_BOUNDARY_Z | BOOLEAN |  | Lammps |
| PERSON_ALIAS | VARCHAR |  | SpecificPersonInfo |
| PERSON_STATUS | CONTROLLEDVOCABULARY | PERSON_STATUS | SpecificPersonInfo |
| PHYSICAL_STATE | CONTROLLEDVOCABULARY | PHYSICAL_STATE | Sample |
| PLASMID_BACTERIAL_ANTIBIOTIC_RESISTANCE | CONTROLLEDVOCABULARY | PLASMID_BACTERIAL_ANTIBIOTIC_RESISTANCE | GmoRecipient, Plasmid |
| PLASMID_MARKER | VARCHAR |  | Plasmid |
| PLASMID_ORI | CONTROLLEDVOCABULARY | PLASMID_ORI | Plasmid |
| PLASMID_OTHER_MARKER | VARCHAR |  | Plasmid |
| PLOT_LEGEND | MULTILINE_VARCHAR |  | Plot |
| PLOT_X_LABEL | VARCHAR |  | Plot |
| PLOT_X_RANGE | REAL |  | Plot |
| PLOT_X_UNITS | VARCHAR |  | Plot |
| PLOT_Y_LABEL | VARCHAR |  | Plot |
| PLOT_Y_RANGE | REAL |  | Plot |
| PLOT_Y_UNITS | VARCHAR |  | Plot |
| PLOT_Z_LABEL | VARCHAR |  | Plot |
| PLOT_Z_RANGE | REAL |  | Plot |
| PLOT_Z_UNITS | VARCHAR |  | Plot |
| POSITIONER_AXIS_COUNT | INTEGER |  | Positioner |
| POSITIONER_PAYLOAD_MAX | REAL |  | Positioner |
| POSITIONER_TYPE | CONTROLLEDVOCABULARY | POSITIONER_TYPE | Positioner |
| POWER_IN_WATT | REAL |  | ThermographyHeating |
| PRECISION_MASS | REAL |  | Scale |
| PROCEDURE | MULTILINE_VARCHAR |  | GeneralProtocol |
| PROCESSING_PROTOCOL_FILE | MULTILINE_VARCHAR |  | MouseMeasurement |
| PRODUCT.CATEGORY | VARCHAR |  | Product |
| PRODUCT.COMPANY | VARCHAR |  | Product |
| PRODUCT.DESCRIPTION | MULTILINE_VARCHAR |  | Product |
| PRODUCT.HAZARD_STATEMENT | VARCHAR |  | Product |
| PRODUCT.PRODUCT_SECONDARY_NAMES | VARCHAR |  | Product |
| PRODUCT.SIZE_OF_ITEM | VARCHAR |  | Product |
| PRODUCTION_DATE | DATE |  | Figure, TestObject |
| PRODUCT_CATEGORY | CONTROLLEDVOCABULARY | CHEMICAL_PRODUCT_CATEGORY | Chemical |
| PROJECT_LEADER | VARCHAR |  | Project |
| PROJECT_LEADER_BAM | OBJECT | PERSON.BAM | Project |
| PROJECT_NAME | VARCHAR |  | TestObjectBAM |
| PROJECT_STATUS | CONTROLLEDVOCABULARY | PROJECT_STATUS | Project |
| PROPAGATION | BOOLEAN |  | FcgStep |
| PSEUDOPOT_FUNC | CONTROLLEDVOCABULARY | PSEUDOPOT_FUNCTIONAL | Pseudopotential |
| PSEUDOPOT_SEMICORE | VARCHAR |  | Pseudopotential |
| PSEUDOPOT_TYPE | CONTROLLEDVOCABULARY | PSEUDOPOT_TYPE | Pseudopotential |
| PSP_NUMBER | VARCHAR |  | BuildingMaterialsSpecimen |
| PUBLICATION | MULTILINE_VARCHAR |  | DefaultExperiment, ExperimentalStep, GeneralProtocol |
| PULSE_ENERGY_IN_JOULE | REAL |  | ThermographyHeating |
| PURITY_IN_PERCENTAGE | REAL |  | RmEthanol |
| QUEUING_SYSTEM | CONTROLLEDVOCABULARY | QUEUING_SYSTEM | Hpc |
| RATED_FLOW | REAL |  | Servovalve |
| RATED_POWER | REAL |  | Servovalve |
| RAWMAT_MECHPROP_SUPPLIER_BREAKELONGATION_10_MAX | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_BREAKELONGATION_10_MIN | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_BREAKELONGATION_5_MAX | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_BREAKELONGATION_5_MIN | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_LOWERYIELDSTRENGTH_MAX | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_LOWERYIELDSTRENGTH_MIN | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_UNIFORMELONGATION_MAX | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_UNIFORMELONGATION_MIN | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_UPPERYIELDSTRENGTH_MAX | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_UPPERYIELDSTRENGTH_MIN | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_UTS_MAX | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_UTS_MIN | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_YIELDLIMIT_MAX | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_YIELDLIMIT_MIN | REAL |  | Aluminium, Steel |
| RAWMAT_MECHPROP_SUPPLIER_YOUNGSMODULUS | REAL |  | Aluminium, Steel |
| RAWMAT_MECH_PROP_SUPPLIER_DENSITY | REAL |  | Aluminium, Steel |
| RAW_MAT_AMOUNT_IN_STOCK | INTEGER |  | Aluminium, Steel |
| RAW_MAT_BATCH_NUMBER | VARCHAR |  | Aluminium, Steel |
| RAW_MAT_COMPONENT_DESCRIPTION | VARCHAR |  | Aluminium, Steel |
| RAW_MAT_DIAMETER | REAL |  | Aluminium, Steel |
| RAW_MAT_FORM | CONTROLLEDVOCABULARY | RAW_MAT_FORM | Aluminium, Steel |
| RAW_MAT_LENGTH | REAL |  | Aluminium, Steel |
| RAW_MAT_THICKNESS | REAL |  | Aluminium, Steel |
| RAW_MAT_WIDTH | REAL |  | Aluminium, Steel |
| RAZOR_DEPTH | REAL |  | RazorbladeNotching |
| RAZOR_STROKECOUNT | REAL |  | RazorbladeNotching |
| RAZOR_STROKELENGTH | REAL |  | RazorbladeNotching |
| RAZOR_STROKESPEED | REAL |  | RazorbladeNotching |
| RECIPIENT | OBJECT | ORGANISM | GmoRecipient |
| RECIPIENT_RISK_GROUP | CONTROLLEDVOCABULARY | ORGANISM_RISK_GROUP | GmoRecipient |
| REFERENCE | MULTILINE_VARCHAR |  | DefaultExperiment, ExperimentalStep, GeneralProtocol, Hpc, InteratomicPotential, MatModel, Pseudopotential, SoftwareC... |
| REFRACTIVE_INDEX_BLUE_SAMPLE | REAL |  | LaserDiffPSDMeasurement |
| REFRACTIVE_INDEX_SAMPLE | REAL |  | LaserDiffPSDMeasurement |
| REQUEST.BUYER | VARCHAR |  | Request |
| REQUEST.DEPARTMENT | VARCHAR |  | Request |
| REQUEST.PROJECT | VARCHAR |  | Request |
| RESEARCH_BAM_PROJECT_ID | VARCHAR |  | Project |
| RESPONSIBLE_PERSON | OBJECT | PERSON.BAM | Chemical, Fcg, GasBottle, Hpc, Instrument, MeasurementSession, MeasuringInstrument, MouseMeasurement, Named, Norm, Sa... |
| ROBOT_AXIS_COUNT | INTEGER |  | Robot |
| ROBOT_CONTROLLER_AXIS_COUNT | INTEGER |  | RobotController |
| ROBOT_CONTROLLER_AXIS_COUNT_EXTERNAL | INTEGER |  | RobotController |
| ROBOT_PAYLOAD_MAX | INTEGER |  | Robot |
| ROBOT_TYPE | CONTROLLEDVOCABULARY | ROBOT_TYPE | Robot |
| ROBOT_WORKING_RANGE | REAL |  | Robot |
| ROTATION_SPEED | REAL |  | PowderXRDMeasurement |
| RS232 | BOOLEAN |  | MeasuringAmplifier, Nanovoltmeter, PowerSupply |
| RTD_ACCURACY_CLASS | CONTROLLEDVOCABULARY | RTD_ACCURACY_CLASS | Rtd |
| RTD_CABLE_LENGTH | REAL |  | Rtd |
| RTD_CONNECTION | CONTROLLEDVOCABULARY | RTD_CONNECTION_TYPE | Rtd |
| RTD_COVER_TUBE_DIAMETER | REAL |  | Rtd |
| RTD_COVER_TUBE_LENGTH | REAL |  | Rtd |
| RTD_INSULATION_MATERIAL | CONTROLLEDVOCABULARY | RTD_INSULATION_MATERIAL | Rtd |
| RTD_MAX_TEMP | REAL |  | Rtd |
| RTD_MIN_TEMP | REAL |  | Rtd |
| RTD_TYPE | CONTROLLEDVOCABULARY | RTD_TYPE | Rtd |
| SAMPLE_AGE_IN_DAYS | INTEGER |  | BuildingMaterialsSpecimen |
| SAMPLE_ANALYTE | VARCHAR |  | MsCenter |
| SAMPLE_CONSUMED | BOOLEAN |  | MsCenter |
| SAMPLE_DIMENSIONS_SET_POINTS | VARCHAR |  | BuildingMaterialsSpecimen |
| SAMPLE_GEOMETRY | CONTROLLEDVOCABULARY | SAMPLE_GEOMETRY | BuildingMaterialsSpecimen |
| SAMPLE_HOLDER_MATERIAL | CONTROLLEDVOCABULARY | SAMPLE_HOLDER_MATERIAL | SampleHolder |
| SAMPLE_HOLDER_THICKNESS_IN_MM | REAL |  | SampleHolder |
| SAMPLE_ID | VARCHAR |  | LaserDiffPSDMeasurement, Named |
| SAMPLE_ID_NUMBER | INTEGER |  | Sample |
| SAMPLE_LOCATION | VARCHAR |  | MsCenter |
| SAMPLE_MATRIX | MULTILINE_VARCHAR |  | MsCenter |
| SAMPLE_NAME | VARCHAR |  | MsCenter |
| SAMPLE_ORIGIN | CONTROLLEDVOCABULARY | SAMPLE_ORIGIN | BuildingMaterialsSpecimen |
| SAMPLE_POSITION | VARCHAR |  | MouseMeasurement |
| SAMPLE_PROVIDER | VARCHAR |  | MsCenter |
| SAMPLE_RECEIVED | TIMESTAMP |  | CreepTestMaterialHistoryAndCondition, MsCenter |
| SAMPLE_TREATMENT | MULTILINE_VARCHAR |  | ThermographySetup |
| SCAN_LINE_COUNT | INTEGER |  | ProfileScan |
| SCAN_LINE_RESOLUTION | INTEGER |  | ProfileScan |
| SCATTERING_MODEL_PSD_LD | CONTROLLEDVOCABULARY | SCATTERING_MODEL_PSD_LD | LaserDiffPSDMeasurement |
| SEM.ACCELERATIONVOLTAGE | VARCHAR |  | Sem |
| SEM.DETECTOR | VARCHAR |  | Sem |
| SEM.IMAGESIZEX | VARCHAR |  | Sem |
| SEM.IMAGESIZEY | VARCHAR |  | Sem |
| SEM.INSTRUMENT | VARCHAR |  | Sem |
| SEM.MAGNIFICATION | VARCHAR |  | Sem |
| SEM.OPERATINGMODE | VARCHAR |  | Sem |
| SEM.PIXELSIZEX | VARCHAR |  | Sem |
| SEM.PIXELSIZEY | VARCHAR |  | Sem |
| SEM.PROJECTORMODE | VARCHAR |  | Sem |
| SEM.WORKINGDISTANCE | VARCHAR |  | Sem |
| SERIAL_NUMBER | VARCHAR |  | Instrument, MeasuringInstrument, TestingEquipment, TestingMachine, Tool |
| SETUP_CONFIGURATION | CONTROLLEDVOCABULARY | THERMOGRAPHIC_SETUP_CONFIG | ThermographySetup |
| SFTW_COMPATIBILITY | VARCHAR |  | InteratomicPotential |
| SHIELDING_GAS_COMPOSITION | VARCHAR |  | LaserMagnet |
| SHIELDING_GAS_FLOWRATE | REAL |  | LaserMagnet |
| SHIELDING_GAS_NOZZLE_ANGLE | REAL |  | LaserMagnet |
| SHIELDING_GAS_NOZZLE_DISTANCE | REAL |  | LaserMagnet |
| SIMS_DSC_CURRENT | REAL |  | SIMS |
| SIMS_DSC_RASTER_SIZE | REAL |  | SIMS |
| SIMS_DSC_VOLTAGE | REAL |  | SIMS |
| SIMS_LMIG_CURRENT_DC | REAL |  | SIMS |
| SIMS_LMIG_CURRENT_P | REAL |  | SIMS |
| SIMS_LMIG_PULSE_WIDTH | REAL |  | SIMS |
| SIMS_LMIG_RASTER_SIZE | REAL |  | SIMS |
| SIMS_POLARITY | CONTROLLEDVOCABULARY | MS_ION_POLARITY | SIMS |
| SIMS_PRIMARY_ION | CONTROLLEDVOCABULARY | SIMS_PRIMARY_ION | SIMS |
| SIM_CELL_ANGLES_IN_DEG | VARCHAR |  | MatSimStructure |
| SIM_CELL_LENGTHS_IN_A | VARCHAR |  | MatSimStructure |
| SIM_CELL_VECTORS | VARCHAR |  | MatSimStructure |
| SIM_CELL_VOLUME_IN_A3 | REAL |  | MatSimStructure |
| SIM_CORETIME_IN_HOURS | REAL |  | PyironJob |
| SIM_JOB_FINISHED | BOOLEAN |  | PyironJob |
| SIM_VIS_CBAR | BOOLEAN |  | SimVis |
| SIM_VIS_CBAR_MAX | REAL |  | SimVis |
| SIM_VIS_CBAR_MIN | REAL |  | SimVis |
| SIM_VIS_CBAR_PROP | VARCHAR |  | SimVis |
| SIM_VIS_CBAR_UNITS | VARCHAR |  | SimVis |
| SIM_VIS_COORD | BOOLEAN |  | SimVis |
| SIM_VIS_COORD_X | VARCHAR |  | SimVis |
| SIM_VIS_COORD_Y | VARCHAR |  | SimVis |
| SIM_VIS_COORD_Z | VARCHAR |  | SimVis |
| SIM_VIS_SCBAR | BOOLEAN |  | SimVis |
| SIM_VIS_SCBAR_UNITS | VARCHAR |  | SimVis |
| SIM_WALLTIME_IN_HOURS | REAL |  | PyironJob |
| SIZE_EFFECTIVE_MM | REAL |  | InstrumentAccessory |
| SIZE_HEIGHT_IN_MILLIMETER | REAL |  | Named |
| SIZE_THICKNESS_IN_MILLIMETER | REAL |  | MouseMeasurement, Named |
| SIZE_WIDTH_IN_MILLIMETER | REAL |  | Named |
| SOFTWARE_NAME | VARCHAR |  | SoftwareCode |
| SOURCE_CODE_LANGUAGE | VARCHAR |  | ComputationalAnalysis, JupyterNotebook, SourceCodeWorkflow |
| SOURCE_LINK | MULTILINE_VARCHAR |  | InteratomicPotential, SoftwareCode |
| SPACE_GROUP | CONTROLLEDVOCABULARY | SPACE_GROUP | Crystal |
| SPECTROMETER_TYPE | CONTROLLEDVOCABULARY | OPTICAL_SPECTROMETER_TYPE | SpectrometerOptical |
| SPEC_FCG_NOTCHLENGTH_MIDDLE | REAL |  | Fcg |
| SPEC_FCG_NOTCHLENGTH_SIDE1 | REAL |  | Fcg |
| SPEC_FCG_NOTCHLENGTH_SIDE2 | REAL |  | Fcg |
| SPEC_FCG_NOTCHTYPE | CONTROLLEDVOCABULARY | NOTCH_TYPE_FCG | Fcg |
| SPEC_FCG_THICKNESS | REAL |  | Fcg |
| SPEC_FCG_TYPE | CONTROLLEDVOCABULARY | SPECIMEN_TYPE_FCG_TEST | Fcg |
| SPEC_FCG_WIDTH_SIDE1 | REAL |  | Fcg |
| SPEC_FCG_WIDTH_SIDE2 | REAL |  | Fcg |
| SPEC_STATUS | CONTROLLEDVOCABULARY | SPECIMEN_STATUS | Fcg |
| SPUTTER_SOURCE | VARCHAR |  | SIMS |
| START_2THETA | REAL |  | PowderXRDMeasurement |
| START_DATE | TIMESTAMP |  | DefaultExperiment, ExperimentalStep, Project, PyironJob, Test |
| STATE_CHECK | BOOLEAN |  | Norm, Sop, Task |
| STEEL_TREATMENT_FIRST | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_STEEL | Steel |
| STEEL_TREATMENT_FOURTH | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_STEEL | Steel |
| STEEL_TREATMENT_SECOND | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_STEEL | Steel |
| STEEL_TREATMENT_THIRD | CONTROLLEDVOCABULARY | RAW_MAT_TREATMENT_STEEL | Steel |
| STEP_NO | INTEGER |  | FcgStep |
| STEP_SIZE_2THETA | REAL |  | PowderXRDMeasurement |
| STITCHING | BOOLEAN |  | SIMS |
| STITCHING_FRAMES_PER_PATCH | INTEGER |  | SIMS |
| STITCHING_PIXEL_DENSITY | REAL |  | SIMS |
| STITCHING_TOTAL_AREA | VARCHAR |  | SIMS |
| STOP_CONDITION | VARCHAR |  | SIMS |
| SUBFRAME | CONTROLLEDVOCABULARY | SUBFRAME_TYPE | IrCameraAcquisition |
| SUBSTANCE_EMPTY | BOOLEAN |  | Chemical |
| SUN_IRRADIANCE_IN_WATT_PER_METER_SQUARED | REAL |  | Outdoor |
| SUPPLIER | VARCHAR |  | Aluminium, AuxiliaryMaterial, Chemical, CreepTestMaterialHistoryAndCondition, GasBottle, GlassWare, Instrument, Organ... |
| SUPPLIER.ADDITIONAL_INFORMATION | VARCHAR |  | Supplier |
| SUPPLIER.COMPANY_CONTACT_EMAIL | VARCHAR |  | Supplier |
| SUPPLIER.COMPANY_CONTACT_NAME | VARCHAR |  | Supplier |
| SUPPLIER.PREFERRED_ORDER_METHOD | CONTROLLEDVOCABULARY | $SUPPLIER.PREFERRED_ORDER_METHOD | Supplier |
| SUPPLIER.URL | HYPERLINK |  | Supplier |
| SURFACE_PREPARATION | VARCHAR |  | LaserMagnet |
| SW_COMPATIBILITY | VARCHAR |  | Pseudopotential |
| TC_CABLE_LENGTH | REAL |  | Thermocouple |
| TC_CONNECTOR | BOOLEAN |  | Thermocouple |
| TC_DIAMETER | REAL |  | Thermocouple |
| TC_MAX_TEMP | REAL |  | Thermocouple |
| TC_MIN_TEMP | REAL |  | Thermocouple |
| TC_TYPE | CONTROLLEDVOCABULARY | THERMOCOUPLE_TYPE | Thermocouple |
| TECHNIKUM_MATERIAL_AMOUNT | VARCHAR |  | Technikum |
| TECHNIKUM_MATERIAL_USAGE | CONTROLLEDVOCABULARY | MATERIAL_USAGE_TECHNIKUM | Technikum |
| TECHNIKUM_SUBSTANCE_CONCENTRATION | REAL |  | Technikum |
| TELEPHONE | VARCHAR |  | Person |
| TEM.ACCELERATIONVOLTAGE | VARCHAR |  | Tem |
| TEM.C2_APERTURE_NAME | VARCHAR |  | Tem |
| TEM.CAMERALENGTH | VARCHAR |  | Tem |
| TEM.DETECTOR | VARCHAR |  | Tem |
| TEM.GUN_LENS_SETTING | VARCHAR |  | Tem |
| TEM.IMAGESIZEX | VARCHAR |  | Tem |
| TEM.IMAGESIZEY | VARCHAR |  | Tem |
| TEM.INSTRUMENT | VARCHAR |  | Tem |
| TEM.MAGNIFICATION | VARCHAR |  | Tem |
| TEM.OBJ_APERTURE_NAME | VARCHAR |  | Tem |
| TEM.OPERATINGMODE | VARCHAR |  | Tem |
| TEM.PIXELSIZEX | VARCHAR |  | Tem |
| TEM.PIXELSIZEY | VARCHAR |  | Tem |
| TEM.PROJECTORMODE | VARCHAR |  | Tem |
| TEM.SAED_APERTUREDIAMETER | VARCHAR |  | Tem |
| TEM.SAED_APERTUREPOSX | VARCHAR |  | Tem |
| TEM.SAED_APERTUREPOSY | VARCHAR |  | Tem |
| TEM.SPOT_INDEX | VARCHAR |  | Tem |
| TEMPERATURE_IN_KELVIN | REAL |  | CreepTest |
| TEMPORAL_HEATING_STRUCTURE | CONTROLLEDVOCABULARY | TEMPORAL_HEATING_STRUCTURE | ThermographyHeating |
| TEMP_MAX_CELSIUS | REAL |  | Freezer1, Freezer2 |
| TEMP_MIN_CELSIUS | REAL |  | Freezer1, Freezer2 |
| TESTING_MACHINE_DRIVE_TYPE | CONTROLLEDVOCABULARY | TESTING_MACHINE_DRIVE_TYPE | TestingMachine |
| TESTING_MACHINE_LOAD_TYPE | CONTROLLEDVOCABULARY | TESTING_MACHINE_LOAD_TYPE | TestingMachine |
| TEST_METHOD_KIND | CONTROLLEDVOCABULARY | TEST_METHOD_KIND | MeasuringInstrument, TestMethod |
| TEST_OBJ_EXT_HEIGHT | REAL |  | TestObjectExternal |
| TEST_OBJ_EXT_LENGTH | REAL |  | TestObjectExternal |
| TEST_OBJ_EXT_WEIGHT | REAL |  | TestObjectExternal |
| TEST_OBJ_EXT_WIDTH | REAL |  | TestObjectExternal |
| TEST_OBJ_HEIGHT | INTEGER |  | TestObject |
| TEST_OBJ_LENGTH | INTEGER |  | TestObject |
| TEST_OBJ_MATERIAL | CONTROLLEDVOCABULARY | BUILDING_MATERIAL_TYPE | TestObject, TestObjectExternal |
| TEST_OBJ_STATUS | CONTROLLEDVOCABULARY | TEST_OBJECT_STATUS | TestObject |
| TEST_OBJ_WEIGHT | REAL |  | TestObjectBAM |
| TEST_OBJ_WIDTH | INTEGER |  | TestObject |
| TEST_SETUP_TYPE | CONTROLLEDVOCABULARY | TEST_SETUP_TYPE | Test |
| TEST_TYPE | CONTROLLEDVOCABULARY | TEST_PROGRAM_TYPE | FcgEvaluation |
| THERMOCOUPLES_SETUP | XML |  | LaserMagnet |
| THICKNESS_IN_MILLIMETER | REAL |  | ObjectiveSpacer |
| TIME_PER_STEP | REAL |  | PowderXRDMeasurement |
| TLC_LASER_PROGRAM_NAME | VARCHAR |  | LaserMagnet |
| TLC_ROBOT_PROGRAM_NAME | VARCHAR |  | LaserMagnet |
| TOOL_PURPOSE | CONTROLLEDVOCABULARY | TOOL_PURPOSE | Tool |
| TRAINED_PERSON | OBJECT | PERSON.BAM | DeviceTraining |
| TUBE_CONFIGURATION_NAME | VARCHAR |  | PowderXRDMeasurement |
| TUBE_MATERIAL | VARCHAR | TUBE_MATERIAL | PowderXRDMeasurement |
| UNIT_MASS | CONTROLLEDVOCABULARY | UNIT_MASS | Scale |
| USB | BOOLEAN |  | MeasuringAmplifier, Nanovoltmeter, PowerSupply |
| USED_CALIBRATION_RANGE_MAX_IN_CELSIUS | REAL |  | IrCameraAcquisition |
| USED_CALIBRATION_RANGE_MIN_IN_CELSIUS | REAL |  | IrCameraAcquisition |
| UUID | VARCHAR |  | ImageSeries, ProfileScan, VideoRecording, Weldment |
| VALVE_MODEL_ID | VARCHAR |  | Servovalve |
| VALVE_TYPE_ID | VARCHAR |  | Servovalve |
| VECTOR | OBJECT | SAMPLE.PLASMID | Gmo |
| VERSION | VARCHAR |  | Document, Norm, Pseudopotential, SoftwareCode, Sop, TestFile |
| VIDEO_CODEC | VARCHAR |  | VideoRecording |
| VIDEO_DYNAMIC_FRAMERATE | BOOLEAN |  | VideoRecording |
| VIDEO_FRAME_PER_SECONDS | INTEGER |  | VideoRecording |
| VOLTAGE | REAL |  | PowderXRDMeasurement |
| VOLUME_MAX_IN_ML | REAL |  | GlassWare |
| VOLUME_MIN_IN_ML | REAL |  | GlassWare |
| VOLUME_PERCENT_ARGON | REAL |  | GasBottle |
| VOLUME_PERCENT_CARBON_DIOXIDE | REAL |  | GasBottle |
| VOLUME_PERCENT_HELIUM | REAL |  | GasBottle |
| VOLUME_PERCENT_HYDROGEN | REAL |  | GasBottle |
| VOLUME_PERCENT_NITROGEN | REAL |  | GasBottle |
| VOLUME_PERCENT_OXYGEN | REAL |  | GasBottle |
| WATER_TO_CEMENT_RATIO | MULTILINE_VARCHAR |  | ConcreteMixture |
| WEATHER_CONDITION | CONTROLLEDVOCABULARY | WEATHER_CONDITION | Outdoor |
| WEIGHTED_DEVIATION | REAL |  | LaserDiffPSDMeasurement |
| WEIGHT_MAX | REAL |  | Scale |
| WEIGHT_MIN | REAL |  | Scale |
| WELDING.ARC_CURRENT_CONTINUOUS | REAL |  | GmawWeldingPowerSource |
| WELDING.ARC_CURRENT_MAX | REAL |  | GmawWeldingPowerSource |
| WELDING.ARC_CURRENT_MIN | REAL |  | GmawWeldingPowerSource |
| WELDING.TORCH_TYPE | CONTROLLEDVOCABULARY | WELDING.GMAW_TORCH_TYPE | GmawTorch |
| WELDING_TRAVEL_SPEED | REAL |  | LaserMagnet |
| WELDING_WIRE.AWS_SPECNAME | VARCHAR |  | WireSolid |
| WELDING_WIRE.AWS_STANDARD | VARCHAR |  | WireSolid |
| WELDING_WIRE.DIAMETER | REAL |  | WireSolid |
| WELDING_WIRE.ISO_SPECNAME | VARCHAR |  | WireSolid |
| WELDING_WIRE.ISO_STANDARD | VARCHAR |  | WireSolid |
| WELDING_WIRE.WEIGHT | REAL |  | WireSolid |
| WELDMENT_FULL_PENETRATION | BOOLEAN |  | LaserMagnet |
| WELDMENT_GROOVE_PREPARATION | VARCHAR |  | LaserMagnet |
| WELD_BEAD_NUMBER | INTEGER |  | Weldment |
| WELD_JOINT_NUMBER | INTEGER |  | Weldment |
| WELD_LAYER_NUMBER | INTEGER |  | Weldment |
| WELD_SEAM_LENGTH | REAL |  | LaserMagnet |
| WELD_WELDMENT_NUMBER | INTEGER |  | Weldment |
| WIND_DIRECTION | CONTROLLEDVOCABULARY | WIND_DIRECTION | Outdoor |
| WIND_SPEED_IN_METER_PER_SECOND | REAL |  | Outdoor |
| WORKFLOW_MANAGER | VARCHAR |  | MatSimStructure, PyironJob |
| WORKPIECE_LENGTH | REAL |  | LaserMagnet |
| WORKPIECE_MATERIAL | VARCHAR |  | LaserMagnet |
| WORKPIECE_MATERIAL_TREATMENTS | VARCHAR |  | LaserMagnet |
| WORKPIECE_THICKNESS | REAL |  | LaserMagnet |
| WORKPIECE_WIDTH | REAL |  | LaserMagnet |
| WORKSHOP_ORDER_ID | VARCHAR |  | CreepTestMaterialHistoryAndCondition, CreepTestTestPiece |
| XRAY_WAVELENGTH | REAL |  | PowderXRDMeasurement |
