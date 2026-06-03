# PLAN — BAM openBIS Reusable PRD-to-Provisioning Agent Architecture

> **Status:** Draft for user approval. Generated 2026-05-27 by the make-plan skill after Phase 0 documentation discovery against `BAMresearch/bam-masterdata` (cloned to `C:\Users\pgerards\repos\bam-masterdata`) and the official openBIS 20.10.0-11 pyBIS docs.
>
> **Mission.** Build a reusable Claude Code agent + command + skill architecture for the BAM FB 7.2 group (and other BAM groups). A user drops a *new PRD* into this project; the pipeline (a) catalogs what is already in `bam-masterdata`, (b) extracts the PRD's required types, (c) diffs and produces a *reuse-first* gap report, (d) generates Python class extensions ONLY for the genuine gaps, and (e) emits a Jupyter notebook that instantiates the experiment (Collection + child Objects + parent links + property values + dataset uploads) in the user's openBIS 20.10.12.5 instance. A "Karpathy-style" self-improvement loop lets the agents critique their own outputs and propose diffs to their own instructions.
>
> **Out of scope for now.** Pushing new masterdata to openBIS at runtime (handled separately by `bam_masterdata.cli.cli:masterdata_sync`). Modifying `bam-masterdata` itself (we only consume it; new types ship as PRs to that repo).

---

## Phase 0 — Documentation Discovery (DONE)

This phase has already executed and produced a body of evidence. The outputs are summarized below and embedded as **Allowed APIs / Anti-Patterns** that all subsequent phases must respect.

### 0.1 Sources of truth (pin these into every phase context)

| Topic | Authoritative source |
|---|---|
| bam-masterdata base classes | `bam-masterdata/bam_masterdata/metadata/definitions.py:1-614` and `entities.py:42-1228` |
| bam-masterdata existing ObjectTypes | `bam_masterdata/datamodel/object_types.py` (118 classes — index reproduced in §0.4) |
| bam-masterdata existing Vocabularies | `bam_masterdata/datamodel/vocabulary_types.py` (95 classes) |
| bam-masterdata welding subpackage | `bam_masterdata/datamodel/welding/{object_types.py,vocabularies.py}` |
| bam-masterdata extend-how-to | `docs/howtos/extend_masterdata.md`, `docs/howtos/object_types.md` |
| bam-masterdata discovery mechanism | `bam_masterdata/utils/paths.py:24-40` + `utils/utils.py:55-110` (recursive glob; skip files starting with `_`) |
| pyBIS API for openBIS 20.10.12.5 | https://openbis.readthedocs.io/en/20.10.0-11/software-developer-documentation/apis/python-v3-api.html |
| pyBIS pin | `pybis==1.37.4` (matches `bam-masterdata/pyproject.toml:27-38`) |
| Karpathy SPL tweet | https://x.com/karpathy/status/1921368644069765486 (2025-05-11) |
| Karpathy Autoresearch repo | https://github.com/karpathy/autoresearch (2026-03-07) |
| Karpathy context engineering | https://x.com/karpathy/status/1937902205765607626 (2025-06-25) |

### 0.2 Allowed pyBIS APIs (openBIS 20.10.12.5)

CONFIRMED in 20.10.0-11 docs (only these may be used in generated notebooks):

```python
from pybis import Openbis
o = Openbis(url, verify_certificates=True)
o.login(username, password, save_token=True)
o.set_token(token, save_token=True)
o.get_or_create_personal_access_token(sessionName=...)
o.is_session_active()
o.logout()

# Collections / Experiments
o.get_experiment(identifier)
o.get_experiments(project=..., space=..., type=..., props=[...])
exp = o.new_experiment(code=..., type=..., project=...)
exp.p.set({...}); exp.save()

# Objects / Samples
o.get_sample(id_or_permid)
o.get_samples(space=..., type=..., tags=[...], props=[...])
sample = o.new_sample(type=..., space=..., experiment=..., parents=[...], children=[...], props={...})
sample.set_parents([...]); sample.add_parents(...); sample.set_children([...])
sample.save()

# DataSets
ds = o.new_dataset(type=..., experiment=..., sample=..., files=[...], zipfile=..., props={...}, kind=...)
ds.save()

# Batch
trans = o.new_transaction()
trans.add(sample); trans.commit()
```

**bam-masterdata parser surface** (used in parser packages under `generated/<prd-stem>/parsers/`):

```python
from bam_masterdata.parsing import AbstractParser
from bam_masterdata.metadata.entities import CollectionType
from bam_masterdata.cli.run_parser import run_parser, run_parser_with_transactions
from bam_masterdata.datamodel.object_types import ExperimentalStep  # or any ObjectType subclass

class MyParser(AbstractParser):
    def parse(self, files: list[str], collection: CollectionType, logger) -> None:
        # file I/O goes here; add objects to the in-memory collection
        obj = ExperimentalStep(name=..., ...)
        obj.code = "EXISTING_CODE"  # optional: to UPDATE an existing object
        obj_id = collection.add(obj)
        child_id = collection.add(ExperimentalStep(...))
        collection.add_relationship(obj_id, child_id)

# Caller (notebook cell or CLI script) — NOT inside the parser class itself:
run_parser(
    openbis=o,
    space_name="MY_SPACE",
    project_name="MY_PROJECT",
    collection_name="MY_COLLECTION",
    files_parser={MyParser(): ["data.csv", "result.json"]},
    collection_type="COLLECTION",  # or "DEFAULT_EXPERIMENT"
)
run_parser_with_transactions(...)  # atomic batch variant
```

