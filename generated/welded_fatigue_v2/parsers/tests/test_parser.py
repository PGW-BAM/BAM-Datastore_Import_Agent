"""Tests for CyclicFatigueTestParser - no openBIS connection (RunParsers is driven by a MagicMock)."""

from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from welded_fatigue_v2_parser import CyclicFatigueTestParser
from welded_fatigue_v2_parser.parser import (
    RowError,
    format_dms_drop_cycles,
    map_recording_mode,
    map_termination_reason,
    next_step_for,
    parse_int,
    read_summary_csv,
)

LOG = logging.getLogger("test")
TEST_TYPE = "EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST"
SPECIMEN_TYPE = "SAMPLE.WELDED_FATIGUE_SPECIMEN"


def _by_code(collection, type_code):
    return {o.code: o for o in collection.attached_objects.values() if o.defs.code == type_code}


# ---------------------------------------------------------------------------------------------- vocabulary mapping
@pytest.mark.parametrize(
    "text, term",
    [
        ("TOTAL_FRACTURE", "TOTAL_FRACTURE"),
        ("Total fracture", "TOTAL_FRACTURE"),
        ("total-fracture", "TOTAL_FRACTURE"),
        ("Bruch", "TOTAL_FRACTURE"),
        ("Totalbruch", "TOTAL_FRACTURE"),
        ("specimen broken", "TOTAL_FRACTURE"),
        ("crack detected", "CRACK_DETECTED"),
        ("Anriss erkannt", "CRACK_DETECTED"),
        ("Riss", "CRACK_DETECTED"),
        ("run-out", "RUN_OUT"),
        ("Run out", "RUN_OUT"),
        ("RUNOUT", "RUN_OUT"),
        ("Durchläufer", "RUN_OUT"),
        ("no fracture (run-out)", "RUN_OUT"),
        ("manual stop", "MANUAL_STOP"),
        ("manueller Abbruch", "MANUAL_STOP"),  # contains 'bruch' but must not become TOTAL_FRACTURE
        ("Abbruch", "MANUAL_STOP"),
        ("stopped by operator", "MANUAL_STOP"),
    ],
)
def test_map_termination_reason(text, term):
    assert map_termination_reason(text) == term


@pytest.mark.parametrize("text", ["", "   ", "exploded somehow", "42"])
def test_map_termination_reason_rejects_unknown(text):
    with pytest.raises(RowError):
        map_termination_reason(text)


@pytest.mark.parametrize(
    "text, term",
    [
        ("Peak-Valley", "PEAK_VALLEY"),
        ("full signal", "FULL_SIGNAL"),
        ("PEAK_COUNTER", "PEAK_COUNTER"),
        ("min/max", "PEAK_VALLEY"),
    ],
)
def test_map_recording_mode(text, term):
    assert map_recording_mode(text) == term


def test_next_step():
    assert next_step_for("RUN_OUT") == "DONE"
    for term in ("TOTAL_FRACTURE", "CRACK_DETECTED", "MANUAL_STOP"):
        assert next_step_for(term) == "S12_FRACTURE_SURFACE_ANALYSIS"


def test_value_helpers():
    assert parse_int("1.234.567", "c") == 1234567
    assert parse_int("512 400", "c") == 512400
    assert parse_int("2e6", "c") == 2000000
    with pytest.raises(RowError):
        parse_int("12.5", "c")
    assert format_dms_drop_cycles("DMS1:214000;DMS2:219500") == "DMS1: 214000\nDMS2: 219500"
    assert format_dms_drop_cycles("DMS1=498000") == "DMS1: 498000"
    with pytest.raises(RowError):
        format_dms_drop_cycles("DMS1 214000")


def test_read_summary_csv(sample_csv):
    rows = read_summary_csv(sample_csv)
    assert len(rows) == 5
    assert rows[0]["specimen"] == "S1B-01"
    assert rows[0]["dms_drop_cycles"] == "DMS1:214000;DMS2:219500"  # quoted ';' inside a ';'-delimited file


