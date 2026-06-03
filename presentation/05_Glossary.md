# Glossary

For newcomers and non-technical stakeholders. Keep this slide handy as an appendix.

---

## Domain terms

| Term | Plain-language meaning |
|---|---|
| **openBIS** | The research-data management database/platform the lab uses to store experiments, samples, and results. |
| **pyBIS** | The Python library used to talk to openBIS programmatically (version 1.37.4 here). |
| **bam-masterdata** | The shared, standardised catalogue of data types (the "master data model") maintained by BAM. The single source of truth this system reuses from. |
| **PRD** | *Product Requirements Document* — the written specification of a lab workflow (e.g. welded-fatigue testing) that drives the whole pipeline. |
| **FB7.2 / welded_fatigue** | The example workflow used throughout: fatigue testing of welded specimens to produce S-N (Wöhler) curves. |
| **Masterdata** | The *definitions* of data types (not the data itself): ObjectTypes, VocabularyTypes, etc. |

---

## Data-model building blocks

| Term | Meaning |
|---|---|
| **ObjectType** | A class of thing you can store (e.g. a `TestingMachine`, a `WeldedFatigueSpecimen`). |
| **ExperimentalStep** | A special ObjectType representing one step in a workflow (e.g. `CyclicFatigueTest`). |
| **VocabularyType** | A controlled list of allowed values (e.g. weld geometries: `BUTT_WELD`, `FILLET`…). |
| **CollectionType / Experiment** | A container grouping related objects in openBIS. |
| **DatasetType** | A type describing attached data files. |
| **PropertyTypeAssignment** | A single property on a type (name, data type, label, mandatory flag). |
| **Bilingual description** | Labels stored as `"English//Deutsch"` (no spaces around `//`) — a BAM convention. |

---

## Pipeline artifacts

| Artifact | What it is |
|---|---|
| **CATALOG.md** | An index of every type that already exists in `bam-masterdata`, with `file:line` citations. |
| **requirements.json** | A normalised, machine-readable list of everything the PRD requires. |
| **gap-report.md** | The REUSE / EXTEND / CREATE verdict for each requirement. The key decision document. |
| **datamodel/*.py** | Generated Python class definitions for the genuinely-new (CREATE) types. |
| **provisioning notebook** | A Jupyter notebook that sets up the openBIS structure once. |
| **parser package** | Reusable code that ingests data after each experiment. |
| **review.json** | A scored evaluation of an agent run, with failure IDs. |
| **proposed.diff** | A minimal, evidence-cited patch to an agent's instructions. |

---

## The three verdicts

| Verdict | Meaning | Generates code? |
|---|---|---|
| **REUSE** | Already exists, fits as-is | No |
| **EXTEND** | Exists, needs 1–3 small additions (→ minimal PR) | No |
| **CREATE** | Genuinely new | Yes |

---

## Architecture / Claude Code terms

| Term | Meaning |
|---|---|
| **Agent (subagent)** | A specialised AI worker defined by a `.md` file in `.claude/agents/`, with its own tool allowlist. |
| **Command (slash-command)** | An operator entry point defined in `.claude/commands/`, e.g. `/bam-sync`. Orchestrates agents. |
| **Skill** | Reusable procedural knowledge in `.claude/skills/` (e.g. the self-improvement loop). |
| **Tool allowlist** | The explicit set of tools an agent may use (Read, Write, Grep…). Least-privilege. |
| **Auto-discovery** | Claude Code finds commands/agents/skills automatically from their folders — no registry. |
| **Human-in-the-loop** | Deliberate pause points where a person must approve before the system proceeds. |
| **Idempotency** | Re-running with the same inputs produces identical output (no surprises). |
| **Karpathy loop** | The 7-step "improve the agent from logged failures" feedback cycle. |
