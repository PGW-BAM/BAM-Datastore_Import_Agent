# Schritt 4: Flache Struktur entwerfen

**Ziel:** Jeder Wert, jede Datei und jeder Ablaufschritt bekommt genau einen Ort in openBIS, nach den
Prinzipien P1–P8 (`workflow/README.md`).

| | |
|---|---|
| Eingabe | `prd.md` (freigegeben, ◆ A), `ablauf.md`, `generated/catalog.json`, `inventory.md` |
| Ausgabe | `requirements.json`, `design.json`, `design.md` |
| Zugang | keiner |
| Prüfpunkt | ◆ **B**: die Fachseite bestätigt die Struktur |

## Tun

1. **Anforderungen abschreiben** (`requirements.json`): Schritte, Messgrößen mit Einheit und Typ, Auswahllisten
   mit Begriffen, Geräte, Dateien, fachliche Entscheidungen. Nur was im PRD steht.
2. **Struktur entwerfen** (`design.json` + `design.md`):
   - Hauptobjekt (meist die Probe) mit allen Eigenschaften, die die Probe beschreiben (P3)
   - Schritt-Objekte nur, wo Gerät, Zeitraum, Person und Dateien zusammengehören (P4). Mehrere Ablaufschritte
     am selben Arbeitsplatz: ein Objekt, nummerierte Sektionen in Title Case („07 Strain Gauge Application“)
   - Collection = Serie; welche Spalten die Serientabelle zeigt
   - Geräte als Eltern aus dem Inventar (Identifier aus `inventory.md`)
   - Feld „Next step“ und ein Ablaufplan-Objekt (P5)
   - Für jede Datei: an welchem Objekt, welcher Dataset-Typ aus dem Standard
3. `design.md` braucht die Tabelle **Ablaufschritt → Objekt → Sektion → Dateien** und eine Skizze der Hierarchie.

## Prüfen

- [ ] Jeder Ablaufschritt aus `ablauf.md` hat genau einen Ort
- [ ] Höchstens eine Ebene Probe → Schritt, keine Ketten Schritt → Schritt
- [ ] Tabellen und Messreihen sind Dateien (P7)
- [ ] Sektionsnamen englisch und in Title Case
- [ ] Jede fachliche Entscheidung aus dem PRD ist wörtlich wiederzufinden

## Stopp

◆ **B**: Die Fachseite liest `design.md`. Leitfrage: „Würde jemand im Labor die Serientabelle so lesen wollen?“
Freigabe oder Änderungen in `STATUS.md`.

## Hilfsmittel

- Claude: Agenten `prd-requirements-extractor` und `structure-designer` (Ausgabepfad auf `projects/<name>/` setzen)
- Beispiel: `generated/welded_fatigue_v2/design.md`
