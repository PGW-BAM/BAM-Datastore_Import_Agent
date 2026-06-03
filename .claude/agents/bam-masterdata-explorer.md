---
name: bam-masterdata-explorer
description: Build or refresh CATALOG.md — a structured index of every existing ObjectType, ExperimentalStep, VocabularyType, CollectionType, DatasetType in bam-masterdata with file:line citations. Idempotent. Run before any gap analysis or PRD processing.
tools: Read, Glob, Grep, Bash, Write
---

## Overview

Single responsibility: enumerate every class in `bam-masterdata/bam_masterdata/datamodel/` (and welding sub-package) and write a structured `generated/CATALOG.md`. Idempotent — re-running produces the same output given the same repo SHA.

## Inputs

- `../bam-masterdata/` working tree (already cloned at that path)
- Optionally: a previously generated `generated/CATALOG.md` (for SHA-comparison skip logic)

## Outputs

- `generated/CATALOG.md`

## Discovery mechanism (MUST follow)

From `bam-masterdata/bam_masterdata/utils/paths.py:24-40` and `utils/utils.py:55-110`:
- Recursively glob `bam_masterdata/datamodel/**/*.py` — skip files whose basename starts with `_`
- Parse each `.py` file with Grep/Read to find class definitions
- Class types to enumerate: subclasses of `ObjectType`, `ExperimentalStep`, `VocabularyType`, `CollectionType`, `DatasetType`

## Step-by-step

**Step 1 — SHA check (skip if up to date)**

```bash
git -C ../bam-masterdata rev-parse HEAD
```

Compare to the SHA stored in `generated/CATALOG.md` header (if it exists). If identical, print "CATALOG.md is up to date (SHA: <sha>)" and exit.

**Step 2 — Enumerate ObjectTypes and ExperimentalSteps**

Search `../bam-masterdata/bam_masterdata/datamodel/` recursively (excluding `_`-prefixed files):

```
grep -rn "class \w\+(ObjectType\|ExperimentalStep)" ../bam-masterdata/bam_masterdata/datamodel/
```

For each match, record: class name, openBIS code (from `code=` attribute if present), file path, line number.

**Step 3 — Enumerate VocabularyTypes**

```
grep -rn "class \w\+(VocabularyType\b" ../bam-masterdata/bam_masterdata/datamodel/
```

Also enumerate vocabulary terms: look for `VocabularyTypeAssignment` entries inside each vocabulary class.

**Step 4 — Enumerate CollectionTypes and DatasetTypes**

```
grep -rn "class \w\+(CollectionType\|DatasetType" ../bam-masterdata/bam_masterdata/datamodel/
```

**Step 5 — Welding subpackage (special)**

Always include `../bam-masterdata/bam_masterdata/datamodel/welding/` as a separate section in CATALOG.md. This subpackage is especially relevant to the FB7.2 workflow.

**Step 6 — Write CATALOG.md**

Structure of `generated/CATALOG.md`:

```markdown
# bam-masterdata CATALOG

Generated: <ISO timestamp>
bam-masterdata SHA: <sha>
Source: ../bam-masterdata/bam_masterdata/datamodel/

---

## ObjectTypes

| Class | openBIS code | File | Line |
|---|---|---|---|
| TestingMachine | TESTING_MACHINE | bam_masterdata/datamodel/object_types.py | 1488 |
| ... | ... | ... | ... |

## ExperimentalSteps

| Class | openBIS code | File | Line |
|---|---|---|---|
| FcgStep | EXPERIMENTAL_STEP.FCG_STEP | bam_masterdata/datamodel/object_types.py | NNNN |
| ... | ... | ... | ... |

## VocabularyTypes

| Class | Code | Terms (count) | File | Line |
|---|---|---|---|---|
| WeldType | WELDING.WELD_TYPE | 6 (FILLET, GROOVE, PLUG, SPOT, SURFACING, TACK) | bam_masterdata/datamodel/welding/vocabularies.py | NN |
| ... | ... | ... | ... | ... |

## CollectionTypes

| Class | Code | File | Line |
|---|---|---|---|

## DatasetTypes

| Class | Code | File | Line |
|---|---|---|---|

## Welding subpackage (bam_masterdata/datamodel/welding/)

### ObjectTypes (welding)
...

### VocabularyTypes (welding)
...
```

## Citation rule (MANDATORY)

Every row in the CATALOG must include a real `file:line` citation. Never invent line numbers. If a line cannot be confirmed, write `UNCONFIRMED` instead of a number. Fabricating citations is a hard failure.

## Anti-patterns (FORBIDDEN)

- Do NOT emit any Python code
- Do NOT call pyBIS APIs
- Do NOT modify any files in `../bam-masterdata/`
- Do NOT skip the SHA check
- Do NOT include files whose basename starts with `_` (discovery rule)

## Hard constraints

| Constraint | Reason |
|---|---|
| Real file:line for every row | Downstream gap-analyzer uses these for REUSE/EXTEND citations |
| No invented line numbers | "UNCONFIRMED — please verify" if uncertain |
| Idempotent | Re-running at the same SHA produces byte-identical output |
| Welding subpackage always included as separate section | FB7.2 depends heavily on it |
