# Live-Inventur dev1 (read-only)

- Instanz: https://dev1.datastore.bam.de — openBIS 20.10.12.5, V3 API 3.7
- Erhoben: 2026-10-06, über die angemeldete ELN-Sitzung (nur `search*`-Aufrufe, keine Änderungen)
- Umfang: 154 Object-Types, 4 Collection-Types, 43 Dataset-Types, 103 Vokabulare

## 1. Stand gegenüber bam-masterdata (Repo `d7a871b`, 2026-10-05)

| Thema | Repo | dev1 | Konsequenz |
|---|---|---|---|
| `SAMPLE` | 19 Props (inkl. BAM-Standort, Verantwortliche) | 8 Props (alter Stand) | dev1 ist nicht auf aktuellem Masterdata-Stand |
| `EXPERIMENTAL_STEP.MECHANICAL_TEST` (+ `CREEP_TEST`) | vorhanden | **fehlt** | neue Prüf-Schritte können trotzdem angelegt werden (openBIS kennt keine Vererbung, nur Code-Namensräume) |
| `SAMPLE.BUILDING_MATERIALS_SPECIMEN` (FB 7) | vorhanden | fehlt | Muster für „Probe erbt von SAMPLE" |
| Geräte `INSTRUMENT.*` (Kamera, Messverstärker, Lastrahmen, Kraftaufnehmer, …) | vorhanden | vorhanden | REUSE |
| `TESTING_MACHINE`, `AUXILIARY_MATERIAL`, `SOP` | vorhanden | vorhanden | REUSE |
| `WELDING.WELD_TYPE` | 6 Terme | 6 Terme | identisch |

## 2. Bereits live vorhandenes FB-7.2-Modell (nicht in bam-masterdata)

Vermutlich direkt per Admin-Import angelegt (Prefix-Muster `STEP-`, `PROBE-`, `DMS-`, `CONS-`, `INST-`).

### Object-Types
| Code | Props | Bemerkung |
|---|---|---|
| `TEST_SPECIMEN` | ORIGINAL_ID, INTERNAL_DESIGNATION, SHEET_ORIGIN, WELD_GEOMETRY_PROP→WELD_GEOMETRY, ISO_5817_CLASS_PROP→ISO_5817_CLASS, FINAL_DESIGNATION | kein `$NAME`, keine Sektionen |
| `PRE_QUALITY_CHECK` | INSPECTOR, DATE_OF_INSPECTION, GROSS_WELD_DEFECTS, INITIAL_/FINAL_ANGULAR_DISTORTION, INITIAL_/FINAL_EDGE_MISALIGNMENT, WAS_STRAIGHTENED | fachlich reicher als PRD (Werte *nach* dem Richten) |
| `CHAMFERING_GRINDING` | OPERATOR, WELD_MODIFICATIONS | |
| `SPECIMEN_RECORDING` | OPERATOR, USED_INSTRUMENT (SAMPLE) | |
| `WELD_ANALYSIS` | OPERATOR, ANALYSIS_RATING→WELD_ANALYSIS_RATING (C56/B90/B125) | |
| `SERIES_ASSIGNMENT` | OPERATOR, RANDOMIZATION_DATE | |
| `TEST_SETUP_GEOMETRY` | OPERATOR, SPECIMEN_THICKNESS_POS_1_3 (REAL!), AVG_SPECIMEN_THICKNESS, SPECIMEN_WIDTH_POS_1_3 (REAL!), AVG_SPECIMEN_WIDTH | 3 Messwerte in einem REAL-Feld nicht abbildbar |
| `MONITORING_APPLICATION` | OPERATOR, APPLICATION_TIMESTAMP, USED_STRAIN_GAUGE_TYPE, USED_ADHESIVE_TYPE, USED_CRACK_LUMINESCENCE_TYPE, CAMERA_SYSTEM, DMS_DISTANCE_TO_WELD/EDGE | Risslumineszenz + Kamera neu ggü. PRD |
| `AMPLIFIER_TEST_BENCH_SETTINGS` | IMC_MEASUREMENT_AMPLIFIER, SAMPLING_FREQUENCY, DATA_RECORDING_MODE_PROP→DATA_RECORDING_MODE, RECORDED_CHANNELS | |
| `INSTALLATION_STRESS_MEASUREMENT` | OPERATOR, PRE_LOAD_FORCE | |
| `CYCLIC_FATIGUE_TEST` | OPERATOR, MARKER_LOADS_ACTIVE, STOP_REASON_PROP→STOP_REASON, FATIGUE_TEST_BENCH | |
| `DATA_EVALUATION` | OPERATOR, FINAL_GROSS_CYCLES, FINAL_NET_CYCLES, CYCLES_AT_10_PERCENT_SG_DEVIATION | |
| `FRACTURE_SURFACE_ANALYSIS` | OPERATOR, USED_CAMERA, USED_MICROSCOPE | |
| `STRAIN_GAUGE_TYPE`, `CONSUMABLE_TYPE`, `INSTRUMENT_DUMMY` | Katalog-Typen | Doppelung zu `AUXILIARY_MATERIAL` / `INSTRUMENT.*` |

