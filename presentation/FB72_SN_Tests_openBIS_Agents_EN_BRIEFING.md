# Designer Briefing – "S-N Fatigue Tests on Welded Joints – Structured Research Data in openBIS with AI Agents"

**Deck:** `FB72_SN_Tests_openBIS_Agents_EN.pptx` (11 slides, 16:9, English) · **Owner:** BAM, Department 7.2 Structural Engineering
**This briefing is self-contained.** It contains every fact, number and background explanation needed to redesign the deck.
You do not need any other file from the repository. If another document contradicts this briefing, **this briefing wins**.

---

## 1. Your task

Redesign the attached deck visually (layout, typography, colours, icons, diagram style, BAM template) **without changing the
facts**. You may rephrase for brevity and restructure layouts, merge or split bullet points, and turn tables into graphics,
as long as every statement and number below stays correct.

### Hard rules
1. **No comparison with any earlier or alternative approach.** The talk presents this approach on its own merits. Do not add
   "before/after", "old vs. new", "previously", "legacy" or improvement percentages. (Earlier internal documents in the
   repository contain such comparisons – do not use them.)
2. **Numbers are fixed.** Use exactly the figures in section 5. Do not round, extrapolate or add new metrics.
3. **Demo data must stay labelled** "DEMO – fictitious values" wherever the series table (slide 9) appears.
4. **Screenshots are real** (openBIS test instance "dev1", 6 Oct 2026) – crop/scale allowed, no retouching of content.
5. **Codes stay verbatim** in a monospace font where shown (e.g. `SAMPLE.WELDED_FATIGUE_SPECIMEN`, `S1B-01-TEST`).
6. Keep speaker notes (English, with timing) – update them only if you change the slide content.

### Open items for the presenter (keep as placeholders)
- Slide 1: date `[Date]`.
- Slide 2: photo of specimen / test rig (dashed placeholder frame).
- All slides: BAM template + BAM logo (top-right corner currently left free). No fake logo.

### Technical pitfall (PowerPoint compatibility)
If you build or edit shapes programmatically: **ellipse, rect and line shapes must not carry adjustment guides**
(`<a:gd name="adj" …>` inside `<a:avLst>`). PowerPoint silently drops the content of the whole slide otherwise. Only presets
that define them (e.g. `roundRect`) may have an `adj` guide. Prefer native, editable shapes over images for diagrams.

---

## 2. Audience, length, storyline

- **Audience:** BAM colleagues (engineers and scientists, mixed familiarity with openBIS and AI). **Length:** ~10–12 min.
- **Part A – the experiments (slides 2–4, ~3 min):** what we test, the 12-step workflow, what has to be captured.
- **Part B – the agent approach for openBIS (slides 5–10, ~6.5 min):** idea, pipeline, agent roles, resulting structure,
  daily use, safeguards & next steps.
- **Backup (slide 11):** sources – shown only on request.
- **One-sentence message of the talk:** *We describe our test workflow in domain language; AI agents check it against the BAM
  data standard and the live openBIS instance, design a flat, readable structure and create only what is really missing –
  humans approve every decision.*

---

## 3. Background knowledge

### 3.1 The experiments (domain)
- **S-N curve (Wöhler curve):** stress range Δσ vs. number of cycles to failure N (log–log). Determined from a series of
  specimens tested at different load levels.
- **Specimens:** welded **butt joints** and **cruciform joints**. Each specimen comes from a known **source sheet** (plate).
- **Weld quality per ISO 5817:** target quality level **B, C or D**; for fatigue-loaded structures ISO 5817 **Annex C**
  ratings **C63, B90, B125** (determined by a 3D-scan-based weld analysis).
- **Series design:** several **load levels** (high / medium / low), **randomised test order** – source sheet and
  randomisation avoid bias. Hence "scatter starts before the test" and the assignment must be documented per specimen.
- **Result per specimen:** number of cycles (gross and net; net excludes marker-load cycles) + **termination reason**:
  total fracture, crack detected, run-out (cycle limit reached), manual stop.
- **Beach marks:** marker loads applied during the test leave lines on the fracture surface used to reconstruct crack growth.

### 3.2 The 12-step workflow (4 phases)

