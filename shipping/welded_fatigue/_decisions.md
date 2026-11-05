# Walkthrough Decision Log — welded_fatigue (FB7.2)

Audit trail of the Step 1 grouped TODO walkthrough. Recorded for traceability into
the shipping package (`SPEC.md`, `masterdata.json`, `masterdata.csv`).

- Date: 2026-06-04
- PRD: BAM_PRD_Workflow_FB72.md
- bam-masterdata CATALOG SHA: 39c0c77dd209b8b5951eb5e2275c78eab9fab400
- Source of truth: `generated/welded_fatigue/gap-report.md`, `.../datamodel/object_types.py`, `.../datamodel/vocabularies.py`

---

## Group A — UNCONFIRMED reuse ObjectTypes (8)

**Decision: REUSE as-is (default).**

All 8 are classified **REUSE** and must NOT be recreated by the admin. Each carries a
"verify against live bam-masterdata" note because they are not listed in CATALOG.md at
SHA 39c0c77 (citation hints come from requirements.json).

| ObjectType | Citation hint | Decision |
|---|---|---|
| MeasuringAmplifier | object_types.py:7627 (hint) | REUSE — verify live |
| Camera | object_types.py:7913 (hint) | REUSE — verify live |
| LoadFrame | object_types.py:7104 (hint) | REUSE — verify live |
| HydraulicCylinder | object_types.py:6963 (hint) | REUSE — verify live |
| Servovalve | object_types.py:7042 (hint) | REUSE — verify live |
| AlignmentFixture | object_types.py:7167 (hint) | REUSE — verify live |
| Thermocouple | object_types.py:7193 (hint) | REUSE — verify live |
| ForceTransducer | object_types.py:6048 (hint) | REUSE — verify live |

Fallback if a type is genuinely missing live: subclass `Instrument` (object_types.py:1254).

## Group B — Optional vocabularies (2)

**Decision: KEEP BOTH.**

`STRAIN_GAUGE_TYPE` and `CONSUMABLE_TYPE` are emitted as CREATE vocabularies. The two
`MonitoringApplication` CONTROLLEDVOCABULARY properties (`strain_gauge_type_ref`,
`consumable_type_ref`) are retained.

## Group C — EXTEND vocabulary (WELDING.WELD_TYPE)

**Decision: CONFIRM BOTH terms.**

Add via PR to `bam-masterdata` (welding/vocabularies.py:38, class `WeldType`):

| Term code | Label (EN//DE) |
|---|---|
| BUTT_WELD | Butt weld//Stumpfstoß |
| CRUCIFORM_WELD | Cruciform weld//Kreuzstoß |

Existing 6 terms left untouched: WELDING_FILLET_WELD, WELDING_GROOVE_WELD,
WELDING_PLUG_WELD, WELDING_SPOT_WELD, WELDING_SURFACING_WELD, WELDING_TACK_WELD.

## Group D — New info from the user

**Decision: NOTHING NEW.** Ship exactly the confirmed inventory. No new ObjectTypes,
properties, or vocabulary terms added.

## Group E — Properties flagged needs_manual_edit=true (10)

**Decision: FLAG two buckets** — OBJECT instrument links + free-text VARCHAR props.

| Property code | Owner type | data_type | Reason |
|---|---|---|---|
| GOM_SCANNER_REF | SpecimenRecording | OBJECT | Bind to live instrument instance in UI |
| TESTING_MACHINE_REF | AmplifierSettings | OBJECT | Bind to live instrument instance in UI |
| MEASURING_AMPLIFIER_REF | AmplifierSettings | OBJECT | Bind to live instrument instance in UI |
| CAMERA_REF | FractureSurfaceAnalysis | OBJECT | Bind to live instrument instance in UI |
| DIGITAL_MICROSCOPE_REF | FractureSurfaceAnalysis | OBJECT | Bind to live instrument instance in UI |
| ORIGINAL_ID | WeldedFatigueSpecimen | VARCHAR | Wording/value to be finalized in UI |
| SHEET_ORIGIN | WeldedFatigueSpecimen | VARCHAR | Wording/value to be finalized in UI |
| RECORDING_MODE | AmplifierSettings | VARCHAR | Wording/value to be finalized in UI |
| WELD_MODIFICATIONS | ChamferingGrinding | MULTILINE_VARCHAR | Wording/value to be finalized in UI |
| CYCLES_DMS_DEVIATION_10 | FatigueDataEvaluation | MULTILINE_VARCHAR | Wording/value to be finalized in UI |

## Group F — Instance-value / operator TODOs (deferred, documented only)

Not schema/admin tasks. Listed in `README.md` → "Manual follow-up". Includes:
- Notebook config: `OPENBIS_URL`, `SPACE`, `PROJECT_CODE`, `COLLECTION_CODE`
- The 12 ExperimentalStep value fill-ins (per-experiment instance data)
- Dataset file paths (load program, scans, fracture images)
- Parser file I/O wiring
