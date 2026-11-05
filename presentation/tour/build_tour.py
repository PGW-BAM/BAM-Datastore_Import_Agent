"""Build the self-contained speaker tour (HTML with embedded screenshots).

    python presentation/tour/build_tour.py
-> presentation/tour/FB72_openBIS_Demo_Tour.html
-> presentation/tour/workflow_plan_procedure.html  (formatted text to paste into the protocol)
"""

import base64
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
IMG = HERE / "img"
URL = "https://dev1.datastore.bam.de/openbis/webapp/eln-lims/"


def img(name: str) -> str:
    data = base64.b64encode((IMG / name).read_bytes()).decode()
    return f"data:image/jpeg;base64,{data}"


# station -> (title, minutes, deck slide, list of steps)
# step: (image, click, see, say)
STATIONS = [
    ("Projekt und Serien", "0:30", "Slide 8", [
        ("01.jpg", "Oben <b>LAB NOTEBOOK</b> → im Baum <b>Fb 72</b> aufklappen → Projekt <b>Welded Fatigue</b> anklicken.",
         "Ein Projekt, darunter zwei Collections = zwei Prüfserien (Stumpfstoß, Kreuzstoß).",
         "Everything for our S-N tests lives in one project – one collection per test series."),
        ("02.jpg", "Auf der Projektseite kurz die <b>Description</b> zeigen, dann im Baum <b>Series 1 – butt weld (DEMO)</b> anklicken.",
         "Beschreibung des Projekts; die Serie ist die Collection.",
         "A test series is simply a collection – no deeper folder structure."),
        ("03.jpg", "In der Serientabelle auf <b>S1B-01</b> klicken. <span class='opt'>Optional: über <b>COLUMNS</b> die Spalten aus der Vorbereitung einblenden.</span>",
         "Alle Objekte der Serie in einer Tabelle: Proben und ihre Schritt-Objekte.",
         "The series table is our test matrix – every specimen and every step of the series in one list."),
    ]),
    ("Probe: „Next step“ und nummerierte Sektionen", "0:45", "Slide 9", [
        ("04.jpg", "Links unten <b>«</b> klicken (Navigation einklappen) und nach unten scrollen bis <b>Workflow status</b>.",
         "<b>Next step</b> steht ganz oben (hier: <i>Done</i>), darunter Identifikation und die Sektion <b>01 Pre-quality check</b>.",
         "Every specimen shows its next step at the very top – here this one is done."),
        ("05.jpg", "Weiter scrollen.",
         "Sektionen <b>04 Weld analysis</b>, <b>05 Series assignment</b>, <b>06 Geometry</b> – die Schrittnummern aus dem Ablaufplan.",
         "The steps done on the specimen itself are numbered sections – the 12-step plan stays readable in the form."),
    ]),
    ("Flache Struktur: Hierarchie-Graph", "0:30", "Slide 8", [
        ("06.jpg", "Oben <b>More …</b> → <b>Hierarchy Graph</b>.", "Menü der Probe.", ""),
        ("07.jpg", "Im Graph-Navigator 2× auf <b>–</b> klicken, bis alle drei Kinder sichtbar sind. Dann auf <b>07-11 Cyclic fatigue test</b> klicken.",
         "Probe → drei Schritt-Objekte (SCAN, TEST, FRACTURE). Genau eine Ebene.",
         "One specimen, three step objects, one level – no chains of steps."),
    ]),
    ("Versuch: Geräte als Eltern, Ergebnisse in Sektionen", "0:45", "Slides 8–9", [
        ("08.jpg", "Oben auf der Versuchsseite die Tabelle <b>Parents</b> zeigen.",
         "7 Eltern: die Probe plus Klebstoff, Risslumineszenz, DMS, Kamera, IMC-Verstärker, Prüfmaschine – alle aus dem Inventar.",
         "Instruments and consumables are linked as parents – created once in the inventory, reused for every test."),
        ("09.jpg", "Nach unten scrollen zu <b>09</b>, <b>10</b>, <b>11</b>.",
         "Sektionen 07–11; Abbruchgrund <i>Total fracture</i>, Brutto/Netto-Schwingspiele, Zyklen bis 10 % DMS-Abfall.",
         "Steps 07 to 11 happen at the test rig, so they share one object – one section per step. The parser fills section 11 from the IMC results."),
    ]),
    ("Laufende Probe finden", "0:30", "Slide 9", [
        ("10.jpg", "Oben in <b>Global Search</b> <code>S1B-04</code> eingeben → <b>Enter</b>.", "Globale Suche über alles.", ""),
        ("11.jpg", "In den Ergebnissen die Probe <b>S1B-04</b> anklicken (Entity Type <code>SAMPLE.WELDED_FATIGUE_SPECIMEN</code>).",
         "3 Treffer: Probe, SCAN und TEST.", ""),
        ("12.jpg", "Bis <b>Workflow status</b> scrollen.",
         "<b>Next step: 10 Cyclic fatigue test</b> – diese Probe ist gerade auf der Maschine.",
         "Specimen S1B-04 is on the machine right now – its next step says so. One glance per specimen."),
    ]),
    ("Inventar: Gerät → wo wurde es eingesetzt?", "0:30", "Slide 8", [
        ("13.jpg", "Oben <b>INVENTORY</b> → <b>Materials</b> → <b>7 2 Equipment</b> aufklappen → <b>Instruments / Geräte</b>.",
         "Geräte-Collections von FB 7.2.", ""),
        ("14.jpg", "In der Liste <b>GOM_ATOS_5</b> anklicken.",
         "Geräte mit Standardtypen (Instrument, Camera, Measuring amplifier). <span class='warn'>Der Button heißt hier noch „+ Instrument Dummy“ – Rest des alten Modells, siehe Vorbereitung.</span>",
         ""),
        ("15.jpg", "Tabelle <b>Children</b> zeigen.",
         "Alle 5 Scans, in denen der Scanner verwendet wurde.",
         "The link works both ways: the scanner knows every scan it was used for."),
    ]),
    ("Ablaufplan im System", "0:30", "Slides 3, 8", [
        ("16.jpg", "Global Search: <code>WORKFLOW_PLAN</code> → Enter → Ergebnis <b>Workflow plan …</b> anklicken.",
         "Der Ablaufplan ist ein Protokoll-Objekt im Projekt.", ""),
        ("17.jpg", "Feld <b>Procedure</b> zeigen.",
         "Für jeden der 12 Schritte: wo (Objekt + Sektion), welche Geräte, welche Dateien. <span class='warn'>Im Screenshot noch ohne Zeilenumbrüche – vor dem Vortrag Text ersetzen (Vorbereitung, Punkt 3).</span>",
         "The workflow plan itself is in openBIS: for each of the twelve steps, where the data and files go."),
    ]),
    ("Masterdaten: das Ablauf-Vokabular", "0:30", "Slide 5", [
        ("18.jpg", "Oben <b>TOOLS</b> → <b>Vocabulary Browser</b> → im Filter <code>WELDED_FATIGUE</code> eingeben → Eintrag anklicken.",
         "Das Vokabular hinter „Next step“.", ""),
        ("19.jpg", "Auf die Spaltenüberschrift <b>Label</b> klicken (sortiert).",
         "13 Terme: 01 … 12 und Done – der Ablaufplan als geordnete Liste.",
         "'Next step' is a controlled vocabulary – the agents created it from our workflow, ordered 01 to 12 plus done."),
    ]),
]

