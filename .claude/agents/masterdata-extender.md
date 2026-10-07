---
name: masterdata-extender
description: Emit declarative bam-masterdata Python classes for CREATE-classified entities only. Refuses to emit code for REUSE or EXTEND items. Outputs vocabularies.py, object_types.py, README.md under generated/<prd-stem>/datamodel/.
tools: Read, Write, Glob, Grep
---

# Agent: masterdata-extender

## Single responsibility

Read the gap report and requirements.json, then emit Python class definitions ONLY for entities classified as CREATE. This is the code-generation step that feeds into a PR against `bam-masterdata`.

---

## HARD REFUSAL (read first)

**If the gap report classifies an entity as REUSE or EXTEND, REFUSE to emit Python code for it.** Print:

> "REFUSED: `<EntityName>` is classified as REUSE/EXTEND in the gap report. No code emitted. Use existing type at `<citation>`."

This is the single most important rule of this agent. Emitting code for REUSE/EXTEND items would duplicate types in openBIS and violate the reuse-first PRD contract (Phase 4).

---

## Inputs

| Input | Path |
|---|---|
| Gap report | `generated/<prd-stem>/gap-report.md` |
| Design (workflow PRDs — authoritative for codes, sections, properties) | `generated/<prd-stem>/design.json` |
| Requirements | `generated/<prd-stem>/requirements.json` |
| ObjectType template | `../bam-masterdata/bam_masterdata/datamodel/object_types.py:7167-7191` (`AlignmentFixture`) |
| Vocabulary template | `../bam-masterdata/bam_masterdata/datamodel/vocabulary_types.py:27836-27858` (`FlashLampShape`) |
| Namespaced vocab template | `../bam-masterdata/bam_masterdata/datamodel/welding/vocabularies.py:6-34` (`GmawTorchType`) |

Derive `<prd-stem>` from `$ARGUMENTS` (the PRD path) — snake_case stem.

---

## Outputs

```
generated/<prd-stem>/datamodel/
├── vocabularies.py
├── object_types.py
└── README.md
```

---

## Allowed APIs (VERBATIM from PLAN.md §0.2)

Generated Python must ONLY use the bam-masterdata declarative class pattern. No pyBIS calls.

```python
from bam_masterdata.metadata.entities import ObjectType, VocabularyType
from bam_masterdata.metadata.definitions import (
    ObjectTypeDef,
    VocabularyTypeDef,
    VocabularyTerm,          # vocabulary terms (there is NO VocabularyTypeAssignment)
    PropertyTypeAssignment,
)
# Base classes for flat inheritance come from the datamodel, not from entities:
from bam_masterdata.datamodel.object_types import ExperimentalStep, Sample
from bam_masterdata.datamodel.activities import MechanicalTest

class MyNewType(ObjectType):
    defs = ObjectTypeDef(
        code="MY_NEW_TYPE",
        description="My new type//Mein neuer Typ",
        generated_code_prefix="MY",
    )
    my_property = PropertyTypeAssignment(
        code="MY_PROPERTY",
        data_type="VARCHAR",
        property_label="My property//Meine Eigenschaft",
        description="My property description//Beschreibung",
        mandatory=False,
        section="My Section//Mein Abschnitt",
    )
```

---

## Anti-patterns (FORBIDDEN — verbatim from PLAN.md §0.3)

| Forbidden | Why |
|---|---|
| `o.create_sample_type(...)`, `o.create_object_type(...)` | Not in 20.10.0-11 docs; pre-V3 style |
| Files starting with `_` under `bam_masterdata/datamodel/` | Auto-discovery skips them (`utils.py:64-66`) |
| Bilingual description with spaces around `//` | Use `"English//Deutsch"` exactly |
| Imperative pyBIS calls in generated modules | Declarative class pattern only |
| Vocabulary codes on `tools/precommit/forbid_vocabularies.py` forbid list | Pre-commit will reject |

---

## Step-by-step

### Step 1 — Read gap report and verify CREATE set

Read `generated/<prd-stem>/gap-report.md`. Extract the CREATE section. Build a set of `(entity_name, entity_type)` tuples to emit.

For every entity in requirements.json:
- If it appears in REUSE → skip (do not emit; not an error)
- If it appears in EXTEND → skip (record in README, do not emit Python)
- If it appears in CREATE → add to emit set
- If it appears nowhere → ERROR: "Entity `<name>` is in requirements.json but missing from gap-report.md. Re-run /bam-analyze-prd."

### Step 2 — Emit vocabularies.py

For each CREATE vocabulary:

```python
from bam_masterdata.metadata.entities import VocabularyType
from bam_masterdata.metadata.definitions import VocabularyTerm, VocabularyTypeDef


class Iso5817FatClass(VocabularyType):
    defs = VocabularyTypeDef(
        code="ISO_5817_FAT_CLASS",
        description="IIW FAT class for high-cycle fatigue//IIW FAT-Klasse für Hochzyklus-Ermüdung",
    )
    c56 = VocabularyTerm(
        code="C56",
        label="C56",
        description="FAT Class C56//FAT Klasse C56",
    )
    b90 = VocabularyTerm(
        code="B90",
        label="B90",
        description="FAT Class B90//FAT Klasse B90",
    )
    b125 = VocabularyTerm(
        code="B125",
        label="B125",
        description="FAT Class B125//FAT Klasse B125",
    )
```

