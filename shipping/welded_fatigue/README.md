# Shipping Package — Welded Fatigue (FB 7.2)

Hand-off package for the **openBIS admin** to create the masterdata (ObjectTypes,
ExperimentalSteps, PropertyTypes, Vocabularies) for the **fatigue testing of weldings**
workflow (FB 7.2) using **his own import code**.

- PRD: `BAM_PRD_Workflow_FB72.md`
- bam-masterdata CATALOG SHA: `39c0c77dd209b8b5951eb5e2275c78eab9fab400`
- Label format throughout: `EN//DE` (English//Deutsch, no spaces around `//`)

## Files in this package

| File | Purpose |
|---|---|
| `SPEC.md` | Human-readable bilingual spec. Section A = ALREADY PRESENT (reuse), B = TO BE CREATED, C = TO EXTEND, D = manual follow-up. |
| `masterdata.json` | Machine-readable: `object_types[]` + `vocabularies[]`, each tagged `classification` (CREATE/REUSE/EXTEND). Ingest this in your import code. |
| `masterdata.csv` | Flat one-row-per-property list of all CREATE property assignments (28 rows). |
| `vocabularies.csv` | Flat one-row-per-term list (CREATE + EXTEND terms). |
| `_decisions.md` | Audit trail of the walkthrough decisions (Groups A–F). |

## How to use

1. **Read classifications, don't blindly create.** Every entry in `masterdata.json`
   carries a `classification`:
   - `REUSE` → already in bam-masterdata; **do not recreate**. For the 8 UNCONFIRMED
     ObjectTypes, verify against live bam-masterdata first; if missing, subclass
     `Instrument` (object_types.py:1254).
   - `EXTEND` → exists, needs new terms; handle via PR (see below), not via create.
   - `CREATE` → genuinely new; create these.

2. **Create order (CREATE only):**
   1. Vocabularies (`vocabularies[]` where `classification == CREATE`): ISO_5817_FAT_CLASS,
      LOAD_LEVEL, FATIGUE_STOP_REASON, STRAIN_GAUGE_TYPE, CONSUMABLE_TYPE.
   2. ObjectType + ExperimentalSteps (`object_types[]` where `classification == CREATE`).
   3. Property assignments per object type (from `properties[]` / `masterdata.csv`).
      A property whose `classification == EXTEND` (e.g. `WELDING.WELD_TYPE` on
      WeldedFatigueSpecimen) must wait until the EXTEND PR below is merged.

3. **EXTEND PR for `WELDING.WELD_TYPE`:** open a PR to `bam-masterdata`
   (`welding/vocabularies.py:38`, class `WeldType`) adding the two `VocabularyTerm`
   entries `BUTT_WELD` (Butt weld//Stumpfstoß) and `CRUCIFORM_WELD`
   (Cruciform weld//Kreuzstoß). Do not duplicate the existing 6 terms.

## Manual follow-up

These are **not** auto-created by your import code; they are deferred tasks.

### Group E — schema created, values/labels edited by hand later in the openBIS UI
Flagged `needs_manual_edit=true` in `masterdata.json` / `masterdata.csv`:

- OBJECT instrument links (bind to live instrument instances):
  `GOM_SCANNER_REF`, `TESTING_MACHINE_REF`, `MEASURING_AMPLIFIER_REF`,
  `CAMERA_REF`, `DIGITAL_MICROSCOPE_REF`
- Free-text (wording/value to finalize): `ORIGINAL_ID`, `SHEET_ORIGIN`,
  `RECORDING_MODE`, `WELD_MODIFICATIONS`, `CYCLES_DMS_DEVIATION_10`

### Group F — operator / instance-value tasks (done by the experiment operator)
- Notebook config: `OPENBIS_URL`, `SPACE`, `PROJECT_CODE`, `COLLECTION_CODE`
- The 12 ExperimentalStep value fill-ins (per-experiment instance data)
- Dataset file paths (load program, 3D scans, fracture images)
- Parser file I/O wiring

## Inventory summary

- CREATE: 13 object types (1 ObjectType + 12 ExperimentalSteps) + 5 vocabularies; 28 property assignments
- EXTEND: 1 vocabulary (WELDING.WELD_TYPE, +2 terms)
- REUSE: 11 ObjectTypes (3 confirmed + 8 verify-live) + 5 vocabularies
- `needs_manual_edit=true`: 10 properties
