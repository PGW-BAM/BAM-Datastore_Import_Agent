---
name: bam-masterdata-explorer
description: Build or refresh CATALOG.md + catalog.json — a structured index of every existing ObjectType, ExperimentalStep, VocabularyType, CollectionType, DatasetType and PropertyType in bam-masterdata with file:line citations. Runs the deterministic AST script tools/build_catalog.py. Idempotent. Run before any gap analysis or PRD processing.
tools: Read, Glob, Grep, Bash, Write
---

## Overview

Single responsibility: produce `generated/CATALOG.md` (human-readable) and `generated/catalog.json`
(machine-readable, incl. own + inherited properties and vocabulary terms) for the current
`../bam-masterdata` working tree.

**Enumeration is done by a script, not by the LLM.** The previous grep-based approach
(`class X(ObjectType|ExperimentalStep)`) only found *direct* subclasses and silently missed every
type inheriting from `Instrument`, `Sample`, `MechanicalTest`, … (run 2026-06-02: 8 instrument types
reported as "UNCONFIRMED" although they existed). `tools/build_catalog.py` parses every module with
`ast` and resolves the full inheritance chain.

## Step-by-step

**Step 1 — SHA check (skip if up to date)**

```bash
git -C ../bam-masterdata rev-parse HEAD
head -3 generated/CATALOG.md
```

If the SHA in the header equals HEAD, print "CATALOG.md is up to date (SHA: <sha>)" and stop.

**Step 2 — Build**

```bash
python tools/build_catalog.py
```

Expected output: one line `SHA <8>: CollectionType=…, DatasetType=…, ExperimentalStep=…, ObjectType=…, VocabularyType=…`.

**Step 3 — Verify idempotency**

Run the script a second time and confirm `generated/CATALOG.md` is byte-identical (e.g. compare `md5sum`).

**Step 4 — Report**

Return the counts line, the SHA and any classes whose root could not be resolved (root = null in catalog.json).

## Anti-patterns (FORBIDDEN)

- Do NOT hand-write or hand-edit CATALOG.md — always regenerate via the script
- Do NOT modify any files in `../bam-masterdata/`
- Do NOT invent line numbers

## Hard constraints

| Constraint | Reason |
|---|---|
| Script-generated, byte-identical on re-run | Downstream citations must be reproducible |
| Full inheritance resolution | Subclasses of Instrument/Sample/MechanicalTest must be visible |
| Property index included | gap-analyzer reuses existing PropertyType codes |
