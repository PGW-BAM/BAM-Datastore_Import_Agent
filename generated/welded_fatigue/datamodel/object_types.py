"""ObjectType and ExperimentalStep definitions for the welded_fatigue PRD (FB7.2).

Only CREATE-classified entities are emitted here:
  - 1 ObjectType: WeldedFatigueSpecimen
  - 12 ExperimentalSteps (FB7.2 workflow §5.3.1 - §5.3.12)

REUSE entities (TestingMachine, Instrument, Calibration, MeasuringAmplifier,
Camera, LoadFrame, HydraulicCylinder, Servovalve, AlignmentFixture,
Thermocouple, ForceTransducer) and EXTEND entities (WELDING.WELD_TYPE)
are documented in README.md and used as-is from bam-masterdata.

CONTROLLEDVOCABULARY properties reference existing or CREATE vocabularies
by openBIS code (e.g. "WELDING.WELD_TYPE" for the EXTEND vocabulary).

Source: generated/welded_fatigue/gap-report.md and requirements.json.
PRD: BAM_PRD_Workflow_FB72.md (§5.2, §5.3).
"""

from bam_masterdata.metadata.entities import ObjectType, ExperimentalStep
from bam_masterdata.metadata.definitions import (
    ObjectTypeDef,
    PropertyTypeAssignment,
)


# ===========================================================================
# ObjectType (1)
# ===========================================================================


class WeldedFatigueSpecimen(ObjectType):
    defs = ObjectTypeDef(
        code="SPECIMEN.WELDED_FATIGUE",
        description="Welded fatigue specimen for S-N curve testing//Geschweisste Ermuedungsprobe fuer Woehlerlinien-Versuche",
        generated_code_prefix="SPEC.WELD",
    )

    original_id = PropertyTypeAssignment(
        code="ORIGINAL_ID",
        data_type="VARCHAR",
        property_label="Manufacturer ID//Herstellerbezeichnung",
        description="Manufacturer ID//Herstellerbezeichnung",
        mandatory=False,
        section="Material Details//Materialdetails",
    )

    sheet_origin = PropertyTypeAssignment(
        code="SHEET_ORIGIN",
        data_type="VARCHAR",
        property_label="Sheet origin//Herkunftsblech",
        description="Sheet origin (Bias-Vermeidung)//Herkunftsblech (Bias-Vermeidung)",
        mandatory=False,
        section="Material Details//Materialdetails",
    )

    weld_geometry = PropertyTypeAssignment(
        code="WELDING.WELD_TYPE",
        data_type="CONTROLLEDVOCABULARY",
        property_label="Weld geometry//Schweissnahtgeometrie",
        description="Weld geometry//Schweissnahtgeometrie",
        mandatory=True,
        section="Weld Details//Schweissnahtdetails",
    )

    iso_fat_class = PropertyTypeAssignment(
        code="ISO_5817_FAT_CLASS",
        data_type="CONTROLLEDVOCABULARY",
        property_label="FAT class (IIW)//FAT-Klasse (IIW)",
        description="FAT class (IIW)//FAT-Klasse (IIW)",
        mandatory=False,
        section="Weld Details//Schweissnahtdetails",
    )

    load_level = PropertyTypeAssignment(
        code="LOAD_LEVEL",
        data_type="CONTROLLEDVOCABULARY",
        property_label="Load level for S-N curve//Lastniveau fuer Woehlerlinie",
        description="Load level for S-N curve//Lastniveau fuer Woehlerlinie",
        mandatory=False,
        section="Test Planning//Versuchsplanung",
    )


# ===========================================================================
# ExperimentalSteps (12) — FB7.2 workflow §5.3.1 - §5.3.12
# ===========================================================================


