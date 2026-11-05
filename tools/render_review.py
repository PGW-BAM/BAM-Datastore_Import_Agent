"""Anschauliche Prüfseiten für Menschen: aus den Projektdateien wird eine HTML-Seite, die man ohne Technikwissen
lesen und mit „passt / ändern“ beantworten kann. Die Antwort wird als Text für den Chat kopiert.

  python tools/render_review.py <projekt> struktur      Prüfpunkt B: Aufbau, Ablauf → Ort, Formulare, Serientabelle

Ausgabe: projects/<projekt>/review/<ansicht>.html (eine Datei, keine Installation, im Browser öffnen).
Mit --fragment entsteht nur der Seiteninhalt (für Plattformen, die selbst ein HTML-Gerüst drumherum setzen).
Die Seite wird aus den Dateien erzeugt, nie von Hand geschrieben: gleicher Stand → gleiche Seite.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import openbis_bridge as ob  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
E = html.escape

TYPE_DE = {
    "VARCHAR": "Text", "MULTILINE_VARCHAR": "Text, mehrzeilig", "REAL": "Zahl", "INTEGER": "ganze Zahl",
    "BOOLEAN": "Ja / Nein", "CONTROLLEDVOCABULARY": "Auswahl", "TIMESTAMP": "Datum und Uhrzeit", "DATE": "Datum",
    "OBJECT": "Verweis auf ein Objekt", "SAMPLE": "Verweis auf ein Objekt", "HYPERLINK": "Link", "XML": "formatierter Text",
}
TYPE_EN = {
    "VARCHAR": "Text", "MULTILINE_VARCHAR": "Text, multi-line", "REAL": "Number", "INTEGER": "Whole number",
    "BOOLEAN": "Yes / No", "CONTROLLEDVOCABULARY": "Choice", "TIMESTAMP": "Date and time", "DATE": "Date",
    "OBJECT": "Link to an object", "SAMPLE": "Link to an object", "HYPERLINK": "Link", "XML": "Formatted text",
}
KIND_COLORS = ["probe", "scan", "test", "fracture", "extra"]


def t(de_txt: str, en_txt: str) -> str:
    """Page text in both languages; the switch at the top shows one (names of objects etc. use Name instead)."""
    return f'<span class="l-de" lang="de">{de_txt}</span><span class="l-en" lang="en">{en_txt}</span>'


def te(de_txt: str, en_txt: str) -> str:
    """Like t(), with escaping for plain text."""
    return t(E(de_txt), E(en_txt))


def de(text: str | None) -> tuple[str, str]:
    """'English//Deutsch' -> (english, deutsch); without '//' both are the text."""
    if not text:
        return "", ""
    en, _, d = text.partition("//")
    return en.strip(), (d or en).strip()


def de_only(text: str | None) -> str:
    """German part of 'English//Deutsch', or '' when there is none."""
    return text.partition("//")[2].strip() if text and "//" in text else ""


def short(text: str, n: int = 90) -> str:
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


# Standard sections of bam-masterdata v0 (German names for display; openBIS keeps the English section name)
SECTION_DE_STD = {"General Information": "Allgemeine Informationen", "Additional Information": "Zusätzliche Informationen",
                  "Comments": "Kommentare", "References": "Referenzen", "Experimental Details": "Versuchsdetails",
                  "BAM Information": "BAM-Informationen", "Properties": "Eigenschaften"}


class Name:
    """A name in both languages. src: 'label' (official German label), 'desc' (taken from the German description)."""

    def __init__(self, de_txt: str | None, en_txt: str | None, src: str = "label"):
        self.de, self.en = (de_txt or "").strip(), (en_txt or "").strip()
        self.src = src if self.de else ("std" if src == "std" else "missing")

    @property
    def text(self) -> str:
        if self.de and self.en and self.de != self.en:
            return f"{self.de} / {self.en}"
        return self.de or self.en

    def html(self, cls: str = "") -> str:
        derived = ' derived" title="aus der deutschen Beschreibung abgeleitet' if self.src == "desc" else ""
        if self.de and self.en and self.de != self.en:
            return (f'<span class="dual {cls}"><span class="de{derived}">{E(self.de)}</span>'
                    f'<span class="sep"> / </span><span class="en">{E(self.en)}</span></span>')
        if self.de:
            return f'<span class="dual {cls}"><span class="de{derived}">{E(self.de)}</span></span>'
        flag = chip("nur EN", "std", "EN only") if self.src == "std" else chip("DE fehlt", "miss", "DE missing")
        return f'<span class="dual {cls}"><span class="en">{E(self.en)}</span> {flag}</span>'


def from_desc(label_en: str, description: str | None, label_de: str | None = None, standard: bool = False) -> Name:
    """Official German label, else a short German description that reads like a name, else missing.
    standard=True: the name belongs to the BAM standard (only English there, nothing to fix in this project)."""
    if label_de:
        return Name(label_de, label_en)
    if label_en and len(label_en) <= 5 and not re.search(r"[a-zäöüß]", label_en):  # B90, C63: same in both languages
        return Name(label_en, label_en)
    d = de_only(description)
    if d and len(d) <= 40 and ";" not in d and d[0].isupper() and not d.lower().startswith(("z.b", "z. b")):
        return Name(d, label_en, "desc")
    return Name("", label_en, "std" if standard else "label")


# --------------------------------------------------------------------------------------------
# data


class Model:
    def __init__(self, repo: Path, name: str):
        self.project = ob.load_project(repo, name)
        cfg, pdir = self.project["cfg"], self.project["dir"]
        self.design = ob.read_json((pdir / cfg.get("design", "design.json")).resolve()) or {}
        self.spec = ob.read_json(self.project["spec"]) or {}
        self.structure = ob.read_json(self.project["structure"]) or {}
        self.catalog = ob.read_json(repo / "generated" / "catalog.json") or {"types": []}
        prd = (pdir / cfg.get("prd", "prd.md")).resolve()
        self.prd_text = prd.read_text(encoding="utf-8") if prd.exists() else ""
        self.prd_rel = str(prd.relative_to(repo.resolve())) if prd.is_relative_to(repo.resolve()) else str(prd)
        first = next((l for l in self.prd_text.splitlines() if l.startswith("# ")), "")
        prd_title = re.sub(r"^#\s*(PRD\s*(v\d+)?\s*:\s*)?", "", first).strip()
        # page heading from the project's own settings (title, title_en, division); the PRD heading only as fallback
        given = lambda k: str(cfg.get(k) or "").strip() if not str(cfg.get(k) or "").strip().startswith("<") else ""
        self.title_de = given("title") or re.sub(r"\s*\(.*?\)\s*$", "", prd_title) or name
        self.title_en = given("title_en") or self.title_de
        self.division = given("division")
        self.title = self.title_de
        self.missing: set[str] = set()  # names shown without German, counted for the header
        self.vocab: dict[str, dict] = {}
        for t in self.catalog["types"]:
            if t.get("root") == "VocabularyType":
                self.vocab[t["code"]] = {"terms": list(t.get("terms", [])), "description": t["defs"].get("description"),
                                         "status": "standard"}
        for v in self.design.get("vocabularies", []):
            existing = self.vocab.get(v["code"])
            self.vocab[v["code"]] = {"terms": (existing or {}).get("terms", []) + [
                t for t in v.get("terms", []) if t["code"] not in {x["code"] for x in (existing or {}).get("terms", [])}],
                "description": v.get("description"), "status": "erweitert" if existing else "neu",
                "new_terms": {t["code"] for t in v.get("terms", [])}}
        for e in self.spec.get("extensions", []):
            v = self.vocab.setdefault(e["vocabulary"], {"terms": [], "description": None, "status": "standard"})
            have = {t["code"] for t in v["terms"]}
            v["terms"] += [t for t in e.get("terms", []) if t["code"] not in have]
            v["status"] = "erweitert"
            v.setdefault("new_terms", set()).update(t["code"] for t in e.get("terms", []))
        # every property code -> label (en, de), type, vocabulary; own (new) codes from the design
        self.props: dict[str, dict] = {}

        def put(code, label, label_de, typ, desc, vocab, force=False):
            if force or code not in self.props:
                self.props[code] = {"label": label or code, "label_de": label_de, "type": typ, "description": desc,
                                    "vocabulary": vocab}
        for t in self.catalog["types"]:
            for p in t.get("properties", []) + t.get("inherited_properties", []):
                put(p["code"], p.get("property_label"), p.get("property_label_de"), p.get("data_type"), p.get("description"),
                    p.get("vocabulary_code"))
        self.new_codes = set()
        for t in self.design.get("object_types", []):
            for p in t.get("properties", []):
                put(p["code"], p.get("property_label"), p.get("property_label_de"), p.get("data_type"), p.get("description"),
                    p.get("vocabulary_code"), force=True)
                if not p.get("reuse_property"):
                    self.new_codes.add(p["code"])
        for t in self.spec.get("object_types", []):
            for p in t.get("properties", []):
                put(p["code"], p.get("label"), p.get("label_de"), p.get("data_type"), p.get("description"), p.get("vocabulary_code"))
        self.request = ob.read_json(pdir / "request" / "request.json")
        self.request_dir = pdir / "request"
        self.sections_de = {**SECTION_DE_STD, **(self.design.get("section_names_de") or {})}
        self.files = {de(x["file"])[0]: x["file"] for x in self.design.get("dataset_mapping", [])}
        self.devices = {de(x["inventory"])[0]: x["inventory"] for x in self.design.get("inventory_links", [])}
        # the main object of the workflow (specimen, batch, component, simulation …): first object in layout.per_specimen
        first = (self.design.get("layout", {}).get("per_specimen") or [{}])[0]
        self.main = Name(first.get("name_de") or "Hauptobjekt", first.get("name_en") or "main object")

    def _note(self, n: Name, key: str) -> Name:
        if n.src == "missing":
            self.missing.add(key)
        return n

    def prop_name(self, code: str) -> Name:
        p = self.props.get(code, {})
        return self._note(from_desc(p.get("label") or code, p.get("description"), p.get("label_de"),
                                    standard=code not in self.new_codes), f"p:{code}")

    def term_name(self, vocab: str | None, code: str) -> Name:
        for t in (self.vocab.get(vocab) or {}).get("terms", []):
            if t["code"] == code:
                new = code in (self.vocab.get(vocab) or {}).get("new_terms", set())
                return self._note(from_desc(t.get("label") or code, t.get("description"), t.get("label_de"), standard=not new),
                                  f"t:{vocab}:{code}")
        return Name(code, code)

    def section_name(self, s: str) -> Name:
        return self._note(Name(self.sections_de.get(s, ""), s), f"s:{s}")

    def type_name(self, t: dict) -> Name:
        dt = next((x for x in self.design.get("object_types", []) if x["code"] == t["code"]), {})
        if dt.get("name_de") or dt.get("name_en"):
            return Name(dt.get("name_de"), dt.get("name_en"))
        en, d = de(t.get("description"))
        return self._note(Name(d if "//" in (t.get("description") or "") else "", en), f"o:{t['code']}")

    def device_name(self, text: str) -> Name:
        text = text.replace(" (parent)", "")
        full = self.devices.get(text) or next((v for k, v in self.devices.items() if k.startswith(text) or text.startswith(k)), None)
        if full and "//" in full:
            en, d = de(full)
            return Name(d, en)
        return Name(text, text)  # proper names (ZEISS GOM ATOS 5) need no translation

    def file_name(self, text: str) -> Name:
        base = re.sub(r"\s*\(.*?\)\s*$", "", text)  # "Randomisation script (collection)" -> "Randomisation script"
        full = self.files.get(text) or next((v for k, v in self.files.items() if re.sub(r"\s*\(.*?\)\s*$", "", k) == base), text)
        if "//" in full:
            en, d = de(full)
            return Name(d, en)
        return self._note(Name("", full), f"f:{text}")

    def objects(self) -> list[dict]:
        """Objects per specimen with a kind (for colours) and a name in both languages."""
        out = []
        per = self.design.get("layout", {}).get("per_specimen", [])
        codes = [o["code_pattern"] for o in per]
        for i, o in enumerate(per):
            name = o.get("name_pattern", "")
            name = name[len(o["code_pattern"]):].strip() if name.startswith(o["code_pattern"]) else name
            nm = Name(o.get("name_de"), o.get("name_en") or name or "Specimen")
            own = [p for p in o.get("parents", []) if "(specimen)" in p or (p.split() or [""])[0] in codes]
            prev = next((p.split()[0] for p in own if "(specimen)" not in p), codes[0] if own and i else None)
            out.append({**o, "kind": KIND_COLORS[min(i, len(KIND_COLORS) - 1)], "name": self._note(nm, f"x:{o['code_pattern']}"),
                        "prev": prev,  # the object this one hangs on (specimen or previous step)
                        "equipment": [p for p in o.get("parents", []) if p not in own],  # inventory parents
                        "fields": list(o.get("links", []))})  # inventory objects linked by OBJECT fields (pattern M4)
        return out

    def object_for(self, text: str) -> dict | None:
        objs = self.objects()
        for o in sorted(objs, key=lambda o: -len(o["code_pattern"])):
            if o["code_pattern"] in text:
                return o
        return objs[0] if objs and ("specimen" in text or text.strip().lower().startswith("main")) else None


# --------------------------------------------------------------------------------------------
# html pieces


def chip(text: str, cls: str = "", en: str | None = None) -> str:
    inner = te(text, en) if en is not None else E(text)
    return f'<span class="chip {cls}">{inner}</span>'


def prop_row(m: Model, code: str, section_prop: dict) -> str:
    p = m.props.get(code, {})
    name = m.prop_name(code)
    d = de_only(p.get("description") or section_prop.get("description"))
    en_desc = de(p.get("description") or section_prop.get("description"))[0]
    dt = p.get("type") or section_prop.get("data_type")
    typ = te(TYPE_DE.get(dt, dt or ""), TYPE_EN.get(dt, dt or ""))
    target = section_prop.get("object_code")
    if dt in ("OBJECT", "SAMPLE"):  # link field: name the kind of object it points to
        tn = type_label(m, target) if target and target != "(ALL)" else Name("beliebiges Objekt", "any object")
        cls = next((x.get("class") for x in m.catalog.get("types", []) if x["code"] == target), None)
        short_en = re.sub(r"(?<!^)(?=[A-Z])", " ", cls) if cls else tn.en  # MeasuringAmplifier -> Measuring Amplifier
        if len(short_en) <= 4 and target:  # class "Bam" of PERSON.BAM -> "Person"
            short_en = target.split(".")[0].replace("_", " ").title()
        de_txt = tn.de if tn.de and len(tn.de) <= 30 else short_en
        en_txt = tn.en if tn.en and len(tn.en) <= 30 else short_en
        typ = t(f"Verweis auf {E(de_txt)}", f"Link to {E(en_txt)}")
    vocab = p.get("vocabulary") or section_prop.get("vocabulary_code")
    choice = ""
    if vocab and vocab in m.vocab:
        terms = [m.term_name(vocab, x["code"]).text for x in m.vocab[vocab]["terms"]]
        choice = f'<span class="terms">{E(" · ".join(terms[:8]))}{" …" if len(terms) > 8 else ""}</span>'
    badge = chip("neu", "new", "new") if code in m.new_codes else chip("Standard", "std", "standard")
    must = chip("Pflicht", "must", "mandatory") if section_prop.get("mandatory") else ""
    expl = te(d, en_desc) if d and d not in (name.de, name.en) else ""
    return (f'<li class="field"><div class="f-main"><span class="f-label">{name.html()}</span>'
            f'<span class="f-de">{expl}</span>{choice}</div>'
            f'<div class="f-meta"><span class="f-type">{typ}</span>{must}{badge}</div></li>')


def object_card(m: Model, ot: dict, role_kind: str) -> str:
    """ELN-like form preview: sections in display order with their fields."""
    secs: dict[str, list] = {}
    for p in ot.get("properties", []):
        secs.setdefault(p.get("section") or "Ohne Sektion", []).append(p)
    order = ot.get("section_order") or list(secs)
    system = {"Comments", "Additional Information", "References", "BAM Information", "Properties", "Ohne Sektion"}
    parts, hidden = [], []
    for s in [*order, *[x for x in secs if x not in order]]:
        fields = [p for p in secs.get(s, []) if not (p["code"].startswith("$") and p["code"] != "$NAME")]
        if not fields:
            continue
        own = sum(p["code"] in m.new_codes for p in fields)
        n = len(fields)
        count = t(f"{n} Felder{f', {own} neu' if own else ''}", f"{n} fields{f', {own} new' if own else ''}")
        block = (f'<section class="sec"><h4>{m.section_name(s).html()} <small>{count}</small></h4><ul>'
                 + "".join(prop_row(m, p["code"], p) for p in fields) + "</ul></section>")
        (hidden if s in system and not own else parts).append(block)
    more = (f'<details><summary>{t(f"Weitere Standard-Felder ({len(hidden)} Sektionen)", f"More standard fields ({len(hidden)} sections)")}'
            f'</summary>{"".join(hidden)}</details>' if hidden else "")
    return (f'<article class="card obj {role_kind}" id="obj-{E(ot["code"])}"><header><span class="dot"></span>'
            f'<div><h3>{m.type_name(ot).html()}</h3><code>{E(ot["code"])}</code></div>{chip("neuer Typ", "new", "new type")}</header>'
            f'{"".join(parts)}{more}</article>')


def feedback(item_id: str, label_de: str, label_en: str) -> str:
    return (f'<div class="fb" data-item="{E(item_id)}" data-label-de="{E(label_de)}" data-label-en="{E(label_en)}">'
            f'<span class="fb-q">{te(label_de, label_en)}:</span>'
            f'<button type="button" class="ok" aria-pressed="false">{t("passt", "fits")}</button>'
            f'<button type="button" class="chg" aria-pressed="false">{t("ändern", "change")}</button>'
            f'<textarea id="fb-{E(item_id)}" data-ph-de="Was soll anders sein?" data-ph-en="What should be different?" '
            f'placeholder="Was soll anders sein?" hidden></textarea></div>')


# --------------------------------------------------------------------------------------------
# view: struktur (Prüfpunkt B)


def form_types(m: Model) -> list[dict]:
    """Object types with all fields in display order. From spec.json when it exists (step 6 on); before that from
    design.json plus the parent's fields in the catalog, so the page also works at checkpoint B of a new project."""
    if m.spec.get("object_types"):
        return m.spec["object_types"]
    by_class = {t["class"]: t for t in m.catalog.get("types", [])}
    out = []
    for dt in m.design.get("object_types", []):
        parent = by_class.get(dt.get("parent_class") or "", {})
        props = {}
        for p in parent.get("inherited_properties", []) + parent.get("properties", []):
            props[p["code"]] = {"code": p["code"], "data_type": p.get("data_type"), "label": p.get("property_label"),
                                "description": p.get("description"), "section": p.get("section"), "mandatory": p.get("mandatory"),
                                "vocabulary_code": p.get("vocabulary_code")}
        for p in dt.get("properties", []):
            props[p["code"]] = {"code": p["code"], "data_type": p.get("data_type"), "label": p.get("property_label"),
                                "description": p.get("description"), "section": p.get("section"), "mandatory": p.get("mandatory"),
                                "vocabulary_code": p.get("vocabulary_code")}
        out.append({"code": dt["code"], "description": dt.get("description"), "section_order": dt.get("section_order"),
                    "properties": list(props.values())})
    return out


