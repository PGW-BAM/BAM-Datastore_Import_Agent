# Gap Report: welded_fatigue

Generated: 2026-06-02T00:00:00Z
PRD: BAM_PRD_Workflow_FB72.md
bam-masterdata CATALOG SHA: 39c0c77dd209b8b5951eb5e2275c78eab9fab400

---

## REUSE — use existing types as-is

| Entity | Type | Citation | Notes |
|---|---|---|---|
| TestingMachine | ObjectType | bam_masterdata/datamodel/object_types.py:1488 | Use for Prüfmaschinen (servo-hydraulic test frames). Exact class/code match in CATALOG. |
| Instrument | ObjectType | bam_masterdata/datamodel/object_types.py:1254 | Generic instrument base; reuse for cameras, microscopes, GOM 3D-scanner, IMC measuring amplifiers. Exact match in CATALOG. |
| Calibration | ObjectType | bam_masterdata/datamodel/object_types.py:1073 | Kalibrierungs-Datensätze. Exact class/code match in CATALOG. |
| MeasuringAmplifier | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:7627; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | IMC-Messverstärker. Fallback: subclass `Instrument` at object_types.py:1254. |
| Camera | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:7913; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | Kamera für Bruchflächenaufnahmen. Fallback: subclass `Instrument` at object_types.py:1254. |
| LoadFrame | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:7104; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | Rahmen der Prüfmaschine. |
| HydraulicCylinder | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:6963; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | Hydraulikzylinder. |
| Servovalve | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:7042; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | Servoventil. |
| AlignmentFixture | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:7167; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | Ausrichtvorrichtung. |
| Thermocouple | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:7193; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | Temperaturfühler. |
| ForceTransducer | ObjectType | UNCONFIRMED — verify against live bam-masterdata (requirements.json hints object_types.py:6048; not listed in CATALOG.md ObjectTypes table for SHA 39c0c77) | Kraftaufnehmer. |
| TESTING_MACHINE_LOAD_TYPE | VocabularyType | bam_masterdata/datamodel/vocabulary_types.py:31452 | Exact code match (class `TestingMachineLoadType`). |
| TESTING_MACHINE_DRIVE_TYPE | VocabularyType | bam_masterdata/datamodel/vocabulary_types.py:31409 | Exact code match (class `TestingMachineDriveType`). |
| LOAD_FRAME_ORIENTATION | VocabularyType | bam_masterdata/datamodel/vocabulary_types.py:28095 | Exact code match (class `LoadFrameOrientation`). |
| SPECIMEN_STATUS | VocabularyType | bam_masterdata/datamodel/vocabulary_types.py:31267 | Exact code match (class `SpecimenStatus`). |
| INSTRUMENT_STATUS | VocabularyType | bam_masterdata/datamodel/vocabulary_types.py:27985 | Exact code match (class `InstrumentStatus`). |

## EXTEND — existing types needing modification (PR to bam-masterdata)

