"""Offline tests for tools/openbis_bridge.py against a small fake openBIS (V3 JSON shapes incl. @id refs).

Run: python -m pytest tools/tests -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import openbis_bridge as ob  # noqa: E402


class FakeOpenBIS:
    """Just enough of the openBIS 20.10 V3 JSON API for the bridge."""

    def __init__(self, types, vocabularies=None, projects=(), experiments=(), samples=()):
        self.types = types  # code -> [(prop_code, mandatory, section, dataType)]
        self.vocabularies = vocabularies or {}  # code -> [terms]
        self.projects = {p.upper() for p in projects}
        self.experiments = {e.upper(): "COLLECTION" for e in experiments}
        self.samples = {s.upper(): {"type": "INSTRUMENT", "props": {"$NAME": s.split("/")[-1]}} for s in samples}
        self.calls = []

    # property types are shared between types -> second use is sent as a number, like the real server
    def _types(self):
        seen, nid, objs = {}, [1], []

        def pt(code, dt):
            if code in seen:
                return seen[code]
            seen[code] = nid[0]
            nid[0] += 1
            return {"@id": seen[code], "code": code, "dataType": dt}

        for code, props in self.types.items():
            objs.append({"code": code, "description": None, "propertyAssignments": [
                {"propertyType": pt(p, dt), "mandatory": m, "section": s, "ordinal": i}
                for i, (p, m, s, dt) in enumerate(props)]})
        return {"objects": objs}

    def __call__(self, method, *params):
        self.calls.append(method)
        if method == "searchVocabularies":
            return {"objects": [{"code": c, "terms": [{"code": t} for t in ts]} for c, ts in self.vocabularies.items()]}
        if method == "searchPropertyTypes":
            codes = sorted({p for props in self.types.values() for p, *_ in props})
            return {"objects": [{"code": c, "label": c, "dataType": "VARCHAR",
                                 "vocabulary": {"code": "LEVEL"} if c == "LEVEL_PROP" else None} for c in codes]}
        if method in ("searchSampleTypes",):
            return self._types()
        if method == "searchExperimentTypes":
            return {"objects": [{"code": "COLLECTION", "propertyAssignments": []}]}
        if method == "searchDataSetTypes":
            return {"objects": []}
        if method == "searchProjects":
            return {"objects": [{"identifier": {"identifier": p}} for p in sorted(self.projects)]}
        if method == "getServerInformation":
            return {"openbis-version": "20.10.12.5"}
        if method == "getProjects":
            ids = [i["identifier"].upper() for i in params[0]]
            fo = params[1]
            out = {}
            for p in ids:
                if p not in self.projects:
                    continue
                d = {"identifier": {"identifier": p}}
                if "experiments" in fo:
                    d["experiments"] = [{"identifier": {"identifier": e}, "type": {"code": t}}
                                        for e, t in self.experiments.items() if e.startswith(p + "/")]
                if "samples" in fo:
                    d["samples"] = [{"identifier": {"identifier": s}, "code": s.split("/")[-1],
                                     "type": {"code": v["type"]}, "properties": v["props"], "experiment": None}
                                    for s, v in self.samples.items() if s.startswith(p + "/")]
                out[p] = d
            return out
        if method == "getExperiments":
            return {i["identifier"].upper(): {} for i in params[0] if i["identifier"].upper() in self.experiments}
        if method == "getSamples":
            return {i["identifier"].upper(): {} for i in params[0] if i["identifier"].upper() in self.samples}
        if method == "createProjects":
            for c in params[0]:
                self.projects.add(f"/{c['spaceId']['permId']}/{c['code']}".upper())
            return [{}]
        if method == "createExperiments":
            for c in params[0]:
                self.experiments[f"{c['projectId']['identifier']}/{c['code']}".upper()] = c["typeId"]["permId"]
            return [{}]
        if method == "createSamples":
            for c in params[0]:
                for p in c.get("parentIds", []):  # parents must exist before the child
                    assert p["identifier"].upper() in self.samples, f"parent {p['identifier']} missing"
                self.samples[f"{c['projectId']['identifier']}/{c['code']}".upper()] = {
                    "type": c["typeId"]["permId"], "props": c["properties"]}
            return [{}]
        raise AssertionError(f"unexpected call {method}")


TYPES = {
    "SAMPLE.SPEC": [("$NAME", True, "General Information", "VARCHAR"), ("LEVEL_PROP", False, "Test", "CONTROLLEDVOCABULARY")],
    "EXPERIMENTAL_STEP": [("$NAME", True, "General Information", "VARCHAR"), ("NOTES", False, "Comments", "MULTILINE_VARCHAR")],
    "INSTRUMENT": [("$NAME", True, "General Information", "VARCHAR")],
}
EQUIP = "/BAM_EQUIPMENT/FB72_EQUIPMENT_OPEN"


def structure():
    return {
        "space": "FB_72", "project": {"code": "TEST_PROJECT", "description": "test"},
        "collections": [{"code": "SERIES_1", "type": "COLLECTION", "props": {"$NAME": "Series 1"}}],
        "objects": [
            {"key": "STEP", "code": "S1-01-TEST", "type": "EXPERIMENTAL_STEP", "collection": "SERIES_1",
             "props": {"$NAME": "test", "NOTES": "@file:notes.txt", "UNKNOWN": "x"},
             "parents": ["S1-01", f"{EQUIP}/GOM"]},
            {"key": "S1-01", "code": "S1-01", "type": "SAMPLE.SPEC", "collection": "SERIES_1",
             "props": {"$NAME": "S1-01", "LEVEL_PROP": "HIGH"}},
        ],
    }


def fake(**kw):
    return FakeOpenBIS(TYPES, {"LEVEL": ["HIGH", "LOW"]}, projects=[EQUIP], samples=[f"{EQUIP}/GOM"], **kw)


def test_read_inventory_resolves_refs_and_lists_projects():
    f = fake()
    inv = ob.read_inventory(f, "https://playground.example", [EQUIP])
    spec = next(t for t in inv["objectTypes"] if t["code"] == "EXPERIMENTAL_STEP")
    assert [p["code"] for p in spec["properties"]] == ["$NAME", "NOTES"]  # $NAME came as a number ref
    assert inv["objects"] == [{"identifier": f"{EQUIP}/GOM", "code": "GOM", "type": "INSTRUMENT",
                               "collection": None, "name": "GOM"}]
    assert inv["vocabularies"][0] == {"code": "LEVEL", "description": None, "terms": ["HIGH", "LOW"]}
    assert inv["read_projects"] == [EQUIP]
    assert f.calls and not any(m.startswith("create") for m in f.calls)  # read-only


def test_check_ready_and_missing():
    inv = ob.read_inventory(fake(), "x", [EQUIP])
    s = structure()
    s["objects"][0]["props"].pop("UNKNOWN")
    assert ob.check(inv, structure=s)["ready"] is True

    s = structure()  # UNKNOWN prop, missing equipment, unknown term, missing mandatory $NAME
    s["objects"][0]["parents"].append(f"{EQUIP}/MISSING_DEVICE")
    s["objects"][1]["props"] = {"LEVEL_PROP": "MEDIUM"}
    rep = ob.check(inv, structure=s)
    kinds = {(m["kind"], m["who"]) for m in rep["missing"]}
    assert ("assignment", "admin") in kinds
    assert ("equipment", "you") in kinds
    assert ("term", "admin") in kinds
    assert ("mandatory field", "agent") in kinds
    assert rep["ready"] is False
    assert "noch nicht bereit" in ob.render_check_md(rep)


def test_check_spec_against_inventory():
    inv = ob.read_inventory(fake(), "x", [])
    spec = {"vocabularies": [{"code": "LEVEL", "terms": [{"code": "HIGH"}, {"code": "MEDIUM"}]}],
            "extensions": [], "object_types": [
                {"code": "SAMPLE.SPEC", "properties": [{"code": "$NAME", "mandatory": True, "section": "General Information"},
                                                       {"code": "NOTES", "mandatory": False, "section": "Comments"}]},
                {"code": "SAMPLE.NEW", "properties": []}]}
    what = {(m["kind"], m["what"]) for m in ob.check(inv, spec=spec)["missing"]}
    assert what == {("term", "LEVEL: MEDIUM"), ("assignment", "SAMPLE.SPEC: NOTES"), ("object type", "SAMPLE.NEW")}


def test_apply_dry_run_creates_nothing(tmp_path):
    (tmp_path / "notes.txt").write_text("hello\n")
    f = fake()
    rep = ob.apply(f, structure(), tmp_path, dry_run=True)
    assert rep["created"] == ["/FB_72/TEST_PROJECT", "/FB_72/TEST_PROJECT/SERIES_1",
                              "/FB_72/TEST_PROJECT/S1-01", "/FB_72/TEST_PROJECT/S1-01-TEST"]
    assert not [c for c in f.calls if c.startswith("create")]
    assert rep["droppedProps"] == ["S1-01-TEST: UNKNOWN"]


def test_apply_creates_parents_first_and_is_idempotent(tmp_path):
    (tmp_path / "notes.txt").write_text("hello\n")
    f = fake()
    ob.apply(f, structure(), tmp_path, dry_run=False)
    step = f.samples["/FB_72/TEST_PROJECT/S1-01-TEST"]
    assert step["props"] == {"$NAME": "test", "NOTES": "hello"}  # @file read, UNKNOWN dropped
    again = ob.apply(f, structure(), tmp_path, dry_run=False)
    assert again["created"] == []
    assert len(again["skipped"]) == 4


def test_validate_structure_errors():
    s = structure()
    s["objects"][0]["parents"] = ["NOPE"]
    s["objects"][1]["collection"] = "OTHER"
    errs = ob.validate_structure(s)
    assert any("parent 'NOPE'" in e for e in errs)
    assert any("collection 'OTHER'" in e for e in errs)
    s = structure()
    s["objects"][1]["parents"] = ["STEP"]  # STEP -> S1-01 -> STEP
    assert any("cycle" in e for e in ob.validate_structure(s))


def test_fb72_example_structure_dry_run():
    path = ROOT / "generated" / "welded_fatigue_v2" / "structure.json"
    s = json.loads(path.read_text(encoding="utf-8"))
    assert ob.validate_structure(s) == []
    types = {o["type"]: [("$NAME", True, "General Information", "VARCHAR")] for o in s["objects"]}
    rep = ob.apply(FakeOpenBIS(types), s, path.parent, dry_run=True)
    assert len(rep["created"]) == 1 + len(s["collections"]) + len(s["objects"])


def test_template_structure_is_valid():
    s = json.loads((ROOT / "templates" / "structure.example.json").read_text(encoding="utf-8"))
    assert ob.validate_structure(s) == []


def test_notebook_matches_its_generator(tmp_path):
    import subprocess

    out = tmp_path / "nb.ipynb"
    subprocess.run([sys.executable, str(ROOT / "tools" / "make_bridge_notebook.py"), str(out)], check=True)
    assert out.read_bytes() == (ROOT / "notebooks" / "openbis_bruecke.ipynb").read_bytes(), \
        "notebook edited by hand? change tools/make_bridge_notebook.py and regenerate"
