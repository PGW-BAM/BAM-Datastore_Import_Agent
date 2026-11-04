# Schritt 2: Ablauf erklären (Interview)

**Ziel:** Aus dem, was die Person mitbringt (Schema oder Erzählung), wird ein vollständiges PRD. Der Agent fragt
nach und bringt eigene Ideen ein, schreibt aber nur auf, was die Person bestätigt.

| | |
|---|---|
| Eingabe | `schema.*` im Projektordner (draw.io, Mermaid, Bild/PDF), Notizen, oder nichts (Ablauf wird erzählt) |
| Ausgabe | `ablauf.md`, `interview.md`, `prd.md` (Vorlagen in `templates/`) |
| Zugang | keiner |
| Prüfpunkt | ◆ **A**: die Person gibt das PRD frei |

## Tun

1. **Ablaufliste bauen.** Je nach Eingabe:
   - `.drawio`: XML lesen. Kästen sind `mxCell` mit `vertex="1"` (Text in `value`, HTML-Tags entfernen), Pfeile
     sind `mxCell` mit `edge="1"` (`source` → `target`). Reihenfolge aus den Pfeilen, nicht aus der Position.
   - Mermaid: Knoten und Pfeile direkt übernehmen.
   - Bild/PDF: lesen, erkannte Schritte besonders sorgfältig zurückfragen (Pfeile, kleine Schrift).
   - Nichts: „Erzähl mir den Ablauf vom ersten bis zum letzten Schritt. Was passiert mit der Probe?“
   Ergebnis in `ablauf.md` (Vorlage) eintragen und der Person zeigen: „Ich habe N Schritte erkannt: … Stimmt die
   Reihenfolge? Fehlt etwas?“ Erst nach Bestätigung weiter.
2. **Schritt für Schritt fragen.** Pro Nachricht ein Schritt aus der Ablaufliste, höchstens etwa fünf Fragen:
   - die Grundfragen aus [interview_fragen.md](interview_fragen.md),
   - die passenden Stichwort-Nachfragen (z. B. „DMS“ → Lage, Typ, Anzahl, Klebstoff),
   - einen Blick in den Katalog als konkrete Frage: „Im Standard gibt es Hilfsstoffe mit Typ ‚Strain gauge‘. Reicht
     das, oder braucht ihr mehr Angaben je DMS?“
   Eigene Ideen immer als **Vorschlag** kennzeichnen. Die Person entscheidet ja/nein.
3. **Nach jeder Runde festhalten.** In `interview.md` Frage, Antwort und Quelle (Person / Schema / Vorschlag
   bestätigt / Vorschlag abgelehnt) anhängen, `ablauf.md` ergänzen, kurz zusammenfassen: verstanden / offen.
   So kann jede neue Session oder ein anderer Agent bei „offen“ weitermachen.
4. **Querschnittsfragen** am Ende: Probe und Kennungen, Serien, Inventar, Personen, Dateien, Auswertung
   (Abschnitt „Querschnitt“ in [interview_fragen.md](interview_fragen.md)).
5. **PRD schreiben** nach `templates/prd.md`: Ziel, Ablauf-Tabelle, Probe, Inventar, Serien, Dateien, fachliche
   Entscheidungen wörtlich. Das PRD beschreibt **was**, nicht welche openBIS-Typen.
6. `STATUS.md`: Schritt 2 „wartet auf Freigabe A“.

## Prüfen

- [ ] Jeder Kasten im Schema steht in `ablauf.md` und umgekehrt
- [ ] Jeder Messwert hat Einheit, Wertebereich oder Auswahlliste, Pflicht ja/nein
- [ ] Jede Datei hat Format und Herkunft (Gerät/Software)
- [ ] Alle Vorschläge sind entschieden (bestätigt oder abgelehnt), keiner ist stillschweigend übernommen
- [ ] Keine openBIS-Typnamen im PRD (die kommen erst in Schritt 4/5)

## Stopp

◆ **A**: Die Person liest `prd.md` und gibt im Chat frei („A freigegeben“) oder nennt Änderungen. Der Agent trägt
die Freigabe wörtlich mit Datum in `STATUS.md` ein.