PREP = [
    ("Anmelden", f"<a href='{URL}'>{URL}</a> im Browser öffnen, als Admin anmelden (Zugangsdaten nicht im Vortrag zeigen). Browser im Vollbild, Zoom 100–110 %."),
    ("Tabs vorbereiten (empfohlen)", "Den Startpunkt (Lab Notebook) in einem Tab offen lassen; bei Problemen kann man jederzeit dorthin zurück. Fallback: dieses Dokument bzw. die Folien 8–9 zeigen."),
    ("Ablaufplan-Text formatieren", "Protokoll <code>WORKFLOW_PLAN</code> öffnen → <b>Edit</b> → Feld <b>Procedure</b> leeren → Inhalt von <code>workflow_plan_procedure.html</code> (im Browser öffnen, alles markieren, kopieren) einfügen → <b>Save</b>. Danach sind die 12 Schritte zeilenweise lesbar."),
    ("Serientabelle (optional)", "In <b>Series 1 – butt weld (DEMO)</b> über <b>COLUMNS</b> nur einblenden: <i>Code, Name, Next step, Load level, Test order, Quality level ISO 5817 Annex C, Net number of cycles, Termination reason</i>. Die Einstellung wird im Benutzerprofil gespeichert."),
    ("Bekannte Reste des alten Modells", "Im Baum stehen noch die Projekte <i>Catalog</i> und <i>Cyclic Fatigue Tests</i> (leer, im Papierkorb) und im Inventar der Button „+ Instrument Dummy“. Einfach nicht anklicken – oder vorher aufräumen (<code>generated/welded_fatigue_v2/CLEANUP_dev1.md</code>)."),
    ("Demo-Daten", "Alle Werte der Serie sind fiktiv (DEMO). Beim Zeigen einmal erwähnen."),
]


