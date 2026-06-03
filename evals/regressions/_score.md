# Regression Scoring Criteria

Used by `skill-reviewer` to evaluate runs captured under `runs/<ts>/output/`.

Each criterion has:
- A **check** (grep command, file existence, import test, etc.)
- An **expected result** (must match / must not match / exit code)
- A **weight** (1 = mandatory, 0.5 = important but not blocking)

Pass threshold: **score ≥ 0.90** (i.e. all weight-1 criteria + most weight-0.5 criteria).

---

## §1 bam-masterdata-explorer / CATALOG.md

Applies when: `runs/<ts>/output/CATALOG.md` exists.

| # | Check | Expected | Weight |
|---|---|---|---|
| C1 | `grep -c "TestingMachine" output/CATALOG.md` | ≥ 1 | 1 |
| C2 | `grep -c "Instrument" output/CATALOG.md` | ≥ 1 | 1 |
| C3 | `grep -c "FcgTest" output/CATALOG.md` | ≥ 1 | 1 |
| C4 | `grep -c "FcgStep" output/CATALOG.md` | ≥ 1 | 1 |
| C5 | `grep -c "Weldment" output/CATALOG.md` | ≥ 1 | 1 |
| C6 | `grep -c "WELDING.WELD_TYPE" output/CATALOG.md` | ≥ 1 | 1 |
| C7 | `grep -c "FCG_STEP_TYPE" output/CATALOG.md` | ≥ 1 | 1 |
| C8 | `grep -c "file:" output/CATALOG.md` | ≥ 10 (citations present) | 1 |
| C9 | `grep -c "UNCONFIRMED" output/CATALOG.md` | = 0 (no invented citations) | 0.5 |

---

## §2 prd-requirements-extractor / requirements.json

Applies when: `runs/<ts>/output/requirements.json` exists.

| # | Check | Expected | Weight |
|---|---|---|---|
| R1 | `python -c "import json; d=json.load(open('output/requirements.json')); assert 'vocabularies' in d"` | exit 0 | 1 |
| R2 | `python -c "import json; d=json.load(open('output/requirements.json')); assert 'experimental_steps' in d"` | exit 0 | 1 |
| R3 | `grep -c "WeldedFatigueSpecimen" output/requirements.json` | ≥ 1 | 1 |
| R4 | `grep -c "CyclicFatigueTest" output/requirements.json` | ≥ 1 | 1 |
| R5 | `python -c "import json; d=json.load(open('output/requirements.json')); steps=d.get('experimental_steps',[]); assert len(steps)>=10"` | exit 0 (≥10 steps extracted) | 1 |

---

## §3 gap-analyzer / gap-report.md

Applies when: `runs/<ts>/output/gap-report.md` exists.

| # | Check | Expected | Weight |
|---|---|---|---|
| G1 | `grep -c "WELD_GEOMETRY.*CREATE\|CREATE.*WELD_GEOMETRY" output/gap-report.md` | ≥ 1 | 1 |
| G2 | `grep -c "ISO_5817_FAT_CLASS.*CREATE\|CREATE.*ISO_5817_FAT_CLASS" output/gap-report.md` | ≥ 1 | 1 |
| G3 | `grep -c "LOAD_LEVEL.*CREATE\|CREATE.*LOAD_LEVEL" output/gap-report.md` | ≥ 1 | 1 |
| G4 | `grep -c "FATIGUE_STOP_REASON.*CREATE\|CREATE.*FATIGUE_STOP_REASON" output/gap-report.md` | ≥ 1 | 1 |
| G5 | `grep -c "TestingMachine.*REUSE\|REUSE.*TestingMachine" output/gap-report.md` | ≥ 1 (no false CREATE) | 1 |
| G6 | `grep -c "WELDING.WELD_TYPE.*EXTEND\|EXTEND.*WELDING.WELD_TYPE" output/gap-report.md` | ≥ 1 | 1 |
| G7 | `grep -c "file:" output/gap-report.md` | ≥ 5 (citations present for REUSE/EXTEND) | 1 |
| G8 | `grep -c "CREATE" output/gap-report.md` | ≥ 12 (12 ExperimentalSteps + vocabs) | 0.5 |

