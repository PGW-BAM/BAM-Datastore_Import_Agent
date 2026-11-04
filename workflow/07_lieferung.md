# Schritt 7: Lieferung prüfen

**Ziel:** Feststellen, ob der Admin alles angelegt hat, bevor irgendetwas angelegt wird.

| | |
|---|---|
| Eingabe | `spec.json`, `structure.json` (falls schon da), neuer Export `inventory_<instanz>.json` |
| Ausgabe | `delivery_check.md` |
| Zugang | openBIS lesen, **nur der Mensch** |
| Prüfpunkt | keiner (fehlt etwas: zurück zu Schritt 6) |

## Tun: Mensch (BAM-Netz)

Im Brücken-Notebook **Einstellungen**, **Anmelden**, **1 Lesen**, **2 Prüfen** ausführen. Das schreibt den neuen
Export und `delivery_check.md`. Beides committen und pushen.

## Tun: Agent (Cloud)

1. Prüfung selbst nachvollziehen (offline, gleiche Logik wie im Notebook):
   ```bash
   python tools/openbis_bridge.py check --inventory projects/<name>/inventory_<instanz>.json \
     --spec projects/<name>/spec.json [--structure projects/<name>/structure.json] --md projects/<name>/delivery_check.md
   ```
2. Ergebnis auswerten, je nach „Wer“ in der Tabelle:
   - **Admin:** Nachfrage für das Issue formulieren (welche Typen, Properties, Begriffe fehlen noch). Die Person postet sie.
   - **du:** Geräte für Schritt 8 vormerken.
   - **Agent:** `structure.json` korrigieren (z. B. Pflichtfeld fehlt).
   - Hinweise (andere Sektion, anderes Pflicht-Flag) kurz bewerten: stört das die Anlage oder nur die Anzeige?
3. `STATUS.md`: „bereit“ oder „wartet auf Admin: …“.

## Prüfen

- [ ] Export ist neuer als die Mail an den Admin
- [ ] „bereit“ nur, wenn `delivery_check.md` keine Zeilen unter „Fehlt“ mit Wer = Admin hat
