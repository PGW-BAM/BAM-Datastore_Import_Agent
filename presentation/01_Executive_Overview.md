# Executive Overview

## The one-paragraph pitch

> The BAM DataStore agent system automates the most error-prone part of research-data
> management: translating a written experiment specification (a **PRD**) into the
> **data-model code and ingestion tooling** that a lab's **openBIS** database needs.
> It does this with a team of eight specialised AI agents, each performing a single
> well-defined step, coordinated by simple slash-commands. A hard "reuse-first" rule
> ensures the system **never duplicates** data types that already exist in the shared
> `bam-masterdata` standard — it reuses, minimally extends, or only creates what is
> genuinely new. Humans review every decision before any code is generated, and the
> system can even **improve its own agents** from logged evidence of past mistakes.

---

## The business problem it solves

| Without the system | With the system |
|---|---|
| Engineers hand-translate PRDs into openBIS types | One command extracts every requirement automatically |
| Types get duplicated → messy, inconsistent database | Reuse-first gap analysis prevents duplication |
| No audit trail for "why was this type created?" | Every type cites a PRD section + a `file:line` source |
| Onboarding a new workflow takes days of expert time | Pipeline produces code + notebook + parser in one sitting |
| Tooling quality drifts, mistakes repeat | Self-improvement loop patches agents from real failures |

---

## Core design principles (slide-ready bullets)

- **Single Responsibility per Agent** — each agent does *one* job and nothing else. Easy to test, easy to improve, easy to reason about.
- **Least Privilege** — every agent declares an explicit tool allowlist (e.g. read-only agents cannot write). Security and safety by construction.
- **Artifacts as Contracts** — agents communicate only through files (`CATALOG.md`, `requirements.json`, `gap-report.md`). Any stage can be re-run or swapped without breaking others.
- **Reuse-First (REUSE / EXTEND / CREATE)** — the central rule. Existing standards are sacred; new code is the last resort, never the default.
- **Human-in-the-Loop** — the pipeline *stops* for review before code generation and before any self-patch is applied. The machine proposes; the human disposes.
- **Evidence-Before-Claims** — no type is "reusable", no run is "passing", and no agent is "fixed" without a cited, reproducible piece of evidence (a `file:line`, a grep result, a failure ID).
- **Idempotency & Traceability** — re-running at the same source version produces identical output; every change is traceable to a run, a failure ID, and a rationale.

---

## What the system produces (the deliverables)

```
A written PRD  ──▶  the system  ──▶  ┌─ Python data-model classes  (for a bam-masterdata PR)
                                     ├─ A Jupyter provisioning notebook (one-time DB setup)
                                     └─ A parser package           (ongoing data ingestion)
```

Plus the decision artifacts that justify them:

- **`CATALOG.md`** — an index of everything that already exists in the shared standard.
- **`requirements.json`** — a normalised list of everything the PRD asks for.
- **`gap-report.md`** — the REUSE / EXTEND / CREATE verdict for every single requirement.

---

## Why two output paths? (the "two-path provisioning" model)

A common point of confusion — clarify it on a slide:

| Path | Question it answers | Run frequency | Produced by |
|---|---|---|---|
| **Provisioning notebook** | "How do I set up the database structure the first time?" | **Once** per workflow | `/bam-generate-notebook` |
| **Parser package** | "How do I push data after every experiment?" | **Every run** | `/bam-generate-parser` |

> *See `diagrams/05_two_path_provisioning.mmd`.*

---

## The self-improvement angle (the differentiator)

Most automation is static. This system includes a **closed feedback loop** (inspired by
Andrej Karpathy's "iterate on the prompt from real failures" philosophy):

1. An agent runs and its full transcript + outputs are captured.
2. A **reviewer agent** scores the run against objective criteria and logs failures with stable IDs.
3. A **prompt-surgeon agent** proposes a *minimal* patch to the failing agent — every change must cite a failure ID.
4. A human approves the patch; it is applied and committed.
5. A **regression suite** guarantees the patch never makes anything else worse.

The result: tooling that **gets measurably better over time**, with a full audit trail of *why* every change was made.

> *See `diagrams/04_self_improvement_loop.mmd`.*

---

## Headline numbers for a title slide

- **8** specialised agents
- **6** orchestration commands
- **1** self-improvement loop (7 disciplined steps)
- **3** classification verdicts that prevent data duplication (REUSE / EXTEND / CREATE)
- **0** hardcoded credentials, **0** invented citations — guardrails enforced by design
