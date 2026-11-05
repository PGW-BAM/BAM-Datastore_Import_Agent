# Gap Report: welded_fatigue_v2

PRD `BAM_PRD_Workflow_FB72_v2.md` (workflow style, predecessor `BAM_PRD_Workflow_FB72.md`) ·
design `generated/welded_fatigue_v2/design.json` (structure-designer, 2026-10-06) ·
catalog bam-masterdata SHA `d7a871be8c6aa934af2bf77357d30d8a5d689d92` (2026-10-05 13:43:38 +0200, `generated/catalog.json` + `generated/CATALOG.md`) ·
live inventory `generated/live/dev1_inventory.md` (instance dev1, openBIS 20.10.12.5, captured 2026-10-06) ·
additional read-only live facts supplied by the coordinator on 2026-10-06 (cited as "coord. live check 2026-10-06").

Analysed: 2026-10-06 by gap-analyzer. Citations are bam-masterdata source `file:line` as recorded in `catalog.json`
(SHA above). The local clone `C:\Users\pgerards\repos\bam-masterdata` was NOT used for citations (its line numbers differ).

---

## REUSE

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

Checked and **not** reused (semantic look-alikes):
- `CREEP_TEST_END_OF_TEST_CRITERIUM` (creep_test/vocabularies.py:99; terms TEST_PIECE_BREAK, TIME_LIMIT, EXTENSION_LIMIT, OTHER_SPECIFY) vs. fatigue termination reason: no "crack detected", no "run-out"/cycle limit, no manual stop; creep-domain code. Does not fit → `FATIGUE.TERMINATION_REASON` CREATE.
- `SPECIMEN_STATUS` (vocabulary_types.py:31187; DISPOSED, IN_PREPARATION, PREPARED, STORED, TESTED) vs. next workflow step: storage/life-cycle state, not an ordered 01-12 step list. Does not fit → `WELDED_FATIGUE_WORKFLOW_STEP` CREATE.
- `TESTING_MACHINE_LOAD_TYPE` (vocabulary_types.py:31372; AXIAL, TORSION, …) vs. load level: load *mode*, not high/medium/low level. Does not fit.
- `MS_ACQUISITION_MODE` (mass_spectrometry/vocabularies.py:158) / `CAMERA_SHUTTER_MODE` (vocabulary_types.py:659) vs. recording mode: other domains. Do not fit.
- `MICROSCOPY_FCG_CRACKLENGTH_TYPE` (vocabulary_types.py:28207; BEACHMARK, FINAL, NOTCH): crack-length type for FCG microscopy, not related to any design vocabulary.
- No ISO 5817 vocabulary exists in the catalog (search `5817`, `QUALITY_LEVEL`, `RATING`: 0 hits).

### Property types (assigned to new types)

| Entity | Kind | Citation (file:line) | On instance | Role in design |
|---|---|---|---|---|
| `EXPERIMENTAL_STEP.WELDMENT_TYPE` (CONTROLLEDVOCABULARY → `WELDING.WELD_TYPE`) | PropertyType | bam_masterdata/datamodel/welding/object_types.py:409 (Weldment) | missing on instance (coord. live check: live Weldment has only generic step props) | Specimen "Weld geometry" (section Specimen Identification) + series table column |
| `DEFECT_DESCRIPTION` (MULTILINE_VARCHAR) | PropertyType | bam_masterdata/datamodel/object_types.py:7429 (Named, `SAMPLE_NDT.NAMED`) | UNCONFIRMED | Specimen step 01 "Gross weld defects" |

Inherited / used without new assignment (no action beyond instance sync): `$NAME` (object_types.py:3012), `ALIAS` (:3021),
`EXPERIMENTAL_STEP.EXPERIMENTAL_DESCRIPTION` (object_types.py:296, GOM software name/version on SCAN step),
`START_DATE`/`END_DATE`/`FINISHED_FLAG`/`NOTES` (object_types.py:269/278/260/341), `OPERATOR` (object_types.py:362),
`AUXILIARY_MATERIAL_TYPE` property (object_types.py:1218), `TESTING_MACHINE_DRIVE_TYPE` property (object_types.py:1773),
`SOP.DESCRIPTION` (object_types.py:2884), `$DEFAULT_OBJECT_TYPE` (collection_types.py:24).

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

## EXTEND

| Entity | Kind | Citation | Additions | On instance | PR action |
|---|---|---|---|---|---|
| `WELDING.WELD_TYPE` | Vocabulary (6 terms: FILLET, GROOVE, PLUG, SPOT, SURFACING, TACK) | bam_masterdata/datamodel/welding/vocabularies.py:38 (last term :74) | `WELDING_BUTT_WELD` "butt weld", `WELDING_CRUCIFORM_WELD` "cruciform weld" (prefix convention of existing terms; resolution Q2) | present, 6 terms identical (inventory §1) → 2 terms missing after PR | PR to bam-masterdata `welding/vocabularies.py` (welding group owns the list; also affects `EXPERIMENTAL_STEP.WELDMENT`) |
| `AUXILIARY_MATERIAL_TYPE` | Vocabulary (10 terms) | bam_masterdata/datamodel/vocabulary_types.py:252 (last term :312) | `STRAIN_GAUGE` "Strain gauge", `CRACK_DETECTION_AGENT` "Crack detection agent" (`ADHESIVE` exists, :264) | present, same 10 terms (coord. live check) → 2 terms missing after PR | PR to bam-masterdata `vocabulary_types.py` |