def test_read_comma_csv_with_aliases(tmp_path):
    f = tmp_path / "summary.csv"
    f.write_text(
        "Specimen Code,Termination Reason,N gross,N net\nS1B-07,fracture,100000,99000\n",
        encoding="utf-8",
    )
    assert read_summary_csv(f) == [
        {
            "specimen": "S1B-07",
            "termination_reason": "fracture",
            "cycles_gross": "100000",
            "cycles_net": "99000",
        }
    ]


def test_missing_required_column(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("specimen,cycles_gross\nS1B-01,1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="termination_reason"):
        read_summary_csv(f)


# ---------------------------------------------------------------------------------------------- parse()
def test_parse_updates_test_objects_and_next_step(sample_csv, empty_collection):
    parser = CyclicFatigueTestParser(bam_oe="VP.7")
    parser.parse([str(sample_csv)], empty_collection, logger=LOG)

    tests = _by_code(empty_collection, TEST_TYPE)
    specimens = _by_code(empty_collection, SPECIMEN_TYPE)
    # S1C-03 has an unmappable termination reason -> skipped entirely (no wrong NEXT_STEP)
    assert set(tests) == {"S1B-01-TEST", "S1B-02-TEST", "S1C-01-TEST", "S1C-02-TEST"}
    assert set(specimens) == {"S1B-01", "S1B-02", "S1C-01", "S1C-02"}
    assert len(parser.errors) == 1 and "S1C-03" in parser.errors[0]
    assert empty_collection.relationships == {}  # TEST is already a child of the specimen (steps 07-09)

    t = tests["S1B-01-TEST"]
    assert t.termination_reason == "TOTAL_FRACTURE"
    assert t.beach_marks_active is True
    assert t.sampling_frequency == 1200
    assert t.recording_mode == "PEAK_VALLEY"
    assert (t.cycles_gross, t.cycles_net) == (245310, 243000)
    assert t.cycles_to_10_percent_strain_gauge_drop == "DMS1: 214000\nDMS2: 219500"
    assert (t.start_date, t.end_date) == ("2026-09-01 08:15:00", "2026-09-03 17:40:12")
    assert t.finished_flag is True

    t2 = tests["S1B-02-TEST"]
    assert (t2.termination_reason, t2.sampling_frequency, t2.recording_mode) == ("RUN_OUT", 1200, "FULL_SIGNAL")
    assert t2.beach_marks_active is False
    assert t2.start_date == "2026-09-01 09:00:00"
    assert t2.cycles_to_10_percent_strain_gauge_drop == "DMS1: no drop\nDMS2: no drop"
    assert tests["S1C-01-TEST"].termination_reason == "CRACK_DETECTED"
    assert tests["S1C-01-TEST"].cycles_gross == 512400
    assert tests["S1C-02-TEST"].termination_reason == "MANUAL_STOP"

    assert specimens["S1B-01"].next_step == "S12_FRACTURE_SURFACE_ANALYSIS"
    assert specimens["S1B-02"].next_step == "DONE"  # run-out: no fracture surface
    assert specimens["S1C-01"].next_step == "S12_FRACTURE_SURFACE_ANALYSIS"
    assert specimens["S1C-02"].next_step == "S12_FRACTURE_SURFACE_ANALYSIS"
    assert specimens["S1B-01"].name == "S1B-01"


def test_only_set_properties_are_sent(sample_csv, empty_collection):
    """The specimen update must not touch any other specimen property (steps 01-06 data stay intact)."""
    from bam_masterdata.metadata.definitions import PropertyTypeAssignment

    CyclicFatigueTestParser(bam_oe="VP.7").parse([str(sample_csv)], empty_collection, logger=LOG)
    spec = _by_code(empty_collection, SPECIMEN_TYPE)["S1B-01"]
    sent = {
        meta.code
        for key, meta in spec._property_metadata.items()
        if not isinstance(getattr(spec, key, None), PropertyTypeAssignment)
    }
    assert sent == {"$NAME", "BAM_OE", "FATIGUE.NEXT_STEP"}


def test_without_bam_oe_only_tests_are_updated(sample_csv, empty_collection):
    parser = CyclicFatigueTestParser()
    parser.parse([str(sample_csv)], empty_collection, logger=LOG)
    assert len(_by_code(empty_collection, TEST_TYPE)) == 4
    assert _by_code(empty_collection, SPECIMEN_TYPE) == {}
    assert sum("NEXT_STEP not set" in e for e in parser.errors) == 4


def test_destination_by_prefix(sample_csv, empty_collection):
    parser = CyclicFatigueTestParser(
        bam_oe="VP.7",
        project="WELDED_FATIGUE",
        collection_by_prefix={"S1B": "SERIES_1_BUTT_WELD", "S1C": "SERIES_1_CRUCIFORM_WELD"},
    )
    parser.parse([str(sample_csv)], empty_collection, logger=LOG)
    by_code = {o.code: oid for oid, o in empty_collection.attached_objects.items()}
    assert empty_collection.destinations[by_code["S1B-01-TEST"]].collection == "SERIES_1_BUTT_WELD"
    assert empty_collection.destinations[by_code["S1C-02"]].collection == "SERIES_1_CRUCIFORM_WELD"
    assert empty_collection.destinations[by_code["S1C-02"]].project == "WELDED_FATIGUE"


def test_non_csv_files_are_ignored(tmp_path, empty_collection):
    raw = tmp_path / "measurement.raw"
    raw.write_bytes(b"\x00\x01")
    CyclicFatigueTestParser(bam_oe="VP.7").parse([str(raw)], empty_collection, logger=LOG)
    assert empty_collection.attached_objects == {}


# ---------------------------------------------------------------------------------------------- RunParsers (mocked)
def _mock_openbis(existing_codes):
    openbis = MagicMock()
    openbis.username = "tester"
    space, project, coll = MagicMock(), MagicMock(), MagicMock()
    space.code, project.code, coll.code = "FB_72", "WELDED_FATIGUE", "SERIES_1"
    openbis.get_space.return_value = space
    space.get_project.return_value = project
    project.get_collections.return_value = [coll]
    registry = {}
    for code in existing_codes:
        obj = MagicMock()
        obj.identifier = f"/FB_72/WELDED_FATIGUE/SERIES_1/{code}"
        registry[obj.identifier] = obj

    def get_object(identifier):
        if identifier not in registry:
            raise KeyError(identifier)
        return registry[identifier]

    openbis.get_object.side_effect = get_object
    return openbis, registry


def test_run_parsers_updates_existing_objects(sample_csv):
    from bam_masterdata.cli.run_parser import RunParsers

    codes = ["S1B-01", "S1B-02", "S1C-01", "S1C-02"]
    openbis, registry = _mock_openbis(codes + [f"{c}-TEST" for c in codes])
    runner = RunParsers(
        openbis=openbis,
        space_name="FB_72",
        project_name="WELDED_FATIGUE",
        collection_name="SERIES_1",
        files_parser={CyclicFatigueTestParser(bam_oe="VP.7"): [str(sample_csv)]},
    )
    runner.run()

    openbis.new_object.assert_not_called()  # nothing is created, only updated
    test_props = registry["/FB_72/WELDED_FATIGUE/SERIES_1/S1B-01-TEST"].set_props.call_args.args[0]
    assert test_props["fatigue.termination_reason"] == "TOTAL_FRACTURE"
    assert test_props["fatigue.cycles_net"] == 243000
    assert registry["/FB_72/WELDED_FATIGUE/SERIES_1/S1B-02"].set_props.call_args.args[0] == {
        "$name": "S1B-02",
        "bam_oe": "VP.7",
        "fatigue.next_step": "DONE",
    }
    for obj in registry.values():
        obj.save.assert_called()


def test_generated_vocabularies_are_validated():
    """The datamodel shim must make bam-masterdata validate the generated FATIGUE.* vocabularies."""
    from welded_fatigue_v2_parser._datamodel import CyclicFatigueTest

    test = CyclicFatigueTest(code="S1B-01-TEST")
    test.termination_reason = "RUN_OUT"
    with pytest.raises(ValueError, match="not in the list of allowed terms"):
        test.termination_reason = "FRACTURE"


def test_parser_has_no_direct_pybis_calls():
    import welded_fatigue_v2_parser.parser as module

    src = Path(module.__file__).read_text(encoding="utf-8")
    for sym in ("Openbis(", "new_sample(", "new_object(", "new_experiment(", "new_dataset(", "run_parser"):
        assert sym not in src
