# BAM Data Store: vom Laborablauf zur openBIS-Struktur

Ein Agenten-Workflow für BAM-Fachbereiche: Aus einem Ablaufschema oder einer Erzählung wird im Interview ein PRD,
daraus eine übersichtliche openBIS-Struktur (mehrere Varianten zur Wahl), ein geprüfter Masterdaten-Antrag an den Admin und am Ende ein Notebook-Lauf,
der die Struktur in deinem Space anlegt.

**Für Agenten:** [AGENTS.md](AGENTS.md) (gilt für jeden Agenten; Claude liest es über `CLAUDE.md`).
**Für Menschen:** [workflow/README.md](workflow/README.md) zeigt alle Schritte, Prüfpunkte und Zugänge auf einer Seite.

## Kurz

| Phase | Schritte | Wer | openBIS |
|---|---|---|---|
| Verstehen | 1 Standard laden · 2 Interview → PRD (◆ A) | Agent + du | – |
| Entwerfen | 3 Ist-Stand · 4 Struktur (◆ B) · 5 Abgleich (◆ C) | Agent, du liest die Instanz | lesen |
| Beantragen | 6 Issue + Mail an datastore@bam.de (◆ D) · 7 Lieferung prüfen | Agent baut, du sendest, Admin legt Typen an | Admin, lesen |
| Anlegen | 8 Trockenlauf (◆ E) · Anlegen | Agent baut `structure.json`, du führst aus | schreiben |

Der Agent arbeitet in der Cloud nur mit Dateien und hat keinen Zugang zu openBIS. Was die Instanz berührt, läuft
im BAM-Netz über einen Befehl, `python tools/bruecke.py <projekt> lesen|pruefen|trockenlauf|anlegen` (mit git pull/push),
oder dasselbe als Notebook [`notebooks/openbis_bruecke.ipynb`](notebooks/openbis_bruecke.ipynb). Test-Instanz:
`https://playground.datastore.bam.de`.

**Was du selbst tust:** [workflow/MENSCH.md](workflow/MENSCH.md). Kurz: Fragen beantworten und freigeben im Chat; wenn
der Agent etwas im BAM-Netz oder nach außen braucht, steht es fertig in `projects/<name>/AUFGABE.md`.

**Plattformen:** Claude Code (Web) und Mistral Vibe (Browser) lesen `AGENTS.md` bzw. den Skill `bam-weiter`; andere
Agenten `AGENTS.md`. Details: [CLOUD.md](CLOUD.md).

## Loslegen

```bash
cp -r templates projects/<name>     # neues Projekt; dann project.yaml ausfüllen
```

Dann einem Agenten sagen: „weiter mit `<name>`“ (Claude: `/bam-weiter <name>`). Er liest `STATUS.md` und macht beim
nächsten Schritt weiter.

Laufendes Projekt: [`projects/fb72_welded_fatigue/`](projects/fb72_welded_fatigue/) (Wöhlerversuche FB 7.2, Test
auf dem Playground). Die Ergebnisse des ersten Laufs gegen dev1 liegen unter `generated/welded_fatigue_v2/`.

## Voraussetzungen

- **Cloud-Session:** nichts. `tools/cloud_setup.sh` legt beim Start `../bam-masterdata` (gepinnt auf `v0.17.0`) an und
  installiert `bam-masterdata`, `pybis==1.37.4`, `nbformat`, `pyyaml`. Andere Agenten rufen `bash tools/cloud_setup.sh` selbst auf.
- **BAM-Netz:** Python mit `pybis==1.37.4` und `pyyaml`, ein Klon dieses Repos, VPN (Einrichtung: `workflow/MENSCH.md`).
- Tests: `python -m pytest tools/tests -q`

## Verzeichnisse

```
AGENTS.md, CLAUDE.md     Regeln und Einstieg für Agenten
workflow/                eine Karte pro Schritt, Interview-Fragen
templates/               Kopiervorlage für ein neues Projekt
projects/<name>/         ein Projekt: project.yaml, STATUS.md, alle Zwischenstände
notebooks/               openbis_bruecke.ipynb (BAM-Netz); ältere projektspezifische Notebooks
tools/                   build_catalog.py, export_spec.py, openbis_bridge.py, cloud_setup.sh, JS-Fallbacks
generated/               Katalog des Standards; Ergebnisse früherer Läufe (welded_fatigue, welded_fatigue_v2)
.claude/                 Claude-Agenten und Befehle (/bam-*) als Abkürzungen für einzelne Schritte
presentation/, shipping/ Vortrag, Poster, Lieferpaket des ersten Laufs
```

## Selbstverbesserung (Claude)

`/bam-improve <agent>` bewertet einen Agenten-Lauf und schlägt Änderungen an seiner Anleitung vor
(`.claude/skills/karpathy-self-improvement/SKILL.md`).

## Versionen

openBIS 20.10.12.5 · pyBIS 1.37.4 · bam-masterdata v0.17.0 (nur `datamodel/v0`)

Interne BAM-Werkzeuge. Nicht ohne Freigabe veröffentlichen.
