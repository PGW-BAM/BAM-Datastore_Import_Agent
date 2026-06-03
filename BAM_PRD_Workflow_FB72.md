# Product Requirements Document (PRD): Automated openBIS Masterdata Extension (Workflow FB 7.2)

> **Rewritten in Phase 4** (reuse-first). Original preserved at `evals/regressions/BAM_PRD_Workflow_FB72_original.md`.
> Gap report: `generated/welded_fatigue/gap-report.md` (produced by `/bam-analyze-prd`).

---

## 1. Kontext & Zielsetzung

**Ziel:** Generierung von Python-Code zur Erweiterung des zentralen BAM-Datenmodells (`bam-masterdata`) für den Prüfstand-Workflow des Fachbereichs 7.2 (Zyklische Ermüdungsprüfungen / Wöhlerlinien).

**Rolle des Agenten:** Agiere als Experte für das BAM-openBIS-Masterdata-Framework. Erzeuge sauberen, deklarativen, klassenbasierten Python-Code, der direkt über einen Pull Request in das bestehende Repository integriert werden kann.

**Sprachvorgabe:** Alle Labels, Beschreibungen (`description`) und Sektionen MÜSSEN strikt im BAM-zweisprachigen Format `"English//Deutsch"` (getrennt durch ein doppeltes Slash **ohne Leerzeichen**) ausgeführt werden.

---

## 2. Reuse Policy (verbindlich)

> *Before defining ANY new vocabulary, ObjectType, ExperimentalStep, or PropertyTypeAssignment, the implementation MUST cite either:*
> *(a) an existing class in `bam-masterdata` (path + line number) and explain why it cannot be reused as-is, OR*
> *(b) the matching entry in `generated/welded_fatigue/gap-report.md` showing the gap is genuine.*
>
> *Violations of this policy — creating a new type without a citation — are a hard failure in the pipeline's verification checklist.*

This policy replaces the informal "Reuse Policy" in the original PRD §2. It is machine-checkable: `generated/welded_fatigue/gap-report.md` must classify every entity in §5 as **CREATE** before the code generator may emit it.

**Forbidden patterns** (carry over from PLAN.md §0.3):
- `o.create_sample_type()`, `o.create_object_type()`, `o.create_collection_type()` — these are not valid pyBIS 1.37.4 methods and must never appear in generated code or notebooks.
- Bilingual strings with spaces around `//` (e.g., `"English // Deutsch"`) — the separator is `//` with no surrounding spaces.

---

## 3. Bekannte Wiederverwendungen — REUSE (locked)

These types exist in `bam-masterdata` and MUST be used as-is. Do NOT redefine them. Do NOT create subclasses unless the gap report explicitly classifies them as EXTEND with a justification.

### 3.1 ObjectTypes — reuse verbatim

| Class | openBIS code | Citation | Usage in FB7.2 |
|---|---|---|---|
| `TestingMachine` | `TESTING_MACHINE` | `bam_masterdata/datamodel/object_types.py:1488` | Prüfmaschinen (servo-hydraulic test frames) |
| `Instrument` | `INSTRUMENT` | `bam_masterdata/datamodel/object_types.py:1254` | Kameras, Mikroskope, GOM 3D-Scanner, IMC-Messverstärker (generic) |
| `MeasuringAmplifier` | `MEASURING_AMPLIFIER` | `bam_masterdata/datamodel/object_types.py:7627` | IMC-Messverstärker (specific) |
| `Camera` | `CAMERA` | `bam_masterdata/datamodel/object_types.py:7913` | Kamera für Bruchflächenaufnahmen |
| `LoadFrame` | `LOAD_FRAME` | `bam_masterdata/datamodel/object_types.py:7104` | Rahmen der Prüfmaschine |
| `HydraulicCylinder` | `HYDRAULIC_CYLINDER` | `bam_masterdata/datamodel/object_types.py:6963` | Hydraulikzylinder |
| `Servovalve` | `SERVOVALVE` | `bam_masterdata/datamodel/object_types.py:7042` | Servoventil |
| `AlignmentFixture` | `ALIGNMENT_FIXTURE` | `bam_masterdata/datamodel/object_types.py:7167` | Ausrichtvorrichtung |
| `Thermocouple` | `THERMOCOUPLE` | `bam_masterdata/datamodel/object_types.py:7193` | Temperaturfühler |
| `Calibration` | `CALIBRATION` | `bam_masterdata/datamodel/object_types.py:1073` | Kalibrierungs-Datensätze |
| `ForceTransducer` | `FORCE_TRANSDUCER` | `bam_masterdata/datamodel/object_types.py:6048` | Kraftaufnehmer |