Machine-readable: `generated/welded_fatigue_v2/datamodel/extend.json`. No ObjectType needs EXTEND (no property added to an existing type).

## CREATE

### Object types

| Entity | Kind | Why not reusable (closest peer + citation) | Replaces live-only |
|---|---|---|---|
| `SAMPLE.WELDED_FATIGUE_SPECIMEN` (WeldedFatigueSpecimen, inherits Sample, prefix `SAM.WFS`) | ObjectType | Closest peers: `SPECIMEN.FCG` (object_types.py:5586) – fatigue-crack-growth CT/SENB specimen with notch geometry, not a welded plate specimen, not a Sample subtype; `SAMPLE.BUILDING_MATERIALS_SPECIMEN` (building_materials/object_types.py:5) – FB 7 pattern only; `SAMPLE.CREEP_TEST_TEST_PIECE` (creep_test/object_types.py:934) – creep domain. None carries weld quality / distortion / series data. | `TEST_SPECIMEN` + section-wise `PRE_QUALITY_CHECK`, `CHAMFERING_GRINDING`, `WELD_ANALYSIS`, `SERIES_ASSIGNMENT`, `TEST_SETUP_GEOMETRY` |
| `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` (CyclicFatigueTest, inherits MechanicalTest, prefix `EXP.MECH.CYC_FAT`) | ObjectType | Closest peers: `EXPERIMENTAL_STEP.FCG_TEST` (activities.py:122) – Paris/threshold crack-growth results, no S-N test data; `EXPERIMENTAL_STEP.FCG_STEP` (activities.py:255) – load-step definition; `EXPERIMENTAL_STEP.MECHANICAL_TEST.CREEP_TEST` (creep_test/object_types.py:14) – creep. None covers strain-gauge application, IMC settings, cycle counts. | `MONITORING_APPLICATION`, `AMPLIFIER_TEST_BENCH_SETTINGS`, `INSTALLATION_STRESS_MEASUREMENT`, `CYCLIC_FATIGUE_TEST`, `DATA_EVALUATION` |

### Vocabularies

| Entity | Kind | Why not reusable (closest peer + citation) | Replaces live-only |
|---|---|---|---|
| `WELDED_FATIGUE_WORKFLOW_STEP` (13 terms S01…S12, DONE) | Vocabulary | `SPECIMEN_STATUS` (vocabulary_types.py:31187) is a life-cycle state, not an ordered step list | `STEP_STATUS` (+ `STEP_ORDER` property) |
| `WELDING.ISO_5817_QUALITY_LEVEL` (B, C, D) | Vocabulary | no ISO 5817 vocabulary in catalog | `ISO_5817_CLASS` (identical terms) |
| `WELDING.ISO_5817_ANNEX_C_RATING` (C63, B90, B125) | Vocabulary | no ISO 5817 vocabulary in catalog | `WELD_ANALYSIS_RATING` (C56 → corrected to C63) |
| `FATIGUE.LOAD_LEVEL` (HIGH, MEDIUM, LOW) | Vocabulary | `TESTING_MACHINE_LOAD_TYPE` (vocabulary_types.py:31372) = load mode, not level | – (legacy had no load level) |
| `FATIGUE.RECORDING_MODE` (FULL_SIGNAL, PEAK_COUNTER, PEAK_VALLEY) | Vocabulary | `MS_ACQUISITION_MODE` (mass_spectrometry/vocabularies.py:158) – MS domain | `DATA_RECORDING_MODE` (identical terms) |
| `FATIGUE.TERMINATION_REASON` (TOTAL_FRACTURE, CRACK_DETECTED, RUN_OUT, MANUAL_STOP) | Vocabulary | `CREEP_TEST_END_OF_TEST_CRITERIUM` (creep_test/vocabularies.py:99) – terms do not cover crack detection / run-out / manual stop | `STOP_REASON` (CRACK_DETECTION → CRACK_DETECTED, DEFINED_CYCLES → RUN_OUT) |

### Property types (33) — see "Property types" table below for codes, data types and collision checks.

Closest catalog peers that were deliberately not reused (verified): `CREEP_TEST_PRELOAD` REAL (creep_test/object_types.py:343) –
creep domain, no fixed unit; `FINAL_CYCLES` REAL (activities.py:344, FcgStep) – data type mismatch vs INTEGER;
`INITIAL_CYCLES` INTEGER (activities.py:290) – meaning "cycles at step start", not gross/net count;
`SPEC_FCG_THICKNESS` REAL (object_types.py:5650) / `WORKPIECE_THICKNESS` REAL (welding/object_types.py:715) – single value, FCG/welding-process context, no position index;
`STOP_CONDITION` VARCHAR (mass_spectrometry/object_types.py:291) – SIMS free text;
`CREEP_TEST_FORCE_RECORDING` BOOLEAN (creep_test/object_types.py:1379) – not a mode list;
`NUMBER_OF_CHANNELS` INTEGER (instruments.py:451) – count, not channel list.

## LIVE-ONLY

All rows cite `generated/live/dev1_inventory.md` (line). Recommendation for every row: **migrate** (no standardisation PR) —
the live model has no `$NAME`, no sections, "EN / DE" labels, chain linking depth 12 and holds no measurement values
(inventory :72), so there is no data to convert; the 189 legacy objects can be archived/deleted by the space admin after
the new model is provisioned (admin decision, not part of this pipeline).

