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
KIND_COLORS = ["probe", "scan", "test", "fracture", "extra"]


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
        flag = chip("nur EN", "std") if self.src == "std" else chip("DE fehlt", "miss")
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
        first = next((l for l in prd.read_text(encoding="utf-8").splitlines() if l.startswith("# ")), "") if prd.exists() else ""
        self.title = re.sub(r"^#\s*(PRD\s*(v\d+)?\s*:\s*)?", "", first).strip() or name
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
        self.sections_de = {**SECTION_DE_STD, **(self.design.get("section_names_de") or {})}
        self.files = {de(x["file"])[0]: x["file"] for x in self.design.get("dataset_mapping", [])}
        self.devices = {de(x["inventory"])[0]: x["inventory"] for x in self.design.get("inventory_links", [])}

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
        for i, o in enumerate(self.design.get("layout", {}).get("per_specimen", [])):
            name = o.get("name_pattern", "")
            name = name[len(o["code_pattern"]):].strip() if name.startswith(o["code_pattern"]) else name
            nm = Name(o.get("name_de"), o.get("name_en") or name or "Specimen")
            out.append({**o, "kind": KIND_COLORS[min(i, len(KIND_COLORS) - 1)], "name": self._note(nm, f"x:{o['code_pattern']}"),
                        "equipment": [p for p in o.get("parents", []) if "(specimen)" not in p]})
        return out

    def object_for(self, text: str) -> dict | None:
        objs = self.objects()
        for o in sorted(objs, key=lambda o: -len(o["code_pattern"])):
            if o["code_pattern"] in text:
                return o
        return objs[0] if objs and "specimen" in text else None


# --------------------------------------------------------------------------------------------
# html pieces


def chip(text: str, cls: str = "") -> str:
    return f'<span class="chip {cls}">{E(text)}</span>'


def prop_row(m: Model, code: str, section_prop: dict) -> str:
    p = m.props.get(code, {})
    name = m.prop_name(code)
    d = de_only(p.get("description") or section_prop.get("description"))
    typ = TYPE_DE.get(p.get("type") or section_prop.get("data_type"), p.get("type") or "")
    vocab = p.get("vocabulary") or section_prop.get("vocabulary_code")
    choice = ""
    if vocab and vocab in m.vocab:
        terms = [m.term_name(vocab, t["code"]).text for t in m.vocab[vocab]["terms"]]
        choice = f'<span class="terms">{E(" · ".join(terms[:8]))}{" …" if len(terms) > 8 else ""}</span>'
    badge = chip("neu", "new") if code in m.new_codes else chip("Standard", "std")
    must = chip("Pflicht", "must") if section_prop.get("mandatory") else ""
    expl = d if d and d not in (name.de, name.en) else ""
    return (f'<li class="field"><div class="f-main"><span class="f-label">{name.html()}</span>'
            f'<span class="f-de">{E(expl)}</span>{choice}</div>'
            f'<div class="f-meta"><span class="f-type">{E(typ)}</span>{must}{badge}</div></li>')


def object_card(m: Model, t: dict, role_kind: str) -> str:
    """ELN-like form preview: sections in display order with their fields."""
    secs: dict[str, list] = {}
    for p in t.get("properties", []):
        secs.setdefault(p.get("section") or "Ohne Sektion", []).append(p)
    order = t.get("section_order") or list(secs)
    system = {"Comments", "Additional Information", "References", "BAM Information", "Properties", "Ohne Sektion"}
    parts, hidden = [], []
    for s in [*order, *[x for x in secs if x not in order]]:
        fields = [p for p in secs.get(s, []) if not (p["code"].startswith("$") and p["code"] != "$NAME")]
        if not fields:
            continue
        own = sum(p["code"] in m.new_codes for p in fields)
        block = (f'<section class="sec"><h4>{m.section_name(s).html()} <small>{len(fields)} Felder'
                 f'{f", {own} neu" if own else ""}</small></h4><ul>'
                 + "".join(prop_row(m, p["code"], p) for p in fields) + "</ul></section>")
        (hidden if s in system and not own else parts).append(block)
    more = (f'<details><summary>Weitere Standard-Felder ({len(hidden)} Sektionen)</summary>{"".join(hidden)}</details>'
            if hidden else "")
    return (f'<article class="card obj {role_kind}" id="obj-{E(t["code"])}"><header><span class="dot"></span>'
            f'<div><h3>{m.type_name(t).html()}</h3><code>{E(t["code"])}</code></div>{chip("neuer Typ", "new")}</header>'
            f'{"".join(parts)}{more}</article>')


