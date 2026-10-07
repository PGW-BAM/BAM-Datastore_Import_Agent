"""CREATE object types for the welded fatigue workflow (prd-stem: welded_fatigue_v2).

Generated 2026-10-06 by masterdata-extender from generated/welded_fatigue_v2/design.json
(gap report: generated/welded_fatigue_v2/gap-report.md, CREATE section).

Only own properties are declared; inherited properties come from the base class
(Sample / MechanicalTest). Reused property types (EXPERIMENTAL_STEP.WELDMENT_TYPE,
DEFECT_DESCRIPTION) are assigned with their existing code, data type and vocabulary.

PR target: bam_masterdata/datamodel/fatigue/object_types.py (new subpackage).
"""

from bam_masterdata.datamodel.activities import MechanicalTest
from bam_masterdata.datamodel.object_types import Sample
from bam_masterdata.metadata.definitions import ObjectTypeDef, PropertyTypeAssignment


class WeldedFatigueSpecimen(Sample):
    defs = ObjectTypeDef(
        code="SAMPLE.WELDED_FATIGUE_SPECIMEN",
        description="""Welded specimen for cyclic fatigue testing (butt or cruciform weld)//Geschweißte Probe für zyklische Ermüdungsversuche (Stumpf- oder Kreuzstoß)""",
        generated_code_prefix="SAM.WFS",
    )

    next_step = PropertyTypeAssignment(
        code="FATIGUE.NEXT_STEP",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="WELDED_FATIGUE_WORKFLOW_STEP",
        property_label="Next step",
        description="""Next workflow step to be carried out on this specimen//Nächster durchzuführender Ablaufschritt an dieser Probe""",
        mandatory=False,
        section="Workflow status",
    )

    manufacturer_designation = PropertyTypeAssignment(
        code="FATIGUE.MANUFACTURER_DESIGNATION",
        data_type="VARCHAR",
        property_label="Manufacturer designation (original ID)",
        description="""Original specimen identifier assigned by the manufacturer//Originale Probenkennung des Herstellers""",
        mandatory=False,
        section="Specimen identification",
    )

    source_sheet = PropertyTypeAssignment(
        code="FATIGUE.SOURCE_SHEET",
        data_type="VARCHAR",
        property_label="Source sheet",
        description="""Plate/sheet the specimen was cut from; used to avoid bias in the series randomisation//Blech, aus dem die Probe entnommen wurde; dient der Bias-Vermeidung bei der Randomisierung""",
        mandatory=False,
        section="Specimen identification",
    )

    # REUSE existing PropertyType: EXPERIMENTAL_STEP.WELDMENT_TYPE (Weldment, bam_masterdata/datamodel/welding/object_types.py:409)
    weld_type = PropertyTypeAssignment(
        code="EXPERIMENTAL_STEP.WELDMENT_TYPE",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="WELDING.WELD_TYPE",
        property_label="Type of weld",
        description="""Type of weldment made//Art der Schweißverbindung""",
        mandatory=False,
        section="Specimen identification",
    )

    target_quality_level = PropertyTypeAssignment(
        code="FATIGUE.TARGET_QUALITY_LEVEL",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="WELDING.ISO_5817_QUALITY_LEVEL",
        property_label="Target quality level (ISO 5817)",
        description="""Quality level according to ISO 5817 the specimen was manufactured for//Angestrebte Bewertungsgruppe nach ISO 5817, für die die Probe gefertigt wurde""",
        mandatory=False,
        section="Specimen identification",
    )

    initial_angular_distortion = PropertyTypeAssignment(
        code="FATIGUE.INITIAL_ANGULAR_DISTORTION",
        data_type="REAL",
        property_label="Initial angular distortion [°]",
        description="""Angular distortion measured at incoming inspection [°]//Winkelverzug bei der Eingangsprüfung [°]""",
        mandatory=False,
        section="01 Pre-quality check",
    )

    initial_edge_misalignment = PropertyTypeAssignment(
        code="FATIGUE.INITIAL_EDGE_MISALIGNMENT",
        data_type="REAL",
        property_label="Initial edge misalignment [mm]",
        description="""Edge misalignment measured at incoming inspection [mm]//Kantenversatz bei der Eingangsprüfung [mm]""",
        mandatory=False,
        section="01 Pre-quality check",
    )

    was_straightened = PropertyTypeAssignment(
        code="FATIGUE.WAS_STRAIGHTENED",
        data_type="BOOLEAN",
        property_label="Was straightened",
        description="""Specimen was straightened after the pre-quality check//Probe wurde nach der Vorqualitätsprüfung gerichtet""",
        mandatory=False,
        section="01 Pre-quality check",
    )

    angular_distortion_after_straightening = PropertyTypeAssignment(
        code="FATIGUE.ANGULAR_DISTORTION_AFTER_STRAIGHTENING",
        data_type="REAL",
        property_label="Angular distortion after straightening [°]",
        description="""Angular distortion after straightening [°]//Winkelverzug nach dem Richten [°]""",
        mandatory=False,
        section="01 Pre-quality check",
    )

    edge_misalignment_after_straightening = PropertyTypeAssignment(
        code="FATIGUE.EDGE_MISALIGNMENT_AFTER_STRAIGHTENING",
        data_type="REAL",
        property_label="Edge misalignment after straightening [mm]",
        description="""Edge misalignment after straightening [mm]//Kantenversatz nach dem Richten [mm]""",
        mandatory=False,
        section="01 Pre-quality check",
    )

    # REUSE existing PropertyType: DEFECT_DESCRIPTION (Named, bam_masterdata/datamodel/object_types.py:7429)
    defect_description = PropertyTypeAssignment(
        code="DEFECT_DESCRIPTION",
        data_type="MULTILINE_VARCHAR",
        property_label="Defect description",
        description="""Defect Description//Beschreibung der Defekte""",
        mandatory=False,
        section="01 Pre-quality check",
    )

    weld_post_treatment_notes = PropertyTypeAssignment(
        code="FATIGUE.WELD_POST_TREATMENT_NOTES",
        data_type="MULTILINE_VARCHAR",
        property_label="Weld reinforcement treatment / grinding notes",
        description="""Documentation of weld reinforcement treatment and grinding//Dokumentation der Nahtüberhöhungs-Bearbeitung und Schleifhinweise""",
        mandatory=False,
        section="02 Chamfering / grinding",
    )

    iso_5817_annex_c_rating = PropertyTypeAssignment(
        code="FATIGUE.ISO_5817_ANNEX_C_RATING",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="WELDING.ISO_5817_ANNEX_C_RATING",
        property_label="Quality level ISO 5817 Annex C",
        description="""Quality level determined by the GOM weld analysis according to ISO 5817 Annex C//Mit der GOM-Nahtanalyse ermittelte Bewertungsgruppe nach ISO 5817 Anhang C""",
        mandatory=False,
        section="04 Weld analysis",
    )

    load_level = PropertyTypeAssignment(
        code="FATIGUE.LOAD_LEVEL",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="FATIGUE.LOAD_LEVEL",
        property_label="Load level",
        description="""Load level the specimen is assigned to within the series//Lastniveau, dem die Probe in der Serie zugeordnet ist""",
        mandatory=False,
        section="05 Series assignment",
    )

    test_order = PropertyTypeAssignment(
        code="FATIGUE.TEST_ORDER",
        data_type="INTEGER",
        property_label="Test order",
        description="""Position of the specimen in the randomised test sequence//Position der Probe in der randomisierten Prüfreihenfolge""",
        mandatory=False,
        section="05 Series assignment",
    )

    thickness_pos_1 = PropertyTypeAssignment(
        code="FATIGUE.THICKNESS_POS_1",
        data_type="REAL",
        property_label="Thickness position 1 [mm]",
        description="""Thickness measured at position 1 before installation [mm]//Dicke an Position 1 vor Einbau [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )

    thickness_pos_2 = PropertyTypeAssignment(
        code="FATIGUE.THICKNESS_POS_2",
        data_type="REAL",
        property_label="Thickness position 2 [mm]",
        description="""Thickness measured at position 2 before installation [mm]//Dicke an Position 2 vor Einbau [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )

    thickness_pos_3 = PropertyTypeAssignment(
        code="FATIGUE.THICKNESS_POS_3",
        data_type="REAL",
        property_label="Thickness position 3 [mm]",
        description="""Thickness measured at position 3 before installation [mm]//Dicke an Position 3 vor Einbau [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )

    width_pos_1 = PropertyTypeAssignment(
        code="FATIGUE.WIDTH_POS_1",
        data_type="REAL",
        property_label="Width position 1 [mm]",
        description="""Width measured at position 1 before installation [mm]//Breite an Position 1 vor Einbau [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )

    width_pos_2 = PropertyTypeAssignment(
        code="FATIGUE.WIDTH_POS_2",
        data_type="REAL",
        property_label="Width position 2 [mm]",
        description="""Width measured at position 2 before installation [mm]//Breite an Position 2 vor Einbau [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )

    width_pos_3 = PropertyTypeAssignment(
        code="FATIGUE.WIDTH_POS_3",
        data_type="REAL",
        property_label="Width position 3 [mm]",
        description="""Width measured at position 3 before installation [mm]//Breite an Position 3 vor Einbau [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )

    mean_thickness = PropertyTypeAssignment(
        code="FATIGUE.MEAN_THICKNESS",
        data_type="REAL",
        property_label="Mean thickness [mm]",
        description="""Mean of the three thickness measurements [mm]//Mittelwert der drei Dickenmessungen [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )

    mean_width = PropertyTypeAssignment(
        code="FATIGUE.MEAN_WIDTH",
        data_type="REAL",
        property_label="Mean width [mm]",
        description="""Mean of the three width measurements [mm]//Mittelwert der drei Breitenmessungen [mm]""",
        mandatory=False,
        section="06 Geometry before installation",
    )


class CyclicFatigueTest(MechanicalTest):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST",
        description="""Cyclic fatigue test of a welded specimen incl. strain gauge application, measurement chain, installation and evaluation//Zyklischer Ermüdungsversuch an einer geschweißten Probe inkl. DMS-Applikation, Messkette, Einbau und Auswertung""",
        generated_code_prefix="EXP.MECH.CYC_FAT",
    )

    strain_gauge_distance_to_weld_toe = PropertyTypeAssignment(
        code="FATIGUE.STRAIN_GAUGE_DISTANCE_TO_WELD_TOE",
        data_type="REAL",
        property_label="Strain gauge distance to weld toe [mm]",
        description="""Distance between strain gauge and weld toe [mm]//Abstand des DMS zum Nahtübergang [mm]""",
        mandatory=False,
        section="07 Strain gauge application",
    )

    strain_gauge_distance_to_edge = PropertyTypeAssignment(
        code="FATIGUE.STRAIN_GAUGE_DISTANCE_TO_EDGE",
        data_type="REAL",
        property_label="Strain gauge distance to edge [mm]",
        description="""Distance between strain gauge and specimen edge [mm]//Abstand des DMS zum Probenrand [mm]""",
        mandatory=False,
        section="07 Strain gauge application",
    )

    strain_gauge_application_time = PropertyTypeAssignment(
        code="FATIGUE.STRAIN_GAUGE_APPLICATION_TIME",
        data_type="TIMESTAMP",
        property_label="Time of strain gauge application",
        description="""Date and time the strain gauges were applied//Zeitpunkt der DMS-Applikation""",
        mandatory=False,
        section="07 Strain gauge application",
    )

    sampling_frequency = PropertyTypeAssignment(
        code="FATIGUE.SAMPLING_FREQUENCY",
        data_type="INTEGER",
        property_label="Sampling frequency [Hz]",
        description="""Sampling frequency of the measuring amplifier [Hz]//Abtastfrequenz des Messverstärkers [Hz]""",
        mandatory=False,
        section="08 Measuring amplifier / test rig",
    )

    recording_mode = PropertyTypeAssignment(
        code="FATIGUE.RECORDING_MODE",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="FATIGUE.RECORDING_MODE",
        property_label="Recording mode",
        description="""Data recording mode of the measuring amplifier//Aufzeichnungsmodus des Messverstärkers""",
        mandatory=False,
        section="08 Measuring amplifier / test rig",
    )

    recorded_channels = PropertyTypeAssignment(
        code="FATIGUE.RECORDED_CHANNELS",
        data_type="VARCHAR",
        property_label="Recorded channels",
        description="""Channels recorded by the measuring amplifier//Vom Messverstärker erfasste Kanäle""",
        mandatory=False,
        section="08 Measuring amplifier / test rig",
    )

    preload_force = PropertyTypeAssignment(
        code="FATIGUE.PRELOAD_FORCE",
        data_type="REAL",
        property_label="Preload force [kN]",
        description="""Preload force during installation (bending moment at 0.0 kN) [kN]//Vorspannkraft beim Einbau (Biegemoment bei 0,0 kN) [kN]""",
        mandatory=False,
        section="09 Installation stress",
    )

    beach_marks_active = PropertyTypeAssignment(
        code="FATIGUE.BEACH_MARKS_ACTIVE",
        data_type="BOOLEAN",
        property_label="Beach marks (marker loads) active",
        description="""Marker loads for beach marks were applied during the test//Markerlasten für Rastlinien waren während des Versuchs aktiv""",
        mandatory=False,
        section="10 Cyclic fatigue test",
    )

    termination_reason = PropertyTypeAssignment(
        code="FATIGUE.TERMINATION_REASON",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="FATIGUE.TERMINATION_REASON",
        property_label="Termination reason",
        description="""Reason the cyclic fatigue test was terminated//Grund für den Abbruch des zyklischen Ermüdungsversuchs""",
        mandatory=False,
        section="10 Cyclic fatigue test",
    )

    cycles_gross = PropertyTypeAssignment(
        code="FATIGUE.CYCLES_GROSS",
        data_type="INTEGER",
        property_label="Gross number of cycles",
        description="""Gross number of load cycles including marker loads//Bruttoschwingspielzahl inklusive Markerlasten""",
        mandatory=False,
        section="11 Evaluation",
    )

    cycles_net = PropertyTypeAssignment(
        code="FATIGUE.CYCLES_NET",
        data_type="INTEGER",
        property_label="Net number of cycles",
        description="""Net number of load cycles//Nettoschwingspielzahl""",
        mandatory=False,
        section="11 Evaluation",
    )

    cycles_to_10_percent_strain_gauge_drop = PropertyTypeAssignment(
        code="FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP",
        data_type="MULTILINE_VARCHAR",
        property_label="Cycles to 10 % strain gauge drop per strain gauge",
        description="""Number of cycles until a 10 % signal drop, listed per strain gauge//Zyklen bis 10 % DMS-Abfall, je DMS aufgelistet""",
        mandatory=False,
        section="11 Evaluation",
    )
