"""CREATE vocabularies for the welded fatigue workflow (prd-stem: welded_fatigue_v2).

Generated 2026-10-06 by masterdata-extender from generated/welded_fatigue_v2/design.json
(gap report: generated/welded_fatigue_v2/gap-report.md, CREATE section).

Only CREATE vocabularies are defined here. The EXTEND vocabularies WELDING.WELD_TYPE and
AUXILIARY_MATERIAL_TYPE are NOT redefined (see extend.json / README.md for the term additions).

Target files in bam-masterdata for the PR:
    WELDING.ISO_5817_QUALITY_LEVEL   -> bam_masterdata/datamodel/welding/vocabularies.py
    WELDING.ISO_5817_ANNEX_C_RATING  -> bam_masterdata/datamodel/welding/vocabularies.py
    WELDED_FATIGUE_WORKFLOW_STEP     -> bam_masterdata/datamodel/fatigue/vocabularies.py (new subpackage)
    FATIGUE.LOAD_LEVEL               -> bam_masterdata/datamodel/fatigue/vocabularies.py (new subpackage)
    FATIGUE.RECORDING_MODE           -> bam_masterdata/datamodel/fatigue/vocabularies.py (new subpackage)
    FATIGUE.TERMINATION_REASON       -> bam_masterdata/datamodel/fatigue/vocabularies.py (new subpackage)
"""

from bam_masterdata.metadata.definitions import VocabularyTerm, VocabularyTypeDef
from bam_masterdata.metadata.entities import VocabularyType


# --- PR target: bam_masterdata/datamodel/fatigue/vocabularies.py ---
class WeldedFatigueWorkflowStep(VocabularyType):
    defs = VocabularyTypeDef(
        code="WELDED_FATIGUE_WORKFLOW_STEP",
        description="""Ordered workflow steps of the welded fatigue test programme//Geordnete Ablaufschritte des Schweißnaht-Ermüdungsprogramms""",
    )

    s01_pre_quality_check = VocabularyTerm(
        code="S01_PRE_QUALITY_CHECK",
        label="01 Pre-quality check",
        label_de="01 Vorqualitätsprüfung",
        description="""Pre-quality check of the weld//Vorqualitätsprüfung der Schweißnaht""",
    )

    s02_chamfering_grinding = VocabularyTerm(
        code="S02_CHAMFERING_GRINDING",
        label="02 Chamfering / grinding",
        label_de="02 Anfasen / Schleifen",
        description="""Chamfering / grinding//Anfasen / Schleifen""",
    )

    s03_3d_scan = VocabularyTerm(
        code="S03_3D_SCAN",
        label="03 3D scan",
        label_de="03 3D-Scan",
        description="""3D scan of the specimen//3D-Scan der Probe""",
    )

    s04_weld_analysis = VocabularyTerm(
        code="S04_WELD_ANALYSIS",
        label="04 Weld analysis",
        label_de="04 Nahtanalyse",
        description="""Weld analysis (GOM)//Nahtanalyse (GOM)""",
    )

    s05_series_assignment = VocabularyTerm(
        code="S05_SERIES_ASSIGNMENT",
        label="05 Series assignment",
        label_de="05 Serienzuordnung",
        description="""Series assignment (randomisation)//Serienzuordnung (Randomisierung)""",
    )

    s06_geometry_before_installation = VocabularyTerm(
        code="S06_GEOMETRY_BEFORE_INSTALLATION",
        label="06 Geometry before installation",
        label_de="06 Geometrie vor Einbau",
        description="""Geometry before installation//Geometrie vor Einbau""",
    )

    s07_strain_gauge_application = VocabularyTerm(
        code="S07_STRAIN_GAUGE_APPLICATION",
        label="07 Strain gauge application",
        label_de="07 DMS-Applikation",
        description="""Strain gauge application//DMS-Applikation""",
    )

    s08_measuring_amplifier_test_rig = VocabularyTerm(
        code="S08_MEASURING_AMPLIFIER_TEST_RIG",
        label="08 Measuring amplifier / test rig",
        label_de="08 Messverstärker / Prüfstand",
        description="""Measuring amplifier / test rig//Messverstärker / Prüfstand""",
    )

    s09_installation_stress = VocabularyTerm(
        code="S09_INSTALLATION_STRESS",
        label="09 Installation stress",
        label_de="09 Einbaubeanspruchung",
        description="""Installation stress//Einbaubeanspruchung""",
    )

    s10_cyclic_fatigue_test = VocabularyTerm(
        code="S10_CYCLIC_FATIGUE_TEST",
        label="10 Cyclic fatigue test",
        label_de="10 Zyklischer Ermüdungsversuch",
        description="""Cyclic fatigue test//Zyklischer Ermüdungsversuch""",
    )

    s11_evaluation = VocabularyTerm(
        code="S11_EVALUATION",
        label="11 Evaluation",
        label_de="11 Auswertung",
        description="""Evaluation//Auswertung""",
    )

    s12_fracture_surface_analysis = VocabularyTerm(
        code="S12_FRACTURE_SURFACE_ANALYSIS",
        label="12 Fracture surface analysis",
        label_de="12 Bruchflächenanalyse",
        description="""Fracture surface analysis//Bruchflächenanalyse""",
    )

    done = VocabularyTerm(
        code="DONE",
        label="Done",
        label_de="Abgeschlossen",
        description="""All workflow steps completed//Alle Ablaufschritte abgeschlossen""",
    )


