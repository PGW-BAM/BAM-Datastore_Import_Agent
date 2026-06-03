---
name: openbis-notebook-generator
description: Generate a Jupyter provisioning notebook from requirements.json + gap-report.md. Uses PAT authentication, creates Collection and child Objects using only pyBIS 1.37.4 APIs. No hardcoded credentials. Outputs notebooks/<prd-stem>_provisioning.ipynb.
tools: Read, Write, Glob
---

# Agent: openbis-notebook-generator

## Single responsibility

Emit a Jupyter notebook (`.ipynb`) that a user can run against a live openBIS 20.10.12.5 instance to provision the Space/Project/Collection hierarchy and parent specimen Objects. This is the **one-time setup path** (complementary to the parser, which is the per-run ingestion path).

---

## Inputs

| Input | Path |
|---|---|
| Requirements | `generated/<prd-stem>/requirements.json` |
| Gap report | `generated/<prd-stem>/gap-report.md` |
| Original PRD (for context only) | `$ARGUMENTS` |

---

## Outputs

- `notebooks/<prd-stem>_provisioning.ipynb`

---

## Allowed pyBIS APIs (VERBATIM — only these may appear in notebook cells)

```python
from pybis import Openbis
o = Openbis(url, verify_certificates=True)
o.login(username, password, save_token=True)          # first-run only
o.set_token(token, save_token=True)
o.get_or_create_personal_access_token(sessionName=...) # preferred auth
o.is_session_active()
o.logout()

# Collections / Experiments
o.get_experiment(identifier)
exp = o.new_experiment(code=..., type=..., project=...)
exp.p.set({...}); exp.save()

# Objects / Samples
o.get_sample(id_or_permid)
sample = o.new_sample(type=..., space=..., experiment=..., parents=[...], children=[...], props={...})
sample.set_parents([...]); sample.add_parents(...); sample.set_children([...])
sample.save()

# DataSets
ds = o.new_dataset(type=..., experiment=..., sample=..., files=[...], props={...}, kind=...)
ds.save()

# Batch
trans = o.new_transaction()
trans.add(sample); trans.commit()
```

---

## Anti-patterns (FORBIDDEN — never appear in generated notebooks)

| Forbidden | Why | Use instead |
|---|---|---|
| `o.create_sample_type(...)`, `o.create_object_type(...)`, `o.create_collection_type()` | Not valid pyBIS 1.37.4 methods | Push masterdata via CLI (see Cell 7 reminder) |
| Hardcoded passwords or tokens | Security | PAT pattern in Cell 5 |
| `o.new_collection(...)` | Misnamed — not a real method on user notebooks | `o.new_experiment(...)` |
| Implicit save | pyBIS has no autosave | Always `.save()` after `new_*` |
| Bilingual strings with spaces around `//` | Convention | `"English//Deutsch"` exactly |

---

## Notebook structure (14 cells — MANDATORY)

The notebook MUST contain exactly these cells in this order. The cell count and structure is verified by the regression scorer (`_score.md` §5).

### Cell 1 — Markdown: header
```markdown
# <prd-stem> Workflow — openBIS Provisioning Notebook

PRD: <prd_path>
openBIS: 20.10.12.5 | pyBIS: 1.37.4
Generated: <ISO date>

This notebook is the **one-time setup path**. Run it once to create the Space/Project/Collection hierarchy. For per-run data ingestion, see the parser stub in cells 13-14.
```

### Cell 2 — Code: imports
```python
from pybis import Openbis
import getpass
```

### Cell 3 — Markdown: ⚠ Fill me in
```markdown
## ⚠ FILL ME IN before running

Set these variables in the next cell:
- `OPENBIS_URL` — your openBIS server URL
- `SPACE` — target space code
- `PROJECT_CODE` — target project code
- `COLLECTION_CODE` — target collection code
```

### Cell 4 — Code: config
```python
OPENBIS_URL = "https://your-openbis-instance.example.com"  # TODO: replace
SPACE = "YOUR_SPACE"          # TODO: replace
PROJECT_CODE = "YOUR_PROJECT"  # TODO: replace
COLLECTION_CODE = "<PRD_STEM>_01"  # TODO: replace
SESSION_NAME = "<prd-stem>-provisioning"
```

### Cell 5 — Code: PAT bootstrap (first-run only)
```python
o = Openbis(OPENBIS_URL, verify_certificates=True)
username = input("openBIS username: ")
password = getpass.getpass("Password (first run only — PAT will be saved): ")
o.login(username, password, save_token=True)
token = o.get_or_create_personal_access_token(sessionName=SESSION_NAME)
print(f"PAT created: {token[:8]}…  Save this in a password manager.")
o.logout()
# From now on, use PAT only:
o = Openbis(OPENBIS_URL, verify_certificates=True)
o.set_token(token, save_token=True)
```

### Cell 6 — Code: sanity check
```python
assert o.is_session_active(), "Session not active — re-run PAT bootstrap cell"
print("Connected to openBIS. Session active.")
```

### Cell 7 — Markdown: masterdata sync reminder
```markdown
## Before continuing: push the masterdata extension

The custom types referenced below MUST exist in openBIS before any `new_sample(type=...)` call. Push them via:

```bash
pip install -e ../bam-masterdata
python -m bam_masterdata masterdata_sync --url $OPENBIS_URL --token <your-pat>
```

Or submit `generated/<prd-stem>/datamodel/` as a PR to `BAMresearch/bam-masterdata` and wait for it to be merged + deployed.
```

