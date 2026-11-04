# Formate der Projektdateien

Gelten für jeden Agenten. `python tools/check_files.py <projekt>` prüft ein Projekt dagegen; `tools/render_review.py`
erzeugt keine Prüfseite, solange Fehler bestehen.

| Schema | Datei | Wer schreibt | Wofür |
|---|---|---|---|
| `project.schema.json` | `projects/<name>/project.yaml` | Mensch + Agent bei der Anlage | Instanz, Space, Projekt, Titel, Fachbereich |
| `design.schema.json` | `design.json` | Agent, Schritt 4 | Prüfseite B, Abgleich, Antrag; jeder neue Name zweisprachig; 2–4 `variants` der Datenstruktur, genau eine `recommended` |
| `structure.schema.json` | `structure.json` | Agent, Schritt 8 | `tools/bruecke.py` / Notebook (Details im Kopf von `tools/openbis_bridge.py`) |

`spec.json` (`tools/export_spec.py`) und `request/request.json` (`tools/build_request.py`) entstehen nur durch Skripte
und brauchen deshalb kein Schema. Zusätze in den Dateien sind erlaubt; die Schemas legen nur fest, was vorhanden sein muss.
Beispiel, das alle Schemas erfüllt: `generated/welded_fatigue_v2/design.json`, `structure.json`, `projects/fb72_welded_fatigue/project.yaml`.
