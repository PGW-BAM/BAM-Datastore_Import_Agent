"""Smoke tests for welded_fatigue_parser.

These tests deliberately do NOT touch a live openBIS instance. They build an
in-memory CollectionType, call each parser's parse() with an empty file list,
and assert that the scaffolded objects were added.
"""

from __future__ import annotations

import pytest

from welded_fatigue_parser import (
    FatigueExecutionParser,
    InstrumentationParser,
    PreparationParser,
)


# --------------------------------------------------------------------------- #
# Instantiation                                                                #
# --------------------------------------------------------------------------- #


def test_preparation_parser_instantiates():
    parser = PreparationParser()
    assert parser is not None


def test_instrumentation_parser_instantiates():
    parser = InstrumentationParser()
    assert parser is not None


def test_fatigue_execution_parser_instantiates():
    parser = FatigueExecutionParser()
    assert parser is not None


# --------------------------------------------------------------------------- #
# Parse smoke tests                                                            #
# --------------------------------------------------------------------------- #


def _collection_size(collection) -> int:
    """Best-effort size lookup across CollectionType variants."""
    for attr in ("objects", "items", "_objects", "_items"):
        bucket = getattr(collection, attr, None)
        if bucket is not None:
            try:
                return len(bucket)
            except TypeError:
                continue
    # Fallback: assume the collection itself is iterable / sized.
    try:
        return len(collection)  # type: ignore[arg-type]
    except TypeError:
        return -1


def test_preparation_parse_adds_five_steps(empty_collection, test_logger):
    parser = PreparationParser()
    parser.parse(files=[], collection=empty_collection, logger=test_logger)
    size = _collection_size(empty_collection)
    assert size >= 5, (
        f"PreparationParser should add 5 ExperimentalSteps "
        f"(PreQualityCheckWeld, ChamferingGrinding, SpecimenRecording, "
        f"WeldAnalysis, SeriesAssignment); collection size = {size}"
    )


def test_instrumentation_parse_adds_four_steps(empty_collection, test_logger):
    parser = InstrumentationParser()
    parser.parse(files=[], collection=empty_collection, logger=test_logger)
    size = _collection_size(empty_collection)
    assert size >= 4, (
        f"InstrumentationParser should add 4 ExperimentalSteps "
        f"(TestSetupGeometry, MonitoringApplication, AmplifierSettings, "
        f"InstallationStressMeasurement); collection size = {size}"
    )


def test_fatigue_execution_parse_adds_three_steps(empty_collection, test_logger):
    parser = FatigueExecutionParser()
    parser.parse(files=[], collection=empty_collection, logger=test_logger)
    size = _collection_size(empty_collection)
    assert size >= 3, (
        f"FatigueExecutionParser should add 3 ExperimentalSteps "
        f"(CyclicFatigueTest, FatigueDataEvaluation, FractureSurfaceAnalysis); "
        f"collection size = {size}"
    )


def test_full_workflow_yields_twelve_steps(empty_collection, test_logger):
    """All three clusters together should reproduce all 12 FB7.2 steps."""
    PreparationParser().parse(files=[], collection=empty_collection, logger=test_logger)
    InstrumentationParser().parse(files=[], collection=empty_collection, logger=test_logger)
    FatigueExecutionParser().parse(files=[], collection=empty_collection, logger=test_logger)
    size = _collection_size(empty_collection)
    assert size >= 12, (
        f"Combined parsers should produce all 12 FB7.2 ExperimentalSteps; "
        f"collection size = {size}"
    )


# --------------------------------------------------------------------------- #
# Static checks: no pybis leakage, no self-invocation of run_parser            #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "forbidden",
    ["Openbis(", "new_sample(", "new_experiment(", "new_dataset(", "from pybis"],
)
def test_no_direct_pybis_calls(forbidden):
    """parser.py must not import or call pybis directly."""
    import welded_fatigue_parser.parser as parser_module

    with open(parser_module.__file__, encoding="utf-8") as f:
        src = f.read()
    assert forbidden not in src, (
        f"parser.py must not contain pybis symbol {forbidden!r}"
    )


def test_parser_does_not_call_run_parser():
    """parse() must never call its own runner."""
    import welded_fatigue_parser.parser as parser_module

    with open(parser_module.__file__, encoding="utf-8") as f:
        src = f.read()
    assert "run_parser" not in src, (
        "parser.py must not call run_parser() — that is the caller's job"
    )