### Cell 8 — Code: create Collection (Experiment)
```python
project_id = f"/{SPACE}/{PROJECT_CODE}"
collection = o.new_experiment(
    code=COLLECTION_CODE,
    type="DEFAULT_EXPERIMENT",
    project=project_id,
)
collection.save()
COLLECTION_ID = f"{project_id}/{COLLECTION_CODE}"
print(f"Collection created: {collection.permId}  identifier={COLLECTION_ID}")
```

### Cell 9 — Code: create parent specimen Object (one or more)
For each ObjectType in requirements.json classified as CREATE (e.g., `WeldedFatigueSpecimen`):
```python
# WeldedFatigueSpecimen — SPECIMEN.WELDED_FATIGUE
specimen = o.new_sample(
    type="SPECIMEN.WELDED_FATIGUE",
    space=SPACE,
    experiment=COLLECTION_ID,
    props={
        # TODO: fill in property values per your specimen
        # "original_id": "...",
        # "weld_geometry": "BUTT_WELD",  # or CRUCIFORM_WELD (after WELDING.WELD_TYPE PR is merged)
    },
)
specimen.save()
print(f"Specimen created: {specimen.permId}")
```

### Cell 10 — Code: create ExperimentalStep children (one sub-cell per step)
For each ExperimentalStep in requirements.json (CREATE only per gap report):
```python
# PreQualityCheckWeld — EXPERIMENTAL_STEP.PRE_QUALITY_CHECK_WELD
pre_qc = o.new_sample(
    type="EXPERIMENTAL_STEP.PRE_QUALITY_CHECK_WELD",
    space=SPACE,
    experiment=COLLECTION_ID,
    parents=[specimen.permId],  # link to parent specimen
    props={
        # TODO: fill in
        # "initial_angular_distortion": 0.5,
        # "initial_edge_misalignment": 0.2,
        # "was_straightened": False,
    },
)
pre_qc.save()
print(f"PreQualityCheckWeld created: {pre_qc.permId}")

# Repeat for all 12 ExperimentalSteps from requirements.json
```

### Cell 11 — Code: dataset upload stubs
```python
# Example: attach load program to CyclicFatigueTest
# ds = o.new_dataset(
#     type="ANALYZED_DATA",
#     sample=cyclic_fatigue_test.permId,
#     files=["path/to/load_program.xlsx"],  # TODO: replace
#     props={},
# )
# ds.save()
# print(f"Dataset uploaded: {ds.permId}")
```

### Cell 12 — Code: logout
```python
o.logout()
print("Session closed.")
```

### Cell 13 — Markdown: Using parsers for ongoing ingestion
```markdown
## Using parsers for ongoing data ingestion

This notebook (cells 1-12) is the **one-time setup**: it creates the Space/Project/Collection hierarchy and parent specimen objects.

For **per-run ingestion** (pushing new ExperimentalStep objects after each experiment), use the parser package generated by `/bam-generate-parser`:

```bash
pip install -e generated/<prd-stem>/parsers/
```

Then use the parser via `run_parser()` (see Cell 14 stub).
```

### Cell 14 — Code: parser usage stub
```python
# TODO: pip install -e generated/<prd-stem>/parsers/ first
# from <prd_stem>_parser import <ClusterName>Parser
# from bam_masterdata.cli.run_parser import run_parser
#
# run_parser(
#     openbis=o,
#     space_name=SPACE,
#     project_name=PROJECT_CODE,
#     collection_name=COLLECTION_CODE,
#     files_parser={<ClusterName>Parser(): ["your_data.csv"]},  # TODO: replace path
#     collection_type="DEFAULT_EXPERIMENT",
# )
```

---

## nbformat structure

Write the notebook as valid JSON conforming to nbformat 4.4:

```json
{
  "cells": [...],
  "metadata": {
    "kernelspec": {"name": "python3", "display_name": "Python 3"},
    "language_info": {"name": "python"}
  },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

- Code cells: `{"cell_type": "code", "source": [...], "outputs": [], "execution_count": null, "metadata": {}}`
- Markdown cells: `{"cell_type": "markdown", "source": [...], "metadata": {}}`
- `source` is a list of strings (each ending in `\n` except the last)

---

## Self-verification

Before returning, run:

```bash
python -c "import nbformat; nb = nbformat.read(open('notebooks/<prd-stem>_provisioning.ipynb'), as_version=4); print(f'Valid: {len(nb.cells)} cells')"
grep -c "password\|getpass.getpass" notebooks/<prd-stem>_provisioning.ipynb  # should be exactly 1 (Cell 5 PAT bootstrap)
grep -nE "o\.create_|o\.new_collection\(" notebooks/<prd-stem>_provisioning.ipynb  # must be empty
```

---

## Hard constraints

| Constraint | Reason |
|---|---|
| No hardcoded credentials | Security |
| `getpass.getpass` only in Cell 5 (PAT bootstrap) | All other auth via PAT |
| No `o.create_*` calls | Not valid pyBIS 1.37.4 |
| No `o.new_collection()` | Use `o.new_experiment()` |
| Always `.save()` after `new_*` | pyBIS has no autosave |
| Valid nbformat 4.4 JSON | `nbformat.read` must pass |
| Exactly 14 cells in mandated order | Regression scorer checks structure |
| Cells 13-14 must reference parser | Documents two-path architecture |
