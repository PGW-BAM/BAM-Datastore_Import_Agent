# welded_fatigue Parser

AbstractParser scaffold for the BAM FB7.2 welded fatigue workflow.

Three parser classes, one per workflow cluster:

| Parser class            | FB7.2 §       | ExperimentalSteps                                                                                  |
|-------------------------|---------------|----------------------------------------------------------------------------------------------------|
| `PreparationParser`     | 5.3.1 – 5.3.5 | PreQualityCheckWeld, ChamferingGrinding, SpecimenRecording, WeldAnalysis, SeriesAssignment         |
| `InstrumentationParser` | 5.3.6 – 5.3.9 | TestSetupGeometry, MonitoringApplication, AmplifierSettings, InstallationStressMeasurement         |
| `FatigueExecutionParser`| 5.3.10 – 5.3.12 | CyclicFatigueTest, FatigueDataEvaluation, FractureSurfaceAnalysis                                |

## Install

```bash
pip install -e generated/welded_fatigue/parsers/
```

## Customize

Open `src/welded_fatigue_parser/parser.py`. Each `parse()` method contains a single
`# TODO: open files and extract data` stub plus pre-wired object instantiations
and parent/child relationships. You only need to:

1. Open the instrument files passed via `files`.
2. Extract values.
3. Pass them as keyword arguments when instantiating each `ExperimentalStep`.

The object structure and parent/child wiring are already scaffolded.

## Use

```python
from welded_fatigue_parser import (
    PreparationParser,
    InstrumentationParser,
    FatigueExecutionParser,
)
from bam_masterdata.cli.run_parser import run_parser

run_parser(
    openbis=o,
    space_name="MY_SPACE",
    project_name="MY_PROJECT",
    collection_name="MY_COLLECTION",
    files_parser={
        PreparationParser():      ["prep_data.json"],
        InstrumentationParser():  ["rig_setup.csv"],
        FatigueExecutionParser(): ["fatigue_log.tsv", "fracture_meta.json"],
    },
    collection_type="DEFAULT_EXPERIMENT",
)
```

## Test

```bash
python -m pytest generated/welded_fatigue/parsers/tests/ -v
```

## Constraints (preserved by design)

- No pybis imports anywhere under `src/`.
- No call to `run_parser()` from inside any parser's `parse()` method.
- No `pyproject.toml` entry point (programmatic use only — not Parser App registration).
- One parser class per workflow cluster (not per ExperimentalStep).
