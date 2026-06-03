# /bam-generate-types

Generate declarative bam-masterdata Python classes from a reviewed gap report.

## Usage

```
/bam-generate-types <prd-path>
```

Example:
```
/bam-generate-types BAM_PRD_Workflow_FB72.md
```

## Pre-requisites

- [ ] `/bam-analyze-prd <prd-path>` has been run.
- [ ] `generated/<prd-stem>/gap-report.md` has been reviewed and approved by a human.
- [ ] CREATE entries in the gap report are confirmed correct (no false CREATE).

## What this command does

Invokes the **`masterdata-extender`** agent:
- Input: `generated/<prd-stem>/requirements.json` + `generated/<prd-stem>/gap-report.md`
- Output:
  - `generated/<prd-stem>/datamodel/vocabularies.py`
  - `generated/<prd-stem>/datamodel/object_types.py`
  - `generated/<prd-stem>/datamodel/README.md`

The extender **REFUSES** to emit code for REUSE or EXTEND items. Only CREATE entities get Python class definitions.

## After generation

### Validate the generated code

```bash
# Syntax
python -c "import ast; ast.parse(open('generated/<prd-stem>/datamodel/vocabularies.py').read()); print('vocabularies.py OK')"
python -c "import ast; ast.parse(open('generated/<prd-stem>/datamodel/object_types.py').read()); print('object_types.py OK')"

# No forbidden API calls
grep -nE "o\.create_|o\.new_collection\(|password" generated/<prd-stem>/datamodel/*.py
# → must return empty
```

### Next steps

1. Review the generated Python in `generated/<prd-stem>/datamodel/`.
2. Open a PR against `BAMresearch/bam-masterdata`:
   ```bash
   cp -r generated/<prd-stem>/datamodel/ ../bam-masterdata/bam_masterdata/datamodel/<prd-stem>/
   cd ../bam-masterdata && git checkout -b add-<prd-stem>-types
   # Follow docs/howtos/extend_masterdata.md for PR instructions
   ```
3. Generate the provisioning notebook: `/bam-generate-notebook <prd-path>`.
4. Generate the parser scaffold: `/bam-generate-parser <prd-path>`.

## Print after success

```
Generated: generated/<prd-stem>/datamodel/
  vocabularies.py   ← <N> new vocabulary classes (CREATE only)
  object_types.py   ← <N> new ObjectType + ExperimentalStep classes (CREATE only)
  README.md         ← PR instructions + EXTEND/REUSE summaries

EXTEND actions required BEFORE this extension is usable:
  <list from README.md>

Next: /bam-generate-notebook <prd-path>
```

## Anti-patterns
- Do NOT run this without reviewing the gap report first.
- Do NOT edit generated files manually — re-run the generator if changes are needed.
- Do NOT push to bam-masterdata `main` directly — always via PR.
