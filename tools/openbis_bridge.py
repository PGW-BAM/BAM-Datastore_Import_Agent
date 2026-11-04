"""openBIS bridge: read, check, dry run, create - one module for both sides of the handover.

The AI agent works in the cloud and never reaches openBIS. A person in the BAM network runs
notebooks/openbis_bruecke.ipynb, which imports this module. Files travel through the git repo:

  BAM network (notebook)                         cloud (agent)
  read_inventory()  -> live/<instance>_inventory.json  -> check() -> delivery_check.md
  apply(structure)  <- structure.json                  <- written by the agent (workflow step 8)
                    -> reports/apply_<date>.json       -> the agent reviews it

Everything that touches openBIS goes through one function `call(method, *params)` (openBIS 20.10,
V3 JSON-RPC, same calls as the proven tools/openbis_inventory.js and tools/openbis_demo.js).
`check()` and `validate_structure()` are pure and run offline, e.g. in the cloud:

  python tools/openbis_bridge.py validate projects/<name>/structure.json
  python tools/openbis_bridge.py check --inventory live/<inst>_inventory.json \
      [--spec projects/<name>/spec.json] [--structure projects/<name>/structure.json] [--md out.md]

Safety: apply() only CREATES what is missing (project, collections, objects). It never changes or
deletes anything, and it never creates types. dry_run=True is the default.

structure.json (written by the agent, see templates/structure.json):
  {"space": "FB_72", "project": {"code": "WELDED_FATIGUE", "description": "..."},
   "collections": [{"code": "SERIES_1", "type": "COLLECTION", "props": {"$NAME": "..."}}],
   "objects": [{"key": "S1-01", "code": "S1-01", "type": "SAMPLE.X", "collection": "SERIES_1",
                "props": {"$NAME": "S1-01", "NOTES": "@file:notes.txt"},
                "parents": ["OTHER_KEY", "/BAM_EQUIPMENT/FB72_EQUIPMENT_OPEN/GOM_ATOS_5"]}]}
  collection: code in this project, "/SPACE/PROJECT/COLLECTION" elsewhere (e.g. the division's
  equipment project), or null for an object directly in this project. Prop values "@file:<path>"
  are read from a text file next to structure.json. parents: keys from this file or identifiers.
  Link fields (property type OBJECT, pattern M4 in workflow/strukturmuster.md): "@obj:<key or identifier>", e.g.
  "props": {"INSTRUMENT": "@obj:RIG"}. The bridge writes the object's identifier, creates linked objects first and
  checks that linked inventory objects exist, like parents.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------------------------
# V3 JSON helpers


def T(t: str, **o) -> dict:
    return {"@type": t, **o}


def SID(i: str) -> dict:
    return T("as.dto.sample.id.SampleIdentifier", identifier=i)


def EID(i: str) -> dict:
    return T("as.dto.experiment.id.ExperimentIdentifier", identifier=i)


def PID(i: str) -> dict:
    return T("as.dto.project.id.ProjectIdentifier", identifier=i)


def SPID(c: str) -> dict:
    return T("as.dto.space.id.SpacePermId", permId=c)


def TID(c: str, kind: str) -> dict:
    return T("as.dto.entitytype.id.EntityTypePermId", permId=c, entityKind=kind)


FO = "as.dto.{}.fetchoptions.{}FetchOptions"
PA = T(FO.format("property", "PropertyAssignment"), propertyType=T(FO.format("property", "PropertyType")))


class Deref:
    """V3 JSON sends a repeated object once (with "@id") and later only its number."""

    def __init__(self, result):
        self.ids = {}
        self._walk(result)

    def _walk(self, o):
        if isinstance(o, dict):
            if "@id" in o:
                self.ids[o["@id"]] = o
            for v in o.values():
                self._walk(v)
        elif isinstance(o, list):
            for v in o:
                self._walk(v)

    def __call__(self, o):
        return self.ids.get(o, o) if isinstance(o, int) and not isinstance(o, bool) else o


def ident(x):
    return (x.get("identifier") or x.get("permId")) if isinstance(x, dict) else x


def v3_caller(o):
    """call(method, *params) on a logged-in pybis.Openbis (pyBIS 1.37.4 transport, token prepended)."""

    def call(method, *params):
        return o._post_request(o.as_v3, {"method": method, "params": [o.token, *params]})

    return call


def connect(url: str, token: str, verify_certificates: bool = True):
    """Return (openbis, call). The token is a personal access token or session token; never stored."""
    from pybis import Openbis

    o = Openbis(url, verify_certificates=verify_certificates)
    o.set_token(token, save_token=False)
    return o, v3_caller(o)


# --------------------------------------------------------------------------------------------
# 1 read


def _types_with_props(call, method, criteria, fetch):
    res = call(method, T(criteria), T(fetch, propertyAssignments=PA))
    ref = Deref(res)
    out = []
    for t in res.get("objects", []):
        pas = sorted((ref(a) for a in t.get("propertyAssignments") or []), key=lambda a: a.get("ordinal") or 0)
        row = {"code": t["code"], "description": t.get("description")}
        if "generatedCodePrefix" in t:
            row["generatedCodePrefix"] = t.get("generatedCodePrefix")
        row["properties"] = [
            {"code": ref(a["propertyType"])["code"], "dataType": ref(a["propertyType"]).get("dataType"),
             "section": a.get("section"), "mandatory": bool(a.get("mandatory"))}
            for a in pas
        ]
        out.append(row)
    return out


def read_inventory(call, instance: str, projects: list[str] = ()) -> dict:
    """Read-only snapshot: masterdata + collections and objects of the given projects (own project,
    the division's equipment projects). Only search*/get* calls."""
    vocs = call("searchVocabularies", T("as.dto.vocabulary.search.VocabularySearchCriteria"),
                T(FO.format("vocabulary", "Vocabulary"), terms=T(FO.format("vocabulary", "VocabularyTerm"))))
    vref = Deref(vocs)
    pts = call("searchPropertyTypes", T("as.dto.property.search.PropertyTypeSearchCriteria"),
               T(FO.format("property", "PropertyType"), vocabulary=T(FO.format("vocabulary", "Vocabulary")),
                 sampleType=T(FO.format("sample", "SampleType"))))
    pref = Deref(pts)
    prj = call("searchProjects", T("as.dto.project.search.ProjectSearchCriteria"), T(FO.format("project", "Project")))
    try:
        server = call("getServerInformation")
    except Exception:  # noqa: BLE001 - informational only
        server = None

    collections, objects = [], []
    if projects:
        got = call("getProjects", [PID(p) for p in projects], T(
            FO.format("project", "Project"),
            experiments=T(FO.format("experiment", "Experiment"), type=T(FO.format("experiment", "ExperimentType"))),
            samples=T(FO.format("sample", "Sample"), type=T(FO.format("sample", "SampleType")),
                      properties=T(FO.format("property", "Property")),
                      experiment=T(FO.format("experiment", "Experiment")))))
        ref = Deref(got)
        for p in got.values():
            p = ref(p)
            for e in p.get("experiments") or []:
                e = ref(e)
                collections.append({"identifier": ident(e["identifier"]), "type": ref(e["type"])["code"]})
            for s in p.get("samples") or []:
                s = ref(s)
                exp = ref(s.get("experiment")) if s.get("experiment") is not None else None
                objects.append({
                    "identifier": ident(s["identifier"]), "code": s["code"], "type": ref(s["type"])["code"],
                    "collection": ident(exp["identifier"]) if exp else None,
                    "name": (s.get("properties") or {}).get("$NAME"),
                })

    inv = {
        "instance": instance,
        "collected": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "server": server,
        "read_projects": list(projects),
        "vocabularies": [{"code": v["code"], "description": v.get("description"),
                          "terms": [vref(t)["code"] for t in v.get("terms") or []]} for v in vocs.get("objects", [])],
        "propertyTypes": [{
            "code": p["code"], "label": p.get("label"), "dataType": p.get("dataType"),
            "vocabulary": pref(p["vocabulary"])["code"] if p.get("vocabulary") is not None else None,
            "objectType": pref(p["sampleType"])["code"] if p.get("sampleType") is not None else None,
        } for p in pts.get("objects", [])],
        "objectTypes": _types_with_props(call, "searchSampleTypes", "as.dto.sample.search.SampleTypeSearchCriteria",
                                         FO.format("sample", "SampleType")),
        "collectionTypes": _types_with_props(call, "searchExperimentTypes",
                                             "as.dto.experiment.search.ExperimentTypeSearchCriteria",
                                             FO.format("experiment", "ExperimentType")),
        "datasetTypes": _types_with_props(call, "searchDataSetTypes", "as.dto.dataset.search.DataSetTypeSearchCriteria",
                                          FO.format("dataset", "DataSetType")),
        "projects": sorted(ident(p["identifier"]) for p in prj.get("objects", [])),
        "collections": sorted(collections, key=lambda c: c["identifier"]),
        "objects": sorted(objects, key=lambda o: o["identifier"]),
    }
    return inv


# --------------------------------------------------------------------------------------------
# project settings (projects/<name>/project.yaml), shared by tools/bruecke.py and the notebook


def load_project(repo: Path, name: str) -> dict:
    """Paths and settings of one project. Needs pyyaml."""
    import yaml

    pdir = Path(repo) / "projects" / name
    cfg = yaml.safe_load((pdir / "project.yaml").read_text(encoding="utf-8"))
    instance = cfg["instance"].rstrip("/")
    return {
        "name": name, "dir": pdir, "cfg": cfg, "instance": instance,
        "structure": (pdir / cfg.get("structure", "structure.json")).resolve(),
        "spec": (pdir / cfg.get("spec", "spec.json")).resolve(),
        "inventory": pdir / f"inventory_{instance.split('//')[-1].split('.')[0]}.json",
        "read_projects": [f"/{cfg['space']}/{cfg['project']}".upper()]
        + [p.upper() for p in cfg.get("inventory_projects") or []],
    }


def read_json(path: Path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def write_json(path: Path, data) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------------------------
# structure.json: resolve identifiers, validate


def load_structure(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _resolve(structure: dict) -> list[dict]:
    """Objects with absolute identifiers: space, project, experiment, identifier."""
    space = structure["space"].upper()
    proj = f"/{space}/{structure['project']['code']}".upper()
    out = []
    for ob in structure.get("objects", []):
        col = ob.get("collection")
        if col and col.startswith("/"):
            parts = col.strip("/").split("/")
            if len(parts) != 3:
                raise ValueError(f"{ob.get('key')}: collection must be /SPACE/PROJECT/COLLECTION, got {col}")
            sp, pj = parts[0].upper(), f"/{parts[0]}/{parts[1]}".upper()
            exp = col.upper()
        elif col:
            sp, pj, exp = space, proj, f"{proj}/{col}".upper()
        else:
            pj = (ob.get("project") or proj).upper()
            sp, exp = pj.strip("/").split("/")[0], None
        out.append({**ob, "_space": sp, "_project": pj, "_experiment": exp,
                    "_identifier": f"{pj}/{ob['code']}".upper()})
    return out


OBJ = "@obj:"


def links(o: dict) -> list[str]:
    """Targets of the link fields of an object ("@obj:<key or identifier>" values)."""
    return [v[len(OBJ):] for v in (o.get("props") or {}).values() if isinstance(v, str) and v.startswith(OBJ)]


def validate_structure(structure: dict) -> list[str]:
    """Offline consistency checks. Returns a list of problems (empty = fine)."""
    errs = []
    for k in ("space", "project"):
        if not structure.get(k):
            errs.append(f"missing '{k}'")
    if errs:
        return errs
    if not structure["project"].get("code"):
        errs.append("project.code missing")
    cols = [c.get("code") for c in structure.get("collections", [])]
    if len(cols) != len(set(cols)):
        errs.append("duplicate collection codes")
    try:
        objs = _resolve(structure)
    except ValueError as e:
        return errs + [str(e)]
    keys = [o.get("key") for o in objs]
    if None in keys:
        errs.append("every object needs a 'key'")
    if len(keys) != len(set(keys)):
        errs.append("duplicate object keys")
    idents = [o["_identifier"] for o in objs]
    if len(idents) != len(set(idents)):
        errs.append("duplicate object identifiers (same code in the same project)")
    keyset = set(keys)
    for o in objs:
        if not o.get("type"):
            errs.append(f"{o.get('key')}: type missing")
        col = o.get("collection")
        if col and not col.startswith("/") and col not in cols:
            errs.append(f"{o['key']}: collection '{col}' is not defined in collections")
        for p in o.get("parents", []):
            if not p.startswith("/") and p not in keyset:
                errs.append(f"{o['key']}: parent '{p}' is neither a key nor an identifier")
        for p in links(o):
            if not p.startswith("/") and p not in keyset:
                errs.append(f"{o['key']}: link '@obj:{p}' is neither a key nor an identifier")
    # cycles among file-internal parents
    try:
        _order(objs)
    except ValueError as e:
        errs.append(str(e))
    return errs


def _order(objs: list[dict]) -> list[list[dict]]:
    """Group objects into passes so that file-internal parents and linked objects are created first."""
    done, passes, rest = set(), [], list(objs)
    while rest:
        ready = [o for o in rest if all(p.startswith("/") or p in done for p in o.get("parents", []) + links(o))]
        if not ready:
            raise ValueError("parent cycle between: " + ", ".join(o["key"] for o in rest))
        passes.append(ready)
        done |= {o["key"] for o in ready}
        rest = [o for o in rest if o["key"] not in done]
    return passes


def _value(v, base_dir: Path | None, ids: dict | None = None):
    if isinstance(v, str) and v.startswith(OBJ):  # link field: key of this file -> identifier
        target = v[len(OBJ):]
        return (ids or {}).get(target, target)
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str) and v.startswith("@file:"):
        if base_dir is None:
            raise ValueError(f"{v}: no base directory for @file values")
        return (Path(base_dir) / v[len("@file:"):]).read_text(encoding="utf-8").strip()
    return str(v)


# --------------------------------------------------------------------------------------------
# 2 check (offline): spec / structure against an inventory snapshot


def check(inventory: dict, spec: dict | None = None, structure: dict | None = None) -> dict:
    """Compare what is wanted (spec: masterdata, structure: objects) with an inventory snapshot.

    missing  -> blocks creation (types/properties/terms absent, mandatory fields not filled,
                equipment absent)
    warnings -> worth a look (different section/mandatory flag, parent outside the read projects)
    """
    ot = {t["code"]: t for t in inventory.get("objectTypes", [])}
    ct = {t["code"]: t for t in inventory.get("collectionTypes", [])}
    voc = {v["code"]: set(v.get("terms") or []) for v in inventory.get("vocabularies", [])}
    pt = {p["code"]: p for p in inventory.get("propertyTypes", [])}
    objs_have = {o["identifier"].upper() for o in inventory.get("objects", [])}
    read_projects = [p.upper() for p in inventory.get("read_projects", [])]
    missing, warnings, info = [], [], []

    def miss(kind, what, who):
        missing.append({"kind": kind, "what": what, "who": who})

    if spec:
        for v in spec.get("vocabularies", []):
            if v["code"] not in voc:
                miss("vocabulary", v["code"], "admin")
            else:
                for t in v.get("terms", []):
                    if t["code"] not in voc[v["code"]]:
                        miss("term", f"{v['code']}: {t['code']}", "admin")
        for e in spec.get("extensions", []):
            if e["vocabulary"] not in voc:
                miss("vocabulary", e["vocabulary"], "admin")
                continue
            for t in e.get("terms", []):
                if t["code"] not in voc[e["vocabulary"]]:
                    miss("term", f"{e['vocabulary']}: {t['code']}", "admin")
        for t in spec.get("object_types", []):
            have = ot.get(t["code"])
            if not have:
                miss("object type", t["code"], "admin")
                continue
            assigned = {p["code"]: p for p in have["properties"]}
            for p in t.get("properties", []):
                if p["code"] not in pt:
                    miss("property type", p["code"], "admin")
                elif p["code"] not in assigned:
                    miss("assignment", f"{t['code']}: {p['code']}", "admin")
                else:
                    a = assigned[p["code"]]
                    if bool(p.get("mandatory")) != bool(a.get("mandatory")):
                        warnings.append(f"{t['code']}: {p['code']} mandatory {a.get('mandatory')} on instance, "
                                        f"{p.get('mandatory')} in spec")
                    if (p.get("section") or None) != (a.get("section") or None):
                        warnings.append(f"{t['code']}: {p['code']} section '{a.get('section')}' on instance, "
                                        f"'{p.get('section')}' in spec")

    if structure:
        for c in structure.get("collections", []):
            ctype = c.get("type") or "COLLECTION"
            if ctype not in ct:
                miss("collection type", ctype, "admin")
        try:
            objs = _resolve(structure)
        except ValueError as e:
            objs = []
            miss("structure", str(e), "agent")
        keys = {o["key"] for o in objs}
        for o in objs:
            t = ot.get(o["type"])
            if not t:
                miss("object type", o["type"], "admin")
                continue
            assigned = {p["code"]: p for p in t["properties"]}
            props = o.get("props") or {}
            for k, v in props.items():
                if k not in assigned:
                    miss("assignment", f"{o['type']}: {k} (used by {o['key']})", "admin")
                    continue
                vc = (pt.get(k) or {}).get("vocabulary")
                if vc and isinstance(v, str) and not v.startswith(("@file:", OBJ)) and v not in voc.get(vc, set()):
                    miss("term", f"{vc}: {v} (used by {o['key']})", "admin")
            for p in t["properties"]:
                if p["mandatory"] and p["code"] not in props:
                    miss("mandatory field", f"{o['key']}: {p['code']}", "agent")
            if o["_identifier"] in objs_have:
                info.append(f"{o['_identifier']} exists already (will be skipped)")
            for rel, par in [("parent", p) for p in o.get("parents", [])] + [("link", p) for p in links(o)]:
                if par in keys:
                    continue
                pu = par.upper()
                in_read = any(pu.startswith(rp + "/") for rp in read_projects)
                if pu not in objs_have:
                    if in_read:
                        miss("equipment", f"{par} ({rel} of {o['key']})", "you")
                    else:
                        warnings.append(f"{o['key']}: {rel} {par} lies outside the read projects, not checked")

    # stable order, no duplicates
    seen, uniq = set(), []
    for m in missing:
        k = (m["kind"], m["what"])
        if k not in seen:
            seen.add(k)
            uniq.append(m)
    return {
        "instance": inventory.get("instance"), "collected": inventory.get("collected"),
        "ready": not uniq, "missing": uniq, "warnings": sorted(set(warnings)), "info": sorted(set(info)),
    }


def save_report(pdir: Path, kind: str, data: dict) -> Path:
    """reports/<kind>_<date>.json (kind: check, dryrun, apply). Same files from the command and the notebook;
    tools/render_review.py <name> trockenlauf reads the newest check and dryrun report."""
    out = Path(pdir) / "reports" / f"{kind}_{datetime.now().date().isoformat()}.json"
    write_json(out, data)
    return out


WHO = {"admin": "Admin (Antrag, Schritt 6)", "you": "du (Inventar, Schritt 8)", "agent": "Agent (structure.json)"}


def render_check_md(rep: dict) -> str:
    lines = [f"# Lieferkontrolle {rep.get('instance') or ''}".rstrip(), "",
             f"Stand der Instanz: {rep.get('collected')}", "",
             f"**Ergebnis: {'bereit' if rep['ready'] else 'noch nicht bereit'}** "
             f"({len(rep['missing'])} fehlend, {len(rep['warnings'])} Hinweise)", ""]
    if rep["missing"]:
        lines += ["## Fehlt", "", "| Art | Was | Wer |", "|---|---|---|"]
        lines += [f"| {m['kind']} | `{m['what']}` | {WHO.get(m['who'], m['who'])} |" for m in rep["missing"]]
        lines.append("")
    if rep["warnings"]:
        lines += ["## Hinweise", ""] + [f"- {w}" for w in rep["warnings"]] + [""]
    if rep["info"]:
        lines += ["## Info", ""] + [f"- {i}" for i in rep["info"]] + [""]
    return "\n".join(lines)


# --------------------------------------------------------------------------------------------
# 3 + 4 dry run / create


def apply(call, structure: dict, base_dir: Path | None = None, dry_run: bool = True) -> dict:
    """Create what is missing: project, collections, objects (parents first). Idempotent."""
    errs = validate_structure(structure)
    if errs:
        raise ValueError("structure.json is not valid: " + "; ".join(errs))
    space = structure["space"].upper()
    proj = f"/{space}/{structure['project']['code']}".upper()
    rep = {"dryRun": dry_run, "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "created": [], "skipped": [], "droppedProps": []}

    def exists(method, ids, mk):
        if not ids:
            return set()
        return {k.upper() for k in call(method, [mk(i) for i in ids], T(FO.format(*_FO[method])))}

    # project
    if exists("getProjects", [proj], PID):
        rep["skipped"].append(proj)
    else:
        rep["created"].append(proj)
        if not dry_run:
            call("createProjects", [T("as.dto.project.create.ProjectCreation", spaceId=SPID(space),
                                       code=structure["project"]["code"],
                                       description=structure["project"].get("description"))])
    # collections
    cols = structure.get("collections", [])
    cids = [f"{proj}/{c['code']}".upper() for c in cols]
    have = exists("getExperiments", cids, EID)
    new = [c for c, i in zip(cols, cids) if i not in have]
    rep["skipped"] += [i for i in cids if i in have]
    rep["created"] += [f"{proj}/{c['code']}".upper() for c in new]
    if not dry_run and new:
        call("createExperiments", [T("as.dto.experiment.create.ExperimentCreation",
                                     typeId=TID(c.get("type") or "COLLECTION", "EXPERIMENT"), projectId=PID(proj),
                                     code=c["code"], properties={k: _value(v, base_dir) for k, v in
                                                                 (c.get("props") or {}).items() if v is not None})
                                   for c in new])
    # assigned properties per object type: drop what the instance does not know instead of failing
    sts = call("searchSampleTypes", T("as.dto.sample.search.SampleTypeSearchCriteria"),
               T(FO.format("sample", "SampleType"), propertyAssignments=PA))
    ref = Deref(sts)
    assigned = {s["code"]: {ref(ref(a)["propertyType"])["code"] for a in s.get("propertyAssignments") or []}
                for s in sts.get("objects", [])}
    objs = _resolve(structure)
    by_key = {o["key"]: o for o in objs}
    key_ids = {o["key"]: o["_identifier"] for o in objs}
    for batch in _order(objs):
        ids = [o["_identifier"] for o in batch]
        have = exists("getSamples", ids, SID)
        todo = [o for o in batch if o["_identifier"] not in have]
        rep["skipped"] += [i for i in ids if i in have]
        rep["created"] += [o["_identifier"] for o in todo]
        creations = []
        for o in todo:
            props = {}
            for k, v in (o.get("props") or {}).items():
                if v is None:
                    continue
                if k in assigned.get(o["type"], set()):
                    props[k] = _value(v, base_dir, key_ids)
                else:
                    rep["droppedProps"].append(f"{o['code']}: {k}")
            c = {"typeId": TID(o["type"], "SAMPLE"), "spaceId": SPID(o["_space"]),
                 "projectId": PID(o["_project"]), "code": o["code"], "properties": props}
            if o["_experiment"]:
                c["experimentId"] = EID(o["_experiment"])
            parents = [by_key[p]["_identifier"] if p in by_key else p for p in o.get("parents", [])]
            if parents:
                c["parentIds"] = [SID(p) for p in parents]
            creations.append(T("as.dto.sample.create.SampleCreation", **c))
        if not dry_run and creations:
            call("createSamples", creations)
    return rep


_FO = {"getProjects": ("project", "Project"), "getExperiments": ("experiment", "Experiment"),
       "getSamples": ("sample", "Sample")}


# --------------------------------------------------------------------------------------------
# CLI (offline parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate", help="check structure.json for consistency (offline)")
    v.add_argument("structure")
    c = sub.add_parser("check", help="compare spec/structure with an inventory snapshot (offline)")
    c.add_argument("--inventory", required=True)
    c.add_argument("--spec")
    c.add_argument("--structure")
    c.add_argument("--md", help="write the report as Markdown to this file")
    a = ap.parse_args(argv)
    if a.cmd == "validate":
        errs = validate_structure(load_structure(a.structure))
        print("\n".join(errs) if errs else "structure.json ok")
        return 1 if errs else 0
    rd = lambda p: json.loads(Path(p).read_text(encoding="utf-8")) if p else None  # noqa: E731
    rep = check(rd(a.inventory), rd(a.spec), rd(a.structure))
    md = render_check_md(rep)
    if a.md:
        Path(a.md).write_text(md + "\n", encoding="utf-8")
    print(md)
    return 0 if rep["ready"] else 2


if __name__ == "__main__":
    sys.exit(main())