### 3.2 VocabularyTypes — reuse verbatim

| Code | Citation | Usage in FB7.2 |
|---|---|---|
| `WELDING.WELD_TYPE` | `bam_masterdata/datamodel/welding/vocabularies.py` — UNCONFIRMED line; verify | Schweißnahttyp (see §4 for EXTEND decision) |
| `TESTING_MACHINE_LOAD_TYPE` | `bam_masterdata/datamodel/vocabulary_types.py` — UNCONFIRMED line; verify | Belastungsart der Prüfmaschine |
| `TESTING_MACHINE_DRIVE_TYPE` | `bam_masterdata/datamodel/vocabulary_types.py` — UNCONFIRMED line; verify | Antriebsart der Prüfmaschine |
| `LOAD_FRAME_ORIENTATION` | `bam_masterdata/datamodel/vocabulary_types.py` — UNCONFIRMED line; verify | Orientierung des Prüfrahmens |
| `SPECIMEN_STATUS` | `bam_masterdata/datamodel/vocabulary_types.py` — UNCONFIRMED line; verify | Probenstatus |
| `INSTRUMENT_STATUS` | `bam_masterdata/datamodel/vocabulary_types.py` — UNCONFIRMED line; verify | Gerätestatus |

> **Note on UNCONFIRMED citations:** These vocabulary line numbers have not been confirmed against the live repository. Before emitting any REUSE code that references them, run `/bam-sync` and verify the lines exist. The gap-analyzer agent will confirm or correct these citations.

---

## 4. Erweiterungen — EXTEND

These types exist in `bam-masterdata` but require additional terms. The extension should be submitted as a PR to `BAMresearch/bam-masterdata`.

### 4.1 `WELDING.WELD_TYPE` — add BUTT_WELD and CRUCIFORM_WELD

**Current terms** (from `bam_masterdata/datamodel/welding/vocabularies.py`):
`FILLET`, `GROOVE`, `PLUG`, `SPOT`, `SURFACING`, `TACK`

**Missing terms required by FB7.2:**
- `BUTT_WELD` — `"Butt weld//Stumpfstoß"`
- `CRUCIFORM_WELD` — `"Cruciform weld//Kreuzstoß"`

**EXTEND decision rationale:**
`BUTT_WELD` and `CRUCIFORM_WELD` are standard IIW weld joint geometry types, consistent with the existing `WELD_TYPE` vocabulary's classification scheme (FILLET, GROOVE, etc.). They belong in the same vocabulary rather than a separate `WELD_GEOMETRY` vocabulary. The original PRD defined `WELD_GEOMETRY` as a new vocabulary — this was a mistake identified by the gap analyzer. The correct action is to **EXTEND** `WELDING.WELD_TYPE` via PR.

**PR action:** Add the two terms to `bam_masterdata/datamodel/welding/vocabularies.py`. The `WeldedFatigueSpecimen.weld_geometry` property (§5.2) should reference `WELDING.WELD_TYPE`, not `WELD_GEOMETRY`.

> **If the gap report classifies `WELDING.WELD_TYPE` differently** (e.g., as CREATE because the welding subpackage is missing), the generator must re-evaluate. The gap report is authoritative; this PRD provides the *intent*, not the final decision.

---

## 5. Neudefinitionen — CREATE

Only these entities are genuinely absent from `bam-masterdata` and may be created. All are confirmed CREATE by the gap analysis (subject to re-verification with `/bam-analyze-prd`).

### 5.1 Neue Vokabulare (CREATE)

