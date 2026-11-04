# Schritt 1: Standard laden

**Ziel:** Der Agent kennt alle Typen, Properties und Vokabulare, die es im BAM-Standard schon gibt, und zwar
genau zum gepinnten Stand.

| | |
|---|---|
| Eingabe | `../bam-masterdata` (Release `v0.17.0`, gepinnt in `tools/cloud_setup.sh` → `BMD_REF`) |
| Ausgabe | `generated/CATALOG.md`, `generated/catalog.json` (mit SHA im Kopf) |
| Zugang | keiner |
| Prüfpunkt | keiner |

## Tun

1. Fehlt `../bam-masterdata` oder sind Pakete nicht installiert: `bash tools/cloud_setup.sh --force`.
2. Stand prüfen: `git -C ../bam-masterdata describe --tags` muss `v0.17.0` ergeben. Sonst meldet das
   Setup-Skript eine Warnung; dann nicht weiterarbeiten, sondern den Ordner neu anlegen lassen.
3. Katalog nur neu bauen, wenn die SHA im Kopf von `generated/CATALOG.md` nicht zu
   `git -C ../bam-masterdata rev-parse HEAD` passt: `python tools/build_catalog.py`.
   Das Skript liest nur `datamodel/v0/` und ist deterministisch (gleicher Stand → gleiche Datei).
4. In `STATUS.md` eintragen: Katalog-SHA und Datum.

## Prüfen

- [ ] SHA im Katalog = SHA von `../bam-masterdata`
- [ ] Ausgabe von `build_catalog.py` zeigt plausible Zahlen (bei v0.17.0: 149 ObjectTypes, 152 Vokabulare)

## Pin ändern (nur bewusst)

Neuer Release von bam-masterdata: `BMD_REF` in `tools/cloud_setup.sh` anheben, `../bam-masterdata` neu
klonen lassen, Katalog neu bauen, `spec.json` laufender Projekte neu exportieren und vergleichen. Das gehört in
einen eigenen Commit mit Begründung. Doku zu Änderungen: https://bamresearch.github.io/bam-masterdata/

## Hilfsmittel

- `tools/build_catalog.py`, `tools/cloud_setup.sh`
- Claude: Agent `bam-masterdata-explorer`
