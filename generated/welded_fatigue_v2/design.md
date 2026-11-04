# Structure design - welded_fatigue_v2

- Requirements: `generated/welded_fatigue_v2/requirements.json` - Catalog: bam-masterdata `d7a871be` (2026-10-05 13:43:38 +0200) - Live: `generated/live/dev1_inventory.md`
- Designed: 2026-10-06 by structure-designer. Machine-readable: `design.json`. Classification REUSE/EXTEND/CREATE is left to gap-analyzer.

## 1. Tree

```
/FB_72 (Space)
└── /FB_72/WELDED_FATIGUE (Project)
    ├── WORKFLOW_PLAN                     SOP  (step -> location table)
    ├── SERIES_1_BUTT_WELD                COLLECTION  ($DEFAULT_OBJECT_TYPE = SAMPLE.WELDED_FATIGUE_SPECIMEN)
    │   ├── S1B-01                        SAMPLE.WELDED_FATIGUE_SPECIMEN   (subject, 01, 02, 04, 05, 06, Next step)
    │   │   ├── S1B-01-SCAN               EXPERIMENTAL_STEP                (03-04)  <- parent: ZEISS GOM ATOS 5
    │   │   ├── S1B-01-TEST               ...MECHANICAL_TEST.CYCLIC_FATIGUE_TEST (07-11)
    │   │   │                             <- parents: strain gauge, adhesive, crack-lum. set,
    │   │   │                                Luxonis camera, IMC amplifier, servo-hydraulic machine
    │   │   └── S1B-01-FRACTURE           EXPERIMENTAL_STEP                (12)     <- parents: macro camera, digital microscope
    │   └── S1B-02 ... (same pattern)
    └── SERIES_1_CRUCIFORM_WELD           COLLECTION  (same pattern: S1C-01, S1C-01-SCAN/-TEST/-FRACTURE, ...)
/MATERIALS (inventory, created once)
    INSTRUMENT: ZEISS GOM ATOS 5, Digital microscope   (caliper: SOP text only)
    INSTRUMENT.CAMERA: Luxonis OAK-4D-Pro, Macro camera
    INSTRUMENT.MEASURING_AMPLIFIER: IMC  ·  TESTING_MACHINE: servo-hydraulic
    AUXILIARY_MATERIAL: HBM LY11-6/120 (STRAIN_GAUGE), HBM X60 (ADHESIVE), MR Chemie set (CRACK_DETECTION_AGENT)
```
All step objects are children of the specimen only (depth 1), live in the series collection, no step->step links.

## 2. Step -> location