> **Pipeline rule:** Emit these only if `generated/welded_fatigue/gap-report.md` classifies them as CREATE.

#### `ISO_5817_FAT_CLASS`
HCF-relevante FAT-Klassen nach IIW. Kein äquivalentes Vokabular in `bam-masterdata`.
- `C56` — `"FAT Class C56//FAT Klasse C56"`
- `B90` — `"FAT Class B90//FAT Klasse B90"`
- `B125` — `"FAT Class B125//FAT Klasse B125"`

#### `LOAD_LEVEL`
Abstrakte Lastniveaus für die Wöhlerlinie. Kein äquivalentes Vokabular in `bam-masterdata`.
- `HIGH` — `"High Load//Hohes Lastniveau"`
- `MEDIUM` — `"Medium Load//Mittleres Lastniveau"`
- `LOW` — `"Low Load//Niedriges Lastniveau"`

#### `FATIGUE_STOP_REASON`
Abbruchgrund des Ermüdungsversuchs. Kein äquivalentes Vokabular in `bam-masterdata`.
- `FRACTURE` — `"Total Fracture//Totalbruch"`
- `RUN_OUT` — `"Target Cycles Reached (Run Out)//Zyklenzahl erreicht (Durchläufer)"`
- `CRACK` — `"Crack Detected//Riss detektiert"`

#### `STRAIN_GAUGE_TYPE` *(optional — emit only if referenced by a CREATE step)*
DMS-Typ für Dehnungsmessstreifen-Konfigurationen. Emit only if required by `MonitoringApplication` (§5.3.7) and confirmed CREATE by the gap report.

#### `CONSUMABLE_TYPE` *(optional — emit only if referenced by a CREATE step)*
Verbrauchsmaterial-Typ. Emit only if required by `MonitoringApplication` and confirmed CREATE.

---

### 5.2 Neuer Probentyp (CREATE)

#### `WeldedFatigueSpecimen`
**Why it can't be a subclass of an existing class:** The closest peer is `Fcg` (fatigue crack growth specimen). However, `WeldedFatigueSpecimen` is a *welded structural specimen tested to S-N curve failure*, not a crack-growth specimen. The `Fcg` class has FCG-specific properties (crack length tracking, DCPD measurement) that are irrelevant here and would pollute the UI. Inherit directly from `ObjectType`.

| Attribute | Value |
|---|---|
| Class name | `WeldedFatigueSpecimen` |
| openBIS code | `SPECIMEN.WELDED_FATIGUE` |
| Parent | `ObjectType` |
| generated_code_prefix | `SPEC.WELD` |

**Properties:**

| Property | Data type | Vocabulary | Section | Mandatory | Description |
|---|---|---|---|---|---|
| `original_id` | VARCHAR | — | "Material Details" | No | `"Manufacturer ID//Herstellerbezeichnung"` |
| `sheet_origin` | VARCHAR | — | "Material Details" | No | `"Sheet origin//Herkunftsblech (Bias-Vermeidung)"` |
| `weld_geometry` | CONTROLLEDVOCABULARY | `WELDING.WELD_TYPE` | "Weld Details" | Yes | `"Weld geometry//Schweißnahtgeometrie"` |
| `iso_fat_class` | CONTROLLEDVOCABULARY | `ISO_5817_FAT_CLASS` | "Weld Details" | No | `"FAT class (IIW)//FAT-Klasse (IIW)"` |
| `load_level` | CONTROLLEDVOCABULARY | `LOAD_LEVEL` | "Test Planning" | No | `"Load level for S-N curve//Lastniveau für Wöhlerlinie"` |

---

### 5.3 Neue Prozessschritte (CREATE) — 12 ExperimentalSteps

All 12 inherit from `ExperimentalStep`. Use `generated_code_prefix="EXP.[KURZNAME]"` as noted.

**Lean Property Rule:** Complex tabular data (load programs, fracture line tables) are **not** stored as discrete property fields. They are attached as file uploads (Excel/CSV) to the relevant step.

---

#### 5.3.1 `PreQualityCheckWeld`
`EXPERIMENTAL_STEP.PRE_QUALITY_CHECK_WELD`