class PreQualityCheckWeld(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.PRE_QUALITY_CHECK_WELD",
        description="Pre-test weld geometry quality check (angular distortion, edge misalignment, straightening)//Geometrische Vorqualitaetspruefung der Schweissnaht (Winkelverzug, Kantenversatz, Richten)",
        generated_code_prefix="EXP.PRE_QC",
    )

    initial_angular_distortion = PropertyTypeAssignment(
        code="INITIAL_ANGULAR_DISTORTION",
        data_type="REAL",
        property_label="Initial angular distortion [deg]//Anfangswinkelverzug [Grad]",
        description="Initial angular distortion [deg]//Anfangswinkelverzug [Grad]",
        mandatory=False,
        section="Geometry Checks//Geometriepruefung",
    )

    initial_edge_misalignment = PropertyTypeAssignment(
        code="INITIAL_EDGE_MISALIGNMENT",
        data_type="REAL",
        property_label="Initial edge misalignment [mm]//Anfangskantenversatz [mm]",
        description="Initial edge misalignment [mm]//Anfangskantenversatz [mm]",
        mandatory=False,
        section="Geometry Checks//Geometriepruefung",
    )

    was_straightened = PropertyTypeAssignment(
        code="WAS_STRAIGHTENED",
        data_type="BOOLEAN",
        property_label="Was straightened//Wurde gerichtet",
        description="Was straightened//Wurde gerichtet",
        mandatory=False,
        section="Geometry Checks//Geometriepruefung",
    )


class ChamferingGrinding(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.CHAMFERING_GRINDING",
        description="Chamfering / grinding processing step (post-weld machining)//Anfasen / Schleifen (Nachbearbeitung der Schweissnaht)",
        generated_code_prefix="EXP.CHAMFER",
    )

    weld_modifications = PropertyTypeAssignment(
        code="WELD_MODIFICATIONS",
        data_type="MULTILINE_VARCHAR",
        property_label="Weld reinforcement modifications//Schweissnahtverstaerkungen",
        description="Weld reinforcement modifications / grinding notes//Schweissnahtverstaerkungen / Schleifhinweise",
        mandatory=False,
        section="Processing Notes//Bearbeitungsnotizen",
    )


class SpecimenRecording(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.SPECIMEN_RECORDING",
        description="Specimen 3D-scan recording (GOM 3D-scanner workflow)//Aufnahme der Probe per 3D-Scan (GOM-Scanner-Workflow)",
        generated_code_prefix="EXP.SPEC_REC",
    )

    gom_scanner_ref = PropertyTypeAssignment(
        code="GOM_SCANNER_REF",
        data_type="OBJECT",
        property_label="GOM 3D-scanner instance//GOM 3D-Scanner Instanz",
        description="Link to the GOM 3D-scanner instance (REUSE Instrument)//Verknuepfung zur GOM 3D-Scanner Instanz (REUSE Instrument)",
        mandatory=False,
        section="Instrument Links//Geraeteverknuepfungen",
    )


class WeldAnalysis(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.WELD_ANALYSIS",
        description="Weld quality / FAT class analysis//Schweissnahtqualitaets- / FAT-Klassen-Analyse",
        generated_code_prefix="EXP.WELD_ANA",
    )

    iso_fat_class = PropertyTypeAssignment(
        code="ISO_5817_FAT_CLASS",
        data_type="CONTROLLEDVOCABULARY",
        property_label="Determined FAT class//Ermittelte FAT-Klasse",
        description="Determined FAT class (IIW)//Ermittelte FAT-Klasse (IIW)",
        mandatory=False,
        section="Weld Quality//Schweissnahtqualitaet",
    )


class SeriesAssignment(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.SERIES_ASSIGNMENT",
        description="Series assignment / randomization to test series collection//Zuordnung zur Versuchsreihe / Randomisierung",
        generated_code_prefix="EXP.SERIES",
    )


class TestSetupGeometry(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.TEST_SETUP_GEOMETRY",
        description="Pre-test specimen geometry measurement (avg thickness/width)//Geometrievermessung der Probe vor dem Versuch (mittlere Dicke/Breite)",
        generated_code_prefix="EXP.SETUP_GEO",
    )

    avg_thickness = PropertyTypeAssignment(
        code="AVG_THICKNESS",
        data_type="REAL",
        property_label="Average thickness [mm]//Durchschnittliche Dicke [mm]",
        description="Average thickness [mm]//Durchschnittliche Dicke [mm]",
        mandatory=False,
        section="Specimen Dimensions//Probenabmessungen",
    )

    avg_width = PropertyTypeAssignment(
        code="AVG_WIDTH",
        data_type="REAL",
        property_label="Average width [mm]//Durchschnittliche Breite [mm]",
        description="Average width [mm]//Durchschnittliche Breite [mm]",
        mandatory=False,
        section="Specimen Dimensions//Probenabmessungen",
    )