# --- PR target: bam_masterdata/datamodel/welding/vocabularies.py ---
class Iso5817QualityLevel(VocabularyType):
    defs = VocabularyTypeDef(
        code="WELDING.ISO_5817_QUALITY_LEVEL",
        description="""Quality levels for imperfections according to ISO 5817//Bewertungsgruppen für Unregelmäßigkeiten nach ISO 5817""",
    )

    b = VocabularyTerm(
        code="B",
        label="B",
        description="""Quality level B (stringent)//Bewertungsgruppe B (hoch)""",
    )

    c = VocabularyTerm(
        code="C",
        label="C",
        description="""Quality level C (intermediate)//Bewertungsgruppe C (mittel)""",
    )

    d = VocabularyTerm(
        code="D",
        label="D",
        description="""Quality level D (moderate)//Bewertungsgruppe D (niedrig)""",
    )


# --- PR target: bam_masterdata/datamodel/welding/vocabularies.py ---
class Iso5817AnnexCRating(VocabularyType):
    defs = VocabularyTypeDef(
        code="WELDING.ISO_5817_ANNEX_C_RATING",
        description="""Quality levels for fatigue-loaded structures according to ISO 5817 Annex C//Bewertungsgruppen für schwingend beanspruchte Konstruktionen nach ISO 5817 Anhang C""",
    )

    c63 = VocabularyTerm(
        code="C63",
        label="C63",
        description="""Quality level C63 according to ISO 5817 Annex C//Bewertungsgruppe C63 nach ISO 5817 Anhang C""",
    )

    b90 = VocabularyTerm(
        code="B90",
        label="B90",
        description="""Quality level B90 according to ISO 5817 Annex C//Bewertungsgruppe B90 nach ISO 5817 Anhang C""",
    )

    b125 = VocabularyTerm(
        code="B125",
        label="B125",
        description="""Quality level B125 according to ISO 5817 Annex C//Bewertungsgruppe B125 nach ISO 5817 Anhang C""",
    )


# --- PR target: bam_masterdata/datamodel/fatigue/vocabularies.py ---
class FatigueLoadLevel(VocabularyType):
    defs = VocabularyTypeDef(
        code="FATIGUE.LOAD_LEVEL",
        description="""Load level of a specimen within a fatigue test series//Lastniveau einer Probe innerhalb einer Ermüdungsprüfserie""",
    )

    high = VocabularyTerm(
        code="HIGH",
        label="High",
        label_de="Hoch",
        description="""High load level//Hohes Lastniveau""",
    )

    medium = VocabularyTerm(
        code="MEDIUM",
        label="Medium",
        label_de="Mittel",
        description="""Medium load level//Mittleres Lastniveau""",
    )

    low = VocabularyTerm(
        code="LOW",
        label="Low",
        label_de="Niedrig",
        description="""Low load level//Niedriges Lastniveau""",
    )


# --- PR target: bam_masterdata/datamodel/fatigue/vocabularies.py ---
class FatigueRecordingMode(VocabularyType):
    defs = VocabularyTypeDef(
        code="FATIGUE.RECORDING_MODE",
        description="""Data recording mode of the measuring amplifier in fatigue tests//Aufzeichnungsmodus des Messverstärkers in Ermüdungsversuchen""",
    )

    full_signal = VocabularyTerm(
        code="FULL_SIGNAL",
        label="Full signal",
        label_de="Vollsignal",
        description="""Full signal recorded//Vollsignal aufgezeichnet""",
    )

    peak_counter = VocabularyTerm(
        code="PEAK_COUNTER",
        label="Peak counter",
        label_de="Peak-Counter",
        description="""Peak counter//Peak-Counter""",
    )

    peak_valley = VocabularyTerm(
        code="PEAK_VALLEY",
        label="Peak-valley",
        label_de="Peak-Valley",
        description="""Peak and valley values recorded//Peak-Valley-Werte aufgezeichnet""",
    )


# --- PR target: bam_masterdata/datamodel/fatigue/vocabularies.py ---
class FatigueTerminationReason(VocabularyType):
    defs = VocabularyTypeDef(
        code="FATIGUE.TERMINATION_REASON",
        description="""Reason for terminating a fatigue test//Grund für den Abbruch eines Ermüdungsversuchs""",
    )

    total_fracture = VocabularyTerm(
        code="TOTAL_FRACTURE",
        label="Total fracture",
        label_de="Totalbruch",
        description="""Total fracture of the specimen//Totalbruch der Probe""",
    )

    crack_detected = VocabularyTerm(
        code="CRACK_DETECTED",
        label="Crack detected",
        label_de="Riss detektiert",
        description="""Crack detected//Riss detektiert""",
    )

    run_out = VocabularyTerm(
        code="RUN_OUT",
        label="Run-out",
        label_de="Durchläufer",
        description="""Run-out, cycle limit reached//Durchläufer, Zyklenzahl erreicht""",
    )

    manual_stop = VocabularyTerm(
        code="MANUAL_STOP",
        label="Manual stop",
        label_de="Manueller Stopp",
        description="""Test stopped manually//Versuch manuell gestoppt""",
    )
