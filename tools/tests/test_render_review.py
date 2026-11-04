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
                 "Stumpfstoß", "Text kopieren", 'data-item="aufbau"', "FB 7.2", "S-N tests on welded joints",
                 "Kette wie bisher auf dev1", "(empfohlen)"):
        assert part in html, part
    assert "<title>Strukturvorschlag · Wöhlerversuche an Schweißverbindungen</title>" in html
    assert html.count('class="fb"') == 7  # build-up, steps, 2 forms, table, lists, terms


def test_fragment_has_no_document_wrapper(tmp_path):
    out = tmp_path / "f.html"
    rr.main(["fb72_welded_fatigue", "struktur", "--fragment", "--out", str(out)])
    html = out.read_text(encoding="utf-8")
    assert html.startswith("<title>") and "<html" not in html and "<body" not in html


def test_every_new_name_is_bilingual():
    m = rr.Model(ROOT, "fb72_welded_fatigue")
    html = rr.view_struktur(m)
    assert m.missing == set(), f"names without German: {sorted(m.missing)}"
    for pair in ("Geschweißte Ermüdungsprobe", "Welded fatigue specimen", "Herkunftsblech", "Source sheet",
                 "Probenidentifikation", "Specimen Identification", "Hoch", "High"):
        assert pair in html, pair
    assert "nur EN" in html  # standard fields without German are shown, not flagged as gaps


def test_new_properties_carry_property_label_de():
    import json
    spec = json.loads((ROOT / "generated" / "welded_fatigue_v2" / "spec.json").read_text(encoding="utf-8"))
    m = rr.Model(ROOT, "fb72_welded_fatigue")
    for t in spec["object_types"]:
        for p in t["properties"]:
            if p["code"] in m.new_codes:
                assert p.get("label_de"), p["code"]
