# Ablauf: fb72_schwingversuche

Die eine Quelle für den Ablauf. Entsteht in Schritt 2 aus Schema oder Erzählung und wird im Interview ergänzt.
Quelle je Zeile: S = Schema, P = Person, V = Vorschlag des Agenten (bestätigt).

| Nr. | Schritt (Deutsch / Englisch) | Was passiert | Erfasste Werte (Deutsch / Englisch, Einheit, Bereich/Auswahl, Pflicht) | Geräte / Material | Dateien (Format, Herkunft) | Quelle |
|---|---|---|---|---|---|---|---|
| 01 | Probeneingang / Specimen receipt | Geschweißte Proben (u. a. Stumpfstoß) kommen vom Hersteller; Probe wird erfasst und identifiziert | offen (z. B. Hersteller, Blech-/Probenkennung, Schweißnahttyp) | – | offen (Lieferschein, Zeichnung als PDF?) | P |
| 02 | Sichtprüfung und Vermessung / Visual inspection and measurement | Probe wird angeschaut: Verzug gemessen, Naht ok?, ggf. Richten | offen (Verzug mit Einheit, Nahtbefund Auswahl, gerichtet ja/nein) | offen (Messmittel für Verzug) | offen (Fotos?) | P |
| 03 | GOM-Scan und Nahtbewertung / GOM scan and weld assessment | Probe wird mit dem GOM gescannt; die Naht wird nach ISO-Norm bewertet | offen (ISO-Norm, Bewertungsergebnis) | GOM-Scanner | GOM-Scan (Format offen) | P |
| 04 | Zufällige Serienaufteilung / Random assignment to series | Proben werden zufällig auf die Serien aufgeteilt, um Bias vom Blech zu vermeiden | offen (Serien, Zufallsverfahren) | – | Randomisierungsliste (Excel?) | P |
| 05 | Geometrievermessung / Geometry measurement | Vor dem Versuch wird die Geometrie der Probe vermessen | offen (welche Maße, Einheiten) | offen (Messmittel) | offen | P |
| 06 | DMS-Applikation / Strain gauge application | DMS werden aufgeklebt | offen (Lage, Typ, Anzahl, Klebstoff) | DMS, Klebstoff | offen | P |
| 07 | Einbau in Prüfmaschine / Mounting in test rig | Probe wird in die Prüfmaschine eingebaut, Messtechnik (IMC) angeschlossen | offen | Prüfmaschine, IMC-Messtechnik | offen | P |
| 08 | Ermüdungsversuch / Fatigue test | Versuch läuft bis zum Bruch oder bis zum Abbruch | offen (Belastung: Ober-/Unterspannung oder Verhältnis, Frequenz, Abbruchkriterium, Schwingspielzahl) | Prüfmaschine, IMC | IMC-Rohdaten (Format offen) | P |
| 09 | Auswertung Schwingspielzahlen / Cycle count evaluation | Schwingspielzahlen werden ausgewertet (Grundlage Wöhlerlinie) | offen | – | Auswertung (Excel?) | P |
| 10 | Bruchflächenanalyse / Fracture surface analysis | Bruchfläche wird angesehen: Fotos und Mikroskop | offen (Befund, Ort des Rissstarts?) | Foto, Mikroskop | Fotos, Mikroskopbilder (Formate offen) | P |

## Reihenfolge und Verzweigungen

- 01–03 je Probe, Reihenfolge wie oben (offen: kann 03 vor 02 laufen?).
- 04 nach 03: erst nach Bewertung wird auf Serien aufgeteilt.
- 05–08 je Probe und Serie; 10 nach 08 (offen: Bruchflächenanalyse bei Abbruch ohne Bruch?).

## Offen

- Naht-Typ(en) außer Stumpfstoß? Hersteller, Blech-Herkunft als Feld?
- Richten: wie oft, wird das dokumentiert?
- ISO-Norm der Nahtbewertung (z. B. ISO 5817?) und Stufe (offen, Vorschlag).
- Serien: wie viele, wie benannt? Wöhlerlinie je Blech/Charge?
- Belastungsparameter des Versuchs (Spannungsverhältnis R, Frequenz, Ober-/Unterspannung, Abbruchkriterien).
- Dateiformate: GOM, IMC, Fotos, Mikroskop, Excel-Listen.
- „Pro Probe sehen, wo sie steht und was als Nächstes dran ist“ → Feld „Next step“ (Standard).
