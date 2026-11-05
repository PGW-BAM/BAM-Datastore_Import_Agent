# Vortrag (10 min): Wöhlerversuche an Schweißverbindungen in openBIS – mit KI-Agenten

> Folienplan für FB 7.2 Ingenieurbau. 4 min Versuche · 6 min Lösung.
> Jede Folie: **Kernaussage** (1 Satz), Inhalt, Bildquelle, Sprechernotiz.
> Alle Zahlen sind am 06.10.2026 gegen dev1 und `bam-masterdata` @ `d7a871b` erhoben (Quellen am Ende).

---

## Teil A – Die Versuche (≈ 4 min, 4 Folien)

### Folie 1 – Titel (0:20)
**Wöhlerversuche an Schweißverbindungen – vom Versuchsablauf zur Datenstruktur in openBIS, unterstützt durch KI-Agenten**
FB 7.2 Ingenieurbau · BAM Data Store · Datum

### Folie 2 – Was wir prüfen (1:00)
**Kernaussage:** Wir bestimmen Wöhlerlinien geschweißter Stumpf- und Kreuzstöße – jede Probe zählt, Streuung entsteht schon vor dem Versuch.
- Proben: Stumpfstoß / Kreuzstoß, Herkunftsblech, Bewertungsgruppe nach ISO 5817 (B/C/D, Anhang C: C63/B90/B125)
- Serie = mehrere Lastniveaus (hoch / mittel / niedrig), randomisierte Prüfreihenfolge
- Ergebnis je Probe: Schwingspielzahl + Abbruchgrund (Bruch / Riss / Durchläufer)
- *Bild:* Foto Probe + Prüfstand (eigenes Foto einsetzen)
- *Sprechernotiz:* Herkunftsblech + Randomisierung → Bias vermeiden; deshalb muss die Zuordnung dokumentiert sein.

### Folie 3 – Der Ablauf in 12 Schritten (1:30)
**Kernaussage:** Zwölf Schritte, vier Arbeitsplätze – und an jedem entstehen Daten und Dateien.

| Phase | Schritte | Geräte / Material | Daten & Dateien |
|---|---|---|---|
| Vorbereitung | 01 Vorqualitätsprüfung · 02 Anfasen/Schleifen | – | Winkelverzug, Kantenversatz (vor/nach Richten), Fotos, Protokoll |
| Charakterisierung | 03 3D-Scan · 04 Nahtanalyse · 05 Serienzuordnung · 06 Geometrie | ZEISS GOM ATOS 5, Messschieber | Scan-Rohdaten, Bewertungsgruppe, Lastniveau, Dicke/Breite ×3 |
| Prüfstand | 07 DMS · 08 Messkette · 09 Einbauspannung · 10 Versuch · 11 Auswertung | HBM-DMS, X60, Risslumineszenz, Luxonis-Kamera, IMC, servohydr. Maschine | Abstände, Abtastrate, Vorspannkraft, Lastprogramm, IMC-Rohdaten, Zyklen |
| Nachuntersuchung | 12 Bruchfläche | Makro-Kamera, Digitalmikroskop | Fotos, Rissausgang, Rastlinien |

- *Bild:* `diagrams/07_ablauf_12_schritte.mmd`
- *Sprechernotiz:* Diese Tabelle ist 1:1 der Inhalt des PRD v2 (§3) – das ist alles, was der Fachbereich schreiben muss.

### Folie 4 – Das Problem (1:10)
**Kernaussage:** Der erste Versuch, das in openBIS abzubilden, war fachlich gut – aber 12 Ebenen tief.
- Jeder Schritt = eigener Typ, Schritt n ist „Elternteil“ von Schritt n+1 → **Kette mit 12 Ebenen**
- **13 Objekte pro Probe**, 189 Objekte für eine Serie – *ohne einen einzigen Messwert*
- Schritte lagen außerhalb der Serie; Reihenfolge per Hand (`STEP_ORDER`); 16 eigene Typen + 17 Dateitypen
- *Bild:* `screenshots/vorher_01_hierarchie_kette.jpg` (+ optional `vorher_02_serie_tabelle.jpg`)
- *Sprechernotiz:* Frage ans Publikum: „Wo trage ich jetzt den Kantenversatz ein – und wo sehe ich, welche Probe als Nächstes auf die Maschine kommt?“

---

## Teil B – Die Lösung (≈ 6 min, 6 Folien)

### Folie 5 – Idee: Agenten prüfen, bevor wir anlegen (1:00)
**Kernaussage:** KI-Agenten gleichen unseren Ablauf mit dem BAM-Standard *und* der Live-Instanz ab und legen nur an, was wirklich fehlt.
- Eingabe: ein PRD in Fachsprache (Ablauf + Prinzipien „flach“, „Reuse-first“)
- Zwei Quellen: `bam-masterdata` (Standard, 141 Objekttypen) + openBIS-Instanz (was ist schon da?)
- Vier Urteile: **REUSE · EXTEND · CREATE · LIVE-ONLY**
- Mensch entscheidet an zwei Stellen (Design, Gap-Report)
- *Bild:* `diagrams/01_system_architecture.mmd`

### Folie 6 – Die Pipeline (1:00)
**Kernaussage:** Sieben Schritte, jeder von einem spezialisierten Agenten oder einem prüfbaren Skript.

`Katalog (Skript) → Live-Inventur → PRD lesen → flache Struktur entwerfen → Gap-Analyse → Python-Klassen (Import-Test) → Anlegen auf openBIS (Trockenlauf, idempotent)`

