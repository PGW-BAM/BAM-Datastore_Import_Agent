# BAM openBIS PRD-to-Provisioning Agent Architecture

A reusable Claude Code agent + command architecture for BAM FB 7.2 and other BAM groups.

## Current state (06.10.2026)

Showcase for FB 7.2 (S-N tests on welded joints) re-run end-to-end with a **flat** structure:

| Artefact | Path |
|---|---|
| PRD v2 (workflow + principles) | `BAM_PRD_Workflow_FB72_v2.md` |
| Catalog of the standard (script) | `generated/CATALOG.md`, `generated/catalog.json` |
| Live inventory of dev1 (read-only) | `generated/live/dev1_inventory.md` |
| Requirements → design → gap report | `generated/welded_fatigue_v2/{requirements.json, design.md, gap-report.md}` |
| PR-ready classes + spec | `generated/welded_fatigue_v2/datamodel/`, `spec.json` |
| Provisioned on dev1 | `/FB_72/WELDED_FATIGUE` (demo series, fictitious values) via `tools/openbis_apply.js`, `tools/openbis_demo.js` |
| Notebook / parser | `notebooks/welded_fatigue_v2_provisioning.ipynb`, `generated/welded_fatigue_v2/parsers/` |
| Talk (10 min) | `presentation/00_Vortrag_10min.md`, `presentation/06_Befunde_und_Entscheidungen.md` |
| Cleanup of the legacy model | `generated/welded_fatigue_v2/CLEANUP_dev1.md` |

The v1 run (`BAM_PRD_Workflow_FB72.md`, `generated/welded_fatigue/`, `shipping/`) is kept for comparison.

## What it does

Drop a Markdown PRD into this folder. The pipeline:
1. Catalogs all existing types in `bam-masterdata` with a deterministic script (`tools/build_catalog.py`)
2. Inventories the target openBIS instance read-only (what is already there?)
3. Extracts the workflow from the PRD and designs a **flat** structure (`structure-designer`)
4. Produces a **gap report** against both sources: REUSE / EXTEND / CREATE / LIVE-ONLY
5. Generates Python extension modules (PR-ready for `BAMresearch/bam-masterdata`) only for genuine gaps — import-tested
6. Applies missing masterdata + object layout idempotently (dry run first), and emits notebook + parser for operators

## Prerequisites

- [Claude Code](https://claude.ai/code) with claude-sonnet-4-6 or better
- `pybis==1.37.4` (`pip install pybis==1.37.4`)
- `nbformat` (`pip install nbformat`)
- Access to a BAM openBIS 20.10.12.5 instance
- `bam-masterdata` cloned next to this repo at `../bam-masterdata` (or run `/bam-sync` first)

**Cloud sessions (Claude Code on the web):** the agent has no network path to openBIS. Setup runs
automatically (`tools/cloud_setup.sh` via SessionStart hook); the instance is reached only through
committed handover files — inventory in (`tools/openbis_inventory.js`), spec out (`tools/openbis_apply.js`,
`tools/openbis_demo.js`). See [CLOUD.md](CLOUD.md).

## Quick start

```bash
# 1. Sync bam-masterdata (first time or to update)
/bam-sync

# 2. Analyze your PRD (produces CATALOG.md + gap-report.md)
/bam-analyze-prd BAM_PRD_Workflow_FB72.md

# 3. Review generated/BAM_PRD_Workflow_FB72.gap-report.md

# 4. Generate Python extension modules (for CREATE items only)
/bam-generate-types BAM_PRD_Workflow_FB72.md

# 5. Generate the provisioning notebook
/bam-generate-notebook BAM_PRD_Workflow_FB72.md

# 6. Open notebooks/welded_fatigue_provisioning.ipynb
#    Fill in OPENBIS_URL, SPACE, PROJECT_CODE, COLLECTION_CODE
#    Run all cells
```

## Improving agents (Karpathy self-improvement loop)

```bash
/bam-improve bam-masterdata-explorer
```

See `.claude/skills/karpathy-self-improvement/SKILL.md` for the 7-step loop.

## Directory layout

```
.claude/
  agents/      # Domain agents (bam-masterdata-explorer, gap-analyzer, ...)
  commands/    # Slash commands (/bam-sync, /bam-analyze-prd, ...)
  skills/      # karpathy-self-improvement skill
runs/          # Karpathy improvement run logs
evals/
  regressions/ # Golden regression task files
notebooks/     # Generated Jupyter notebooks
generated/     # Generated masterdata extension modules (PR candidates)
```

## openBIS version

Targeting **openBIS 20.10.12.5** with `pybis==1.37.4`.

## License

Internal BAM tooling. Not for public distribution without explicit approval.