### Object types (16)

| Live entity | Kind | Citation | Replacement in design / proposal |
|---|---|---|---|
| `TEST_SPECIMEN` | ObjectType | dev1_inventory.md:25 | → migrated to `SAMPLE.WELDED_FATIGUE_SPECIMEN` (CREATE) |
| `PRE_QUALITY_CHECK` | ObjectType | dev1_inventory.md:26 | → specimen section "Initial Quality Check" (no own object) |
| `CHAMFERING_GRINDING` | ObjectType | dev1_inventory.md:27 | → specimen section "Chamfering And Grinding" |
| `SPECIMEN_RECORDING` | ObjectType | dev1_inventory.md:28 | → `EXPERIMENTAL_STEP` (REUSE) object `<specimen>-SCAN`, instrument as parent |
| `WELD_ANALYSIS` | ObjectType | dev1_inventory.md:29 | → specimen section "Weld Analysis" + files on `<specimen>-SCAN` |
| `SERIES_ASSIGNMENT` | ObjectType | dev1_inventory.md:30 | → specimen section "Series Assignment" + collection membership |
| `TEST_SETUP_GEOMETRY` | ObjectType | dev1_inventory.md:31 | → specimen section "Geometry Before Installation" (3 REAL per quantity instead of one) |
| `MONITORING_APPLICATION` | ObjectType | dev1_inventory.md:32 | → `…CYCLIC_FATIGUE_TEST` section 07; materials/camera as parents |
| `AMPLIFIER_TEST_BENCH_SETTINGS` | ObjectType | dev1_inventory.md:33 | → `…CYCLIC_FATIGUE_TEST` section 08; amplifier/machine as parents |
| `INSTALLATION_STRESS_MEASUREMENT` | ObjectType | dev1_inventory.md:34 | → `…CYCLIC_FATIGUE_TEST` section 09 |
| `CYCLIC_FATIGUE_TEST` | ObjectType | dev1_inventory.md:35 | → `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` section 10 (CREATE; different code, no clash) |
| `DATA_EVALUATION` | ObjectType | dev1_inventory.md:36 | → `…CYCLIC_FATIGUE_TEST` section 11 |
| `FRACTURE_SURFACE_ANALYSIS` | ObjectType | dev1_inventory.md:37 | → `EXPERIMENTAL_STEP` (REUSE) object `<specimen>-FRACTURE`, camera/microscope as parents |
| `STRAIN_GAUGE_TYPE` | ObjectType | dev1_inventory.md:38 | → `AUXILIARY_MATERIAL` (REUSE) + `AUXILIARY_MATERIAL_TYPE=STRAIN_GAUGE` (EXTEND) |
| `CONSUMABLE_TYPE` | ObjectType | dev1_inventory.md:38 | → `AUXILIARY_MATERIAL` (REUSE) + `ADHESIVE` / `CRACK_DETECTION_AGENT` (EXTEND) |
| `INSTRUMENT_DUMMY` | ObjectType | dev1_inventory.md:38 | → `INSTRUMENT` / `INSTRUMENT.CAMERA` / `INSTRUMENT.MEASURING_AMPLIFIER` / `TESTING_MACHINE` (REUSE) |

Common legacy properties `STEP_ORDER` (INTEGER) and `STATUS` (→ `STEP_STATUS`) on all 12 step types (dev1_inventory.md:40)
→ replaced by `FATIGUE.NEXT_STEP` on the specimen + inherited `FINISHED_FLAG` on step objects; step order is implicit in the step codes / SOP.

### Vocabularies (6)

| Live entity | Kind | Citation | Replacement in design / proposal |
|---|---|---|---|
| `WELD_GEOMETRY` (BUTT_WELD, CRUCIFORM_WELD) | Vocabulary | dev1_inventory.md:44 | → `WELDING.WELD_TYPE` + `WELDING_BUTT_WELD`, `WELDING_CRUCIFORM_WELD` (EXTEND) |
| `ISO_5817_CLASS` (B, C, D) | Vocabulary | dev1_inventory.md:44 | → `WELDING.ISO_5817_QUALITY_LEVEL` (CREATE, same terms) |
| `WELD_ANALYSIS_RATING` (C56, B90, B125) | Vocabulary | dev1_inventory.md:44 | → `WELDING.ISO_5817_ANNEX_C_RATING` (CREATE; C56 corrected to C63 per decision 3) |
| `STOP_REASON` (TOTAL_FRACTURE, CRACK_DETECTION, DEFINED_CYCLES, MANUAL_STOP) | Vocabulary | dev1_inventory.md:45 | → `FATIGUE.TERMINATION_REASON` (CREATE; CRACK_DETECTION→CRACK_DETECTED, DEFINED_CYCLES→RUN_OUT) |
| `DATA_RECORDING_MODE` (FULL_SIGNAL, PEAK_COUNTER, PEAK_VALLEY) | Vocabulary | dev1_inventory.md:45 | → `FATIGUE.RECORDING_MODE` (CREATE, same terms) |
| `STEP_STATUS` (PLANNED, IN_PROGRESS, DONE) | Vocabulary | dev1_inventory.md:46 | → no 1:1 replacement; status expressed by `WELDED_FATIGUE_WORKFLOW_STEP` (CREATE) via `FATIGUE.NEXT_STEP` + `FINISHED_FLAG` |

### Collection type (1)