def build() -> None:
    n = 0
    nav, cards = [], []
    for si, (title, minutes, slide, steps) in enumerate(STATIONS, 1):
        nav.append(f"<li><a href='#s{si}'><span class='num'>{si}</span>{html.escape(title)}<span class='t'>{minutes}</span></a></li>")
        step_html = []
        for image, click, see, say in steps:
            n += 1
            say_html = f"<div class='say'><span>Say</span>“{html.escape(say)}”</div>" if say else ""
            step_html.append(f"""
      <article class='step' id='step{n}' data-step='{n}'>
        <figure><img src='{img(image)}' alt='Screenshot Schritt {n}' loading='lazy'><figcaption>Rote Markierung = hier klicken bzw. hierauf zeigen</figcaption></figure>
        <div class='txt'>
          <div class='badge'>{n}</div>
          <p class='click'><span>Klicken</span>{click}</p>
          <p class='see'><span>Zu sehen</span>{see}</p>
          {say_html}
        </div>
      </article>""")
        cards.append(f"""
    <section class='station' id='s{si}'>
      <header><span class='snum'>Station {si}</span><h2>{html.escape(title)}</h2><span class='meta'>≈ {minutes} · {slide}</span></header>
      {''.join(step_html)}
    </section>""")
    prep = "".join(f"<li><b>{html.escape(t)}.</b> {d}</li>" for t, d in PREP)
    out = TEMPLATE.replace("%%NAV%%", "".join(nav)).replace("%%CARDS%%", "".join(cards)) \
        .replace("%%PREP%%", prep).replace("%%LOGIN%%", img("00_login.jpg")).replace("%%TOTAL%%", str(n)) \
        .replace("%%URL%%", URL)
    (HERE / "FB72_openBIS_Demo_Tour.html").write_text(out, encoding="utf-8")

    # formatted procedure text (HTML) to paste into the protocol
    src = (REPO / "generated/welded_fatigue_v2/sop_workflow_plan.txt").read_text(encoding="utf-8")
    src = src.replace("<Probe>", "S1x-NN")
    parts, items = [], []
    for line in src.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("["):
            items.append([html.escape(s), []])
        elif items and (s.startswith("where/wo") or s.startswith("equipment") or s.startswith("files")):
            items[-1][1].append(html.escape(s))
        else:
            parts.append(f"<p>{html.escape(s)}</p>")
    lis = "".join(f"<li><b>{h}</b><br>{'<br>'.join(sub)}</li>" for h, sub in items)
    (HERE / "workflow_plan_procedure.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>Workflow plan – procedure text</title>"
        "<body style='font-family:Arial;max-width:900px;margin:24px'>"
        "<p style='color:#a00'><i>Alles unterhalb der Linie markieren, kopieren und in das Feld „Procedure“ des Protokolls WORKFLOW_PLAN einfügen.</i></p><hr>"
        + "".join(parts) + f"<ol style='list-style:none;padding-left:0'>{lis}</ol></body>", encoding="utf-8")
    print(f"tour: {n} steps, {len(STATIONS)} stations")


