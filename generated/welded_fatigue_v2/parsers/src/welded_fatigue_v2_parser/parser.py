"""Parser for workflow steps 10-11 (cyclic fatigue test + evaluation) of the welded fatigue workflow.

Input: a small CSV summary exported from the IMC evaluation, one row per specimen (columns: see README.md).

Per row the parser adds two objects to the collection, both identified by their EXISTING openBIS code so that
``RunParsers.run()`` updates them (``openbis.get_object(identifier)`` + ``set_props``) instead of creating new ones:

* ``<specimen>-TEST`` (EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST): FATIGUE.* values of steps 10 and 11,
  START_DATE / END_DATE, FINISHED_FLAG.
* ``<specimen>`` (SAMPLE.WELDED_FATIGUE_SPECIMEN): FATIGUE.NEXT_STEP = S12_FRACTURE_SURFACE_ANALYSIS, or DONE for a
  run-out (no fracture surface).

No relationship is added: the TEST object is already a child of the specimen (created in steps 07-09).
Only properties that are set here are sent to openBIS (unset PropertyTypeAssignments are skipped by RunParsers).
"""

from __future__ import annotations

import csv
import datetime as dt
import re
import unicodedata
from pathlib import Path
from typing import TYPE_CHECKING, Any

from bam_masterdata.logger import logger as default_logger
from bam_masterdata.metadata.destination import Destination
from bam_masterdata.metadata.entities import CollectionType
from bam_masterdata.parsing import AbstractParser

from ._datamodel import CyclicFatigueTest, WeldedFatigueSpecimen

if TYPE_CHECKING:
    from structlog._config import BoundLoggerLazyProxy


NEXT_STEP_AFTER_TEST = "S12_FRACTURE_SURFACE_ANALYSIS"
NEXT_STEP_RUN_OUT = "DONE"
TEST_CODE_SUFFIX = "-TEST"

# --------------------------------------------------------------------------------------------------------------------
# Column names (normalised: lower case, separators -> "_") and accepted aliases
# --------------------------------------------------------------------------------------------------------------------
COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "specimen": ("specimen", "specimen_code", "specimen_id", "probe", "proben_id", "sample"),
    "start": ("start", "start_date", "start_time", "test_start", "versuchsbeginn"),
    "end": ("end", "end_date", "end_time", "test_end", "versuchsende"),
    "cycles_gross": ("cycles_gross", "n_gross", "gross_cycles", "bruttoschwingspielzahl"),
    "cycles_net": ("cycles_net", "n_net", "net_cycles", "nettoschwingspielzahl"),
    "termination_reason": ("termination_reason", "termination", "end_criterion", "abbruchgrund"),
    "beach_marks_active": ("beach_marks_active", "beach_marks", "marker_loads", "rastlinien"),
    "sampling_frequency": ("sampling_frequency", "sampling_rate", "abtastfrequenz"),
    "recording_mode": ("recording_mode", "aufzeichnungsmodus"),
    "dms_drop_cycles": ("dms_drop_cycles", "strain_gauge_drop_cycles", "cycles_to_10_percent_drop"),
    "specimen_name": ("specimen_name", "name"),
    "bam_oe": ("bam_oe", "oe"),
}

# --------------------------------------------------------------------------------------------------------------------
# Vocabulary mapping
# --------------------------------------------------------------------------------------------------------------------
TERMINATION_REASON_TERMS = ("TOTAL_FRACTURE", "CRACK_DETECTED", "RUN_OUT", "MANUAL_STOP")