| Live entity | Kind | Citation | Replacement in design / proposal |
|---|---|---|---|
| `TEST_SERIES` | CollectionType | dev1_inventory.md:49 | → `COLLECTION` (REUSE; identical props per inventory) |

### Dataset types (17)

| Live entity | Kind | Citation | Replacement in design / proposal |
|---|---|---|---|
| `REWORK_PROTOCOL` | DatasetType | dev1_inventory.md:50 | → `ATTACHMENT` (step 02 post-processing report, on specimen) |
| `SPECIMEN_PHOTOS` | DatasetType | dev1_inventory.md:50 | → `RAW_DATA` (step 01, on specimen) |
| `3D_SCAN_RAW` | DatasetType | dev1_inventory.md:50 | → `RAW_DATA` (step 03, on SCAN step) |
| `WELD_ANALYSIS_EVAL` | DatasetType | dev1_inventory.md:50 | → `ANALYZED_DATA` (step 04, on SCAN step) |
| `RANDOMIZATION_CODE` | DatasetType | dev1_inventory.md:50 | → `SOURCE_CODE` (step 05, on collection) |
| `STRAIN_GAUGE_POSITION_DRAWING` | DatasetType | dev1_inventory.md:51 | → `ATTACHMENT` (step 07, on TEST step) |
| `SETUP_PHOTO` | DatasetType | dev1_inventory.md:51 | → `RAW_DATA` (step 07, on TEST step) |
| `BENDING_MOMENT_RAW` | DatasetType | dev1_inventory.md:51 | → `RAW_DATA` (step 09, on TEST step) |
| `RAW_CONVERSION_SCRIPT` | DatasetType | dev1_inventory.md:51 | → `SOURCE_CODE` (step 11 conversion script, on TEST step) |
| `LOAD_PROGRAM_EXCEL` | DatasetType | dev1_inventory.md:51 | → `MEASUREMENT_PROTOCOL_FILE` (step 10, on TEST step) |
| `FATIGUE_MESS_RAW` | DatasetType | dev1_inventory.md:52 | → `RAW_DATA` (step 10, on TEST step) |
| `MONITORING_IMAGES` | DatasetType | dev1_inventory.md:52 | → `RAW_DATA` (step 10, on TEST step) |
| `EVALUATION_PLOTS` | DatasetType | dev1_inventory.md:52 | → `FIGURE.PLOT` (step 11, on TEST step) |
| `CLEANED_DATA_TABULAR` | DatasetType | dev1_inventory.md:52 | → `PROCESSED_DATA` (step 11, on TEST step) |
| `MACRO_FRACTURE_PHOTOS` | DatasetType | dev1_inventory.md:52 | → `RAW_DATA` (step 12, on FRACTURE step) |
| `MICROSCOPE_CRACK_IMAGES` | DatasetType | dev1_inventory.md:53 | → `RAW_DATA` (step 12, on FRACTURE step) |
| `BEACH_MARK_EVALUATION_EXCEL` | DatasetType | dev1_inventory.md:53 | → `ANALYZED_DATA` (step 12, on FRACTURE step) |

### Legacy property types (informative, not counted as classes)

