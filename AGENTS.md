# Anleitung für KI-Agenten

Dieses Repo macht aus einem Laborablauf eine openBIS-Struktur im BAM Data Store. Die Anleitung gilt für
jeden Agenten (Claude, Codex, Cursor, Copilot …). Claude-spezifische Abkürzungen liegen unter `.claude/`,
sind aber nicht nötig: maßgeblich sind die Schrittkarten unter `workflow/`.

## So fängst du an

Kurzform für Agenten mit Skills oder Slash-Befehlen: Skill `bam-weiter` (`.agents/skills/bam-weiter/`, Claude: `/bam-weiter`).

0. **Setup:** `bash tools/cloud_setup.sh`. Idempotent und schnell; Claude Code macht das per Hook selbst, alle anderen
   Agenten (z. B. Mistral Vibe) rufen es als Erstes auf.
1. Welches Projekt? Liegt es unter `projects/<name>/`, lies dort `STATUS.md`. Die Datei sagt, welcher
   Schritt dran ist und ob ein Prüfpunkt auf Freigabe wartet.
2. Neues Projekt: wie in `workflow/README.md` → „Neues Projekt“ anlegen.
3. Öffne die Karte des aktuellen Schritts (`workflow/0N_*.md`) und arbeite sie ab: Eingabe → Tun → Prüfen → Stopp.
4. Trag das Ergebnis in `STATUS.md` ein (Datum, was entstanden ist, offene Fragen), dann **committen und pushen**.
   Sitzungen können jederzeit enden (Mistral Vibe: 3 h ohne Antwort); der nächste Agent macht nur mit dem weiter, was im
   Repo steht. Zweige und Pull Requests: `CLOUD.md` → „Zweige“.

## Feste Regeln

1. **Kein Zugriff auf openBIS.** Der Agent arbeitet nur mit Dateien im Repo. Lesen und Anlegen macht
   ein Mensch im BAM-Netz mit `tools/bruecke.py` oder `notebooks/openbis_bruecke.ipynb`; die Ergebnisse kommen als
   Dateien über das Repo zurück. Nach jeder Aufgabe des Menschen: `git pull`.
2. **Keine Zugangsdaten.** Keine Tokens, Passwörter oder Benutzer-Kennungen in Dateien, Commits oder im Chat.
3. **Prüfpunkte sind Stopps.** Bei ◆ A–E hältst du an, stellst im Chat zusammengefasst zur Freigabe, was zu prüfen
   ist, und schreibst „wartet auf Freigabe“ in `STATUS.md`. Weiter erst nach einer ausdrücklichen Freigabe im Chat
   („A freigegeben“). Du trägst sie wörtlich mit Datum in `STATUS.md` ein. Änderungswünsche sind keine Freigabe.
4. **Aufgaben für den Menschen** (openBIS lesen/anlegen, Antrag senden) stehen immer in `projects/<name>/AUFGABE.md`
   (Vorlage `workflow/AUFGABE_VORLAGE.md`) und gleichzeitig im Chat, mit allen Befehlen, Links und Texten zum
   Kopieren. Arbeitest du nicht auf dem Standard-Zweig, steht der vollständige Befehl mit `--zweig <dein Zweig>` drin
   (Befehle wie `python tools/bruecke.py <name> lesen --zweig <zweig>`), und du pushst vorher. Höchstens eine
   offene Aufgabe pro Projekt; erledigt → Datei löschen. Alles, was der Mensch tun kann: `workflow/MENSCH.md`.
5. **Nichts erfinden.** Ins Modell kommt nur, was die Person im Interview bestätigt hat oder im PRD steht.
   Eigene Ideen sind willkommen, aber immer als **Vorschlag** markiert, bis sie bestätigt sind.
6. **Nichts nach außen schicken.** Issue oder PR bei `BAMresearch/bam-masterdata`, Mail an datastore@bam.de: das macht
   der Mensch (Prüfpunkt D). Zweige und Pull Requests in diesem Repo sind normale Arbeit des Agenten.