| Phase | Steps | Equipment / material | Data & files |
|---|---|---|---|
| Preparation | 01 Pre-quality check · 02 Chamfering / grinding | – | angular distortion and edge misalignment (initial / after straightening), gross weld defects, photos, post-processing report |
| Characterisation | 03 3D scan · 04 Weld analysis (GOM) · 05 Series assignment · 06 Geometry before installation | ZEISS GOM ATOS 5 (3D scanner, GOM software), caliper | scan raw data, GOM export, Annex C rating, load level, test order, randomisation script, thickness & width at 3 positions each + means |
| Test rig | 07 Strain gauge application · 08 Measuring chain · 09 Installation stress · 10 Cyclic fatigue test · 11 Evaluation | HBM LY11-6/120 strain gauges, HBM X60 adhesive, crack luminescence set (MR Chemie), Luxonis OAK-4D-Pro camera, IMC measuring amplifier, servo-hydraulic testing machine | gauge distances (to weld toe / edge), application time, sampling rate, recording mode (full signal / peak counter / peak-valley), recorded channels, preload force, beach marks on/off, termination reason, gross/net cycles, cycles to 10 % strain-gauge drop; files: gauge drawing, setup photo, bending-moment raw data, load programme (Excel), IMC raw data, monitoring images, cleaned data, plots, conversion script |
| Post-test analysis | 12 Fracture surface analysis | macro camera, digital microscope | macro photos, microscope images of crack origin, beach-mark evaluation (Excel) |

In total: **34 data items, ~10 instruments/consumables, 17 kinds of files.**

### 3.3 openBIS / BAM Data Store (concepts used on the slides)
- **openBIS** is the research data platform behind the BAM Data Store (ELN = electronic lab notebook + inventory).
- Hierarchy: **Space → Project → Collection → Object**; objects can be linked as **parent/child**; files are stored as
  **datasets** attached to objects or collections.
- **Masterdata** = the type system: object types, property types, **vocabularies** (controlled lists), dataset types.
- **bam-masterdata** = BAM's shared, versioned standard data model (a Python package on GitHub, BAMresearch/bam-masterdata).
  At the time of the analysis: **141 object types**, 35 experimental-step types, 148 vocabularies (commit `d7a871b`, 5 Oct 2026).

### 3.4 The agent approach
- **Input:** a requirements document (PRD) in domain language – the workflow table above plus eight principles **P1–P8**:
  P1 flat object hierarchy · P2 flat type hierarchy · P3 specimen data on the specimen · P4 activities with
  instrument/time/files = step object · P5 workflow progress visible · P6 reuse-first · P7 tables as files, not properties ·
  P8 BAM language convention (descriptions "English//German", labels and section names English).
- **Two sources checked:** (1) the **bam-masterdata** standard, (2) the **live openBIS instance** (read-only inventory).
- **Four verdicts per element:** **REUSE** (exists in the standard, fits) · **EXTEND** (exists, needs a few terms) ·
  **CREATE** (genuinely missing) · **LIVE-ONLY** (found on the instance but not in the standard → migrated to standard
  types instead of being built upon).
- **Seven pipeline steps** (script = deterministic, agent = understands/decides, human = approves):
  1. Catalog of the standard – *script*
  2. Live inventory of the instance (read-only) – *script*
  3. Extract requirements from the PRD – *agent*
  4. Design a flat structure – *agent* → **human approves the design**
  5. Gap analysis (4 verdicts) – *agent* → **human approves the gap report**
  6. Python classes for CREATE items, verified by a real import test – *agent + script*
  7. Apply to openBIS – *script*, dry run first, idempotent (re-runs create nothing twice), conflicts reported
- **Rule of thumb:** counting is done by a script, deciding by an agent, approving by a human.
- **Agents (9, each with one job and one guardrail, explicit tool allowlist):**

| Agent | Role | Guardrail |
|---|---|---|
| bam-masterdata-explorer | catalogs the standard by running a script | never hand-writes the catalog; identical re-runs |
| prd-requirements-extractor | transcribes the PRD (steps, data items, equipment, files) | never invents types; never classifies |
| structure-designer | gives every item exactly one place in a flat structure | depth 1, no step→step links, nothing unplaced |
| gap-analyzer | classifies against standard and instance (4 verdicts) | every REUSE/EXTEND cites file:line |
| masterdata-extender | writes Python classes for CREATE items only | no code for REUSE/EXTEND; must pass import test |
| openbis-notebook-generator | builds the one-time setup notebook | no hard-coded credentials; only valid pyBIS calls |
| openbis-parser-generator | scaffolds the per-run ingestion parser | parser never calls the database directly |
| skill-reviewer (meta) | scores a captured run, logs failures with stable IDs | evidence mandatory for every failure |
| prompt-surgeon (meta) | proposes a minimal patch to an agent definition | never edits frozen sections; cites failure IDs |

Plus **4 deterministic scripts:** catalog, live inventory, spec export, apply.

