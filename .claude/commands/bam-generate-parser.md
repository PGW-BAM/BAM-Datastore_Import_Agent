# /bam-generate-parser

Generate an AbstractParser subclass scaffold for each workflow cluster in the PRD.

## Usage

```
/bam-generate-parser <prd-path>
```

Example:
```
/bam-generate-parser BAM_PRD_Workflow_FB72.md
```

## Pre-requisites

Before running this command, ensure:
- [ ] `/bam-analyze-prd <prd-path>` has been run and `generated/<prd-stem>/gap-report.md` exists.
- [ ] The gap report has been reviewed — workflow clusters and ExperimentalStep types are confirmed.
- [ ] `generated/<prd-stem>/datamodel/object_types.py` exists (run `/bam-generate-types` first if not).

## What this command does

Invokes the `openbis-parser-generator` agent with the provided PRD path.

The agent will:
1. Read `generated/<prd-stem>/gap-report.md` to identify workflow clusters.
2. Read `generated/<prd-stem>/datamodel/object_types.py` for the ObjectType classes.
3. Generate a complete parser package at `generated/<prd-stem>/parsers/` including:
   - One `AbstractParser` subclass per workflow cluster
   - In-memory smoke tests (no live openBIS needed)
   - `pyproject.toml` for `pip install -e` installation
   - `README.md` with usage instructions

## Output

```
generated/<prd-stem>/parsers/
├── pyproject.toml
├── README.md
├── src/
│   └── <prd_stem>_parser/
│       ├── __init__.py
│       ├── parser.py       ← implement # TODO stubs here
│       └── _version.py
└── tests/
    ├── conftest.py
    └── test_parser.py
```

## After generation

Install and test the scaffold:

```bash
pip install -e generated/<prd-stem>/parsers/
python -m pytest generated/<prd-stem>/parsers/tests/ -v
```

Then open `parser.py` and replace the `# TODO: open files and extract data` stubs with real file I/O for your instrument format.

## Architecture note

This command generates the **ongoing ingestion path** — complementary to the one-time provisioning notebook:

| Path | When | Command |
|---|---|---|
| Provisioning notebook | Once, to create Space/Project/Collection + parent specimens | `/bam-generate-notebook` |
| Parser package | After every experiment, to push new ExperimentalStep objects | `/bam-generate-parser` |

## Invoking the agent

Use the `openbis-parser-generator` agent with the PRD path as input:

```
<agent>openbis-parser-generator</agent>
Arguments: $ARGUMENTS
```