### 0.3 Anti-patterns (FORBIDDEN in generated code)

| Forbidden | Why | Use instead |
|---|---|---|
| `o.create_sample_type(...)`, `o.create_object_type(...)` | Not in 20.10.0-11 docs; pre-V3 style. | Define types declaratively in `bam-masterdata` and push via `bam_masterdata` CLI. |
| Plain username/password in checked-in notebooks | Security; PAT is the 20.10.x recommendation (SSDM-11792 / -11586). | `o.get_or_create_personal_access_token(sessionName=...)` + `set_token(..., save_token=True)`. |
| Implicit save / "fire-and-forget" `new_*` calls | pyBIS has no autosave. | Always `.save()` after `new_*` and after property edits. |
| Inventing methods that "should" exist (`o.new_collection`, `o.create_collection`) | Misnamed. | `o.new_experiment(...)` (openBIS *Experiment* = pyBIS *Experiment* = your "Collection"). |
| Imperative `o.create_*` calls inside `bam-masterdata`-style extension modules | Violates the declarative class-based pattern (PRD §2.1). | Inherit from `ObjectType`/`VocabularyType`; rely on `to_openbis(logger, openbis)` invoked by the CLI. |
| Files starting with `_` under `bam_masterdata/datamodel/` | Auto-discovery skips them (`utils.py:64-66`). | Use a non-underscore filename. |
| Adding new vocabulary codes already on the forbid list | Pre-commit hook `tools/precommit/forbid_vocabularies.py` rejects them. | Read the hook before naming new vocabularies. |
| Bilingual description in a non-`English//Deutsch` form | Convention required by BAM, e.g. `description="Total Fracture//Totalbruch"`. | Always English first, `//` separator, no spaces around `//`. |
| Calling `openbis.new_collection()` from user notebooks or parser code | It's called internally by `run_parser()`; double-calling breaks idempotency. | Use `run_parser()` or `run_parser_with_transactions()` for parser-based workflows; `o.new_experiment()` for direct provisioning notebooks. |

### 0.4 Reuse catalog (must be consulted BEFORE creating anything new)

Existing items relevant to fatigue / welded specimens / testing rigs:

- **Object types**: `Instrument`, `TestingMachine`, `LoadFrame`, `HydraulicCylinder`, `Servovalve`, `AlignmentFixture`, `Thermocouple`, `Rtd`, `Nanovoltmeter`, `MeasuringAmplifier`, `Camera`, `ForceTransducer`, `Calibration`, `Steel`, `Aluminium`, `Sample`, `TestObject`, `Project`, `Person`, `Document`, `Storage`, `StoragePosition`, `Supplier`, `GeneralProtocol`, `Entry`.
- **Fatigue specifically**: `Fcg` (specimen `SPECIMEN.FCG`), `FcgTest`, `FcgStep`, `FcgEvaluation`, `Dcpd`, `MicroscopyFcgFractureSurfaceCracklength`, `RazorbladeNotching`.
- **Welding subpackage**: `Welding(CONSUMABLE.WELDING)`, `WeldingEquipment`, `GmawTorch`, `GmawWeldingPowerSource`, `Positioner`, `RobotController`, `Robot`, `StationLayout`, `Weldment`, `GmawBase`, `LaserHybridMagnet`, `LaserMagnet`, `WireSolid`.
- **Vocabularies (welding/fatigue-adjacent)**: `WELDING.WELD_TYPE` (FILLET, GROOVE, PLUG, SPOT, SURFACING, TACK — note: NO `BUTT_WELD`/`CRUCIFORM_WELD`), `WELDING.GMAW_TORCH_TYPE`, `FCG_STEP_TYPE`, `NOTCH_TYPE_FCG`, `SPECIMEN_TYPE_FCG_TEST`, `SPECIMEN_STATUS`, `TESTING_MACHINE_LOAD_TYPE`, `TESTING_MACHINE_DRIVE_TYPE`, `LOAD_FRAME_ORIENTATION`, `DCPD_POT_CAL`, `INSTRUMENT_STATUS`.
- **Generic test-step parents**: `ExperimentalStep` (parent for everything in PRD §3 Phase 3).

Confirmed *missing* (must be created if the FB7.2 workflow needs them):
- Vocabularies: `WELD_GEOMETRY`, `ISO_5817_FAT_CLASS`, `LOAD_LEVEL`, `FATIGUE_STOP_REASON`, `STRAIN_GAUGE_TYPE`, `CONSUMABLE_TYPE`.
- ObjectType: `WeldedFatigueSpecimen` (closest existing peer is `Fcg`, but it lacks weld-specific properties).
- ExperimentalSteps named in PRD §3: `PreQualityCheckWeld`, `ChamferingGrinding`, `SpecimenRecording`, `WeldAnalysis`, `SeriesAssignment`, `TestSetupGeometry`, `MonitoringApplication`, `AmplifierSettings`, `InstallationStressMeasurement`, `CyclicFatigueTest`, `FatigueDataEvaluation`, `FractureSurfaceAnalysis` — **all 12 absent**. However, several of their property needs (force transducer linkage, instrument linkage, camera linkage) are already covered by existing instrument types and can be satisfied with `data_type="OBJECT"` references rather than new dedicated properties.

