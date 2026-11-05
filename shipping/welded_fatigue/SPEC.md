# Masterdata Specification — Welded Fatigue (FB 7.2)
# Stammdaten-Spezifikation — Schweißnaht-Ermüdung (FB 7.2)

- PRD: `BAM_PRD_Workflow_FB72.md`
- Workflow: FB7.2 — fatigue testing of weldings (S-N) // Ermüdungsprüfung von Schweißverbindungen (Wöhler)
- bam-masterdata CATALOG SHA: `39c0c77dd209b8b5951eb5e2275c78eab9fab400`
- Generated: 2026-06-04
- Label format: `EN//DE` (no spaces around `//`)

This spec separates entities into three groups so the openBIS admin can run his own
import code: **A — ALREADY PRESENT (reuse)**, **B — TO BE CREATED (new)**,
**C — TO EXTEND**. Section **D** lists manual follow-up tasks. Machine-readable
equivalents live in `masterdata.json` / `masterdata.csv` / `vocabularies.csv`.

---

## Section A — ALREADY PRESENT (REUSE) — do not recreate
## Abschnitt A — BEREITS VORHANDEN (WIEDERVERWENDEN) — nicht neu anlegen

### A.1 ObjectTypes (reuse)

| Code | Citation (bam-masterdata) | Notes |
|---|---|---|
| TestingMachine | object_types.py:1488 | Servo-hydraulic test frame // Servohydraulische Prüfmaschine. Exact match. |
| Instrument | object_types.py:1254 | Generic instrument base (cameras, microscopes, GOM 3D-scanner, IMC amplifiers). Exact match. |
| Calibration | object_types.py:1073 | Calibration record // Kalibrierungs-Datensatz. Exact match. |
| MeasuringAmplifier | UNCONFIRMED (hint object_types.py:7627) | IMC measuring amplifier // IMC-Messverstärker. **Verify against live**; fallback subclass Instrument. |
| Camera | UNCONFIRMED (hint object_types.py:7913) | Camera for fracture imaging // Kamera für Bruchflächenaufnahmen. **Verify against live**; fallback subclass Instrument. |
| LoadFrame | UNCONFIRMED (hint object_types.py:7104) | Load frame // Rahmen der Prüfmaschine. **Verify against live**; fallback subclass Instrument. |
| HydraulicCylinder | UNCONFIRMED (hint object_types.py:6963) | Hydraulic cylinder // Hydraulikzylinder. **Verify against live**; fallback subclass Instrument. |
| Servovalve | UNCONFIRMED (hint object_types.py:7042) | Servo valve // Servoventil. **Verify against live**; fallback subclass Instrument. |
| AlignmentFixture | UNCONFIRMED (hint object_types.py:7167) | Alignment fixture // Ausrichtvorrichtung. **Verify against live**; fallback subclass Instrument. |
| Thermocouple | UNCONFIRMED (hint object_types.py:7193) | Thermocouple // Temperaturfühler. **Verify against live**; fallback subclass Instrument. |
| ForceTransducer | UNCONFIRMED (hint object_types.py:6048) | Force transducer // Kraftaufnehmer. **Verify against live**; fallback subclass Instrument. |

> **Group A decision (walkthrough):** all 8 UNCONFIRMED types are treated as **REUSE as-is**.
> They are not listed in CATALOG.md at SHA 39c0c77; the admin must verify each against live
> bam-masterdata. If one is genuinely missing, subclass `Instrument` (object_types.py:1254).

### A.2 Vocabularies (reuse)

| Code | Citation (bam-masterdata) |
|---|---|
| TESTING_MACHINE_LOAD_TYPE | vocabulary_types.py:31452 (class TestingMachineLoadType) |
| TESTING_MACHINE_DRIVE_TYPE | vocabulary_types.py:31409 (class TestingMachineDriveType) |
| LOAD_FRAME_ORIENTATION | vocabulary_types.py:28095 (class LoadFrameOrientation) |
| SPECIMEN_STATUS | vocabulary_types.py:31267 (class SpecimenStatus) |
| INSTRUMENT_STATUS | vocabulary_types.py:27985 (class InstrumentStatus) |

---

## Section B — TO BE CREATED (NEW) — emit
## Abschnitt B — NEU ANZULEGEN — erzeugen

### B.1 Vocabularies (CREATE, 5)

**ISO_5817_FAT_CLASS** — IIW FAT class for high-cycle fatigue per ISO 5817 // IIW FAT-Klasse für Hochzyklus-Ermüdung nach ISO 5817