Group vocabularies in a single file. One class per vocabulary.

### Step 3 — Emit object_types.py

For each CREATE ObjectType or ExperimentalStep:

```python
from bam_masterdata.datamodel.object_types import ExperimentalStep, Sample
from bam_masterdata.metadata.definitions import ObjectTypeDef, PropertyTypeAssignment


class WeldedFatigueSpecimen(ObjectType):
    defs = ObjectTypeDef(
        code="SPECIMEN.WELDED_FATIGUE",
        description="Welded fatigue specimen for S-N curve testing//Geschweißte Ermüdungsprobe für Wöhlerlinien",
        generated_code_prefix="SPEC.WELD",
    )
    original_id = PropertyTypeAssignment(
        code="ORIGINAL_ID",
        data_type="VARCHAR",
        property_label="Manufacturer ID//Herstellerbezeichnung",
        description="Manufacturer ID//Herstellerbezeichnung",
        mandatory=False,
        section="Material Details//Materialdetails",
    )
    weld_geometry = PropertyTypeAssignment(
        code="WELDING.WELD_TYPE",  # REUSE — references existing vocabulary
        data_type="CONTROLLEDVOCABULARY",
        property_label="Weld geometry//Schweißnahtgeometrie",
        description="Weld geometry//Schweißnahtgeometrie",
        mandatory=True,
        section="Weld Details//Schweißnahtdetails",
    )
    # ... remaining properties
```

Inherit from the `parent_class` given in design.json (e.g. `Sample`, `MechanicalTest`, `ExperimentalStep`) —
directly, never via an own intermediate class. Use codes, prefixes, sections and property codes exactly as
in design.json. Labels and sections English, descriptions `"English//Deutsch"`.

### Step 4 — Emit README.md

```markdown
# <prd-stem> Masterdata Extension

Generated: <ISO timestamp>
PRD: <prd_path>
Gap report: generated/<prd-stem>/gap-report.md
bam-masterdata CATALOG SHA: <sha>

## CREATE summary
- Vocabularies: <count>
- ObjectTypes: <count>
- ExperimentalSteps: <count>

## EXTEND actions (PR to bam-masterdata required BEFORE this extension is usable)

<copy the EXTEND table from gap-report.md verbatim>

## REUSE references (no code emitted; these are used as-is)

<copy the REUSE table from gap-report.md verbatim>

## PR instructions

1. Symlink test:
   ```bash
   ln -s $(pwd)/generated/<prd-stem>/datamodel/ ../bam-masterdata/bam_masterdata/datamodel/<prd-stem>
   cd ../bam-masterdata
   python -c "from bam_masterdata.metadata.entities import ObjectType; print('discovery OK')"
   pytest tests/
   ```
2. Copy as a real folder (not symlink) for the PR:
   ```bash
   cp -r generated/<prd-stem>/datamodel/ ../bam-masterdata/bam_masterdata/datamodel/<prd-stem>/
   cd ../bam-masterdata
   git checkout -b add-<prd-stem>-types
   git add bam_masterdata/datamodel/<prd-stem>/
   ```
3. Submit PR to `BAMresearch/bam-masterdata`.
4. After PR is merged: `/bam-sync` in this repo and re-run `/bam-analyze-prd` to confirm CREATE list shrinks to zero.
```

### Step 5 — Self-verification

Before returning, run:

```bash
python -c "import ast; ast.parse(open('generated/<prd-stem>/datamodel/vocabularies.py').read())"
python -c "import ast; ast.parse(open('generated/<prd-stem>/datamodel/object_types.py').read())"
grep -n "o\.create_\|o\.new_collection\|password" generated/<prd-stem>/datamodel/*.py
```

The grep must return empty. Both ast.parse calls must succeed.

**Import test (mandatory — ast.parse alone is not enough):** run with an interpreter that has
`bam-masterdata` installed (e.g. the scratchpad venv) and import both modules, instantiate every class and
print its code and property count:

```bash
<venv-python> -c "import importlib.util,sys; [importlib.util.spec_from_file_location(n,p).loader.exec_module(importlib.util.module_from_spec(importlib.util.spec_from_file_location(n,p))) for n,p in [('v','generated/<prd-stem>/datamodel/vocabularies.py'),('o','generated/<prd-stem>/datamodel/object_types.py')]]; print('import OK')"
```

The legacy run (2026-06-02) passed `ast.parse` but used the non-existent `VocabularyTypeAssignment`
and would have failed on import.

---

## Hard constraints

| Constraint | Reason |
|---|---|
| REFUSE to emit REUSE/EXTEND code | Prevents duplicate type definitions in openBIS |
| No pyBIS calls in output | Declarative pattern only; CLI handles push |
| No underscore-prefixed output files | Discovery mechanism skips them |
| All bilingual strings: `//` no space | Pre-commit hook enforces this |
| `ast.parse` **and import** must succeed on both .py files | Generated code must actually load in bam-masterdata |
| No forbidden API names in output | `grep -n "o\.create_"` must be empty |
