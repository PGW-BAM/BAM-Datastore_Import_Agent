# Schritt 5: Abgleich mit Standard und Instanz

**Ziel:** Für jedes Element der Struktur steht fest, ob es da ist, erweitert, neu beantragt, auf der Instanz
nachgezogen oder als Gerät eingetragen werden muss.

| | |
|---|---|
| Eingabe | `design.json`, `requirements.json`, `generated/catalog.json`, `inventory_<instanz>.json` / `inventory.md` |
| Ausgabe | `gap-report.md` |
| Zugang | keiner |
| Prüfpunkt | ◆ **C**: jedes NEU ist wirklich neu |

## Klassen

| Klasse | Englisch (Claude-Agent) | Bedeutung | Wer handelt |
|---|---|---|---|
| **NUTZEN** | REUSE | im Standard und passt | niemand |
| **ERWEITERN** | EXTEND | im Standard, braucht 1–3 Begriffe oder Properties | Admin (Antrag) |
| **NEU** | CREATE | weder im Standard noch passend auf der Instanz | Admin (Antrag) |
| **NACHZIEHEN** | instance sync | im Standard, fehlt oder veraltet auf der Instanz | Admin (Sync, kein PR) |
| **GERÄT FEHLT** | equipment missing | Typ ist da, das Gerät fehlt im Inventar des Fachbereichs | Mensch (Schritt 8) |
| **ALTBESTAND** | LIVE-ONLY | nur auf der Instanz, nicht im Standard | nicht weiterverwenden: ersetzen oder zur Aufnahme vorschlagen |

## Tun

1. Typen, Vokabulare, Properties der Struktur im Katalog suchen, nach Code **und** nach Bedeutung (ähnliche
   Vokabulare anderer Fachgebiete prüfen und begründen, warum sie passen oder nicht).
2. Jede NUTZEN/ERWEITERN-Zeile mit `datei:zeile` aus `catalog.json` belegen. Unsicher: `UNCONFIRMED`, nie erfinden.
3. Gegen den Export prüfen: vorhanden / fehlt / veraltet → NACHZIEHEN; Geräte gegen `objects` → GERÄT FEHLT.
4. Neue Codes auf Kollision prüfen (Katalog und Instanz, auch gleicher Code mit anderem Datentyp).
5. `gap-report.md` mit einer Tabelle je Klasse und einer Zusammenfassung (Anzahl je Klasse).

## Prüfen

- [ ] Jede NUTZEN/ERWEITERN-Zeile hat einen Beleg
- [ ] Kein NEU, für das es im Katalog einen passenden Typ gibt (Teiltreffer → ERWEITERN mit Begründung)
- [ ] Kein ALTBESTAND als NUTZEN
- [ ] Jede Auswahlliste zeigt auf ein Vokabular, jedes OBJECT-Property auf einen vorhandenen Typ

## Stopp

◆ **C**: Die Person prüft die NEU-Zeilen. Leitfrage: „Würde ein vorhandener Typ mit 1–2 zusätzlichen Properties
reichen?“ Freigabe im Chat; der Agent trägt sie in `STATUS.md` ein.

## Hilfsmittel

- Claude: Agent `gap-analyzer`
- Beispiel: `generated/welded_fatigue_v2/gap-report.md`