def feedback(item_id: str, label: str) -> str:
    return (f'<div class="fb" data-item="{E(item_id)}" data-label="{E(label)}">'
            f'<span class="fb-q">{E(label)}:</span>'
            f'<button type="button" class="ok" aria-pressed="false">passt</button>'
            f'<button type="button" class="chg" aria-pressed="false">ändern</button>'
            f'<textarea id="fb-{E(item_id)}" placeholder="Was soll anders sein?" hidden></textarea></div>')


# --------------------------------------------------------------------------------------------
# view: struktur (Prüfpunkt B)


def view_struktur(m: Model) -> str:
    d, lay = m.design, m.design.get("layout", {})
    objs = m.objects()
    st = m.structure
    space, project = lay.get("space", f"/{st.get('space', '')}"), lay.get("project", "")
    cols = lay.get("collections", [])
    body = []

    # 1 hierarchy
    collections = "".join(f'<div class="node col"><b>{E(c.get("$NAME") or c["code"])}</b><code>{E(c["code"])}</code></div>'
                          for c in cols)
    plan = "".join(f'<div class="node plan"><b>{E(o.get("$NAME") or o["code"])}</b><span>einmal im Projekt</span></div>'
                   for o in lay.get("project_objects", []))
    steps = "".join(f'<div class="node obj {o["kind"]}"><span class="dot"></span><b>{o["name"].html()}</b>'
                    f'<code>{E(o["code_pattern"])}</code>'
                    f'{"<span>Schritte " + E(", ".join(o.get("covers_steps", []))) + "</span>" if o.get("covers_steps") else ""}'
                    f'{"".join(chip(short(m.device_name(e).text, 60), "dev") for e in o["equipment"])}</div>'
                    for o in objs[1:])
    probe = objs[0] if objs else {"name": Name("Probe", "Specimen"), "code_pattern": "", "kind": "probe"}
    body.append(f"""<section aria-labelledby="h1s"><h2 id="h1s"><span class="n">1</span>So ist dein Projekt aufgebaut</h2>
<p>Eine Serie ist eine Collection. In jeder Serie steht jede Probe einmal, und direkt an der Probe hängen ihre Versuchsschritte.
Geräte und Material kommen aus dem Inventar des Fachbereichs und werden nur verlinkt.</p>
<div class="tree"><div class="node root"><span>Space</span><b>{E(space)}</b></div><div class="arrow">↓</div>
<div class="node root"><span>Projekt / Project</span><b>{E(project)}</b></div><div class="arrow">↓</div>
<div class="row">{collections}{plan}</div><div class="arrow">↓ in jeder Serie, je Probe</div>
<div class="specimen"><div class="node obj {probe['kind']} big"><span class="dot"></span><b>{probe['name'].html()}</b><code>{E(probe['code_pattern'])}</code>
<span>trägt alles, was die Probe beschreibt</span></div><div class="arrow">↓ hängen direkt daran</div><div class="row">{steps}</div></div></div>
{feedback("aufbau", "Aufbau")}</section>""")

    # 2 step -> location
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
<p class="where">→ <b>{o['name'].html()}</b>{f" · Abschnitt {sec_html}" if sec else ""}</p>
{'<p class="items">' + E(" · ".join(items)) + "</p>" if items else ""}
<div class="chips">{"".join(chip(short(m.device_name(e).text, 60), "dev") for e in s.get("equipment", []))}{"".join(chip(m.file_name(f).text, "file") for f in s.get("files", []))}</div></div></li>""")
    body.append(f"""<section aria-labelledby="h2s"><h2 id="h2s"><span class="n">2</span>Wo landet welcher Ablaufschritt?</h2>
