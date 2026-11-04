"""The review page for checkpoint B renders from the FB 7.2 example files (offline)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import render_review as rr  # noqa: E402


def test_struktur_page_renders_fb72(tmp_path):
    out = tmp_path / "struktur.html"
    assert rr.main(["fb72_welded_fatigue", "struktur", "--out", str(out)]) == 0
    html = out.read_text(encoding="utf-8")
    assert html.startswith("<!doctype html>") and "</html>" in html
    for part in ("Prüfpunkt B", "SAMPLE.WELDED_FATIGUE_SPECIMEN", "Strain Gauge Application", "Serientabelle",
                 "Stumpfstoß", "Text kopieren", 'data-item="aufbau"'):
        assert part in html, part
    assert html.count('class="fb"') == 6  # one answer per part: build-up, steps, 2 forms, table, lists


def test_fragment_has_no_document_wrapper(tmp_path):
    out = tmp_path / "f.html"
    rr.main(["fb72_welded_fatigue", "struktur", "--fragment", "--out", str(out)])
    html = out.read_text(encoding="utf-8")
    assert html.startswith("<title>") and "<html" not in html and "<body" not in html