TEMPLATE = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>openBIS Demo Tour</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--ink:#1d2433;--mute:#5b6577;--line:#e2e6ec;--accent:#1f3b73;--accent2:#e5383b;--say:#eef4ff;--warn:#fff4e5;--warnink:#8a4b00}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11151c;--card:#1a2029;--ink:#e6e9ef;--mute:#a3acbb;--line:#2b3340;--accent:#8fb0ff;--say:#1d2a44;--warn:#3a2a12;--warnink:#ffcf8a}}
:root[data-theme="dark"]{--bg:#11151c;--card:#1a2029;--ink:#e6e9ef;--mute:#a3acbb;--line:#2b3340;--accent:#8fb0ff;--say:#1d2a44;--warn:#3a2a12;--warnink:#ffcf8a}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 "Segoe UI",system-ui,Arial,sans-serif}
.wrap{display:grid;grid-template-columns:280px 1fr;max-width:1500px;margin:0 auto}
nav{position:sticky;top:0;height:100vh;overflow:auto;padding:24px 16px;border-right:1px solid var(--line)}
nav h1{font-size:17px;margin:0 0 4px;color:var(--accent)}
nav p{margin:0 0 16px;color:var(--mute);font-size:13px}
nav ol{list-style:none;padding:0;margin:0}
nav a{display:flex;gap:8px;align-items:center;padding:7px 8px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:14px}
nav a:hover{background:var(--card)}
nav .num{flex:none;width:22px;height:22px;border-radius:11px;background:var(--accent);color:var(--card);font-size:12px;font-weight:700;display:grid;place-items:center}
nav .t{margin-left:auto;color:var(--mute);font-size:12px}
nav .ctl{margin-top:20px;display:flex;flex-direction:column;gap:8px}
button{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:8px 10px;cursor:pointer}
button.primary{background:var(--accent);color:var(--card);border-color:var(--accent)}
main{padding:28px 32px 80px;min-width:0}
.hero{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 24px;margin-bottom:22px}
.hero h1{margin:0 0 6px;font-size:24px}
.hero .sub{color:var(--mute);margin:0 0 14px}
.hero .grid{display:grid;grid-template-columns:1.2fr 1fr;gap:20px;align-items:start}
.hero img{width:100%;border:1px solid var(--line);border-radius:8px}
.prep li{margin:0 0 8px}
.station{margin:28px 0}
.station header{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:2px solid var(--accent);padding-bottom:6px;margin-bottom:14px}
.station h2{margin:0;font-size:20px}
.snum{color:var(--accent);font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.06em}
.meta{margin-left:auto;color:var(--mute);font-size:13px}
.step{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:18px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:0 0 14px}
.step figure{margin:0}
.step img{width:100%;height:auto;border-radius:6px;border:1px solid var(--line);display:block;cursor:zoom-in}
figcaption{font-size:12px;color:var(--mute);margin-top:4px}
.txt{position:relative;padding-top:4px}
.badge{width:34px;height:34px;border-radius:17px;background:var(--accent2);color:#fff;font-weight:700;display:grid;place-items:center;margin-bottom:10px}
.txt p{margin:0 0 12px}
.txt p span,.say span{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--mute);margin-bottom:2px}
.click{font-size:16px}
.say{background:var(--say);border-radius:8px;padding:10px 12px;font-style:italic}
.opt{display:block;color:var(--mute);font-size:13px;margin-top:4px}
.warn{display:block;background:var(--warn);color:var(--warnink);border-radius:6px;padding:6px 8px;margin-top:6px;font-size:13px}
code{font-family:Consolas,monospace;font-size:.92em;background:var(--bg);padding:1px 5px;border-radius:4px}
a{color:var(--accent)}
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;z-index:9;cursor:zoom-out}
.lightbox img{max-width:96vw;max-height:94vh}
body.focus .station,body.focus .hero{display:none}
body.focus .station.cur{display:block}
body.focus .step{display:none}
body.focus .step.cur{display:grid;grid-template-columns:minmax(0,2.4fr) minmax(0,1fr)}
body.focus main{max-width:none}
.focusbar{display:none;position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 10px;gap:8px;align-items:center;box-shadow:0 6px 24px rgba(0,0,0,.18)}
body.focus .focusbar{display:flex}
@media (max-width:900px){.wrap{grid-template-columns:1fr}nav{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}.step,.hero .grid{grid-template-columns:1fr}main{padding:16px}}
@media print{nav,.focusbar{display:none}.wrap{grid-template-columns:1fr}.step{break-inside:avoid}}
</style>
</head>
<body>
<div class="wrap">
<nav>
  <h1>openBIS Demo-Tour</h1>
  <p>FB 7.2 · S-N tests on welded joints<br>Nur für die/den Vortragende(n) · ca. 4–5 min live</p>
  <ol>%%NAV%%</ol>
  <div class="ctl">
    <button class="primary" id="focusBtn">▶ Schritt-Modus (← →)</button>
    <button id="themeBtn">Hell / Dunkel</button>
  </div>