def lang_switch() -> str:
    return ('<div class="lang" role="group" aria-label="Sprache / Language">'
            '<button type="button" data-lang="de" aria-pressed="true">Deutsch</button>'
            '<button type="button" data-lang="en" aria-pressed="false">English</button></div>')


def section_head(n: str, sid: str, de_txt: str, en_txt: str) -> str:
    return f'<h2 id="{sid}"><span class="n">{n}</span>{te(de_txt, en_txt)}</h2>'


def hero_top(m: Model, gate_de: str, gate_en: str) -> str:
    """Eyebrow (division · checkpoint), language switch and the project title in both languages, from project.yaml."""
    div = f"{E(m.division)} · " if m.division else ""
    other = (f'<p class="sub">{t(E(m.title_en), E(m.title_de))}</p>' if m.title_en != m.title_de else "")
    return (f'<div class="hero-top"><span class="eyebrow">{div}{t(gate_de, gate_en)}</span>{lang_switch()}</div>'
            f'<h1>{t(E(m.title_de), E(m.title_en))}</h1>{other}')


def step_range(steps: list[str]) -> str:
    """['07','08','09','11'] -> '07–09, 11'."""
    out, run = [], []
    for x in steps:
        if run and x.isdigit() and run[-1].isdigit() and int(x) == int(run[-1]) + 1 and len(x) == len(run[-1]):
            run.append(x)
            continue
        if run:
            out.append(run[0] if len(run) < 3 else f"{run[0]}–{run[-1]}")
            out += run[1:] if len(run) == 2 else []
        run = [x]
    if run:
        out.append(run[0] if len(run) < 3 else f"{run[0]}–{run[-1]}")
        out += run[1:] if len(run) == 2 else []
    return ", ".join(out)


def variant_shape(v: dict) -> str:
    """Small sketch of a variant: main object, the objects hanging on it (flat), a chain, or one object."""
    objs = [{"name": Name(o.get("name_de"), o.get("name_en")), "steps": o.get("steps") or [], "before": o.get("before")}
            for o in v["objects"]]
    main = objs[0]
    before = [o for o in objs[1:] if o["before"]]  # the main object is made from these (pattern M3)
    rest = [o for o in objs[1:] if not o["before"]]

    def box(o, cls=""):
        st = f'<small>{te("Schritte ", "Steps ")}{E(step_range(o["steps"]))}</small>' if o["steps"] else ""
        return f'<div class="vbox {cls}">{o["name"].html()}{st}</div>'

    def pill(o):
        label = step_range(o["steps"]) or str(objs.index(o))
        return f'<span class="vpill" title="{E(o["name"].text)}">{E(label)}</span>'
    if v["shape"] == "single" or not rest:
        sketch = box(main, "main")
    elif len(rest) <= 5 and v["shape"] == "flat":
        sketch = (f'{box(main, "main")}<div class="arrow">↓ {t("hängen direkt daran", "attached directly")}</div>'
                  f'<div class="vrow">{"".join(box(o) for o in rest)}</div>')
    elif v["shape"] == "flat":
        sketch = (f'{box(main, "main")}<div class="arrow">↓ {t(f"{len(rest)} Objekte, alle direkt daran", f"{len(rest)} objects, all attached directly")}</div>'
                  f'<div class="vrow pills">{"".join(pill(o) for o in rest)}</div>')
    elif len(rest) <= 5:  # short process line
        sketch = box(main, "main") + "".join(f'<div class="arrow">↓</div>{box(o)}' for o in rest)
    else:  # long chain
        sketch = (f'<div class="vrow chain">{box(main, "main")}<span class="arrow">→</span>'
                  + '<span class="arrow">→</span>'.join(pill(o) for o in rest) + "</div>")
    if before:
        sketch = ("".join(box(o) for o in before) + f'<div class="arrow">↓ {t("daraus entsteht", "makes")}</div>' + sketch)
    names = ""
    if len(rest) > 5:
        names = (f'<details><summary>{t("Alle Objekte anzeigen", "Show all objects")}</summary><ol class="vlist">'
                 + "".join(f'<li><code>{E(step_range(o["steps"]))}</code> {o["name"].html()}</li>' for o in rest) + "</ol></details>")
    return f'<div class="vsketch {v["shape"]}">{sketch}</div>{names}'


def variants_section(m: Model, num: str) -> str:
    d = m.design
    vs = d.get("variants") or []
    if not vs:
        return ""
    rec = next((v for v in vs if v.get("recommended")), vs[0])
    shown = d.get("variant") or rec["id"]
    cards = []
    for v in vs:
        nm = Name(v["name_de"], v["name_en"])
        is_rec, is_shown = v is rec, v["id"] == shown
        tags = (f'<span class="rec">{t("(empfohlen)", "(recommended)")}</span>' if is_rec else "")
        marks = chip("unten ausgearbeitet", "new", "worked out below") if is_shown else ""
        figs = "".join(f'<div><b>{E(str(v[k]))}</b><span>{te(a, b)}</span></div>' for k, a, b in (
            ("objects_per_specimen", f"Objekte je {m.main.de}", f"objects per {m.main.en.lower()}"),
            ("max_link_depth", "Ebenen darunter", "levels below it"),
            ("new_object_types", "neue Objekttypen", "new object types"),
            ("new_dataset_types", "neue Datei-Typen", "new file types"),
            ("shared_parents", "Geräte als Eltern im Graphen", "instruments as parents in the graph")) if v.get(k) is not None)
        pros = "".join(f'<li>{te(x["de"], x["en"])}</li>' for x in v["pros"])
        cons = "".join(f'<li>{te(x["de"], x["en"])}</li>' for x in v["cons"])
        src = f'<p class="muted">{t("Herkunft", "Source")}: {E(v["source"])}</p>' if v.get("source") else ""
        cards.append(f"""<label class="variant{' recommended' if is_rec else ''}{' shown' if is_shown else ''}">
<input type="radio" name="variant" value="{E(v['id'])}" data-name="{E(nm.text)}"{' checked' if is_rec else ''}>
<div class="v-head"><span class="v-id">{E(v['id'])}</span><h3>{nm.html()} {tags}</h3>{marks}</div>
<p>{te(v['summary_de'], v['summary_en'])}</p>{variant_shape(v)}
{f'<div class="vfigs">{figs}</div>' if figs else ''}
<div class="pc"><ul class="pros" aria-label="{E('Vorteile / Advantages')}">{pros}</ul><ul class="cons" aria-label="{E('Nachteile / Disadvantages')}">{cons}</ul></div>{src}</label>""")
    rnm = Name(rec["name_de"], rec["name_en"]).text
    if rec["id"] == shown:
        why = t(f"Empfohlen ist Variante <b>{E(rec['id'])}</b> ({E(rnm)}); sie ist auf dieser Seite ausgearbeitet. "
                "Wählen Sie eine andere, arbeitet der Agent diese aus und zeigt Ihnen eine neue Seite.",
                f"Variant <b>{E(rec['id'])}</b> ({E(rnm)}) is recommended; it is worked out on this page. "
                "If you choose another one, the agent works it out and shows you a new page.")
    else:
        why = t(f"Empfohlen ist Variante <b>{E(rec['id'])}</b> ({E(rnm)}). Weiter unten ist noch Variante <b>{E(shown)}</b> ausgearbeitet. "
                f"Bleibt Ihre Wahl bei {E(rec['id'])}, arbeitet der Agent sie aus und zeigt Ihnen eine neue Seite; die Teile unten müssen Sie dann nicht beantworten.",
                f"Variant <b>{E(rec['id'])}</b> ({E(rnm)}) is recommended. Further down, variant <b>{E(shown)}</b> is still worked out. "
                f"If you keep {E(rec['id'])}, the agent works it out and shows you a new page; you do not need to answer the parts below then.")
    return f"""<section aria-labelledby="hvs" class="variants" data-shown="{E(shown)}" data-rec="{E(rec['id'])}">{section_head(num, "hvs", "Welche Struktur soll es werden?", "Which structure should it be?")}
<p>{t(f"Der Agent hat {len(vs)} Möglichkeiten durchgespielt, Ihren Ablauf in openBIS abzubilden. ", f"The agent worked through {len(vs)} ways of mapping your workflow in openBIS. ")}{why}
{t('Muster und Quellen: <code>workflow/strukturmuster.md</code>.', 'Patterns and sources: <code>workflow/strukturmuster.md</code>.')}</p>
<fieldset class="vgrid"><legend class="sr">{t("Variante wählen", "Choose a variant")}</legend>{"".join(cards)}</fieldset>
<p id="v-note" class="vnote" hidden>{t(f"Ihre Wahl ist nicht die Variante, die weiter unten ausgearbeitet ist ({E(shown)}). Die Teile unten müssen Sie "
      "jetzt nicht beantworten. Ihr Text ganz unten bittet den Agenten, Ihre Wahl auszuarbeiten.",
      f"Your choice is not the variant worked out further down ({E(shown)}). You do not need to answer the parts below now. "
      "Your text at the bottom asks the agent to work out your choice.")}</p></section>"""