| Term | Label (EN//DE) |
|---|---|
| C56 | FAT Class C56//FAT Klasse C56 |
| B90 | FAT Class B90//FAT Klasse B90 |
| B125 | FAT Class B125//FAT Klasse B125 |

**LOAD_LEVEL** — Abstract load level for the S-N curve // Abstraktes Lastniveau für die Wöhlerlinie

| Term | Label (EN//DE) |
|---|---|
| HIGH | High Load//Hohes Lastniveau |
| MEDIUM | Medium Load//Mittleres Lastniveau |
| LOW | Low Load//Niedriges Lastniveau |

**FATIGUE_STOP_REASON** — Reason for fatigue test termination // Grund für den Abbruch des Ermüdungsversuchs

| Term | Label (EN//DE) |
|---|---|
| FRACTURE | Total Fracture//Totalbruch |
| RUN_OUT | Target Cycles Reached (Run Out)//Zyklenzahl erreicht (Durchlaeufer) |
| CRACK | Crack Detected//Riss detektiert |

**STRAIN_GAUGE_TYPE** — Type of strain gauge (DMS) used for monitoring // Typ des verwendeten Dehnungsmessstreifens (DMS) *(Group B: kept)*

| Term | Label (EN//DE) |
|---|---|
| LINEAR | Linear strain gauge (uniaxial)//Linearer DMS (einachsig) |
| ROSETTE | Strain gauge rosette//DMS-Rosette |
| CHAIN | Strain gauge chain (linear array)//DMS-Kette |

**CONSUMABLE_TYPE** — Type of consumable for instrumentation // Typ des bei der Instrumentierung verwendeten Verbrauchsmaterials *(Group B: kept)*

| Term | Label (EN//DE) |
|---|---|
| ADHESIVE | Adhesive (e.g. cyanoacrylate)//Klebstoff (z.B. Cyanacrylat) |
| SOLDER | Solder for cable connection//Loetzinn fuer Kabelanschluss |
| COATING | Protective coating//Schutzbeschichtung |
| CABLE | Cable/wire//Kabel/Draht |

### B.2 ObjectType (CREATE, 1)

**SPECIMEN.WELDED_FATIGUE** (parent: ObjectType, prefix `SPEC.WELD`)
Welded fatigue specimen for S-N curve testing//Geschweisste Ermuedungsprobe fuer Woehlerlinien-Versuche

| Property code | data_type | Label (EN//DE) | Mand. | Section (EN//DE) | Vocab ref | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| ORIGINAL_ID | VARCHAR | Manufacturer ID//Herstellerbezeichnung | no | Material Details//Materialdetails | — | CREATE | **yes** |
| SHEET_ORIGIN | VARCHAR | Sheet origin//Herkunftsblech | no | Material Details//Materialdetails | — | CREATE | **yes** |
| WELDING.WELD_TYPE | CONTROLLEDVOCABULARY | Weld geometry//Schweissnahtgeometrie | **yes** | Weld Details//Schweissnahtdetails | WELDING.WELD_TYPE | EXTEND | no |
| ISO_5817_FAT_CLASS | CONTROLLEDVOCABULARY | FAT class (IIW)//FAT-Klasse (IIW) | no | Weld Details//Schweissnahtdetails | ISO_5817_FAT_CLASS | CREATE | no |
| LOAD_LEVEL | CONTROLLEDVOCABULARY | Load level for S-N curve//Lastniveau fuer Woehlerlinie | no | Test Planning//Versuchsplanung | LOAD_LEVEL | CREATE | no |

### B.3 ExperimentalSteps (CREATE, 12) — FB7.2 §5.3.1–§5.3.12

**EXPERIMENTAL_STEP.PRE_QUALITY_CHECK_WELD** (prefix `EXP.PRE_QC`) — §5.3.1
Pre-test weld geometry quality check//Geometrische Vorqualitaetspruefung der Schweissnaht

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| INITIAL_ANGULAR_DISTORTION | REAL | Initial angular distortion [deg]//Anfangswinkelverzug [Grad] | no | Geometry Checks//Geometriepruefung | — | CREATE | no |
| INITIAL_EDGE_MISALIGNMENT | REAL | Initial edge misalignment [mm]//Anfangskantenversatz [mm] | no | Geometry Checks//Geometriepruefung | — | CREATE | no |
| WAS_STRAIGHTENED | BOOLEAN | Was straightened//Wurde gerichtet | no | Geometry Checks//Geometriepruefung | — | CREATE | no |

**EXPERIMENTAL_STEP.CHAMFERING_GRINDING** (prefix `EXP.CHAMFER`) — §5.3.2
Chamfering / grinding processing step//Anfasen / Schleifen

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| WELD_MODIFICATIONS | MULTILINE_VARCHAR | Weld reinforcement modifications//Schweissnahtverstaerkungen | no | Processing Notes//Bearbeitungsnotizen | — | CREATE | **yes** |

**EXPERIMENTAL_STEP.SPECIMEN_RECORDING** (prefix `EXP.SPEC_REC`) — §5.3.3
Specimen 3D-scan recording (GOM)//Aufnahme der Probe per 3D-Scan (GOM)

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| GOM_SCANNER_REF | OBJECT | GOM 3D-scanner instance//GOM 3D-Scanner Instanz | no | Instrument Links//Geraeteverknuepfungen | — | CREATE | **yes** |

**EXPERIMENTAL_STEP.WELD_ANALYSIS** (prefix `EXP.WELD_ANA`) — §5.3.4
Weld quality / FAT class analysis//Schweissnahtqualitaets- / FAT-Klassen-Analyse

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| ISO_5817_FAT_CLASS | CONTROLLEDVOCABULARY | Determined FAT class//Ermittelte FAT-Klasse | no | Weld Quality//Schweissnahtqualitaet | ISO_5817_FAT_CLASS | CREATE | no |

**EXPERIMENTAL_STEP.SERIES_ASSIGNMENT** (prefix `EXP.SERIES`) — §5.3.5
Series assignment / randomization//Zuordnung zur Versuchsreihe / Randomisierung
*(no properties)*

**EXPERIMENTAL_STEP.TEST_SETUP_GEOMETRY** (prefix `EXP.SETUP_GEO`) — §5.3.6
Pre-test specimen geometry measurement//Geometrievermessung der Probe vor dem Versuch

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| AVG_THICKNESS | REAL | Average thickness [mm]//Durchschnittliche Dicke [mm] | no | Specimen Dimensions//Probenabmessungen | — | CREATE | no |
| AVG_WIDTH | REAL | Average width [mm]//Durchschnittliche Breite [mm] | no | Specimen Dimensions//Probenabmessungen | — | CREATE | no |

**EXPERIMENTAL_STEP.MONITORING_APPLICATION** (prefix `EXP.MON`) — §5.3.7
DMS / strain-gauge application step//DMS-Applikation

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| STRAIN_GAUGE_TYPE | CONTROLLEDVOCABULARY | Strain gauge type//DMS-Typ | no | Instrumentation//Instrumentierung | STRAIN_GAUGE_TYPE | CREATE | no |
| CONSUMABLE_TYPE | CONTROLLEDVOCABULARY | Consumable type//Verbrauchsmaterial-Typ | no | Instrumentation//Instrumentierung | CONSUMABLE_TYPE | CREATE | no |
| MEASURED_DMS_DISTANCE_WELD | REAL | DMS distance to weld toe [mm]//DMS-Abstand zur Schweissnahtuebergang [mm] | no | Instrumentation//Instrumentierung | — | CREATE | no |
| MEASURED_DMS_DISTANCE_EDGE | REAL | DMS distance to specimen edge [mm]//DMS-Abstand zur Probenachse [mm] | no | Instrumentation//Instrumentierung | — | CREATE | no |

**EXPERIMENTAL_STEP.AMPLIFIER_SETTINGS** (prefix `EXP.AMP`) — §5.3.8
Acquisition / amplifier settings//Verstaerker-Einstellungen

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| SAMPLING_FREQUENCY | INTEGER | Sampling frequency [Hz]//Abtastfrequenz [Hz] | no | Acquisition Settings//Aufzeichnungseinstellungen | — | CREATE | no |
| RECORDING_MODE | VARCHAR | Recording mode//Aufzeichnungsmodus | no | Acquisition Settings//Aufzeichnungseinstellungen | — | CREATE | **yes** |
| TESTING_MACHINE_REF | OBJECT | Testing machine//Pruefmaschine | no | Instrument Links//Geraeteverknuepfungen | — | CREATE | **yes** |
| MEASURING_AMPLIFIER_REF | OBJECT | Measuring amplifier//Messverstaerker | no | Instrument Links//Geraeteverknuepfungen | — | CREATE | **yes** |

**EXPERIMENTAL_STEP.INSTALLATION_STRESS_MEASUREMENT** (prefix `EXP.INST_STRESS`) — §5.3.9
Installation stress measurement (0.0 kN)//Einbauspannungsmessung (0.0 kN)
*(no properties)*

**EXPERIMENTAL_STEP.CYCLIC_FATIGUE_TEST** (prefix `EXP.CYC_FAT`) — §5.3.10
S-N cyclic fatigue test//Zyklischer Ermuedungsversuch (S-N)

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| MARKER_LOADS_ACTIVE | BOOLEAN | Marker loads active//Rastlinien aktiv | no | Test Configuration//Versuchskonfiguration | — | CREATE | no |
| FATIGUE_STOP_REASON | CONTROLLEDVOCABULARY | Stop reason//Abbruchgrund | no | Test Outcome//Versuchsergebnis | FATIGUE_STOP_REASON | CREATE | no |

**EXPERIMENTAL_STEP.FATIGUE_DATA_EVALUATION** (prefix `EXP.FAT_EVAL`) — §5.3.11
S-N fatigue data evaluation//Auswertung der Ermuedungsdaten

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| CYCLES_GROSS_FINAL | INTEGER | Final gross cycle count//Bruttoschwingspielzahl | no | Cycle Counts//Schwingspielzahlen | — | CREATE | no |
| CYCLES_NET_FINAL | INTEGER | Final net cycle count//Nettoschwingspielzahl | no | Cycle Counts//Schwingspielzahlen | — | CREATE | no |
| CYCLES_DMS_DEVIATION_10 | MULTILINE_VARCHAR | Cycles to 10% DMS deviation per gauge//Zyklen bis 10% Abfall je DMS | no | Cycle Counts//Schwingspielzahlen | — | CREATE | **yes** |

**EXPERIMENTAL_STEP.FRACTURE_SURFACE_ANALYSIS** (prefix `EXP.FRAC_SURF`) — §5.3.12
Light-microscopic and macroscopic fracture surface analysis//Lichtmikroskopische und makroskopische Bruchflaechenanalyse

| Property | data_type | Label (EN//DE) | Mand. | Section | Vocab | Class | manual_edit |
|---|---|---|---|---|---|---|---|
| CAMERA_REF | OBJECT | Camera//Kamera | no | Instrument Links//Geraeteverknuepfungen | — | CREATE | **yes** |
| DIGITAL_MICROSCOPE_REF | OBJECT | Digital microscope//Digitalmikroskop | no | Instrument Links//Geraeteverknuepfungen | — | CREATE | **yes** |

**Section B totals:** 13 CREATE object types (1 ObjectType + 12 ExperimentalSteps),
5 CREATE vocabularies, **28 property assignments** (10 flagged `needs_manual_edit`).

---

## Section C — TO EXTEND
## Abschnitt C — ZU ERWEITERN

**WELDING.WELD_TYPE** (class `WeldType`, bam-masterdata `welding/vocabularies.py:38`)
Add two new terms via PR to bam-masterdata // Zwei neue Begriffe per PR ergänzen:

| New term | Label (EN//DE) |
|---|---|
| BUTT_WELD | Butt weld//Stumpfstoß |
| CRUCIFORM_WELD | Cruciform weld//Kreuzstoß |

Existing 6 terms remain unchanged: WELDING_FILLET_WELD, WELDING_GROOVE_WELD,
WELDING_PLUG_WELD, WELDING_SPOT_WELD, WELDING_SURFACING_WELD, WELDING_TACK_WELD.

---

## Section D — Manual follow-up
## Abschnitt D — Manuelle Nacharbeit

### D.1 Group E — properties to finalize by hand in the openBIS UI (`needs_manual_edit=true`)
The schema is created by the admin, but the value/label/section is edited later in the UI:

- OBJECT instrument links: `GOM_SCANNER_REF`, `TESTING_MACHINE_REF`, `MEASURING_AMPLIFIER_REF`, `CAMERA_REF`, `DIGITAL_MICROSCOPE_REF`
- Free-text: `ORIGINAL_ID`, `SHEET_ORIGIN`, `RECORDING_MODE`, `WELD_MODIFICATIONS`, `CYCLES_DMS_DEVIATION_10`

### D.2 Group F — operator / instance-value tasks (not schema; documented only)
- Notebook config: `OPENBIS_URL`, `SPACE`, `PROJECT_CODE`, `COLLECTION_CODE`
- The 12 ExperimentalStep value fill-ins (per-experiment instance data)
- Dataset file paths (load program, 3D scans, fracture images)
- Parser file I/O wiring