---

## §4 masterdata-extender / vocabularies.py + object_types.py

Applies when: `runs/<ts>/output/vocabularies.py` and `runs/<ts>/output/object_types.py` exist.

| # | Check | Expected | Weight |
|---|---|---|---|
| T1 | `python -c "import ast; ast.parse(open('output/vocabularies.py').read())"` | exit 0 (valid Python) | 1 |
| T2 | `python -c "import ast; ast.parse(open('output/object_types.py').read())"` | exit 0 (valid Python) | 1 |
| T3 | `grep -c "class WeldedFatigueSpecimen" output/object_types.py` | ≥ 1 | 1 |
| T4 | `grep -c "class CyclicFatigueTest" output/object_types.py` | ≥ 1 | 0.5 |
| T5 | `grep -c "o\.create_sample_type\|o\.create_object_type" output/vocabularies.py output/object_types.py` | = 0 (no forbidden API) | 1 |
| T6 | `grep -c "REUSE\|EXTEND" output/object_types.py` | = 0 (extender must not emit code for REUSE/EXTEND items) | 1 |

---

## §5 openbis-notebook-generator / provisioning.ipynb

Applies when: `runs/<ts>/output/provisioning.ipynb` exists.

| # | Check | Expected | Weight |
|---|---|---|---|
| N1 | `python -c "import nbformat; nbformat.read(open('output/provisioning.ipynb'), as_version=4)"` | exit 0 (valid notebook) | 1 |
| N2 | `grep -c "password\|PASSWORD\|getpass" output/provisioning.ipynb` | = 0 (no hardcoded credentials) | 1 |
| N3 | `grep -c "o.create_sample_type\|o.create_object_type" output/provisioning.ipynb` | = 0 (no forbidden API) | 1 |
| N4 | `grep -c "get_or_create_personal_access_token\|PAT\|personal_access_token" output/provisioning.ipynb` | ≥ 1 (PAT used) | 1 |
| N5 | `grep -c "FILL ME IN\|TODO\|OPENBIS_URL" output/provisioning.ipynb` | ≥ 1 (config cells present) | 0.5 |
| N6 | `grep -c "run_parser" output/provisioning.ipynb` | ≥ 1 (parser usage stub present in cell 13) | 0.5 |

---

## §6 openbis-parser-generator / parser.py

Applies when: `runs/<ts>/output/parser.py` exists.

| # | Check | Expected | Weight |
|---|---|---|---|
| P1 | `python -c "import ast; ast.parse(open('output/parser.py').read())"` | exit 0 (valid Python) | 1 |
| P2 | `grep -c "class.*AbstractParser" output/parser.py` | ≥ 1 | 1 |
| P3 | `grep -c "def parse" output/parser.py` | ≥ 1 | 1 |
| P4 | `grep -c "Openbis\|new_sample\|new_experiment\|new_dataset" output/parser.py` | = 0 (no pybis calls) | 1 |
| P5 | `grep -c "run_parser\|run_parser_with_transactions" output/parser.py` | = 0 (not called inside parser) | 1 |
| P6 | `grep -c "collection\.add\|collection\.add_relationship" output/parser.py` | ≥ 1 | 1 |
| P7 | `python -c "import ast; ast.parse(open('output/test_parser.py').read())"` | exit 0 (valid test file) | 1 |

---

## Scoring formula

```python
total_weight = sum(criterion.weight for criterion in all_criteria)
passed_weight = sum(criterion.weight for criterion in passed_criteria)
score = passed_weight / total_weight
pass = (score >= 0.90) and all(c.weight == 1 and c.passed for c in mandatory_criteria)
```

A run **fails** if:
- Any weight-1 criterion fails (hard failure), OR
- Score < 0.90 (too many weight-0.5 criteria failed).