def view_struktur(m: Model) -> str:
    d, lay = m.design, m.design.get("layout", {})
    objs = m.objects()
    st = m.structure
    space, project = lay.get("space", f"/{st.get('space', '')}"), lay.get("project", "")
    cols = lay.get("collections", [])
    body = [variants_section(m, "1")]

    # 2 hierarchy: hub (steps hang on the specimen) or process line (specimen -> step -> step)
    collections = "".join(f'<div class="node col"><b>{E(c.get("$NAME") or c["code"])}</b><code>{E(c["code"])}</code></div>'
                          for c in cols)
    plan = "".join(f'<div class="node plan"><b>{E(o.get("$NAME") or o["code"])}</b><span>{t("einmal im Projekt", "once per project")}</span></div>'
                   for o in lay.get("project_objects", []))
    probe = objs[0] if objs else {"name": m.main, "code_pattern": "", "kind": "probe"}
    up_codes = {p.split()[0] for p in probe.get("parents", []) if p.split()}
    upstream = [o for o in objs[1:] if o["code_pattern"] in up_codes]  # the main object is made from these (M3)
    objs_down = [o for o in objs[1:] if o not in upstream]
    line = len(objs_down) > 1 and any(o["prev"] not in (None, probe["code_pattern"]) for o in objs_down)

    def node(o):
        return (f'<div class="node obj {o["kind"]}"><span class="dot"></span><b>{o["name"].html()}</b>'
                f'<code>{E(o["code_pattern"])}</code>'
                f'{"<span>" + te("Schritte ", "Steps ") + E(step_range(o.get("covers_steps", []))) + "</span>" if o.get("covers_steps") else ""}'
                f'{"".join(chip(short(m.device_name(e).text, 60), "dev") for e in o["equipment"])}'
                f'{"".join(chip(short(m.device_name(e).text, 60), "dev lnk") for e in o["fields"])}</div>')
    if line:
        steps = "".join(f'<div class="arrow">↓ {t("danach", "then")}</div>{node(o)}' for o in objs_down)
        below = f'<div class="line">{steps}</div>'
        intro = t(f"Eine Serie ist eine Collection. Darin steht jedes Objekt „{E(m.main.de)}“ einmal. Seine Ablaufschritte folgen als Linie "
                  "aufeinander, so wie sie im Labor stattfinden. Geräte und Material kommen aus dem Inventar des Fachbereichs.",
                  f"A series is a collection. Each “{E(m.main.en)}” object appears once in it. Its workflow steps follow each other as a line, "
                  "in the order they happen in the lab. Instruments and materials come from the division's inventory.")
    else:
        steps = "".join(node(o) for o in objs_down)
        below = (f'<div class="arrow">↓ {t("hängen direkt daran", "attached directly")}</div><div class="row">{steps}</div>'
                 if objs_down else "")
        intro = t(f"Eine Serie ist eine Collection. Darin steht jedes Objekt „{E(m.main.de)}“ einmal, und seine Ablaufschritte hängen direkt daran. "
                  "Geräte und Material kommen aus dem Inventar des Fachbereichs.",
                  f"A series is a collection. Each “{E(m.main.en)}” object appears once in it, and its workflow steps hang directly on it. "
                  "Instruments and materials come from the division's inventory.")
    legend = t(f"{chip('Gerät', 'dev', 'instrument')} als Eltern verlinkt (im Graphen sichtbar)"
               f"{' · ' + chip('Gerät', 'dev lnk', 'instrument') + ' als Feld verlinkt (im Formular, nicht im Graphen)' if any(o['fields'] for o in objs) else ''}",
               f"{chip('Gerät', 'dev', 'instrument')} linked as parent (shown in the graph)"
               f"{' · ' + chip('Gerät', 'dev lnk', 'instrument') + ' linked as a field (in the form, not in the graph)' if any(o['fields'] for o in objs) else ''}")
    body.append(f"""<section aria-labelledby="h1s">{section_head("2", "h1s", "So ist Ihr Projekt aufgebaut", "How your project is built")}
<p>{intro}</p>
<div class="tree"><div class="node root"><span>Space</span><b>{E(space)}</b></div><div class="arrow">↓</div>
<div class="node root"><span>{t("Projekt", "Project")}</span><b>{E(project)}</b></div><div class="arrow">↓</div>
<div class="row">{collections}{plan}</div><div class="arrow">↓ {t(f"in jeder Serie, je {E(m.main.de)}", f"in every series, per {E(m.main.en.lower())}")}</div>
<div class="specimen">{"".join(node(o) + '<div class="arrow">↓ ' + t("daraus entsteht", "makes") + '</div>' for o in upstream)}<div class="node obj {probe['kind']} big"><span class="dot"></span><b>{probe['name'].html()}</b><code>{E(probe['code_pattern'])}</code>
<span>{t("Hauptobjekt: trägt alle beschreibenden Angaben", "main object: holds all describing data")}</span>{"".join(chip(short(m.device_name(e).text, 60), "dev") for e in probe.get("equipment", []))}{"".join(chip(short(m.device_name(e).text, 60), "dev lnk") for e in probe.get("fields", []))}</div>
{below}</div></div>
<p class="hint">{legend}</p>
{feedback("aufbau", "Aufbau", "Build-up")}</section>""")

    # 3 step -> location
    rows = []
    for s in d.get("step_location_map", []):
        o = m.object_for(s.get("object", "")) or {"kind": "extra", "name": Name("", s.get("object", ""))}
        items = []
        for it in s.get("data_items", []):
            code = it.split()[0]
            quoted = re.match(r"'([^']+)'", it)
            if code in m.props:
                items.append(m.prop_name(code).text)
            else:
                items.append(quoted.group(1) if quoted else short(it.split(" = ")[0], 60))
        sec = s.get("section") if s.get("section") not in (None, "-") else ""
        sec_html = " + ".join(m.section_name(x.strip()).html() for x in sec.split("+")) if sec else ""
        rows.append(f"""<li class="step {o['kind']}"><span class="no">{E(s.get('no', ''))}</span><div class="s-body">
<h3>{m._note(Name(s.get('step_de'), s.get('step', '')), 'st:' + s.get('no', '')).html()}</h3>
<p class="where">→ <b>{o['name'].html()}</b>{f" · {t('Abschnitt', 'Section')} {sec_html}" if sec else ""}</p>
{'<p class="items">' + E(" · ".join(items)) + "</p>" if items else ""}
<div class="chips">{"".join(chip(short(m.device_name(e).text, 60), "dev") for e in s.get("equipment", []))}{"".join(chip(m.file_name(f).text, "file") for f in s.get("files", []))}</div></div></li>""")
    body.append(f"""<section aria-labelledby="h2s">{section_head("3", "h2s", "Wo landet welcher Ablaufschritt?", "Where does each workflow step go?")}
<p>{t("Die Farbe zeigt das Objekt, in das der Schritt geschrieben wird. Umrandete Marken sind Geräte oder Material, gestrichelte sind Dateien.",
      "The colour shows the object the step is recorded in. Outlined tags are instruments or materials, dashed ones are files.")}</p>
<ol class="timeline">{"".join(rows)}</ol>{feedback("ablauf", "Zuordnung der Schritte", "Step assignment")}</section>""")

    # 4 object forms
    kinds = {o["type"]: o["kind"] for o in reversed(objs)}
    order = {o["type"]: i for i, o in enumerate(objs)}
    spec_types = sorted(form_types(m), key=lambda x: order.get(x["code"], 99))
    cards = [object_card(m, x, kinds.get(x["code"], "extra")) for x in spec_types]
    reused = [o for o in objs if o["type"] not in {x["code"] for x in spec_types}]
    for o in reused:
        role = next((r.get("role", "") for r in d.get("reused_types", []) if r.get("code") == o["type"] and
                     r.get("used_as", "").endswith(o["code_pattern"][len(objs[0]["code_pattern"]):] or "~")), "")
        default = te("Standard-Versuchsschritt: Datum, Bearbeiter*in, Notizen, Dateien. Keine neuen Felder.",
                     "Standard experimental step: date, operator, notes, files. No new fields.")
        cards.append(f'<article class="card obj {o["kind"]} slim"><header><span class="dot"></span><div><h3>{o["name"].html()}</h3>'
                     f'<code>{E(o["type"])}</code></div>{chip("aus dem Standard", "std", "from the standard")}</header>'
                     f'<p>{E(short(role, 220)) if role else default}</p></article>')
    fb = "".join(feedback(f"obj-{x['code']}", f"Felder „{short(m.type_name(x).de or m.type_name(x).en, 50)}“",
                          f"Fields “{short(m.type_name(x).en, 50)}”") for x in spec_types)
    body.append(f"""<section aria-labelledby="h3s">{section_head("4", "h3s", "Welche Felder bekommt jedes Objekt?", "Which fields does each object get?")}
<p>{t("So ungefähr sieht das Formular in der ELN aus. <b>neu</b> heißt: beantragt der Agent beim Data Store, <b>Standard</b> gibt es schon. "
      "Felder mit <b>Pflicht</b> müssen beim Anlegen ausgefüllt sein.",
      "This is roughly how the form looks in the ELN. <b>new</b> means the agent requests it from the Data Store, <b>standard</b> exists already. "
      "Fields marked <b>mandatory</b> must be filled in when an object is created.")}</p>
<div class="cards">{"".join(cards)}</div>{fb}</section>""")

    # 5 series table
    cols_ = lay.get("series_table", [])
    specimens = [o for o in st.get("objects", []) if objs and o.get("type") == objs[0]["type"]][:4]
    by_key = {o["key"]: o for o in st.get("objects", [])}

    main_pattern = objs[0]["code_pattern"] if objs else ""

    def cell(src: str, sp: dict) -> str:
        """source = '<object> <PROPERTY …>': object 'main'/'specimen' or the suffix of a per-object code (TEST for S1-01-TEST)."""
        first = (src.split() or [""])[0]
        codes = re.findall(r"[A-Z$][A-Z0-9_.$]+", src)
        target = sp
        other = next((o for o in objs[1:] if first and (o["code_pattern"].endswith("-" + first) or o["type"] == first)), None)
        if other:
            suffix = other["code_pattern"][len(main_pattern):] if other["code_pattern"].startswith(main_pattern) else "-" + first
            target = by_key.get(f"{sp['key']}{suffix}") or {}
            codes = codes[1:] if codes and codes[0] == first else codes
        for c in codes:
            v = (target.get("props") or {}).get(c)
            if v is not None:
                vocab = m.props.get(c, {}).get("vocabulary")
                return m.term_name(vocab, str(v)).text if vocab else str(v)
        return "–"
    head = "".join(f"<th>{m._note(Name(de(c['column'])[1] if '//' in c['column'] else '', de(c['column'])[0]), 'c:' + c['column']).html('th')}</th>"
                   for c in cols_)
    rows_ = "".join("<tr>" + "".join(f"<td>{E(cell(c['source'], sp))}</td>" for c in cols_) + "</tr>" for sp in specimens)
    if not specimens:
        rows_ = (f'<tr><td colspan="{max(len(cols_), 1)}">{t("Beispielzeilen folgen, sobald structure.json mit Beispielobjekten steht (Schritt 8).", "Example rows follow once structure.json with example objects exists (step 8).")}</td></tr>')
    body.append(f"""<section aria-labelledby="h4s">{section_head("5", "h4s", "So sieht die Serientabelle aus", "What the series table looks like")}
<p>{t("Das ist die Tabelle, die man beim Öffnen einer Serie sieht. Die Werte sind Beispieldaten aus structure.json (fiktiv).",
      "This is the table you see when you open a series. The values are example data from structure.json (fictitious).")}</p>
<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{rows_}</tbody></table></div>{feedback("tabelle", "Serientabelle", "Series table")}</section>""")

    # 6 vocabularies
    vcards = []
    for code, v in m.vocab.items():
        if v["status"] == "standard":
            continue
        new = v.get("new_terms", set())
        terms = "".join(f'<li class="{"newt" if x["code"] in new else ""}">{m.term_name(code, x["code"]).html()}</li>' for x in v["terms"])
        en, dd = de(v.get("description"))
        badge = chip("neu", "new", "new") if v["status"] == "neu" else chip("ergänzt", "new", "extended")
        vcards.append(f'<article class="card voc"><header><div><h3>{m._note(Name(dd if "//" in (v.get("description") or "") else "", en), "v:" + code).html()}</h3>'
                      f'<code>{E(code)}</code></div>{badge}</header><ul class="tlist">{terms}</ul></article>')
    body.append(f"""<section aria-labelledby="h5s">{section_head("6", "h5s", "Auswahllisten", "Choice lists")}
<p>{t("Hier wählt man im Formular aus einer festen Liste. Hervorgehoben sind die Einträge, die neu dazukommen.",
      "In the form you pick from a fixed list. Entries that are being added are highlighted.")}</p>
<div class="cards">{"".join(vcards)}</div>{feedback("listen", "Auswahllisten", "Choice lists")}</section>""")

    # 7 terms in both languages
    body.append(f'<section aria-labelledby="h8s">{section_head("7", "h8s", "Begriffe in beiden Sprachen", "Terms in both languages")}'
                f'<p>{t("Alle Namen oben stehen auf Deutsch und Englisch. Stimmen die Begriffe in beiden Sprachen? Schreiben Sie bei „ändern“ "
                        "die gewünschten Begriffe einfach dazu, z. B. „alter Begriff → neuer Begriff“.",
                        "All names above are given in German and English. Are the terms right in both languages? With “change”, just write "
                        "the terms you want, e.g. “old term → new term”.")}</p>'
                f'{feedback("begriffe", "Begriffe Deutsch / Englisch", "Terms German / English")}</section>')

    # 8 answer
    body.append(f"""<section aria-labelledby="h7s" class="answer" data-gate="B"><h2 id="h7s"><span class="n">✓</span>{t("Ihre Antwort an den Agenten", "Your reply to the agent")}</h2>
<label for="fb-gesamt">{t("Noch etwas Allgemeines? (freiwillig)", "Anything else? (optional)")}</label><textarea id="fb-gesamt" rows="3"></textarea>
<p id="state" class="state"></p>
<pre id="out" class="out" aria-live="polite"></pre>
<button type="button" data-copy="#out" class="primary">{t("Text kopieren", "Copy text")}</button>
<p class="hint">{t("Den kopierten Text fügen Sie im Chat mit dem Agenten ein. Die Seite speichert nichts und schickt nichts ab.",
                   "Paste the copied text into the chat with the agent. The page stores nothing and sends nothing.")}</p></section>""")

    # header last, because it reports how many names still lack German
    n = len(m.missing)
    legend = (t(f"Alle Namen stehen als <b>Deutsch</b> / Englisch. <i>Kursiv</i> = aus der deutschen Beschreibung übernommen. "
                f"{chip('DE fehlt', 'miss', 'DE missing')} = deutsche Fassung fehlt noch ({n if n else 'hier keine'}). "
                f"{chip('nur EN', 'std', 'EN only')} = Name aus dem BAM-Standard, den es dort nur auf Englisch gibt.",
                f"All names are shown as <b>German</b> / English. <i>Italics</i> = taken from the German description. "
                f"{chip('DE fehlt', 'miss', 'DE missing')} = German version still missing ({n if n else 'none here'}). "
                f"{chip('nur EN', 'std', 'EN only')} = name from the BAM standard that exists only in English there."))
    header = f"""<header class="hero">{hero_top(m, "Prüfpunkt B · Struktur bestätigen", "Checkpoint B · Confirm the structure")}
<p class="lead">{t("So würde der Agent Ihren Ablauf in openBIS abbilden. Bitte lesen Sie die Seite von oben nach unten. "
                   "Zuerst wählen Sie die Variante, danach bei jedem Teil <b>passt</b> oder <b>ändern</b>. Ganz unten entsteht daraus Ihr Text für den Chat.",
                   "This is how the agent would map your workflow in openBIS. Please read the page from top to bottom. "
                   "First choose the variant, then <b>fits</b> or <b>change</b> for each part. At the bottom this becomes your reply for the chat.")}</p>
<ol class="ask">{"<li>" + t("Passt die empfohlene Variante, oder soll es eine andere werden?", "Does the recommended variant fit, or should it be a different one?") + "</li>" if d.get("variants") else ""}<li>{t("Hat jeder Ablaufschritt genau einen Ort?", "Does every workflow step have exactly one place?")}</li>
<li>{t("Sind die Felder die, die im Labor wirklich notiert werden?", "Are these the fields that are actually recorded in the lab?")}</li>
<li>{t("Würden Sie die Serientabelle so lesen wollen?", "Would you want to read the series table like this?")}</li>
<li>{t("Passen die Begriffe auf Deutsch und auf Englisch?", "Are the terms right in German and in English?")}</li></ol>
<p class="names">{legend}</p>
<p class="meta">{t("Vorschlag vom", "Proposal of")} {E((d.get("designed_at") or "")[:10])} · {t("Projekt", "Project")} <code>{E(m.project["name"])}</code></p></header>"""
    return "\n".join([header, *body])