class MonitoringApplication(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.MONITORING_APPLICATION",
        description="DMS / strain-gauge application step (instrumentation placement)//DMS-Applikation (Instrumentierung)",
        generated_code_prefix="EXP.MON",
    )

    strain_gauge_type_ref = PropertyTypeAssignment(
        code="STRAIN_GAUGE_TYPE",
        data_type="CONTROLLEDVOCABULARY",
        property_label="Strain gauge type//DMS-Typ",
        description="Strain gauge type (DMS)//DMS-Typ",
        mandatory=False,
        section="Instrumentation//Instrumentierung",
    )

    consumable_type_ref = PropertyTypeAssignment(
        code="CONSUMABLE_TYPE",
        data_type="CONTROLLEDVOCABULARY",
        property_label="Consumable type//Verbrauchsmaterial-Typ",
        description="Consumable type//Verbrauchsmaterial-Typ",
        mandatory=False,
        section="Instrumentation//Instrumentierung",
    )

    measured_dms_distance_weld = PropertyTypeAssignment(
        code="MEASURED_DMS_DISTANCE_WELD",
        data_type="REAL",
        property_label="DMS distance to weld toe [mm]//DMS-Abstand zur Schweissnahtuebergang [mm]",
        description="DMS distance to weld toe [mm]//DMS-Abstand zum Schweissnahtuebergang [mm]",
        mandatory=False,
        section="Instrumentation//Instrumentierung",
    )

    measured_dms_distance_edge = PropertyTypeAssignment(
        code="MEASURED_DMS_DISTANCE_EDGE",
        data_type="REAL",
        property_label="DMS distance to specimen edge [mm]//DMS-Abstand zur Probenachse [mm]",
        description="DMS distance to specimen edge [mm]//DMS-Abstand zur Probenachse [mm]",
        mandatory=False,
        section="Instrumentation//Instrumentierung",
    )


class AmplifierSettings(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.AMPLIFIER_SETTINGS",
        description="Acquisition / amplifier settings (sampling, recording mode)//Verstaerker-Einstellungen (Abtastrate, Aufzeichnungsmodus)",
        generated_code_prefix="EXP.AMP",
    )

    sampling_frequency = PropertyTypeAssignment(
        code="SAMPLING_FREQUENCY",
        data_type="INTEGER",
        property_label="Sampling frequency [Hz]//Abtastfrequenz [Hz]",
        description="Sampling frequency [Hz]//Abtastfrequenz [Hz]",
        mandatory=False,
        section="Acquisition Settings//Aufzeichnungseinstellungen",
    )

    recording_mode = PropertyTypeAssignment(
        code="RECORDING_MODE",
        data_type="VARCHAR",
        property_label="Recording mode//Aufzeichnungsmodus",
        description="Recording mode (e.g. Peak-Valley)//Aufzeichnungsmodus (z.B. Peak-Valley)",
        mandatory=False,
        section="Acquisition Settings//Aufzeichnungseinstellungen",
    )

    testing_machine_ref = PropertyTypeAssignment(
        code="TESTING_MACHINE_REF",
        data_type="OBJECT",
        property_label="Testing machine//Pruefmaschine",
        description="Link to TestingMachine (REUSE)//Verknuepfung zur Pruefmaschine (REUSE)",
        mandatory=False,
        section="Instrument Links//Geraeteverknuepfungen",
    )

    measuring_amplifier_ref = PropertyTypeAssignment(
        code="MEASURING_AMPLIFIER_REF",
        data_type="OBJECT",
        property_label="Measuring amplifier//Messverstaerker",
        description="Link to MeasuringAmplifier (REUSE)//Verknuepfung zum Messverstaerker (REUSE)",
        mandatory=False,
        section="Instrument Links//Geraeteverknuepfungen",
    )