# Exact matches after normalisation (see _norm_key)
TERMINATION_REASON_SYNONYMS: dict[str, str] = {
    "total_fracture": "TOTAL_FRACTURE",
    "fracture": "TOTAL_FRACTURE",
    "fractured": "TOTAL_FRACTURE",
    "broken": "TOTAL_FRACTURE",
    "failure": "TOTAL_FRACTURE",
    "bruch": "TOTAL_FRACTURE",
    "totalbruch": "TOTAL_FRACTURE",
    "durchbruch": "TOTAL_FRACTURE",
    "crack": "CRACK_DETECTED",
    "crack_detected": "CRACK_DETECTED",
    "crack_detection": "CRACK_DETECTED",
    "riss": "CRACK_DETECTED",
    "anriss": "CRACK_DETECTED",
    "riss_erkannt": "CRACK_DETECTED",
    "run_out": "RUN_OUT",
    "runout": "RUN_OUT",
    "durchlaufer": "RUN_OUT",
    "durchlaeufer": "RUN_OUT",
    "manual_stop": "MANUAL_STOP",
    "manual": "MANUAL_STOP",
    "stopped": "MANUAL_STOP",
    "manually_stopped": "MANUAL_STOP",
    "operator_stop": "MANUAL_STOP",
    "abbruch": "MANUAL_STOP",
    "manueller_abbruch": "MANUAL_STOP",
    "manuell": "MANUAL_STOP",
}

# Keyword fallback, checked IN THIS ORDER (first hit wins). Order matters:
# "no fracture (run-out)" -> RUN_OUT; "Abbruch" contains "bruch" -> MANUAL_STOP before TOTAL_FRACTURE;
# "Anriss" -> CRACK_DETECTED before the fracture keywords.
TERMINATION_REASON_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("RUN_OUT", ("run_out", "runout", "durchlaufer", "durchlaeufer", "grenzschwingspiel", "limit_cycles")),
    ("MANUAL_STOP", ("manual", "manuell", "abbruch", "operator", "stopped", "aborted")),
    ("CRACK_DETECTED", ("crack", "riss")),
    ("TOTAL_FRACTURE", ("fracture", "bruch", "broken", "failure", "failed")),
)

RECORDING_MODE_SYNONYMS: dict[str, str] = {
    "full_signal": "FULL_SIGNAL",
    "full": "FULL_SIGNAL",
    "fullsignal": "FULL_SIGNAL",
    "continuous": "FULL_SIGNAL",
    "vollsignal": "FULL_SIGNAL",
    "volles_signal": "FULL_SIGNAL",
    "peak_counter": "PEAK_COUNTER",
    "peakcounter": "PEAK_COUNTER",
    "peak_count": "PEAK_COUNTER",
    "spitzenwertzahler": "PEAK_COUNTER",
    "spitzenwertzaehler": "PEAK_COUNTER",
    "peak_valley": "PEAK_VALLEY",
    "peakvalley": "PEAK_VALLEY",
    "min_max": "PEAK_VALLEY",
    "minmax": "PEAK_VALLEY",
}

TRUE_STRINGS = {"1", "true", "yes", "y", "ja", "j", "x", "on", "wahr", "active", "aktiv"}
FALSE_STRINGS = {"0", "false", "no", "n", "nein", "off", "falsch", "inactive", "inaktiv", "-"}


class RowError(ValueError):
    """A single CSV row could not be mapped; the row is skipped."""


# --------------------------------------------------------------------------------------------------------------------
# Value helpers (module level so they can be unit tested)
# --------------------------------------------------------------------------------------------------------------------
def _norm_key(text: str) -> str:
    """Lower case, umlauts/accents folded (ü -> u), every run of non-alphanumerics -> '_'."""
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", folded.lower()).strip("_")


def map_termination_reason(value: str) -> str:
    """Map a free-text termination reason to a FATIGUE.TERMINATION_REASON term code.

    Raises:
        RowError: if the text cannot be mapped unambiguously.
    """
    if value is None or not str(value).strip():
        raise RowError("termination_reason is empty")
    raw = str(value).strip()
    if raw.upper() in TERMINATION_REASON_TERMS:
        return raw.upper()
    key = _norm_key(raw)
    if key.upper() in TERMINATION_REASON_TERMS:
        return key.upper()
    if key in TERMINATION_REASON_SYNONYMS:
        return TERMINATION_REASON_SYNONYMS[key]
    for term, keywords in TERMINATION_REASON_KEYWORDS:
        if any(kw in key for kw in keywords):
            return term
    raise RowError(
        f"Unknown termination reason {raw!r}; expected one of {', '.join(TERMINATION_REASON_TERMS)} or a known synonym"
    )


