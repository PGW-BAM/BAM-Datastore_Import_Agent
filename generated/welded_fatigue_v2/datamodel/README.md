# welded_fatigue_v2 Masterdata Extension

Generated: 2026-10-06 (masterdata-extender)
PRD: BAM_PRD_Workflow_FB72_v2.md
Design: generated/welded_fatigue_v2/design.json
Gap report: generated/welded_fatigue_v2/gap-report.md
bam-masterdata CATALOG SHA: d7a871be8c6aa934af2bf77357d30d8a5d689d92

## CREATE summary

- Vocabularies: 6 (`vocabularies.py`)
  - `WELDED_FATIGUE_WORKFLOW_STEP` (13 terms), `FATIGUE.LOAD_LEVEL` (3), `FATIGUE.RECORDING_MODE` (3), `FATIGUE.TERMINATION_REASON` (4)
  - `WELDING.ISO_5817_QUALITY_LEVEL` (3), `WELDING.ISO_5817_ANNEX_C_RATING` (3)
- ObjectTypes: 2 (`object_types.py`)
  - `SAMPLE.WELDED_FATIGUE_SPECIMEN` (`WeldedFatigueSpecimen(Sample)`, prefix `SAM.WFS`) - 23 own assignments (21 new + 2 reused property types)
  - `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` (`CyclicFatigueTest(MechanicalTest)`, prefix `EXP.MECH.CYC_FAT`) - 12 own assignments (12 new)
- ExperimentalSteps: 0 (the steps 03-04 and 12 use `EXPERIMENTAL_STEP` as-is, REUSE)
- New property types: 33 `FATIGUE.*` codes (21 specimen + 12 test), plus 2 existing property types assigned
  (`EXPERIMENTAL_STEP.WELDMENT_TYPE`, `DEFECT_DESCRIPTION`) - consistent with the gap report.

Only own properties are declared; inherited ones (`$NAME`, `ALIAS`, `NOTES`, `OPERATOR`, `START_DATE`, ...) come from the
base classes. Codes, sections, labels, descriptions, order, mandatory flags and prefixes are taken 1:1 from design.json.

Display order caveat: bam-masterdata collects inherited properties BEFORE own ones (`instance.properties`, MRO order), so
`spec.json` lists e.g. the specimen as General Information, Properties, BAM Information, Additional Information, Comments,
then "Workflow Status", "Specimen Identification", 01..06. design.json `section_order` wants "Workflow Status" first (and
for the test type the inherited "Experimental Details"/"References"/... after section 11). This cannot be expressed in the
declarative classes without redeclaring inherited properties; the apply step should order assignments by
design.json `section_order` if that layout is required. Sample also contributes one inherited assignment with an empty
section (`$ANNOTATIONS_STATE`, ELN-internal).

Property counts after inheritance (import test): `SAMPLE.WELDED_FATIGUE_SPECIMEN` 42 (19 inherited + 23 own),
`…CYCLIC_FATIGUE_TEST` 26 (14 inherited + 12 own).

## Target files in bam-masterdata

| Generated class | Code | Target file in the PR |
|---|---|---|
| `Iso5817QualityLevel` | `WELDING.ISO_5817_QUALITY_LEVEL` | `bam_masterdata/datamodel/welding/vocabularies.py` (append) |
| `Iso5817AnnexCRating` | `WELDING.ISO_5817_ANNEX_C_RATING` | `bam_masterdata/datamodel/welding/vocabularies.py` (append) |
| `WeldedFatigueWorkflowStep` | `WELDED_FATIGUE_WORKFLOW_STEP` | `bam_masterdata/datamodel/fatigue/vocabularies.py` (new subpackage) |
| `FatigueLoadLevel` | `FATIGUE.LOAD_LEVEL` | `bam_masterdata/datamodel/fatigue/vocabularies.py` |
| `FatigueRecordingMode` | `FATIGUE.RECORDING_MODE` | `bam_masterdata/datamodel/fatigue/vocabularies.py` |
| `FatigueTerminationReason` | `FATIGUE.TERMINATION_REASON` | `bam_masterdata/datamodel/fatigue/vocabularies.py` |
| `WeldedFatigueSpecimen` | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | `bam_masterdata/datamodel/fatigue/object_types.py` (new subpackage) |
| `CyclicFatigueTest` | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | `bam_masterdata/datamodel/fatigue/object_types.py` |

## EXTEND actions (PR to bam-masterdata required BEFORE this extension is usable)

No Python classes are emitted for these (HARD REFUSAL: REUSE/EXTEND). Machine-readable: `extend.json` (this folder).