### 0.5 Copy-ready snippet locations (use verbatim as templates)

- **Minimal new ObjectType**: `bam-masterdata/bam_masterdata/datamodel/object_types.py:7167-7191` (`class AlignmentFixture`).
- **Minimal new Vocabulary**: `bam-masterdata/bam_masterdata/datamodel/vocabulary_types.py:27836-27858` (`class FlashLampShape`).
- **Namespaced (dotted-code) Vocabulary**: `bam-masterdata/bam_masterdata/datamodel/welding/vocabularies.py:6-34` (`class GmawTorchType(code="WELDING.GMAW_TORCH_TYPE")`).
- **Whole new sub-package with welding-style namespacing**: `bam-masterdata/bam_masterdata/datamodel/welding/` (whole folder).

### 0.6 Karpathy self-improvement loop (canonical 7 steps)

Encoded in `karpathy-self-improvement` skill, applied via `/bam-improve` command:

1. **Run** the agent against a task → capture stdin/stdout/tools.
2. **Persist** to `runs/<timestamp>/{input.md,transcript.jsonl,output/,trace.log}` + git SHA of the agent's instructions file.
3. **Score / annotate** (reviewer subagent or human) — write pass/fail + failure note.
4. **Critique → diff** (`prompt-surgeon` subagent) — propose minimal unified diff against `SKILL.md`/agent `.md`, with rationale tied to specific failure IDs.
5. **Approve** (human-in-the-loop via diff render).
6. **Apply + version** (git commit with `runs/<ts>/` references; tag the agent file with a semver bump).
7. **Regress** — re-run the regression set under `evals/regressions/*.task.md`; monotone score requirement.

---

## Phase 1 — Repo Scaffolding & bam-masterdata Sync

**Purpose.** Create the on-disk layout that all later phases write into. No business logic yet.

### 1.1 What to implement

Create the following structure inside `C:\Users\pgerards\repos\51_BAM_DataStore\`:

```
.claude/
  agents/                  # (empty; populated in Phase 2)
  commands/                # (empty; populated in Phase 2)
  skills/                  # (empty; populated in Phase 3)
  settings.json
.gitignore
runs/                      # Karpathy run logs (Phase 3)
evals/regressions/         # regression task files (Phase 3)
notebooks/                 # generated Jupyter notebooks (Phase 5)
generated/                 # generated masterdata extension modules (Phase 4-5)
README.md                  # operator-facing README
PLAN.md                    # already exists
BAM_PRD_Workflow_FB72.md   # already exists (rewritten in Phase 4)
```

External to this repo but referenced:
- `C:\Users\pgerards\repos\bam-masterdata\` — already cloned in Phase 0; Phase 1 confirms it is present and on `main`.

### 1.2 `/bam-sync` command (`.claude/commands/bam-sync.md`)

Behaviour:
1. If `C:\Users\pgerards\repos\bam-masterdata\` does NOT exist, `git clone https://github.com/BAMresearch/bam-masterdata.git` to that path.
2. Else `git -C ../bam-masterdata fetch --all && git -C ../bam-masterdata pull --ff-only origin main`.
3. Print the resolved commit SHA and date.
4. Refuse to overwrite local changes (no `--force`, no `reset --hard`); abort and surface them.

### 1.3 `settings.json` baseline

Minimal settings file that:
- Adds `C:/Users/pgerards/repos/bam-masterdata` to `additionalDirectories` so agents can `Read`/`Grep` it without re-prompts.
- Optionally registers a `PostToolUse` hook stub for Phase 3's `runs/` persistence (commented-out for now).

### 1.4 Documentation references

- bam-masterdata README: `bam-masterdata/README.md` (install + test instructions).
- Discovery mechanism: `bam-masterdata/bam_masterdata/utils/paths.py:24-40`.

### 1.5 Verification checklist

- [ ] `C:\Users\pgerards\repos\bam-masterdata\bam_masterdata\datamodel\object_types.py` exists and contains `class TestingMachine` (`grep -n "class TestingMachine" ...` returns line ~1488).
- [ ] `.claude/commands/bam-sync.md` exists and runs cleanly (manual test: invoke `/bam-sync`).
- [ ] `.gitignore` excludes `runs/`, `*.ipynb_checkpoints/`, `.env`, `*.token`.
- [ ] Tree above is created (`ls -la` shows every dir).

### 1.6 Anti-pattern guards

- Do NOT add `bam-masterdata/` as a git submodule (per user decision — separate clone is preferred).
- Do NOT vendor `bam-masterdata` source into this repo's tree.
- Do NOT modify `bam-masterdata` itself in this phase.

---

## Phase 2 — Core Agent Architecture (Discovery → Gap → Extension → Notebook)

