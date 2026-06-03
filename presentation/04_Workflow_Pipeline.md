# End-to-End Workflow Pipeline

A narrated walk-through of one complete run, from a written PRD to deployable tooling.
Use this as the "demo storyboard" for a live presentation.

---

## Stage 0 — Sync the standard

```
Operator:  /bam-sync
```

- Pulls the latest `BAMresearch/bam-masterdata` (the shared data-model standard).
- Refuses to overwrite local changes; never force-pushes or resets.
- Prints the resolved commit **SHA** — every downstream artifact is tagged with it for reproducibility.

**Artifact:** a clean `bam-masterdata/` working tree + a known SHA.

---

## Stage 1 — Analyze the PRD (3 agents, one command)

```
Operator:  /bam-analyze-prd BAM_PRD_Workflow_FB72.md
```

| Step | Agent | Produces | In plain English |
|---|---|---|---|
| 1a | **bam-masterdata-explorer** | `generated/CATALOG.md` | "Here is everything the standard already contains." |
| 1b | **prd-requirements-extractor** | `generated/<stem>/requirements.json` | "Here is everything the PRD asks for." |
| 1c | **gap-analyzer** | `generated/<stem>/gap-report.md` | "For each requirement: reuse, extend, or build new." |

> Step 1a is **skipped** if the catalog's SHA already matches the synced `bam-masterdata` HEAD (idempotency).

### ⏸ HUMAN REVIEW CHECKPOINT ⏸

The pipeline **halts**. A reviewer reads `gap-report.md` and confirms the REUSE / EXTEND / CREATE
verdicts are correct before any code is generated. *Nothing is generated automatically.*

---

## Stage 2 — Generate deliverables (parallel, after approval)

Once the gap report is approved, run any/all of:

### 2a — Data-model code

```
Operator:  /bam-generate-types BAM_PRD_Workflow_FB72.md
```

- **masterdata-extender** emits declarative Python classes — **only** for CREATE items.
- It **hard-refuses** to emit code for REUSE/EXTEND (prevents duplicate types in the database).
- Self-verifies: the generated `.py` files must parse, and must contain no forbidden API calls.

**Artifact:** `generated/<stem>/datamodel/{vocabularies.py, object_types.py, README.md}` → becomes a PR to `bam-masterdata`.

### 2b — Provisioning notebook (one-time setup path)

```
Operator:  /bam-generate-notebook BAM_PRD_Workflow_FB72.md
```

- **openbis-notebook-generator** emits a **14-cell** Jupyter notebook.
- Authenticates via a **Personal Access Token** (PAT) — exactly one credential prompt, no hardcoded secrets.
- Creates the Space / Project / Collection hierarchy + parent specimen objects.

**Artifact:** `notebooks/<stem>_provisioning.ipynb`.

### 2c — Parser package (ongoing ingestion path)

```
Operator:  /bam-generate-parser BAM_PRD_Workflow_FB72.md
```

- **openbis-parser-generator** scaffolds an `AbstractParser` subclass per workflow cluster.
- Parser code is **pyBIS-free** — it populates an in-memory collection; the framework handles the database.
- Ships with smoke tests and `pip install -e` packaging.

**Artifact:** `generated/<stem>/parsers/` package.

---

## The two-path model (why 2b and 2c are separate)

| | Notebook (2b) | Parser (2c) |
|---|---|---|
| **Purpose** | Build the structure once | Push data repeatedly |
| **Frequency** | One-time | Every experiment |
| **Analogy** | Pouring the foundation | Driving on the road every day |

> *Diagram: `diagrams/05_two_path_provisioning.mmd`.*

---

## Stage 3 (meta) — Improve an agent from real failures

```
Operator:  /bam-improve gap-analyzer --runs 3
```

The **Karpathy 7-step loop** (see `diagrams/04_self_improvement_loop.mmd`):

1. **Run** the agent → capture `runs/<ts>/` (transcript, outputs, SHA).
2. **Persist** the run immutably.
3. **Score** via **skill-reviewer** → `review.json` (failures get stable IDs `F001…`).
4. **Critique → Diff** via **prompt-surgeon** → `proposed.diff` (every hunk cites a failure ID).
5. **Approve** — human reviews the diff. *No auto-apply.*
6. **Apply + version** — `git apply`, commit, bump agent version.
7. **Regress** — re-run the regression suite; **revert automatically** if any score drops.

> The loop refuses to touch "frozen" sections (Allowed APIs / Anti-patterns) — those are governed by evidence in `PLAN.md`, not by run data.

---

## Full artifact-flow summary

```
PRD.md
  │  /bam-sync ........................ bam-masterdata @ SHA
  ▼
/bam-analyze-prd
  ├─ explorer ........................ CATALOG.md
  ├─ extractor ....................... requirements.json
  └─ gap-analyzer .................... gap-report.md   ──⏸ HUMAN REVIEW ⏸
                                            │
        ┌───────────────────────────────────┼───────────────────────────────┐
        ▼                                   ▼                                 ▼
/bam-generate-types              /bam-generate-notebook            /bam-generate-parser
  masterdata-extender              notebook-generator                 parser-generator
  → datamodel/*.py                 → *_provisioning.ipynb             → parsers/ package
  (PR to bam-masterdata)           (one-time DB setup)                (per-run ingestion)
```