| Entity | Kind | Citation | Additions | On instance | PR action |
|---|---|---|---|---|---|
| `WELDING.WELD_TYPE` | Vocabulary (6 terms: FILLET, GROOVE, PLUG, SPOT, SURFACING, TACK) | bam_masterdata/datamodel/welding/vocabularies.py:38 (last term :74) | `WELDING_BUTT_WELD` "butt weld", `WELDING_CRUCIFORM_WELD` "cruciform weld" (prefix convention of existing terms; resolution Q2) | present, 6 terms identical (inventory §1) → 2 terms missing after PR | PR to bam-masterdata `welding/vocabularies.py` (welding group owns the list; also affects `EXPERIMENTAL_STEP.WELDMENT`) |
| `AUXILIARY_MATERIAL_TYPE` | Vocabulary (10 terms) | bam_masterdata/datamodel/vocabulary_types.py:252 (last term :312) | `STRAIN_GAUGE` "Strain gauge", `CRACK_DETECTION_AGENT` "Crack detection agent" (`ADHESIVE` exists, :264) | present, same 10 terms (coord. live check) → 2 terms missing after PR | PR to bam-masterdata `vocabulary_types.py` |

### Ready-to-paste term snippets

Append to `class WeldType(VocabularyType)` in `bam_masterdata/datamodel/welding/vocabularies.py`
(after `welding_tack_weld`):

```python
    welding_butt_weld = VocabularyTerm(
        code="WELDING_BUTT_WELD",
        label="butt weld",
        description="""Butt weld//Stumpfstoß""",
    )

    welding_cruciform_weld = VocabularyTerm(
        code="WELDING_CRUCIFORM_WELD",
        label="cruciform weld",
        description="""Cruciform weld//Kreuzstoß""",
    )
```

Append to `class AuxiliaryMaterialType(VocabularyType)` in `bam_masterdata/datamodel/vocabulary_types.py`
(after its last term):

```python
    strain_gauge = VocabularyTerm(
        code="STRAIN_GAUGE",
        label="Strain gauge",
        description="""Strain gauge//Dehnungsmessstreifen""",
    )

    crack_detection_agent = VocabularyTerm(
        code="CRACK_DETECTION_AGENT",
        label="Crack detection agent",
        description="""Crack detection agent (e.g. crack luminescence)//Rissprüfmittel (z. B. Risslumineszenz)""",
    )
```

PR note (gap report, design remark 4): butt/cruciform are joint geometries rather than weld types like fillet/groove; the
`WELDING.WELD_TYPE` change needs review by the welding group (the list is also used by `EXPERIMENTAL_STEP.WELDMENT`).

## REUSE references (no code emitted; these are used as-is)

### Types

| Entity | Kind | Citation (file:line) | On instance | Role in design |
|---|---|---|---|---|
| `SAMPLE` (Sample) | ObjectType | bam_masterdata/datamodel/object_types.py:3005 | outdated (8 of 19 props) | Base class of `SAMPLE.WELDED_FATIGUE_SPECIMEN`; inherited `$NAME` = series designation, `ALIAS` = internal designation |
| `EXPERIMENTAL_STEP` (ExperimentalStep) | ObjectType | bam_masterdata/datamodel/object_types.py:235 | outdated (no `OPERATOR`) | Used directly for `<specimen>-SCAN` (steps 03-04) and `<specimen>-FRACTURE` (step 12) |
| `EXPERIMENTAL_STEP.MECHANICAL_TEST` (MechanicalTest) | ObjectType | bam_masterdata/datamodel/activities.py:2196 | missing on instance | Base class of `…CYCLIC_FATIGUE_TEST` (0 own props, 14 inherited) |
| `INSTRUMENT` (Instrument) | ObjectType | bam_masterdata/datamodel/object_types.py:1370 | present (BAM_* props impossible on dev1 → outdated) | ZEISS GOM ATOS 5, digital microscope |
| `INSTRUMENT.CAMERA` (Camera) | ObjectType | bam_masterdata/datamodel/instruments.py:1221 | present | Luxonis OAK-4D-Pro, macro camera |
| `INSTRUMENT.MEASURING_AMPLIFIER` (MeasuringAmplifier) | ObjectType | bam_masterdata/datamodel/instruments.py:631 | present | IMC measuring amplifier |
| `TESTING_MACHINE` (TestingMachine) | ObjectType | bam_masterdata/datamodel/object_types.py:1604 | present (BAM_* props impossible on dev1 → outdated) | Servo-hydraulic testing machine |
| `AUXILIARY_MATERIAL` (AuxiliaryMaterial) | ObjectType | bam_masterdata/datamodel/object_types.py:1175 | present | Strain gauge, adhesive, crack luminescence set |
| `SOP` (Sop) | ObjectType | bam_masterdata/datamodel/object_types.py:2868 | outdated (4 of 14 props) | Project object `WORKFLOW_PLAN` (uses only `$NAME`, `DESCRIPTION` → sufficient on dev1) |
| `COLLECTION` (Collection) | CollectionType | bam_masterdata/datamodel/collection_types.py:8 | present | One collection per series, `$DEFAULT_OBJECT_TYPE` (collection_types.py:24) = `SAMPLE.WELDED_FATIGUE_SPECIMEN` |

### Vocabularies

