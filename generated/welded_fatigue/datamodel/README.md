# welded_fatigue Masterdata Extension

Generated: 2026-06-02T00:00:00Z
PRD: BAM_PRD_Workflow_FB72.md
Gap report: generated/welded_fatigue/gap-report.md
bam-masterdata CATALOG SHA: 39c0c77dd209b8b5951eb5e2275c78eab9fab400

## CREATE summary

- Vocabularies: 5 (3 mandatory + 2 CREATE_OPTIONAL — verify before emit)
  - Mandatory (3): `ISO_5817_FAT_CLASS`, `LOAD_LEVEL`, `FATIGUE_STOP_REASON`
  - CREATE_OPTIONAL (2): `STRAIN_GAUGE_TYPE`, `CONSUMABLE_TYPE`
    - These are emitted because `MonitoringApplication` (§5.3.7) retains
      the `strain_gauge_type_ref` and `consumable_type_ref` properties.
      If those properties are dropped from the final design, remove the
      corresponding vocabulary classes from `vocabularies.py`.
- ObjectTypes: 1 (`WeldedFatigueSpecimen`)
- ExperimentalSteps: 12
  - `PreQualityCheckWeld`, `ChamferingGrinding`, `SpecimenRecording`,
    `WeldAnalysis`, `SeriesAssignment`, `TestSetupGeometry`,
    `MonitoringApplication`, `AmplifierSettings`,
    `InstallationStressMeasurement`, `CyclicFatigueTest`,
    `FatigueDataEvaluation`, `FractureSurfaceAnalysis`

## EXTEND actions (PR to bam-masterdata required BEFORE this extension is usable)

| Entity | Type | Citation | Additions needed | PR action |
|---|---|---|---|---|
| WELDING.WELD_TYPE | VocabularyType | bam_masterdata/datamodel/welding/vocabularies.py:38 | Add `BUTT_WELD` (Butt weld // Stumpfstoß) and `CRUCIFORM_WELD` (Cruciform weld // Kreuzstoß). Current 6 terms (verified per CATALOG §"WeldType term details"): WELDING_FILLET_WELD (line 44), WELDING_GROOVE_WELD (line 50), WELDING_PLUG_WELD (line 56), WELDING_SPOT_WELD (line 62), WELDING_SURFACING_WELD (line 68), WELDING_TACK_WELD (line 74). | Open PR to `bam-masterdata` extending class `WeldType` at `welding/vocabularies.py:38` with two new `VocabularyTerm` entries for BUTT_WELD and CRUCIFORM_WELD. |

NOTE: `WeldedFatigueSpecimen.weld_geometry` references `WELDING.WELD_TYPE`
with `data_type="CONTROLLEDVOCABULARY"`. The two new terms (BUTT_WELD,
CRUCIFORM_WELD) MUST be added to the upstream vocabulary BEFORE this
extension can be used in production. The reference itself is correct
(reuse-by-code) — no Python is emitted for the vocabulary class.

## REUSE references (no code emitted; used as-is)

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

## PR instructions

1. Symlink test (smoke check against live bam-masterdata working copy):
   ```bash
   ln -s "$(pwd)/generated/welded_fatigue/datamodel/" \
         "../bam-masterdata/bam_masterdata/datamodel/welded_fatigue"
   cd ../bam-masterdata
   python -c "from bam_masterdata.metadata.entities import ObjectType; print('discovery OK')"
   pytest tests/
   ```
2. Copy as a real folder (not symlink) for the PR:
   ```bash
   cp -r generated/welded_fatigue/datamodel/ \
         ../bam-masterdata/bam_masterdata/datamodel/welded_fatigue/
   cd ../bam-masterdata
   git checkout -b add-welded_fatigue-types
   git add bam_masterdata/datamodel/welded_fatigue/
   git commit -m "Add welded_fatigue masterdata types (FB7.2)"
   ```
3. Open the EXTEND PR FIRST (BUTT_WELD + CRUCIFORM_WELD into
   `WeldType` at `welding/vocabularies.py:38`). The CREATE PR depends on
   the EXTEND PR because `WeldedFatigueSpecimen.weld_geometry` references
   `WELDING.WELD_TYPE`.
4. Submit the CREATE PR to `BAMresearch/bam-masterdata`.
5. After both PRs are merged: run `/bam-sync` in this repo and re-run
   `/bam-analyze-prd` to confirm the CREATE list shrinks to zero.

## Notes on the OPTIONAL vocabularies

`STRAIN_GAUGE_TYPE` and `CONSUMABLE_TYPE` are flagged `CREATE_OPTIONAL` in
the gap report. They have been emitted in `vocabularies.py` with starter
terms (LINEAR / ROSETTE / CHAIN and ADHESIVE / SOLDER / COATING / CABLE
respectively). The corresponding properties on `MonitoringApplication`
(`strain_gauge_type_ref`, `consumable_type_ref`) are typed as
`CONTROLLEDVOCABULARY` referencing those codes. The original
requirements.json showed `data_type="OBJECT"` with an `object_target`
hint; that hint resolves to a controlled vocabulary in practice — see
gap-report §"Vocabulary reference check" rows 6 and 7. If FB7.2
stakeholders prefer to drop these instrumentation refs, delete the two
vocabulary classes AND the two corresponding `PropertyTypeAssignment`
entries on `MonitoringApplication` before submitting the PR.