**Purpose.** Define the five domain agents and the four orchestrating slash commands that drive the pipeline. Each agent is a single Markdown file under `.claude/agents/`. Each command is a single Markdown file under `.claude/commands/`.

### 2.1 Agents (each is a `<name>.md` in `.claude/agents/`)

| Agent | Single responsibility | Inputs | Outputs |
|---|---|---|---|
| `bam-masterdata-explorer` | Build/refresh a CATALOG of every existing `ObjectType`, `ExperimentalStep`, `VocabularyType`, `CollectionType`, `DatasetType` in `../bam-masterdata` with file:line citations. Idempotent. | `../bam-masterdata` working tree | `generated/CATALOG.md` |
| `prd-requirements-extractor` | Parse a Markdown PRD into a normalized JSON structure of required entities: vocabularies, object types, experimental steps, properties (with data type, mandatory flag, section, bilingual description). Must NOT invent types not in the PRD. | `<prd-path>.md` | `generated/<prd-stem>.requirements.json` |
| `gap-analyzer` | Diff `requirements.json` against `CATALOG.md`. Output three tables: **REUSE** (exact match — use as-is), **EXTEND** (existing type that needs one or two extra terms/properties — suggest a PR against `bam-masterdata`), **CREATE** (genuinely new). For each REUSE/EXTEND entry, cite the exact `file:line`. | `requirements.json`, `CATALOG.md` | `generated/<prd-stem>.gap-report.md` |
| `masterdata-extender` | For CREATE-only items, write Python modules that follow the canonical snippet patterns from Phase 0 §0.5. One file per logical grouping (one for vocabularies, one for ObjectTypes, optionally a sub-package). Honor bilingual format, `section` strings, `generated_code_prefix`, declarative-only constraint. Emit into `generated/<prd-stem>/datamodel/*.py` — ready to PR into `bam-masterdata`. | `gap-report.md`, copy-ready snippets at `bam_masterdata/datamodel/object_types.py:7167-7191` and `vocabulary_types.py:27836-27858` | `generated/<prd-stem>/datamodel/*.py` + `generated/<prd-stem>/datamodel/README.md` |
| `openbis-notebook-generator` | Emit a Jupyter notebook that, given a PAT, creates the Collection (Experiment), then the child Objects (Samples) with parent links + properties, then attaches datasets (file uploads). Use ONLY APIs in Phase 0 §0.2. Insert a clearly marked "FILL ME IN" cell for `OPENBIS_URL`, PAT bootstrap, and Space/Project codes. | `requirements.json`, `gap-report.md` | `notebooks/<prd-stem>_provisioning.ipynb` |
| `openbis-parser-generator` | Generate an `AbstractParser` subclass scaffold for each workflow cluster in the gap report. Uses **programmatic `run_parser()` only** (no Parser App registration). One parser class per workflow cluster (not one per ExperimentalStep). Skips file I/O entirely — emits a single `# TODO: open files and extract data` stub; focuses on instantiating the correct ObjectType classes with properties and relationships. Includes `tests/test_parser.py` with a smoke test using in-memory mocked data. | `gap-report.md`, template at `bam-masterdata/docs/howtos/parsing/create_new_parsers.md` | `generated/<prd-stem>/parsers/` package |

### 2.2 Commands (each is a `<name>.md` in `.claude/commands/`)

| Command | Pipeline |
|---|---|
| `/bam-sync` | (already created in Phase 1) refresh `../bam-masterdata`. |
| `/bam-analyze-prd <prd-path>` | Run `bam-masterdata-explorer` (only if `CATALOG.md` is stale by SHA), then `prd-requirements-extractor`, then `gap-analyzer`. Stop here for human review of the gap report. |
| `/bam-generate-types <prd-path>` | Pre-req: gap report reviewed. Invokes `masterdata-extender`. Output goes to `generated/<prd-stem>/datamodel/`. Prints a follow-up suggestion: open a PR against `BAMresearch/bam-masterdata` with this content. |
| `/bam-generate-notebook <prd-path>` | Invokes `openbis-notebook-generator`. Notebook goes to `notebooks/<prd-stem>_provisioning.ipynb`. |
| `/bam-generate-parser <prd-path>` | Pre-req: gap report reviewed. Invokes `openbis-parser-generator`. Output: `generated/<prd-stem>/parsers/`. Prints install instructions: `pip install -e generated/<prd-stem>/parsers/` |
| `/bam-improve <skill-or-agent-name>` | Karpathy loop (Phase 3). |

### 2.3 Authoring rules (apply to every `.md` agent/command file)

1. **Frontmatter**: `description:` field is the trigger string. Keep tight (≤140 chars), trigger phrases first.
2. **Allowed APIs section**: every agent must repeat the relevant subset of Phase 0 §0.2 (APIs) and §0.3 (anti-patterns) verbatim. This is what prevents drift across sessions.
3. **"You MUST cite"** rule: any claim about an existing type in `bam-masterdata` requires a `file:line` citation in the agent's output.
4. **No `o.create_*` ever** — agents may only call methods from §0.2.
5. **Bilingual rule**: emit `description="English//Deutsch"` literally; no space around `//`.

### 2.4 Documentation references

