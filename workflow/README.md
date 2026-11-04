# Workflow: vom Laborablauf zur openBIS-Struktur

Vier Phasen, acht Schritte, fünf Prüfpunkte (◆). Der Agent arbeitet in der Cloud nur mit Dateien. Was openBIS
berührt, macht ein Mensch im BAM-Netz mit `tools/bruecke.py` (ein Befehl) oder `notebooks/openbis_bruecke.ipynb`.
Alles, was der Mensch tut, auf einer Seite: [MENSCH.md](MENSCH.md). Freigaben gibt er im Chat; Aufgaben bekommt er als
`projects/<name>/AUFGABE.md`.

| # | Schritt | Karte | Wer | openBIS | Ergebnis (in `projects/<name>/`) | Prüfpunkt |
|---|---|---|---|---|---|---|
| **I** | **Verstehen** | | | | | |
| 1 | Standard laden | [01_standard.md](01_standard.md) | Agent | – | `generated/CATALOG.md` (gepinnter Stand) | |
| 2 | Ablauf erklären (Interview) | [02_interview.md](02_interview.md) | Mensch + Agent | – | `ablauf.md`, `interview.md`, `prd.md` | ◆ **A** PRD freigeben |
| **II** | **Entwerfen** | | | | | |
| 3 | Ist-Stand der Instanz | [03_ist_stand.md](03_ist_stand.md) | Mensch liest, Agent wertet aus | lesen | `inventory_<instanz>.json`, `inventory.md` | |
| 4 | Struktur entwerfen | [04_struktur.md](04_struktur.md) | Agent | – | `requirements.json`, `design.json`, `design.md` | ◆ **B** Struktur passt fachlich |
| 5 | Abgleich | [05_abgleich.md](05_abgleich.md) | Agent | – | `gap-report.md` | ◆ **C** jedes NEU ist wirklich neu |
| **III** | **Beantragen** | | | | | |
| 6 | Antrag an den Admin | [06_antrag.md](06_antrag.md) | Agent baut, Mensch sendet | Admin | `datamodel/`, `spec.json`, `request/` | ◆ **D** Mensch sendet |
| 7 | Lieferung prüfen | [07_lieferung.md](07_lieferung.md) | Mensch liest, Agent vergleicht | lesen | `delivery_check.md` | (zurück zu 6, falls etwas fehlt) |
| **IV** | **Anlegen** | | | | | |
| 8 | Struktur anlegen | [08_anlegen.md](08_anlegen.md) | Agent baut, Mensch führt aus | schreiben | `structure.json`, `reports/apply_<datum>.json` | ◆ **E** Trockenlauf freigeben |

Fehlen nach Schritt 7 nur Geräte (GERÄT FEHLT), geht es direkt mit Schritt 8 weiter: Die Geräte legt der
Mensch selbst an (als Data Store Steward/Group Admin im Equipment-Projekt des Fachbereichs).

## Zugänge

| Zugang | Schritte | Wer |
|---|---|---|
| keiner | 1, 2, 4, 5, 6 | jeder Agent, auch in der Cloud |
| openBIS lesen | 3, 7, 8 (Prüfung, Trockenlauf) | Mensch im BAM-Netz: `bruecke.py … lesen/pruefen/trockenlauf` oder Notebook Teil 1–3 |
| Admin | zwischen 6 und 7 | BAM-Admin über bam-masterdata (Issue + PR/Excel), Mail an datastore@bam.de |
| openBIS schreiben | 8 | Mensch im BAM-Netz: `bruecke.py … anlegen` oder Notebook Teil 4, nur nach ◆ E |

Instanzen: zum Testen `https://playground.datastore.bam.de` (VPN), später die Hauptinstanz. Welche gilt,
steht in `projects/<name>/project.yaml`.

## Neues Projekt

```bash
cp -r templates projects/<name>          # <name>: kleinbuchstaben_mit_unterstrich
# dann in projects/<name>/project.yaml Instanz, Space, Projekt-Code, Equipment-Projekt(e) eintragen
```

Danach mit Schritt 1 beginnen. `STATUS.md` ist die Wahrheit über den Fortschritt: Jeder Agent liest sie
zuerst und schreibt sie zuletzt.

## Strukturprinzipien (gelten für jedes Projekt)