### 3.5 The resulting structure in openBIS
```
Project  /FB_72/WELDED_FATIGUE
├── WORKFLOW_PLAN            protocol object: the 12 steps and where each value/file goes
├── SERIES_1_BUTT_WELD       collection = one test series (table view = test matrix)
│   └── S1B-01               specimen  (type SAMPLE.WELDED_FATIGUE_SPECIMEN)
│       ├── S1B-01-SCAN      step 03–04   ← parent: ZEISS GOM ATOS 5
│       ├── S1B-01-TEST      steps 07–11  ← parents: strain gauge, adhesive, crack set, camera, IMC, machine
│       └── S1B-01-FRACTURE  step 12      ← parents: macro camera, digital microscope
└── SERIES_1_CRUCIFORM_WELD  collection (S1C-01, …)
```
- **Specimen form:** field **"Next step"** at the top (ordered list 01–12 + done), then identification and numbered sections
  **01 Pre-quality check · 02 Chamfering/grinding · 04 Weld analysis · 05 Series assignment · 06 Geometry**.
- **TEST step form:** sections **07 Strain gauge application · 08 Measuring amplifier / test rig · 09 Installation stress ·
  10 Cyclic fatigue test · 11 Evaluation**.
- Step objects exist only where instrument, time span and files belong together; they are **direct children** of the specimen
  (one level, no step-to-step chains) and live in the same series collection.
- Instruments and consumables are created **once in the inventory** and linked as **parents**.
- Files use **standard dataset types** (raw data, processed data, analysed data, attachment, figure/plot, source code,
  measurement protocol) – no new dataset types.
- **New types (code):** `SAMPLE.WELDED_FATIGUE_SPECIMEN` (inherits the standard `Sample`),
  `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` (inherits the standard `MechanicalTest`).
- **New vocabularies (6):** workflow steps (S01…S12, DONE), ISO 5817 quality level (B/C/D), ISO 5817 Annex C rating
  (C63/B90/B125), load level, recording mode, termination reason. **Extended (2):** weld type (+ butt weld, cruciform weld),
  auxiliary material type (+ strain gauge, crack detection agent).

### 3.6 Daily use
- **Notebook (once per series):** sets up the structure, registers specimens and starts steps (updates "Next step").
- **Parser (after every test run):** reads the IMC evaluation summary and fills the TEST step (cycles, termination reason),
  then sets the specimen's next step (fracture analysis, or done for run-outs).

### 3.7 Safeguards (why the approach can be trusted)
1. **Deterministic catalog** – the standard is indexed by a script, not by the language model; re-runs are byte-identical.
2. **Real import test** – generated classes must import against the actual bam-masterdata package (syntax check is not enough).
3. **Dry run + idempotent apply** – changes previewed first; re-runs create nothing twice; conflicts reported, not overwritten.
4. **Instance behind the standard** – fields the instance cannot hold yet (e.g. missing BAM location vocabularies) are
   skipped and reported, not guessed.
5. **Mandatory fields checked up front** – creation is transactional; nothing is left half-created.
6. **Human review checkpoints** – design and gap report are approved before anything is generated or applied.

### 3.8 Next steps and limits
- Pull request to bam-masterdata: **2 object types, 6 vocabularies, 2 vocabulary extensions**.
- Sync the openBIS instance with the standard (admin task).
- Upstream issue for bam-masterdata: skip the mandatory-field check when only updating existing objects.
- Transfer the pattern: other departments write a workflow PRD and run the same pipeline (agents and scripts are in the repository).
- **Limits:** domain decisions stay with humans (e.g. quality levels; whether butt/cruciform is a joint type or a weld type).

---

## 4. Slide-by-slide specification