- Agent file format: official Claude Code docs on subagents (frontmatter + body).
- Slash-command file format: official Claude Code docs on slash commands.
- Subagent reporting contract (this PLAN, §0 → Sources / Findings / Snippets / Confidence) is mandatory in every agent body.

### 2.5 Verification checklist

- [ ] `.claude/agents/bam-masterdata-explorer.md` runs end-to-end against `../bam-masterdata` and produces `generated/CATALOG.md` containing AT LEAST the following entries (assert by grep): `TestingMachine`, `Instrument`, `FcgTest`, `FcgStep`, `Weldment`, `WELDING.WELD_TYPE`, `FCG_STEP_TYPE`.
- [ ] `/bam-analyze-prd BAM_PRD_Workflow_FB72.md` produces a gap report that lists `WELD_GEOMETRY`, `ISO_5817_FAT_CLASS`, `LOAD_LEVEL`, `FATIGUE_STOP_REASON` as **CREATE** (no false REUSE).
- [ ] `WELDING.WELD_TYPE` appears in **EXTEND** (since BUTT_WELD/CRUCIFORM_WELD are missing) — agent must propose either adding terms there OR creating `WELD_GEOMETRY` and justify the choice with a citation.
- [ ] `/bam-generate-types …` writes files that `python -c "from bam_masterdata.metadata.entities import ObjectType; ..."` can import without error after symlinking into `bam-masterdata/bam_masterdata/datamodel/`.
- [ ] The generated notebook (Phase 5 will exercise it) parses (`nbformat.read`) and contains NO occurrence of `o.create_sample_type`, `o.create_object_type`, or hardcoded passwords.

### 2.6 Anti-pattern guards

- The `masterdata-extender` must REFUSE to emit Python for anything classified **REUSE** or **EXTEND** in the gap report; otherwise we duplicate existing types.
- The notebook generator must NOT inline a password; it MUST use PAT (`get_or_create_personal_access_token`).
- No agent may invent line numbers. If a citation cannot be produced, the agent must say "UNCONFIRMED — please verify" rather than fabricate.

---

## Phase 3 — Karpathy Self-Improvement Meta-Skill

**Purpose.** Make the agents in Phase 2 improvable. The improvement is itself a tool: `/bam-improve`.

### 3.1 What to implement

- `.claude/skills/karpathy-self-improvement/SKILL.md` — distilled 7-step loop from Phase 0 §0.6. Includes the explicit "**Surgical Changes**" rule: critique diffs must touch only sections justified by a logged failure ID.
- `.claude/agents/skill-reviewer.md` — reads `runs/<ts>/transcript.jsonl` + `output/`; emits `runs/<ts>/review.json` (pass/fail + failure notes with stable IDs).
- `.claude/agents/prompt-surgeon.md` — reads `review.json` + the target `.md` instructions file; emits a unified diff + per-hunk rationale (failure-ID → hunk mapping).
- `.claude/commands/bam-improve.md` — orchestrates: pick latest N runs → `skill-reviewer` → `prompt-surgeon` → render diff → prompt user for approval → `git apply` → commit → run regression set under `evals/regressions/`.
- `.claude/hooks/` (optional, behind a settings flag): `PostToolUse` hook that snapshots tool calls to `runs/<ts>/transcript.jsonl`. Default off for now.

### 3.2 Regression harness

- `evals/regressions/fb72.task.md` — the FB7.2 PRD as a regression case (Phase 4 will rewrite the PRD; we keep an immutable snapshot of the original here as a "golden input").
- `evals/regressions/_score.md` — defines the pass criteria (e.g. "gap report must list all 12 ExperimentalSteps as CREATE", "notebook must lint via `nbformat`", "no forbidden API names appear").

### 3.3 Documentation references

- Karpathy SPL: https://x.com/karpathy/status/1921368644069765486
- Karpathy Autoresearch: https://github.com/karpathy/autoresearch (README "give an AI agent a small but real LLM training setup…")
- Karpathy Context Engineering: https://x.com/karpathy/status/1937902205765607626
- (Supporting context — NOT primary attribution) Reflexion (Shinn et al., 2023), Self-Refine (Madaan et al., 2023).

### 3.4 Verification checklist

- [ ] `/bam-improve bam-masterdata-explorer` on a deliberately broken catalog run produces a non-empty diff that targets ONLY the section relevant to the failure.
- [ ] Approving the diff applies it via `git apply` (NOT manual `Edit`) so the change is auditable.
- [ ] `evals/regressions/fb72.task.md` exists and re-running the pipeline against it produces a deterministic gap report (byte-identical given the same `../bam-masterdata` SHA).

### 3.5 Anti-pattern guards

- `prompt-surgeon` MUST NOT propose hunks that aren't justified by a logged failure (one of the most common LLM critique failure modes — speculative tightening).
- `prompt-surgeon` MUST NOT touch the "Allowed APIs" or "Anti-patterns" sections of an agent — those are governed by Phase 0 evidence, not by run data. Add a hard refusal at the top of `prompt-surgeon.md`.
- No silent edits to `.claude/agents/*.md` outside the `/bam-improve` flow. (Future hardening: `PreToolUse` hook on `Edit` that checks the caller is `prompt-surgeon`.)

