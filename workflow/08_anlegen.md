# Schritt 8: Struktur anlegen

**Ziel:** Projekt, Collections, Proben, Schritte und Geräte-Links stehen auf der Instanz. Angelegt wird nur, was
fehlt. Nichts wird geändert oder gelöscht, keine Typen.

| | |
|---|---|
| Eingabe | `design.json`, aktueller Export, `delivery_check.md` („bereit“) |
| Ausgabe | `structure.json` (Agent), `reports/dryrun_<datum>.json`, `reports/apply_<datum>.json` (Befehl/Notebook) |
| Zugang | openBIS schreiben, **nur der Mensch**, nur nach ◆ E |
| Prüfpunkt | ◆ **E**: der Trockenlauf ist freigegeben |

## Tun: Agent (Cloud)

1. `structure.json` aus `design.json` und dem Export schreiben. Format und Beispiel: Kopf von
   `tools/openbis_bridge.py`, `templates/structure.example.json`, `generated/welded_fatigue_v2/structure.json`.
   - `space` und `project.code` aus `project.yaml`
   - Codes in Großbuchstaben, eindeutig, mit führender Null sortierbar (`S1-01`, nicht `S1-1`)
   - `$NAME` von Collections, Ablaufplan, Schritten und Geräten als „Deutsch / Englisch“
     (z. B. „Serie 1 – Stumpfstoß / Series 1 – butt weld“); Eigennamen wie „ZEISS GOM ATOS 5“ einmal
   - Eltern: Schlüssel aus der Datei oder Identifier aus dem Export (`/SPACE/PROJEKT/CODE`)
   - Pflichtfelder der Typen setzen (stehen im Export, `mandatory: true`)
   - Lange Texte (Ablaufplan) als Datei daneben und `"@file:<datei>"`
   - **GERÄT FEHLT:** nur nach Zustimmung der Person als eigenes Objekt mit `collection` = Collection im
     Equipment-Projekt aufnehmen
2. Offline prüfen:
   ```bash
   python tools/openbis_bridge.py validate projects/<name>/structure.json
   python tools/openbis_bridge.py check --inventory projects/<name>/inventory_<instanz>.json --structure projects/<name>/structure.json
   ```
3. `STATUS.md`: „wartet auf Trockenlauf“, `AUFGABE.md` schreiben.

## Tun: Mensch (BAM-Netz)

1. Trockenlauf: `python tools/bruecke.py <name> trockenlauf` oder Notebook Teil 1–3. Der Plan landet als
   `reports/dryrun_<datum>.json` im Repo, der Agent prüft ihn mit dir.
2. ◆ **E** (unten): Freigabe im Chat.
3. Anlegen: `python tools/bruecke.py <name> anlegen` (zeigt den Plan noch einmal, fragt nach „ja“) oder Notebook
   Teil 4 mit `FREIGABE = True`. Der Bericht `reports/apply_<datum>.json` geht ins Repo (Befehl: automatisch).

## Tun: Agent nach dem Anlegen

`reports/apply_<datum>.json` lesen: Stimmt `created` mit `structure.json` überein? Jede Zeile in
`droppedProps` erklären (Property nicht am Typ zugewiesen → zurück zu Schritt 7/6). `STATUS.md` abschließen.

## Prüfen (◆ E)

- [ ] Richtige Instanz (Playground oder Hauptinstanz), richtiger Space, richtiges Projekt
- [ ] „würde anlegen“ enthält genau das Erwartete, keine Code-Kollisionen
- [ ] `droppedProps` ist leer oder jede Zeile ist erklärt
- [ ] Auf der Hauptinstanz: vorher einmal auf dem Playground durchgelaufen

## Vom Playground auf die Hauptinstanz

In `project.yaml` die Instanz umstellen, dann Schritt 3 (Lesen), 7 (Prüfen) und 8 (Anlegen) wiederholen. Die
Hauptinstanz kann einen anderen Stand haben als der Playground.
