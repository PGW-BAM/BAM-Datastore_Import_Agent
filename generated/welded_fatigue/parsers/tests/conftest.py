"""Shared pytest fixtures for welded_fatigue_parser smoke tests."""

from __future__ import annotations

import logging

import pytest

try:
    from bam_masterdata.metadata.entities import CollectionType
except ImportError:  # pragma: no cover - allow tests to be collected without dep
    CollectionType = None  # type: ignore[assignment,misc]


@pytest.fixture
def empty_collection():
    """A fresh in-memory CollectionType for parser smoke tests."""
    if CollectionType is None:
        pytest.skip("bam-masterdata not installed; cannot build CollectionType")
    return CollectionType(code="TEST_COLLECTION")


@pytest.fixture
def test_logger() -> logging.Logger:
    """A standard-library logger usable in place of the structlog logger."""
    log = logging.getLogger("welded_fatigue_parser.tests")
    log.setLevel(logging.DEBUG)
    return log