<p>Die Farbe zeigt das Objekt, in das der Schritt geschrieben wird. Umrandete Marken sind Geräte oder Material, gestrichelte sind Dateien.</p>
<ol class="timeline">{"".join(rows)}</ol>{feedback("ablauf", "Zuordnung der Schritte")}</section>""")

    # 3 object forms
    kinds = {o["type"]: o["kind"] for o in reversed(objs)}
    order = {o["type"]: i for i, o in enumerate(objs)}
    spec_types = sorted(m.spec.get("object_types", []), key=lambda t: order.get(t["code"], 99))
    cards = [object_card(m, t, kinds.get(t["code"], "extra")) for t in spec_types]
    reused = [o for o in objs if o["type"] not in {t["code"] for t in m.spec.get("object_types", [])}]
    for o in reused:
        role = next((r.get("role", "") for r in d.get("reused_types", []) if r.get("code") == o["type"] and
                     r.get("used_as", "").endswith(o["code_pattern"][len(objs[0]["code_pattern"]):] or "~")), "")
        cards.append(f'<article class="card obj {o["kind"]} slim"><header><span class="dot"></span><div><h3>{o["name"].html()}</h3>'
                     f'<code>{E(o["type"])}</code></div>{chip("aus dem Standard", "std")}</header>'
                     f'<p>{E(short(role, 220)) if role else "Standard-Versuchsschritt: Datum, Bearbeiter*in, Notizen, Dateien. Keine neuen Felder."}</p></article>')
    fb = "".join(feedback(f"obj-{t['code']}", f"Felder „{short(m.type_name(t).text, 60)}“") for t in spec_types)
    body.append(f"""<section aria-labelledby="h3s"><h2 id="h3s"><span class="n">3</span>Welche Felder bekommt jedes Objekt?</h2>
<p>So ungefähr sieht das Formular in der ELN aus. <b>neu</b> heißt: beantragt der Agent beim Data Store, <b>Standard</b> gibt es schon.
Felder mit <b>Pflicht</b> müssen beim Anlegen ausgefüllt sein.</p><div class="cards">{"".join(cards)}</div>{fb}</section>""")

    # 4 series table
    cols_ = lay.get("series_table", [])
    specimens = [o for o in st.get("objects", []) if objs and o.get("type") == objs[0]["type"]][:4]
    by_key = {o["key"]: o for o in st.get("objects", [])}

    def cell(src: str, sp: dict) -> str:
        codes = re.findall(r"[A-Z$][A-Z0-9_.$]+", src)
        target = sp
        if "TEST" in src.split()[0:2]:
            target = by_key.get(f"{sp['key']}-TEST") or {}
        for c in codes:
            v = (target.get("props") or {}).get(c)
            if v is not None:
                vocab = m.props.get(c, {}).get("vocabulary")
                return m.term_name(vocab, str(v)).text if vocab else str(v)
        return "–"
    head = "".join(f"<th>{m._note(Name(de(c['column'])[1] if '//' in c['column'] else '', de(c['column'])[0]), 'c:' + c['column']).html('th')}</th>"
                   for c in cols_)
    rows_ = "".join("<tr>" + "".join(f"<td>{E(cell(c['source'], sp))}</td>" for c in cols_) + "</tr>" for sp in specimens)
    body.append(f"""<section aria-labelledby="h4s"><h2 id="h4s"><span class="n">4</span>So sieht die Serientabelle aus</h2>