| Entity | Kind | Citation (file:line) | On instance | Role in design |
|---|---|---|---|---|
| `TESTING_MACHINE_DRIVE_TYPE` | Vocabulary | bam_masterdata/datamodel/vocabulary_types.py:31329 (term `SERVOHYDRAULIC` :31359) | UNCONFIRMED (not in inventory) | Drive type of the servo-hydraulic machine |
| `PHYSICAL_STATE` | Vocabulary (inherited via Sample) | bam_masterdata/datamodel/vocabulary_types.py:28904 | present (coord. live check 2026-10-06) | Inherited Sample property; not used by the workflow |

### Property types (assigned to new types)

| Entity | Kind | Citation (file:line) | On instance | Role in design |
|---|---|---|---|---|
| `EXPERIMENTAL_STEP.WELDMENT_TYPE` (CONTROLLEDVOCABULARY → `WELDING.WELD_TYPE`) | PropertyType | bam_masterdata/datamodel/welding/object_types.py:409 (Weldment) | missing on instance (coord. live check: live Weldment has only generic step props) | Specimen "Weld geometry" (section Specimen Identification) + series table column |
| `DEFECT_DESCRIPTION` (MULTILINE_VARCHAR) | PropertyType | bam_masterdata/datamodel/object_types.py:7429 (Named, `SAMPLE_NDT.NAMED`) | UNCONFIRMED | Specimen step 01 "Gross weld defects" |

### Dataset types

| Entity | Kind | Citation (file:line) | On instance | Role in design |
|---|---|---|---|---|
| `RAW_DATA` | DatasetType | bam_masterdata/datamodel/dataset_types.py:42 | presumed present (inventory §2 mapping target; not itemised) | Photos, 3D scan, IMC raw, monitoring images, macro/microscope images (9 files) |
| `PROCESSED_DATA` | DatasetType | bam_masterdata/datamodel/dataset_types.py:79 | presumed present | Cleaned measurement data (11) |
| `ANALYZED_DATA` | DatasetType | bam_masterdata/datamodel/dataset_types.py:116 | presumed present | GOM evaluation export (04), beach-mark evaluation (12) |
| `ATTACHMENT` | DatasetType | bam_masterdata/datamodel/dataset_types.py:153 | presumed present | Post-processing report (02), strain gauge position drawing (07) |
| `SOURCE_CODE` | DatasetType | bam_masterdata/datamodel/dataset_types.py:227 | presumed present | Randomisation script (05, collection), conversion script (11) |
| `MEASUREMENT_PROTOCOL_FILE` | DatasetType | bam_masterdata/datamodel/dataset_types.py:541 | presumed present | Load programme (10) |
| `FIGURE.PLOT` | DatasetType | bam_masterdata/datamodel/dataset_types.py:1274 | presumed present | Evaluation plots (11) |

## PR instructions

The generated files are split across two target locations (see "Target files" above), so the PR is assembled by hand
rather than copying this folder 1:1. `extend.json` and `README.md` are pipeline artefacts and are NOT copied.

1. Local test (symlink, before editing bam-masterdata):
   ```bash
   ln -s $(pwd)/generated/welded_fatigue_v2/datamodel/ ../bam-masterdata/bam_masterdata/datamodel/welded_fatigue_v2
   cd ../bam-masterdata
   python -c "from bam_masterdata.metadata.entities import ObjectType; print('discovery OK')"
   pytest tests/
   rm bam_masterdata/datamodel/welded_fatigue_v2   # remove the symlink again
   ```
2. Build the PR branch in bam-masterdata:
   ```bash
   cd ../bam-masterdata
   git checkout main && git pull
   git checkout -b add-welded-fatigue-types
   mkdir -p bam_masterdata/datamodel/fatigue
   touch bam_masterdata/datamodel/fatigue/__init__.py
   ```
   - `fatigue/vocabularies.py`: imports + classes `WeldedFatigueWorkflowStep`, `FatigueLoadLevel`, `FatigueRecordingMode`,
     `FatigueTerminationReason` from `vocabularies.py`.
   - `welding/vocabularies.py`: append classes `Iso5817QualityLevel`, `Iso5817AnnexCRating`.
   - `fatigue/object_types.py`: copy `object_types.py` unchanged.
   - EXTEND: paste the two term snippets above into `WeldType` and `AuxiliaryMaterialType`.
   ```bash
   pytest tests/
   git add bam_masterdata/datamodel/fatigue/ bam_masterdata/datamodel/welding/vocabularies.py bam_masterdata/datamodel/vocabulary_types.py
   ```
3. Submit PR to `BAMresearch/bam-masterdata`. Mention in the description: new `FATIGUE.` namespace, prefix
   `EXP.MECH.CYC_FAT` follows sibling CreepTest (`EXP.MECH.CREEP`), reuse of `EXPERIMENTAL_STEP.WELDMENT_TYPE` on a Sample
   type, and the `WELDING.WELD_TYPE` extension (welding group review).
4. After the PR is merged: `/bam-sync` in this repo and re-run `/bam-analyze-prd` to confirm the CREATE list shrinks to zero.
