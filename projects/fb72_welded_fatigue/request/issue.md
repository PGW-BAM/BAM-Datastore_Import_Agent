<!-- Title: Masterdata request: S-N tests on welded joints -->
<!-- Repository: https://github.com/BAMresearch/bam-masterdata/issues · suggested label: semver:minor (new entity types) -->

## Summary

FB 7.2 documents S-N tests on welded joints in the BAM Data Store. This needs **2 new object types**, **6 new vocabularies**, **33 new property types** and **4 additional terms** in existing vocabularies. Everything else reuses bam-masterdata v0.17.0 (`datamodel/v0`) as it is.

Contribution: Python modules (ready for a PR, attached) and `masterdata.xlsx` (attached).

## Why

Cyclic fatigue tests (S-N curves) on welded specimens (butt and cruciform welds). Each specimen must be traceable from the incoming inspection to the fracture surface, every series must show which specimen is in which workflow step, and the data must be machine-readable (S-N curve from the series table, parser for the measurement raw data).

## New object types

| Code | Name (EN / DE) | Parent (v0) | Fields (new) | Covers workflow steps |
|---|---|---|---|---|
| `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | Cyclic fatigue test / Zyklischer Ermüdungsversuch | `MechanicalTest` | 26 (12) | 07, 08, 09, 10, 11 |
| `SAMPLE.WELDED_FATIGUE_SPECIMEN` | Welded fatigue specimen / Geschweißte Ermüdungsprobe | `Sample` | 42 (21) | subject, 01, 02, 04, 05, 06 |

## New property types

| Code | Label (EN) | Label (DE) | Type | Section | On type | Source |
|---|---|---|---|---|---|---|
| `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_WELD_TOE` | Strain gauge distance to weld toe [mm] | DMS-Abstand zum Nahtübergang [mm] | REAL | Strain Gauge Application | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 07 |
| `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_EDGE` | Strain gauge distance to edge [mm] | DMS-Abstand zum Probenrand [mm] | REAL | Strain Gauge Application | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 07 |
| `FATIGUE.STRAIN_GAUGE_APPLICATION_TIME` | Time of strain gauge application | Zeitpunkt der DMS-Applikation | TIMESTAMP | Strain Gauge Application | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 07 |
| `FATIGUE.SAMPLING_FREQUENCY` | Sampling frequency [Hz] | Abtastfrequenz [Hz] | INTEGER | Measuring Amplifier And Test Rig | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 08 (INTEGER per decision 7; requirements.json had 'real') |
| `FATIGUE.RECORDING_MODE` | Recording mode | Aufzeichnungsmodus | CONTROLLEDVOCABULARY → `FATIGUE.RECORDING_MODE` | Measuring Amplifier And Test Rig | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 08 |
| `FATIGUE.RECORDED_CHANNELS` | Recorded channels | Erfasste Kanäle | VARCHAR | Measuring Amplifier And Test Rig | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 08 |
| `FATIGUE.PRELOAD_FORCE` | Preload force [kN] | Vorspannkraft [kN] | REAL | Installation Stress | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 09 |
| `FATIGUE.BEACH_MARKS_ACTIVE` | Beach marks (marker loads) active | Rastlinien (Markerlasten) aktiv | BOOLEAN | Cyclic Fatigue Test | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 10 |
| `FATIGUE.TERMINATION_REASON` | Termination reason | Abbruchgrund | CONTROLLEDVOCABULARY → `FATIGUE.TERMINATION_REASON` | Cyclic Fatigue Test | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 10 |
| `FATIGUE.CYCLES_GROSS` | Gross number of cycles | Bruttoschwingspielzahl | INTEGER | Evaluation | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 11 |
| `FATIGUE.CYCLES_NET` | Net number of cycles | Nettoschwingspielzahl | INTEGER | Evaluation | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 11 |
| `FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP` | Cycles to 10 % strain gauge drop per strain gauge | Zyklen bis 10 % DMS-Abfall je DMS | MULTILINE_VARCHAR | Evaluation | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | PRD §3 step 11 (kind text) |
| `FATIGUE.NEXT_STEP` | Next step | Nächster Schritt | CONTROLLEDVOCABULARY → `WELDED_FATIGUE_WORKFLOW_STEP` | Workflow Status | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §2 P5 / domain_decisions 'next step field' (principle-required, not a PRD data item) |
| `FATIGUE.MANUFACTURER_DESIGNATION` | Manufacturer designation (original ID) | Herstellerbezeichnung (Original-ID) | VARCHAR | Specimen Identification | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §4 subject |
| `FATIGUE.SOURCE_SHEET` | Source sheet | Herkunftsblech | VARCHAR | Specimen Identification | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §4 subject + §3 step 05 (same data item, placed once) |
| `FATIGUE.TARGET_QUALITY_LEVEL` | Target quality level (ISO 5817) | Angestrebte Bewertungsgruppe (ISO 5817) | CONTROLLEDVOCABULARY → `WELDING.ISO_5817_QUALITY_LEVEL` | Specimen Identification | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §4 subject |
| `FATIGUE.INITIAL_ANGULAR_DISTORTION` | Initial angular distortion [°] | Winkelverzug initial [°] | REAL | Initial Quality Check | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 01 |
| `FATIGUE.INITIAL_EDGE_MISALIGNMENT` | Initial edge misalignment [mm] | Kantenversatz initial [mm] | REAL | Initial Quality Check | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 01 |
| `FATIGUE.WAS_STRAIGHTENED` | Was straightened | Wurde gerichtet | BOOLEAN | Initial Quality Check | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 01 |
| `FATIGUE.ANGULAR_DISTORTION_AFTER_STRAIGHTENING` | Angular distortion after straightening [°] | Winkelverzug nach dem Richten [°] | REAL | Initial Quality Check | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 01 |
| `FATIGUE.EDGE_MISALIGNMENT_AFTER_STRAIGHTENING` | Edge misalignment after straightening [mm] | Kantenversatz nach dem Richten [mm] | REAL | Initial Quality Check | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 01 |
| `FATIGUE.WELD_POST_TREATMENT_NOTES` | Weld reinforcement treatment / grinding notes | Nahtüberhöhungs-Bearbeitung / Schleifhinweise | MULTILINE_VARCHAR | Chamfering And Grinding | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 02 |
| `FATIGUE.ISO_5817_ANNEX_C_RATING` | Quality level ISO 5817 Annex C | Bewertungsgruppe ISO 5817 Anhang C | CONTROLLEDVOCABULARY → `WELDING.ISO_5817_ANNEX_C_RATING` | Weld Analysis | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 04 |
| `FATIGUE.LOAD_LEVEL` | Load level | Lastniveau | CONTROLLEDVOCABULARY → `FATIGUE.LOAD_LEVEL` | Series Assignment | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 05 |
| `FATIGUE.TEST_ORDER` | Test order | Prüfreihenfolge | INTEGER | Series Assignment | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 05 (INTEGER per decision 7) |
| `FATIGUE.THICKNESS_POS_1` | Thickness position 1 [mm] | Dicke Position 1 [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 (repeat 3) |
| `FATIGUE.THICKNESS_POS_2` | Thickness position 2 [mm] | Dicke Position 2 [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 (repeat 3) |
| `FATIGUE.THICKNESS_POS_3` | Thickness position 3 [mm] | Dicke Position 3 [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 (repeat 3) |
| `FATIGUE.WIDTH_POS_1` | Width position 1 [mm] | Breite Position 1 [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 (repeat 3) |
| `FATIGUE.WIDTH_POS_2` | Width position 2 [mm] | Breite Position 2 [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 (repeat 3) |
| `FATIGUE.WIDTH_POS_3` | Width position 3 [mm] | Breite Position 3 [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 (repeat 3) |
| `FATIGUE.MEAN_THICKNESS` | Mean thickness [mm] | Mittlere Dicke [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 |
| `FATIGUE.MEAN_WIDTH` | Mean width [mm] | Mittlere Breite [mm] | REAL | Geometry Before Installation | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | PRD §3 step 06 |

## New vocabularies

- `FATIGUE.LOAD_LEVEL`: Load level of a specimen within a fatigue test series / Lastniveau einer Probe innerhalb einer Ermüdungsprüfserie. Terms: `HIGH` High / Hoch, `MEDIUM` Medium / Mittel, `LOW` Low / Niedrig
- `FATIGUE.RECORDING_MODE`: Data recording mode of the measuring amplifier in fatigue tests / Aufzeichnungsmodus des Messverstärkers in Ermüdungsversuchen. Terms: `FULL_SIGNAL` Full signal / Vollsignal, `PEAK_COUNTER` Peak counter / Peak-Counter, `PEAK_VALLEY` Peak-valley / Peak-Valley
- `FATIGUE.TERMINATION_REASON`: Reason for terminating a fatigue test / Grund für den Abbruch eines Ermüdungsversuchs. Terms: `TOTAL_FRACTURE` Total fracture / Totalbruch, `CRACK_DETECTED` Crack detected / Riss detektiert, `RUN_OUT` Run-out / Durchläufer, `MANUAL_STOP` Manual stop / Manueller Stopp
- `WELDING.ISO_5817_ANNEX_C_RATING`: Quality levels for fatigue-loaded structures according to ISO 5817 Annex C / Bewertungsgruppen für schwingend beanspruchte Konstruktionen nach ISO 5817 Anhang C. Terms: `C63` C63, `B90` B90, `B125` B125 (ref: decision 3 (C63, not legacy C56))
- `WELDING.ISO_5817_QUALITY_LEVEL`: Quality levels for imperfections according to ISO 5817 / Bewertungsgruppen für Unregelmäßigkeiten nach ISO 5817. Terms: `B` B, `C` C, `D` D (ref: decision 3)
- `WELDED_FATIGUE_WORKFLOW_STEP`: Ordered workflow steps of the welded fatigue test programme / Geordnete Ablaufschritte des Schweißnaht-Ermüdungsprogramms. Terms: `S01_PRE_QUALITY_CHECK` 01 Pre-quality check / 01 Vorqualitätsprüfung, `S02_CHAMFERING_GRINDING` 02 Chamfering / grinding / 02 Anfasen / Schleifen, `S03_3D_SCAN` 03 3D scan / 03 3D-Scan, `S04_WELD_ANALYSIS` 04 Weld analysis / 04 Nahtanalyse, `S05_SERIES_ASSIGNMENT` 05 Series assignment / 05 Serienzuordnung, `S06_GEOMETRY_BEFORE_INSTALLATION` 06 Geometry before installation / 06 Geometrie vor Einbau, `S07_STRAIN_GAUGE_APPLICATION` 07 Strain gauge application / 07 DMS-Applikation, `S08_MEASURING_AMPLIFIER_TEST_RIG` 08 Measuring amplifier / test rig / 08 Messverstärker / Prüfstand, `S09_INSTALLATION_STRESS` 09 Installation stress / 09 Einbaubeanspruchung, `S10_CYCLIC_FATIGUE_TEST` 10 Cyclic fatigue test / 10 Zyklischer Ermüdungsversuch, `S11_EVALUATION` 11 Evaluation / 11 Auswertung, `S12_FRACTURE_SURFACE_ANALYSIS` 12 Fracture surface analysis / 12 Bruchflächenanalyse, `DONE` Done / Abgeschlossen (ref: decision 9; PRD §2 P5)

## Additions to existing vocabularies

| Vocabulary | Defined at | New terms (EN / DE) |
|---|---|---|
| `WELDING.WELD_TYPE` | `bam_masterdata/datamodel/welding/vocabularies.py:38` | `WELDING_BUTT_WELD` butt weld / Stumpfstoß, `WELDING_CRUCIFORM_WELD` cruciform weld / Kreuzstoß |
| `AUXILIARY_MATERIAL_TYPE` | `bam_masterdata/datamodel/vocabulary_types.py:252` | `STRAIN_GAUGE` Strain gauge / Dehnungsmessstreifen (DMS), `CRACK_DETECTION_AGENT` Crack detection agent / Rissprüfmittel |

## Instance sync only (no PR needed)

To be determined: `https://playground.datastore.bam.de` has not been read yet.

## Checks

- `bam_masterdata checker --mode individual`: 0 errors, 3 warnings (all inherited from the standard itself)
- import test with bam-masterdata v0.17.0: passed
- German names via `property_label_de` / `label_de` (written to openBIS as `English//Deutsch`); sections in Title Case
