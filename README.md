# BAM openBIS PRD-to-Provisioning Agent Architecture

A reusable Claude Code agent + command architecture for BAM FB 7.2 and other BAM groups.

## What it does

Drop a Markdown PRD into this folder. The pipeline:
1. Catalogs all existing types in `bam-masterdata` (ObjectTypes, Vocabularies, ExperimentalSteps)
2. Extracts required entities from the PRD
3. Produces a **gap report**: what to REUSE, what to EXTEND, what to CREATE (new)
4. Generates Python extension modules (PR-ready for `BAMresearch/bam-masterdata`) only for genuine gaps
5. Emits a Jupyter notebook that provisions your Collection + child Objects + Datasets in openBIS 20.10.12.5

## Prerequisites

- [Claude Code](https://claude.ai/code) with claude-sonnet-4-6 or better
- `pybis==1.37.4` (`pip install pybis==1.37.4`)
- `nbformat` (`pip install nbformat`)
- Access to a BAM openBIS 20.10.12.5 instance
- `bam-masterdata` cloned at `C:/Users/<you>/repos/bam-masterdata` (or run `/bam-sync` first)

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