def copy_block(cid: str, text: str, label_de: str, label_en: str) -> str:
    return (f'<div class="copyblock"><div class="cb-head"><b>{te(label_de, label_en)}</b>'
            f'<button type="button" data-copy="#{cid}">{t("Kopieren", "Copy")}</button></div>'
            f'<pre id="{cid}" class="out">{E(text)}</pre></div>')


def view_antrag(m: Model) -> str:
    r = m.request
    if not r:
        return (f'<header class="hero">{hero_top(m, "Prüfpunkte C und D", "Checkpoints C and D")}<p class="lead">'
                f'{t("Noch kein Antragspaket. Der Agent erzeugt es mit <code>python tools/build_request.py " + E(m.project["name"]) + "</code>.", "No request package yet. The agent creates it with <code>python tools/build_request.py " + E(m.project["name"]) + "</code>.")}'
                f'</p></header>')
    tname = {x["code"]: Name(x.get("name_de"), x.get("name_en")) for x in r["new_types"]}
    body = []
    n_ext = sum(len(e["terms"]) for e in r["extensions"])
    sync = r.get("sync")
    tiles = "".join(f'<div class="tile"><span>{te(a, b)}</span><b>{E(str(n))}</b></div>' for a, b, n in (
        ("neue Objekttypen", "new object types", len(r["new_types"])), ("neue Felder", "new fields", len(r["new_properties"])),
        ("neue Auswahllisten", "new choice lists", len(r["new_vocabularies"])), ("ergänzte Begriffe", "added terms", n_ext)))
    tiles += (f'<div class="tile"><span>{t("Admin zieht nach", "Admin syncs")}</span><b>{len(sync)}</b></div>' if sync is not None else
              f'<div class="tile"><span>{t("Admin zieht nach", "Admin syncs")}</span><b>?</b><small>{t("Instanz noch nicht gelesen", "instance not read yet")}</small></div>')
    body.append(f'<section aria-labelledby="a0">{section_head("1", "a0", "Das beantragen Sie", "What you request")}'
                f'<p>{t("Nur was es im BAM-Standard noch nicht gibt, wird beantragt. Alles andere wird wiederverwendet (Abschnitt 6).", "Only what does not exist in the BAM standard yet is requested. Everything else is reused (section 6).")}</p>'
                f'<div class="tiles">{tiles}</div></section>')

    # 2 new types
    cards = []
    for x in r["new_types"]:
        steps = ", ".join(x.get("covers_steps", []))
        cards.append(f'<article class="card obj"><header><div><h3>{tname[x["code"]].html()}</h3><code>{E(x["code"])}</code></div>'
                     f'{chip("neu", "new", "new")}</header>'
                     f'<p>{t(f"Baut auf dem Standard-Typ <b>{E(x.get("parent") or "")}</b> auf und übernimmt dessen Felder. "
                             f"{x["fields"]} Felder, davon {x["new_fields"]} neu. Ablaufschritte {E(steps)}.",
                             f"Builds on the standard type <b>{E(x.get("parent") or "")}</b> and inherits its fields. "
                             f"{x["fields"]} fields, {x["new_fields"]} of them new. Workflow steps {E(steps)}.")}</p></article>')
    body.append(f'<section aria-labelledby="a1">{section_head("2", "a1", "Neue Objekttypen", "New object types")}'
                f'<div class="cards">{"".join(cards)}</div>{feedback("typen", "Neue Objekttypen", "New object types")}</section>')

    # 3 new fields
    rows = []
    for p in r["new_properties"]:
        nm = m._note(Name(p.get("label_de"), p["label"]), f"p:{p['code']}")
        dt = p["data_type"]
        rows.append(f'<tr><td>{nm.html()}<br><code>{E(p["code"])}</code></td><td>{te(TYPE_DE.get(dt, dt), TYPE_EN.get(dt, dt))}</td>'
                    f'<td>{m.section_name(p.get("section") or "").html()}</td><td>{tname.get(p["type"], Name("", p["type"])).html()}</td>'
                    f'<td class="src">{E(p.get("source") or "")}</td></tr>')
    body.append(f'<section aria-labelledby="a2">{section_head("3", "a2", "Neue Felder", "New fields")}'
                f'<p>{t("Jedes Feld mit seinem Typ, dem Abschnitt im Formular und der Stelle im PRD, aus der es stammt.", "Each field with its type, its section in the form and the place in the PRD it comes from.")}</p>'
                f'<div class="tbl"><table class="tw"><thead><tr><th>{t("Feld", "Field")}</th><th>{t("Art", "Kind")}</th><th>{t("Abschnitt", "Section")}</th>'
                f'<th>{t("Objekttyp", "Object type")}</th><th>{t("Quelle", "Source")}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
                f'{feedback("felder", "Neue Felder", "New fields")}</section>')

    # 4 vocabularies and additions
    vc = []
    for v in r["new_vocabularies"]:
        en, dd = de(v.get("description"))
        terms = "".join(f'<li class="newt">{m.term_name(v["code"], x["code"]).html()}</li>' for x in v["terms"])
        vc.append(f'<article class="card voc"><header><div><h3>{m._note(Name(dd if "//" in (v.get("description") or "") else "", en), "v:" + v["code"]).html()}</h3>'
                  f'<code>{E(v["code"])}</code></div>{chip("neu", "new", "new")}</header><ul class="tlist">{terms}</ul></article>')
    for e in r["extensions"]:
        terms = "".join(f'<li class="newt">{m.term_name(e["vocabulary"], x["code"]).html()}</li>' for x in e["terms"])
        vc.append(f'<article class="card voc"><header><div><h3><code>{E(e["vocabulary"])}</code></h3>'
                  f'<span class="muted">{t("bestehende Liste, nur neue Begriffe", "existing list, new terms only")}</span></div>'
                  f'{chip("ergänzt", "new", "extended")}</header><ul class="tlist">{terms}</ul></article>')
    body.append(f'<section aria-labelledby="a3">{section_head("4", "a3", "Auswahllisten", "Choice lists")}'
                f'<div class="cards">{"".join(vc)}</div>{feedback("listen", "Auswahllisten", "Choice lists")}</section>')

    # 5 sync
    if sync is None:
        sync_html = t(f"Die Instanz <code>{E(r['instance'])}</code> ist noch nicht gelesen. Ob der Admin Standard-Typen nur nachziehen muss, "
                      f"zeigt sich nach dem Lesen (Schritt 3). Der Antrag kann trotzdem schon raus.",
                      f"The instance <code>{E(r['instance'])}</code> has not been read yet. Whether the admin only needs to sync standard types "
                      f"shows after reading it (step 3). The request can go out anyway.")
    elif not sync:
        sync_html = te("Nichts: Alles, was aus dem Standard genutzt wird, ist auf der Instanz vorhanden.", "Nothing: everything used from the standard exists on the instance.")
    else:
        sync_html = "<ul>" + "".join(f"<li><code>{E(x['what'])}</code> ({E(x['kind'])})</li>" for x in sync) + "</ul>"
    body.append(f'<section aria-labelledby="a4">{section_head("5", "a4", "Was der Admin nur nachziehen muss", "What the admin only needs to sync")}'
                f'<p>{t("Das gibt es im BAM-Standard schon, auf der Instanz aber noch nicht. Dafür braucht es keinen neuen Typ.", "This exists in the BAM standard but not yet on the instance. No new type is needed for it.")}</p>'
                f'<div class="card">{sync_html}</div></section>')

    # 6 reused
    reused = sorted({x["code"] for x in r["reused_types"]}) + sorted(x["code"] for x in r["reused_properties"])
    body.append(f'<section aria-labelledby="a5">{section_head("6", "a5", "Was wiederverwendet wird", "What is reused")}'
                f'<p>{t("Diese Typen und Felder gibt es im Standard schon. Sie werden nicht beantragt.", "These types and fields already exist in the standard. They are not requested.")}</p>'
                f'<div class="chips">{"".join(chip(c, "dev") for c in reused)}</div></section>')

    # 7 checks
    ck = r.get("checker") or {}
    if ck.get("ran"):
        inh = [w for w in ck.get("warning_texts", []) if any(x in w for x in ("$ANNOTATIONS_STATE", "same properties defined as EXPERIMENTAL_STEP"))]
        own = [w for w in ck.get("warning_texts", []) if w not in inh]
        check_html = (f'<p><b>{ck["errors"]}</b> {t("Fehler", "errors")} · <b>{ck["warnings"]}</b> {t("Warnungen", "warnings")}'
                      f'{" · " + t("alle Warnungen stammen aus dem BAM-Standard selbst", "all warnings come from the BAM standard itself") if not own else ""}</p>'
                      + ("<ul>" + "".join(f"<li>{E(w)}</li>" for w in own) + "</ul>" if own else ""))
    else:
        check_html = te("Der checker ist für diesen Entwurf nicht gelaufen.", "The checker has not run for this draft.")
    body.append(f'<section aria-labelledby="a6">{section_head("7", "a6", "Automatische Prüfung", "Automatic check")}'
                f'<p>{t("Der checker von bam-masterdata prüft Codes, Beschreibungen und Sektionen nach den BAM-Regeln.", "The bam-masterdata checker validates codes, descriptions and sections against the BAM rules.")}</p>'
                f'<div class="card">{check_html}</div>'
                f'{feedback("begriffe", "Begriffe Deutsch / Englisch", "Terms German / English")}</section>')

    # answer C
    body.append(f"""<section aria-labelledby="h7s" class="answer" data-gate="C"><h2 id="h7s"><span class="n">✓</span>{t("Ihre Antwort an den Agenten", "Your reply to the agent")}</h2>
<label for="fb-gesamt">{t("Noch etwas Allgemeines? (freiwillig)", "Anything else? (optional)")}</label><textarea id="fb-gesamt" rows="3"></textarea>
<p id="state" class="state"></p><pre id="out" class="out" aria-live="polite"></pre>
<button type="button" data-copy="#out" class="primary">{t("Text kopieren", "Copy text")}</button>
<p class="hint">{t("Den kopierten Text fügen Sie im Chat mit dem Agenten ein. Die Seite speichert nichts und schickt nichts ab.",
                   "Paste the copied text into the chat with the agent. The page stores nothing and sends nothing.")}</p></section>""")

    # send (D)
    issue = (m.request_dir / "issue.md").read_text(encoding="utf-8") if (m.request_dir / "issue.md").exists() else ""
    mail = (m.request_dir / "mail.txt").read_text(encoding="utf-8") if (m.request_dir / "mail.txt").exists() else ""
    title = next((re.sub(r"^<!--\s*Title:\s*|\s*-->$", "", ln) for ln in issue.splitlines() if ln.startswith("<!-- Title:")), "")
    issue_body = "\n".join(ln for ln in issue.splitlines() if not ln.startswith("<!--")).strip()
    mail_lines = mail.splitlines()
    to = mail_lines[0].split(":", 1)[1].strip() if mail_lines and mail_lines[0].startswith("An:") else "datastore@bam.de"
    subject = mail_lines[1].split(":", 1)[1].strip() if len(mail_lines) > 1 and mail_lines[1].startswith("Betreff:") else ""
    mail_body = "\n".join(mail_lines[3:]).strip() if subject else mail
    xlsx = f"projects/{m.project['name']}/request/masterdata.xlsx"
    new_issue = "https://github.com/BAMresearch/bam-masterdata/issues/new?title=" + __import__("urllib.parse").parse.quote(title)
    body.append(f"""<section aria-labelledby="a8" id="send" class="send locked">{section_head("D", "a8", "Antrag senden", "Send the request")}
<p class="locked-msg">{t("Dieser Teil öffnet sich, wenn oben alle Teile mit <b>passt</b> bestätigt sind.", "This part opens once every part above is confirmed with <b>fits</b>.")}</p>
<div class="send-body"><ol class="sendsteps">
<li><b>{t("Issue anlegen", "Create the issue")}</b> · <a href="{E(new_issue)}" target="_blank" rel="noopener">{t("neues Issue bei bam-masterdata öffnen", "open a new issue at bam-masterdata")}</a>
{t(" (Titel ist schon eingetragen). Text einfügen, die Excel-Datei anhängen, absenden.", " (title already filled in). Paste the text, attach the Excel file, submit.")}
{copy_block("c-title", title, "Titel", "Title")}{copy_block("c-issue", issue_body, "Text des Issues (englisch)", "Issue text (English)")}
<p class="hint">{t("Excel-Datei im Repo:", "Excel file in the repository:")} <code>{E(xlsx)}</code></p></li>
<li><b>{t("Mail schreiben", "Write the mail")}</b> · {t("an", "to")} <code class="sel">{E(to)}</code>. {t("Den Issue-Link anstelle von &lt;Issue-Link&gt; einsetzen.", "Replace &lt;Issue-Link&gt; with the issue link.")}
{copy_block("c-subject", subject, "Betreff", "Subject")}{copy_block("c-mail", mail_body, "Text der Mail (deutsch)", "Mail text (German)")}</li>
<li><b>{t("Dem Agenten Bescheid geben", "Tell the agent")}</b>
<label for="issue-url">{t("Link des Issues", "Link of the issue")}</label><input id="issue-url" type="url" placeholder="https://github.com/BAMresearch/bam-masterdata/issues/…">
<pre id="out-d" class="out"></pre><button type="button" data-copy="#out-d" class="primary">{t("Text kopieren", "Copy text")}</button></li>
</ol></div></section>""")

    n = len(m.missing)
    header = f"""<header class="hero">{hero_top(m, "Prüfpunkte C und D · Antrag prüfen und senden", "Checkpoints C and D · Review and send the request")}
<p class="lead">{t("Das geht an den BAM Data Store: ein Issue bei bam-masterdata und eine Mail an datastore@bam.de. Prüfen Sie zuerst, "
                   "ob nur beantragt wird, was es wirklich noch nicht gibt. Danach öffnet sich unten der Teil zum Senden.",
                   "This goes to the BAM Data Store: an issue at bam-masterdata and a mail to datastore@bam.de. First check that only "
                   "what really does not exist yet is requested. Then the sending part opens at the bottom.")}</p>
<ol class="ask"><li>{t("Ist jeder neue Typ wirklich nötig, oder reicht ein vorhandener mit ein, zwei Feldern mehr?", "Is every new type really needed, or would an existing one with one or two more fields do?")}</li>
<li>{t("Stimmen Feldnamen, Einheiten und Auswahlbegriffe, auf Deutsch und auf Englisch?", "Are field names, units and choice terms right, in German and in English?")}</li>
<li>{t("Ist der Antrag so kurz wie möglich?", "Is the request as short as possible?")}</li></ol>
<p class="names">{t(f"Alle Namen stehen als <b>Deutsch</b> / Englisch. {chip('DE fehlt', 'miss', 'DE missing')} = deutsche Fassung fehlt ({n if n else 'hier keine'}).",
                      f"All names are shown as <b>German</b> / English. {chip('DE fehlt', 'miss', 'DE missing')} = German version missing ({n if n else 'none here'}).")}</p>
<p class="meta">{t("Stand", "State")}: bam-masterdata {E(r.get("bam_masterdata") or "")} · {t("Projekt", "Project")} <code>{E(m.project["name"])}</code></p></header>"""
    return "\n".join([header, *body])


