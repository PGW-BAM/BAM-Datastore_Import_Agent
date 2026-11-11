# Ablauf: fb72_schwingversuche

Die eine Quelle für den Ablauf. Entsteht in Schritt 2 aus Schema oder Erzählung und wird im Interview ergänzt.
Quelle je Zeile: S = Schema, P = Person, V = Vorschlag des Agenten (bestätigt).

| Nr. | Schritt (Deutsch / Englisch) | Was passiert | Erfasste Werte (Deutsch / Englisch, Einheit, Bereich/Auswahl, Pflicht) | Geräte / Material | Dateien (Format, Herkunft) | Quelle |
|---|---|---|---|---|---|---|---|
| 01 | Sichtprüfung und Vermessung / Visual inspection and measurement | Proben kommen vom Hersteller an (kein eigener Eingangsschritt) und werden direkt angeschaut: Verzug messen, Befund als freier Text, ggf. richten (dann nochmal messen) | Winkelverzug [°] Pflicht; Versatz an der Naht [mm] Pflicht (bei Kreuzstoß: der ungünstigere von zwei Werten); Wiederholungsmessung nach Richten; Befund freier Text optional; gerichtet ja/nein Pflicht; Herstellernummer, interne Nummer, Blech (eingeschlagen) Pflicht; Stoßart (Stumpfstoß/Kreuzstoß) Pflicht | offen (Messmittel, nicht wichtig) | Foto je Probe (Format offen) | P |
| 02 | Anschleifen/Anfasen der Naht / Grinding and facing of the weld | Direkt nach der Sichtprüfung, vor dem Scan (sonst würde eine Naht gescannt, die es so nicht mehr gibt); nur dokumentiert, keine Messwerte | durchgeführt ja/nein Pflicht; Art (angeschliffen/angefast) offen | offen | – | P |
| 03 | GOM-Scan / GOM scan | Kollege scannt die Probe am ATOS; Rohdaten als GOM-Projektordner; Bearbeiter*in und Datum je Schritt sichtbar | offen (Namensschema der Rohdaten, Person fragt Kollegen) | ATOS-Scanner | GOM-Projektordner mit Rohdaten (Format offen) | P |
| 04 | Nahtbewertung / Weld assessment | Nach ISO 5817, Anhang C, mit der GOM-Software, später am Rechner; je Probe einzeln; bestellt sind die Proben mit Bewertungsgruppe B | Bewertungsgruppe ISO 5817 Anhang C (z. B. C63, B90, B125) Pflicht; bestellte Gruppe (B) Pflicht; Bearbeiter*in und Datum | GOM-Software | Bericht aus der GOM-Software (Format offen) | P |
| 05 | Zufällige Serienaufteilung / Random assignment to series | Erst, wenn alle Proben gescannt und bewertet sind; zufällig, um Bias vom Blech zu vermeiden; danach heißen die Proben S1-01, S1-02 usw.; eigene Serien je Stoßart (Stumpfstoß, Kreuzstoß) | Serienname je Probe Pflicht (S1-01 …); Zufallsverfahren offen | – | Randomisierungsliste (Excel?) | P |
| 06 | Geometrievermessung / Geometry measurement | Vor dem Versuch wird die Geometrie der Probe vermessen | offen (welche Maße, Einheiten) | offen (Messmittel) | offen | P |
| 07 | DMS-Applikation / Strain gauge application | DMS werden aufgeklebt | offen (Lage, Typ, Anzahl, Klebstoff) | DMS, Klebstoff | offen | P |
| 08 | Einbau in Prüfmaschine / Mounting in test rig | Probe wird in die Prüfmaschine eingebaut, Messtechnik (IMC) angeschlossen; Bearbeiter*in und Datum | offen | Prüfmaschine, IMC-Messtechnik | offen | P |
| 09 | Ermüdungsversuch / Fatigue test | Versuch läuft bis zum Bruch oder bis zum Abbruch (Durchläufer); Bearbeiter*in und Datum | offen (Belastung: Ober-/Unterspannung oder Verhältnis, Frequenz, Abbruchkriterium, Schwingspielzahl) | Prüfmaschine, IMC | IMC-Rohdaten (Format offen) | P |
| 10 | Auswertung Schwingspielzahlen / Cycle count evaluation | Schwingspielzahlen werden ausgewertet (Grundlage Wöhlerlinie) | offen | – | Auswertung (Excel?) | P |
| 11 | Bruchflächenanalyse / Fracture surface analysis | Bruchfläche wird angesehen: Fotos und Mikroskop. Entfällt bei Durchläufern ohne Riss; wurde bei einem Abbruch ein Riss gesehen, wird die Probe manchmal aufgebrochen und trotzdem analysiert | offen (Befund, Rissstart, Ausgang: Bruch/Durchläufer/abgebrochen mit Riss) | Foto, Mikroskop | Fotos, Mikroskopbilder (Formate offen) | P |

## Reihenfolge und Verzweigungen

- 01 → 02 → 03 → 04 je Probe: Sichtprüfung zuerst (Richten ändert die Geometrie), dann ggf. Anfasen/Anschleifen vor dem Scan, Scan am ATOS, Bewertung später am Rechner (Tage Abstand möglich).
- 05 erst, wenn alle Proben gescannt (03) und bewertet (04) sind; danach erhalten die Proben ihre Seriennamen (S1-01 …). Eigene Serien je Stoßart.
- 06–09 je Probe und Serie.
- 11 nach 09: nur bei Bruch; bei Durchläufern entfällt sie, außer ein Riss wurde gesehen → Probe manchmal aufgebrochen und dann analysiert.

## Offen

- Kreuzstoß-Versatz: erfasst als der ungünstigere der zwei Werte (bestätigt).
- Stoßart: im Standard gibt es `WELDING.WELD_TYPE` (Nahttypen), aber keine Liste der Stoßarten (Stumpfstoß/Kreuzstoß) → vermutlich NEU im Abgleich (Schritt 5).
- Namensschema der GOM-Rohdaten (Kollege fragen).
- Serien: wie viele, wie benannt (S1, S2 …)? Wöhlerlinie je Stoßart?
- Belastungsparameter (Spannungsverhältnis R, Frequenz, Ober-/Unterspannung, Abbruchkriterien).
- Dateiformate: GOM-Projektordner, GOM-Bericht, IMC, Fotos, Mikroskop, Excel-Listen.
- „Pro Probe sehen, wo sie steht und was als Nächstes dran ist“ → Feld „Next step“ (Standard).