| Live property (type) | Citation | Replacement |
|---|---|---|
| `FINAL_DESIGNATION` | dev1_inventory.md:25 | `$NAME` (inherited) |
| `INTERNAL_DESIGNATION` | dev1_inventory.md:25 | `ALIAS` (inherited, resolution Q4) |
| `ORIGINAL_ID` | dev1_inventory.md:25 | `FATIGUE.MANUFACTURER_DESIGNATION` |
| `SHEET_ORIGIN` | dev1_inventory.md:25 | `FATIGUE.SOURCE_SHEET` |
| `WELD_GEOMETRY_PROP` | dev1_inventory.md:25 | `EXPERIMENTAL_STEP.WELDMENT_TYPE` (REUSE) |
| `ISO_5817_CLASS_PROP` | dev1_inventory.md:25 | `FATIGUE.TARGET_QUALITY_LEVEL` |
| `INITIAL_ANGULAR_DISTORTION` / `FINAL_ANGULAR_DISTORTION` | dev1_inventory.md:26 | `FATIGUE.INITIAL_ANGULAR_DISTORTION` / `FATIGUE.ANGULAR_DISTORTION_AFTER_STRAIGHTENING` |
| `INITIAL_EDGE_MISALIGNMENT` / `FINAL_EDGE_MISALIGNMENT` | dev1_inventory.md:26 | `FATIGUE.INITIAL_EDGE_MISALIGNMENT` / `FATIGUE.EDGE_MISALIGNMENT_AFTER_STRAIGHTENING` |
| `WAS_STRAIGHTENED` | dev1_inventory.md:26 | `FATIGUE.WAS_STRAIGHTENED` |
| `GROSS_WELD_DEFECTS` | dev1_inventory.md:26 | `DEFECT_DESCRIPTION` (REUSE) |
| `INSPECTOR`, `DATE_OF_INSPECTION` | dev1_inventory.md:26 | **no replacement** (not a PRD v2 data item; see Design remarks) |
| `WELD_MODIFICATIONS` | dev1_inventory.md:27 | `FATIGUE.WELD_POST_TREATMENT_NOTES` |
| `USED_INSTRUMENT` (SAMPLE link) | dev1_inventory.md:28 | parent link ZEISS GOM ATOS 5 → SCAN step |
| `ANALYSIS_RATING` | dev1_inventory.md:29 | `FATIGUE.ISO_5817_ANNEX_C_RATING` |
| `RANDOMIZATION_DATE` | dev1_inventory.md:30 | **no replacement** (not a PRD v2 data item; registration date of the `SOURCE_CODE` dataset) |
| `SPECIMEN_THICKNESS_POS_1_3`, `SPECIMEN_WIDTH_POS_1_3` (REAL) | dev1_inventory.md:31 | `FATIGUE.THICKNESS_POS_1..3`, `FATIGUE.WIDTH_POS_1..3` |
| `AVG_SPECIMEN_THICKNESS`, `AVG_SPECIMEN_WIDTH` | dev1_inventory.md:31 | `FATIGUE.MEAN_THICKNESS`, `FATIGUE.MEAN_WIDTH` |
| `APPLICATION_TIMESTAMP` | dev1_inventory.md:32 | `FATIGUE.STRAIN_GAUGE_APPLICATION_TIME` |
| `USED_STRAIN_GAUGE_TYPE`, `USED_ADHESIVE_TYPE`, `USED_CRACK_LUMINESCENCE_TYPE`, `CAMERA_SYSTEM` | dev1_inventory.md:32 | parent links (AUXILIARY_MATERIAL ×3, INSTRUMENT.CAMERA) → TEST step |
| `DMS_DISTANCE_TO_WELD`, `DMS_DISTANCE_TO_EDGE` | dev1_inventory.md:32 | `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_WELD_TOE`, `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_EDGE` |
| `IMC_MEASUREMENT_AMPLIFIER` | dev1_inventory.md:33 | parent link INSTRUMENT.MEASURING_AMPLIFIER → TEST step |
| `SAMPLING_FREQUENCY`, `DATA_RECORDING_MODE_PROP`, `RECORDED_CHANNELS` | dev1_inventory.md:33 | `FATIGUE.SAMPLING_FREQUENCY`, `FATIGUE.RECORDING_MODE`, `FATIGUE.RECORDED_CHANNELS` |
| `PRE_LOAD_FORCE` | dev1_inventory.md:34 | `FATIGUE.PRELOAD_FORCE` |
| `MARKER_LOADS_ACTIVE`, `STOP_REASON_PROP` | dev1_inventory.md:35 | `FATIGUE.BEACH_MARKS_ACTIVE`, `FATIGUE.TERMINATION_REASON` |
| `FATIGUE_TEST_BENCH` | dev1_inventory.md:35 | parent link TESTING_MACHINE → TEST step |
| `FINAL_GROSS_CYCLES`, `FINAL_NET_CYCLES`, `CYCLES_AT_10_PERCENT_SG_DEVIATION` | dev1_inventory.md:36 | `FATIGUE.CYCLES_GROSS`, `FATIGUE.CYCLES_NET`, `FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP` |
| `USED_CAMERA`, `USED_MICROSCOPE` | dev1_inventory.md:37 | parent links → FRACTURE step |
| `OPERATOR` (on 11 legacy step types; data type not recorded) | dev1_inventory.md:27-37 | inherited `OPERATOR` (VARCHAR, object_types.py:362) on step objects only; see collision check |
| `STEP_ORDER`, `STATUS` | dev1_inventory.md:40 | `FATIGUE.NEXT_STEP` + `FINISHED_FLAG` |

Inventory objects under `/MATERIALS/7_2_EQUIPMENT` and `/MATERIALS/7_2_MATERIALS` (dev1_inventory.md:66-68) exist live, but their
object types are not recorded (likely the live-only `INSTRUMENT_DUMMY` / `STRAIN_GAUGE_TYPE` / `CONSUMABLE_TYPE`) — UNCONFIRMED.
If so they must be re-created as standard types (9 inventory objects in design.json `inventory_links`).

## Property types

Collision check = (a) exact code in catalog property index (1172 codes, all types), (b) exact code on dev1 (legacy codes from
dev1_inventory.md §2 + coord. live check), with data-type comparison. All new codes use the `FATIGUE.` namespace, which does
not exist in the catalog (0 hits) nor on dev1; legacy live codes are unprefixed → **no exact collision for any new code**.
Property/vocabulary code pairs (`FATIGUE.LOAD_LEVEL`, `FATIGUE.RECORDING_MODE`, `FATIGUE.TERMINATION_REASON`) are separate
openBIS namespaces (same pattern as `AUXILIARY_MATERIAL_TYPE`, `PHYSICAL_STATE` in the catalog) → no conflict.

