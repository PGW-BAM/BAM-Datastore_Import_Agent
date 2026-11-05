"""Import shim for the welded_fatigue_v2 datamodel classes.

Resolution order:

1. ``bam_masterdata.datamodel.fatigue.object_types`` - where the classes live once the masterdata PR
   (generated/welded_fatigue_v2/datamodel/README.md) is merged. Nothing is patched in that case.
2. The generated, not-yet-merged files ``generated/welded_fatigue_v2/datamodel/{object_types,vocabularies}.py``
   (directory overridable with the env var ``WELDED_FATIGUE_V2_DATAMODEL_DIR``).

Why (2) needs a small patch: ``ObjectType.__setattr__`` validates CONTROLLEDVOCABULARY values by scanning only the
``vocabularies.py`` files below ``bam_masterdata.utils.DATAMODEL_DIR``. The generated vocabularies
(FATIGUE.TERMINATION_REASON, FATIGUE.RECORDING_MODE, WELDED_FATIGUE_WORKFLOW_STEP) are not there before the PR, so
the scan list used by ``bam_masterdata.metadata.entities`` is extended by the generated ``vocabularies.py``.
The patch is additive (upstream files are still scanned first), idempotent, and is not applied in case (1).
Delete this module and import from ``bam_masterdata.datamodel.fatigue.object_types`` after the merge.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

DATAMODEL_SOURCE: str


def _default_datamodel_dir() -> Path:
    env = os.environ.get("WELDED_FATIGUE_V2_DATAMODEL_DIR")
    if env:
        return Path(env).resolve()
    # parsers/src/welded_fatigue_v2_parser/_datamodel.py -> generated/welded_fatigue_v2/datamodel
    return Path(__file__).resolve().parents[3] / "datamodel"


def _load_module(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _register_vocabularies(vocab_file: Path) -> None:
    """Make the generated vocabularies visible to bam-masterdata's CONTROLLEDVOCABULARY validation."""
    from bam_masterdata.metadata import entities

    original = entities.listdir_py_modules
    if getattr(original, "_welded_fatigue_v2_patched", False):
        return

    def listdir_py_modules_with_generated(directory_path, *args, **kwargs):
        files = list(original(directory_path, *args, **kwargs))
        extra = str(vocab_file)
        if extra not in files:
            files.append(extra)
        return files

    listdir_py_modules_with_generated._welded_fatigue_v2_patched = True  # type: ignore[attr-defined]
    entities.listdir_py_modules = listdir_py_modules_with_generated


try:  # (1) after the PR
    from bam_masterdata.datamodel.fatigue.object_types import (  # type: ignore[import-not-found]
        CyclicFatigueTest,
        WeldedFatigueSpecimen,
    )

    DATAMODEL_SOURCE = "bam_masterdata.datamodel.fatigue"
except ImportError:  # (2) before the PR: generated files
    _dir = _default_datamodel_dir()
    _obj_file = _dir / "object_types.py"
    _vocab_file = _dir / "vocabularies.py"
    if not _obj_file.is_file() or not _vocab_file.is_file():
        raise ImportError(
            f"welded_fatigue_v2 datamodel not found: neither bam_masterdata.datamodel.fatigue nor {_dir}. "
            "Set WELDED_FATIGUE_V2_DATAMODEL_DIR to the generated datamodel directory."
        )
    _register_vocabularies(_vocab_file)
    _object_types = _load_module("welded_fatigue_v2_datamodel.object_types", _obj_file)
    WeldedFatigueSpecimen = _object_types.WeldedFatigueSpecimen
    CyclicFatigueTest = _object_types.CyclicFatigueTest
    DATAMODEL_SOURCE = str(_dir)

__all__ = ["CyclicFatigueTest", "WeldedFatigueSpecimen", "DATAMODEL_SOURCE"]