| Property | Data type | Section | Description |
|---|---|---|---|
| `initial_angular_distortion` | REAL | "Geometry Checks" | `"Initial angular distortion [°]//Anfangswinkelverzug [°]"` |
| `initial_edge_misalignment` | REAL | "Geometry Checks" | `"Initial edge misalignment [mm]//Anfangskantenversatz [mm]"` |
| `was_straightened` | BOOLEAN | "Geometry Checks" | `"Was straightened//Wurde gerichtet"` |

---

#### 5.3.2 `ChamferingGrinding`
`EXPERIMENTAL_STEP.CHAMFERING_GRINDING`

| Property | Data type | Section | Description |
|---|---|---|---|
| `weld_modifications` | MULTILINE_VARCHAR | "Processing Notes" | `"Weld reinforcement modifications//Schweißnahtverstärkungen / Schleifhinweise"` |

---

#### 5.3.3 `SpecimenRecording`
`EXPERIMENTAL_STEP.SPECIMEN_RECORDING`

Object link (OBJECT data type) to the GOM 3D-scanner instance, using the REUSE `Instrument` type. No additional scalar properties beyond the standard `ExperimentalStep` fields.

---

#### 5.3.4 `WeldAnalysis`
`EXPERIMENTAL_STEP.WELD_ANALYSIS`

| Property | Data type | Section | Description |
|---|---|---|---|
| `iso_fat_class` | CONTROLLEDVOCABULARY `ISO_5817_FAT_CLASS` | "Weld Quality" | `"Determined FAT class//Ermittelte FAT-Klasse"` |

---

#### 5.3.5 `SeriesAssignment`
`EXPERIMENTAL_STEP.SERIES_ASSIGNMENT`

Dokumentiert die zeitliche Randomisierung und Zuteilung zur Prüfserie (Collection). No additional scalar properties beyond the standard `ExperimentalStep` fields.

---

#### 5.3.6 `TestSetupGeometry`
`EXPERIMENTAL_STEP.TEST_SETUP_GEOMETRY`

| Property | Data type | Section | Description |
|---|---|---|---|
| `avg_thickness` | REAL | "Specimen Dimensions" | `"Average thickness [mm]//Durchschnittliche Dicke [mm]"` |
| `avg_width` | REAL | "Specimen Dimensions" | `"Average width [mm]//Durchschnittliche Breite [mm]"` |

---

#### 5.3.7 `MonitoringApplication`
`EXPERIMENTAL_STEP.MONITORING_APPLICATION`

| Property | Data type | Section | Description |
|---|---|---|---|
| `strain_gauge_type_ref` | OBJECT (`STRAIN_GAUGE_TYPE`) | "Instrumentation" | `"Strain gauge type//DMS-Typ"` |
| `consumable_type_ref` | OBJECT (`CONSUMABLE_TYPE`) | "Instrumentation" | `"Consumable type//Verbrauchsmaterial-Typ"` |
| `measured_dms_distance_weld` | REAL | "Instrumentation" | `"DMS distance to weld toe [mm]//DMS-Abstand zur Schweißnaht [mm]"` |
| `measured_dms_distance_edge` | REAL | "Instrumentation" | `"DMS distance to specimen edge [mm]//DMS-Abstand zur Probenachse [mm]"` |

---

#### 5.3.8 `AmplifierSettings`
`EXPERIMENTAL_STEP.AMPLIFIER_SETTINGS`

Object links to `TestingMachine` (REUSE) and `MeasuringAmplifier` (REUSE).

| Property | Data type | Section | Description |
|---|---|---|---|
| `sampling_frequency` | INTEGER | "Acquisition Settings" | `"Sampling frequency [Hz]//Abtastfrequenz [Hz]"` |
| `recording_mode` | VARCHAR | "Acquisition Settings" | `"Recording mode (e.g. Peak-Valley)//Aufzeichnungsmodus"` |

---

#### 5.3.9 `InstallationStressMeasurement`
`EXPERIMENTAL_STEP.INSTALLATION_STRESS_MEASUREMENT`