<p>Das ist die Tabelle, die man beim Öffnen einer Serie sieht. Die Werte sind Beispieldaten aus der Demo-Serie (fiktiv).</p>
<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{rows_}</tbody></table></div>{feedback("tabelle", "Serientabelle")}</section>""")

    # 5 vocabularies
    vcards = []
    for code, v in m.vocab.items():
        if v["status"] == "standard":
            continue
        new = v.get("new_terms", set())
        terms = "".join(f'<li class="{"newt" if t["code"] in new else ""}">{m.term_name(code, t["code"]).html()}</li>' for t in v["terms"])
        en, dd = de(v.get("description"))
        vcards.append(f'<article class="card voc"><header><div><h3>{m._note(Name(dd if "//" in (v.get("description") or "") else "", en), "v:" + code).html()}</h3>'
                      f'<code>{E(code)}</code></div>{chip("neu" if v["status"] == "neu" else "ergänzt", "new")}</header><ul class="tlist">{terms}</ul></article>')
    body.append(f"""<section aria-labelledby="h5s"><h2 id="h5s"><span class="n">5</span>Auswahllisten</h2>
<p>Hier wählt man im Formular aus einer festen Liste. Hervorgehoben sind die Einträge, die neu dazukommen.</p>
<div class="cards">{"".join(vcards)}</div>{feedback("listen", "Auswahllisten")}</section>""")

    # 6 numbers
    mt = d.get("metrics", {})
    if mt.get("new") and mt.get("legacy_live"):
        a, b = mt["new"], mt["legacy_live"]
        tiles = "".join(f'<div class="tile"><span>{E(lbl)}</span><b>{E(str(a.get(k, "–")))}</b><small>vorher {E(str(b.get(k, "–")))}</small></div>'
                        for k, lbl in (("objects_per_specimen", "Objekte je Probe"), ("max_link_depth", "Ebenen unter der Probe"),
                                       ("new_object_types", "neue Typen"), ("new_dataset_types", "neue Datei-Typen")))
        body.append(f'<section aria-labelledby="h6s"><h2 id="h6s"><span class="n">6</span>Einfacher als vorher</h2>'
                    f'<p>Vergleich mit dem bisherigen Modell auf der Übungsinstanz.</p><div class="tiles">{tiles}</div></section>')

    # 7 answer
    body.append("""<section aria-labelledby="h7s" class="answer"><h2 id="h7s"><span class="n">✓</span>Deine Antwort an den Agenten</h2>
<label for="fb-gesamt">Noch etwas Allgemeines? (freiwillig)</label><textarea id="fb-gesamt" rows="3"></textarea>
<p id="state" class="state">Noch nicht alles beantwortet.</p>
<pre id="out" class="out" aria-live="polite"></pre>
<button type="button" id="copy" class="primary">Text kopieren</button> <span id="copied" class="copied" hidden>Kopiert. Jetzt im Chat einfügen.</span>
<p class="hint">Den kopierten Text fügst du im Chat mit dem Agenten ein. Die Seite speichert nichts und schickt nichts ab.</p></section>""")

    # header last, because it reports how many names still lack German
    n_missing = len(m.missing)
    header = f"""<header class="hero"><span class="eyebrow">Prüfpunkt B · Struktur bestätigen</span>
<h1>{E(m.title)}</h1>
<p class="lead">So würde der Agent deinen Versuchsablauf in openBIS abbilden. Lies die Seite von oben nach unten.
Bei jedem Teil sagst du <b>passt</b> oder <b>ändern</b>. Ganz unten entsteht daraus dein Text für den Chat.</p>
<ol class="ask"><li>Hat jeder Ablaufschritt genau einen Ort?</li><li>Sind die Felder die, die ihr im Labor wirklich notiert?</li>
<li>Würdet ihr die Serientabelle so lesen wollen?</li><li>Passen die Begriffe auf Deutsch und auf Englisch?</li></ol>
<p class="names">Alle Namen stehen als <span class="dual"><span class="de">Deutsch</span><span class="sep"> / </span><span class="en">Englisch</span></span>.
<span class="de derived">Kursiv</span> = aus der deutschen Beschreibung übernommen, noch kein eigener deutscher Name.
{chip("DE fehlt", "miss")} = die deutsche Fassung fehlt noch{f" (hier {n_missing}×)" if n_missing else " (hier keine)"}.
{chip("nur EN", "std")} = Name aus dem BAM-Standard, den es dort nur auf Englisch gibt.</p>
<p class="meta">Vorschlag vom {E((d.get("designed_at") or "")[:10])} · Projekt <code>{E(m.project["name"])}</code></p></header>"""
    terms_fb = feedback("begriffe", "Begriffe Deutsch / Englisch")
    return "\n".join([header, *body[:-1], f'<section aria-labelledby="h8s"><h2 id="h8s"><span class="n">7</span>Begriffe in beiden Sprachen</h2>'
                      f'<p>Alle Namen oben stehen auf Deutsch und Englisch. Stimmen die Begriffe in beiden Sprachen? '
                      f'Schreib bei „ändern“ die gewünschten Begriffe einfach dazu, z. B. „Herkunftsblech → Ausgangsblech“.</p>{terms_fb}</section>',
                      body[-1]])


# --------------------------------------------------------------------------------------------
# page

CSS = """
/* BAM Design System (00_BAM_Design_System): Petrol #002832 für Überschriften und dunkle Flächen, Cyan #00AFF0 als einziger
   Akzent, Rot nur für Warnungen; Fira Sans/Fira Mono als Ersatz für TheSans; eckig, Pillen nur für Tags; nur heller Modus.
   Objektfarben: Probe Petrol (gefüllt), Scan Steel, Versuch Cyan, Bruch Grau */
