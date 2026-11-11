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

## Runde 3: Schritt 01 + Ordnungsfragen (2026-11-11)

| Frage | Antwort | Quelle |
|---|---|---|
| Schritt 04 (Anfasen/Anschleifen): wo im Ablauf? | Direkt nach der Sichtprüfung, vor dem Scan – sonst würde eine Naht gescannt, die es so nicht mehr gibt | Person |
| Schritt 05: vor oder nach dem Scannen aufgeteilt? | Erst, wenn alle Proben gescannt und bewertet sind | Person |
| 01: Was wird gemessen (Verzug)? | Winkelverzug in Grad, Versatz an der Naht in mm. Messmittel unbekannt/nicht wichtig. Nach dem Richten wird nochmal gemessen. Bei Kreuzstößen ist der Versatz anders, da zwei Bleche | Person |
| 01: Naht ok? als Auswahl? | Nein, wenn was Grobes auffällt, freier Text dazu. Keine feste Auswahl | Person |
| 01: Richten wie? | Nur ob gerichtet wurde, nicht wie | Person |
| 01: Probekennung? | Hersteller hat eigene Nummern; intern wird eine vergeben; wenn Serien feststehen, heißen Proben S1-01, S1-02 usw.; Blech steht auf der Probe drauf (eingeschlagen) | Person |
| 01: Dateien? | Fotos von jeder Probe | Person |
| Instanz bestätigt? | dev1.datastore.bam.de klingt richtig; Space noch nicht nachgeguckt | Person |

**Verstanden:** Reihenfolge 01 → 04 → 02 → 03 → 05; Messwerte Winkelverzug [°], Versatz [mm] (+ Wiederholungsmessung nach Richten), Befund freier Text, gerichtet ja/nein, Kennungen: Herstellernummer, interne Nummer, Serienname S1-01 …, Blech eingeschlagen; Fotos je Probe.
**Offen:** Details 02/03 (Scan, Bewertung); Kreuzstoß: wie genau ist der Versatz dort anders (zwei Bleche)? Englische Namen der Begriffe; Details 06–11.

## Runde 4: Schritte 02/03 (jetzt 03/04) + Kreuzstoß (2026-11-11)

| Frage | Antwort | Quelle |
|---|---|---|
| Kreuzstoß: Versatz? | Ein Versatz, der ungünstigere. Beide Stoßarten (Stumpfstoß, Kreuzstoß) im Projekt; eigene Serien je Nahttyp; andere Nahttypen aktuell nicht | Person |
| Gibt es im Standard schon eine Liste für Nahttypen? | Standard hat WELDING.WELD_TYPE (Kehlnaht, Nutnaht, Punktnaht, …), aber keine Stoßarten (Stumpfstoß/Kreuzstoß) → als NEU im Abgleich vorgemerkt | Katalog / Vorschlag |
| 03: Was kommt vom ATOS zurück? | Rohdaten, GOM-Projektordner; Namensschema kennt der Kollege (Person fragt) | Person |
| 04: Nach welcher Norm, was ist das Ergebnis? | ISO 5817, Anhang C; Bewertungsgruppe (C63, B90, B125); Proben beim Hersteller mit B bestellt; aus der GOM-Software wird ein Bericht exportiert | Person |
| 04: Bewerten Sie jede Probe einzeln? | Ja, jede Probe einzeln | Person |
| Bearbeiter*in und Datum je Schritt sichtbar? | Ja, wäre gut | Person |
| Nummern in Ausführungsreihenfolge? | Ja, gewünscht (steht so auch an der Tafel im Labor) → ablauf.md neu nummeriert 01–11 | Person |

**Verstanden:** Neue Reihenfolge 01 Sichtprüfung, 02 Anfasen/Anschleifen, 03 GOM-Scan, 04 Nahtbewertung (ISO 5817 Anhang C, Bewertungsgruppe, bestellt B), 05 Serienaufteilung (eigene Serien je Stoßart), 06–11 wie gehabt. Bearbeiter*in/Datum je Schritt.
**Offen:** Namensschema GOM-Rohdaten (Kollege); Seriennamen/-anzahl; Details 06–11; Stoßart-Vokabular NEU vormerken.
