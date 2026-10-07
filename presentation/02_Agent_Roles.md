# Agent Roles — High-Level Reference

Nine single-responsibility agents plus four deterministic scripts, grouped into three layers:

- **Scripts (4)** — count, verify and apply (no LLM): `tools/build_catalog.py`, live inventory (read-only V3 queries), `tools/export_spec.py`, `tools/openbis_apply.js` / `tools/openbis_demo.js`.
- **Production agents (7)** — understand, design and decide.
- **Meta agents (2)** — improve the production agents from run evidence.

Each agent declares an explicit **tool allowlist** in its frontmatter (least-privilege).

---

## Master table (the slide table)

| # | Agent | Layer | One-line role | Reads | Writes | Tools (allowlist) |
|---|---|---|---|---|---|---|
| 1 | **bam-masterdata-explorer** | Production | Run the AST catalog script and verify it (no hand enumeration) | `bam-masterdata/` source tree | `CATALOG.md`, `catalog.json` | Read, Glob, Grep, Bash, Write |
| 2 | **prd-requirements-extractor** | Production | Transcribe the PRD (workflow steps, data items, equipment, files, decisions) | PRD `.md` | `requirements.json` | Read, Write, Glob |
| 2b | **structure-designer** ✨ | Production | Map every data item / device / file to exactly one place in a **flat** openBIS structure | `requirements.json` + catalog + live inventory | `design.json`, `design.md` | Read, Write, Glob, Grep, Bash |
| 3 | **gap-analyzer** | Production | Classify against standard **and** live instance: REUSE / EXTEND / CREATE / LIVE-ONLY | `design.json` + catalog + live inventory | `gap-report.md`, `extend.json` | Read, Write, Glob, Grep |
| 4 | **masterdata-extender** | Production | Emit Python classes — **only** for CREATE items | `gap-report.md` + `requirements.json` | `datamodel/*.py` + `README.md` | Read, Write, Glob, Grep |
| 5 | **openbis-notebook-generator** | Production | Build the one-time provisioning Jupyter notebook | `requirements.json` + `gap-report.md` | `*_provisioning.ipynb` | Read, Write, Glob |
| 6 | **openbis-parser-generator** | Production | Scaffold the ongoing-ingestion parser package | `gap-report.md` + `object_types.py` | `parsers/` package | Read, Write, Glob, Grep, Bash |
| 7 | **skill-reviewer** | Meta | Score a captured run; log failures with stable IDs | `runs/<ts>/` + `_score.md` | `review.json` | Read, Glob, Grep, Bash, Write |
| 8 | **prompt-surgeon** | Meta | Propose a minimal, evidence-cited patch to an agent | `review.json` + agent `.md` | `proposed.diff` + `rationale.md` | Read, Glob, Grep, Write, Bash |

---

## Why each agent exists (the rationale column)

| Agent | The single problem it owns | Key guardrail (what it refuses to do) |
|---|---|---|
| **bam-masterdata-explorer** | "What already exists, and exactly where?" | Never hand-writes the catalog; byte-identical re-runs (the grep-based v1 missed all indirect subclasses) |
| **structure-designer** | "Where does each value live — flat?" | Max link depth 1, no step→step links, no new dataset types, nothing unplaced |
| **prd-requirements-extractor** | "What does the PRD actually ask for?" | Never invents types; never classifies (that's the gap-analyzer's job) |
| **gap-analyzer** | "Reuse, extend, build new — or migrate a live-only type?" | Never treats a live-only type as standard; every REUSE/EXTEND cites `file:line` |
| **masterdata-extender** | "Generate code for the genuine gaps." | **Hard-refuses** REUSE/EXTEND code; must pass a real **import test** (v1 only parsed syntax and shipped a non-existent class) |
| **openbis-notebook-generator** | "Set up the database once." | No hardcoded credentials; exactly one auth prompt; no invalid pyBIS calls |
| **openbis-parser-generator** | "Ingest data after every experiment." | Parser code stays pyBIS-free; never calls the database directly |
| **skill-reviewer** | "Did the run actually pass?" | Evidence mandatory for every failure; evaluates captured output, never live files |
| **prompt-surgeon** | "Fix the agent — minimally." | **Refuses** to touch frozen sections (Allowed APIs / Anti-patterns); every hunk cites a failure ID |

---

## Separation of concerns at a glance

```
DISCOVER        EXTRACT          DECIDE           GENERATE
─────────       ─────────        ─────────        ──────────────────────────
explorer   ──▶  extractor   ──▶  gap-analyzer ──▶ ┌ masterdata-extender  (types)
(what is)       (what's                           ├ notebook-generator   (setup)
                 needed)                           └ parser-generator     (ingest)

                                  IMPROVE
                                  ─────────
                                  skill-reviewer ──▶ prompt-surgeon
                                  (score)            (patch)
```

---

## The "REUSE / EXTEND / CREATE" decision — the heart of the system

Owned by **gap-analyzer**, enforced by **masterdata-extender**:

| Verdict | Meaning | Downstream action |
|---|---|---|
| **REUSE** | The type already exists and fits as-is | Cite its `file:line`; generate **no** code |
| **EXTEND** | The type exists but needs 1–3 extra terms/properties | Suggest a **minimal PR** to `bam-masterdata`; generate **no** new class |
| **CREATE** | Genuinely absent from the standard | Generate a new declarative Python class |
| **LIVE-ONLY** | Exists on the openBIS instance, not in the standard | Migrate to a REUSE/CREATE replacement (or propose for the standard) — never extend silently |

> This single classification is what keeps the shared `bam-masterdata` standard clean and non-redundant.
