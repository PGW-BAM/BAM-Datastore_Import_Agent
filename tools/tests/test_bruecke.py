"""Offline tests for tools/bruecke.py (the one-command bridge): actions against the fake openBIS, git round trip.

Run: python -m pytest tools/tests -q
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bruecke  # noqa: E402
import openbis_bridge as ob  # noqa: E402
from test_openbis_bridge import EQUIP, fake, structure  # noqa: E402

YAML = f"""name: demo
instance: https://playground.example.de
space: FB_72
project: TEST_PROJECT
inventory_projects:
  - {EQUIP}
"""


def make_project(repo: Path) -> dict:
    pdir = repo / "projects" / "demo"
    pdir.mkdir(parents=True)
    (pdir / "project.yaml").write_text(YAML)
    s = structure()
    s["objects"][0]["props"].pop("UNKNOWN")
    (pdir / "structure.json").write_text(json.dumps(s))
    (pdir / "notes.txt").write_text("hello")
    return ob.load_project(repo, "demo")


def test_load_project(tmp_path):
    p = make_project(tmp_path)
    assert p["inventory"].name == "inventory_playground.json"
    assert p["read_projects"] == ["/FB_72/TEST_PROJECT", EQUIP]


def test_lesen_pruefen_trockenlauf_write_files_but_create_nothing(tmp_path):
    p = make_project(tmp_path)
    for action, code in (("lesen", 0), ("pruefen", 0), ("trockenlauf", 0)):
        f = fake()
        assert bruecke.run(p, action, f) == code
        assert not [c for c in f.calls if c.startswith("create")]
    assert p["inventory"].exists() and (p["dir"] / "delivery_check.md").exists()
    assert list((p["dir"] / "reports").glob("dryrun_*.json"))


def test_anlegen_asks_and_refuses_on_gaps(tmp_path):
    p = make_project(tmp_path)
    f = fake()
    assert bruecke.run(p, "anlegen", f, ask=lambda _: "nein") == 1
    assert "createSamples" not in f.calls
    assert bruecke.run(p, "anlegen", f, ask=lambda _: "ja") == 0
    assert "/FB_72/TEST_PROJECT/S1-01-TEST" in f.samples
    assert list((p["dir"] / "reports").glob("apply_*.json"))

    s = json.loads(p["structure"].read_text())  # a property the instance does not know -> gap
    s["objects"][1]["props"]["MISSING_PROP"] = "x"
    p["structure"].write_text(json.dumps(s))
    f2 = fake()
    assert bruecke.run(p, "anlegen", f2, yes=True) == 2
    assert "createSamples" not in f2.calls


def test_git_round_trip_pushes_only_project_files(tmp_path, monkeypatch):
    remote, work = tmp_path / "remote.git", tmp_path / "work"
    run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True)  # noqa: E731
    run("git", "init", "-q", "--bare", "-b", "main", str(remote))
    run("git", "clone", "-q", str(remote), str(work))
    for k, v in (("user.email", "t@example.org"), ("user.name", "Test")):
        run("git", "config", k, v, cwd=work)
    make_project(work)
    (work / "other.txt").write_text("not part of the project")
    run("git", "add", "projects", cwd=work)
    run("git", "commit", "-q", "-m", "init", cwd=work)
    run("git", "push", "-q", "-u", "origin", "main", cwd=work)

    monkeypatch.setattr(bruecke, "login", lambda instance: (type("O", (), {"logout": lambda self: None})(), fake()))
    assert bruecke.main(["demo", "pruefen", "--repo", str(work)]) == 0
    log = run("git", "--git-dir", str(remote), "log", "--name-only", "--format=%s", "-1").stdout
    assert log.startswith("demo: pruefen")
    assert "projects/demo/inventory_playground.json" in log and "delivery_check.md" in log
    assert "other.txt" not in log


def test_zweig_switches_branch_and_pushes_there(tmp_path, monkeypatch):
    remote, seed, work = tmp_path / "remote.git", tmp_path / "seed", tmp_path / "work"
    run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True)  # noqa: E731
    run("git", "init", "-q", "--bare", "-b", "main", str(remote))
    run("git", "clone", "-q", str(remote), str(seed))
    for k, v in (("user.email", "t@example.org"), ("user.name", "Test")):
        run("git", "config", k, v, cwd=seed)
    (seed / "README").write_text("main")
    run("git", "add", "README", cwd=seed)
    run("git", "commit", "-q", "-m", "main", cwd=seed)
    run("git", "push", "-q", "origin", "main", cwd=seed)
    run("git", "checkout", "-q", "-b", "agent/work", cwd=seed)  # the agent's branch holds the project
    make_project(seed)
    run("git", "add", "projects", cwd=seed)
    run("git", "commit", "-q", "-m", "project", cwd=seed)
    run("git", "push", "-q", "origin", "agent/work", cwd=seed)

    run("git", "clone", "-q", str(remote), str(work))  # the person's clone, on main, without the project
    for k, v in (("user.email", "t@example.org"), ("user.name", "Test")):
        run("git", "config", k, v, cwd=work)
    monkeypatch.setattr(bruecke, "login", lambda instance: (type("O", (), {"logout": lambda self: None})(), fake()))
    assert bruecke.main(["demo", "lesen", "--zweig", "agent/work", "--repo", str(work)]) == 0
    log = run("git", "--git-dir", str(remote), "log", "agent/work", "--format=%s", "-1").stdout
    assert log.startswith("demo: lesen")
    assert run("git", "--git-dir", str(remote), "log", "main", "--format=%s", "-1").stdout.strip() == "main"


def test_dry_run_feeds_review_page_e(tmp_path):
    import render_review as rr
    p = make_project(tmp_path)
    (p["dir"] / "project.yaml").write_text(YAML + 'title: Testablauf\ntitle_en: Test workflow\ndivision: FB 0.0\n'
                                           'summary_en: test\nbam_masterdata: v0.17.0\n')
    s = json.loads(p["structure"].read_text())
    for c in s["collections"]:
        c.setdefault("props", {})["$NAME"] = "Serie 1 / Series 1"  # names in both languages (schemas/structure)
    p["structure"].write_text(json.dumps(s))
    page = tmp_path / "e.html"
    assert rr.main(["demo", "trockenlauf", "--repo", str(tmp_path), "--out", str(page)]) == 0
    before = page.read_text(encoding="utf-8")
    assert "Noch kein Trockenlauf" in before and 'data-block-de="Noch kein Trockenlauf' in before  # no approval possible yet

    assert bruecke.run(p, "trockenlauf", fake()) == 0
    assert list((p["dir"] / "reports").glob("check_*.json")) and list((p["dir"] / "reports").glob("dryrun_*.json"))
    assert rr.main(["demo", "trockenlauf", "--repo", str(tmp_path), "--out", str(page)]) == 0
    html = page.read_text(encoding="utf-8")
    assert "Noch kein Trockenlauf" not in html and "data-block-de" not in html  # check is clean -> E can be approved
    assert "wird angelegt" in html and "S1-01-TEST" in html and "FB 0.0" in html
    md = page.with_suffix(".md").read_text(encoding="utf-8")
    assert "E freigegeben" in md and "| Objekt | Typ |" in md