def map_recording_mode(value: str) -> str:
    raw = str(value).strip()
    key = _norm_key(raw)
    if key.upper() in {"FULL_SIGNAL", "PEAK_COUNTER", "PEAK_VALLEY"}:
        return key.upper()
    if key in RECORDING_MODE_SYNONYMS:
        return RECORDING_MODE_SYNONYMS[key]
    raise RowError(f"Unknown recording mode {raw!r}; expected FULL_SIGNAL, PEAK_COUNTER or PEAK_VALLEY")


def parse_bool(value: str, column: str) -> bool:
    key = str(value).strip().lower()
    if key in TRUE_STRINGS:
        return True
    if key in FALSE_STRINGS:
        return False
    raise RowError(f"{column}: cannot interpret {value!r} as boolean")


def parse_int(value: str, column: str) -> int:
    """Parse cycle counts like '1234567', '1 234 567', "1'234'567", '1.234.567' (German grouping), '2.5e6', '2,0E6'."""
    text = str(value).strip().replace(" ", "").replace(" ", "").replace("'", "").replace("_", "")
    if re.fullmatch(r"[+-]?\d{1,3}([.,]\d{3})+", text):  # thousands grouping with . or ,
        text = re.sub(r"[.,]", "", text)
    text = text.replace(",", ".")
    try:
        number = float(text)
    except ValueError as exc:
        raise RowError(f"{column}: cannot interpret {value!r} as integer") from exc
    if number != int(number):
        raise RowError(f"{column}: {value!r} is not a whole number")
    return int(number)


def parse_frequency_hz(value: str, column: str) -> int:
    """'1200', '1200 Hz', '1.2 kHz' -> 1200."""
    text = str(value).strip().lower().replace(" ", "")
    factor = 1
    if text.endswith("khz"):
        factor, text = 1000, text[:-3]
    elif text.endswith("hz"):
        text = text[:-2]
    try:
        number = float(text.replace(",", ".")) * factor
    except ValueError as exc:
        raise RowError(f"{column}: cannot interpret {value!r} as frequency") from exc
    if abs(number - round(number)) > 1e-9:
        raise RowError(f"{column}: {value!r} is not a whole number of Hz")
    return int(round(number))


_DATETIME_FORMATS = (
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H:%M",
    "%d.%m.%Y",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
)


def parse_datetime(value: str, column: str) -> dt.datetime:
    """ISO 8601 ('2026-09-01T08:15:00', '2026-09-01 08:15') or German ('01.09.2026 08:15:00')."""
    text = str(value).strip()
    try:
        return dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in _DATETIME_FORMATS:
        try:
            return dt.datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise RowError(f"{column}: cannot interpret {value!r} as date/time")


def format_dms_drop_cycles(value: str, column: str = "dms_drop_cycles") -> str:
    """'DMS1:214000;DMS2:219500' -> 'DMS1: 214000\\nDMS2: 219500' (one strain gauge per line, counts validated)."""
    entries = [e.strip() for e in re.split(r"[;\n|]+", str(value)) if e.strip()]
    lines = []
    for entry in entries:
        match = re.fullmatch(r"([^:=]+?)\s*[:=]\s*(.+)", entry)
        if not match:
            raise RowError(f"{column}: entry {entry!r} is not '<gauge>:<cycles>'")
        gauge, cycles = match.group(1).strip(), match.group(2).strip()
        if _norm_key(cycles) in {"none", "n_a", "na", "no_drop", "kein_abfall"}:
            lines.append(f"{gauge}: no drop")
            continue
        lines.append(f"{gauge}: {parse_int(cycles, column)}")
    if not lines:
        raise RowError(f"{column}: no entries in {value!r}")
    return "\n".join(lines)


def next_step_for(termination_reason: str) -> str:
    """Run-outs have no fracture surface -> DONE; every other termination continues with step 12."""
    return NEXT_STEP_RUN_OUT if termination_reason == "RUN_OUT" else NEXT_STEP_AFTER_TEST