| Code | Data type | Status (reuse: citation / new) | Collision check |
|---|---|---|---|
| `EXPERIMENTAL_STEP.WELDMENT_TYPE` | CONTROLLEDVOCABULARY → WELDING.WELD_TYPE | reuse: welding/object_types.py:409 | catalog: same type ✓ · dev1: missing on instance (create with same type) |
| `DEFECT_DESCRIPTION` | MULTILINE_VARCHAR | reuse: object_types.py:7429 | catalog: same type ✓ · dev1: UNCONFIRMED |
| `FATIGUE.NEXT_STEP` | CONTROLLEDVOCABULARY → WELDED_FATIGUE_WORKFLOW_STEP | new | none · live near-name: `STATUS`/`STEP_ORDER` (different code) |
| `FATIGUE.MANUFACTURER_DESIGNATION` | VARCHAR | new | none · live near-name `ORIGINAL_ID`; catalog `MANUFACTURER` VARCHAR (object_types.py:3048) = company, not ID |
| `FATIGUE.SOURCE_SHEET` | VARCHAR | new | none · live near-name `SHEET_ORIGIN` |
| `FATIGUE.TARGET_QUALITY_LEVEL` | CONTROLLEDVOCABULARY → WELDING.ISO_5817_QUALITY_LEVEL | new | none · live near-name `ISO_5817_CLASS_PROP` |
| `FATIGUE.INITIAL_ANGULAR_DISTORTION` | REAL | new | none · live `INITIAL_ANGULAR_DISTORTION` (different code) |
| `FATIGUE.INITIAL_EDGE_MISALIGNMENT` | REAL | new | none · live `INITIAL_EDGE_MISALIGNMENT` (different code) |
| `FATIGUE.WAS_STRAIGHTENED` | BOOLEAN | new | none · live `WAS_STRAIGHTENED` (different code) |
| `FATIGUE.ANGULAR_DISTORTION_AFTER_STRAIGHTENING` | REAL | new | none · live `FINAL_ANGULAR_DISTORTION` |
| `FATIGUE.EDGE_MISALIGNMENT_AFTER_STRAIGHTENING` | REAL | new | none · live `FINAL_EDGE_MISALIGNMENT` |
| `FATIGUE.WELD_POST_TREATMENT_NOTES` | MULTILINE_VARCHAR | new | none · live `WELD_MODIFICATIONS` |
| `FATIGUE.ISO_5817_ANNEX_C_RATING` | CONTROLLEDVOCABULARY → WELDING.ISO_5817_ANNEX_C_RATING | new | none · live `ANALYSIS_RATING` |
| `FATIGUE.LOAD_LEVEL` | CONTROLLEDVOCABULARY → FATIGUE.LOAD_LEVEL | new | none |
| `FATIGUE.TEST_ORDER` | INTEGER | new | none |
| `FATIGUE.THICKNESS_POS_1` | REAL | new | none · live `SPECIMEN_THICKNESS_POS_1_3`; catalog `SPEC_FCG_THICKNESS` REAL (object_types.py:5650) different code |
| `FATIGUE.THICKNESS_POS_2` | REAL | new | none |
| `FATIGUE.THICKNESS_POS_3` | REAL | new | none |
| `FATIGUE.WIDTH_POS_1` | REAL | new | none · live `SPECIMEN_WIDTH_POS_1_3` |
| `FATIGUE.WIDTH_POS_2` | REAL | new | none |
| `FATIGUE.WIDTH_POS_3` | REAL | new | none |
| `FATIGUE.MEAN_THICKNESS` | REAL | new | none · live `AVG_SPECIMEN_THICKNESS` |
| `FATIGUE.MEAN_WIDTH` | REAL | new | none · live `AVG_SPECIMEN_WIDTH` |
| `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_WELD_TOE` | REAL | new | none · live `DMS_DISTANCE_TO_WELD` |
| `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_EDGE` | REAL | new | none · live `DMS_DISTANCE_TO_EDGE` |
| `FATIGUE.STRAIN_GAUGE_APPLICATION_TIME` | TIMESTAMP | new | none · live `APPLICATION_TIMESTAMP` |
| `FATIGUE.SAMPLING_FREQUENCY` | INTEGER | new | none · live `SAMPLING_FREQUENCY` (different code; live data type not recorded) |
| `FATIGUE.RECORDING_MODE` | CONTROLLEDVOCABULARY → FATIGUE.RECORDING_MODE | new | none · live `DATA_RECORDING_MODE_PROP` |
| `FATIGUE.RECORDED_CHANNELS` | VARCHAR | new | none · live `RECORDED_CHANNELS` (different code) |
| `FATIGUE.PRELOAD_FORCE` | REAL | new | none · live `PRE_LOAD_FORCE`; catalog `CREEP_TEST_PRELOAD` REAL (creep_test/object_types.py:343) |
| `FATIGUE.BEACH_MARKS_ACTIVE` | BOOLEAN | new | none · live `MARKER_LOADS_ACTIVE` |
| `FATIGUE.TERMINATION_REASON` | CONTROLLEDVOCABULARY → FATIGUE.TERMINATION_REASON | new | none · live `STOP_REASON_PROP` |
| `FATIGUE.CYCLES_GROSS` | INTEGER | new | none · live `FINAL_GROSS_CYCLES`; catalog `FINAL_CYCLES` REAL (activities.py:344) |
| `FATIGUE.CYCLES_NET` | INTEGER | new | none · live `FINAL_NET_CYCLES` |
| `FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP` | MULTILINE_VARCHAR | new | none · live `CYCLES_AT_10_PERCENT_SG_DEVIATION` |

Inherited codes with a live-side risk:
- `OPERATOR` — catalog VARCHAR (object_types.py:362). dev1 `EXPERIMENTAL_STEP` lacks it, but a live `OPERATOR` property type
  exists (used by 11 legacy step types, dev1_inventory.md:27-37) with **unrecorded data type** → must be checked before sync;
  if it is not VARCHAR, the assignment to `…CYCLIC_FATIGUE_TEST` / `EXPERIMENTAL_STEP` collides (UNCONFIRMED).
- `RESPONSIBLE_PERSON`, `CO_RESPONSIBLE_PERSON` (OBJECT → PERSON.BAM, object_types.py:3095/3105) — `PERSON.BAM` exists on dev1;
  property-type presence UNCONFIRMED.

## Instance sync

