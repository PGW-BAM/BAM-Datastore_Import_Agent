# PRD: Synthese von Silber-Nanopartikeln / Synthesis of silver nanoparticles (FB 0.0, Testprojekt)

> Frei erfundenes Testprojekt für die Werkzeuge. Quelle: kein Interview. Stand: 2026-11-04.

## 1. Ziel

Silber-Nanopartikel werden chargenweise hergestellt. In openBIS soll nachvollziehbar sein,

1. aus welchen **Edukten** (Charge im Inventar) und unter welchen **Bedingungen** eine Charge entstand,
2. welche **Größe und Form** jede Charge hat (DLS, TEM),
3. wie sich die Chargen einer Serie **vergleichen** lassen (Serientabelle).

## 2. Strukturprinzipien

Es gelten P1–P8 aus `workflow/README.md`. Abweichungen für dieses Projekt (mit Begründung):

- keine

## 3. Ablauf

| Nr. | Schritt (Deutsch / Englisch) | Erfasste Daten (Deutsch / Englisch, Einheit, Auswahl, Pflicht) | Geräte / Material | Dateien |
|---|---|---|---|---|
| 01 | Einwaage der Edukte / Weighing of reactants | Masse Silbernitrat / Mass of silver nitrate [mg], Masse Natriumcitrat / Mass of sodium citrate [mg] | Silbernitrat / Silver nitrate, Trinatriumcitrat / Trisodium citrate, Analysenwaage / Analytical balance | – |
| 02 | Synthese / Synthesis | Reaktionstemperatur / Reaction temperature [°C], Reaktionszeit / Reaction time [min] (Pflicht) | Heizrührer / Heating stirrer | Temperaturverlauf / Temperature log (CSV) |
| 03 | Aufreinigung / Purification | Ausbeute / Yield [%], Zieldurchmesser / Target diameter [nm] | Zentrifuge / Centrifuge | – |
| 04 | DLS-Messung / DLS measurement | mittlerer hydrodynamischer Durchmesser / mean hydrodynamic diameter [nm], PDI | DLS-Gerät / DLS instrument | DLS-Rohdaten / DLS raw data |
| 05 | TEM-Aufnahmen / TEM imaging | Partikelform / Particle shape (Kugel / sphere, Stäbchen / rod, Plättchen / plate) | Transmissionselektronenmikroskop / Transmission electron microscope | TEM-Bilder / TEM images |

## 4. Hauptobjekt

**Charge / Batch** einer Synthese. Kennung `AG-<laufende Nummer>` (z. B. `AG-01`), vergeben bei der Synthese. Beschreibt:
Zieldurchmesser, Ausbeute, Partikelform, nächster Schritt.

## 5. Inventar

Edukte (Chemikalien) und Geräte stehen einmal im Inventar. Edukte sind Herkunft der Charge (Eltern der Synthese),
Geräte werden über Link-Felder verlinkt, wo der Schritt-Typ eines hat.

## 6. Serien

Eine Serie = eine Synthese-Route (z. B. „Citrat-Route“). Die Serientabelle zeigt je Charge: Name, Zieldurchmesser,
Ausbeute, Partikelform, nächster Schritt.

## 7. Dateien

| Datei | Format | Entsteht in Schritt | Gerät/Software | gehört an |
|---|---|---|---|---|
| Temperaturverlauf / Temperature log | CSV | 02 | Heizrührer | Synthese |
| DLS-Rohdaten / DLS raw data | geräteeigen | 04 | DLS-Gerät | DLS-Messung |
| TEM-Bilder / TEM images | TIFF | 05 | TEM | TEM-Aufnahmen |

## 8. Fachliche Entscheidungen

| Entscheidung | Von | Datum |
|---|---|---|
| Für DLS und TEM die Standard-Schritte aus bam-masterdata verwenden | Testprojekt | 2026-11-04 |

## 9. Offen / später

- Zeta-Potential als weiterer Messwert?