---

## Phase 4 — Rewrite `BAM_PRD_Workflow_FB72.md` (reuse-first)

**Purpose.** The current PRD assumed bare metal. Rewrite it so future runs of the pipeline produce a *minimum-delta* result. This also dogfoods the architecture: the rewrite is informed by the gap report from `/bam-analyze-prd BAM_PRD_Workflow_FB72.md` produced in Phase 2.

### 4.1 What to implement

Rewrite `BAM_PRD_Workflow_FB72.md` with this structure (verbatim section order):

1. **Kontext & Zielsetzung** — unchanged from current §1.
2. **Reuse Policy (verbindlich)** — replace current §2 with an EXPLICIT pipeline contract:
   > *Before defining ANY new vocabulary, ObjectType, ExperimentalStep, or PropertyTypeAssignment, the implementation MUST cite either (a) an existing class in `bam-masterdata` (path + line) and explain why it cannot be reused, or (b) the matching entry in `generated/<prd-stem>.gap-report.md` showing the gap is genuine.*
3. **Bekannte Wiederverwendungen (locked)** — list the items confirmed REUSE during Phase 2's gap analysis. Examples to include (subject to gap-analyzer output):
   - `TestingMachine` (`bam_masterdata/datamodel/object_types.py:1488`) — for Prüfmaschinen.
   - `Instrument` (`object_types.py:1254`) — for Kameras, Mikroskope, 3D-Scanner, IMC-Messverstärker.
   - `MeasuringAmplifier` (`object_types.py:7627`) — Verstärker konkret.
   - `Camera` (`object_types.py:7913`), `LoadFrame` (`object_types.py:7104`), `HydraulicCylinder` (`object_types.py:6963`), `Servovalve` (`object_types.py:7042`), `AlignmentFixture` (`object_types.py:7167`), `Thermocouple` (`object_types.py:7193`), `Calibration` (`object_types.py:1073`), `ForceTransducer` (`object_types.py:6048`).
   - Vocabularies: `WELDING.WELD_TYPE`, `TESTING_MACHINE_LOAD_TYPE`, `TESTING_MACHINE_DRIVE_TYPE`, `LOAD_FRAME_ORIENTATION`, `SPECIMEN_STATUS`, `INSTRUMENT_STATUS`.
4. **Erweiterungen (EXTEND)** — items where existing types are extended:
   - **`WELDING.WELD_TYPE`** — propose adding `BUTT_WELD` and `CRUCIFORM_WELD` terms (a PR-grade extension), OR justify creating a new `WELD_GEOMETRY` vocabulary instead. Decision must reference the gap report.
5. **Neudefinitionen (CREATE)** — only items genuinely absent:
   - Vocabularies (provisional list, subject to gap report): `ISO_5817_FAT_CLASS`, `LOAD_LEVEL`, `FATIGUE_STOP_REASON`, optionally `STRAIN_GAUGE_TYPE`, `CONSUMABLE_TYPE`.
   - ObjectType: `WeldedFatigueSpecimen` (parent: `ObjectType`; or a subclass of `Fcg` if the gap report shows ≥80 % overlap of properties).
   - ExperimentalSteps: the 12 listed in the original PRD §3 (subject to gap report — some may collapse if they overlap heavily with existing FCG steps).
6. **Sprache & Format** — keep the `English//Deutsch` rule; add the explicit `//` no-space requirement.
7. **Lieferform** — replace current §4 with:
   > *Output: (a) a PR-ready Python module under `generated/welded_fatigue/datamodel/` mirroring `bam-masterdata/bam_masterdata/datamodel/welding/` layout, AND (b) `notebooks/welded_fatigue_provisioning.ipynb` that instantiates a Collection plus the child Objects in a target openBIS 20.10.12.5 instance using only the APIs listed in PLAN.md §0.2.*

### 4.2 Documentation references

- The locked / extended / new sections must be **populated from the actual gap report**, not from the orchestrator's memory. The Phase 4 executor runs `/bam-analyze-prd BAM_PRD_Workflow_FB72.md` FIRST, reads `generated/BAM_PRD_Workflow_FB72.gap-report.md`, then writes the PRD.
- Use `bam-masterdata/docs/howtos/extend_masterdata.md` as the model for the "how to PR an extension" subsection.

### 4.3 Verification checklist

- [ ] The rewritten PRD includes **at least one** explicit citation of `bam_masterdata/datamodel/object_types.py:<line>` per locked-reuse entry.
- [ ] The §4 "EXTEND" decision for `WELDING.WELD_TYPE` is recorded with rationale.
- [ ] No new ObjectType in §5 lacks a "Why it can't be a subclass of an existing class" sentence.
- [ ] `grep -nE 'description="[^/]+//[^"]+"' BAM_PRD_Workflow_FB72.md` shows every bilingual string conforms (English first, `//`, no space, German).

### 4.4 Anti-pattern guards

- The Phase 4 executor MUST NOT skip running `/bam-analyze-prd` before rewriting; otherwise the rewrite re-introduces the very assumptions we are removing.
- The executor MUST preserve the original PRD as `evals/regressions/fb72.task.md` BEFORE rewriting, so the regression set survives.

---

