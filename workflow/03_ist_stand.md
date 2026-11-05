# Schritt 3: Ist-Stand der Zielinstanz

**Ziel:** Wissen, was auf der Instanz wirklich da ist. Sie hinkt dem Standard oft hinterher, und Geräte für
Eltern-Links gibt es nur dort.

| | |
|---|---|
| Eingabe | `project.yaml` (Instanz, Space, Projekt, `inventory_projects`) |
| Ausgabe | `inventory_<instanz>.json` (Mensch, Notebook), `inventory.md` (Agent) |
| Zugang | openBIS lesen, **nur der Mensch** im BAM-Netz |
| Prüfpunkt | keiner |

## Tun: Mensch (BAM-Netz)

Der Agent hat die Aufgabe in `AUFGABE.md` beschrieben. Zwei gleichwertige Wege (Einrichtung: `workflow/MENSCH.md`):

- **Befehl:** `python tools/bruecke.py <name> lesen` (holt vorher den Stand, lädt hinterher die Datei hoch)
- **Notebook:** `git pull`, `notebooks/openbis_bruecke.ipynb`, `PROJECT = "<name>"`, Zellen **Einstellungen**,
  **Anmelden**, **1 Lesen**, dann die Datei committen und pushen

Ergebnis: `projects/<name>/inventory_<instanz>.json`. Gelesen werden nur Masterdaten und die Projekte aus
`project.yaml` (eigenes Projekt + Equipment-Projekte), keine Messdaten.

## Tun: Agent (Cloud)

1. Datei vorhanden? Fehlt sie, ist `collected` älter als 7 Tage oder passt `read_projects` nicht zu `project.yaml`:
   `AUFGABE.md` schreiben (Vorlage `workflow/AUFGABE_VORLAGE.md`) und anhalten, nicht raten.
2. `inventory.md` schreiben:
   - Kopf: Instanz, Zeitpunkt, Server-Version, gelesene Projekte
   - Standard-Typen, die für dieses Projekt wichtig sind: vorhanden / fehlt / veraltet (weniger Properties als im
     Katalog). Das wird in Schritt 5 zu NUTZEN bzw. NACHZIEHEN.
   - Typen auf der Instanz, die nicht im Standard sind (Altbestand), soweit sie das Thema berühren
   - Geräteliste aus `objects`: Identifier, Typ, Name. Das sind die Kandidaten für Eltern-Links.
   - Vergebene Codes im eigenen Projekt (Collections, Objekte)
3. `STATUS.md` aktualisieren.

## Prüfen

- [ ] Export nicht älter als 7 Tage, Instanz = `project.yaml`
- [ ] Jede Aussage „fehlt auf der Instanz“ ist mit dem Export belegt

## Hilfsmittel

- `tools/bruecke.py lesen` oder `notebooks/openbis_bruecke.ipynb` (Teil 1); Logik in `tools/openbis_bridge.py` (`read_inventory`)
- Ohne Python im BAM-Netz: `tools/openbis_inventory.js` in der Browser-Konsole des ELN (siehe `CLOUD.md`)