Erfassung des Biegemoments bei 0.0 kN vor Versuchsstart (Einbaubeanspruchung). No additional scalar properties beyond the standard `ExperimentalStep` fields. Results stored as attached file.

---

#### 5.3.10 `CyclicFatigueTest`
`EXPERIMENTAL_STEP.CYCLIC_FATIGUE_TEST`

**Lean property rule applied:** Das Lastprogramm wird als Excel-Datei an diesen Schritt angehängt — keine dedizierten Lastfelder.

| Property | Data type | Section | Description |
|---|---|---|---|
| `marker_loads_active` | BOOLEAN | "Test Configuration" | `"Marker loads active (fracture lines)//Rastlinien aktiv"` |
| `stop_reason` | CONTROLLEDVOCABULARY `FATIGUE_STOP_REASON` | "Test Outcome" | `"Stop reason//Abbruchgrund"` |

---

#### 5.3.11 `FatigueDataEvaluation`
`EXPERIMENTAL_STEP.FATIGUE_DATA_EVALUATION`

| Property | Data type | Section | Description |
|---|---|---|---|
| `cycles_gross_final` | INTEGER | "Cycle Counts" | `"Final gross cycle count//Bruttoschwingspielzahl"` |
| `cycles_net_final` | INTEGER | "Cycle Counts" | `"Final net cycle count//Nettoschwingspielzahl"` |
| `cycles_dms_deviation_10` | MULTILINE_VARCHAR | "Cycle Counts" | `"Cycles to 10% DMS deviation per gauge//Zyklen bis 10% Abfall je DMS"` |

---

#### 5.3.12 `FractureSurfaceAnalysis`
`EXPERIMENTAL_STEP.FRACTURE_SURFACE_ANALYSIS`

Lichtmikroskopische und makroskopische Auswertung der Bruchfläche. Object links to `Camera` (REUSE) and digital microscope via `Instrument` (REUSE). No additional scalar properties.

---

## 6. Sprache & Format

- **Bilingual format:** `"English//Deutsch"` — double slash, **no spaces** before or after `//`.
- English label always first.
- Applies to: `description`, `property_label`, section names, vocabulary term descriptions.
- Violation: `"English // Deutsch"` (spaces) — hard error in verification (`grep -nE`).

---

## 7. Lieferform

The pipeline produces two complementary outputs:

### 7.1 Masterdata extension module (PR-ready)

Output path: `generated/welded_fatigue/datamodel/`

Structure mirrors `bam-masterdata/bam_masterdata/datamodel/welding/`:
```
generated/welded_fatigue/datamodel/
├── vocabularies.py      # §5.1 vocabularies (CREATE only)
├── object_types.py      # §5.2 WeldedFatigueSpecimen + §5.3 ExperimentalSteps
└── README.md            # PR instructions + EXTEND table
```

The generator MUST NOT emit code for REUSE or EXTEND items. The README must include:
- The EXTEND table (§4) with PR instructions for `WELDING.WELD_TYPE`.
- A symlink test: `python -c "from bam_masterdata.metadata.entities import ObjectType; ..."` after symlinking into `bam-masterdata/bam_masterdata/datamodel/`.

### 7.2 Provisioning notebook

Output path: `notebooks/welded_fatigue_provisioning.ipynb`

A Jupyter notebook using only the APIs in PLAN.md §0.2. Structure:
- Cells 1-11: one-time provisioning (Collection + specimen Objects + dataset stubs).
- Cell 12-13: parser usage stub (see §7.3).
- No hardcoded credentials. PAT via `get_or_create_personal_access_token`.
- No `o.create_sample_type`, `o.create_object_type`, or `o.create_collection`.

### 7.3 Parser scaffold

Output path: `generated/welded_fatigue/parsers/`

An `AbstractParser` subclass scaffold for per-run data ingestion. Install with:
```bash
pip install -e generated/welded_fatigue/parsers/
```

The parser is the *ongoing ingestion path*; the notebook (§7.2) is the *one-time setup path*. Run the notebook once to provision the openBIS hierarchy; run the parser after every experiment to push new `ExperimentalStep` objects.
