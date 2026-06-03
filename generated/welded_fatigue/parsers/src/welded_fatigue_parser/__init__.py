"""welded_fatigue_parser — AbstractParser scaffolds for the FB7.2 welded fatigue workflow.

Three parser classes, one per workflow cluster:
- PreparationParser:        specimen preparation & series assignment
- InstrumentationParser:    test rig setup, monitoring, amplifier, installation stress
- FatigueExecutionParser:   cyclic fatigue test, data evaluation, fracture analysis
"""

from ._version import __version__
from .parser import (
    FatigueExecutionParser,
    InstrumentationParser,
    PreparationParser,
)

__all__ = [
    "PreparationParser",
    "InstrumentationParser",
    "FatigueExecutionParser",
    "__version__",
]
