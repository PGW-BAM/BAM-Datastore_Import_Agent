# /bam-analyze-prd

Run the full PRD analysis pipeline: catalog → requirements → gap report.

## Usage

```
/bam-analyze-prd <prd-path>
```

Examples:
```
/bam-analyze-prd BAM_PRD_Workflow_FB72.md
/bam-analyze-prd evals/regressions/BAM_PRD_Workflow_FB72_original.md
```

## What this command does

Runs three agents in sequence:

1. **`bam-masterdata-explorer`** (skipped if `generated/CATALOG.md` SHA matches current `../bam-masterdata` HEAD)
   → `generated/CATALOG.md`

2. **`prd-requirements-extractor`**
   → `generated/<prd-stem>/requirements.json`

3. **`gap-analyzer`**
   → `generated/<prd-stem>/gap-report.md`

Then **stops for human review** of the gap report. Do NOT auto-proceed to `/bam-generate-types` without reviewing the gap report first.

## Pre-requisites

- [ ] `../bam-masterdata/` exists (run `/bam-sync` if not).
- [ ] PRD file exists at the provided path.

## Pipeline

### Step 1 — Sync check
Run `/bam-sync` first (or confirm `../bam-masterdata` is current). Record the resolved commit SHA — the catalog will be tagged with it.

### Step 2 — Build/refresh CATALOG
Invoke the `bam-masterdata-explorer` agent:
- Input: `../bam-masterdata/` working tree
- Output: `generated/CATALOG.md`
- Skip if CATALOG.md SHA matches current `git -C ../bam-masterdata rev-parse HEAD`

### Step 3 — Extract requirements
Invoke the `prd-requirements-extractor` agent:
- Input: `$ARGUMENTS` (the PRD path)
- Output: `generated/<prd-stem>/requirements.json`

Derive `<prd-stem>` from the PRD filename (snake_case stem). For `BAM_PRD_Workflow_FB72.md` use `welded_fatigue` (consistent with existing `generated/` directories).

### Step 4 — Gap analysis
Invoke the `gap-analyzer` agent:
- Input: `generated/<prd-stem>/requirements.json` + `generated/CATALOG.md`
- Output: `generated/<prd-stem>/gap-report.md`

### Step 5 — Human review checkpoint

Print:

```
════════════════════════════════════════════════════════
  Gap report ready: generated/<prd-stem>/gap-report.md
════════════════════════════════════════════════════════

Review the gap report, especially:
  [ ] All REUSE entries have valid file:line citations
  [ ] EXTEND entries list only realistic additions (PR-grade, not rewrites)
  [ ] CREATE entries are genuinely absent from bam-masterdata
  [ ] WELDING.WELD_TYPE appears as EXTEND (not CREATE)
  [ ] TestingMachine appears as REUSE (not CREATE)
  [ ] All 12 ExperimentalSteps appear as CREATE

When satisfied, run:
  /bam-generate-types <prd-path>
  /bam-generate-notebook <prd-path>
  /bam-generate-parser <prd-path>
```

## Anti-patterns
- Do NOT auto-run `/bam-generate-types` after this command — human review is mandatory.
- Do NOT re-run `bam-masterdata-explorer` if CATALOG SHA is current (idempotency).
- Do NOT skip the catalog refresh check — stale CATALOG.md leads to wrong REUSE/CREATE classifications.