| No | Step | Object | Section | Data items (property codes) | Equipment | Files |
|---|---|---|---|---|---|---|
| 00 | Subject (identity) | specimen | General Information + Specimen Identification | $NAME (final series designation), ALIAS (internal designation, inherited), FATIGUE.MANUFACTURER_DESIGNATION, FATIGUE.SOURCE_SHEET, EXPERIMENTAL_STEP.WELDMENT_TYPE, FATIGUE.TARGET_QUALITY_LEVEL | - | - |
| 01 | Pre-quality check of the weld | specimen | Initial Quality Check | FATIGUE.INITIAL_ANGULAR_DISTORTION, FATIGUE.INITIAL_EDGE_MISALIGNMENT, FATIGUE.WAS_STRAIGHTENED, FATIGUE.ANGULAR_DISTORTION_AFTER_STRAIGHTENING, FATIGUE.EDGE_MISALIGNMENT_AFTER_STRAIGHTENING, DEFECT_DESCRIPTION | - | Specimen photos |
| 02 | Chamfering / grinding | specimen | Chamfering And Grinding | FATIGUE.WELD_POST_TREATMENT_NOTES | - | Post-processing report |
| 03 | 3D scan of the specimen | S1B-01-SCAN (EXPERIMENTAL_STEP) | - | - | ZEISS GOM ATOS 5 (parent) | 3D scan raw data |
| 04 | Weld analysis (GOM) | specimen (rating) + S1B-01-SCAN (files) | Weld Analysis | FATIGUE.ISO_5817_ANNEX_C_RATING | GOM software (text in SCAN step) | Evaluation export |
| 05 | Series assignment (randomisation) | specimen + collection membership | Series Assignment | FATIGUE.LOAD_LEVEL, FATIGUE.TEST_ORDER, 'Assignment to test series' = specimen placed in the series collection (no property), 'Source sheet (bias avoidance)' = FATIGUE.SOURCE_SHEET (placed once, Specimen Identification) | - | Randomisation script (collection) |
| 06 | Geometry before installation | specimen | Geometry Before Installation | FATIGUE.THICKNESS_POS_1, FATIGUE.THICKNESS_POS_2, FATIGUE.THICKNESS_POS_3, FATIGUE.WIDTH_POS_1, FATIGUE.WIDTH_POS_2, FATIGUE.WIDTH_POS_3, FATIGUE.MEAN_THICKNESS, FATIGUE.MEAN_WIDTH | Caliper (no inventory object/link; named in SOP only) | - |
| 07 | Strain gauge application | S1B-01-TEST | Strain Gauge Application | FATIGUE.STRAIN_GAUGE_DISTANCE_TO_WELD_TOE, FATIGUE.STRAIN_GAUGE_DISTANCE_TO_EDGE, FATIGUE.STRAIN_GAUGE_APPLICATION_TIME | Strain gauge, Adhesive, Crack luminescence set, Luxonis OAK-4D-Pro | Strain gauge position drawing, Setup photo |
| 08 | Measuring amplifier / test rig | S1B-01-TEST | Measuring Amplifier And Test Rig | FATIGUE.SAMPLING_FREQUENCY, FATIGUE.RECORDING_MODE, FATIGUE.RECORDED_CHANNELS | IMC measuring amplifier, Servo-hydraulic testing machine | - |
| 09 | Installation stress | S1B-01-TEST | Installation Stress | FATIGUE.PRELOAD_FORCE | IMC measuring amplifier (same link as 08) | Bending moment raw data |
| 10 | Cyclic fatigue test | S1B-01-TEST | Cyclic Fatigue Test | FATIGUE.BEACH_MARKS_ACTIVE, FATIGUE.TERMINATION_REASON | Servo-hydraulic testing machine (same link as 08) | Load programme, Measurement raw data, Monitoring images |
| 11 | Evaluation | S1B-01-TEST | Evaluation | FATIGUE.CYCLES_GROSS, FATIGUE.CYCLES_NET, FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP | - | Cleaned measurement data, Evaluation plots, Conversion script |
| 12 | Fracture surface analysis | S1B-01-FRACTURE (EXPERIMENTAL_STEP) | - | - | Macro camera, Digital microscope | Macro photos, Microscope images of crack origin, Beach-mark evaluation |
| P5 | Workflow Status | specimen | Workflow Status | FATIGUE.NEXT_STEP | - | - |

## 3.1 `SAMPLE.WELDED_FATIGUE_SPECIMEN` (WeldedFatigueSpecimen, inherits `Sample` - bam_masterdata/datamodel/object_types.py:3005, prefix `SAM.WFS`)

Section order: Workflow Status > General Information > Specimen Identification > Initial Quality Check > Chamfering And Grinding > Weld Analysis > Series Assignment > Geometry Before Installation > Properties > BAM Information > Additional Information > Comments

- Inherited, not duplicated: `$NAME` - The series designation (e.g. 'S1B-01') is the specimen's display name; no new property.
- Inherited, not duplicated: `ALIAS` - Inherited Sample property 'Alternative Name' holds the internal BAM designation (resolution Q4); no new property.

