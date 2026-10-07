# /bam-analyze-prd

Run the full PRD analysis pipeline: catalog → (live inventory) → requirements → structure design → gap report.

## Usage

```
/bam-analyze-prd <prd-path> [prd-stem]
```

Examples:
```
/bam-analyze-prd BAM_PRD_Workflow_FB72_v2.md welded_fatigue_v2     # workflow-style PRD (current)
/bam-analyze-prd BAM_PRD_Workflow_FB72.md welded_fatigue           # legacy type-style PRD
```

## Pipeline

| # | Step | Agent / tool | Output |
|---|---|---|---|
| 1 | Sync standard | `/bam-sync` (fast-forward only) | `../bam-masterdata` at origin/main |
| 2 | Catalog the standard | `bam-masterdata-explorer` → `python tools/build_catalog.py` | `generated/CATALOG.md`, `generated/catalog.json` |
| 3 | Inventory the instance (optional, recommended) | browser session on the target instance, **read-only** V3 `search*` calls | `generated/live/<instance>_inventory.md` |
| 4 | Transcribe the PRD | `prd-requirements-extractor` | `generated/<stem>/requirements.json` |
| 5 | Design a flat structure (workflow PRDs only) | `structure-designer` | `generated/<stem>/design.json`, `design.md` |
| 6 | Classify | `gap-analyzer` (REUSE / EXTEND / CREATE / LIVE-ONLY) | `generated/<stem>/gap-report.md` |
| 7 | **Human review** | — | stop |

Step 2 is skipped if the CATALOG SHA equals `git -C ../bam-masterdata rev-parse HEAD`.
Step 3 must never write to the instance. Credentials are never typed by an agent — the user signs in
in the browser and the agent reuses that session, or the user runs a script with their own token.

## Human review checkpoint

```
════════════════════════════════════════════════════════
  Design:     generated/<stem>/design.md
  Gap report: generated/<stem>/gap-report.md
════════════════════════════════════════════════════════
Check:
  [ ] Every workflow step has exactly one location (design.md step→location table)
  [ ] Max link depth = 1 (specimen → step); no step→step chains
  [ ] REUSE/EXTEND rows cite file:line; LIVE-ONLY rows name their replacement
  [ ] No new dataset types; no live-only legacy type reused
  [ ] Domain decisions from the PRD are reflected verbatim

Then: /bam-generate-types <prd> <stem> → provisioning (/bam-generate-notebook) → /bam-generate-parser
```

## Anti-patterns
- Do NOT auto-run `/bam-generate-types` — human review is mandatory.
- Do NOT skip the catalog refresh check — a stale catalog causes false CREATE classifications.
- Do NOT treat the live instance as the standard: live-only types are migrated or proposed for PR, not reused.