# --------------------------------------------------------------------------------------------
# page

# --------------------------------------------------------------------------------------------
# view: prd (Prüfpunkt A)


def _inline(text: str) -> str:
    """Markdown inline -> HTML (escaped): **bold**, *italic*, `code`, [text](url)."""
    s = E(text)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def md_blocks(text: str) -> list[tuple]:
    """Small, fixed Markdown reader: ('p', text), ('ul'|'ol', [items]), ('table', head, rows), ('quote', text), ('h', text)."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip() or re.match(r"^-{3,}$", ln.strip()):
            i += 1
            continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            head, rows, i = _cells(ln), [], i + 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(_cells(lines[i]))
                i += 1
            out.append(("table", head, rows))
            continue
        if re.match(r"^#{3,6}\s", ln):
            out.append(("h", ln.lstrip("#").strip()))
            i += 1
            continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append(("quote", " ".join(buf)))
            continue
        m_ = re.match(r"^\s*([-*]|\d+\.)\s+", ln)
        if m_:
            kind, items = ("ol" if m_.group(1)[0].isdigit() else "ul"), []
            while i < len(lines) and (re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) or
                                      (lines[i].startswith("   ") and lines[i].strip() and items)):
                if re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                    items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i]).strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            items = [x for x in items if x]
            if items:
                out.append((kind, items))
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(("|", ">", "#")) \
                and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append(("p", " ".join(buf)))
    return out


def blocks_html(blocks: list[tuple]) -> str:
    parts = []
    for b in blocks:
        if b[0] == "p":
            parts.append(f"<p>{_inline(b[1])}</p>")
        elif b[0] == "h":
            parts.append(f"<h3>{_inline(b[1])}</h3>")
        elif b[0] == "quote":
            parts.append(f'<p class="muted">{_inline(b[1])}</p>')
        elif b[0] in ("ul", "ol"):
            parts.append(f"<{b[0]} class=\"plist\">" + "".join(f"<li>{_inline(x)}</li>" for x in b[1]) + f"</{b[0]}>")
        else:
            head = "".join(f"<th>{_inline(h)}</th>" for h in b[1])
            rows = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in b[2])
            parts.append(f'<div class="tbl"><table class="tw"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
    return "".join(parts)


def split_top(cell: str) -> list[str]:
    """'a, b (x, y), c' -> ['a', 'b (x, y)', 'c']; '–' -> []."""
    out, depth, cur = [], 0, ""
    for ch in cell:
        depth += ch in "([" ; depth -= ch in ")]"
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return [x for x in out if x and x not in ("–", "-", "—")]


def prd_sections(m: Model) -> tuple[str, list[dict]]:
    """(title, [{'no', 'title', 'blocks', 'steps'}]) from prd.md; '## N. Title' starts a section."""
    text = m.prd_text
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), "")
    secs, cur = [], None
    for ln in text.splitlines():
        h = re.match(r"^##\s+(?:(\d+)\.\s*)?(.+)$", ln)
        if h:
            cur = {"no": h.group(1) or str(len(secs) + 1), "title": h.group(2).strip(), "body": []}
            secs.append(cur)
        elif cur is not None:
            cur["body"].append(ln)
    for s in secs:
        s["blocks"] = md_blocks("\n".join(s["body"]))
        s["steps"] = []
        for b in s["blocks"]:
            if b[0] == "table" and len(b[1]) >= 2 and re.match(r"^(nr|no)\.?$", b[1][0].strip().lower()) \
                    and "schritt" in b[1][1].lower():
                cols = [h.lower() for h in b[1]]
                pick = lambda r, key: next((r[i] for i, c in enumerate(cols) if key in c and i < len(r)), "")
                s["steps"] = [{"no": r[0], "name": r[1] if len(r) > 1 else "", "data": pick(r, "daten"),
                               "equipment": split_top(pick(r, "ger")), "files": split_top(pick(r, "datei"))}
                              for r in b[2] if any(c.strip() for c in r)]
    return title, secs


PRD_HINT_TYPES = re.compile(r"\b(?:EXPERIMENTAL_STEP|SAMPLE|INSTRUMENT|COLLECTION)(?:\.[A-Z_]+)*\b|\b[A-Z][A-Z0-9_]+\.[A-Z][A-Z0-9_.]+\b")


def prd_hints(m: Model, secs: list[dict]) -> list[tuple[str, str]]:
    """Things the agent points out (not blocking): names without English, openBIS type names, open points."""
    hints = []
    steps = [st for s in secs for st in s["steps"]]
    mono = [st["no"] for st in steps if " / " not in st["name"]]
    if mono:
        hints.append((f"Schrittnamen wohl ohne englische Fassung („Deutsch / Englisch“): {', '.join(mono)}",
                      f"Step names probably without an English version (“German / English”): {', '.join(mono)}"))
    codes = sorted(set(PRD_HINT_TYPES.findall(m.prd_text)))
    if codes:
        hints.append((f"Das PRD nennt schon openBIS-Codes ({', '.join(codes[:6])}{' …' if len(codes) > 6 else ''}). Das ist erlaubt, wenn es eine fachliche Vorgabe ist; sonst entscheidet das erst Schritt 4/5.",
                      f"The PRD already names openBIS codes ({', '.join(codes[:6])}{' …' if len(codes) > 6 else ''}). That is fine if it is a domain requirement; otherwise steps 4/5 decide."))
    for s in secs:
        if re.search(r"offen|später|open", s["title"], re.I):
            items = [x for b in s["blocks"] if b[0] in ("ul", "ol") for x in b[1]]
            if items:
                hints.append((f"Noch offen ({len(items)}): " + "; ".join(items), f"Still open ({len(items)}): " + "; ".join(items)))
    return hints


def view_prd(m: Model) -> str:
    if not m.prd_text:
        return (f'<header class="hero">{hero_top(m, "Prüfpunkt A · Anforderungen freigeben", "Checkpoint A · Approve the requirements")}'
                f'<p class="lead">{t("Noch kein PRD. Der Agent schreibt es im Interview (Schritt 2).", "No PRD yet. The agent writes it in the interview (step 2).")}</p></header>')
    _, secs = prd_sections(m)
    body = []
    steps = [st for s in secs for st in s["steps"]]
    n_files = sum(len(st["files"]) for st in steps)
    n_dev = len({e for st in steps for e in st["equipment"]})
    tiles = "".join(f'<div class="tile"><span>{te(a, b)}</span><b>{n}</b></div>' for a, b, n in (
        ("Ablaufschritte", "workflow steps", len(steps)), ("Geräte und Material", "instruments and materials", n_dev),
        ("Dateien", "files", n_files), ("Abschnitte", "sections", len(secs))))
    hints = prd_hints(m, secs)
    hint_html = ("<ul class=\"plist hints\">" + "".join(f"<li>{te(a, b)}</li>" for a, b in hints) + "</ul>") if hints else \
        f'<p>{t("Keine Auffälligkeiten.", "Nothing stands out.")}</p>'
    body.append(f'<section aria-labelledby="pa0">{section_head("✓", "pa0", "Auf einen Blick", "At a glance")}<div class="tiles">{tiles}</div>'
                f'<h3>{t("Hinweise des Agenten", "Notes from the agent")}</h3>{hint_html}</section>')
    for s in secs:
        sid = f"pa{s['no']}"
        if s["steps"]:
            rows = "".join(f"""<li class="step test"><span class="no">{E(st['no'])}</span><div class="s-body"><h3>{_inline(st['name'])}</h3>
{'<p class="items">' + _inline(st['data']) + '</p>' if st['data'] and st['data'] not in ('–', '-') else ''}
<div class="chips">{''.join(chip(short(e, 60), 'dev') for e in st['equipment'])}{''.join(chip(short(f, 60), 'file') for f in st['files'])}</div></div></li>"""
                           for st in s["steps"])
            other = [b for b in s["blocks"] if not (b[0] == "table" and b[1] and re.match(r"^(nr|no)\.?$", b[1][0].strip().lower()))]
            content = f'{blocks_html(other)}<ol class="timeline">{rows}</ol>'
        else:
            content = blocks_html(s["blocks"])
        body.append(f'<section aria-labelledby="{sid}">{section_head(E(s["no"]), sid, s["title"], s["title"])}{content}'
                    f'{feedback("prd-" + s["no"], s["title"], s["title"])}</section>')
    body.append(answer_section("A"))
    header = f"""<header class="hero">{hero_top(m, "Prüfpunkt A · Anforderungen freigeben", "Checkpoint A · Approve the requirements")}
<p class="lead">{t("Das hat der Agent aus dem Interview aufgeschrieben (PRD). Daraus entsteht später die Struktur in openBIS. "
                   "Bitte lesen Sie jeden Abschnitt und wählen Sie <b>passt</b> oder <b>ändern</b>. Ganz unten entsteht daraus Ihr Text für den Chat.",
                   "This is what the agent wrote down from the interview (PRD). The structure in openBIS is built from it later. "
                   "Please read each section and choose <b>fits</b> or <b>change</b>. At the bottom this becomes your reply for the chat.")}</p>
<ol class="ask"><li>{t("Fehlt ein Ablaufschritt, oder ist die Reihenfolge falsch?", "Is a workflow step missing, or is the order wrong?")}</li>
<li>{t("Hat jeder Messwert Einheit oder Auswahlliste und die Angabe, ob er Pflicht ist?", "Does every value have a unit or a choice list and whether it is mandatory?")}</li>
<li>{t("Stehen alle Geräte und Dateien dabei?", "Are all instruments and files listed?")}</li>
<li>{t("Sind die fachlichen Entscheidungen richtig wiedergegeben?", "Are the domain decisions stated correctly?")}</li></ol>
<p class="names">{t("Der Text der Abschnitte steht so im PRD, wie er mit Ihnen erarbeitet wurde (meist auf Deutsch).",
                      "The section text is shown as written in the PRD with you (mostly in German).")}</p>
<p class="meta">{t("Datei", "File")} <code>{E(m.prd_rel)}</code> · {t("Projekt", "Project")} <code>{E(m.project["name"])}</code></p></header>"""
    return "\n".join([header, *body])


def answer_section(gate: str, block_de: str = "", block_en: str = "") -> str:
    """block: why this checkpoint cannot be approved yet (the reply then says so instead of '<gate> freigegeben')."""
    blk = f' data-block-de="{E(block_de)}" data-block-en="{E(block_en)}"' if block_de else ""
    return f"""<section aria-labelledby="hans" class="answer" data-gate="{gate}"{blk}><h2 id="hans"><span class="n">✓</span>{t("Ihre Antwort an den Agenten", "Your reply to the agent")}</h2>