| Section | Code | Type | Label | Vocabulary | Reuse |
|---|---|---|---|---|---|
| Workflow Status | `FATIGUE.NEXT_STEP` | CONTROLLEDVOCABULARY | Next step | WELDED_FATIGUE_WORKFLOW_STEP | new |
| Specimen Identification | `FATIGUE.MANUFACTURER_DESIGNATION` | VARCHAR | Manufacturer designation (original ID) |  | new |
| Specimen Identification | `FATIGUE.SOURCE_SHEET` | VARCHAR | Source sheet |  | new |
| Specimen Identification | `EXPERIMENTAL_STEP.WELDMENT_TYPE` | CONTROLLEDVOCABULARY | Type of weld | WELDING.WELD_TYPE | yes - EXPERIMENTAL_STEP.WELDMENT_TYPE (Weldment, bam_masterdata/datamodel/welding/object_types.py:409) |
| Specimen Identification | `FATIGUE.TARGET_QUALITY_LEVEL` | CONTROLLEDVOCABULARY | Target quality level (ISO 5817) | WELDING.ISO_5817_QUALITY_LEVEL | new |
| Initial Quality Check | `FATIGUE.INITIAL_ANGULAR_DISTORTION` | REAL | Initial angular distortion [°] |  | new |
| Initial Quality Check | `FATIGUE.INITIAL_EDGE_MISALIGNMENT` | REAL | Initial edge misalignment [mm] |  | new |
| Initial Quality Check | `FATIGUE.WAS_STRAIGHTENED` | BOOLEAN | Was straightened |  | new |
| Initial Quality Check | `FATIGUE.ANGULAR_DISTORTION_AFTER_STRAIGHTENING` | REAL | Angular distortion after straightening [°] |  | new |
| Initial Quality Check | `FATIGUE.EDGE_MISALIGNMENT_AFTER_STRAIGHTENING` | REAL | Edge misalignment after straightening [mm] |  | new |
| Initial Quality Check | `DEFECT_DESCRIPTION` | MULTILINE_VARCHAR | Defect description |  | yes - DEFECT_DESCRIPTION (Named, bam_masterdata/datamodel/object_types.py:7429) |
| Chamfering And Grinding | `FATIGUE.WELD_POST_TREATMENT_NOTES` | MULTILINE_VARCHAR | Weld reinforcement treatment / grinding notes |  | new |
| Weld Analysis | `FATIGUE.ISO_5817_ANNEX_C_RATING` | CONTROLLEDVOCABULARY | Quality level ISO 5817 Annex C | WELDING.ISO_5817_ANNEX_C_RATING | new |
| Series Assignment | `FATIGUE.LOAD_LEVEL` | CONTROLLEDVOCABULARY | Load level | FATIGUE.LOAD_LEVEL | new |
| Series Assignment | `FATIGUE.TEST_ORDER` | INTEGER | Test order |  | new |
| Geometry Before Installation | `FATIGUE.THICKNESS_POS_1` | REAL | Thickness position 1 [mm] |  | new |
| Geometry Before Installation | `FATIGUE.THICKNESS_POS_2` | REAL | Thickness position 2 [mm] |  | new |
| Geometry Before Installation | `FATIGUE.THICKNESS_POS_3` | REAL | Thickness position 3 [mm] |  | new |
| Geometry Before Installation | `FATIGUE.WIDTH_POS_1` | REAL | Width position 1 [mm] |  | new |
| Geometry Before Installation | `FATIGUE.WIDTH_POS_2` | REAL | Width position 2 [mm] |  | new |
| Geometry Before Installation | `FATIGUE.WIDTH_POS_3` | REAL | Width position 3 [mm] |  | new |
| Geometry Before Installation | `FATIGUE.MEAN_THICKNESS` | REAL | Mean thickness [mm] |  | new |
| Geometry Before Installation | `FATIGUE.MEAN_WIDTH` | REAL | Mean width [mm] |  | new |

- `FATIGUE.MANUFACTURER_DESIGNATION`: Internal designation uses the inherited ALIAS (resolution Q4), so the manufacturer ID gets its own property.
- `EXPERIMENTAL_STEP.WELDMENT_TYPE`: Existing PropertyType bound to WELDING.WELD_TYPE (decision 2); label/description are fixed by the PropertyType. Kept reuse-first (resolution Q3).
- `DEFECT_DESCRIPTION`: Free-text description of gross weld defects; data type and meaning match the existing PropertyType.

## 3.2 `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` (CyclicFatigueTest, inherits `MechanicalTest` - bam_masterdata/datamodel/activities.py:2196, prefix `EXP.MECH.CYC_FAT`)

Section order: General Information > Strain Gauge Application > Measuring Amplifier And Test Rig > Installation Stress > Cyclic Fatigue Test > Evaluation > Experimental Details > References > Additional Information > Comments

- Inherited, not duplicated: `OPERATOR / START_DATE / END_DATE / FINISHED_FLAG / NOTES` - Provided by ExperimentalStep; used as-is for the whole 07-11 session. Not mapped to any PRD data item.