- *Bild:* `diagrams/03_pipeline_sequence.mmd`
- *Sprechernotiz:* „Zählen“ macht ein Skript (deterministisch), „Entscheiden“ der Agent, „Freigeben“ der Mensch.

### Folie 7 – Ergebnis: flach statt tief (1:15)
**Kernaussage:** Eine Probe, drei Schritte, eine Ebene – und der Ablaufplan bleibt sichtbar.
- *Bild links:* `screenshots/vorher_01_hierarchie_kette.jpg` · *rechts:* `screenshots/nachher_01_hierarchie_flach.jpg`
- Probe trägt Schritte 01/02/04/05/06 als **nummerierte Sektionen**; Feld **„Next step“** oben
- SCAN (03–04) · TEST (07–11, Sektionen 07…11) · FRACTURE (12) als Kinder, Geräte als Eltern
- *Bild:* `diagrams/06_vorher_nachher.mmd`

| | Vorher | Nachher |
|---|---|---|
| Objekte pro Probe | 13 | **4** |
| Verknüpfungstiefe | 12 | **1** |
| Neue Objekttypen | 16 | **2** |
| Neue Dateitypen | 17 | **0** |
| Objekte für die Demo-Serie | 189 (0 Messwerte) | **19** (8 Proben, mit Werten) |

### Folie 8 – „Was kommt als Nächstes?“ (0:45)
**Kernaussage:** Jede Probe zeigt ihren nächsten Schritt; die Serie ist eine Versuchsmatrix.
- *Bild:* `screenshots/nachher_02_probe_formular.jpg` + Serienübersicht (Tabelle unten)

| Probe | Lastniveau | Reihenfolge | Anhang C | Nächster Schritt | Zyklen (netto) | Abbruch |
|---|---|---|---|---|---|---|
| S1B-01 | hoch | 3 | B90 | fertig | 231 900 | Totalbruch |
| S1B-02 | niedrig | 1 | B90 | fertig | 10 000 000 | Durchläufer |
| S1B-03 | mittel | 2 | B125 | 12 Bruchfläche | 1 052 000 | Riss |
| S1B-04 | hoch | 4 | B90 | 10 Versuch läuft | – | – |
| S1B-05 | mittel | 5 | C63 | 07 DMS-Applikation | – | – |
| S1B-06 | – | – | – | 03 3D-Scan | – | – |

*(DEMO – fiktive Werte)*

### Folie 9 – Was die Agenten gefunden haben (1:00)
**Kernaussage:** Der Mehrwert liegt im Prüfen – nicht im Generieren.
- Alter generierter Code war **nie lauffähig** (nicht existierende Klasse; Prüfung war nur Syntax) → jetzt echter Import-Test
- Alter Katalog hat **8 vorhandene Gerätetypen übersehen** (nur direkte Unterklassen) → jetzt AST-Skript, reproduzierbar
- Alte Regel „Labels zweisprachig“ widersprach dem Standard (0 von 1 786 Sektionen) → korrigiert
- dev1 hinkt dem Standard hinterher (z. B. fehlende BAM-Standort-Vokabulare) → Skript überspringt & meldet, statt zu raten
- Wiederverwendet statt neu: Basistypen `Sample`/`MechanicalTest`, Geräte, Hilfsstoffe, Dateitypen, Nahtart-Property
- *Sprechernotiz:* Jeder dieser Punkte ist im Repo belegt (Gap-Report, Commit, Skript-Ausgabe).

### Folie 10 – Übertragbarkeit & nächste Schritte (1:00)
**Kernaussage:** Das Muster ist für jeden Fachbereich wiederverwendbar: Ablauf beschreiben → Agenten prüfen → Mensch gibt frei.
- Für FB 7.2: PR an `bam-masterdata` (2 Typen, 6 Vokabulare, 2 Erweiterungen) · Parser für IMC-Auswertung · Aufräumen Altbestand
- Für andere: neues PRD v2 schreiben, Pipeline laufen lassen (Agenten + Skripte liegen im Repo)
- Grenzen: Fachentscheidungen (z. B. Bewertungsgruppen, Stoß- vs. Nahtart) bleiben beim Menschen
- *Bild:* `diagrams/05_two_path_provisioning.mmd`

---

## Quellen für Zahlen und Bilder

| Aussage | Beleg |
|---|---|
| 141 Objekttypen, 35 Schritte, 148 Vokabulare | `generated/CATALOG.md` (Skript `tools/build_catalog.py`, SHA d7a871b) |
| Altbestand 189 Objekte, 12 Ebenen, 16/6/17 Typen | `generated/live/dev1_inventory.md` |
| 2 Typen, 6+2 Vokabulare, 33+2 Property-Typen, Metriken | `generated/welded_fatigue_v2/design.md`, `gap-report.md` |
| 20 REUSE · 2 EXTEND · 41 CREATE · 40 LIVE-ONLY | `generated/welded_fatigue_v2/gap-report.md` |
| Angelegt: 6 Vokabulare, 4 Terme, 36 Property-Typen, 2 Typen, 28+3 Objekte | Ausgabe `tools/openbis_apply.js` / `tools/openbis_demo.js` (06.10.2026) |
| Alter Code nicht importierbar | Import-Test gegen `bam-masterdata` (ImportError `VocabularyTypeAssignment`) |
| Screenshots | `presentation/screenshots/` (dev1, 06.10.2026) |