openBIS has no inheritance: when `SAMPLE.WELDED_FATIGUE_SPECIMEN` and `…CYCLIC_FATIGUE_TEST` are created on dev1, all inherited
property assignments are created explicitly. Whatever is missing on dev1 must be created first or is skipped.

| Entity | Status on instance | Needed action |
|---|---|---|
| `SAMPLE` | outdated (8 of 19 props; coord. live check) | Admin: sync standard masterdata. Not blocking for the new type. |
| Inherited Sample props `BAM_OE`, `BAM_ROOM`, `BAM_FLOOR`, `BAM_HOUSE`, `BAM_LOCATION`, `BAM_LOCATION_COMPLETE` (object_types.py:3085/3115/3126/3137/3148/3159) | **missing on instance** — their vocabularies `BAM_OE`, `BAM_ROOM`, `BAM_FLOOR`, `BAM_HOUSE`, `BAM_LOCATION`, `BAM_LOCATION_COMPLETE` do not exist on dev1 (coord. live check) | **Skipped on dev1** when provisioning `SAMPLE.WELDED_FATIGUE_SPECIMEN` until the standard masterdata (incl. these BAM vocabularies) is synced by an admin. Note: these vocabularies are only referenced in bam-masterdata, not defined as VocabularyType in the catalog (0 hits) → they come from the central BAM admin import, not from a bam-masterdata sync. |
| Inherited Sample props `RESPONSIBLE_PERSON`, `CO_RESPONSIBLE_PERSON` (:3095/:3105) | UNCONFIRMED (target type `PERSON.BAM` present) | Create property types if missing (OBJECT → PERSON.BAM), then assign. |
| Inherited Sample props `NOTES`, `$XMLCOMMENTS` | present (on live EXPERIMENTAL_STEP) | assign |
| Inherited Sample prop `$ANNOTATIONS_STATE` (:3187) | UNCONFIRMED | assign if present, otherwise skip (ELN-internal) |
| Inherited Sample props `$NAME`, `ALIAS`, `DESCRIPTION`, `SAMPLE_ID_NUMBER`, `MANUFACTURER`, `BARCODE_EXTERNAL`, `SUPPLIER`, `PHYSICAL_STATE` | present | assign |
| `PHYSICAL_STATE` (vocabulary) | present | none |
| `EXPERIMENTAL_STEP` | outdated (no `OPERATOR`; coord. live check) | Admin sync; for the new step type: create/verify `OPERATOR` (see collision check) before assigning it |
| `EXPERIMENTAL_STEP.MECHANICAL_TEST` | missing on instance (inventory :12) | Optional (not required for creating the child type); recommended standard sync |
| `EXPERIMENTAL_STEP.WELDMENT` | present, but without `EXPERIMENTAL_STEP.WELDMENT_TYPE` (outdated) | Admin sync (not required by this workflow) |
| `EXPERIMENTAL_STEP.WELDMENT_TYPE` (property type) | **missing on instance** | Create (CONTROLLEDVOCABULARY → WELDING.WELD_TYPE) before assigning to `SAMPLE.WELDED_FATIGUE_SPECIMEN` |
| `DEFECT_DESCRIPTION` (property type) | UNCONFIRMED | Create if missing (MULTILINE_VARCHAR) |
| `WELDING.WELD_TYPE` | present (6 terms, identical) → outdated after EXTEND | Add `WELDING_BUTT_WELD`, `WELDING_CRUCIFORM_WELD` after PR merge |
| `AUXILIARY_MATERIAL_TYPE` | present (10 terms) → outdated after EXTEND | Add `STRAIN_GAUGE`, `CRACK_DETECTION_AGENT` after PR merge |
| `AUXILIARY_MATERIAL` | present | none |
| `INSTRUMENT` | present; outdated (BAM_* location props cannot exist on dev1) | none for this workflow |
| `INSTRUMENT.CAMERA`, `INSTRUMENT.MEASURING_AMPLIFIER` | present | none |
| `TESTING_MACHINE` | present; outdated (BAM_* location props) | none for this workflow |
| `TESTING_MACHINE_DRIVE_TYPE` (term `SERVOHYDRAULIC`) | UNCONFIRMED | Verify; create/extend if missing |
| `SOP` | outdated (4 of 14 props; coord. live check) | none for this workflow (`$NAME`, `DESCRIPTION` suffice) |
| `COLLECTION` | present | none |
| `PERSON.BAM` | present | none |
| Dataset types `RAW_DATA`, `PROCESSED_DATA`, `ANALYZED_DATA`, `ATTACHMENT`, `SOURCE_CODE`, `MEASUREMENT_PROTOCOL_FILE`, `FIGURE.PLOT` | presumed present (inventory :53-54 names them as mapping targets; not itemised) | Verify before upload |
| CREATE entities (2 object types, 6 vocabularies, 33 property types) | missing on instance (by definition) | Provision after bam-masterdata PR (masterdata-extender → notebook) |
| Inventory objects (9) in `/MATERIALS/7_2_*` | exist live, types UNCONFIRMED (probably live-only) | Re-create/re-type as standard types if they are `INSTRUMENT_DUMMY`/`STRAIN_GAUGE_TYPE`/`CONSUMABLE_TYPE` |

## Consistency