| Section | Code | Type | Label | Vocabulary | Reuse |
|---|---|---|---|---|---|
| Strain Gauge Application | `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_WELD_TOE` | REAL | Strain gauge distance to weld toe [mm] |  | new |
| Strain Gauge Application | `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_EDGE` | REAL | Strain gauge distance to edge [mm] |  | new |
| Strain Gauge Application | `FATIGUE.STRAIN_GAUGE_APPLICATION_TIME` | TIMESTAMP | Time of strain gauge application |  | new |
| Measuring Amplifier And Test Rig | `FATIGUE.SAMPLING_FREQUENCY` | INTEGER | Sampling frequency [Hz] |  | new |
| Measuring Amplifier And Test Rig | `FATIGUE.RECORDING_MODE` | CONTROLLEDVOCABULARY | Recording mode | FATIGUE.RECORDING_MODE | new |
| Measuring Amplifier And Test Rig | `FATIGUE.RECORDED_CHANNELS` | VARCHAR | Recorded channels |  | new |
| Installation Stress | `FATIGUE.PRELOAD_FORCE` | REAL | Preload force [kN] |  | new |
| Cyclic Fatigue Test | `FATIGUE.BEACH_MARKS_ACTIVE` | BOOLEAN | Beach marks (marker loads) active |  | new |
| Cyclic Fatigue Test | `FATIGUE.TERMINATION_REASON` | CONTROLLEDVOCABULARY | Termination reason | FATIGUE.TERMINATION_REASON | new |
| Evaluation | `FATIGUE.CYCLES_GROSS` | INTEGER | Gross number of cycles |  | new |
| Evaluation | `FATIGUE.CYCLES_NET` | INTEGER | Net number of cycles |  | new |
| Evaluation | `FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP` | MULTILINE_VARCHAR | Cycles to 10 % strain gauge drop per strain gauge |  | new |

- `FATIGUE.STRAIN_GAUGE_APPLICATION_TIME`: START_DATE (inherited) not reused: it spans the whole merged object 07-11 and is reserved for the step start (parser of steps 10/11 may fill START_DATE/END_DATE from IMC raw data); the application time matters on its own (adhesive curing).
- `FATIGUE.PRELOAD_FORCE`: CREEP_TEST_PRELOAD (CreepTest) not reused: creep-test domain code without fixed unit.
- `FATIGUE.TERMINATION_REASON`: CREEP_TEST_END_OF_TEST_CRITERIUM terms do not cover the choices.
- `FATIGUE.CYCLES_GROSS`: FINAL_CYCLES (FcgStep) is REAL - data type mismatch.

## 4. Vocabularies

| Code | Status | Terms |
|---|---|---|
| `WELDED_FATIGUE_WORKFLOW_STEP` | new | S01_PRE_QUALITY_CHECK, S02_CHAMFERING_GRINDING, S03_3D_SCAN, S04_WELD_ANALYSIS, S05_SERIES_ASSIGNMENT, S06_GEOMETRY_BEFORE_INSTALLATION, S07_STRAIN_GAUGE_APPLICATION, S08_MEASURING_AMPLIFIER_TEST_RIG, S09_INSTALLATION_STRESS, S10_CYCLIC_FATIGUE_TEST, S11_EVALUATION, S12_FRACTURE_SURFACE_ANALYSIS, DONE |
| `WELDING.ISO_5817_QUALITY_LEVEL` | new | B, C, D |
| `WELDING.ISO_5817_ANNEX_C_RATING` | new | C63, B90, B125 |
| `FATIGUE.LOAD_LEVEL` | new | HIGH, MEDIUM, LOW |
| `FATIGUE.RECORDING_MODE` | new | FULL_SIGNAL, PEAK_COUNTER, PEAK_VALLEY |
| `FATIGUE.TERMINATION_REASON` | new | TOTAL_FRACTURE, CRACK_DETECTED, RUN_OUT, MANUAL_STOP |
| `WELDING.WELD_TYPE` | extend existing (bam_masterdata/datamodel/welding/vocabularies.py:38) | WELDING_BUTT_WELD, WELDING_CRUCIFORM_WELD |
| `AUXILIARY_MATERIAL_TYPE` | extend existing (bam_masterdata/datamodel/vocabulary_types.py:252) | STRAIN_GAUGE, CRACK_DETECTION_AGENT |

ISO 5817: **two vocabularies** - Two vocabularies instead of one: target level (B/C/D) and Annex C rating (C63/B90/B125) are different value domains; one shared list would allow invalid values on each property (e.g. target 'B125', rating 'D') and makes the series table ambiguous. WELDING. namespace because both are generic welding-standard lists (like WELDING.WELD_TYPE) and avoid the live-only codes ISO_5817_CLASS / WELD_ANALYSIS_RATING.

