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


def short(text: str, n: int = 90) -> str:
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


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
        self.vocab: dict[str, dict] = {}
        for t in self.catalog["types"]:
            if t.get("root") == "VocabularyType":
                self.vocab[t["code"]] = {"terms": t.get("terms", []), "description": t["defs"].get("description"),
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
        # every property code -> label, type, vocabulary; own (new) codes from the design
        self.props: dict[str, dict] = {}
        for t in self.catalog["types"]:
            for p in t.get("properties", []) + t.get("inherited_properties", []):
                self.props.setdefault(p["code"], {"label": p.get("property_label") or p["code"], "type": p.get("data_type"),
                                                  "description": p.get("description"), "vocabulary": p.get("vocabulary_code")})
        self.new_codes = set()
        for t in self.design.get("object_types", []):
            for p in t.get("properties", []):
                self.props[p["code"]] = {"label": p.get("property_label") or p["code"], "type": p.get("data_type"),
                                         "description": p.get("description"), "vocabulary": p.get("vocabulary_code")}
                if not p.get("reuse_property"):
                    self.new_codes.add(p["code"])
        for t in self.spec.get("object_types", []):
            for p in t.get("properties", []):
                self.props.setdefault(p["code"], {"label": p.get("label") or p["code"], "type": p.get("data_type"),
                                                  "description": p.get("description"), "vocabulary": p.get("vocabulary_code")})

    def term_label(self, vocab: str | None, code: str) -> str:
        """Short German text if the description has one, else the term's label."""
        for t in (self.vocab.get(vocab) or {}).get("terms", []):
            if t["code"] == code:
                d = de(t.get("description"))[1]
                return d if d and len(d) <= 40 else (t.get("label") or d or code)
        return code

    def objects(self) -> list[dict]:
        """Objects per specimen with a kind (for colours) and a friendly name."""
        out = []
        for i, o in enumerate(self.design.get("layout", {}).get("per_specimen", [])):
            name = o.get("name_pattern", "")
            name = name[len(o["code_pattern"]):].strip() if name.startswith(o["code_pattern"]) else name
            out.append({**o, "kind": KIND_COLORS[min(i, len(KIND_COLORS) - 1)], "label": name or "Probe",
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
    en, d = de(p.get("description") or section_prop.get("description"))
    typ = TYPE_DE.get(p.get("type") or section_prop.get("data_type"), p.get("type") or "")
    vocab = p.get("vocabulary") or section_prop.get("vocabulary_code")
    choice = ""
    if vocab and vocab in m.vocab:
        terms = [m.term_label(vocab, t["code"]) for t in m.vocab[vocab]["terms"]]
        choice = f'<span class="terms">{E(" · ".join(terms[:8]))}{" …" if len(terms) > 8 else ""}</span>'
    badge = chip("neu", "new") if code in m.new_codes else chip("Standard", "std")
    must = chip("Pflicht", "must") if section_prop.get("mandatory") else ""
    label = p.get("label") or section_prop.get("label") or code
    return (f'<li class="field"><div class="f-main"><span class="f-label">{E(label)}</span>'
            f'<span class="f-de">{E(d) if d and d != label else ""}</span>{choice}</div>'
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
        block = (f'<section class="sec"><h4>{E(s)} <small>{len(fields)} Felder'
                 f'{f", {own} neu" if own else ""}</small></h4><ul>'
                 + "".join(prop_row(m, p["code"], p) for p in fields) + "</ul></section>")
        (hidden if s in system and not own else parts).append(block)
    en, d = de(t.get("description"))
    more = (f'<details><summary>Weitere Standard-Felder ({len(hidden)} Sektionen)</summary>{"".join(hidden)}</details>'
            if hidden else "")
    return (f'<article class="card obj {role_kind}" id="obj-{E(t["code"])}"><header><span class="dot"></span>'
            f'<div><h3>{E(d or t["code"])}</h3><code>{E(t["code"])}</code></div>{chip("neuer Typ", "new")}</header>'
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
    out = []

    # header
    out.append(f"""<header class="hero"><span class="eyebrow">Prüfpunkt B · Struktur bestätigen</span>
<h1>{E(m.title)}</h1>
<p class="lead">So würde der Agent deinen Versuchsablauf in openBIS abbilden. Lies die Seite von oben nach unten.
Bei jedem Teil sagst du <b>passt</b> oder <b>ändern</b>. Ganz unten entsteht daraus dein Text für den Chat.</p>
<ol class="ask"><li>Hat jeder Ablaufschritt genau einen Ort?</li><li>Sind die Felder die, die ihr im Labor wirklich notiert?</li>
<li>Würdet ihr die Serientabelle so lesen wollen?</li></ol>
<p class="meta">Vorschlag vom {E((d.get("designed_at") or "")[:10])} · Projekt <code>{E(m.project["name"])}</code></p></header>""")

    # 1 hierarchy
    collections = "".join(f'<div class="node col"><b>{E(de(c.get("$NAME") or c["code"])[1])}</b><code>{E(c["code"])}</code></div>'
                          for c in cols)
    plan = "".join(f'<div class="node plan"><b>{E(o.get("$NAME") or o["code"])}</b><span>einmal im Projekt</span></div>'
                   for o in lay.get("project_objects", []))
    steps = "".join(f'<div class="node obj {o["kind"]}"><span class="dot"></span><b>{E(o["label"])}</b>'
                    f'<code>{E(o["code_pattern"])}</code>'
                    f'{"<span>Schritte " + E(", ".join(o.get("covers_steps", []))) + "</span>" if o.get("covers_steps") else ""}'
                    f'{"".join(chip(short(de(e)[1], 34), "dev") for e in o["equipment"])}</div>'
                    for o in objs[1:])
    probe = objs[0] if objs else {"label": "Probe", "code_pattern": "", "kind": "probe"}
    out.append(f"""<section aria-labelledby="h1s"><h2 id="h1s"><span class="n">1</span>So ist dein Projekt aufgebaut</h2>
<p>Eine Serie ist eine Collection. In jeder Serie steht jede Probe einmal, und direkt an der Probe hängen ihre Versuchsschritte.
Geräte und Material kommen aus dem Inventar des Fachbereichs und werden nur verlinkt.</p>
<div class="tree"><div class="node root"><span>Space</span><b>{E(space)}</b></div><div class="arrow">↓</div>
<div class="node root"><span>Projekt</span><b>{E(project)}</b></div><div class="arrow">↓</div>
<div class="row">{collections}{plan}</div><div class="arrow">↓ in jeder Serie, je Probe</div>
<div class="specimen"><div class="node obj {probe['kind']} big"><span class="dot"></span><b>{E(probe['label'])}</b><code>{E(probe['code_pattern'])}</code>
<span>trägt alles, was die Probe beschreibt</span></div><div class="arrow">↓ hängen direkt daran</div><div class="row">{steps}</div></div></div>
{feedback("aufbau", "Aufbau")}</section>""")

    # 2 step -> location
    rows = []
    for s in d.get("step_location_map", []):
        o = m.object_for(s.get("object", "")) or {"kind": "extra", "label": s.get("object", "")}
        items = []
        for it in s.get("data_items", []):
            code = it.split()[0]
            quoted = re.match(r"'([^']+)'", it)
            items.append(m.props.get(code, {}).get("label") or (quoted.group(1) if quoted else short(it.split(" = ")[0], 60)))
        files = [de(next((x["file"] for x in d.get("dataset_mapping", []) if de(x["file"])[0] == f), f))[1]
                 for f in s.get("files", [])]
        sec = s.get("section") if s.get("section") not in (None, "-") else ""
        rows.append(f"""<li class="step {o['kind']}"><span class="no">{E(s.get('no', ''))}</span><div class="s-body">
<h3>{E(s.get('step', ''))}</h3><p class="where">→ <b>{E(o['label'])}</b>{f" · Abschnitt „{E(sec)}“" if sec else ""}</p>
{'<p class="items">' + E(" · ".join(items)) + "</p>" if items else ""}
<div class="chips">{"".join(chip(short(de(e)[1].replace(" (parent)", ""), 40), "dev") for e in s.get("equipment", []))}{"".join(chip(f, "file") for f in files)}</div></div></li>""")
    out.append(f"""<section aria-labelledby="h2s"><h2 id="h2s"><span class="n">2</span>Wo landet welcher Ablaufschritt?</h2>
<p>Farbe = Objekt, in das der Schritt geschrieben wird. Grüne Marken sind Geräte oder Material, graue sind Dateien.</p>
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
        cards.append(f'<article class="card obj {o["kind"]} slim"><header><span class="dot"></span><div><h3>{E(o["label"])}</h3>'
                     f'<code>{E(o["type"])}</code></div>{chip("aus dem Standard", "std")}</header>'
                     f'<p>{E(short(role, 220)) if role else "Standard-Versuchsschritt: Datum, Bearbeiter*in, Notizen, Dateien. Keine neuen Felder."}</p></article>')
    fb = "".join(feedback(f"obj-{t['code']}", f"Felder „{short(de(t.get('description'))[1], 50) or t['code']}“")
                 for t in spec_types)
    out.append(f"""<section aria-labelledby="h3s"><h2 id="h3s"><span class="n">3</span>Welche Felder bekommt jedes Objekt?</h2>
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
                return m.term_label(m.props.get(c, {}).get("vocabulary"), str(v)) if m.props.get(c, {}).get("vocabulary") else str(v)
        return "–"
    head = "".join(f"<th>{E(de(c['column'])[1])}</th>" for c in cols_)
    body = "".join("<tr>" + "".join(f"<td>{E(cell(c['source'], sp))}</td>" for c in cols_) + "</tr>" for sp in specimens)
    out.append(f"""<section aria-labelledby="h4s"><h2 id="h4s"><span class="n">4</span>So sieht die Serientabelle aus</h2>
<p>Das ist die Tabelle, die man beim Öffnen einer Serie sieht. Die Werte sind Beispieldaten aus der Demo-Serie (fiktiv).</p>
<div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>{feedback("tabelle", "Serientabelle")}</section>""")

    # 5 vocabularies
    vcards = []
    for code, v in m.vocab.items():
        if v["status"] == "standard":
            continue
        new = v.get("new_terms", set())
        terms = "".join(f'<li class="{"newt" if t["code"] in new else ""}">{E(m.term_label(code, t["code"]))}</li>' for t in v["terms"])
        vcards.append(f'<article class="card voc"><header><div><h3>{E(de(v.get("description"))[1] or code)}</h3><code>{E(code)}</code></div>'
                      f'{chip("neu" if v["status"] == "neu" else "ergänzt", "new")}</header><ul class="tlist">{terms}</ul></article>')
    out.append(f"""<section aria-labelledby="h5s"><h2 id="h5s"><span class="n">5</span>Auswahllisten</h2>
<p>Hier wählt man im Formular aus einer festen Liste. Hervorgehoben sind die Einträge, die neu dazukommen.</p>
<div class="cards">{"".join(vcards)}</div>{feedback("listen", "Auswahllisten")}</section>""")

    # 6 numbers
    mt = d.get("metrics", {})
    if mt.get("new") and mt.get("legacy_live"):
        a, b = mt["new"], mt["legacy_live"]
        tiles = "".join(f'<div class="tile"><span>{E(lbl)}</span><b>{E(str(a.get(k, "–")))}</b><small>vorher {E(str(b.get(k, "–")))}</small></div>'
                        for k, lbl in (("objects_per_specimen", "Objekte je Probe"), ("max_link_depth", "Ebenen unter der Probe"),
                                       ("new_object_types", "neue Typen"), ("new_dataset_types", "neue Datei-Typen")))
        out.append(f'<section aria-labelledby="h6s"><h2 id="h6s"><span class="n">6</span>Einfacher als vorher</h2>'
                   f'<p>Vergleich mit dem bisherigen Modell auf der Übungsinstanz.</p><div class="tiles">{tiles}</div></section>')

    # 7 answer
    out.append("""<section aria-labelledby="h7s" class="answer"><h2 id="h7s"><span class="n">✓</span>Deine Antwort an den Agenten</h2>
<label for="fb-gesamt">Noch etwas Allgemeines? (freiwillig)</label><textarea id="fb-gesamt" rows="3"></textarea>
<p id="state" class="state">Noch nicht alles beantwortet.</p>
<pre id="out" class="out" aria-live="polite"></pre>
<button type="button" id="copy" class="primary">Text kopieren</button> <span id="copied" class="copied" hidden>Kopiert. Jetzt im Chat einfügen.</span>
<p class="hint">Den kopierten Text fügst du im Chat mit dem Agenten ein. Die Seite speichert nichts und schickt nichts ab.</p></section>""")
    return "\n".join(out)


# --------------------------------------------------------------------------------------------
# page

CSS = """
:root{--bg:#f4f6f5;--paper:#fff;--fg:#1b2420;--muted:#5b6862;--line:#d9e0dc;--accent:#1f6f5c;
--probe:#2f6db5;--probe-bg:#e7f0fa;--scan:#0f8a8a;--scan-bg:#e2f4f3;--test:#c0661b;--test-bg:#fcefe2;
--fracture:#7b4fb0;--fracture-bg:#f1eafa;--extra:#69707a;--extra-bg:#eef0f2;--dev:#2e7d4f;--dev-bg:#e5f3ea;
--new:#9a3d00;--new-bg:#ffe9d6;--ok:#2e7d4f;--chg:#b3261e;
--f:"Atkinson Hyperlegible Next","Atkinson Hyperlegible","Segoe UI",system-ui,sans-serif;--m:"Atkinson Hyperlegible Mono",ui-monospace,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121816;--paper:#1a2220;--fg:#e6ece9;--muted:#9fb0a8;--line:#2d3a35;--accent:#6cc7ae;
--probe:#8db8ef;--probe-bg:#1d2a3a;--scan:#6fd0cf;--scan-bg:#163130;--test:#f0a868;--test-bg:#3a2816;--fracture:#c3a3ef;--fracture-bg:#2b2140;
--extra:#a9b0b8;--extra-bg:#262b30;--dev:#86d1a3;--dev-bg:#1b3226;--new:#ffb27a;--new-bg:#3e2614;--ok:#86d1a3;--chg:#ff9a92;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121816;--paper:#1a2220;--fg:#e6ece9;--muted:#9fb0a8;--line:#2d3a35;--accent:#6cc7ae;
--probe:#8db8ef;--probe-bg:#1d2a3a;--scan:#6fd0cf;--scan-bg:#163130;--test:#f0a868;--test-bg:#3a2816;--fracture:#c3a3ef;--fracture-bg:#2b2140;
--extra:#a9b0b8;--extra-bg:#262b30;--dev:#86d1a3;--dev-bg:#1b3226;--new:#ffb27a;--new-bg:#3e2614;--ok:#86d1a3;--chg:#ff9a92;color-scheme:dark}
*{box-sizing:border-box}body{overflow-wrap:anywhere;margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 var(--f)}
.wrap{max-width:1000px;margin:0 auto;padding-block:32px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:44px}
h1,h2,h3,h4{margin:0;line-height:1.2;text-wrap:balance}h1{font-size:clamp(28px,5vw,40px)}h2{font-size:24px;display:flex;align-items:center;gap:12px}
h3{font-size:18px}h4{font-size:15px;color:var(--muted);font-weight:700}h4 small{font-weight:400}p{margin:0;max-width:70ch}
code{font:13px var(--m);color:var(--muted);overflow-wrap:anywhere}section{display:flex;flex-direction:column;gap:16px}
.eyebrow{font:700 13px var(--f);letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.hero{display:flex;flex-direction:column;gap:12px}.lead{font-size:19px}.meta{color:var(--muted);font-size:14px}
.ask{margin:0;padding:14px 14px 14px 36px;background:var(--paper);border:1px solid var(--line);border-radius:10px;display:flex;flex-direction:column;gap:4px}
.n{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--accent);color:var(--paper);font-size:17px;flex:none}
.tree{display:flex;flex-direction:column;align-items:center;gap:8px;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:20px}
.row{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;width:100%}.arrow{color:var(--muted);font-size:14px}
.node{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;border:2px solid var(--line);border-radius:10px;padding:10px 14px;min-width:0;max-width:100%;background:var(--paper)}
.node span{font-size:13px;color:var(--muted)}.node.root{background:var(--extra-bg)}.node.col{border-style:dashed}.node.plan{border-style:dotted}
.specimen{display:flex;flex-direction:column;align-items:center;gap:8px;width:100%;border:1px dashed var(--line);border-radius:12px;padding:14px}
.specimen>.node.big{padding:14px 26px;flex:none}.node .chip{margin-top:2px}
.obj{--c:var(--extra);--cb:var(--extra-bg)}.probe{--c:var(--probe);--cb:var(--probe-bg)}.scan{--c:var(--scan);--cb:var(--scan-bg)}
.test{--c:var(--test);--cb:var(--test-bg)}.fracture{--c:var(--fracture);--cb:var(--fracture-bg)}.extra{--c:var(--extra);--cb:var(--extra-bg)}
.node.obj{border-color:var(--c);background:var(--cb);flex:1 1 220px}.dot{width:12px;height:12px;border-radius:50%;background:var(--c);flex:none}
.chip{display:inline-block;font-size:13px;padding:2px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted);white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis}
.chip.dev{background:var(--dev-bg);color:var(--dev);border-color:transparent}.chip.file{background:var(--extra-bg)}
.chip.new{background:var(--new-bg);color:var(--new);border-color:transparent;font-weight:700}.chip.std{opacity:.8}.chip.must{border-color:var(--chg);color:var(--chg)}
.timeline{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.step{display:grid;grid-template-columns:52px 1fr;gap:12px;background:var(--paper);border:1px solid var(--line);border-left:6px solid var(--c);border-radius:10px;padding:12px}
.step .no{font:700 20px var(--m);color:var(--c)}.s-body{display:flex;flex-direction:column;gap:6px;min-width:0}
.where{color:var(--c)}.items{font-size:15px;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:14px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0}
.card.obj{border-top:6px solid var(--c)}.card header{display:flex;gap:10px;align-items:flex-start}.card header>div{flex:1;min-width:0}
.sec ul,.tlist{list-style:none;margin:0;padding:0}.sec{display:flex;flex-direction:column;gap:6px}
.field{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;padding:7px 0;border-bottom:1px solid var(--line)}
.f-main{display:flex;flex-direction:column;min-width:0;max-width:100%}.f-label{font-weight:700;overflow-wrap:anywhere}.f-de{overflow-wrap:anywhere}.f-de{font-size:14px;color:var(--muted)}
.f-meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:14px}.f-type{color:var(--muted)}.terms{font-size:13px;color:var(--muted);margin-top:2px}
details summary{cursor:pointer;color:var(--accent)}.tlist{display:flex;flex-wrap:wrap;gap:6px}
.tlist li{padding:4px 10px;border-radius:8px;background:var(--extra-bg);font-size:15px}.tlist li.newt{background:var(--new-bg);color:var(--new);font-weight:700}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;background:var(--paper);font-size:15px}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}th{background:var(--probe-bg);color:var(--probe)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}.tile{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;flex-direction:column}
.tile b{font-size:34px;color:var(--accent)}.tile small{color:var(--muted)}
.fb{display:flex;flex-wrap:wrap;align-items:center;gap:8px;background:var(--paper);border:1px dashed var(--line);border-radius:10px;padding:10px 12px}
.fb-q{font-weight:700;margin-right:auto}.fb textarea{flex-basis:100%}
button{font:inherit;font-weight:700;border-radius:999px;border:2px solid var(--line);background:var(--paper);color:var(--fg);padding:6px 16px;cursor:pointer}
button:focus-visible,textarea:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
button.ok[aria-pressed="true"]{background:var(--ok);border-color:var(--ok);color:var(--paper)}button.chg[aria-pressed="true"]{background:var(--chg);border-color:var(--chg);color:var(--paper)}
textarea{font:inherit;width:100%;border:1px solid var(--line);border-radius:8px;padding:8px;background:var(--bg);color:var(--fg)}
.answer{background:var(--paper);border:2px solid var(--accent);border-radius:14px;padding:20px}
.out{margin:0;white-space:pre-wrap;background:var(--bg);border-radius:8px;padding:12px;font:15px var(--m);min-height:3em}
.primary{background:var(--accent);border-color:var(--accent);color:var(--paper);font-size:18px;padding:10px 22px}.state{font-weight:700}
.copied{color:var(--ok);font-weight:700}.hint{font-size:14px;color:var(--muted)}
@media (max-width:640px){.step{grid-template-columns:40px 1fr}}
@media (prefers-reduced-motion:no-preference){button{transition:background .15s}}
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

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Mono:wght@400;700'
         '&family=Atkinson+Hyperlegible+Next:wght@400;700&display=swap">')


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