7. **Standard zuerst.** Vor jedem neuen Typ, Property oder Vokabular im Katalog (`generated/CATALOG.md`)
   suchen. Neu ist nur, was es dort wirklich nicht gibt.
8. **bam-masterdata ist gepinnt** auf `v0.17.0` (`BMD_REF` in `tools/cloud_setup.sh`) und es zählt nur
   `bam_masterdata/datamodel/v0/`. Das Datenmodell `v1` wird nicht verwendet.

## Konventionen für Masterdaten (bam-masterdata)

| Was | Regel |
|---|---|
| Codes | GROSSBUCHSTABEN_MIT_UNTERSTRICH; Namensraum mit Punkt nur wie in v0 üblich (z. B. `FATIGUE.LOAD_LEVEL`) |
| Beschreibungen | zweisprachig `English//Deutsch`, ohne Leerzeichen um `//` |
| Labels, Sektionen | englisch; Sektionen in **Title Case** und nur aus Buchstaben: jedes Wort groß, keine Ziffern, kein `/` oder `-` („Strain Gauge Application“, „Measuring Amplifier And Test Rig“), sonst warnt der `checker`. Schrittnummern stehen im Auswahlfeld „Next step“ und im Ablaufplan, nicht in Sektionen |
| Pflichtangaben | `mandatory` und `section` immer setzen; Einheiten über `units` (Label wird zu „Length in [mm]“) |
| Tabellen, Messreihen | als Datei, nicht als Properties |
| Struktur | flach: Space → Projekt → Collection (= Serie) → Objekte; Schritte hängen direkt an der Probe |

## Umgebung

- **Setup:** `bash tools/cloud_setup.sh` legt `../bam-masterdata` an (gepinnt) und installiert `bam-masterdata`,
  `pybis==1.37.4`, `nbformat`, `pyyaml`. Braucht git und Python ≥ 3.11.
- **Netz:** Gebraucht werden `github.com`, `pypi.org`, `files.pythonhosted.org`, für die Doku
  `bamresearch.github.io`. Die openBIS-Instanzen sind aus der Cloud nicht erreichbar, und das ist gewollt.
- **Plattformen:**

  | Plattform | liest | Setup |
  |---|---|---|
  | Claude Code (Web) | `CLAUDE.md` → diese Datei, `.claude/` | SessionStart-Hook ruft `cloud_setup.sh --hook` |
  | Mistral Vibe (Browser) | `AGENTS.md`, Skills in `.agents/skills/` | selbst `bash tools/cloud_setup.sh` (noch keine Setup-Skripte; Projekt-Hooks laufen nicht). Sitzungen enden nach höchstens 24 h bzw. 3 h ohne Antwort |
  | andere (Codex, Copilot, Cursor, …) | `AGENTS.md` | selbst `bash tools/cloud_setup.sh` oder als Setup-Skript der Umgebung eintragen |

  Details und Netz-Einstellungen: `CLOUD.md`.
- **Tests:** `python -m pytest tools/tests -q`

## Wo was liegt

| Pfad | Inhalt |
|---|---|
| `workflow/` | Überblick, eine Karte pro Schritt, Interview-Fragen, `MENSCH.md` (Aufgaben des Menschen) |
| `templates/` | Vorlagen für ein neues Projekt (Kopiervorlage) |
| `projects/<name>/` | ein Projekt: Einstellungen, Status, alle Zwischenstände |
| `tools/bruecke.py`, `notebooks/openbis_bruecke.ipynb` | die Werkzeuge im BAM-Netz (Befehl oder Notebook, gleiche Logik): Lesen, Prüfen, Trockenlauf, Anlegen |
| `tools/` | Skripte: Katalog, Spec-Export, Brücke (`openbis_bridge.py`), Cloud-Setup |
| `generated/CATALOG.md`, `catalog.json` | Katalog des Standards (gepinnter Stand) |
| `generated/welded_fatigue_v2/` | Referenzbeispiel FB 7.2 (Wöhlerversuche), entstanden vor dem Umbau |
| `.claude/` | Claude-Agenten und Befehle (`/bam-*`) als Abkürzungen für einzelne Schritte |
