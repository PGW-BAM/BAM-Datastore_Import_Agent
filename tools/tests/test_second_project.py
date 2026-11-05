"""A second, completely different project (fictitious synthesis of silver nanoparticles, tools/tests/fixtures/synthese)
goes through the whole chain with the same tools as FB 7.2: file check, review pages A, B, C/D, E (HTML + Markdown),
request package, dry run against a fake openBIS. Nothing from the FB 7.2 reference may leak into its pages.

If this test breaks after a change to the tools, the change was probably specific to one project.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parent / "fixtures" / "synthese"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bruecke  # noqa: E402
import build_request  # noqa: E402
import check_files  # noqa: E402
import openbis_bridge as ob  # noqa: E402
import render_review as rr  # noqa: E402
from test_openbis_bridge import FakeOpenBIS  # noqa: E402

NAME = "synthese"
# fixed wording that used to come from FB 7.2 ("Probe" alone may appear: standard fields like SAMPLE_ID_NUMBER say "Probennummer")
LEAKS = ("FB 7.2", "FB_72", "Wöhler", "Schweiß", "welded", "Herkunftsblech", "Demo-Serie", "FATIGUE",
         "je Probe", "jede Probe", "der Probe", "die Probe", "per specimen", "the specimen", "Versuchsablauf")


def make_repo(tmp: Path) -> Path:
    (tmp / "generated").mkdir(parents=True)
    shutil.copy(ROOT / "generated" / "catalog.json", tmp / "generated" / "catalog.json")
    shutil.copytree(ROOT / "schemas", tmp / "schemas")
    shutil.copytree(FIX, tmp / "projects" / NAME, ignore=shutil.ignore_patterns("__pycache__"))
    return tmp


def fake_instance(repo: Path) -> FakeOpenBIS:
    """An instance that already has the requested types (as after the admin's import) and the inventory objects."""
    spec = json.loads((repo / "projects" / NAME / "spec.json").read_text(encoding="utf-8"))
    catalog = json.loads((repo / "generated" / "catalog.json").read_text(encoding="utf-8"))
    types = {t["code"]: [(p["code"], bool(p.get("mandatory")), p.get("section"), p.get("data_type") or "VARCHAR")
                         for p in t["properties"]] for t in spec["object_types"]}
    for t in catalog["types"]:
        if t["code"] in ("EXPERIMENTAL_STEP.DLS", "EXPERIMENTAL_STEP.TEM", "GENERAL_PROTOCOL"):
            types[t["code"]] = [(p["code"], bool(p.get("mandatory")), p.get("section"), p.get("data_type") or "VARCHAR")
                                for p in t.get("inherited_properties", []) + t["properties"]]
    inv = "/BAM_EQUIPMENT/TEST_EQUIPMENT_OPEN"
    items = ["AGNO3_01", "NA3CITRATE_01", "BALANCE_01", "HEATING_STIRRER_01", "CENTRIFUGE_01", "DLS_01", "TEM_01"]
    vocab = {v["code"]: [x["code"] for x in v["terms"]] for v in spec["vocabularies"]}
    vocab["BAM_OE"] = ["TEST_OE"]  # organisational units come from the instance
    return FakeOpenBIS(types, vocab, projects=[inv], samples=[f"{inv}/{i}" for i in items])


def page(repo: Path, view: str, tmp: Path) -> tuple[str, str]:
    out = tmp / f"{view}.html"
    assert rr.main([NAME, view, "--repo", str(repo), "--out", str(out)]) == 0, view
    return out.read_text(encoding="utf-8"), out.with_suffix(".md").read_text(encoding="utf-8")


def visible(html: str) -> str:
    """Page text without CSS/JS (class names like .probe are not shown to anyone)."""
    html = re.sub(r"(?s)<(style|script)>.*?</\1>", "", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def test_files_pass_the_format_check(tmp_path):
    repo = make_repo(tmp_path)
    errors, _ = check_files.check_project(repo, NAME)
    assert errors == []
    assert ob.validate_structure(json.loads((repo / "projects" / NAME / "structure.json").read_text())) == []


def test_page_a_from_the_prd(tmp_path):
    repo = make_repo(tmp_path / "r")
    html, md = page(repo, "prd", tmp_path)
    assert html.count('class="step test"') == 5 and "Synthese von Silber-Nanopartikeln" in html and "FB 0.0" in html
    assert "Silbernitrat / Silver nitrate" in html
    for leak in LEAKS:
        assert leak not in visible(html), leak


def test_page_b_names_the_main_object_and_draws_pattern_m3(tmp_path):
    repo = make_repo(tmp_path / "r")
    html, md = page(repo, "struktur", tmp_path)
    text = visible(html)
    for part in ("Objekte je Charge", "jedes Objekt „Charge“", "je Charge", "daraus entsteht", "(empfohlen)",
                 "Charge aus der Synthese, Messungen an der Charge", "Zieldurchmesser [nm] / Target diameter [nm]",
                 "Verweis auf Zentrifuge", "Kugel / Sphere"):
        assert part in text, part
    # the synthesis is drawn above the batch, DLS and TEM below it
    a = html.index('aria-labelledby="h1s"')
    build_up = visible(html[a:html.index("</section>", a)])
    assert build_up.index("Synthese / Synthesis") < build_up.index("Hauptobjekt: trägt") < build_up.index("DLS-Messung / DLS measurement")
    assert "Zentrifuge / Centrifuge" in build_up  # link field of the main object itself
    # series table: values of the batch and of the DLS step (source "DLS DLS.ZAVG")
    table = html[html.index("<table"):html.index("</table>")]
    assert "78.5" in table and "17.6" in table and "Kugel / Sphere" in table
    assert "B freigegeben" in md and "(empfohlen / recommended)" in md and "Objekte je Charge" in md
    for leak in LEAKS:
        assert leak not in text and leak not in md, leak


def test_request_and_page_cd(tmp_path):
    repo = make_repo(tmp_path / "r")
    assert build_request.main([NAME, "--repo", str(repo), "--ohne-werkzeuge"]) == 0
    r = json.loads((repo / "projects" / NAME / "request" / "request.json").read_text(encoding="utf-8"))
    assert {t["code"] for t in r["new_types"]} == {"SAMPLE.NANOPARTICLE_BATCH", "EXPERIMENTAL_STEP.NANOPARTICLE_SYNTHESIS"}
    assert "INSTRUMENT" not in {p["code"] for p in r["new_properties"]}  # reused standard link field
    assert r["division"] == "FB 0.0"
    html, md = page(repo, "antrag", tmp_path)
    assert "Nanopartikel-Charge / Nanoparticle batch" in visible(html) and "FB 0.0" in html
    for leak in LEAKS:
        assert leak not in visible(html), leak


def test_dry_run_and_page_e(tmp_path):
    repo = make_repo(tmp_path / "r")
    prj = ob.load_project(repo, NAME)
    html, _ = page(repo, "trockenlauf", tmp_path)
    assert "Noch kein Trockenlauf" in html  # no approval before the person has run the dry run

    assert bruecke.run(prj, "trockenlauf", fake_instance(repo)) == 0
    check = json.loads(sorted((prj["dir"] / "reports").glob("check_*.json"))[-1].read_text())
    assert check["missing"] == [], check["missing"]
    html, md = page(repo, "trockenlauf", tmp_path)
    assert "data-block-de" not in html and "wird angelegt" in html and "E freigegeben" in md
    assert "Links: " in html and "/BAM_EQUIPMENT/TEST_EQUIPMENT_OPEN/CENTRIFUGE_01" in html

    f = fake_instance(repo)  # create for real on the fake: link fields carry identifiers, synthesis before batch
    assert bruecke.run(prj, "anlegen", f, yes=True) == 0
    batch = f.samples["/TEST_SPACE/AG_NANO/AG-01"]
    assert batch["props"]["NANO.CENTRIFUGE"] == "/BAM_EQUIPMENT/TEST_EQUIPMENT_OPEN/CENTRIFUGE_01"
    assert f.samples["/TEST_SPACE/AG_NANO/AG-01-SYN"]["props"]["INSTRUMENT"].endswith("HEATING_STIRRER_01")