| # | Prinzip |
|---|---|
| P1 | Übersichtlich lesbar statt pauschal flach: Space → Projekt → Collection (= Serie) → Objekte; wie die Objekte einer Probe verbunden sind, wählt der Agent aus den Mustern in [strukturmuster.md](strukturmuster.md) (Prozesslinie, Probe als Mittelpunkt, Zustände des Materials, Bezüge als Felder …) und zeigt 2–4 Varianten. Eltern/Kind für Herkunft und Reihenfolge, Felder vom Typ OBJECT für „wurde benutzt“. Tiefe ist erlaubt, wenn sie eine Linie ist. |
| P2 | Flache Typ-Hierarchie: neue Typen erben direkt von einer BAM-Basisklasse, so wenige neue Typen wie möglich. |
| P3 | Was die Probe beschreibt, ist Property der Probe. Die Collection-Tabelle ist die Versuchsmatrix. |
| P4 | Eigenes Schritt-Objekt nur, wo Gerät, Zeitraum, Bearbeiter*in und Dateien zusammengehören. Mehrere Ablaufschritte am selben Arbeitsplatz: ein Objekt mit einer Sektion je Schritt, in Ablauf-Reihenfolge. |
| P5 | Ablauf sichtbar: Sektionen stehen in Ablauf-Reihenfolge, die Probe hat ein Feld „Next step“ (Auswahl mit Schrittnummern), ein Ablaufplan-Objekt beschreibt alle Schritte. Sektionsnamen selbst ohne Nummern (Regel des `checker`). |
| P6 | Standard zuerst: Geräte, Materialien, Standard-Schritte, Collection- und Dataset-Typen aus bam-masterdata. Nicht standardisierte Typen auf der Instanz werden nicht weiterverwendet. |
| P7 | Tabellen und Messreihen sind Dateien, keine Properties. |
| P8 | Jeder Name auf Deutsch und Englisch: angezeigt als „Deutsch / Englisch“, in den Masterdaten `property_label` + `property_label_de` (Begriffe `label` + `label_de`), Beschreibungen `English//Deutsch`. Sektionen in openBIS englisch, Title Case, nur Buchstaben. |

## Dateien eines Projekts

| Datei | Entsteht in | Inhalt |
|---|---|---|
| `project.yaml` | Anlage | Instanz, Space, Projekt, Equipment-Projekte, bam-masterdata-Stand |
| `STATUS.md` | immer | Schritt, Prüfpunkte, wer, wann, offene Fragen |
| `AUFGABE.md` | bei Bedarf | die eine offene Aufgabe für den Menschen (Vorlage `AUFGABE_VORLAGE.md`) |
| `schema.*` | 2 (Eingabe) | draw.io, Mermaid, Bild oder PDF des Ablaufs (optional) |
| `ablauf.md` | 2 | die eine Quelle für den Ablauf: nummerierte Schritte mit Daten, Geräten, Dateien |
| `interview.md` | 2 | Frage, Antwort, Quelle; Vorschläge des Agenten markiert |
| `prd.md` | 2 | Anforderungen nach Vorlage (was, nicht welche Typen) |
| `inventory_<instanz>.json` | 3, 7 (Notebook) | Export der Instanz (nur lesen) |
| `inventory.md` | 3 | Auswertung des Exports durch den Agenten |
| `requirements.json`, `design.json`, `design.md` | 4 | Anforderungen, 2–4 Varianten (eine empfohlen), Struktur, Schritt → Ort |
| `gap-report.md` | 5 | Abgleich mit Standard und Instanz |
| `datamodel/`, `spec.json` | 6 | neue Klassen (PR-fähig), Soll-Zustand der Masterdaten |
| `request/` | 6 | `issue.md`, `mail.txt`, `masterdata.xlsx`, `checker.log` |
| `delivery_check.md` | 7 | Soll/Ist: bereit oder was fehlt |
| `structure.json` | 8 | Projekt, Collections, Objekte, Eltern-Links (Format: `tools/openbis_bridge.py`) |
| `reports/dryrun_<datum>.json`, `reports/apply_<datum>.json` | 8 (Befehl/Notebook) | Plan des Trockenlaufs, was angelegt oder übersprungen wurde |
