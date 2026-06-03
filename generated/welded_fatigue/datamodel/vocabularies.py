"""Vocabulary definitions for the welded_fatigue PRD (FB7.2).

Only CREATE-classified vocabularies are emitted here.
REUSE/EXTEND vocabularies (e.g. WELDING.WELD_TYPE, TESTING_MACHINE_LOAD_TYPE,
TESTING_MACHINE_DRIVE_TYPE, LOAD_FRAME_ORIENTATION, SPECIMEN_STATUS,
INSTRUMENT_STATUS) are documented in README.md and used as-is from
bam-masterdata.

Source: generated/welded_fatigue/gap-report.md (CREATE section)
PRD: BAM_PRD_Workflow_FB72.md (§5.1)
"""

from bam_masterdata.metadata.entities import VocabularyType
from bam_masterdata.metadata.definitions import (
    VocabularyTypeDef,
    VocabularyTypeAssignment,
)


class Iso5817FatClass(VocabularyType):
    defs = VocabularyTypeDef(
        code="ISO_5817_FAT_CLASS",
        description="IIW FAT class for high-cycle fatigue per ISO 5817//IIW FAT-Klasse fuer Hochzyklus-Ermuedung nach ISO 5817",
    )

    c56 = VocabularyTypeAssignment(
        code="C56",
        description="FAT Class C56//FAT Klasse C56",
    )

    b90 = VocabularyTypeAssignment(
        code="B90",
        description="FAT Class B90//FAT Klasse B90",
    )

    b125 = VocabularyTypeAssignment(
        code="B125",
        description="FAT Class B125//FAT Klasse B125",
    )


class LoadLevel(VocabularyType):
    defs = VocabularyTypeDef(
        code="LOAD_LEVEL",
        description="Abstract load level for the S-N curve//Abstraktes Lastniveau fuer die Woehlerlinie",
    )

    high = VocabularyTypeAssignment(
        code="HIGH",
        description="High Load//Hohes Lastniveau",
    )

    medium = VocabularyTypeAssignment(
        code="MEDIUM",
        description="Medium Load//Mittleres Lastniveau",
    )

    low = VocabularyTypeAssignment(
        code="LOW",
        description="Low Load//Niedriges Lastniveau",
    )


class FatigueStopReason(VocabularyType):
    defs = VocabularyTypeDef(
        code="FATIGUE_STOP_REASON",
        description="Reason for fatigue test termination//Grund fuer den Abbruch des Ermuedungsversuchs",
    )

    fracture = VocabularyTypeAssignment(
        code="FRACTURE",
        description="Total Fracture//Totalbruch",
    )

    run_out = VocabularyTypeAssignment(
        code="RUN_OUT",
        description="Target Cycles Reached (Run Out)//Zyklenzahl erreicht (Durchlaeufer)",
    )

    crack = VocabularyTypeAssignment(
        code="CRACK",
        description="Crack Detected//Riss detektiert",
    )


# --- CREATE_OPTIONAL vocabularies ---------------------------------------
# The two vocabularies below are flagged CREATE_OPTIONAL in the gap report.
# They are emitted because MonitoringApplication (§5.3.7) retains the
# strain_gauge_type_ref and consumable_type_ref properties. See README.md
# for the conditional emit rule.

class StrainGaugeType(VocabularyType):
    defs = VocabularyTypeDef(
        code="STRAIN_GAUGE_TYPE",
        description="Type of strain gauge (DMS) used for monitoring//Typ des verwendeten Dehnungsmessstreifens (DMS)",
    )

    linear = VocabularyTypeAssignment(
        code="LINEAR",
        description="Linear strain gauge (uniaxial)//Linearer DMS (einachsig)",
    )

    rosette = VocabularyTypeAssignment(
        code="ROSETTE",
        description="Strain gauge rosette//DMS-Rosette",
    )

    chain = VocabularyTypeAssignment(
        code="CHAIN",
        description="Strain gauge chain (linear array)//DMS-Kette",
    )


class ConsumableType(VocabularyType):
    defs = VocabularyTypeDef(
        code="CONSUMABLE_TYPE",
        description="Type of consumable used for instrumentation application//Typ des bei der Instrumentierung verwendeten Verbrauchsmaterials",
    )

    adhesive = VocabularyTypeAssignment(
        code="ADHESIVE",
        description="Adhesive (e.g. cyanoacrylate)//Klebstoff (z.B. Cyanacrylat)",
    )

    solder = VocabularyTypeAssignment(
        code="SOLDER",
        description="Solder for cable connection//Loetzinn fuer Kabelanschluss",
    )

    coating = VocabularyTypeAssignment(
        code="COATING",
        description="Protective coating//Schutzbeschichtung",
    )

    cable = VocabularyTypeAssignment(
        code="CABLE",
        description="Cable/wire//Kabel/Draht",
    )
