"""Projektdateien gegen die Formate in schemas/ prüfen. Gleiche Prüfung für jeden Agenten.

  python tools/check_files.py <projekt>            prüft alle vorhandenen Dateien des Projekts
  python tools/check_files.py <projekt> design     nur bestimmte (project, design, structure)

Exit 0: alles in Ordnung (Hinweise möglich), 1: Fehler. tools/render_review.py ruft dieselbe Prüfung auf und erzeugt
keine Prüfseite, solange Fehler bestehen. So entsteht auf jeder Plattform dieselbe Seite, oder eine klare Liste, was fehlt.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import openbis_bridge as ob  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SCHEMAS = REPO / "schemas"
KINDS = ("project", "design", "structure")


def _schema_errors(data, kind: str) -> list[str]:
    try:
        import jsonschema
    except ImportError:  # minimal fallback: required top-level keys only
        sch = json.loads((SCHEMAS / f"{kind}.schema.json").read_text(encoding="utf-8"))
        return [f"{kind}: '{k}' fehlt" for k in sch.get("required", []) if k not in (data or {})]
    sch = json.loads((SCHEMAS / f"{kind}.schema.json").read_text(encoding="utf-8"))
    out = []
    for e in sorted(jsonschema.Draft202012Validator(sch).iter_errors(data), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(x) for x in e.absolute_path) or "(oben)"
        out.append(f"{kind}: {where}: {e.message}")
    return out


def check_project(repo: Path, name: str, kinds=KINDS, required=()) -> tuple[list[str], list[str]]:
    """(errors, notes). kinds: which files to check if present; required: which must exist."""
    errors, notes = [], []
    try:
        prj = ob.load_project(repo, name)
    except FileNotFoundError:
        return [f"projects/{name}/project.yaml fehlt (Vorlage: templates/)"], []
    except Exception as e:  # noqa: BLE001 - broken YAML etc.
        return [f"project.yaml lässt sich nicht lesen: {e}"], []
    cfg, pdir = prj["cfg"], prj["dir"]
    if "project" in kinds:
        errors += _schema_errors(cfg, "project")
        todo = [k for k, v in cfg.items() if isinstance(v, str) and v.startswith("<")]
        todo += [k for k, v in cfg.items() if isinstance(v, list) and any(str(x).startswith("/<") or str(x).startswith("<") for x in v)]
        if todo:
            notes.append("project.yaml: noch auszufüllen: " + ", ".join(sorted(set(todo))))
    paths = {"design": (pdir / cfg.get("design", "design.json")).resolve(), "structure": prj["structure"]}
    for kind in ("design", "structure"):
        if kind not in kinds:
            continue
        path = paths[kind]
        if not path.exists():
            (errors if kind in required else notes).append(f"{kind}.json fehlt ({path.relative_to(repo.resolve()) if path.is_relative_to(repo.resolve()) else path})")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{kind}.json ist kein gültiges JSON: {e}")
            continue
        errors += _schema_errors(data, kind)
        if kind == "structure":
            errors += [f"structure: {x}" for x in ob.validate_structure(data)]
        if kind == "design":
            secs = {p.get("section") for t in data.get("object_types", []) for p in t.get("properties", [])}
            missing = sorted(s for s in secs if s and s not in (data.get("section_names_de") or {}) and s not in (
                "General Information", "Additional Information", "Comments", "References", "Experimental Details",
                "BAM Information", "Properties"))
            if missing:
                errors.append("design: section_names_de: deutscher Name fehlt für " + ", ".join(missing))
            for v in data.get("vocabularies", []):
                for t in v.get("terms", []):
                    if not t.get("label_de") and any(c.islower() for c in t.get("label", "")):
                        errors.append(f"design: vocabularies/{v['code']}/{t['code']}: label_de fehlt")
    return errors, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Projektdateien gegen schemas/ prüfen")
    ap.add_argument("projekt")
    ap.add_argument("dateien", nargs="*", help="project, design, structure (Standard: alle)")
    ap.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    bad = [d for d in a.dateien if d not in KINDS]
    if bad:
        ap.error(f"unbekannt: {', '.join(bad)} (erlaubt: {', '.join(KINDS)})")
    errors, notes = check_project(a.repo, a.projekt, tuple(a.dateien) or KINDS)
    for n in notes:
        print("Hinweis:", n)
    for e in errors:
        print("Fehler: ", e)
    print("in Ordnung" if not errors else f"{len(errors)} Fehler")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
