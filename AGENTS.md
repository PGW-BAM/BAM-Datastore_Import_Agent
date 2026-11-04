# Anleitung für KI-Agenten

Dieses Repo macht aus einem Laborablauf eine openBIS-Struktur im BAM Data Store. Die Anleitung gilt für
jeden Agenten (Claude, Codex, Cursor, Copilot …). Claude-spezifische Abkürzungen liegen unter `.claude/`,
sind aber nicht nötig: maßgeblich sind die Schrittkarten unter `workflow/`.

## So fängst du an

1. Welches Projekt? Liegt es unter `projects/<name>/`, lies dort `STATUS.md`. Die Datei sagt, welcher
   Schritt dran ist und ob ein Prüfpunkt auf Freigabe wartet.
2. Neues Projekt: wie in `workflow/README.md` → „Neues Projekt“ anlegen.
3. Öffne die Karte des aktuellen Schritts (`workflow/0N_*.md`) und arbeite sie ab: Eingabe → Tun → Prüfen → Stopp.
4. Trag das Ergebnis in `STATUS.md` ein (Datum, was entstanden ist, offene Fragen).

## Feste Regeln

1. **Kein Zugriff auf openBIS.** Der Agent arbeitet nur mit Dateien im Repo. Lesen und Anlegen macht
   ein Mensch im BAM-Netz mit `notebooks/openbis_bruecke.ipynb`; die Ergebnisse kommen als Dateien zurück.
2. **Keine Zugangsdaten.** Keine Tokens, Passwörter oder Benutzer-Kennungen in Dateien, Commits oder im Chat.
3. **Prüfpunkte sind Stopps.** Bei ◆ A–E hältst du an, schreibst „wartet auf Freigabe“ in `STATUS.md` und
   machst erst weiter, wenn dort die Freigabe steht.
4. **Nichts erfinden.** Ins Modell kommt nur, was die Person im Interview bestätigt hat oder im PRD steht.
   Eigene Ideen sind willkommen, aber immer als **Vorschlag** markiert, bis sie bestätigt sind.
5. **Nichts nach außen schicken.** Issue anlegen, Mail senden, PR öffnen macht der Mensch (Prüfpunkt D).
6. **Standard zuerst.** Vor jedem neuen Typ, Property oder Vokabular im Katalog (`generated/CATALOG.md`)
   suchen. Neu ist nur, was es dort wirklich nicht gibt.
7. **bam-masterdata ist gepinnt** auf `v0.17.0` (`BMD_REF` in `tools/cloud_setup.sh`) und es zählt nur
   `bam_masterdata/datamodel/v0/`. Das Datenmodell `v1` wird nicht verwendet.

## Konventionen für Masterdaten (bam-masterdata)

| Was | Regel |
|---|---|
| Codes | GROSSBUCHSTABEN_MIT_UNTERSTRICH; Namensraum mit Punkt nur wie in v0 üblich (z. B. `FATIGUE.LOAD_LEVEL`) |
| Beschreibungen | zweisprachig `English//Deutsch`, ohne Leerzeichen um `//` |
| Labels, Sektionen | englisch; Sektionen in **Title Case**, jedes Wort groß („07 Strain Gauge Application“), sonst warnt der `checker` |
| Pflichtangaben | `mandatory` und `section` immer setzen; Einheiten über `units` (Label wird zu „Length in [mm]“) |
| Tabellen, Messreihen | als Datei, nicht als Properties |
| Struktur | flach: Space → Projekt → Collection (= Serie) → Objekte; Schritte hängen direkt an der Probe |

## Umgebung

- **Cloud:** Beim Start läuft `tools/cloud_setup.sh` (Claude: SessionStart-Hook). Andere Agenten oder
  Sessions ohne Hook: `bash tools/cloud_setup.sh --force`. Das legt `../bam-masterdata` an (gepinnt) und
  installiert `bam-masterdata`, `pybis==1.37.4`, `nbformat`, `pyyaml`.
- **Netz:** Die openBIS-Instanzen sind aus der Cloud gesperrt (gewollt). Erreichbar sind GitHub, PyPI und
  die Doku `https://bamresearch.github.io/bam-masterdata/`.
- **Tests:** `python -m pytest tools/tests -q`

## Wo was liegt

| Pfad | Inhalt |
|---|---|
| `workflow/` | Überblick und eine Karte pro Schritt, Interview-Fragen |
| `templates/` | Vorlagen für ein neues Projekt (Kopiervorlage) |
| `projects/<name>/` | ein Projekt: Einstellungen, Status, alle Zwischenstände |
| `notebooks/openbis_bruecke.ipynb` | das einzige Werkzeug im BAM-Netz: Lesen, Prüfen, Trockenlauf, Anlegen |
| `tools/` | Skripte: Katalog, Spec-Export, Brücke (`openbis_bridge.py`), Cloud-Setup |
| `generated/CATALOG.md`, `catalog.json` | Katalog des Standards (gepinnter Stand) |
| `generated/welded_fatigue_v2/` | Referenzbeispiel FB 7.2 (Wöhlerversuche), entstanden vor dem Umbau |
| `.claude/` | Claude-Agenten und Befehle (`/bam-*`) als Abkürzungen für einzelne Schritte |
