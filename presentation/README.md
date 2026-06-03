# BAM DataStore — Agent Architecture Documentation

> Presentation-ready documentation of the Claude Code agent system that turns a
> **PRD (Product Requirements Document)** into **openBIS-ready data-model code,
> provisioning notebooks, and ingestion parsers** — reuse-first, human-in-the-loop.

This folder is the single source of truth for business presentations (PowerPoint),
onboarding, and architecture reviews.

---

## How to read this folder

| File | Audience | Use it for |
|---|---|---|
| `01_Executive_Overview.md` | Management / non-technical | The "why" + one-paragraph pitch + slide bullets |
| `02_Agent_Roles.md` | Architects / leads | High-level table: each agent's role, inputs, outputs, guardrails |
| `03_Command_Hierarchy.md` | Operators / users | What each `/command` does and in which order to run them |
| `04_Workflow_Pipeline.md` | Everyone | End-to-end walkthrough with the artifact hand-offs |
| `05_Glossary.md` | Newcomers | Domain + technical terms (openBIS, pyBIS, PRD, masterdata…) |
| `diagrams/*.mmd` | Slide authors | [Mermaid.js](https://mermaid.live) source for every diagram |

---

## Rendering the diagrams (for slides)

All diagrams live in `diagrams/` as `.mmd` (Mermaid) files. To export PNG/SVG for PowerPoint:

1. **Quickest** — paste the `.mmd` content into <https://mermaid.live>, then *Export → PNG/SVG*.
2. **CLI** — `npx @mermaid-js/mermaid-cli -i diagrams/01_system_architecture.mmd -o architecture.png`
3. **VS Code** — install the *Markdown Preview Mermaid Support* extension; diagrams render inline in the `.md` files.

| Diagram file | Shows |
|---|---|
| `diagrams/01_system_architecture.mmd` | The whole system: commands → agents → artifacts |
| `diagrams/02_command_hierarchy.mmd` | Command tree and execution order |
| `diagrams/03_pipeline_sequence.mmd` | Sequence diagram of one full PRD run |
| `diagrams/04_self_improvement_loop.mmd` | The Karpathy 7-step improvement loop |
| `diagrams/05_two_path_provisioning.mmd` | Notebook (setup) vs Parser (ingestion) split |

---

## 30-second summary

- **8 specialised agents**, each doing exactly one job, with a locked tool allowlist.
- **6 slash-commands** that orchestrate those agents into a repeatable pipeline.
- **1 self-improvement skill** that lets the system critique and patch its own agents from real run data.
- **Reuse-first principle**: never recreate a data type that already exists in `bam-masterdata`; classify everything as **REUSE / EXTEND / CREATE** and only generate code for genuine gaps.
- **Human-in-the-loop**: the pipeline deliberately *stops* for human review before any code generation and before any self-improvement patch is applied.
