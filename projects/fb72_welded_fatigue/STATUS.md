# Status: fb72_welded_fatigue

Jeder Agent liest diese Datei zuerst und aktualisiert sie zuletzt. Freigaben (◆) trägt nur ein Mensch ein.

Die Schritte 2–6 sind im Oktober 2026 gegen die Übungsinstanz dev1 gelaufen, noch vor dem neuen Ablauf. Die
Ergebnisse liegen unter `generated/welded_fatigue_v2/` und gelten als Ausgangspunkt. Ziel jetzt: Test auf dem
Playground.

| # | Schritt | Stand | Datum | Ergebnis / Notiz |
|---|---|---|---|---|
| 1 | Standard laden | erledigt | 2026-11-04 | Katalog-SHA `3cc15ca` (v0.17.0). Spec gegen v0.17.0 neu exportiert: unverändert |
| 2 | Interview → PRD | erledigt (alt) | 2026-10-06 | `BAM_PRD_Workflow_FB72_v2.md`; ohne `ablauf.md`/`interview.md` (gab es damals nicht) |
| ◆ A | PRD freigegeben | erledigt (alt) | 2026-10-06 | Fachbereich, siehe `presentation/06_Befunde_und_Entscheidungen.md` |
| 3 | Ist-Stand der Instanz | **offen** | | Playground noch nicht gelesen. Vorher `space` und `inventory_projects` in `project.yaml` prüfen |
| 4 | Struktur entwerfen | erledigt (alt) | 2026-10-06 | `generated/welded_fatigue_v2/design.md` |
| ◆ B | Struktur bestätigt | erledigt (alt) | 2026-10-06 | Fachbereich |
| 5 | Abgleich | teilweise | 2026-10-06 | gegen dev1 + Katalog `d7a871b`; für den Playground nach Schritt 3 neu bewerten (NACHZIEHEN, GERÄT FEHLT) |
| ◆ C | NEU geprüft | erledigt (alt) | 2026-10-06 | |
| 6 | Antrag gebaut | teilweise | 2026-11-04 | Klassen + `spec.json` vorhanden; checker: 0 Fehler, 3 Warnungen (alle aus dem Standard geerbt). Sektionen am 2026-11-04 umbenannt (Title Case, ohne Nummern). Issue/Mail noch nicht geschrieben |
| ◆ D | Antrag gesendet | offen | | |
| 7 | Lieferung geprüft | offen | | |
| 8 | structure.json gebaut | erledigt (alt) | 2026-11-04 | aus `demo_series.json` umgewandelt; Equipment-Pfade sind noch die von dev1 |
| ◆ E | Trockenlauf freigegeben | offen | | Instanz: Playground |
| 8 | angelegt | offen | | |

## Offene Fragen

- Equipment auf dem Playground: Welche Projekte/Collections? Nach Schritt 3 die Eltern-Pfade in `structure.json` anpassen.
- Der Space `FB_72` und die neuen Typen (`SAMPLE.WELDED_FATIGUE_SPECIMEN`, `…CYCLIC_FATIGUE_TEST`, Vokabulare `FATIGUE.*`)
  gibt es auf dem Playground vermutlich nicht. Schritt 7 zeigt, was fehlt; für den Test entweder Antrag (Schritt 6)
  oder vorerst nur mit Standard-Typen testen.

## Verlauf

- 2026-11-04: Sektionen umbenannt (Title Case ohne Nummern, Entscheidung im Chat); Nummern bleiben in „Next step“ und im Ablaufplan
- 2026-11-04: Projekt im neuen Format angelegt, Katalog auf v0.17.0, `structure.json` aus der dev1-Demo erzeugt