| # | Title (action title) | Must show | Visual / asset | Time |
|---|---|---|---|---|
| 1 | S-N Fatigue Tests on Welded Joints – Structured Research Data in openBIS with AI Agents | BAM · FB 7.2 Structural Engineering · BAM Data Store · [Date] | optional schematic S-N curve (log Δσ vs. log N, **no data**) | 0:20 |
| 2 | We determine S-N curves of welded butt and cruciform joints – every specimen counts, and scatter starts before the test | 3 blocks: specimens (joint types, source sheet, ISO 5817 B/C/D, Annex C C63/B90/B125) · test series (load levels, randomised order) · result (cycles + 4 termination reasons) | photo placeholder "specimen / test rig" | 1:00 |
| 3 | Twelve steps in four phases – each phase produces data and files | workflow table §3.2 (may be shortened to keywords), steps 01–12 as a sequence | process graphic 01→12 grouped in 4 phases | 1:15 |
| 4 | Data items, instruments and files for every specimen – each needs exactly one place | three groups: data items · instruments & consumables · 17 kinds of files; requirement: one place per value, visible progress, machine-evaluable | three-column layout or icon groups | 0:50 |
| 5 | AI agents check our workflow against the BAM standard and the live instance – and create only what is really missing | 1 input (PRD) · 2 sources · agents + scripts · 4 verdicts with counts **20 / 2 / 41 / 40** · 2 human approvals · output: openBIS (only missing) + PR to bam-masterdata | flow diagram left→right | 1:00 |
| 6 | Seven steps – each done by a specialised agent or a verifiable script | 7 pipeline steps, lanes Script / Agent / Human, 2 approval gates; rule of thumb | swimlane diagram | 1:00 |
| 7 | Nine single-purpose agents – one job and one hard guardrail each | agent table §3.4 + "4 deterministic scripts · explicit tool allowlist" | table or card grid | 1:00 |
| 8 | One specimen, three step objects, one level – the workflow stays visible | structure §3.5; key figures **2 / 6 (+2) / 0 / 1 / 4** | native structure diagram + screenshot `nachher_01_hierarchie_flach.jpg` | 1:15 |
| 9 | Every specimen shows its next step – the series table is the test matrix | demo table §5.3 labelled "DEMO – fictitious values"; notebook (once) vs. parser (after every run) | screenshot `nachher_02_probe_formular.jpg` | 1:00 |
| 10 | The value lies in checking, not in generating | 6 safeguards §3.7 · next steps · limits §3.8 | numbered list / icon grid | 1:15 |
| 11 | Backup · Sources | sources table §6 | – | on request |

**Screenshot captions:**
- `nachher_01_hierarchie_flach.jpg` – "openBIS hierarchy graph: specimen S1B-01 with its three child steps (fracture surface,
  3D scan & weld analysis, cyclic fatigue test)". (The file name is internal; it contains no comparison.)
- `nachher_02_probe_formular.jpg` – "openBIS form of specimen S1B-01: 'Next step' on top, then identification and the numbered
  sections (01 Pre-quality check, 04 Weld analysis, …)".

---

## 5. Fixed figures

### 5.1 Approach
| Figure | Value |
|---|---|
| Object types in the bam-masterdata standard | 141 |
| Verdicts for this workflow | REUSE 20 · EXTEND 2 · CREATE 41 · LIVE-ONLY 40 |
| Pipeline steps / human approvals | 7 / 2 |
| Agents / deterministic scripts | 9 (7 production + 2 meta) / 4 |
| Principles in the PRD | 8 (P1–P8) |

### 5.2 Resulting design
| Figure | Value |
|---|---|
| New object types | 2 |
| New vocabularies / extended vocabularies | 6 / 2 |
| New dataset types | 0 |
| Link depth (specimen → step) | 1 |
| Objects per specimen | 4 (specimen + SCAN + TEST + FRACTURE) |
| Workflow: steps / data items / file kinds | 12 / 34 / 17 |

### 5.3 Demo series (fictitious values – must be labelled)
| Specimen | Load level | Order | Annex C | Next step | Cycles (net) | Termination |
|---|---|---|---|---|---|---|
| S1B-01 | high | 3 | B90 | done | 231,900 | total fracture |
| S1B-02 | low | 1 | B90 | done | 10,000,000 | run-out |
| S1B-03 | medium | 2 | B125 | 12 Fracture surface | 1,052,000 | crack detected |
| S1B-04 | high | 4 | B90 | 10 Test running | – | – |
| S1B-05 | medium | 5 | C63 | 07 Strain gauges | – | – |
| S1B-06 | – | – | – | 03 3D scan | – | – |

---

## 6. Sources (for slide 11)
All figures as of 6 Oct 2026, checked against the openBIS test instance dev1 and bam-masterdata @ `d7a871b`.

| Statement | Source in repository |
|---|---|
| Workflow, equipment, files, principles P1–P8 | `BAM_PRD_Workflow_FB72_v2.md` |
| 141 object types in the standard | `generated/CATALOG.md` (script `tools/build_catalog.py`) |
| Structure, sections, vocabularies, key figures | `generated/welded_fatigue_v2/design.md` |
| 20 REUSE · 2 EXTEND · 41 CREATE · 40 LIVE-ONLY | `generated/welded_fatigue_v2/gap-report.md` |
| Agents, safeguards, next steps; full talk background | this briefing (`presentation/FB72_SN_Tests_openBIS_Agents_EN_BRIEFING.md`) |
| Screenshots (dev1, 6 Oct 2026); demo values fictitious | `presentation/screenshots/nachher_*.jpg` |

## 7. Assets
- Deck: `presentation/FB72_SN_Tests_openBIS_Agents_EN.pptx`
- Screenshots: `presentation/screenshots/nachher_01_hierarchie_flach.jpg`, `presentation/screenshots/nachher_02_probe_formular.jpg`
  (do **not** use any `vorher_*` images).