<label for="fb-gesamt">{t("Noch etwas Allgemeines? (freiwillig)", "Anything else? (optional)")}</label><textarea id="fb-gesamt" rows="3"></textarea>
<p id="state" class="state"></p>
<pre id="out" class="out" aria-live="polite"></pre>
<button type="button" data-copy="#out" class="primary">{t("Text kopieren", "Copy text")}</button>
<p class="hint">{t("Den kopierten Text fügen Sie im Chat mit dem Agenten ein. Die Seite speichert nichts und schickt nichts ab.",
                   "Paste the copied text into the chat with the agent. The page stores nothing and sends nothing.")}</p></section>"""


# --------------------------------------------------------------------------------------------
# view: trockenlauf (Prüfpunkt E)

KIND_DE = {"object type": ("Objekttyp", "object type"), "property type": ("Feld", "field"), "assignment": ("Feld am Typ", "field on type"),
           "vocabulary": ("Auswahlliste", "choice list"), "term": ("Begriff", "term"), "collection type": ("Collection-Typ", "collection type"),
           "mandatory field": ("Pflichtfeld leer", "mandatory field empty"), "equipment": ("Gerät fehlt im Inventar", "instrument missing in inventory"),
           "structure": ("structure.json", "structure.json")}
WHO_DE = {"admin": ("Admin (Antrag, Schritt 6)", "admin (request, step 6)"), "you": ("Sie (Inventar)", "you (inventory)"),
          "agent": ("Agent (structure.json)", "agent (structure.json)")}


def newest(pdir: Path, kind: str) -> tuple[dict | None, str]:
    files = sorted((pdir / "reports").glob(f"{kind}_*.json"))
    return (ob.read_json(files[-1]), files[-1].name) if files else (None, "")


class DryRun:
    """Plan of step 8: structure.json plus the newest check and dry-run reports from the bridge."""

    def __init__(self, m: Model):
        pdir = m.project["dir"]
        self.check, self.check_file = newest(pdir, "check")
        self.plan, self.plan_file = newest(pdir, "dryrun")
        st = m.structure or {}
        try:
            self.objs = ob._resolve(st) if st else []
        except ValueError:
            self.objs = []
        created = {x.upper() for x in (self.plan or {}).get("created", [])}
        skipped = {x.upper() for x in (self.plan or {}).get("skipped", [])}
        self.status = lambda ident: ("neu" if ident.upper() in created else "da" if ident.upper() in skipped else "?")
        self.space = st.get("space", "")
        self.project = (st.get("project") or {}).get("code", "")
        self.collections = st.get("collections", [])
        self.dropped = (self.plan or {}).get("droppedProps", [])
        self.missing = (self.check or {}).get("missing", [])
        self.warnings = (self.check or {}).get("warnings", [])
        self.instance = (self.check or {}).get("instance") or m.project.get("instance") or ""


def type_label(m: Model, code: str) -> Name:
    dt = next((x for x in m.design.get("object_types", []) if x["code"] == code), None)
    if dt:
        return Name(dt.get("name_de"), dt.get("name_en"))
    ct = next((x for x in m.catalog.get("types", []) if x["code"] == code), None)
    desc = ((ct or {}).get("defs") or {}).get("description") or ""
    if "//" in desc:
        en, d = de(desc)
        return Name(d, en, "std")
    return Name("", code, "std")


def status_chip(s: str) -> str:
    return {"neu": chip("wird angelegt", "new", "will be created"), "da": chip("schon da", "std", "exists"),
            "?": chip("noch nicht geprüft", "must", "not checked yet")}[s]


def view_trockenlauf(m: Model) -> str:
    r = DryRun(m)
    body = []
    num = iter(str(i) for i in range(1, 10))
    n_new = len((r.plan or {}).get("created", []))
    n_have = len((r.plan or {}).get("skipped", []))
    tiles = "".join(f'<div class="tile"><span>{te(a, b)}</span><b>{v}</b></div>' for a, b, v in (
        ("wird angelegt", "will be created", n_new if r.plan else "?"), ("schon da", "exists already", n_have if r.plan else "?"),
        ("fehlt noch (Prüfung)", "still missing (check)", len(r.missing) if r.check else "?"),
        ("Felder kommen nicht an", "fields not stored", len(r.dropped) if r.plan else "?")))
    where = (f'<dl class="kv"><dt>{t("Instanz", "Instance")}</dt><dd><code>{E(r.instance)}</code></dd>'
             f'<dt>Space</dt><dd><code>{E(r.space)}</code></dd><dt>{t("Projekt", "Project")}</dt><dd><code>/{E(r.space)}/{E(r.project)}</code></dd>'
             f'<dt>Collections</dt><dd>{"<br>".join(E((c.get("props") or {}).get("$NAME") or c["code"]) + " <code>" + E(c["code"]) + "</code>" for c in r.collections)}</dd></dl>')
    if not r.plan:
        state = t(f"Noch kein Trockenlauf im Repo. Aufgabe für Sie im BAM-Netz: <code>python tools/bruecke.py {E(m.project['name'])} trockenlauf</code> "
                  "(oder Teil 2 und 3 im Notebook). Bis dahin zeigt die Seite nur den Plan aus <code>structure.json</code>.",
                  f"No dry run in the repository yet. Your task in the BAM network: <code>python tools/bruecke.py {E(m.project['name'])} trockenlauf</code> "
                  "(or parts 2 and 3 in the notebook). Until then the page only shows the plan from <code>structure.json</code>.")
    elif r.missing:
        state = t("Die Prüfung meldet Lücken. So lange legt die Brücke nichts an; zuerst die Lücken unten schließen.",
                  "The check reports gaps. Until they are closed the bridge creates nothing; close the gaps below first.")
    else:
        state = t("Die Prüfung meldet keine Lücken. Nach Ihrer Freigabe legt die Brücke genau das an, was unten als „wird angelegt“ steht.",
                  "The check reports no gaps. After your approval the bridge creates exactly what is marked “will be created” below.")
    body.append(f'<section aria-labelledby="e1">{section_head(next(num), "e1", "Wohin wird geschrieben?", "Where will it be written?")}'
                f'<p class="vnote">{state}</p><div class="tiles">{tiles}</div>{where}'
                f'{feedback("ziel", "Instanz, Space und Projekt", "Instance, space and project")}</section>')

    # 2 gaps
    if r.check:
        if r.missing:
            rows = "".join(f'<tr><td>{te(*KIND_DE.get(x["kind"], (x["kind"], x["kind"])))}</td><td><code>{E(x["what"])}</code></td>'
                           f'<td>{te(*WHO_DE.get(x["who"], (x["who"], x["who"])))}</td></tr>' for x in r.missing)
            gaps = (f'<div class="tbl"><table class="tw"><thead><tr><th>{t("Was", "What")}</th><th>Code</th><th>{t("Wer", "Who")}</th></tr></thead>'
                    f'<tbody>{rows}</tbody></table></div>')
        else:
            gaps = f'<p>{t("Keine Lücken: Typen, Felder, Auswahllisten und Geräte sind auf der Instanz vorhanden.", "No gaps: types, fields, choice lists and instruments exist on the instance.")}</p>'
        warn = ("<details><summary>" + t(f"Hinweise ({len(r.warnings)})", f"Notes ({len(r.warnings)})") + "</summary><ul class=\"plist\">"
                + "".join(f"<li><code>{E(w)}</code></li>" for w in r.warnings) + "</ul></details>") if r.warnings else ""
        body.append(f'<section aria-labelledby="e2">{section_head(next(num), "e2", "Was auf der Instanz noch fehlt", "What is still missing on the instance")}'
                    f'<p class="muted">{t("Prüfung", "Check")}: <code>reports/{E(r.check_file)}</code>, {t("Stand der Instanz", "instance as of")} {E(str(r.check.get("collected") or ""))}</p>'
                    f'{gaps}{warn}</section>')

    # 3 objects per collection
    groups: dict[str, list] = {}
    for o in r.objs:
        groups.setdefault(o.get("_experiment") or o.get("_project") or "", []).append(o)
    names = {o["key"]: ((o.get("props") or {}).get("$NAME") or o["code"]) for o in r.objs}
    blocks = []
    for coll, objs in groups.items():
        rows = []
        for o in objs:
            par = E(", ".join(names.get(p, p) for p in o.get("parents", [])))
            lk = ob.links(o)
            if lk:  # link fields (pattern M4): shown in the form, not in the graph
                par = (par + "<br>" if par else "") + t("Links: ", "Links: ") + E(", ".join(names.get(p, p) for p in lk))
            n_props = len([k for k in (o.get("props") or {}) if not k.startswith("$")])
            rows.append(f'<tr><td><b>{E(names[o["key"]])}</b><br><code>{E(o["code"])}</code></td><td>{type_label(m, o["type"]).html()}</td>'
                        f'<td>{par or "–"}</td><td>{n_props}</td><td>{status_chip(r.status(o["_identifier"]))}</td></tr>')
        blocks.append(f'<h3><code>{E(coll)}</code> <small>{t(f"{len(objs)} Objekte", f"{len(objs)} objects")}</small></h3>'
                      f'<div class="tbl"><table class="tw"><thead><tr><th>{t("Objekt", "Object")}</th><th>{t("Typ", "Type")}</th>'
                      f'<th>{t("Eltern", "Parents")}</th><th>{t("Felder", "Fields")}</th><th>Status</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    body.append(f'<section aria-labelledby="e3">{section_head(next(num), "e3", "Diese Objekte entstehen", "These objects are created")}'
                f'<p>{t("Aus <code>structure.json</code>, geordnet nach Collection. Eltern werden vor ihren Kindern angelegt; was schon da ist, bleibt unverändert.", "From <code>structure.json</code>, grouped by collection. Parents are created before their children; what exists already stays unchanged.")}</p>'
                f'{"".join(blocks) or "<p>" + t("Noch keine structure.json.", "No structure.json yet.") + "</p>"}'
                f'{feedback("objekte", "Objekte und Eltern", "Objects and parents")}</section>')

    # 4 dropped fields
    if r.plan:
        dr = ("<ul class=\"plist\">" + "".join(f"<li><code>{E(x)}</code></li>" for x in r.dropped) + "</ul>") if r.dropped else \
            f'<p>{t("Alle Werte kommen an.", "All values are stored.")}</p>'
        body.append(f'<section aria-labelledby="e4">{section_head(next(num), "e4", "Werte, die nicht gespeichert würden", "Values that would not be stored")}'
                    f'<p>{t("Felder, die der Typ auf der Instanz (noch) nicht hat. Die Brücke lässt sie weg, statt abzubrechen.", "Fields the type does not have on the instance (yet). The bridge leaves them out instead of failing.")}</p>'
                    f'{dr}<p class="muted">{t("Trockenlauf", "Dry run")}: <code>reports/{E(r.plan_file)}</code></p>'
                    f'{feedback("werte", "Fehlende Werte", "Missing values")}</section>')
    if not r.plan:
        body.append(answer_section("E", "Noch kein Trockenlauf im Repo: E kann noch nicht freigegeben werden.",
                                   "No dry run in the repository yet: E cannot be approved yet."))
    elif r.missing:
        body.append(answer_section("E", f"Die Prüfung meldet {len(r.missing)} Lücken: E kann erst danach freigegeben werden.",
                                   f"The check reports {len(r.missing)} gaps: E can only be approved after that."))
    else:
        body.append(answer_section("E"))
    header = f"""<header class="hero">{hero_top(m, "Prüfpunkt E · Trockenlauf freigeben", "Checkpoint E · Approve the dry run")}
<p class="lead">{t("Das würde die Brücke in openBIS anlegen. Der Trockenlauf hat noch nichts geschrieben. Erst nach Ihrer Freigabe "
                   "führen Sie <b>anlegen</b> aus.", "This is what the bridge would create in openBIS. The dry run has not written anything yet. "
                   "Only after your approval do you run <b>create</b>.")}</p>
<ol class="ask"><li>{t("Stimmen Instanz, Space und Projekt?", "Are instance, space and project right?")}</li>
<li>{t("Sind das die Objekte, die entstehen sollen, mit den richtigen Eltern?", "Are these the objects that should be created, with the right parents?")}</li>
<li>{t("Gehen keine wichtigen Werte verloren?", "Are no important values lost?")}</li></ol>
<p class="meta">{t("Projekt", "Project")} <code>{E(m.project["name"])}</code></p></header>"""
    return "\n".join([header, *body])


# --------------------------------------------------------------------------------------------
# Markdown versions (readable directly on GitHub, e.g. for Mistral Vibe). Same content, no buttons.


def md_esc(s) -> str:
    return str(s or "").replace("|", "\\|").replace("\n", " ")


def md_head(m: Model, gate_de: str, gate_en: str, view: str) -> list[str]:
    div = f"{m.division} · " if m.division else ""
    return [f"# {m.title_de} / {m.title_en}", "", f"**{div}{gate_de} / {gate_en}**", "",
            f"> Markdown-Fassung der Prüfseite. Mit Auswahl und Antworttext: `review/{view}.html` herunterladen und im Browser öffnen. "
            "Hier antworten Sie direkt im Chat. / Markdown version of the review page; for buttons and the reply text, "
            f"download `review/{view}.html` and open it in a browser. Here, reply directly in the chat.", ""]


def md_answer(gate: str, parts: list[str], extra: str = "") -> list[str]:
    return ["## Ihre Antwort / Your reply", "",
            f"Schreiben Sie im Chat „{gate} freigegeben“{extra} oder eine Liste der Änderungen, je Teil eine Zeile. / "
            f"Write “{gate} approved”{extra} in the chat, or a list of changes, one line per part.", "",
            "Teile / Parts: " + " · ".join(parts), ""]


def md_struktur(m: Model) -> str:
    d, lay = m.design, m.design.get("layout", {})
    L = md_head(m, "Prüfpunkt B · Struktur bestätigen", "Checkpoint B · Confirm the structure", "struktur")
    vs = d.get("variants") or []
    rec = next((v for v in vs if v.get("recommended")), vs[0] if vs else None)
    shown = d.get("variant") or (rec or {}).get("id")
    if vs:
        L += ["## 1 Welche Struktur soll es werden? / Which structure should it be?", "",
              f"Empfohlen / recommended: **{rec['id']}**. Unten ausgearbeitet / worked out below: **{shown}**. "
              "Muster und Quellen: `workflow/strukturmuster.md`.", "",
              f"| | Variante / Variant | Objekte je {m.main.de} | Ebenen | neue Typen | Geräte als Eltern |", "|---|---|---|---|---|---|"]
        for v in vs:
            tag = " **(empfohlen / recommended)**" if v is rec else ""
            L.append(f"| {v['id']} | {md_esc(v['name_de'])} / {md_esc(v['name_en'])}{tag} | {v.get('objects_per_specimen', '–')} | "
                     f"{v.get('max_link_depth', '–')} | {v.get('new_object_types', '–')} | {v.get('shared_parents', '–')} |")
        L.append("")
        for v in vs:
            nms = [o["name_de"] for o in v["objects"]]
            sketch = (" → ".join(nms) if v["shape"] == "chain" else
                      f"{nms[0]} ← " + " · ".join(nms[1:]) if v["shape"] == "flat" and len(nms) > 1 else nms[0])
            L += [f"### {v['id']} {v['name_de']} / {v['name_en']}{' (empfohlen / recommended)' if v is rec else ''}", "",
                  v["summary_de"], "", f"*{v['summary_en']}*", "", f"Aufbau / build-up: {sketch}", ""]
            L += [f"- ＋ {x['de']} / *{x['en']}*" for x in v["pros"]] + [f"- – {x['de']} / *{x['en']}*" for x in v["cons"]] + [""]
    objs = m.objects()
    L += ["## 2 So ist Ihr Projekt aufgebaut / How your project is built", "",
          f"`{lay.get('project', '')}` → " + ", ".join(f"{c.get('$NAME') or c['code']} (`{c['code']}`)" for c in lay.get("collections", [])), ""]
    for o in objs:
        prev = next((x["name"].text for x in objs if x["code_pattern"] == o["prev"]), "")
        devs = ", ".join(m.device_name(e).text for e in o["equipment"] + o["fields"])
        L.append(f"- **{o['name'].text}** `{o['code_pattern']}`" + (f" ← {prev}" if prev else "")
                 + (f" · Schritte / steps {step_range(o.get('covers_steps', []))}" if o.get("covers_steps") else "")
                 + (f" · {devs}" if devs else ""))
    L += ["", "## 3 Wo landet welcher Ablaufschritt? / Where does each workflow step go?", "",
          "| Nr. | Schritt / Step | Objekt / Object | Sektion / Section | Geräte, Dateien |", "|---|---|---|---|---|"]
    for s in d.get("step_location_map", []):
        o = m.object_for(s.get("object", ""))
        sec = s.get("section") if s.get("section") not in (None, "-") else ""
        secn = " + ".join(m.section_name(x.strip()).text for x in sec.split("+")) if sec else ""
        L.append(f"| {s.get('no')} | {md_esc(Name(s.get('step_de'), s.get('step')).text)} | {md_esc(o['name'].text if o else s.get('object'))} | "
                 f"{md_esc(secn)} | {md_esc(', '.join([m.device_name(e).text for e in s.get('equipment', [])] + [m.file_name(f).text for f in s.get('files', [])]))} |")
    L += ["", "## 4 Welche Felder bekommt jedes Objekt? / Which fields does each object get?", ""]
    for x in form_types(m):
        L += [f"### {m.type_name(x).text} (`{x['code']}`)", "", "| Sektion / Section | Feld / Field | Typ | Pflicht | neu |", "|---|---|---|---|---|"]
        for p in x.get("properties", []):
            if p["code"].startswith("$") and p["code"] != "$NAME":
                continue
            dt = p.get("data_type") or m.props.get(p["code"], {}).get("type")
            L.append(f"| {md_esc(m.section_name(p.get('section') or '').text)} | {md_esc(m.prop_name(p['code']).text)} | {TYPE_DE.get(dt, dt or '')} | "
                     f"{'ja' if p.get('mandatory') else ''} | {'neu' if p['code'] in m.new_codes else ''} |")
        L.append("")
    L += ["## 5 Serientabelle / Series table", "", "Spalten / columns: " + " · ".join(
        Name(de(c["column"])[1], de(c["column"])[0]).text for c in lay.get("series_table", [])), ""]
    L += ["## 6 Auswahllisten / Choice lists", ""]
    for code, v in m.vocab.items():
        if v["status"] == "standard":
            continue
        en, dd = de(v.get("description"))
        new = v.get("new_terms", set())
        L.append(f"- **{Name(dd, en).text}** (`{code}`, {'neu' if v['status'] == 'neu' else 'ergänzt / extended'}): "
                 + " · ".join(("**" + m.term_name(code, x["code"]).text + "**") if x["code"] in new else m.term_name(code, x["code"]).text
                              for x in v["terms"]))
    L.append("")
    L += md_answer("B", ["Variante", "Aufbau", "Zuordnung der Schritte", "Felder je Objekt", "Serientabelle", "Auswahllisten", "Begriffe"],
                   f" (Variante {rec['id'] if rec else ''})" if vs else "")
    return "\n".join(L)


def md_antrag(m: Model) -> str:
    r = m.request
    L = md_head(m, "Prüfpunkte C und D · Antrag prüfen und senden", "Checkpoints C and D · Review and send the request", "antrag")
    if not r:
        return "\n".join(L + [f"Noch kein Antragspaket: `python tools/build_request.py {m.project['name']}`.", ""])
    L += ["## Das beantragen Sie / What you request", "",
          f"- neue Objekttypen / new object types: {len(r['new_types'])}", f"- neue Felder / new fields: {len(r['new_properties'])}",
          f"- neue Auswahllisten / new choice lists: {len(r['new_vocabularies'])}",
          f"- ergänzte Begriffe / added terms: {sum(len(e['terms']) for e in r['extensions'])}", "",
          "## Neue Objekttypen / New object types", ""]
    L += [f"- **{Name(x.get('name_de'), x.get('name_en')).text}** (`{x['code']}`)" for x in r["new_types"]] + [""]
    L += ["## Neue Felder / New fields", "", "| Code | Name | Typ |", "|---|---|---|"]
    for p in r["new_properties"]:
        L.append(f"| `{p.get('code')}` | {md_esc(Name(p.get('label_de'), p.get('label')).text)} | {md_esc(p.get('data_type'))} |")
    L += ["", f"Dateien zum Senden / files to send: `request/issue.md`, `request/mail.txt`, `request/masterdata.xlsx`.", ""]
    L += md_answer("C", ["neue Typen", "neue Felder", "Auswahllisten", "Wiederverwendung"])
    L += ["Nach dem Senden / after sending: „D gesendet: <Link des Issues>“.", ""]
    return "\n".join(L)


def md_prd(m: Model) -> str:
    L = md_head(m, "Prüfpunkt A · Anforderungen freigeben", "Checkpoint A · Approve the requirements", "prd")
    if not m.prd_text:
        return "\n".join(L + ["Noch kein PRD (Schritt 2).", ""])
    _, secs = prd_sections(m)
    hints = prd_hints(m, secs)
    L += ["## Hinweise des Agenten / Notes from the agent", ""] + ([f"- {a}" for a, _ in hints] or ["- keine / none"]) + [""]
    L += [f"Den vollständigen Text lesen Sie in `{m.prd_rel}`. Abschnitte / sections:", ""]
    L += [f"{s['no']}. {s['title']}" + (f" ({len(s['steps'])} Schritte)" if s["steps"] else "") for s in secs] + [""]
    L += md_answer("A", [s["title"] for s in secs])
    return "\n".join(L)


def md_trockenlauf(m: Model) -> str:
    r = DryRun(m)
    L = md_head(m, "Prüfpunkt E · Trockenlauf freigeben", "Checkpoint E · Approve the dry run", "trockenlauf")
    if not r.plan:
        L += [f"**Noch kein Trockenlauf.** Im BAM-Netz: `python tools/bruecke.py {m.project['name']} trockenlauf`. "
              "Bis dahin nur der Plan aus `structure.json`. / No dry run yet; only the plan from `structure.json`.", ""]
    L += ["## Wohin / Where", "", f"- Instanz / instance: `{r.instance}`", f"- Projekt / project: `/{r.space}/{r.project}`",
          "- Collections: " + ", ".join(f"`{c['code']}`" for c in r.collections), ""]
    if r.check:
        L += [f"## Was noch fehlt / Still missing ({len(r.missing)})", ""]
        L += [f"- {KIND_DE.get(x['kind'], (x['kind'],))[0]}: `{x['what']}` – {WHO_DE.get(x['who'], (x['who'],))[0]}" for x in r.missing] or ["- nichts / nothing"]
        L.append("")
    L += ["## Objekte / Objects", "", "| Objekt | Typ | Eltern / Parents | Status |", "|---|---|---|---|"]
    names = {o["key"]: ((o.get("props") or {}).get("$NAME") or o["code"]) for o in r.objs}
    st = {"neu": "wird angelegt", "da": "schon da", "?": "noch nicht geprüft"}
    for o in r.objs:
        L.append(f"| {md_esc(names[o['key']])} `{o['code']}` | {md_esc(type_label(m, o['type']).text)} | "
                 f"{md_esc(', '.join(names.get(p, p) for p in o.get('parents', [])) or '–')} | {st[r.status(o['_identifier'])]} |")
    if r.plan:
        L += ["", f"## Werte, die nicht gespeichert würden / Values not stored ({len(r.dropped)})", ""] + \
             ([f"- `{x}`" for x in r.dropped] or ["- keine / none"])
    L += [""] + md_answer("E", ["Instanz, Space und Projekt", "Objekte und Eltern", "Fehlende Werte"])
    return "\n".join(L)


CSS = """
/* BAM Design System (00_BAM_Design_System): Petrol #002832 für Überschriften und dunkle Flächen, Cyan #00AFF0 als einziger
   Akzent, Rot nur für Warnungen; BAM-Hausschrift Klavika (lokal installiert), Barlow als Web-Ersatz; eckig, Pillen nur für Tags; nur heller Modus.
   Objektfarben (Reihenfolge der Objekte je Hauptobjekt): 1 Petrol (gefüllt), 2 Steel, 3 Cyan, 4 Grau, weitere Grau */