## 5. Inventory links (parents of steps)

| Inventory object | Type | Parent of | Steps | Note |
|---|---|---|---|---|
| ZEISS GOM ATOS 5 | `INSTRUMENT` | SCAN step | 03 |  |
| Strain gauge HBM LY11-6/120//DMS HBM LY11-6/120 | `AUXILIARY_MATERIAL` | TEST step | 07 | AUXILIARY_MATERIAL_TYPE=STRAIN_GAUGE (new term) |
| Adhesive HBM X60//Klebstoff HBM X60 | `AUXILIARY_MATERIAL` | TEST step | 07 | AUXILIARY_MATERIAL_TYPE=ADHESIVE (existing) |
| Crack luminescence set (MR Chemie)//Risslumineszenz-Set (MR Chemie) | `AUXILIARY_MATERIAL` | TEST step | 07 | AUXILIARY_MATERIAL_TYPE=CRACK_DETECTION_AGENT (new term) |
| Camera system Luxonis OAK-4D-Pro//Kamerasystem Luxonis OAK-4D-Pro | `INSTRUMENT.CAMERA` | TEST step | 07 |  |
| IMC measuring amplifier//IMC-Messverstärker | `INSTRUMENT.MEASURING_AMPLIFIER` | TEST step | 08, 09 |  |
| Servo-hydraulic testing machine//Servohydraulische Prüfmaschine | `TESTING_MACHINE` | TEST step | 08, 10 | TESTING_MACHINE_DRIVE_TYPE=SERVOHYDRAULIC (existing) |
| Macro camera//Makro-Kamera | `INSTRUMENT.CAMERA` | FRACTURE step | 12 |  |
| Digital microscope//Digitalmikroskop | `INSTRUMENT` | FRACTURE step | 12 |  |
| GOM software//GOM-Software | - (not inventory) | text in SCAN step | 04 | decision 5 |
| Caliper//Messschieber | - (not inventory) | - (SOP / step 06 text) | 06 | resolution Q5 |

## 6. Files -> datasets (standard types only)

| Step | File | Attach to | Dataset type |
|---|---|---|---|
| 01 | Specimen photos//Probenfotos | specimen | `RAW_DATA` |
| 02 | Post-processing report//Nachbearbeitungsprotokoll (PDF) | specimen | `ATTACHMENT` |
| 03 | 3D scan raw data//3D-Scan-Rohdaten | SCAN step | `RAW_DATA` |
| 04 | Evaluation export//Auswerte-Export | SCAN step | `ANALYZED_DATA` |
| 05 | Randomisation script//Randomisierungs-Skript | collection | `SOURCE_CODE` |
| 07 | Strain gauge position drawing//DMS-Positionszeichnung | TEST step | `ATTACHMENT` |
| 07 | Setup photo//Aufbaufoto | TEST step | `RAW_DATA` |
| 09 | Bending moment raw data//Biegemoment-Rohdaten (IMC .raw) | TEST step | `RAW_DATA` |
| 10 | Load programme//Lastprogramm (Excel) | TEST step | `MEASUREMENT_PROTOCOL_FILE` |
| 10 | Measurement raw data//Mess-Rohdaten (IMC .raw) | TEST step | `RAW_DATA` |
| 10 | Monitoring images (time-lapse)//Monitoring-Bilder (Zeitraffer) | TEST step | `RAW_DATA` |
| 11 | Cleaned measurement data//Bereinigte Messdaten (CSV/HDF5) | TEST step | `PROCESSED_DATA` |
| 11 | Evaluation plots//Auswerteplots | TEST step | `FIGURE.PLOT` |
| 11 | Conversion script//Konvertierungsskript | TEST step | `SOURCE_CODE` |
| 12 | Macro photos//Makrofotos | FRACTURE step | `RAW_DATA` |
| 12 | Microscope images of crack origin//Mikroskopbilder Rissausgang | FRACTURE step | `RAW_DATA` |
| 12 | Beach-mark evaluation//Rastlinien-Auswertung (Excel) | FRACTURE step | `ANALYZED_DATA` |

## 7. Series table (collection view)

