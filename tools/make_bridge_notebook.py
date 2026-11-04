"""Build notebooks/openbis_bruecke.ipynb (the bridge notebook) from this source.

Edit the cells here, not the .ipynb JSON, then run:
  python tools/make_bridge_notebook.py notebooks/openbis_bruecke.ipynb
"""
import nbformat as nbf, sys
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
cells = [
md("""# openBIS-Brücke

Läuft **im BAM-Netz** (VPN). Der KI-Agent in der Cloud kommt nicht an openBIS heran; dieses Notebook ist die einzige Stelle, die die Instanz berührt.

| Teil | Wann (Workflow-Schritt) | Was | Schreibt in openBIS? |
|---|---|---|---|
| 1 Lesen | 3 und 7 | Typen, Properties, Vokabulare, Geräte deines Fachbereichs, vergebene Codes | nein |
| 2 Prüfen | 7 und vor 8 | Soll (`spec.json`, `structure.json`) gegen Ist | nein |
| 3 Trockenlauf | 8 | zeigt, was angelegt würde | nein |
| 4 Anlegen | 8, nach **Prüfpunkt E** | legt nur Fehlendes an (Projekt, Collections, Objekte) | **ja** |

Nichts wird geändert oder gelöscht, keine Typen werden angelegt. Der Token wird nur abgefragt und nirgends gespeichert.

**Vorher:** `git pull` im Repo. **Nachher:** die neuen Dateien committen und pushen (Zelle ganz unten)."""),
code("""# Einmalig, falls noch nicht installiert:
# %pip install pybis==1.37.4 pyyaml"""),
md("## Einstellungen"),
code("""PROJECT = "fb72_welded_fatigue"   # Ordner unter projects/

import getpass, json, sys
from datetime import date
from pathlib import Path
import yaml

REPO = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(REPO / "tools"))
import openbis_bridge as ob

P = REPO / "projects" / PROJECT
cfg = yaml.safe_load((P / "project.yaml").read_text(encoding="utf-8"))
STRUCTURE = (P / cfg.get("structure", "structure.json")).resolve()
SPEC = (P / cfg.get("spec", "spec.json")).resolve()
INSTANCE = cfg["instance"].rstrip("/")
INV_FILE = P / f"inventory_{INSTANCE.split('//')[-1].split('.')[0]}.json"
READ = [f"/{cfg['space']}/{cfg['project']}".upper()] + [p.upper() for p in cfg.get("inventory_projects") or []]
print("Instanz:", INSTANCE)
print("Lese Projekte:", READ)
print("structure.json:", STRUCTURE if STRUCTURE.exists() else "(noch keine)")
print("spec.json:", SPEC if SPEC.exists() else "(noch keine)")"""),
md("## Anmelden\nToken leer lassen, um dich mit BAM-Benutzername und Passwort anzumelden."),
code("""token = getpass.getpass("openBIS Personal Access Token (leer = Passwort-Login): ").strip()
if token:
    o, call = ob.connect(INSTANCE, token)
else:
    from pybis import Openbis
    o = Openbis(INSTANCE)
    o.login(input("Benutzername: "), getpass.getpass("Passwort: "), save_token=False)
    call = ob.v3_caller(o)
del token
print("angemeldet:", o.is_session_active())"""),
md("## 1 Lesen (Schritt 3 und 7)"),
code("""inv = ob.read_inventory(call, INSTANCE, READ)
INV_FILE.write_text(json.dumps(inv, indent=1, ensure_ascii=False) + "\\n", encoding="utf-8")
print(f"{len(inv['objectTypes'])} Object-Types, {len(inv['vocabularies'])} Vokabulare, "
      f"{len(inv['collections'])} Collections und {len(inv['objects'])} Objekte in {len(READ)} Projekten")
print("gespeichert:", INV_FILE.relative_to(REPO))"""),
md("## 2 Prüfen (Schritt 7, vor 8)"),
code("""from IPython.display import Markdown, display
spec = json.loads(SPEC.read_text(encoding="utf-8")) if SPEC.exists() else None
structure = json.loads(STRUCTURE.read_text(encoding="utf-8")) if STRUCTURE.exists() else None
rep = ob.check(inv, spec, structure)
(P / "delivery_check.md").write_text(ob.render_check_md(rep) + "\\n", encoding="utf-8")
display(Markdown(ob.render_check_md(rep)))"""),
md("## 3 Trockenlauf (Schritt 8)\nÄndert nichts. Lies die Liste: Passt der Space, passt das Projekt, gibt es Konflikte?"),
code("""plan = ob.apply(call, structure, STRUCTURE.parent, dry_run=True)
print(f"würde anlegen: {len(plan['created'])}, schon da: {len(plan['skipped'])}, "
      f"verworfene Properties: {len(plan['droppedProps'])}")
for i in plan["created"]: print("  +", i)
for i in plan["droppedProps"]: print("  ! nicht zugewiesen:", i)"""),
md("""## 4 Anlegen (nur nach ◆ Prüfpunkt E)

Erst wenn der Trockenlauf stimmt: `FREIGABE = True` setzen und die Zelle ausführen. Die Zelle verweigert das Anlegen, solange Teil 2 Lücken meldet. Auf der Hauptinstanz erst, wenn es auf dem Playground durchgelaufen ist."""),
code("""FREIGABE = False
TROTZ_LUECKEN = False   # nur für Tests auf dem Playground: anlegen, obwohl Teil 2 Lücken meldet
assert FREIGABE, "Erst den Trockenlauf prüfen, dann FREIGABE = True setzen."
assert rep["ready"] or TROTZ_LUECKEN, "Teil 2 meldet Lücken: erst beheben (sonst fehlen Properties an den Objekten)."
done = ob.apply(call, structure, STRUCTURE.parent, dry_run=False)
done["instance"] = INSTANCE
out = P / "reports" / f"apply_{date.today().isoformat()}.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(done, indent=1, ensure_ascii=False) + "\\n", encoding="utf-8")
print(f"angelegt: {len(done['created'])}, übersprungen: {len(done['skipped'])}  ->", out.relative_to(REPO))"""),
md("## Abmelden und Dateien zurück ins Repo"),
code("""o.logout()
print("Jetzt im Terminal:")
print(f"  git add projects/{PROJECT}")
print(f'  git commit -m "{PROJECT}: openBIS-Export {date.today().isoformat()}"')
print("  git push")"""),
]
for i, c in enumerate(cells):
    c.id = f"cell-{i:02d}"  # stable ids: same source -> same file
nb = nbf.v4.new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
     "language_info": {"name": "python"}})
nbf.validate(nb)
nbf.write(nb, sys.argv[1])