:root{color-scheme:light;
--bam-petrol:#002832;--bam-cyan:#00aff0;--bam-steel:#00556a;--bam-red:#d2001f;--cyan-tint:#e0f5fd;--petrol-tint:#e6ebec;
--gray-1:#f4f7f8;--gray-2:#e6ebec;--gray-3:#c9d3d6;--gray-4:#9fadb2;--gray-5:#66787f;
--bg:var(--gray-1);--paper:#ffffff;--fg:#1c343c;--head:var(--bam-petrol);--muted:var(--gray-5);--line:var(--gray-3);
--accent:var(--bam-cyan);--accent-strong:#0079ab;--success:#1e7d5a;--warning:#b96a00;
--probe:var(--bam-petrol);--probe-bg:var(--bam-petrol);--scan:var(--bam-steel);--scan-bg:#e3eef1;
--test:var(--accent-strong);--test-bg:var(--cyan-tint);--fracture:var(--gray-5);--fracture-bg:var(--gray-2);--extra:var(--gray-5);--extra-bg:var(--gray-2);
--shadow-card:0 1px 3px rgba(0,40,50,.10),0 4px 16px rgba(0,40,50,.08);
--f:"BAM Klavika Light","Klavika Light","BAM Klavika","Klavika","Barlow",system-ui,"Segoe UI",sans-serif;--fh:"BAM Klavika Medium","Klavika Medium","BAM Klavika","Klavika","Barlow",system-ui,"Segoe UI",sans-serif;--m:"Fira Mono",ui-monospace,Consolas,monospace}
*{box-sizing:border-box}body{overflow-wrap:anywhere;margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 var(--f);-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding-block:32px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:48px}
h1,h2,h3,h4{margin:0;line-height:1.15;text-wrap:balance;color:var(--head);font-family:var(--fh);font-weight:500}
h1{font-size:clamp(30px,5vw,44px)}h2{font-size:24px;display:flex;align-items:center;gap:12px}h3{font-size:19px;line-height:1.3}
h4{font-size:14px;color:var(--bam-steel);font-weight:600}h4 small{font-weight:400;color:var(--muted)}p{margin:0;max-width:70ch}b{font-weight:600}
code{font:13px var(--m);color:var(--muted);overflow-wrap:anywhere}section{display:flex;flex-direction:column;gap:16px}
.eyebrow{font:500 12px var(--fh);letter-spacing:.08em;text-transform:uppercase;color:var(--bam-cyan)}
.hero{display:flex;flex-direction:column;gap:14px;background:var(--bam-petrol);color:#fff;padding:32px clamp(20px,4vw,40px)}
.hero h1{color:#fff}.hero .sub{color:var(--gray-3);font-size:20px;margin-top:-6px}.hero .lead{font-size:19px;font-weight:300}.hero .meta{color:var(--gray-4);font-size:14px}.hero code{color:var(--gray-3)}
.ask{margin:0;padding:14px 16px 14px 38px;background:rgba(255,255,255,.08);border-left:3px solid var(--bam-cyan);display:flex;flex-direction:column;gap:4px}
.n{display:inline-grid;place-items:center;width:34px;height:34px;background:var(--bam-petrol);color:#fff;font:500 16px var(--fh);flex:none}
.tree{display:flex;flex-direction:column;align-items:center;gap:8px;background:var(--paper);border:1px solid var(--line);padding:24px}
.row{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;width:100%}.arrow{color:var(--muted);font-size:14px}
.node{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;border:1px solid var(--line);padding:10px 16px;min-width:0;max-width:100%;background:var(--paper)}
.node span{font-size:13px;color:var(--muted)}.node.root{background:var(--gray-1)}.node.col{border-style:dashed}.node.plan{border-style:dotted}
.specimen{display:flex;flex-direction:column;align-items:center;gap:8px;width:100%;border:1px dashed var(--line);padding:16px}
.obj{--c:var(--extra);--cb:var(--extra-bg)}.probe{--c:var(--probe);--cb:var(--probe-bg)}.scan{--c:var(--scan);--cb:var(--scan-bg)}
.test{--c:var(--test);--cb:var(--test-bg)}.fracture{--c:var(--fracture);--cb:var(--fracture-bg)}.extra{--c:var(--extra);--cb:var(--extra-bg)}
.node.obj{border:1px solid var(--line);border-top:3px solid var(--c);background:var(--cb);flex:1 1 220px}
.node.obj.probe{color:#fff;border-color:var(--bam-petrol)}.node.obj.probe b{color:#fff}.node.obj.probe span,.node.obj.probe code{color:var(--gray-3)}
.specimen>.node.big{padding:16px 28px;flex:none}.dot{width:10px;height:10px;background:var(--c);flex:none}.probe .dot{background:var(--bam-cyan)}
.chip{display:inline-block;font:500 11px var(--fh);letter-spacing:.05em;text-transform:uppercase;padding:3px 8px;background:var(--gray-2);color:var(--bam-petrol);white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis}
.chip.new{background:var(--cyan-tint);color:var(--accent-strong)}.chip.std{background:var(--gray-2);color:var(--gray-5)}
.chip.must{background:#f8ecdd;color:var(--warning)}
.chip.dev,.chip.file{font:400 13px var(--f);letter-spacing:0;text-transform:none;padding:3px 12px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--fg)}
.chip.dev{border-color:var(--bam-steel);color:var(--bam-steel)}.chip.file{border-style:dashed;color:var(--muted)}
.node .chip{margin-top:2px}.chip.dev.lnk{border-style:dashed;border-width:1.5px;background:var(--cyan-tint);color:var(--accent-strong);border-color:var(--accent-strong)}.line{display:flex;flex-direction:column;align-items:center;gap:8px;width:100%;max-width:480px}.line>.node{width:100%;flex:none}.node.obj.probe .chip.dev{background:transparent;color:#fff;border-color:var(--gray-4)}
.timeline{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.step{display:grid;grid-template-columns:52px 1fr;gap:12px;background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--c);padding:14px}
.step .no{font:500 20px var(--m);color:var(--c)}.s-body{display:flex;flex-direction:column;gap:6px;min-width:0}
.where{color:var(--c);font-weight:500}.where b{color:var(--c)}.items{font-size:15px;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px}
.card{background:var(--paper);border:1px solid var(--line);padding:20px 24px;display:flex;flex-direction:column;gap:12px;min-width:0}
.card.obj{border-top:3px solid var(--c)}.card header{display:flex;gap:10px;align-items:flex-start}.card header>div{flex:1;min-width:0}
.card .dot{margin-top:7px}.sec ul,.tlist{list-style:none;margin:0;padding:0}.sec{display:flex;flex-direction:column;gap:4px}
.field{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;padding:8px 0;border-bottom:1px solid var(--gray-2)}
.f-main{display:flex;flex-direction:column;min-width:0;max-width:100%}.f-label{font-family:var(--fh);font-weight:500;color:var(--head);overflow-wrap:anywhere}.f-de{font-size:14px;color:var(--muted);overflow-wrap:anywhere}
.f-meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:14px}.f-type{color:var(--muted)}.terms{font-size:13px;color:var(--muted);margin-top:2px}
details summary{cursor:pointer;color:var(--accent-strong)}.tlist{display:flex;flex-wrap:wrap;gap:6px}
.tlist li{padding:4px 12px;border-radius:999px;border:1px solid var(--line);background:#fff;font-size:13px}
.tlist li.newt{border-color:var(--accent-strong);background:var(--cyan-tint);color:var(--accent-strong)}
.tbl{overflow-x:auto;border:1px solid var(--line)}table{border-collapse:collapse;width:100%;background:var(--paper);font-size:15px}
th,td{padding:10px 14px;border-bottom:1px solid var(--gray-2);text-align:left;white-space:nowrap}th{background:var(--gray-1);color:var(--head);font-weight:600}
td{font-variant-numeric:tabular-nums}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px}.tile{background:var(--paper);border:1px solid var(--line);padding:16px 20px;display:flex;flex-direction:column}
.tile b{font:500 40px var(--fh);color:var(--bam-petrol)}.tile small{color:var(--muted)}.tile span{font-size:14px;color:var(--muted)}
.fb{display:flex;flex-wrap:wrap;align-items:center;gap:8px;background:var(--paper);border:1px solid var(--line);padding:12px 16px}
.fb-q{font-weight:600;color:var(--head);margin-right:auto}.fb textarea{flex-basis:100%}
button{font:500 15px var(--fh);line-height:1;border-radius:0;border:1px solid var(--bam-petrol);background:#fff;color:var(--bam-petrol);padding:10px 20px;cursor:pointer;transition:background-color 120ms cubic-bezier(.4,0,.2,1),color 120ms cubic-bezier(.4,0,.2,1)}
button:hover{background:var(--gray-1)}button:focus-visible,textarea:focus-visible{outline:none;box-shadow:0 0 0 3px rgba(0,175,240,.4)}
button.ok[aria-pressed="true"]{background:var(--bam-petrol);color:#fff}button.chg[aria-pressed="true"]{background:var(--bam-cyan);border-color:var(--bam-cyan);color:var(--bam-petrol)}
textarea{font:inherit;width:100%;border:1px solid var(--line);border-radius:2px;padding:10px;background:#fff;color:var(--fg)}
.answer{background:var(--paper);border-top:3px solid var(--bam-cyan);box-shadow:var(--shadow-card);padding:24px}
.out{margin:0;white-space:pre-wrap;background:var(--gray-1);border:1px solid var(--gray-2);padding:12px;font:14px var(--m);min-height:3em}
.primary{background:var(--bam-petrol);color:#fff;font-size:16px;padding:14px 28px}.primary:hover{background:#00404f}.state{font-weight:600;color:var(--head)}
.dual .sep{color:var(--gray-4);font-weight:400}.dual .en{color:var(--muted);font-weight:400}.de.derived{font-style:italic}
.chip.miss{background:#f8ecdd;color:var(--warning)}.hero .dual .en{color:var(--gray-3)}.hero .dual .sep{color:var(--gray-4)}
.names{font-size:15px;color:var(--gray-3)}.hero .names .de{color:#fff}.dual.th{display:flex;flex-direction:column;gap:0}.dual.th .sep{display:none}
.node.obj.probe .dual .en,.node.obj.probe .dual .sep{color:var(--gray-3)}
html:not(.lang-en) .l-en,html.lang-en .l-de{display:none}
.copyblock{display:flex;flex-direction:column;gap:6px;margin-top:10px}.cb-head{display:flex;justify-content:space-between;align-items:center;gap:8px}
.cb-head button{padding:6px 14px;font-size:13px}.copyblock .out{max-height:260px;overflow:auto}.sendsteps{margin:0;padding-left:22px;display:flex;flex-direction:column;gap:22px}
.send{background:var(--paper);border:1px solid var(--line);border-top:3px solid var(--bam-petrol);padding:24px}.send.locked .send-body{display:none}.send:not(.locked) .locked-msg{display:none}
.locked-msg{color:var(--muted)}input[type=url]{font:inherit;width:100%;border:1px solid var(--line);border-radius:2px;padding:10px;margin:6px 0}
table.tw td{white-space:normal;vertical-align:top}table.tw td,table.tw th{overflow-wrap:break-word;hyphens:auto}table.tw td:first-child{white-space:nowrap}td.src{font-size:13px;color:var(--muted)}.muted{color:var(--muted);font-size:14px}.sel{user-select:all}
a{color:var(--accent-strong)}a:hover{color:var(--bam-petrol)}
.hero-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px}
.lang{display:flex}.lang button{background:transparent;color:#fff;border-color:var(--gray-4);padding:6px 14px;font-size:14px}
.lang button[aria-pressed="true"]{background:var(--bam-cyan);border-color:var(--bam-cyan);color:var(--bam-petrol)}.lang button:hover{background:rgba(255,255,255,.1)}
.lang button[aria-pressed="true"]:hover{background:var(--bam-cyan)}
.copied{color:var(--success);font-weight:600}.hint{font-size:14px;color:var(--muted)}
.variants .vgrid{border:0;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:16px;min-width:0}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.variant{position:relative;background:var(--paper);border:1px solid var(--line);border-top:3px solid var(--gray-3);padding:20px 24px;display:flex;flex-direction:column;gap:12px;cursor:pointer;min-width:0}
.variant.recommended{border-top-color:var(--bam-cyan)}.variant.chosen{border-color:var(--bam-petrol);box-shadow:0 0 0 2px var(--bam-petrol)}
.variant input{position:absolute;top:22px;right:22px;width:20px;height:20px;accent-color:var(--bam-petrol)}
.variant input:focus-visible{outline:none;box-shadow:0 0 0 3px rgba(0,175,240,.4)}
.v-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;padding-right:32px}.v-head h3{flex:1 1 200px}
.v-id{display:inline-grid;place-items:center;width:30px;height:30px;background:var(--gray-2);color:var(--bam-petrol);font:500 16px var(--fh)}
.variant.recommended .v-id{background:var(--bam-cyan)}.rec{color:var(--accent-strong);font-weight:500;white-space:nowrap}
.vsketch{display:flex;flex-direction:column;align-items:center;gap:6px;background:var(--gray-1);padding:14px}
.vrow{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px}.vrow.chain{gap:4px}
.vbox{display:flex;flex-direction:column;align-items:center;text-align:center;font-size:14px;background:#fff;border:1px solid var(--line);border-top:3px solid var(--bam-steel);padding:6px 10px;min-width:0}
.vbox.main{background:var(--bam-petrol);border-color:var(--bam-petrol);color:#fff}.vbox.main .dual .en,.vbox.main .dual .sep,.vbox.main small{color:var(--gray-3)}
.vbox small{color:var(--muted);font-size:12px}.vpill{font:13px var(--m);padding:2px 8px;border:1px solid var(--bam-steel);background:#fff;color:var(--bam-steel);border-radius:999px}
.vfigs{display:grid;grid-template-columns:repeat(auto-fit,minmax(84px,1fr));gap:8px}.vfigs div{display:flex;flex-direction:column;border-left:3px solid var(--gray-3);padding-left:10px}
.vfigs b{font:500 26px var(--fh);color:var(--bam-petrol)}.vfigs span{font-size:13px;color:var(--muted)}
.pc{display:flex;flex-direction:column;gap:6px}.pros,.cons{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px;font-size:15px}
.pros li,.cons li{padding-left:22px;position:relative}.pros li::before{content:"+";position:absolute;left:4px;color:var(--success);font-weight:600}
.cons li::before{content:"–";position:absolute;left:4px;color:var(--warning);font-weight:600}
.vlist{margin:6px 0 0;padding-left:0;list-style:none;font-size:14px;display:flex;flex-direction:column;gap:2px}.vlist code{display:inline-block;min-width:3em}
.vnote{background:var(--cyan-tint);border-left:3px solid var(--bam-cyan);padding:12px 16px;font-weight:500;color:var(--bam-petrol)}
.plist{margin:0;padding-left:22px;display:flex;flex-direction:column;gap:4px;max-width:75ch}.hints li{color:var(--warning)}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;margin:0;background:var(--paper);border:1px solid var(--line);padding:16px 20px}
.kv dt{color:var(--muted)}.kv dd{margin:0}section h3 small{font-weight:400;color:var(--muted);font-size:14px}
@media (max-width:640px){.step{grid-template-columns:40px 1fr}.hero{padding:24px 20px}}
@media (prefers-reduced-motion:reduce){button{transition:none}}
"""

JS = """
(function(){
  var KEY='review-'+document.title, st={}, root=document.documentElement, lang='de';
  try{st=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  try{lang=localStorage.getItem('review-lang')||'de'}catch(e){}
  var L={de:{open:'Noch %o von %n Teilen offen.',ok:'Alles passt: Das ist eine Freigabe.',one:' Änderungswunsch.',many:' Änderungswünsche.',
             wait:'(erscheint, sobald alle Teile beantwortet sind)',app:' freigegeben',not:' noch nicht freigegeben. Bitte ändern:',
             note:'Anmerkung: ',also:'Außerdem: ',dflt:'(bitte ändern)',sel:'Markiert: jetzt kopieren (Strg+C) und im Chat einfügen.',
             vn:'Variante',vchg:'Variante: bitte Variante %c „%n“ ausarbeiten statt %s.',vother:'Der Agent arbeitet Ihre Wahl aus und zeigt Ihnen eine neue Seite.'},
         en:{open:'%o of %n parts still open.',ok:'Everything fits: this is an approval.',one:' change request.',many:' change requests.',
             wait:'(appears once every part is answered)',app:' approved',not:' not approved yet. Please change:',
             note:'Note: ',also:'Also: ',dflt:'(please change)',sel:'Selected: now copy (Ctrl+C) and paste it into the chat.',
             vn:'variant',vchg:'Variant: please work out variant %c “%n” instead of %s.',vother:'The agent works out your choice and shows you a new page.'}};
  var gate=((document.querySelector('[data-gate]')||{}).dataset||{}).gate||'B';
  var fbs=[].slice.call(document.querySelectorAll('.fb')), gen=document.getElementById('fb-gesamt');
  var vsec=document.querySelector('.variants'), vrs=[].slice.call(document.querySelectorAll('input[name=variant]')),
      shown=vsec?vsec.dataset.shown:'', rec=vsec?(vsec.dataset.rec||vsec.dataset.shown):'';
  function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
  function render(){
    var T=L[lang], open=0, changes=[];
    fbs.forEach(function(f){var s=st[f.dataset.item]||{}, label=lang==='en'?f.dataset.labelEn:f.dataset.labelDe;
      f.querySelector('.ok').setAttribute('aria-pressed',s.v==='ok');f.querySelector('.chg').setAttribute('aria-pressed',s.v==='chg');
      var t=f.querySelector('textarea');t.hidden=s.v!=='chg';if(t.value!==(s.t||''))t.value=s.t||'';
      if(!s.v)open++; if(s.v==='chg')changes.push('- '+label+': '+((s.t||'').trim()||T.dflt));});
    if(gen.value!==(st._g||''))gen.value=st._g||'';
    var ans=document.querySelector('[data-gate]')||{dataset:{}}, blk=(lang==='en'?ans.dataset.blockEn:ans.dataset.blockDe)||'';
    var g=(st._g||'').trim(), txt='', state, chosen=st._v||rec, other=!!vsec&&chosen!==shown, cn='';
    vrs.forEach(function(r){r.checked=r.value===chosen;r.parentNode.classList.toggle('chosen',r.checked);if(r.checked)cn=r.dataset.name;});
    if(vsec)document.getElementById('v-note').hidden=!other;
    if(other){changes.unshift('- '+T.vchg.replace('%c',chosen).replace('%n',cn).replace('%s',shown));
      txt=gate+T.not+'\\n'+changes.join('\\n')+(g?'\\n\\n'+T.also+g:'');state=T.vother;}
    else if(open){state=T.open.replace('%o',open).replace('%n',fbs.length);}
    else if(!changes.length&&blk){txt=gate+T.not+'\\n- '+blk+(g?'\\n\\n'+T.also+g:'');state=blk;}
    else if(!changes.length){txt=gate+T.app+(vsec?' ('+T.vn+' '+shown+')':'')+(g?'\\n\\n'+T.note+g:'');state=T.ok;}
    else{txt=gate+T.not+'\\n'+changes.join('\\n')+(g?'\\n\\n'+T.also+g:'');state=changes.length+(changes.length>1?T.many:T.one);}
    document.getElementById('state').textContent=state;
    document.getElementById('out').textContent=txt||T.wait;
    var send=document.getElementById('send');
    if(send){send.classList.toggle('locked',open>0||changes.length>0);
      var u=(document.getElementById('issue-url')||{}).value||'';
      document.getElementById('out-d').textContent=(lang==='en'?'D sent':'D gesendet')+(u.trim()?': '+u.trim():'');}
  }
  function setLang(l){lang=l==='en'?'en':'de';root.classList.toggle('lang-en',lang==='en');root.setAttribute('lang',lang);
    [].forEach.call(document.querySelectorAll('.lang button'),function(b){b.setAttribute('aria-pressed',b.dataset.lang===lang)});
    [].forEach.call(document.querySelectorAll('textarea[data-ph-de]'),function(t){t.placeholder=lang==='en'?t.dataset.phEn:t.dataset.phDe});
    try{localStorage.setItem('review-lang',lang)}catch(e){} render();}
  [].forEach.call(document.querySelectorAll('.lang button'),function(b){b.onclick=function(){setLang(b.dataset.lang)}});
  fbs.forEach(function(f){var id=f.dataset.item;
    f.querySelector('.ok').onclick=function(){st[id]={v:'ok'};save();render()};
    f.querySelector('.chg').onclick=function(){st[id]={v:'chg',t:(st[id]||{}).t||''};save();render();f.querySelector('textarea').focus()};
    f.querySelector('textarea').oninput=function(e){st[id]={v:'chg',t:e.target.value};save();render()};});
  gen.oninput=function(e){st._g=e.target.value;save();render()};
  vrs.forEach(function(r){r.onchange=function(){st._v=r.value;save();render()}});
  var iu=document.getElementById('issue-url'); if(iu)iu.oninput=render;
  [].forEach.call(document.querySelectorAll('button[data-copy]'),function(btn){btn.onclick=function(){
    var el=document.querySelector(btn.dataset.copy), t=el.textContent;
    function sel(){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}
    function done(msg){var o=btn.getAttribute('data-orig')||btn.innerHTML;btn.setAttribute('data-orig',o);
      btn.textContent=msg;setTimeout(function(){btn.innerHTML=o},1800)}
    var ok=lang==='en'?'Copied':'Kopiert';
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(function(){done(ok)},function(){sel();done(L[lang].sel)})}else{sel();done(L[lang].sel)}}});
  setLang(lang);
})();
"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600'
         '&family=Fira+Mono:wght@400;500&display=swap">')


def page(title: str, body: str, fragment: bool) -> str:
    inner = (f'<title>{E(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n'
             f'<style>{CSS}</style>\n<div class="wrap">\n{body}\n</div>\n<script>{JS}</script>\n')
    if fragment:
        return inner
    return ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + inner.replace("<div class=\"wrap\">", "</head>\n<body>\n<div class=\"wrap\">", 1) + "</body>\n</html>\n")


# view -> (page name, HTML, Markdown, (files to check if present, files that must exist))
VIEWS = {"prd": ("Anforderungen", view_prd, md_prd, (("project",), ())),
         "struktur": ("Strukturvorschlag", view_struktur, md_struktur, (("project", "design"), ("design",))),
         "antrag": ("Masterdaten-Antrag", view_antrag, md_antrag, (("project", "design"), ())),
         "trockenlauf": ("Trockenlauf", view_trockenlauf, md_trockenlauf, (("project", "design", "structure"), ()))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Prüfseiten (HTML) für Menschen erzeugen")
    ap.add_argument("projekt")
    ap.add_argument("ansicht", choices=sorted(VIEWS))
    ap.add_argument("--fragment", action="store_true", help="nur den Seiteninhalt ausgeben (ohne <html>-Gerüst)")
    ap.add_argument("--out", type=Path, help="Zieldatei (Standard: projects/<projekt>/review/<ansicht>.html)")
    ap.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    import check_files
    label, fn, md_fn, need = VIEWS[a.ansicht]
    errors, notes = check_files.check_project(a.repo, a.projekt, *need)
    for n in notes:
        print("Hinweis:", n)
    if errors:
        print("Keine Prüfseite erzeugt. Bitte zuerst beheben (Formate: schemas/):")
        for e in errors:
            print("  -", e)
        return 1
    m = Model(a.repo, a.projekt)
    out = a.out or m.project["dir"] / "review" / f"{a.ansicht}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(f"{label} · {m.title_de}", fn(m), a.fragment), encoding="utf-8")
    print(out)
    if not a.fragment:  # same content as Markdown, readable directly on GitHub
        md = out.with_suffix(".md")
        md.write_text(md_fn(Model(a.repo, a.projekt)) + "\n", encoding="utf-8")
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
