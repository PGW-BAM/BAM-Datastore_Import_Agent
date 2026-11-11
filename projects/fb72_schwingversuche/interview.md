# Interview: fb72_schwingversuche

Laufendes Protokoll von Schritt 2. Jede Runde wird angehängt. Eine neue Session macht bei „Offen“ weiter.
Quelle: Person · Schema · Vorschlag bestätigt · Vorschlag abgelehnt

## Runde 1: Ablaufliste (2026-11-11)

| Frage | Antwort | Quelle |
|---|---|---|
| Erzählen Sie den Ablauf vom ersten bis zum letzten Schritt | Bisher alles in Excel-Listen und Ordnern auf dem Laufwerk, chaotisch. Ablauf: geschweißte Proben (Stumpfstoß u. a.) vom Hersteller → Sichtprüfung (Verzug messen, Naht ok?, ggf. richten) → GOM-Scan, Nahtbewertung nach ISO-Norm → zufällige Aufteilung auf Serien (kein Bias vom Blech) → Geometrie vermessen, DMS kleben, Einbau in Prüfmaschine (Messtechnik IMC) → Ermüdungsversuch bis Bruch oder Abbruch → Auswertung Schwingspielzahlen (Wöhlerlinie) → Bruchfläche (Fotos, Mikroskop) | Person |
| Wichtig pro Probe | Sehen, wo die Probe steht und was als Nächstes dran ist; am Ende Wöhlerlinie aus den Daten; viele Dateien (Scans, IMC-Rohdaten, Bilder, Excel) wieder auffindbar ablegen | Person |
| Gibt es schon Sachen in openBIS? | Ja, einiges angelegt, Qualität unklar → Schritt 3 prüft den Ist-Stand (Inventory) | Person |

**Verstanden:** 10 Schritte (01–10 in `ablauf.md`), Hauptobjekt ist die Probe, Serien = Collections, Auswertung Wöhlerlinie, viele Dateien je Probe.
**Offen:** Ablauf bestätigen (Reihenfolge, Verzweigungen); Details je Schritt (Runde 2 ff.); project.yaml: Space, Projekt-Code, Equipment-Projekt(e) im ELN nachsehen; Instanz (Playground zum Testen?).

## Runde 2: Korrekturen Ablaufliste (2026-11-11)

| Frage | Antwort | Quelle |
|---|---|---|
| Stimmt die Reihenfolge der 10 Schritte? Fehlt etwas? | Korrekturen: Probeneingang kein eigener Schritt (zusammen mit Sichtprüfung); Scan und Nahtbewertung sind zwei Schritte (Scan am ATOS durch Kollegen, Bewertung später am Rechner mit GOM-Software, Tage Abstand möglich); zusätzlich: Naht wird manchmal angeschliffen/angefast, nur dokumentiert, keine Messwerte | Person |
| Kann GOM vor der Sichtprüfung laufen? | Nein, GOM immer nach der Sichtprüfung, da ggf. vorher gerichtet wird und sich dann die Geometrie ändert | Person |
| Bruchflächenanalyse bei Abbruch ohne Bruch? | Durchläufer: keine Bruchflächenanalyse. Außer ein Riss wurde gesehen: dann wird die Probe manchmal aufgebrochen und trotzdem angeschaut | Person |
| Instanz? | Eigene Testinstanz „dev1 oder so ähnlich“, nicht playground → https://dev1.datastore.bam.de (aus Referenzlauf bekannt, eingetragen) | Person / Repo |
| Space? | „FB72 oder so“, wird nachgeguckt | Person |

**Verstanden:** 11 Schritte (01 Sichtprüfung inkl. Eingang, 02 GOM-Scan am ATOS, 03 Nahtbewertung GOM-Software, 04 Anschleifen/Anfasen nur Dokumentation, 05 Serienaufteilung, 06 Geometrie, 07 DMS, 08 Einbau, 09 Ermüdungsversuch, 10 Auswertung, 11 Bruchflächenanalyse mit Durchläufer-Regel).
**Offen:** Details je Schritt (Runde 3 ff.), Position von 04 im Ablauf, Reihenfolge 05 zu 02–04, Space/Projekt-Code/Equipment-Projekt nachsehen.