| Entity | Type | Citation | Additions needed | PR action |
|---|---|---|---|---|
| WELDING.WELD_TYPE | VocabularyType | bam_masterdata/datamodel/welding/vocabularies.py:38 | Add `BUTT_WELD` (Butt weld // Stumpfstoß) and `CRUCIFORM_WELD` (Cruciform weld // Kreuzstoß). Current 6 terms (verified per CATALOG §"WeldType term details"): WELDING_FILLET_WELD (line 44), WELDING_GROOVE_WELD (line 50), WELDING_PLUG_WELD (line 56), WELDING_SPOT_WELD (line 62), WELDING_SURFACING_WELD (line 68), WELDING_TACK_WELD (line 74). | Open PR to `bam-masterdata` extending class `WeldType` at `welding/vocabularies.py:38` with two new `VocabularyTerm` entries for BUTT_WELD and CRUCIFORM_WELD. |

## CREATE — genuinely new (emit Python)

| Entity | Type | Why it can't be reused | PRD section |
|---|---|---|---|
| WeldedFatigueSpecimen | ObjectType | No specimen type for welded S-N fatigue exists. Closest peer `Fcg` (`SPECIMEN.FCG`) at `bam_masterdata/datamodel/object_types.py:6156` carries FCG-specific properties (notch geometry, crack-growth fields) incompatible with a welded structural specimen tested to S-N curve failure. Inherit directly from ObjectType. | §5.2 |
| ISO_5817_FAT_CLASS | VocabularyType | No fatigue (FAT) class vocabulary exists in CATALOG. Terms C56, B90, B125 (HCF-relevant IIW classes) are absent. | §5.1 |
| LOAD_LEVEL | VocabularyType | No load-level vocabulary exists in CATALOG. Terms HIGH, MEDIUM, LOW (abstract S-N curve levels) are absent. | §5.1 |
| FATIGUE_STOP_REASON | VocabularyType | No fatigue test-termination vocabulary exists in CATALOG. Terms FRACTURE, RUN_OUT, CRACK are absent. | §5.1 |
| STRAIN_GAUGE_TYPE | VocabularyType (CREATE_OPTIONAL) | No strain-gauge type vocabulary exists in CATALOG. Emit only if MonitoringApplication §5.3.7 retains the `strain_gauge_type_ref` OBJECT property. | §5.1 |
| CONSUMABLE_TYPE | VocabularyType (CREATE_OPTIONAL) | No generic consumable-type vocabulary exists in CATALOG. Emit only if MonitoringApplication §5.3.7 retains the `consumable_type_ref` OBJECT property. | §5.1 |
| PreQualityCheckWeld | ExperimentalStep | No weld pre-check step exists. Closest peers (`FcgTest`, `FcgStep`, `Weldment`) target crack-growth or weld production, not pre-test geometry checks (angular distortion, edge misalignment, straightening). | §5.3.1 |
| ChamferingGrinding | ExperimentalStep | No chamfering/grinding processing step exists in CATALOG. FcgStep variants target crack-growth and `Weldment` covers weld production, not post-weld machining/grinding for fatigue specimens. | §5.3.2 |
| SpecimenRecording | ExperimentalStep | No specimen 3D-scan recording step exists in CATALOG. Generic peers (`ImageSeries`, `ProfileScan`) do not bind GOM 3D-scanner workflow for welded fatigue specimens. | §5.3.3 |
| WeldAnalysis | ExperimentalStep | No weld-quality / FAT-class analysis step exists in CATALOG. References the new `ISO_5817_FAT_CLASS` vocabulary which is itself CREATE. | §5.3.4 |
| SeriesAssignment | ExperimentalStep | No series-assignment / randomization step exists in CATALOG. Documents temporal randomization and assignment to test series Collection. | §5.3.5 |
| TestSetupGeometry | ExperimentalStep | No specimen-geometry pre-test measurement step exists in CATALOG. Closest peer `ProfileScan` is a generic scan, not the avg_thickness/avg_width capture per FB7.2. | §5.3.6 |
| MonitoringApplication | ExperimentalStep | No DMS/strain-gauge application step exists in CATALOG. No closest peer for instrumentation placement (DMS distance to weld toe / specimen edge). | §5.3.7 |
| AmplifierSettings | ExperimentalStep | No amplifier-settings step exists in CATALOG. CATALOG only has `MeasuringAmplifierType` vocabulary (line 28268) — no acquisition-settings ExperimentalStep. | §5.3.8 |
| InstallationStressMeasurement | ExperimentalStep | No installation-stress capture step exists in CATALOG. Captures bending moment at 0.0 kN before test start — unique to FB7.2 welded fatigue. | §5.3.9 |
| CyclicFatigueTest | ExperimentalStep | No S-N cyclic fatigue test step exists in CATALOG. Closest peer `FcgTest` at `bam_masterdata/datamodel/object_types.py:5591` is FCG-specific (crack growth), not S-N to failure; closeness is not reuse. | §5.3.10 |
| FatigueDataEvaluation | ExperimentalStep | No S-N fatigue-data evaluation step exists in CATALOG. Closest peer `FcgEvaluation` at `bam_masterdata/datamodel/object_types.py:6137` is FCG-specific (da/dN, ΔK) — incompatible with gross/net cycle counts and DMS-deviation evaluation. | §5.3.11 |
| FractureSurfaceAnalysis | ExperimentalStep | No fracture-surface analysis step exists in CATALOG. Closest peer `MicroscopyFcgFractureSurfaceCracklength` at `bam_masterdata/datamodel/object_types.py:6101` measures FCG crack length, not generic light-microscopic / macroscopic fracture-surface evaluation. | §5.3.12 |

---

## Vocabulary reference check

CONTROLLEDVOCABULARY references in CREATE object types / experimental steps:

| Property location | Vocabulary referenced | Classification | Status |
|---|---|---|---|
| WeldedFatigueSpecimen.weld_geometry | WELDING.WELD_TYPE | EXTEND | OK — class exists, extension queued |
| WeldedFatigueSpecimen.iso_fat_class | ISO_5817_FAT_CLASS | CREATE | OK — emitted in this run |
| WeldedFatigueSpecimen.load_level | LOAD_LEVEL | CREATE | OK — emitted in this run |
| WeldAnalysis.iso_fat_class | ISO_5817_FAT_CLASS | CREATE | OK — emitted in this run |
| CyclicFatigueTest.stop_reason | FATIGUE_STOP_REASON | CREATE | OK — emitted in this run |
| MonitoringApplication.strain_gauge_type_ref (OBJECT) | STRAIN_GAUGE_TYPE | CREATE_OPTIONAL | OK — conditional; verify before emit |
| MonitoringApplication.consumable_type_ref (OBJECT) | CONSUMABLE_TYPE | CREATE_OPTIONAL | OK — conditional; verify before emit |

All vocabulary references resolve to either REUSE, EXTEND, or CREATE entries in this report — no dangling references.

---

## Summary

- REUSE: 16 entities (3 confirmed ObjectTypes + 8 UNCONFIRMED ObjectTypes + 5 VocabularyTypes)
- EXTEND: 1 entity (WELDING.WELD_TYPE)
- CREATE: 18 entities (1 ObjectType + 5 VocabularyTypes incl. 2 OPTIONAL + 12 ExperimentalSteps)
- Vocabulary references: all consistent ✓
- UNCONFIRMED citations: 8 (MeasuringAmplifier, Camera, LoadFrame, HydraulicCylinder, Servovalve, AlignmentFixture, Thermocouple, ForceTransducer — not listed in CATALOG.md ObjectTypes table at SHA 39c0c77; verify against live bam-masterdata)
- All 12 FB7.2 ExperimentalSteps appear as CREATE ✓
