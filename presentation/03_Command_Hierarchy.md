# Command Hierarchy

Commands are the **operator-facing entry points**. They are thin orchestrators: a command
decides *which agents run, in what order*, and *where the pipeline pauses for a human*.

> Mental model: **Commands orchestrate. Agents execute. Artifacts connect them.**

---

## The six commands, in execution order

```
/bam-sync                  ← 0. Refresh the shared standard (run first, always)
   │
/bam-analyze-prd <prd>     ← 1. DISCOVER + EXTRACT + DECIDE  (3 agents)
   │                           ⏸  HUMAN REVIEW CHECKPOINT
   ├── /bam-generate-types     <prd>   ← 2a. Python data-model classes
   ├── /bam-generate-notebook  <prd>   ← 2b. One-time provisioning notebook
   └── /bam-generate-parser    <prd>   ← 2c. Ongoing-ingestion parser package

/bam-improve <agent>       ← (meta) Self-improvement loop on any agent
```

---

## Command reference table

| Command | Orchestrates (agents) | Input | Produces | Stops for human? |
|---|---|---|---|---|
| `/bam-sync` | *(none — git only)* | — | Fresh `bam-masterdata` checkout + commit SHA | No |
| `/bam-analyze-prd <prd>` | explorer → extractor → gap-analyzer | PRD path | `CATALOG.md`, `requirements.json`, `gap-report.md` | **Yes** — mandatory gap-report review |
| `/bam-generate-types <prd>` | masterdata-extender | reviewed gap report | `datamodel/*.py` + `README.md` | No (but PR-gated downstream) |
| `/bam-generate-notebook <prd>` | openbis-notebook-generator | gap report + requirements | `*_provisioning.ipynb` (14 cells) | No |
| `/bam-generate-parser <prd>` | openbis-parser-generator | gap report + object types | `parsers/` package | No |
| `/bam-improve <agent> [--runs N]` | skill-reviewer → prompt-surgeon | captured `runs/<ts>/` | `review.json`, `proposed.diff`, `rationale.md` | **Yes** — approve diff before apply |

---

## The critical sequencing rule

```
/bam-sync  ➜  /bam-analyze-prd  ➜  ⏸ HUMAN REVIEW ⏸  ➜  generate-* commands
```

- **`/bam-sync` must run before any analysis** — a stale catalog produces wrong REUSE/CREATE verdicts.
- **`/bam-analyze-prd` deliberately stops** and prints a review checklist. It will **not** auto-proceed to code generation. This is a feature, not a limitation.
- The three `generate-*` commands can run **in any order** after review, but `generate-types` is conventionally first (the notebook + parser reference the types it defines).

---

## What the human checks at the review checkpoint

Printed by `/bam-analyze-prd` (abbreviated):

- [ ] All REUSE entries have valid `file:line` citations
- [ ] EXTEND entries list only realistic additions (PR-grade, not rewrites)
- [ ] CREATE entries are genuinely absent from the standard
- [ ] Known-reusable types (e.g. `WELDING.WELD_TYPE`, `TestingMachine`) are *not* wrongly classified as CREATE

---

## Auto-discovery note (for the technical audience)

Commands and agents are **auto-discovered** by Claude Code simply by placing a `.md` file in:

```
.claude/commands/   → slash-commands  (/bam-*)
.claude/agents/     → subagents       (invoked by commands)
.claude/skills/     → skills          (e.g. karpathy-self-improvement)
```

No central registry to edit — drop the file in, and it becomes invocable. This is what makes
the architecture cheap to extend: adding a new workflow stage = adding one agent file + one command file.
