---
name: structure-designer
description: Turn a workflow-style requirements.json into a flat openBIS structure (design.json + design.md) - which data item lives on which object, in which section (in workflow order), which steps become objects, which inventory objects are linked as parents, which files go where. Applies the PRD principles (flat object + type hierarchy, reuse-first) using CATALOG + live inventory as reference. Does NOT classify REUSE/EXTEND/CREATE (gap-analyzer does).
tools: Read, Write, Glob, Grep, Bash
---

# Agent: structure-designer

## Single responsibility

Map every data item, equipment item and file of `requirements.json` to **exactly one place** in openBIS
and keep that place **flat**. Output is the design that the gap-analyzer classifies and the
masterdata-extender implements.

## Inputs

| Input | Path |
|---|---|
| Requirements (workflow style) | `generated/<prd-stem>/requirements.json` |
| Catalog (machine-readable) | `generated/catalog.json` — types, inherited properties, PropertyType index |
| Catalog (human-readable) | `generated/CATALOG.md` |
| Live inventory | `generated/live/*_inventory.md` (what the target instance already has) |

## Outputs

- `generated/<prd-stem>/design.json`
- `generated/<prd-stem>/design.md` — human-readable: tree, step→location table, metrics before/after

Output format: `schemas/design.schema.json` (checked by `python tools/check_files.py <name>`; the review page refuses
to render until it passes).

## Design algorithm (follow in order)

1. **Subject first (P3).** Every data item that *describes the specimen* (identity, geometry, weld
   rating, distortion, series assignment, load level, test order) goes on the specimen type, grouped into
   sections named after the workflow step (`"Initial Quality Check"`, `"Geometry Before Installation"`, …), in workflow order.
2. **Group activities (P4).** Remaining steps are activities. Consecutive steps performed at the same
   workplace / with the same equipment / in one session become **one** step object with one section per workflow step, in workflow order
   (`"Strain Gauge Application"`, `"Measuring Amplifier And Test Rig"`, …). Section names: Title Case, letters
   only (no digits, `/`, `-`), as the bam-masterdata checker requires; step numbers go into the "next step"
   vocabulary labels and the workflow plan. A step that needs only an instrument link
   + files and has no own data items does **not** get a new type — use the generic `EXPERIMENTAL_STEP`.
3. **Flat links (P1).** Steps are children of the specimen only. Instruments, testing machines and
   auxiliary materials are **parents** of the step that uses them (inventory objects), never OBJECT
   properties to dummy catalog types. No step→step links.
4. **Workflow visibility (P5).** Add to the specimen one CONTROLLEDVOCABULARY property "Next step" whose
   vocabulary lists the workflow steps in order (`S01_…` … `S12_…`, `DONE`). Plan one `SOP` object
   "Workflow plan" per project holding the step→location table.
5. **Base classes (P2).** Pick the closest existing base from catalog.json and inherit directly:
   specimen → `Sample`; mechanical test → `MechanicalTest` (if present); otherwise `ExperimentalStep`/
   `ObjectType`. Never introduce an intermediate class of your own.
6. **Properties.** For each data item choose:
   - an **existing PropertyType code** from the catalog's property index when data type *and* meaning
     match (record `"reuse_property": "<code> (<class>)"`), else
   - a new code with the domain prefix `FATIGUE.` (e.g. `FATIGUE.INITIAL_ANGULAR_DISTORTION`), so new codes
     cannot collide with live-only legacy codes of a different data type.
   - `repeat: n` items become n properties (`…_POS_1`, `…_POS_2`, …) — never several numbers in one REAL.
   - `choice` items reference a vocabulary: an existing one from the catalog if its terms cover the
     choices, otherwise a new vocabulary (list its terms). Respect `domain_decisions` verbatim.
   - Every name in both languages: `property_label` (English) + `property_label_de`, vocabulary terms `label` +
     `label_de`, `section_names_de` for sections, `step_de` in `step_location_map`, `name_de`/`name_en` for objects
     and object types; collection/object names (`$NAME`) as "Deutsch / Englisch". Descriptions `"English//Deutsch"`.
     Sections stay English in openBIS (checker: Title Case, letters only).