# --------------------------------------------------------------------------------------------------------------------
# CSV reading
# --------------------------------------------------------------------------------------------------------------------
def _read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def read_summary_csv(path: str | Path) -> list[dict[str, str]]:
    """Read the IMC summary CSV. Delimiter (',', ';' or tab) is detected from the header line.

    Returns rows keyed by the canonical column names of COLUMN_ALIASES (unknown columns are dropped).
    """
    text = _read_text(Path(path))
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        return []
    header = lines[0]
    delimiter = max((";", ",", "\t"), key=header.count)
    reader = csv.DictReader(lines, delimiter=delimiter)

    alias_to_canonical = {alias: canon for canon, aliases in COLUMN_ALIASES.items() for alias in aliases}
    field_map: dict[str, str] = {}
    for field in reader.fieldnames or []:
        canonical = alias_to_canonical.get(_norm_key(field or ""))
        if canonical and canonical not in field_map.values():
            field_map[field] = canonical
    if "specimen" not in field_map.values():
        raise ValueError(f"{path}: required column 'specimen' not found (header: {reader.fieldnames})")
    if "termination_reason" not in field_map.values():
        raise ValueError(f"{path}: required column 'termination_reason' not found (header: {reader.fieldnames})")

    rows = []
    for raw_row in reader:
        row = {canon: (raw_row.get(field) or "").strip() for field, canon in field_map.items()}
        if any(row.values()):
            rows.append(row)
    return rows