Alle 12 Schritt-Typen zusätzlich mit `STEP_ORDER` (INTEGER) und `STATUS` (→ `STEP_STATUS`), **ohne `$NAME`**,
ohne Sektionen, Labels im Format `"EN / DE"` statt `"EN//DE"`.

### Vokabulare (live-only)
`WELD_GEOMETRY` (BUTT_WELD, CRUCIFORM_WELD) · `ISO_5817_CLASS` (B, C, D) · `WELD_ANALYSIS_RATING` (C56, B90, B125) ·
`STOP_REASON` (TOTAL_FRACTURE, CRACK_DETECTION, DEFINED_CYCLES, MANUAL_STOP) · `DATA_RECORDING_MODE` (FULL_SIGNAL, PEAK_COUNTER, PEAK_VALLEY) ·
`STEP_STATUS` (PLANNED, IN_PROGRESS, DONE)

### Collection-Type / Dataset-Types (live-only)
- `TEST_SERIES` — identische Props wie Standard-`COLLECTION`
- 17 Dataset-Types: REWORK_PROTOCOL, SPECIMEN_PHOTOS, 3D_SCAN_RAW, WELD_ANALYSIS_EVAL, RANDOMIZATION_CODE,
  STRAIN_GAUGE_POSITION_DRAWING, SETUP_PHOTO, BENDING_MOMENT_RAW, RAW_CONVERSION_SCRIPT, LOAD_PROGRAM_EXCEL,
  FATIGUE_MESS_RAW, MONITORING_IMAGES, EVALUATION_PLOTS, CLEANED_DATA_TABULAR, MACRO_FRACTURE_PHOTOS,
  MICROSCOPE_CRACK_IMAGES, BEACH_MARK_EVALUATION_EXCEL — alle auf Standardtypen abbildbar
  (RAW_DATA, PROCESSED_DATA, ANALYZED_DATA, ATTACHMENT, FIGURE, FIGURE.PLOT, SOURCE_CODE, MEASUREMENT_PROTOCOL_FILE)

## 3. Live-Objekte (Ist-Struktur)

```
/FB_72 (Space)
├── /FB_72/CATALOG                    (leer)
└── /FB_72/CYCLIC_FATIGUE_TESTS
    ├── SERIE_1_BUTT_WELD             Collection, 13 Proben S1-0 … S1-12
    ├── SERIE_1_CRUCIFORM_WELD        Collection, leer
    └── Demo-Proben PROBE-DEMO-001_1, PROBE-DEMO-002, RENEW_19_1 (ohne Collection)
/FB_72/S1-n-<STEP>                    156 Schritt-Objekte auf Space-Ebene, OHNE Collection
/MATERIALS/7_2_EQUIPMENT             Instruments (ZEISS GOM ATOS 5, IMC-Verstärker, Luxonis OAK-4D-Pro,
                                      Makro-Kamera, Digitalmikroskop), DMS HBM LY11-6/120, Lastrahmen, Prüfmaschinen-Vorlage
/MATERIALS/7_2_MATERIALS             HBM X60 Klebstoff, MR-Chemie Risslumineszenz-Set
```

**Kettenstruktur:** Probe → Schritt 1 → Schritt 2 → … → Schritt 12, jeweils als Eltern-Kind-Link.
Pro Probe 13 Objekte, **12 Ebenen tief**; 189 Objekte im Space ohne einen einzigen Messwert/Datensatz.

## 4. Nachher (nach Pipeline-Lauf v2, 2026-10-06)

```
/FB_72/WELDED_FATIGUE                 Projekt (neu)
├── WORKFLOW_PLAN                     GENERAL_PROTOCOL (Ablaufplan, Schritt → Ort)
├── SERIES_1_BUTT_WELD                COLLECTION: S1B-01 … S1B-06 + 10 Schritt-Objekte (SCAN/TEST/FRACTURE)
└── SERIES_1_CRUCIFORM_WELD           COLLECTION: S1C-01, S1C-02
/MATERIALS/7_2_EQUIPMENT|7_2_MATERIALS  9 Inventarobjekte mit Standardtypen (INSTRUMENT*, TESTING_MACHINE, AUXILIARY_MATERIAL)
```

- Masterdaten angelegt: 6 Vokabulare, 4 Terme (WELDING.WELD_TYPE, AUXILIARY_MATERIAL_TYPE), 36 Property-Typen,
  2 Objekttypen (`SAMPLE.WELDED_FATIGUE_SPECIMEN`, `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST`)
- Übersprungen (Instanz veraltet): 6 BAM-Standort-Properties, `$ANNOTATIONS_STATE`; Konflikt `DESCRIPTION` (VARCHAR vs. MULTILINE)
- Altbestand: 197 Objekte + 2 Collections im Papierkorb (Einträge 7, 8); Rest siehe `generated/welded_fatigue_v2/CLEANUP_dev1.md`
