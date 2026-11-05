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


def test_prd_page_a_and_markdown_versions(tmp_path):
    out = tmp_path / "prd.html"
    assert rr.main(["fb72_welded_fatigue", "prd", "--out", str(out)]) == 0
    html = out.read_text(encoding="utf-8")
    for part in ("Prüfpunkt A", 'data-gate="A"', "Vorqualitätsprüfung der Schweißnaht", "ZEISS GOM ATOS 5",
                 "Hinweise des Agenten", "WELDING.WELD_TYPE"):
        assert part in html, part
    assert html.count('class="step test"') == 12  # the workflow table becomes 12 step cards
    for view in ("prd", "struktur", "antrag", "trockenlauf"):
        o = tmp_path / f"{view}.html"
        assert rr.main(["fb72_welded_fatigue", view, "--out", str(o)]) == 0
        md = o.with_suffix(".md").read_text(encoding="utf-8")
        assert md.startswith("# Wöhlerversuche an Schweißverbindungen / S-N tests on welded joints"), view
        assert "<" not in md.split("\n")[0] and "freigegeben" in md
    assert "(empfohlen / recommended)" in (tmp_path / "struktur.md").read_text(encoding="utf-8")


def test_markdown_reader():
    blocks = rr.md_blocks("Text **fett**\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n- x\n- y\n\n1. eins\n   weiter\n")
    assert [b[0] for b in blocks] == ["p", "table", "ul", "ol"]
    assert blocks[1][2] == [["1", "2"]] and blocks[3][1] == ["eins weiter"]
    assert rr.split_top("a, b (x, y), –") == ["a", "b (x, y)"]
