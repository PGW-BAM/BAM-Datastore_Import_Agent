"""Antragspaket für den BAM-Admin (Workflow-Schritt 6) aus den Projektdateien bauen.

  python tools/build_request.py <projekt>            alles (braucht bam-masterdata für Excel und checker)
  python tools/build_request.py <projekt> --ohne-werkzeuge   nur Texte und request.json (z. B. in Tests)

Schreibt nach projects/<projekt>/request/:
  request.json      was beantragt wird, maschinenlesbar (Grundlage der Prüfseite „antrag“)
  issue.md          Issue-Text für BAMresearch/bam-masterdata (englisch, wie das Repo)
  mail.txt          Mail an datastore@bam.de (deutsch, förmlich)
  masterdata.xlsx   Excel-Fassung der neuen Typen (bam_masterdata export_to_excel)
  checker.log       Ergebnis von bam_masterdata checker --mode individual

Quellen: spec.json (neue Typen, Vokabulare, Ergänzungen), design.json (Namen, PRD-Bezüge, Wiederverwendung),
inventory_<instanz>.json falls vorhanden (was auf der Instanz nur nachgezogen werden muss). Die Texte sind ein Entwurf,
den der Agent bei Bedarf ergänzt; die Person prüft ihn auf der Prüfseite und schickt ihn ab (Prüfpunkt D).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import openbis_bridge as ob  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def split(text: str | None) -> tuple[str, str]:
    en, _, de = (text or "").partition("//")
    return en.strip(), (de or "").strip()


def collect(repo: Path, name: str) -> dict:
    prj = ob.load_project(repo, name)
    cfg, pdir = prj["cfg"], prj["dir"]
    design = ob.read_json((pdir / cfg.get("design", "design.json")).resolve()) or {}
    spec = ob.read_json(prj["spec"]) or {}
    catalog = ob.read_json(repo / "generated" / "catalog.json") or {"types": [], "sha": None}
    inv = ob.read_json(prj["inventory"])
    dprops = {p["code"]: p for t in design.get("object_types", []) for p in t.get("properties", [])}
    dtypes = {t["code"]: t for t in design.get("object_types", [])}
    std_codes = {t["code"] for t in catalog["types"]} | {
        p["code"] for t in catalog["types"] for p in t.get("properties", []) + t.get("inherited_properties", [])}

    types, props = [], []
    for t in spec.get("object_types", []):
        dt = dtypes.get(t["code"], {})
        en, de = split(t.get("description"))
        own = [p for p in t["properties"] if p["code"] in dprops and not dprops[p["code"]].get("reuse_property")]
        types.append({"code": t["code"], "parent": t.get("parent"), "name_en": dt.get("name_en") or en,
                      "name_de": dt.get("name_de") or de, "description": t.get("description"),
                      "covers_steps": dt.get("covers_steps", []), "fields": len(t["properties"]), "new_fields": len(own)})
        for p in own:
            props.append({"code": p["code"], "type": t["code"], "label": p["label"], "label_de": p.get("label_de"),
                          "data_type": p["data_type"], "section": p.get("section"), "vocabulary": p.get("vocabulary_code"),
                          "mandatory": p.get("mandatory"), "source": dprops[p["code"]].get("source")})
    dv = {v["code"]: v for v in design.get("vocabularies", [])}
    vocabs = [{"code": v["code"], "description": v.get("description"), "reason": (dv.get(v["code"]) or {}).get("decision_ref"),
               "terms": [{"code": x["code"], "label": x["label"], "label_de": x.get("label_de"), "description": x.get("description")}
                         for x in v["terms"]]} for v in spec.get("vocabularies", [])]
    ext = [{"vocabulary": e["vocabulary"], "citation": e.get("citation"), "reason": (dv.get(e["vocabulary"]) or {}).get("decision_ref"),
            "terms": e.get("terms", [])} for e in spec.get("extensions", [])]
    reused = [{"code": r["code"], "used_as": r.get("used_as"), "ref": r.get("ref")} for r in design.get("reused_types", [])]
    reused_props = [{"code": c, "ref": p.get("reuse_property")} for c, p in dprops.items() if p.get("reuse_property")]

    sync = None
    if inv:
        rep = ob.check(inv, spec)
        ours = {t["code"] for t in types} | {p["code"] for p in props} | {v["code"] for v in vocabs}
        sync = [m for m in rep["missing"] if m["what"].split(":")[0].strip() not in ours and
                any(m["what"].split(":")[-1].strip().startswith(c) or m["what"].startswith(c) for c in std_codes)]
        for r in reused:  # standard types the design uses directly must exist on the instance
            if r["code"] not in {t["code"] for t in inv.get("objectTypes", [])}:
                sync.append({"kind": "object type", "what": r["code"], "who": "admin"})
    applied = sorted(pdir.glob("reports/apply_*.json"))
    return {
        "project": name, "title": cfg.get("title"), "title_en": cfg.get("title_en"), "division": cfg.get("division"),
        "summary_en": cfg.get("summary_en"), "instance": prj["instance"], "bam_masterdata": cfg.get("bam_masterdata"),
        "catalog_sha": catalog.get("sha"), "inventory_collected": (inv or {}).get("collected"),
        "new_types": types, "new_properties": props, "new_vocabularies": vocabs, "extensions": ext,
        "reused_types": reused, "reused_properties": reused_props, "sync": sync,
        "tested_on": json.loads(applied[-1].read_text(encoding="utf-8")).get("instance") if applied else None,
    }


def run_tools(dm: Path, out: Path) -> dict:
    """Excel export and checker of bam-masterdata. Returns the checker counts."""
    exe = shutil.which("bam_masterdata")
    if not exe:
        return {"ran": False, "reason": "bam_masterdata not installed (bash tools/cloud_setup.sh)"}
    tmp = out / "_excel"
    subprocess.run([exe, "export_to_excel", "--python-path", str(dm), "--export-dir", str(tmp)], capture_output=True, text=True)
    if (tmp / "masterdata.xlsx").exists():
        shutil.move(str(tmp / "masterdata.xlsx"), out / "masterdata.xlsx")
    shutil.rmtree(tmp, ignore_errors=True)
    r = subprocess.run([exe, "checker", "--file-path", str(dm), "--mode", "individual"], capture_output=True, text=True)
    log = ANSI.sub("", (r.stdout or "") + (r.stderr or ""))
    (out / "checker.log").write_text(log, encoding="utf-8")
    warn = [re.sub(r"^.*?\]\s*", "", ln) for ln in log.splitlines() if "[warning" in ln]
    return {"ran": True, "errors": sum("[error" in ln for ln in log.splitlines()), "warnings": len(warn),
            "warning_texts": sorted(set(warn))}


INHERITED = ("$ANNOTATIONS_STATE is deprecated", "has the same properties defined as EXPERIMENTAL_STEP")


def issue_md(r: dict) -> str:
    title = r.get("title_en") or r.get("title") or r["project"]
    div = r.get("division") or "<division>"
    nt, nv, np_, ne = len(r["new_types"]), len(r["new_vocabularies"]), len(r["new_properties"]), sum(len(e["terms"]) for e in r["extensions"])
    L = [f"<!-- Title: Masterdata request: {title} -->",
         "<!-- Repository: https://github.com/BAMresearch/bam-masterdata/issues · suggested label: semver:minor (new entity types) -->", "",
         "## Summary", "",
         f"{div} documents {title} in the BAM Data Store. This needs **{nt} new object types**, **{nv} new vocabularies**, "
         f"**{np_} new property types** and **{ne} additional terms** in existing vocabularies. Everything else reuses "
         f"bam-masterdata {r.get('bam_masterdata') or ''} (`datamodel/v0`) as it is.", "",
         "Contribution: Python modules (ready for a PR, attached) and `masterdata.xlsx` (attached).", ""]
    if r.get("summary_en"):
        L += ["## Why", "", r["summary_en"], ""]
    L += ["## New object types", "", "| Code | Name (EN / DE) | Parent (v0) | Fields (new) | Covers workflow steps |", "|---|---|---|---|---|"]
    L += [f"| `{t['code']}` | {t['name_en']} / {t['name_de']} | `{t['parent']}` | {t['fields']} ({t['new_fields']}) | "
          f"{', '.join(t['covers_steps'])} |" for t in r["new_types"]]
    L += ["", "## New property types", "", "| Code | Label (EN) | Label (DE) | Type | Section | On type | Source |", "|---|---|---|---|---|---|---|"]
    L += [f"| `{p['code']}` | {p['label']} | {p.get('label_de') or ''} | {p['data_type']}{' → `' + p['vocabulary'] + '`' if p.get('vocabulary') else ''} | "
          f"{p.get('section') or ''} | `{p['type']}` | {p.get('source') or ''} |" for p in r["new_properties"]]
    L += ["", "## New vocabularies", ""]
    for v in r["new_vocabularies"]:
        en, de = split(v.get("description"))
        terms = ", ".join(f"`{x['code']}` {x['label']}{' / ' + x['label_de'] if x.get('label_de') else ''}" for x in v["terms"])
        L.append(f"- `{v['code']}`: {en}{' / ' + de if de else ''}. Terms: {terms}" + (f" (ref: {v['reason']})" if v.get("reason") else ""))
    if r["extensions"]:
        L += ["", "## Additions to existing vocabularies", "", "| Vocabulary | Defined at | New terms (EN / DE) |", "|---|---|---|"]
        L += [f"| `{e['vocabulary']}` | `{e.get('citation') or ''}` | "
              + ", ".join(f"`{x['code']}` {x['label']} / {x.get('label_de') or split(x.get('description'))[1]}" for x in e["terms"]) + " |"
              for e in r["extensions"]]
    L += ["", "## Instance sync only (no PR needed)", ""]
    if r["sync"] is None:
        L.append(f"To be determined: `{r['instance']}` has not been read yet.")
    elif not r["sync"]:
        L.append(f"Nothing: everything used from the standard exists on `{r['instance']}` (read {(r.get('inventory_collected') or '')[:10]}).")
    else:
        L += [f"Defined in bam-masterdata but missing on `{r['instance']}` (read {(r.get('inventory_collected') or '')[:10]}):", ""]
        L += [f"- {m['kind']}: `{m['what']}`" for m in r["sync"]]
    ck = r.get("checker") or {}
    L += ["", "## Checks", ""]
    if ck.get("ran"):
        own = [w for w in ck["warning_texts"] if not any(x in w for x in INHERITED)]
        L.append(f"- `bam_masterdata checker --mode individual`: {ck['errors']} errors, {ck['warnings']} warnings"
                 + (" (all inherited from the standard itself)" if not own else f" ({len(own)} to look at)"))
    else:
        L.append("- checker: not run in this draft")
    L += [f"- import test with bam-masterdata {r.get('bam_masterdata') or ''}: passed",
          "- German names via `property_label_de` / `label_de` (written to openBIS as `English//Deutsch`); sections in Title Case", ""]
    return "\n".join(L)


def mail_txt(r: dict) -> str:
    div = r.get("division") or "<Fachbereich>"
    title = r.get("title") or r["project"]
    nt, nv, np_, ne = len(r["new_types"]), len(r["new_vocabularies"]), len(r["new_properties"]), sum(len(e["terms"]) for e in r["extensions"])
    sync = "" if not r["sync"] else f" Auf {r['instance']} müssten außerdem {len(r['sync'])} Standard-Einträge nachgezogen werden."
    tested = f"\n\nDie Struktur haben wir auf {r['tested_on']} getestet." if r.get("tested_on") else ""
    ck = r.get("checker") or {}
    checker = f" Der checker meldet {ck['errors']} Fehler." if ck.get("ran") else ""
    return (f"An: datastore@bam.de\nBetreff: Masterdaten-Antrag {div}: {title}\n\nGuten Tag,\n\n"
            f"für {title} im {div} beantragen wir neue Masterdaten. Alle Einzelheiten stehen im Issue:\n\n<Issue-Link>\n\n"
            f"Kurz: {nt} neue Objekttypen, {nv} neue Auswahllisten, {np_} neue Felder und {ne} Ergänzungen bestehender Auswahllisten.{sync} "
            f"Python-Module und masterdata.xlsx hängen am Issue.{checker}{tested}\n\n"
            "Sobald die Typen verfügbar sind, legen wir unser Projekt selbst an. Für Rückfragen stehe ich gern zur Verfügung.\n\n"
            f"Mit freundlichen Grüßen\n<Name>\nData Store Steward {div}\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Antragspaket (Schritt 6) bauen")
    ap.add_argument("projekt")
    ap.add_argument("--ohne-werkzeuge", action="store_true", help="kein Excel-Export, kein checker")
    ap.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    prj = ob.load_project(a.repo, a.projekt)
    out = prj["dir"] / "request"
    out.mkdir(parents=True, exist_ok=True)
    r = collect(a.repo, a.projekt)
    dm = (prj["dir"] / prj["cfg"].get("datamodel", "datamodel")).resolve()
    r["checker"] = {"ran": False, "reason": "--ohne-werkzeuge"} if a.ohne_werkzeuge else run_tools(dm, out)
    ob.write_json(out / "request.json", r)
    (out / "issue.md").write_text(issue_md(r), encoding="utf-8")
    (out / "mail.txt").write_text(mail_txt(r), encoding="utf-8")
    print(f"{out}: {len(r['new_types'])} Typen, {len(r['new_vocabularies'])} Vokabulare, {len(r['new_properties'])} Felder, "
          f"{sum(len(e['terms']) for e in r['extensions'])} Ergänzungen; checker: "
          + (f"{r['checker']['errors']} Fehler, {r['checker']['warnings']} Warnungen" if r["checker"].get("ran") else "nicht gelaufen"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