- Every CONTROLLEDVOCABULARY property points to a classified vocabulary: `FATIGUE.NEXT_STEP`→`WELDED_FATIGUE_WORKFLOW_STEP` (CREATE),
  `FATIGUE.TARGET_QUALITY_LEVEL`→`WELDING.ISO_5817_QUALITY_LEVEL` (CREATE), `FATIGUE.ISO_5817_ANNEX_C_RATING`→`WELDING.ISO_5817_ANNEX_C_RATING` (CREATE),
  `FATIGUE.LOAD_LEVEL`/`FATIGUE.RECORDING_MODE`/`FATIGUE.TERMINATION_REASON` → same-code vocabularies (CREATE),
  `EXPERIMENTAL_STEP.WELDMENT_TYPE`→`WELDING.WELD_TYPE` (EXTEND). ✓
- No OBJECT properties in the design (inventory linked as parents, design `link_rules`). ✓
- All parent-link target types exist in the catalog (INSTRUMENT, INSTRUMENT.CAMERA, INSTRUMENT.MEASURING_AMPLIFIER, TESTING_MACHINE, AUXILIARY_MATERIAL). ✓
- All 17 dataset mappings use catalog dataset types; 0 new dataset types. ✓
- Vocabulary terms match the PRD choices in requirements.json (load level, recording mode, termination reason, ISO 5817 B/C/D, Annex C C63/B90/B125). ✓

## Design remarks

1. **`OPERATOR` on dev1** – the design relies on the inherited `OPERATOR` for the TEST step, but dev1's `EXPERIMENTAL_STEP` lacks it and a
   legacy live `OPERATOR` of unknown data type exists. Verify its data type before provisioning (see collision check).
2. **Operator/date per specimen step lost vs. legacy** – legacy steps 01/02/04/05/06 recorded `OPERATOR`, `INSPECTOR`, `DATE_OF_INSPECTION`,
   `RANDOMIZATION_DATE`; the flat specimen sections have none (not PRD v2 data items, so not a design error). Confirm with the PRD owner that
   this traceability is not needed (otherwise: `FATIGUE.*_DATE`/operator fields or ELN comments).
3. **`EXPERIMENTAL_STEP.WELDMENT_TYPE` on a Sample type** – valid in openBIS (global property types) and reuse-first (Q3), but the
   step-namespaced code on a specimen is semantically odd; long-term a generic weld-type property in bam-masterdata would be cleaner.
   Its label is fixed ("Type of weld").
4. **EXTEND of `WELDING.WELD_TYPE`** changes a list owned by the welding group and also used by `EXPERIMENTAL_STEP.WELDMENT`; the PR needs
   their review. Butt/cruciform are joint geometries (ISO 9692 / ISO 2553 "joint type") rather than weld types like fillet/groove — acceptable
   per decision 2, but worth stating in the PR.
5. **New namespaces** – `WELDING.ISO_5817_*` vocabularies go into `bam_masterdata/datamodel/welding/vocabularies.py`; `FATIGUE.*` is a new
   namespace with no existing module (masterdata-extender must choose the target file).
6. **Prefix** `EXP.MECH.CYC_FAT` follows sibling CreepTest (`EXP.MECH.CREEP`) rather than parent `EXP.MECH_TEST` – consistent with the catalog
   precedent, noted for the PR.
7. **`FATIGUE.SAMPLING_FREQUENCY` INTEGER** (decision 7) although requirements.json listed `real` – excludes non-integer Hz; acceptable for IMC.
8. **BAM_* location vocabularies** are not defined in bam-masterdata (only referenced) – a bam-masterdata-based sync alone will not fix the
   skipped Sample/Instrument/TestingMachine properties on dev1; an admin import of the central BAM vocabularies is required.
9. Design metrics re-checked against design.json content: 2 object types, 6 new + 2 extended vocabularies, 33 new property types
   (21 specimen + 12 test) + 2 reused, 4 objects/specimen, 9 inventory links – all consistent.

## Summary

| Class | Types | Vocabularies | Property types | Dataset types | Collection types | Total |
|---|---|---|---|---|---|---|
| REUSE | 9 object types | 1 (`TESTING_MACHINE_DRIVE_TYPE`; `PHYSICAL_STATE` inherited, not counted) | 2 | 7 | 1 (`COLLECTION`) | **20** |
| EXTEND | 0 | 2 (`WELDING.WELD_TYPE`, `AUXILIARY_MATERIAL_TYPE`; +4 terms) | 0 | 0 | 0 | **2** |
| CREATE | 2 | 6 | 33 | 0 | 0 | **41** |
| LIVE-ONLY | 16 | 6 | (~45 legacy, informative) | 17 | 1 (`TEST_SERIES`) | **40** (all → migrate) |

Metrics (design.json `metrics`):

| Metric | New design | Live legacy (dev1) |
|---|---|---|
| New object types | 2 | 16 |
| New vocabularies | 6 | 6 |
| Extended vocabularies | 2 | 0 |
| New property types | 33 (+2 reused assigned) | n/a (all live-only) |
| New collection types | 0 | 1 |
| New dataset types | 0 | 17 |
| Objects per specimen | 4 | 13 |
| Max link depth | 1 | 12 |
| Step→step links per specimen | 0 | 11 |
| Inventory objects | 9 | – |

Blocking items before provisioning on dev1: (1) bam-masterdata PR for the 2 EXTEND vocabularies + CREATE entities,
(2) create `EXPERIMENTAL_STEP.WELDMENT_TYPE` on dev1, (3) verify live `OPERATOR` data type. Non-blocking: BAM_* Sample
properties are skipped on dev1 until an admin syncs the standard masterdata.
