import sys
from pathlib import Path

import pytest

# Make `welded_fatigue_v2_parser` importable without `pip install -e .`
SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

DATA = Path(__file__).resolve().parent / "data"


@pytest.fixture
def sample_csv() -> Path:
    return DATA / "imc_summary_sample.csv"


@pytest.fixture
def empty_collection():
    from bam_masterdata.metadata.entities import CollectionType

    return CollectionType()