## Phase 5 — Generate the FB7.2 Jupyter Notebook

**Purpose.** Exercise the pipeline end-to-end on the (now-rewritten) PRD. Produce a runnable notebook that the user can complete with their openBIS connection details.

### 5.1 What to implement

Invoke, in order:
1. `/bam-sync` (idempotent refresh).
2. `/bam-analyze-prd BAM_PRD_Workflow_FB72.md` (recomputes against the rewritten PRD).
3. `/bam-generate-types BAM_PRD_Workflow_FB72.md` → `generated/welded_fatigue/datamodel/{vocabularies.py, object_types.py, README.md}`.
4. `/bam-generate-notebook BAM_PRD_Workflow_FB72.md` → `notebooks/welded_fatigue_provisioning.ipynb`.
5. `/bam-generate-parser BAM_PRD_Workflow_FB72.md` → `generated/welded_fatigue/parsers/`.

### 5.2 Notebook structure (cells)

The notebook is generated, not hand-written, but the generator must follow this skeleton (cell-by-cell):

1. **Markdown: header** — PRD link, openBIS version, generated-on date, generator git SHA.
2. **Code: imports** — `from pybis import Openbis; import os, getpass`.
3. **Markdown: "⚠ Fill me in"** — `OPENBIS_URL`, `SPACE`, `PROJECT_CODE`, `COLLECTION_CODE`.
4. **Code: PAT bootstrap** — uses `o.get_or_create_personal_access_token(sessionName=...)` + `o.set_token(..., save_token=True)`. Reads username via `getpass.getuser()` / `input()`; reads password via `getpass.getpass()` only on first run. NEVER hardcodes credentials.
5. **Code: sanity check** — `assert o.is_session_active()`.
6. **Code: optionally `o.masterdata_sync`-style nudge** — print a reminder to push `generated/welded_fatigue/datamodel/` to openBIS via `python -m bam_masterdata masterdata_sync` **before** running the rest. (We do NOT do the push from the notebook; that is `bam-masterdata`'s job.)
7. **Code: create Collection** — `o.new_experiment(code=COLLECTION_CODE, type='DEFAULT_EXPERIMENT', project=f"/{SPACE}/{PROJECT_CODE}")`; `.save()`.
8. **Code: create child Objects (Samples)** — one cell per `ExperimentalStep`/specimen; use `o.new_sample(type=..., space=SPACE, experiment=..., parents=[...], props={...})`; `.save()`.
9. **Code: link parent/child** — explicit `sample.set_parents([...])` / `sample.add_children([...])`; `.save()`.
10. **Code: dataset upload stubs** — for each step that the PRD says receives a file upload (e.g. load program Excel for `CyclicFatigueTest`), generate `o.new_dataset(type='ANALYZED_DATA', sample='/SPACE/...', files=['path/to/file.xlsx'], props={...}).save()` with a clearly marked `# TODO: replace path` comment.
11. **Code: logout** — `o.logout()`.
12. **Markdown: "Using parsers for ongoing data ingestion"** — explains the two-path model: the notebook (cells 1-11) is the *one-time setup* that creates the Space/Project/Collection hierarchy and parent specimen objects; the parser package (`generated/<prd-stem>/parsers/`) is the *per-run ingestion* path that pushes new `ExperimentalStep` objects after every experiment. Users should run the notebook once, then use the parser for each new dataset.
13. **Code: parser usage stub** — shows `run_parser()` invocation pattern with clear `# TODO` markers:
    ```python
    # TODO: pip install -e generated/welded_fatigue/parsers/ first
    from welded_fatigue_parser import WeldedFatigueParser
    from bam_masterdata.cli.run_parser import run_parser

    run_parser(
        openbis=o,
        space_name=SPACE,          # same variable as cell 3
        project_name=PROJECT_CODE,
        collection_name=COLLECTION_CODE,
        files_parser={WeldedFatigueParser(): ["your_data.csv"]},  # TODO: replace path
        collection_type="DEFAULT_EXPERIMENT",
    )
    ```

### 5.3 Documentation references

- pyBIS API: https://openbis.readthedocs.io/en/20.10.0-11/software-developer-documentation/apis/python-v3-api.html (sections: "Constructor & Login", "Personal Access Tokens", "Create experiment", "Create sample", "Create dataset").
- `pybis==1.37.4` on PyPI.

### 5.4 Verification checklist

- [ ] `notebooks/welded_fatigue_provisioning.ipynb` opens in Jupyter without errors.
- [ ] `python -c "import nbformat; nbformat.read('notebooks/welded_fatigue_provisioning.ipynb', as_version=4)"` succeeds.
- [ ] `grep -nE "create_sample_type|create_object_type|create_collection" notebooks/welded_fatigue_provisioning.ipynb` returns **no matches**.
- [ ] `grep -nE "password\s*=\s*[\"']" notebooks/welded_fatigue_provisioning.ipynb` returns no matches (no hardcoded passwords).
- [ ] Every `new_experiment` / `new_sample` / `new_dataset` is followed by a `.save()` in the same cell (grep + visual review).
- [ ] Every child Object has either an `experiment=` argument or an explicit `set_parents`/`add_parents` call.
- [ ] `generated/welded_fatigue/parsers/src/welded_fatigue_parser/parser.py` contains a class inheriting `AbstractParser`.
- [ ] `grep -n "class.*AbstractParser" generated/welded_fatigue/parsers/src/*/parser.py` returns ≥1 match.
- [ ] `python -m pytest generated/welded_fatigue/parsers/tests/` passes (smoke test only — no live openBIS needed).
- [ ] No `run_parser` call inside `parser.py` (it belongs in the caller, not the parser itself).

### 5.5 Anti-pattern guards

- The notebook generator MUST refuse to emit cells that call `o.create_*` (use only methods in §0.2).
- It MUST NOT inline secrets — only environment-variable lookup or PAT bootstrap.
- It MUST keep all `# TODO` markers clearly labeled so the user knows what to fill in.

---

## Phase 6 — Final Verification & Hand-off

### 6.1 Static verification (grep-style)

| Check | Command |
|---|---|
| No forbidden pyBIS calls anywhere in `generated/`, `notebooks/`, `.claude/`. | `grep -rnE "create_sample_type\|create_object_type\|create_collection" generated/ notebooks/ .claude/` → empty |
| No hardcoded passwords. | `grep -rnE "password\s*=\s*['\"][^'\"]+['\"]" notebooks/ generated/` → empty |
| Bilingual format honored. | `grep -rnE 'description="[^"]+"' generated/ \| grep -vE '"[^/]*//[^/]*"'` → empty |
| All citations resolve. | for every `file:line` in `generated/CATALOG.md` and `BAM_PRD_Workflow_FB72.md`, run `sed -n "<line>p" <file>` and confirm non-empty. |
| Pre-commit policy honored. | New vocabularies are not on `bam-masterdata/tools/precommit/forbid_vocabularies.py` forbid list (currently only `BAM_LOCATION_COMPLETE`). |
| Parser does not call pybis directly. | `grep -rn "Openbis\|new_sample\|new_experiment\|new_dataset" generated/*/parsers/src/` → empty |

### 6.2 Functional verification

| Check | Command |
|---|---|
| Round-trip of generated datamodel files into bam-masterdata. | Symlink `generated/welded_fatigue/datamodel/` into `bam-masterdata/bam_masterdata/datamodel/welded_fatigue/`; run `python -m pytest -sv tests` in the bam-masterdata clone. Expect green. |
| Notebook parses. | `python -c "import nbformat; nbformat.read('notebooks/welded_fatigue_provisioning.ipynb', as_version=4)"`. |
| Karpathy loop produces a non-trivial diff on a seeded failure. | Manually break `bam-masterdata-explorer.md` (e.g. tell it to ignore the welding subpackage), run a task, then `/bam-improve bam-masterdata-explorer`. Confirm `prompt-surgeon` proposes a hunk restoring welding recursion. |
| Regression set is stable. | Re-run `/bam-analyze-prd evals/regressions/fb72.task.md`; compare the gap report against the committed reference. |

### 6.3 Hand-off deliverables for the dev team

Drop these into a single tagged commit / release notes:

- `PLAN.md` (this file).
- `BAM_PRD_Workflow_FB72.md` (rewritten in Phase 4).
- `.claude/{agents,commands,skills}/` (the architecture itself).
- `generated/welded_fatigue/datamodel/*.py` — proposed PR content for `BAMresearch/bam-masterdata` (open the PR manually; not from this repo).
- `notebooks/welded_fatigue_provisioning.ipynb` — the runnable provisioning notebook.
- `evals/regressions/fb72.task.md` — golden input.
- `runs/<seed-run>/` — at least one Karpathy-loop run kept as an example.
- `generated/welded_fatigue/parsers/` — parser scaffold package (install with `pip install -e generated/welded_fatigue/parsers/`; customize `parse()` per instrument file format).

---

## Cross-phase invariants

1. **Reuse before invention.** No agent emits a new type without a citation showing the gap is real.
2. **No raw `o.create_*` in any artifact.** Use only the §0.2 surface.
3. **PAT > password.** Always.
4. **Bilingual format always `English//Deutsch`.**
5. **Citations or it didn't happen.** Every existence-claim about `bam-masterdata` requires a `file:line`. UNCONFIRMED is acceptable; fabrication is not.
6. **The Karpathy loop is the only path that edits agent `.md` files.**
7. **Every phase is re-runnable in a new chat context** because every phase has its own §X.1 (what), §X.2-X.3 (refs), §X.4 (verification), §X.5 (anti-patterns).

## Task checklist

- [x] Phase 1 — Repo Scaffolding (complete)
- [ ] **Phase 2 amendment** — add `openbis-parser-generator` agent + `/bam-generate-parser` command
- [ ] Phase 3 — Karpathy self-improvement (unchanged)
- [x] Phase 4 — Rewrite PRD (complete)
- [ ] Phase 5 — Generate notebook + parser scaffold (extended)
- [ ] Phase 6 — Final verification (extended with parser checks)

---

## Open questions for the operator (answer before Phase 1)

(None blocking — earlier `AskUserQuestion` covered them. Re-raise after Phase 2 if the gap analysis surfaces surprises in the welding subpackage.)
