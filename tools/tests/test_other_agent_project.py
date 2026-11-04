"""A project written by another agent (only project.yaml + design.json, no spec/structure yet) gets the same review page;
a design that breaks the format gets no page but a precise list of what to fix."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import check_files  # noqa: E402
import render_review as rr  # noqa: E402

YAML = """name: demo
title: Zugversuche an Klebverbindungen
title_en: Tensile tests on adhesive joints
division: FB 5.1
instance: https://playground.datastore.bam.de
space: FB_51
project: ADHESIVE_TENSILE
inventory_projects: ["/BAM_EQUIPMENT/FB51_EQUIPMENT_OPEN"]
bam_masterdata: v0.17.0
"""
DESIGN = {
    "object_types": [{"code": "SAMPLE.ADHESIVE_JOINT", "parent_class": "Sample", "name_de": "Klebprobe", "name_en": "Adhesive joint specimen",
                      "description": "Adhesive joint specimen//Klebprobe", "section_order": ["General Information", "Measurement Data"],
                      "properties": [{"code": "ADH.BOND_LENGTH", "data_type": "REAL", "property_label": "Bond length [mm]",
                                      "property_label_de": "Klebelänge [mm]", "description": "Overlap length//Überlappungslänge",
                                      "section": "Measurement Data", "mandatory": False, "reuse_property": None}]}],
    "vocabularies": [{"code": "ADH.FAILURE_MODE", "description": "Failure mode//Versagensart",
                      "terms": [{"code": "ADHESIVE", "label": "Adhesive failure", "label_de": "Adhäsionsbruch"},
                                {"code": "COHESIVE", "label": "Cohesive failure", "label_de": "Kohäsionsbruch"}]}],
    "section_names_de": {"Measurement Data": "Messdaten"},
    "layout": {"project": "/FB_51/ADHESIVE_TENSILE",
               "collections": [{"code": "SERIES_A", "$NAME": "Serie A / Series A"}],
               "per_specimen": [{"code_pattern": "A-01", "type": "SAMPLE.ADHESIVE_JOINT", "name_de": "Klebprobe", "name_en": "Specimen"},
                                {"code_pattern": "A-01-TEST", "type": "EXPERIMENTAL_STEP", "name_de": "Zugversuch", "name_en": "Tensile test",
                                 "parents": ["A-01 (specimen)", "Universal testing machine"]}],
               "series_table": [{"column": "Name//Name", "source": "specimen $NAME"}]},
    "step_location_map": [{"no": "01", "step": "Measure the bond", "step_de": "Klebung vermessen", "object": "specimen",
                           "section": "Measurement Data", "data_items": ["ADH.BOND_LENGTH"], "equipment": ["Caliper"], "files": ["Photo"]},
                          {"no": "02", "step": "Tensile test", "step_de": "Zugversuch", "object": "A-01-TEST", "section": "-",
                           "data_items": [], "equipment": ["Universal testing machine"], "files": []}],
    "dataset_mapping": [{"file": "Photo//Foto", "attach_to": "specimen"}],
    "variant": "A",
    "variants": [
        {"id": "A", "recommended": True, "shape": "flat", "name_de": "Probe mit Zugversuch", "name_en": "Specimen with tensile test",
         "summary_de": "Zugversuch als eigenes Objekt an der Probe.", "summary_en": "Tensile test as an object on the specimen.",
         "objects": [{"name_de": "Klebprobe", "name_en": "Specimen", "steps": ["01"]},
                     {"name_de": "Zugversuch", "name_en": "Tensile test", "steps": ["02"]}],
         "objects_per_specimen": 2, "max_link_depth": 1, "new_object_types": 1,
         "pros": [{"de": "Prüfmaschine hängt am Versuch", "en": "Testing machine hangs on the test"}],
         "cons": [{"de": "Zwei Objekte je Probe", "en": "Two objects per specimen"}]},
        {"id": "B", "shape": "single", "name_de": "Alles an der Probe", "name_en": "Everything on the specimen",
         "summary_de": "Nur die Probe.", "summary_en": "Only the specimen.",
         "objects": [{"name_de": "Klebprobe", "name_en": "Specimen", "steps": ["01", "02"]}],
         "pros": [{"de": "Ein Objekt", "en": "One object"}], "cons": [{"de": "Gerät ohne Schritt", "en": "Instrument without a step"}]}],
}


def make_repo(tmp: Path, design: dict) -> Path:
    (tmp / "generated").mkdir(parents=True)
    shutil.copy(ROOT / "generated" / "catalog.json", tmp / "generated" / "catalog.json")
    shutil.copytree(ROOT / "schemas", tmp / "schemas")
    pdir = tmp / "projects" / "demo"
    pdir.mkdir(parents=True)
    (pdir / "project.yaml").write_text(YAML, encoding="utf-8")
    (pdir / "design.json").write_text(json.dumps(design), encoding="utf-8")
    return tmp


def test_other_agents_design_renders(tmp_path):
    repo = make_repo(tmp_path, DESIGN)
    assert check_files.check_project(repo, "demo")[0] == []
    out = tmp_path / "s.html"
    assert rr.main(["demo", "struktur", "--repo", str(repo), "--out", str(out)]) == 0
    html = out.read_text(encoding="utf-8")
    for part in ("Klebprobe", "Adhesive joint specimen", "Klebelänge [mm]", "Messdaten", "Klebung vermessen",
                 "Adhäsionsbruch", "Beispielzeilen folgen", "Name",  # "Name" comes from the parent type in the catalog
                 "Zugversuche an Klebverbindungen", "Tensile tests on adhesive joints", "FB 5.1",  # heading from project.yaml
                 "Alles an der Probe / Everything on the specimen", "(empfohlen)", "(recommended)", 'data-shown="A"'):
        assert part in html, part
    assert "FB 7.2" not in html and "Wöhler" not in html  # nothing from the reference project leaks into another one
    assert html.count('name="variant"') == 2 and html.count(" checked") == 1


def test_process_line_is_drawn_as_a_line(tmp_path):
    design = json.loads(json.dumps(DESIGN))
    per = design["layout"]["per_specimen"]
    per.append({"code_pattern": "A-01-FRACTURE", "type": "EXPERIMENTAL_STEP", "name_de": "Bruchbild", "name_en": "Fracture image",
                "parents": ["A-01-TEST (step)"], "links": ["Microscope"]})
    repo = make_repo(tmp_path, design)
    out = tmp_path / "s.html"
    assert rr.main(["demo", "struktur", "--repo", str(repo), "--out", str(out)]) == 0
    html = out.read_text(encoding="utf-8")
    assert 'class="line"' in html and "als Linie" in html  # specimen -> test -> fracture, not a star
    assert "dev field" in html and "als Feld verlinkt" in html  # instrument linked by an OBJECT field (pattern M4)
    assert "A-01-TEST (step)" not in html  # the previous step is not listed as an instrument


def test_variants_are_required_with_one_recommendation(tmp_path):
    for change, needle in ((lambda d: d.pop("variants"), "variants fehlt"),
                           (lambda d: d["variants"][1].update(recommended=True), "genau eine Variante"),
                           (lambda d: d["variants"][0].pop("recommended"), "genau eine Variante"),
                           (lambda d: d.update(variant="Z"), "keine der Varianten"),
                           (lambda d: d["variants"].pop(), "variants")):
        design = json.loads(json.dumps(DESIGN))
        change(design)
        repo = make_repo(tmp_path / needle.replace(" ", "_") / str(id(change)), design)
        errors = check_files.check_project(repo, "demo")[0]
        assert any(needle in e for e in errors), (needle, errors)


def test_broken_design_gets_no_page_but_a_list(tmp_path, capsys):
    broken = json.loads(json.dumps(DESIGN))
    del broken["step_location_map"][0]["step_de"]
    broken["object_types"][0]["properties"][0].pop("property_label_de")
    broken["object_types"][0]["properties"][0]["section"] = "02 measurement data"
    repo = make_repo(tmp_path, broken)
    out = tmp_path / "s.html"
    assert rr.main(["demo", "struktur", "--repo", str(repo), "--out", str(out)]) == 1
    assert not out.exists()
    msg = capsys.readouterr().out
    assert "step_location_map/0" in msg and "step_de" in msg
    assert "property_label_de" in msg and "02 measurement data" in msg
