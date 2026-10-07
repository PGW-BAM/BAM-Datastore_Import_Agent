"""Deterministic catalog of bam-masterdata (replaces grep-based enumeration).

Parses every datamodel module with `ast`, resolves the *full* inheritance chain
(e.g. Camera -> Instrument -> ObjectType) and writes:

  generated/catalog.json  machine-readable (types, own + inherited properties, vocab terms)
  generated/CATALOG.md    human-readable index with file:line citations

Usage:
  python tools/build_catalog.py [--repo ../bam-masterdata]

Idempotent: same repo SHA -> byte-identical output (no timestamps, sorted keys).
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
from collections import defaultdict
from pathlib import Path

ROOTS = {"ObjectType", "VocabularyType", "CollectionType", "DatasetType"}
DEF_CALLS = {"ObjectTypeDef", "VocabularyTypeDef", "CollectionTypeDef", "DatasetTypeDef"}


def _kwargs(call: ast.Call) -> dict:
    out = {}
    for kw in call.keywords:
        try:
            out[kw.arg] = ast.literal_eval(kw.value)
        except ValueError:
            out[kw.arg] = ast.unparse(kw.value)
    return out


def parse_file(path: Path, rel: str) -> list[dict]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    classes = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        cls = {
            "class": node.name,
            "bases": [ast.unparse(b).split(".")[-1] for b in node.bases],
            "file": rel,
            "line": node.lineno,
            "defs": {},
            "properties": [],
            "terms": [],
        }
        for stmt in node.body:
            if not (isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call)):
                continue
            fn = ast.unparse(stmt.value.func).split(".")[-1]
            kw = _kwargs(stmt.value)
            if fn in DEF_CALLS:
                cls["defs"] = kw
            elif fn == "PropertyTypeAssignment":
                kw["attr"] = stmt.targets[0].id
                kw["line"] = stmt.lineno
                cls["properties"].append(kw)
            elif fn == "VocabularyTerm":
                kw["line"] = stmt.lineno
                cls["terms"].append(kw)
        classes.append(cls)
    return classes


def build(repo: Path) -> dict:
    dm = repo / "bam_masterdata" / "datamodel"
    classes = {}
    for path in sorted(dm.rglob("*.py")):
        if path.name.startswith("_"):
            continue
        rel = path.relative_to(repo).as_posix()
        for cls in parse_file(path, rel):
            classes[cls["class"]] = cls

    def chain(name: str) -> list[str]:
        seen = []
        while name in classes and name not in seen:
            seen.append(name)
            bases = classes[name]["bases"]
            name = bases[0] if bases else ""
        if name in ROOTS:
            seen.append(name)
        return seen

    for cls in classes.values():
        ch = chain(cls["class"])
        cls["chain"] = ch[1:]
        cls["root"] = ch[-1] if ch[-1] in ROOTS else None
        cls["code"] = cls["defs"].get("code")
        # inherited properties: walk parents, child overrides by code
        inherited = {}
        for anc in reversed(ch[1:]):
            for p in classes.get(anc, {}).get("properties", []):
                inherited[p["code"]] = {**p, "from": anc}
        own_codes = {p["code"] for p in cls["properties"]}
        cls["inherited_properties"] = [
            {"code": c, "data_type": p.get("data_type"), "from": p["from"]}
            for c, p in inherited.items() if c not in own_codes
        ]

    sha = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    date = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%cd", "--date=iso"],
        capture_output=True, text=True,
    ).stdout.strip()
    types = sorted(
        (c for c in classes.values() if c["root"]), key=lambda c: (c["root"], c["file"], c["line"])
    )
    return {"sha": sha, "commit_date": date, "types": types}


def is_step(c: dict) -> bool:
    return "ExperimentalStep" in c["chain"] or c["class"] == "ExperimentalStep"


def render_md(cat: dict) -> str:
    L = [
        "# bam-masterdata CATALOG",
        "",
        f"bam-masterdata SHA: {cat['sha']}",
        f"bam-masterdata commit date: {cat['commit_date']}",
        "Generator: `tools/build_catalog.py` (AST, full inheritance resolution — deterministic)",
        "",
        "Every row cites `file:line`. `Parent` is the direct base class; inherited",
        "properties are listed in `generated/catalog.json`.",
        "",
    ]
    by_root = defaultdict(list)
    for c in cat["types"]:
        key = "ExperimentalStep" if is_step(c) else c["root"]
        by_root[key].append(c)

    def table(title, rows, vocab=False):
        L.extend([f"## {title} ({len(rows)})", ""])
        if vocab:
            L.append("| Class | Code | Terms | File:Line |")
            L.append("|---|---|---|---|")
            for c in rows:
                terms = ", ".join(t.get("code", "?") for t in c["terms"])
                if len(terms) > 160:
                    terms = terms[:157] + "..."
                L.append(f"| {c['class']} | {c['code']} | {len(c['terms'])}: {terms} | {c['file']}:{c['line']} |")
        else:
            L.append("| Class | Code | Parent | Own props | File:Line |")
            L.append("|---|---|---|---|---|")
            for c in rows:
                parent = c["bases"][0] if c["bases"] else ""
                L.append(
                    f"| {c['class']} | {c['code']} | {parent} | {len(c['properties'])} | {c['file']}:{c['line']} |"
                )
        L.append("")

    table("ObjectTypes", by_root["ObjectType"])
    table("ExperimentalSteps", by_root["ExperimentalStep"])
    table("VocabularyTypes", by_root["VocabularyType"], vocab=True)
    table("CollectionTypes", by_root["CollectionType"])
    table("DatasetTypes", by_root["DatasetType"])

    # property-type index: which types already use a property code (reuse of PropertyTypes)
    idx = defaultdict(list)
    for c in cat["types"]:
        for p in c["properties"]:
            idx[p["code"]].append((c["class"], p.get("data_type"), p.get("vocabulary_code") or p.get("object_code") or ""))
    L.extend([f"## PropertyType index ({len(idx)} codes)", "",
              "| Property code | Data type | Vocab/Object ref | Used by |", "|---|---|---|---|"])
    for code in sorted(idx):
        users = idx[code]
        names = ", ".join(sorted({u[0] for u in users}))
        if len(names) > 120:
            names = names[:117] + "..."
        L.append(f"| {code} | {users[0][1]} | {users[0][2]} | {names} |")
    L.append("")
    return "\n".join(L)


def main() -> None:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(here.parent / "bam-masterdata"))
    args = ap.parse_args()
    cat = build(Path(args.repo))
    out = here / "generated"
    (out / "catalog.json").write_text(json.dumps(cat, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    (out / "CATALOG.md").write_text(render_md(cat), encoding="utf-8")
    n = defaultdict(int)
    for c in cat["types"]:
        n["ExperimentalStep" if is_step(c) else c["root"]] += 1
    print(f"SHA {cat['sha'][:8]}: " + ", ".join(f"{k}={v}" for k, v in sorted(n.items())))


if __name__ == "__main__":
    main()