7. **Files (P7).** Map every file to an object (specimen / step / collection) and a **standard** dataset
   type from the catalog (RAW_DATA, PROCESSED_DATA, ANALYZED_DATA, ATTACHMENT, FIGURE, FIGURE.PLOT,
   SOURCE_CODE, MEASUREMENT_PROTOCOL_FILE). No new dataset types.
8. **Series.** Collection type `COLLECTION` with `$DEFAULT_OBJECT_TYPE` = specimen type, unless the catalog
   offers a better fit.
9. **Metrics.** Compute and report: new object types, new vocabularies, objects per specimen, max link
   depth, new dataset types — and the same numbers for the live legacy model (from the live inventory).

## design.json schema (abridged)

```json
{
  "prd_stem": "…", "catalog_sha": "…", "designed_at": "<ISO>",
  "object_types": [
    {"class_name": "WeldedFatigueSpecimen", "code": "SAMPLE.WELDED_FATIGUE_SPECIMEN",
     "parent_class": "Sample", "generated_code_prefix": "SAM.WFS",
     "description": "…//…", "covers_steps": ["01","02","04","05","06"],
     "properties": [
       {"attr": "initial_angular_distortion", "code": "FATIGUE.INITIAL_ANGULAR_DISTORTION",
        "data_type": "REAL", "property_label": "Initial angular distortion [°]",
        "property_label_de": "Winkelverzug initial [°]",
        "description": "…//…", "section": "Initial Quality Check", "mandatory": false,
        "vocabulary_code": null, "object_code": null, "reuse_property": null,
        "source": "PRD §3 step 01"}
     ]}
  ],
  "vocabularies": [{"class_name": "…", "code": "…", "description": "…//…",
                    "terms": [{"code": "…", "label": "…", "label_de": "…", "description": "…//…"}],
                    "existing": null, "decision_ref": null}],
  "reused_types": [{"code": "EXPERIMENTAL_STEP", "role": "Steps 03-04 3D scan + weld analysis"}],
  "inventory_links": [{"inventory": "ZEISS GOM ATOS 5", "type_code": "INSTRUMENT", "parent_of": "SCAN step"}],
  "layout": {"project": "…", "collections": ["…"],
             "per_specimen": [{"code_pattern": "S1-01", "type": "…", "name_pattern": "…"},
                              {"code_pattern": "S1-01-TEST", "type": "…", "parents": ["specimen", "…"]}]},
  "dataset_mapping": [{"file": "…", "attach_to": "specimen|<step>|collection", "dataset_type": "RAW_DATA"}],
  "section_names_de": {"Initial Quality Check": "Vorqualitätsprüfung"},
  "step_location_map": [{"no": "01", "step": "…", "step_de": "…", "object": "specimen", "section": "Initial Quality Check",
                         "files": ["…"]}],
  "metrics": {"new": {…}, "legacy_live": {…}}
}
```

## Rules / anti-patterns

- Every data item, equipment item and file of requirements.json appears **exactly once** in
  `step_location_map` / properties / `inventory_links` / `dataset_mapping`. List any you could not place
  under `"unplaced"` (should be empty).
- Do NOT reuse live-only legacy types (`TEST_SPECIMEN`, `INSTRUMENT_DUMMY`, `STEP_STATUS`, …) — they are
  migrated, not extended. Their *domain content* may inform labels.
- Do NOT classify REUSE/EXTEND/CREATE, do NOT emit Python, do NOT call openBIS.
- Do NOT add data items that are not in requirements.json (exception: the "Next step" property and the
  SOP from P5, which the principles require).
- Run `python -c "import json; json.load(open('generated/<prd-stem>/design.json', encoding='utf-8'))"` before
  returning.

## Final response

Path of both files, the tree, the metrics table (new vs legacy), and the `unplaced` list.