</nav>
<main>
  <section class="hero">
    <h1>Klick-Tour durch openBIS</h1>
    <p class="sub">Begleitet Folien 8–9 der englischen Präsentation. %%TOTAL%% Schritte in 8 Stationen – jede Station ist einzeln vorführbar. Rote Rahmen = Klickziel.</p>
    <div class="grid">
      <div>
        <h3 style="margin:0 0 8px">Vor dem Vortrag</h3>
        <ol class="prep">%%PREP%%</ol>
      </div>
      <figure style="margin:0"><img src="%%LOGIN%%" alt="openBIS Anmeldung"><figcaption>Start: %%URL%%</figcaption></figure>
    </div>
  </section>
  %%CARDS%%
  <p style="color:var(--mute);font-size:13px">Screenshots: openBIS-Testinstanz dev1, 13.10.2026. Alle Serienwerte sind fiktiv (DEMO). Erzeugt mit <code>presentation/tour/build_tour.py</code>.</p>
</main>
</div>
<div class="focusbar"><button id="prev">←</button><span id="pos"></span><button id="next">→</button><button id="exit">✕</button></div>
<div class="lightbox" id="lb"><img alt=""></div>
<script>
(function(){
  const steps=[...document.querySelectorAll('.step')]; let i=0;
  const show=()=>{steps.forEach((s,k)=>s.classList.toggle('cur',k===i));
    document.querySelectorAll('.station').forEach(st=>st.classList.toggle('cur',st.contains(steps[i])));
    document.getElementById('pos').textContent=(i+1)+' / '+steps.length; window.scrollTo(0,0);};
  const on=()=>{document.body.classList.add('focus');show();}, off=()=>document.body.classList.remove('focus');
  document.getElementById('focusBtn').onclick=on; document.getElementById('exit').onclick=off;
  document.getElementById('prev').onclick=()=>{i=Math.max(0,i-1);show();};
  document.getElementById('next').onclick=()=>{i=Math.min(steps.length-1,i+1);show();};
  document.addEventListener('keydown',e=>{ if(!document.body.classList.contains('focus')) return;
    if(e.key==='ArrowRight'){i=Math.min(steps.length-1,i+1);show();} if(e.key==='ArrowLeft'){i=Math.max(0,i-1);show();} if(e.key==='Escape') off();});
  const lb=document.getElementById('lb');
  document.querySelectorAll('.step img,.hero img').forEach(im=>im.onclick=()=>{lb.firstElementChild.src=im.src;lb.style.display='flex';});
  lb.onclick=()=>lb.style.display='none';
  document.getElementById('themeBtn').onclick=()=>{const r=document.documentElement;
    const dark=r.dataset.theme? r.dataset.theme==='dark' : matchMedia('(prefers-color-scheme: dark)').matches; r.dataset.theme=dark?'light':'dark';};
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