class InstallationStressMeasurement(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.INSTALLATION_STRESS_MEASUREMENT",
        description="Installation stress measurement (bending moment at 0.0 kN pre-test)//Einbauspannungsmessung (Biegemoment bei 0.0 kN vor Versuchsstart)",
        generated_code_prefix="EXP.INST_STRESS",
    )


class CyclicFatigueTest(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.CYCLIC_FATIGUE_TEST",
        description="S-N cyclic fatigue test (load program attached as file)//Zyklischer Ermuedungsversuch (S-N, Lastprogramm als Datei angehaengt)",
        generated_code_prefix="EXP.CYC_FAT",
    )

    marker_loads_active = PropertyTypeAssignment(
        code="MARKER_LOADS_ACTIVE",
        data_type="BOOLEAN",
        property_label="Marker loads active//Rastlinien aktiv",
        description="Marker loads active (fracture lines)//Rastlinien aktiv (Bruchlinien)",
        mandatory=False,
        section="Test Configuration//Versuchskonfiguration",
    )

    stop_reason = PropertyTypeAssignment(
        code="FATIGUE_STOP_REASON",
        data_type="CONTROLLEDVOCABULARY",
        property_label="Stop reason//Abbruchgrund",
        description="Stop reason//Abbruchgrund",
        mandatory=False,
        section="Test Outcome//Versuchsergebnis",
    )


class FatigueDataEvaluation(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.FATIGUE_DATA_EVALUATION",
        description="S-N fatigue data evaluation (gross/net cycle counts, DMS deviation)//Auswertung der Ermuedungsdaten (Brutto-/Nettoschwingspiele, DMS-Abweichung)",
        generated_code_prefix="EXP.FAT_EVAL",
    )

    cycles_gross_final = PropertyTypeAssignment(
        code="CYCLES_GROSS_FINAL",
        data_type="INTEGER",
        property_label="Final gross cycle count//Bruttoschwingspielzahl",
        description="Final gross cycle count//Bruttoschwingspielzahl",
        mandatory=False,
        section="Cycle Counts//Schwingspielzahlen",
    )

    cycles_net_final = PropertyTypeAssignment(
        code="CYCLES_NET_FINAL",
        data_type="INTEGER",
        property_label="Final net cycle count//Nettoschwingspielzahl",
        description="Final net cycle count//Nettoschwingspielzahl",
        mandatory=False,
        section="Cycle Counts//Schwingspielzahlen",
    )

    cycles_dms_deviation_10 = PropertyTypeAssignment(
        code="CYCLES_DMS_DEVIATION_10",
        data_type="MULTILINE_VARCHAR",
        property_label="Cycles to 10% DMS deviation per gauge//Zyklen bis 10% Abfall je DMS",
        description="Cycles to 10% DMS deviation per gauge//Zyklen bis 10% Abfall je DMS",
        mandatory=False,
        section="Cycle Counts//Schwingspielzahlen",
    )


class FractureSurfaceAnalysis(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.FRACTURE_SURFACE_ANALYSIS",
        description="Light-microscopic and macroscopic fracture surface analysis//Lichtmikroskopische und makroskopische Bruchflaechenanalyse",
        generated_code_prefix="EXP.FRAC_SURF",
    )

    camera_ref = PropertyTypeAssignment(
        code="CAMERA_REF",
        data_type="OBJECT",
        property_label="Camera//Kamera",
        description="Link to Camera (REUSE)//Verknuepfung zur Kamera (REUSE)",
        mandatory=False,
        section="Instrument Links//Geraeteverknuepfungen",
    )

    digital_microscope_ref = PropertyTypeAssignment(
        code="DIGITAL_MICROSCOPE_REF",
        data_type="OBJECT",
        property_label="Digital microscope//Digitalmikroskop",
        description="Link to digital microscope via Instrument (REUSE)//Verknuepfung zum Digitalmikroskop ueber Instrument (REUSE)",
        mandatory=False,
        section="Instrument Links//Geraeteverknuepfungen",
    )
