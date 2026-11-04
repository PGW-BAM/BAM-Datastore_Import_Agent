# Schritt 4: Struktur entwerfen

**Ziel:** Jeder Wert, jede Datei und jeder Ablaufschritt bekommt genau einen Ort in openBIS, nach den
Prinzipien P1–P8 (`workflow/README.md`). Die Struktur soll in openBIS übersichtlich lesbar sein; Muster und
Entscheidungshilfe: [strukturmuster.md](strukturmuster.md).

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
   - Hauptobjekt (Probe, Charge, Bauteil, Simulation …) mit allen Eigenschaften, die es beschreiben (P3). Es steht zuerst in
     `layout.per_specimen` (der Schlüssel heißt aus Kompatibilitätsgründen so) mit `name_de`/`name_en`; die Prüfseiten nennen
     es überall bei diesem Namen
   - Schritt-Objekte nur, wo Gerät, Zeitraum, Person und Dateien zusammengehören (P4). Mehrere Ablaufschritte
     am selben Arbeitsplatz: ein Objekt, je Ablaufschritt eine Sektion in Ablauf-Reihenfolge, Name in Title Case
     ohne Ziffern („Strain Gauge Application“). Die Schrittnummer steht im Begriff des „Next step“-Feldes
     („07 Strain gauge application“) und im Ablaufplan
   - Collection = Serie; welche Spalten die Serientabelle zeigt (`series_table`: `source` = `main <PROPERTY>` für das
     Hauptobjekt oder `<ENDUNG> <PROPERTY>` für ein anderes Objekt je Hauptobjekt, z. B. `TEST` für `S1-01-TEST`)
   - Verbindungen nach `strukturmuster.md`: Eltern/Kind für Herkunft und Reihenfolge (Prozesslinie oder Probe als
     Mittelpunkt), Geräte und Hilfsstoffe aus dem Inventar als Feld vom Typ OBJECT oder als Eltern, je nach PRD und
     Variante (Identifier aus `inventory.md`)
   - Feld „Next step“ und ein Ablaufplan-Objekt (P5)
   - Für jede Datei: an welchem Objekt, welcher Dataset-Typ aus dem Standard
3. **Varianten zeigen** (`design.json` → `variants`, Pflicht): 2–4 Möglichkeiten, denselben Ablauf abzubilden, z. B.
   „Prozesslinie, Geräte als Felder“, „Hauptobjekt als Mittelpunkt“, „Zustände des Materials“, „alles an einem Objekt“ und, falls es ein bisheriges
   Modell gibt, dieses zum Vergleich (Muster M1–M7 aus `strukturmuster.md`, in der Kurzbeschreibung nennen). Genau eine bekommt `"recommended": true` (die Seite zeigt „(empfohlen)“). Je Variante:
   Name und Kurzbeschreibung auf Deutsch und Englisch, Form (`flat`, `chain`, `single`), Objekte je Hauptobjekt mit ihren
   Schritten, Kennzahlen (Objekte je Hauptobjekt, Ebenen, neue Typen, Geräte als Eltern), Vor- und Nachteile, Herkunft. Widerspricht eine Variante dem
   PRD oder P1–P8, steht das bei den Nachteilen. Alle Varianten außer einem bisherigen Modell sind **Vorschläge** (Regel 5).
   Ausgearbeitet (Objekte, Felder, Ablauf) wird nur die Variante in `"variant"`, zuerst die empfohlene.
4. `design.md` braucht die Tabelle **Ablaufschritt → Objekt → Sektion → Dateien** und eine Skizze der Hierarchie.

## Prüfen

- [ ] Jeder Ablaufschritt aus `ablauf.md` hat genau einen Ort
- [ ] Der Graph eines Hauptobjekts ist lesbar: wenige Knoten, keine geteilten Inventar-Objekte mit vielen Verbindungen
      (`strukturmuster.md` → Entscheidungshilfe)
- [ ] Tabellen und Messreihen sind Dateien (P7)
- [ ] Sektionsnamen englisch, Title Case, nur Buchstaben (Regel des `checker`, siehe `AGENTS.md`)
- [ ] Jeder neue Name hat beide Sprachen: `property_label_de`, `label_de` (Begriffe), `section_names_de`, `step_de`,
      `name_de`/`name_en` (Objekte, Typen); Collection- und Objektnamen als „Deutsch / Englisch“. Die Prüfseite zeigt Lücken als „DE fehlt“
- [ ] Jede fachliche Entscheidung aus dem PRD ist wörtlich wiederzufinden
- [ ] 2–4 Varianten mit genau einer Empfehlung; Kennzahlen nur, wo sie sich belegen lassen

## Stopp

◆ **B**: Prüfseite erzeugen und der Person zeigen, nicht `design.md`:

```bash
python tools/check_files.py <name>                 # Format von design.json (schemas/design.schema.json)
python tools/render_review.py <name> struktur      # -> projects/<name>/review/struktur.html, committen
```

Die Seite zeigt zuerst die Varianten nebeneinander (die empfohlene mit „(empfohlen)“), danach für die ausgearbeitete
Variante Aufbau, Ablauf → Ort, Formulare, Serientabelle und Auswahllisten. Zu jedem Teil gibt es „passt / ändern“,
daraus entsteht ein Text, den die Person in den Chat kopiert. Überschrift und Fachbereich kommen aus `project.yaml`
(`title`, `title_en`, `division`).

Antworten: „B freigegeben (Variante A)“ → eintragen, weiter. „Variante: bitte Variante C … ausarbeiten“ → keine
Freigabe: `"variant": "C"` setzen, `object_types`, `layout`, `step_location_map` usw. für C neu schreiben (die Empfehlung
bleibt, wo sie war), Seite neu erzeugen und wieder zeigen. Zeigen: wo die Plattform Seiten anzeigen kann (Claude:
Artifact mit `--fragment`), sonst Link auf die Datei im Repo mit dem Hinweis „herunterladen und im Browser öffnen“.
Leitfrage: „Würde jemand im Labor die Serientabelle so lesen wollen?“
Freigabe oder Änderungen im Chat; der Agent trägt sie in `STATUS.md` ein.

## Hilfsmittel

- Claude: Agenten `prd-requirements-extractor` und `structure-designer` (Ausgabepfad auf `projects/<name>/` setzen)
- Beispiel: `generated/welded_fatigue_v2/design.md`