| Column | Source |
|---|---|
| Series designation//Serienbezeichnung | specimen $NAME |
| Weld geometry//Nahtgeometrie | specimen EXPERIMENTAL_STEP.WELDMENT_TYPE |
| Load level//Lastniveau | specimen FATIGUE.LOAD_LEVEL |
| Test order//Prüfreihenfolge | specimen FATIGUE.TEST_ORDER |
| Quality level//Bewertungsgruppe | specimen FATIGUE.ISO_5817_ANNEX_C_RATING (+ FATIGUE.TARGET_QUALITY_LEVEL as extra column) |
| Next step//Nächster Schritt | specimen FATIGUE.NEXT_STEP |
| Number of cycles//Schwingspielzahl | TEST step FATIGUE.CYCLES_GROSS / FATIGUE.CYCLES_NET (TEST objects live in the same collection) |
| Termination reason//Abbruchgrund | TEST step FATIGUE.TERMINATION_REASON |

Collection table column order (`series_table_columns`): `$NAME`, `EXPERIMENTAL_STEP.WELDMENT_TYPE`, `FATIGUE.LOAD_LEVEL`, `FATIGUE.TEST_ORDER`, `FATIGUE.ISO_5817_ANNEX_C_RATING`, `FATIGUE.TARGET_QUALITY_LEVEL`, `FATIGUE.NEXT_STEP`, `FATIGUE.CYCLES_GROSS`, `FATIGUE.CYCLES_NET`, `FATIGUE.TERMINATION_REASON`

## 8. Metrics

| Metric | New design | Live legacy (dev1) |
|---|---|---|
| New object types | 2 | 16 |
| New vocabularies | 6 | 6 |
| Extended vocabularies | 2 | 0 |
| New collection types | 0 | 1 |
| New dataset types | 0 | 17 |
| Objects per specimen | 4 | 13 |
| Max link depth | 1 | 12 |
| Step->step links per specimen | 0 | 11 |
| New property types | 33 (+2 existing assigned) | n/a (all live-only, no $NAME, labels 'EN / DE') |

## 9. Unplaced

None - every data item, equipment item and file of requirements.json has exactly one location.

## 10. Open questions

None open. Resolved by the coordinator (2026-10-06):

- Q1 codes: S1B-NN (butt) / S1C-NN (cruciform), steps <specimen>-SCAN/-TEST/-FRACTURE.
- Q2 WELDING.WELD_TYPE terms: WELDING_BUTT_WELD, WELDING_CRUCIFORM_WELD (existing prefix convention).
- Q3 weld geometry: reuse EXPERIMENTAL_STEP.WELDMENT_TYPE.
- Q4 internal designation: inherited ALIAS; FATIGUE.INTERNAL_DESIGNATION dropped.
- Q5 caliper: no inventory object, no parent link; SOP/step_location_map only.
- Q6 series table: Annex C rating main column, target quality level additional column.
- Q7 cycles to 10 % strain gauge drop: MULTILINE_VARCHAR text.
- Q8 dev1 has project samples enabled: SOP WORKFLOW_PLAN at project level.


## Änderung 2026-11-04: Variante E (◆ B „B freigegeben (Variante E)“)

Die vier Objekte je Probe bilden eine **Prozesslinie**: Probe → 3D-Scan & Nahtanalyse → Zyklischer Ermüdungsversuch →
Bruchflächenanalyse (Eltern → Kind). Die sechs Geräte und Hilfsstoffe des Ermüdungsversuchs sind **Link-Felder**
(Typ OBJECT) statt Eltern: `FATIGUE.STRAIN_GAUGE`, `FATIGUE.STRAIN_GAUGE_ADHESIVE`, `FATIGUE.CRACK_DETECTION_AGENT`,
`FATIGUE.MONITORING_CAMERA`, `FATIGUE.MEASURING_AMPLIFIER` (neu) und `INSTRUMENT` (Standard, Prüfmaschine).
3D-Scan und Bruchflächenanalyse bleiben Standard-`EXPERIMENTAL_STEP` ohne Link-Feld; Scanner, Makro-Kamera und
Mikroskop bleiben dort Eltern. Muster und Quellen: `workflow/strukturmuster.md`. Die Tabellen oben beschreiben noch
Variante A, soweit sie Eltern-Verknüpfungen nennen; maßgeblich ist `design.json`.
