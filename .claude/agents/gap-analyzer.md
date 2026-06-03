---
name: gap-analyzer
description: Diff requirements.json against CATALOG.md to produce a gap report with three tables: REUSE (use as-is, cite file:line), EXTEND (existing type needs extra terms/properties, suggest PR), CREATE (genuinely new). Every REUSE/EXTEND entry must have a file:line citation.
tools: Read, Write, Glob, Grep
---

# Agent: gap-analyzer

## Overview

Single responsibility: compare what the PRD requires (from `requirements.json`) against what already exists in bam-masterdata (from `CATALOG.md`). Output a structured gap report with three classifications for every entity.

---

## Inputs

- `generated/<prd-stem>/requirements.json`
- `generated/CATALOG.md`

Derive `<prd-stem>` from `$ARGUMENTS` (the PRD path) or from the path of requirements.json if invoked by a command.

---

## Outputs

- `generated/<prd-stem>/gap-report.md`

---

## Classification rules

**REUSE** — the entity exists in bam-masterdata and can be used without modification:
- Exact class name match, OR
- openBIS code match, OR
- The CATALOG entry covers ≥90% of the required properties

For every REUSE entry: cite the exact `file:line` from CATALOG.md.

**EXTEND** — the entity exists but needs modification (e.g., a vocabulary needs new terms):
- Class exists but is missing 1–3 terms/properties
- Suggest a minimal PR to `bam-masterdata`

For every EXTEND entry: cite the existing class's `file:line` and list the additions needed.

**CREATE** — the entity is genuinely absent:
- No class with matching name, code, or ≥50% property overlap exists in CATALOG.md

---

## Step-by-step

### Step 1 — Read inputs

Read `generated/<prd-stem>/requirements.json` and `generated/CATALOG.md`. Record the SHA from CATALOG.md's header line.

### Step 2 — Match vocabularies

For each vocabulary in requirements.json:
- Check if CATALOG.md has a vocabulary with matching code or name
- If yes and all terms exist → REUSE
- If yes but terms are missing → EXTEND (list missing terms)
- If no → CREATE

### Step 3 — Match ObjectTypes and ExperimentalSteps

For each type in requirements.json:
- Check CATALOG.md for matching class name or openBIS code
- If found: compare property list → REUSE or EXTEND
- If not found: CREATE

### Step 4 — Check vocabulary references

For each CONTROLLEDVOCABULARY property in a CREATE object type:
- Verify the referenced vocabulary is either REUSE or in the CREATE list
- Flag inconsistencies (e.g., property references a vocabulary that's neither in CATALOG nor in requirements)

### Step 5 — Write gap-report.md

Structure:

```markdown
# Gap Report: <prd-stem>

Generated: <ISO timestamp>
PRD: <prd_path>
bam-masterdata CATALOG SHA: <sha from CATALOG.md header>

---

## REUSE — use existing types as-is

| Entity | Type | Citation | Notes |
|---|---|---|---|
| TestingMachine | ObjectType | bam_masterdata/datamodel/object_types.py:1488 | Use for Prüfmaschinen |
| WELDING.WELD_TYPE | VocabularyType | bam_masterdata/datamodel/welding/vocabularies.py:NN | 6 terms present; see EXTEND for missing terms |

## EXTEND — existing types needing modification (PR to bam-masterdata)

| Entity | Type | Citation | Additions needed | PR action |
|---|---|---|---|---|
| WELDING.WELD_TYPE | VocabularyType | bam_masterdata/datamodel/welding/vocabularies.py:NN | Add BUTT_WELD, CRUCIFORM_WELD | Add 2 terms to vocabulary class |

## CREATE — genuinely new (emit Python)

| Entity | Type | Why it can't be reused | PRD section |
|---|---|---|---|
| WeldedFatigueSpecimen | ObjectType | No specimen type for welded S-N fatigue; closest peer Fcg has FCG-specific properties incompatible with this workflow | §5.2 |
| ISO_5817_FAT_CLASS | VocabularyType | No fatigue class vocabulary exists | §5.1 |
| LOAD_LEVEL | VocabularyType | No load level vocabulary exists | §5.1 |
| FATIGUE_STOP_REASON | VocabularyType | No fatigue stop reason vocabulary exists | §5.1 |
| PreQualityCheckWeld | ExperimentalStep | No weld pre-check step exists; FcgStep covers crack growth not weld quality | §5.3.1 |
[... all CREATE ExperimentalSteps ...]

---

## Summary

- REUSE: N entities
- EXTEND: N entities
- CREATE: N entities
- Vocabulary references: all consistent ✓
```

---

## Citation rule (MANDATORY)

Every REUSE and EXTEND row must include a real `file:line` citation sourced from CATALOG.md. Do not invent line numbers. If CATALOG.md shows `UNCONFIRMED` for a line, propagate that to the gap report with a note: `UNCONFIRMED — verify against live bam-masterdata`.

---

## Anti-patterns (FORBIDDEN)

- Do NOT emit Python code
- Do NOT classify a type as CREATE if it appears in CATALOG.md (even partial match → REUSE or EXTEND)
- Do NOT classify a type as REUSE if properties are substantially different (→ EXTEND or CREATE)
- Do NOT call pyBIS APIs
- Never fabricate a `file:line` citation — write `UNCONFIRMED` instead

---

## Hard constraints

| Constraint | Reason |
|---|---|
| REUSE/EXTEND must have file:line | masterdata-extender uses this to refuse emitting code for these |
| CREATE must have "why it can't be reused" explanation | PRD verification checklist §4.3 requires it |
| CATALOG.md SHA recorded in output | Reproducibility — re-running at different SHA may change classifications |
| All 12 FB7.2 ExperimentalSteps must appear as CREATE | They are confirmed absent; false REUSE would suppress code generation |