# --------------------------------------------------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------------------------------------------------
class CyclicFatigueTestParser(AbstractParser):
    """Steps 10 (cyclic fatigue test) and 11 (evaluation): update ``<specimen>-TEST`` and the specimen's NEXT_STEP.

    Args:
        bam_oe: BAM_OE term written to the specimen. Needed because ``CollectionType.add()`` enforces the mandatory
            properties of SAMPLE.WELDED_FATIGUE_SPECIMEN ($NAME, BAM_OE) also for objects that are only updated.
            A ``bam_oe`` CSV column overrides it per row. Without either, the specimen update is skipped (logged)
            and only the TEST object is updated.
        update_specimen: set to False to update only the TEST objects (e.g. on an instance where BAM_OE is not
            assigned to the specimen type yet).
        project / collection_by_prefix: optional per-object destination (``collection.add(..., destination=...)``),
            e.g. ``project="WELDED_FATIGUE", collection_by_prefix={"S1B": "SERIES_1_BUTT_WELD",
            "S1C": "SERIES_1_CRUCIFORM_WELD"}`` for a CSV with specimens of several series. Without it, the
            RunParsers default destination (its ``collection_name``) is used for all objects.
    """

    def __init__(
        self,
        bam_oe: str | None = None,
        update_specimen: bool = True,
        project: str | None = None,
        collection_by_prefix: dict[str, str] | None = None,
    ) -> None:
        if collection_by_prefix and not project:
            raise ValueError("`project` is required when `collection_by_prefix` is given")
        self.bam_oe = bam_oe
        self.update_specimen = update_specimen
        self.project = project
        self.collection_by_prefix = dict(collection_by_prefix or {})
        self.errors: list[str] = []

    # ---- helpers ----------------------------------------------------------------------------------------------
    def _destination(self, specimen_code: str) -> Destination | None:
        if not self.collection_by_prefix:
            return None
        for prefix in sorted(self.collection_by_prefix, key=len, reverse=True):
            if specimen_code.startswith(prefix.upper()):
                return Destination(project=self.project, collection=self.collection_by_prefix[prefix])
        raise RowError(f"No collection configured for specimen {specimen_code!r} (prefixes: {list(self.collection_by_prefix)})")

    def _build_test(self, row: dict[str, str], specimen_code: str, termination_reason: str) -> Any:
        test = CyclicFatigueTest(code=f"{specimen_code}{TEST_CODE_SUFFIX}")
        # Step 10
        test.termination_reason = termination_reason
        if row.get("beach_marks_active"):
            test.beach_marks_active = parse_bool(row["beach_marks_active"], "beach_marks_active")
        # Step 08 values that the IMC evaluation reports as well
        if row.get("sampling_frequency"):
            test.sampling_frequency = parse_frequency_hz(row["sampling_frequency"], "sampling_frequency")
        if row.get("recording_mode"):
            test.recording_mode = map_recording_mode(row["recording_mode"])
        # Step 11
        cycles_gross = parse_int(row["cycles_gross"], "cycles_gross") if row.get("cycles_gross") else None
        cycles_net = parse_int(row["cycles_net"], "cycles_net") if row.get("cycles_net") else None
        if cycles_gross is not None and cycles_net is not None and cycles_net > cycles_gross:
            raise RowError(f"cycles_net ({cycles_net}) > cycles_gross ({cycles_gross})")
        if cycles_gross is not None:
            test.cycles_gross = cycles_gross
        if cycles_net is not None:
            test.cycles_net = cycles_net
        if row.get("dms_drop_cycles"):
            test.cycles_to_10_percent_strain_gauge_drop = format_dms_drop_cycles(row["dms_drop_cycles"])
        # Inherited ExperimentalStep properties (design.md 3.2: START/END_DATE from the IMC data)
        start = parse_datetime(row["start"], "start") if row.get("start") else None
        end = parse_datetime(row["end"], "end") if row.get("end") else None
        if start and end and end < start:
            raise RowError(f"end ({end}) is before start ({start})")
        if start:
            test.start_date = start
        if end:
            test.end_date = end
        test.finished_flag = True
        return test

    # ---- AbstractParser API -----------------------------------------------------------------------------------
    def parse(
        self,
        files: list[str],
        collection: CollectionType,
        logger: BoundLoggerLazyProxy = default_logger,
    ) -> None:
        self.errors = []
        for file in files:
            path = Path(file)
            if path.suffix.lower() not in {".csv", ".txt"}:
                logger.warning(f"CyclicFatigueTestParser: skipping {file} (not a CSV summary)")
                continue
            rows = read_summary_csv(path)
            logger.info(f"CyclicFatigueTestParser: {len(rows)} row(s) in {path.name}")
            for line_no, row in enumerate(rows, start=2):
                self._parse_row(row, f"{path.name}:{line_no}", collection, logger)
        if self.errors:
            logger.error(f"CyclicFatigueTestParser: {len(self.errors)} row(s) skipped: {self.errors}")

    def _parse_row(self, row: dict[str, str], where: str, collection: CollectionType, logger) -> None:
        specimen_code = row.get("specimen", "").strip().upper()
        try:
            if not specimen_code:
                raise RowError("specimen is empty")
            if specimen_code.endswith(TEST_CODE_SUFFIX):  # tolerate 'S1B-01-TEST' in the specimen column
                specimen_code = specimen_code[: -len(TEST_CODE_SUFFIX)]
            termination_reason = map_termination_reason(row.get("termination_reason", ""))
            destination = self._destination(specimen_code)
            test = self._build_test(row, specimen_code, termination_reason)
        except (RowError, TypeError, ValueError) as exc:
            msg = f"{where} ({specimen_code or '?'}): {exc}"
            self.errors.append(msg)
            logger.error(f"CyclicFatigueTestParser: row skipped - {msg}")
            return

        test_id = collection.add(test, destination=destination)
        logger.info(f"CyclicFatigueTestParser: update {test.code} ({termination_reason}) -> {test_id}")

        if not self.update_specimen:
            return
        bam_oe = row.get("bam_oe") or self.bam_oe
        if not bam_oe:
            msg = f"{where} ({specimen_code}): FATIGUE.NEXT_STEP not set - no BAM_OE (parser arg or 'bam_oe' column)"
            self.errors.append(msg)
            logger.warning(f"CyclicFatigueTestParser: {msg}")
            return
        specimen = WeldedFatigueSpecimen(
            code=specimen_code,
            name=row.get("specimen_name") or specimen_code,  # $NAME = series designation (design.md 3.1)
            bam_oe=bam_oe,
            next_step=next_step_for(termination_reason),
        )
        specimen_id = collection.add(specimen, destination=destination)
        logger.info(f"CyclicFatigueTestParser: update {specimen_code} NEXT_STEP={specimen.next_step} -> {specimen_id}")
