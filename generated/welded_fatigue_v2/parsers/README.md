# welded_fatigue_v2 parser - steps 10-11 (cyclic fatigue test + evaluation)

One parser for the flat welded-fatigue design (`design.md`): `CyclicFatigueTestParser`.
It reads the small CSV summary exported from the IMC evaluation and **updates existing objects**:

| Object (existing code) | Type | What is written |
|---|---|---|
| `<specimen>-TEST` | `EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST` | step 10: `FATIGUE.TERMINATION_REASON`, `FATIGUE.BEACH_MARKS_ACTIVE`; step 08 values reported by IMC: `FATIGUE.SAMPLING_FREQUENCY`, `FATIGUE.RECORDING_MODE`; step 11: `FATIGUE.CYCLES_GROSS`, `FATIGUE.CYCLES_NET`, `FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP`; inherited `START_DATE`, `END_DATE`, `FINISHED_FLAG=true` |
| `<specimen>` | `SAMPLE.WELDED_FATIGUE_SPECIMEN` | `FATIGUE.NEXT_STEP` = `S12_FRACTURE_SURFACE_ANALYSIS`, or `DONE` for `RUN_OUT` (a run-out has no fracture surface). Also `$NAME` and `BAM_OE` - see "Limitations". |

How the update works (bam-masterdata class-based API, #332/#376): the parser sets `obj.code` to the existing code and
calls `collection.add(obj, destination=...)`. `RunParsers.run()` builds the identifier from that code, finds the object
with `openbis.get_object()` and calls `set_props()` with **only the properties set by the parser** (unset properties
are skipped), so data from steps 01-09 is not touched. No relationship is added: the TEST object is already a child of
the specimen (created in steps 07-09). Steps 07-09 and 12 are not covered by this parser.

## Input CSV

One row per specimen. Delimiter `;`, `,` or tab (detected from the header); UTF-8 or cp1252; `#` lines are comments.
Header names are case/space-insensitive; aliases in `COLUMN_ALIASES` (`parser.py`). Empty cells are not written.

| Column | Required | Target | Accepted values |
|---|---|---|---|
| `specimen` | yes | object codes `<specimen>`, `<specimen>-TEST` | e.g. `S1B-01` (a trailing `-TEST` is tolerated) |
| `termination_reason` | yes | `FATIGUE.TERMINATION_REASON` | term codes or free text, see mapping below |
| `start`, `end` | no | `START_DATE`, `END_DATE` | ISO 8601 (`2026-09-01 08:15:00`, `2026-09-01T08:15`) or `01.09.2026 08:15[:00]` |
| `cycles_gross`, `cycles_net` | no | `FATIGUE.CYCLES_GROSS`, `FATIGUE.CYCLES_NET` | integers; `1 234 567`, `1.234.567`, `2e6` accepted; net > gross is rejected |
| `beach_marks_active` | no | `FATIGUE.BEACH_MARKS_ACTIVE` | `yes/no`, `ja/nein`, `true/false`, `1/0`, `x` |
| `sampling_frequency` | no | `FATIGUE.SAMPLING_FREQUENCY` [Hz] | `1200`, `1200 Hz`, `1.2 kHz` |
| `recording_mode` | no | `FATIGUE.RECORDING_MODE` | `FULL_SIGNAL` (full signal, Vollsignal), `PEAK_COUNTER` (peak counter), `PEAK_VALLEY` (peak-valley, min/max) |
| `dms_drop_cycles` | no | `FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP` | `"DMS1:214000;DMS2:219500"` (quote it in a `;` file; `=` also allowed, `none` = no drop) -> stored one gauge per line |
| `specimen_name` | no | specimen `$NAME` | default: the specimen code (= series designation, design.md 3.1) |
| `bam_oe` | no | specimen `BAM_OE` | overrides the parser argument `bam_oe` |

Example: `tests/data/imc_summary_sample.csv`.

### Termination reason mapping

1. Exact term code (`TOTAL_FRACTURE`, `CRACK_DETECTED`, `RUN_OUT`, `MANUAL_STOP`, any case / `-` / space).
2. Exact synonym, e.g. `fracture`, `Bruch`, `Totalbruch` -> TOTAL_FRACTURE; `crack`, `Anriss` -> CRACK_DETECTED;
   `runout`, `Durchläufer` -> RUN_OUT; `manual`, `Abbruch`, `manueller Abbruch` -> MANUAL_STOP.
3. Keyword search in this order: RUN_OUT > MANUAL_STOP > CRACK_DETECTED > TOTAL_FRACTURE
   (so `no fracture (run-out)` -> RUN_OUT and `Abbruch` is not read as `Bruch`).
4. Anything else: the **whole row is skipped** and reported in `parser.errors` / the log - no guessed term and no
   wrong `NEXT_STEP`.

`MANUAL_STOP` and `CRACK_DETECTED` lead to `S12_FRACTURE_SURFACE_ANALYSIS` as specified; only `RUN_OUT` leads to `DONE`.

## Use

```python
from bam_masterdata.cli.run_parser import RunParsers
from welded_fatigue_v2_parser import CyclicFatigueTestParser

RunParsers(
    openbis=o,                               # pybis.Openbis, logged in with a PAT
    space_name="FB_72",
    project_name="WELDED_FATIGUE",
    collection_name="SERIES_1_BUTT_WELD",    # where the <specimen> / <specimen>-TEST objects live
    files_parser={CyclicFatigueTestParser(bam_oe="<BAM_OE term>"): ["imc_summary.csv"]},
).run()                                      # or RunParsersWithTransactions(...).run()
```

A CSV with specimens of both series: pass `project="WELDED_FATIGUE", collection_by_prefix={"S1B": "SERIES_1_BUTT_WELD",
"S1C": "SERIES_1_CRUCIFORM_WELD"}`; each object then gets a `Destination` and lands in its own series collection.

## Datamodel import (before / after the masterdata PR)

`src/welded_fatigue_v2_parser/_datamodel.py` resolves `WeldedFatigueSpecimen` / `CyclicFatigueTest`:

1. `bam_masterdata.datamodel.fatigue.object_types` - after the PR (generated/welded_fatigue_v2/datamodel/README.md)
   is merged. Nothing is patched then.
2. Otherwise the generated files `generated/welded_fatigue_v2/datamodel/object_types.py` (path relative to this
   package, override with env var `WELDED_FATIGUE_V2_DATAMODEL_DIR`), loaded with `importlib`. Because
   bam-masterdata validates CONTROLLEDVOCABULARY values only against `vocabularies.py` files inside its own
   `datamodel/` directory, the shim additionally appends the generated `vocabularies.py` to that scan list
   (additive, idempotent). Without it, setting `FATIGUE.TERMINATION_REASON` would fail with
   "No matching vocabulary class".

After the merge: delete `_datamodel.py` and import from `bam_masterdata.datamodel.fatigue.object_types` in `parser.py`.

## Limitations

- **Mandatory properties on update.** `CollectionType.add()` checks mandatory properties also for objects that only
  get updated. `SAMPLE.WELDED_FATIGUE_SPECIMEN` inherits two mandatory ones from `Sample`: `$NAME` (set to the
  specimen code or `specimen_name`) and `BAM_OE` (parser argument or `bam_oe` column). Both are therefore re-sent
  with the update. Without a BAM_OE value the specimen update is skipped (logged, in `parser.errors`) and only the
  TEST object is updated. On dev1 `BAM_OE` is not assigned yet (gap-report.md: BAM vocabularies missing) - there
  use `update_specimen=False` and set NEXT_STEP by hand until the BAM standard masterdata is synced.
  Upstream improvement worth proposing: skip the mandatory check for objects with an explicit `code` (updates).
- **Identifier.** `RunParsers` looks objects up as `/SPACE/PROJECT/COLLECTION/CODE` when a collection is set. If the
  lookup misses, RunParsers would *create* a new object with that code (openBIS then rejects the duplicate code).
  Pass the collection the objects actually live in.
- Raw files of steps 10/11 (IMC `.raw`, cleaned data, plots, scripts) are not attached as datasets by this parser.

## Install / test

```bash
pip install -e generated/welded_fatigue_v2/parsers[dev]     # optional; tests also run without install
python -m pytest generated/welded_fatigue_v2/parsers/tests -q
```

Tests never contact openBIS: they parse into an in-memory `CollectionType` and drive `RunParsers` with a
`MagicMock` openBIS that already holds the specimen and TEST objects (asserts `set_props`, no `new_object`).
Note: one parse takes a few seconds because bam-masterdata imports every vocabulary module per vocabulary value.
