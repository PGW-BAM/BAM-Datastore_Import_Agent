# Ablauf: fb72_schwingversuche

Die eine Quelle für den Ablauf. Entsteht in Schritt 2 aus Schema oder Erzählung und wird im Interview ergänzt.
Quelle je Zeile: S = Schema, P = Person, V = Vorschlag des Agenten (bestätigt).

| Nr. | Schritt (Deutsch / Englisch) | Was passiert | Erfasste Werte (Deutsch / Englisch, Einheit, Bereich/Auswahl, Pflicht) | Geräte / Material | Dateien (Format, Herkunft) | Quelle |
|---|---|---|---|---|---|---|---|
| 01 | Sichtprüfung und Vermessung / Visual inspection and measurement | Proben kommen vom Hersteller an (kein eigener Eingangsschritt) und werden direkt angeschaut: Verzug messen, Naht ok?, ggf. richten | offen (Verzug mit Einheit, Nahtbefund Auswahl, gerichtet ja/nein, Hersteller, Proben-/Blechkennung, Schweißnahttyp) | offen (Messmittel für Verzug) | offen (Lieferschein/Zeichnung als PDF?, Fotos?) | P |
| 02 | GOM-Scan / GOM scan | Kollege scannt die Probe am ATOS | offen | ATOS-Scanner | Scan (Format offen) | P |
| 03 | Nahtbewertung / Weld assessment | Bewertung der Naht nach ISO-Norm, später am Rechner mit der GOM-Software; kann Tage nach dem Scan passieren | offen (ISO-Norm, Bewertungsergebnis) | GOM-Software | Bewertungsdatei (Format offen) | P |
| 04 | Anschleifen/Anfasen der Naht / Grinding and facing of the weld | Naht wird manchmal angeschliffen bzw. angefast; nur dokumentiert, keine Messwerte | offen (durchgeführt ja/nein, Art: angeschliffen/angefast, Datum/Bearbeiter*in) | offen (Schleifmittel?) | – | P |
| 05 | Zufällige Serienaufteilung / Random assignment to series | Proben werden zufällig auf die Serien aufgeteilt, um Bias vom Blech zu vermeiden; immer nach der Sichtprüfung, da Richten die Geometrie ändern kann | offen (Serien, Zufallsverfahren) | – | Randomisierungsliste (Excel?) | P |
| 06 | Geometrievermessung / Geometry measurement | Vor dem Versuch wird die Geometrie der Probe vermessen | offen (welche Maße, Einheiten) | offen (Messmittel) | offen | P |
| 07 | DMS-Applikation / Strain gauge application | DMS werden aufgeklebt | offen (Lage, Typ, Anzahl, Klebstoff) | DMS, Klebstoff | offen | P |
| 08 | Einbau in Prüfmaschine / Mounting in test rig | Probe wird in die Prüfmaschine eingebaut, Messtechnik (IMC) angeschlossen | offen | Prüfmaschine, IMC-Messtechnik | offen | P |
| 09 | Ermüdungsversuch / Fatigue test | Versuch läuft bis zum Bruch oder bis zum Abbruch (Durchläufer) | offen (Belastung: Ober-/Unterspannung oder Verhältnis, Frequenz, Abbruchkriterium, Schwingspielzahl) | Prüfmaschine, IMC | IMC-Rohdaten (Format offen) | P |
| 10 | Auswertung Schwingspielzahlen / Cycle count evaluation | Schwingspielzahlen werden ausgewertet (Grundlage Wöhlerlinie) | offen | – | Auswertung (Excel?) | P |
| 11 | Bruchflächenanalyse / Fracture surface analysis | Bruchfläche wird angesehen: Fotos und Mikroskop. Entfällt bei Durchläufern ohne Riss; wurde bei einem Abbruch ein Riss gesehen, wird die Probe manchmal aufgebrochen und trotzdem analysiert | offen (Befund, Rissstart, Durchläufer/Bruch/abgebrochen mit Riss) | Foto, Mikroskop | Fotos, Mikroskopbilder (Formate offen) | P |

## Reihenfolge und Verzweigungen

- 01–03 je Probe: immer Sichtprüfung zuerst (Richten ändert die Geometrie), dann Scan am ATOS, Bewertung später am Rechner (Tage Abstand möglich).
- 04 optional, nur dokumentiert (offen: an welcher Stelle im Ablauf?).
- 05 nach 01 (Sichtprüfung), Reihenfolge zu 02–04 offen.
- 06–09 je Probe und Serie.
- 11 nach 09: nur bei Bruch; bei Durchläufern entfällt sie, außer ein Riss wurde gesehen → Probe manchmal aufgebrochen und dann analysiert.

## Offen

- Schritt 04: wann genau im Ablauf (nach Bewertung? vor dem Versuch?).
- 05: Reihenfolge zu Scan/Bewertung — wird vor oder nach dem Scannen aufgeteilt?
- Naht-Typ(en) außer Stumpfstoß? Hersteller, Blech-Herkunft als Feld?
- ISO-Norm der Nahtbewertung (z. B. ISO 5817?) und Stufe.
- Serien: wie viele, wie benannt? Wöhlerlinie je Blech/Charge?
- Belastungsparameter (Spannungsverhältnis R, Frequenz, Ober-/Unterspannung, Abbruchkriterien).
- Dateiformate: ATOS/GOM, IMC, Fotos, Mikroskop, Excel-Listen.
- „Pro Probe sehen, wo sie steht und was als Nächstes dran ist“ → Feld „Next step“ (Standard).