:root{color-scheme:light;
--bam-petrol:#002832;--bam-cyan:#00aff0;--bam-steel:#00556a;--bam-red:#d2001f;--cyan-tint:#e0f5fd;--petrol-tint:#e6ebec;
--gray-1:#f4f7f8;--gray-2:#e6ebec;--gray-3:#c9d3d6;--gray-4:#9fadb2;--gray-5:#66787f;
--bg:var(--gray-1);--paper:#ffffff;--fg:#1c343c;--head:var(--bam-petrol);--muted:var(--gray-5);--line:var(--gray-3);
--accent:var(--bam-cyan);--accent-strong:#0079ab;--success:#1e7d5a;--warning:#b96a00;
--probe:var(--bam-petrol);--probe-bg:var(--bam-petrol);--scan:var(--bam-steel);--scan-bg:#e3eef1;
--test:var(--accent-strong);--test-bg:var(--cyan-tint);--fracture:var(--gray-5);--fracture-bg:var(--gray-2);--extra:var(--gray-5);--extra-bg:var(--gray-2);
--shadow-card:0 1px 3px rgba(0,40,50,.10),0 4px 16px rgba(0,40,50,.08);
--f:"Fira Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--m:"Fira Mono",ui-monospace,Consolas,monospace}
*{box-sizing:border-box}body{overflow-wrap:anywhere;margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 var(--f);-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding-block:32px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:48px}
h1,h2,h3,h4{margin:0;line-height:1.15;text-wrap:balance;color:var(--head);font-weight:600}
h1{font-size:clamp(30px,5vw,44px)}h2{font-size:24px;display:flex;align-items:center;gap:12px}h3{font-size:19px;line-height:1.3}
h4{font-size:14px;color:var(--bam-steel);font-weight:600}h4 small{font-weight:400;color:var(--muted)}p{margin:0;max-width:70ch}b{font-weight:600}
code{font:13px var(--m);color:var(--muted);overflow-wrap:anywhere}section{display:flex;flex-direction:column;gap:16px}
.eyebrow{font:600 12px var(--f);letter-spacing:.08em;text-transform:uppercase;color:var(--bam-cyan)}
.hero{display:flex;flex-direction:column;gap:14px;background:var(--bam-petrol);color:#fff;padding:32px clamp(20px,4vw,40px)}
.hero h1{color:#fff}.hero .lead{font-size:19px;font-weight:300}.hero .meta{color:var(--gray-4);font-size:14px}.hero code{color:var(--gray-3)}
.ask{margin:0;padding:14px 16px 14px 38px;background:rgba(255,255,255,.08);border-left:3px solid var(--bam-cyan);display:flex;flex-direction:column;gap:4px}
.n{display:inline-grid;place-items:center;width:34px;height:34px;background:var(--bam-petrol);color:#fff;font:600 16px var(--f);flex:none}
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
.chip{display:inline-block;font:600 11px var(--f);letter-spacing:.05em;text-transform:uppercase;padding:3px 8px;background:var(--gray-2);color:var(--bam-petrol);white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis}
.chip.new{background:var(--cyan-tint);color:var(--accent-strong)}.chip.std{background:var(--gray-2);color:var(--gray-5)}
.chip.must{background:#f8ecdd;color:var(--warning)}
.chip.dev,.chip.file{font:400 13px var(--f);letter-spacing:0;text-transform:none;padding:3px 12px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--fg)}
.chip.dev{border-color:var(--bam-steel);color:var(--bam-steel)}.chip.file{border-style:dashed;color:var(--muted)}
.node .chip{margin-top:2px}.node.obj.probe .chip.dev{background:transparent;color:#fff;border-color:var(--gray-4)}
.timeline{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.step{display:grid;grid-template-columns:52px 1fr;gap:12px;background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--c);padding:14px}
.step .no{font:500 20px var(--m);color:var(--c)}.s-body{display:flex;flex-direction:column;gap:6px;min-width:0}
.where{color:var(--c);font-weight:500}.where b{color:var(--c)}.items{font-size:15px;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px}
.card{background:var(--paper);border:1px solid var(--line);padding:20px 24px;display:flex;flex-direction:column;gap:12px;min-width:0}
.card.obj{border-top:3px solid var(--c)}.card header{display:flex;gap:10px;align-items:flex-start}.card header>div{flex:1;min-width:0}
.card .dot{margin-top:7px}.sec ul,.tlist{list-style:none;margin:0;padding:0}.sec{display:flex;flex-direction:column;gap:4px}
.field{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;padding:8px 0;border-bottom:1px solid var(--gray-2)}
.f-main{display:flex;flex-direction:column;min-width:0;max-width:100%}.f-label{font-weight:500;color:var(--head);overflow-wrap:anywhere}.f-de{font-size:14px;color:var(--muted);overflow-wrap:anywhere}
.f-meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:14px}.f-type{color:var(--muted)}.terms{font-size:13px;color:var(--muted);margin-top:2px}
details summary{cursor:pointer;color:var(--accent-strong)}.tlist{display:flex;flex-wrap:wrap;gap:6px}
.tlist li{padding:4px 12px;border-radius:999px;border:1px solid var(--line);background:#fff;font-size:13px}
.tlist li.newt{border-color:var(--accent-strong);background:var(--cyan-tint);color:var(--accent-strong)}
.tbl{overflow-x:auto;border:1px solid var(--line)}table{border-collapse:collapse;width:100%;background:var(--paper);font-size:15px}
th,td{padding:10px 14px;border-bottom:1px solid var(--gray-2);text-align:left;white-space:nowrap}th{background:var(--gray-1);color:var(--head);font-weight:600}
td{font-variant-numeric:tabular-nums}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px}.tile{background:var(--paper);border:1px solid var(--line);padding:16px 20px;display:flex;flex-direction:column}
.tile b{font:600 40px var(--f);color:var(--bam-petrol)}.tile small{color:var(--muted)}.tile span{font-size:14px;color:var(--muted)}
.fb{display:flex;flex-wrap:wrap;align-items:center;gap:8px;background:var(--paper);border:1px solid var(--line);padding:12px 16px}
.fb-q{font-weight:600;color:var(--head);margin-right:auto}.fb textarea{flex-basis:100%}
button{font:600 15px var(--f);line-height:1;border-radius:0;border:1px solid var(--bam-petrol);background:#fff;color:var(--bam-petrol);padding:10px 20px;cursor:pointer;transition:background-color 120ms cubic-bezier(.4,0,.2,1),color 120ms cubic-bezier(.4,0,.2,1)}
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
.copied{color:var(--success);font-weight:600}.hint{font-size:14px;color:var(--muted)}
@media (max-width:640px){.step{grid-template-columns:40px 1fr}.hero{padding:24px 20px}}
@media (prefers-reduced-motion:reduce){button{transition:none}}
"""

JS = """
(function(){
  var KEY='review-'+document.title, st={};
  try{st=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  var fbs=[].slice.call(document.querySelectorAll('.fb')), gen=document.getElementById('fb-gesamt');
  function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
  function render(){
    var open=0, changes=[];
    fbs.forEach(function(f){var s=st[f.dataset.item]||{};
      f.querySelector('.ok').setAttribute('aria-pressed',s.v==='ok');f.querySelector('.chg').setAttribute('aria-pressed',s.v==='chg');
      var t=f.querySelector('textarea');t.hidden=s.v!=='chg';if(t.value!==(s.t||''))t.value=s.t||'';
      if(!s.v)open++; if(s.v==='chg')changes.push('- '+f.dataset.label+': '+((s.t||'').trim()||'(bitte ändern)'));});
    if(gen.value!==(st._g||''))gen.value=st._g||'';
    var g=(st._g||'').trim(), txt;
    if(open){txt='';document.getElementById('state').textContent='Noch '+open+' von '+fbs.length+' Teilen offen.';}
    else if(!changes.length){txt='B freigegeben'+(g?'\\n\\nAnmerkung: '+g:'');document.getElementById('state').textContent='Alles passt: Das ist eine Freigabe.';}
    else{txt='B noch nicht freigegeben. Bitte ändern:\\n'+changes.join('\\n')+(g?'\\n\\nAußerdem: '+g:'');document.getElementById('state').textContent=changes.length+' Änderungswunsch'+(changes.length>1?'e':'')+'.';}
    document.getElementById('out').textContent=txt||'(erscheint, sobald alle Teile beantwortet sind)';
  }
  fbs.forEach(function(f){var id=f.dataset.item;
    f.querySelector('.ok').onclick=function(){st[id]={v:'ok'};save();render()};
    f.querySelector('.chg').onclick=function(){st[id]={v:'chg',t:(st[id]||{}).t||''};save();render();f.querySelector('textarea').focus()};
    f.querySelector('textarea').oninput=function(e){st[id]={v:'chg',t:e.target.value};save();render()};});
  gen.oninput=function(e){st._g=e.target.value;save();render()};
  document.getElementById('copy').onclick=function(){var t=document.getElementById('out').textContent,ok=document.getElementById('copied');
    function sel(){var r=document.createRange();r.selectNodeContents(document.getElementById('out'));var s=getSelection();s.removeAllRanges();s.addRange(r)}
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(function(){ok.hidden=false},function(){sel();ok.hidden=false;ok.textContent='Markiert: jetzt kopieren (Strg+C) und im Chat einfügen.'})}else{sel();ok.hidden=false}};
  render();
})();
"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fira+Mono:wght@400;500'
         '&family=Fira+Sans:wght@300;400;500;600&display=swap">')


def page(title: str, body: str, fragment: bool) -> str:
    inner = (f'<title>{E(title)}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n'
             f'<style>{CSS}</style>\n<div class="wrap">\n{body}\n</div>\n<script>{JS}</script>\n')
    if fragment:
        return inner
    return ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + inner.replace("<div class=\"wrap\">", "</head>\n<body>\n<div class=\"wrap\">", 1) + "</body>\n</html>\n")


VIEWS = {"struktur": ("Strukturvorschlag", view_struktur)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Prüfseiten (HTML) für Menschen erzeugen")
    ap.add_argument("projekt")
    ap.add_argument("ansicht", choices=sorted(VIEWS))
    ap.add_argument("--fragment", action="store_true", help="nur den Seiteninhalt ausgeben (ohne <html>-Gerüst)")
    ap.add_argument("--out", type=Path, help="Zieldatei (Standard: projects/<projekt>/review/<ansicht>.html)")
    ap.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    m = Model(a.repo, a.projekt)
    label, fn = VIEWS[a.ansicht]
    out = a.out or m.project["dir"] / "review" / f"{a.ansicht}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"\s*\(.*?\)\s*$", "", m.title)  # page name without the trailing "(FB …)"
    out.write_text(page(f"{label} {name}", fn(m), a.fragment), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
