# Interview-Fragen

Fragen für Schritt 2. Nicht alle auf einmal stellen: pro Ablaufschritt die Grundfragen, dazu nur die
Stichwort-Nachfragen, die zum Gesagten passen. Eigene Ergänzungen sind erwünscht, immer als Vorschlag.

## Grundfragen je Schritt

1. Was passiert hier, wer macht es, wie lange dauert es?
2. Welche Geräte, Werkzeuge, Materialien werden benutzt? Sind sie schon im Inventar des Fachbereichs?
3. Welche Werte werden erfasst? Einheit, Wertebereich oder feste Auswahl, Pflicht ja/nein, wie oft (einmal, je Position, je Sensor)?
4. Welche Dateien entstehen? Format, Größe, aus welchem Gerät oder welcher Software?
5. Was davon willst du später filtern, vergleichen oder auswerten?
6. Was ist das Ergebnis, und was entscheidet sich hier für den nächsten Schritt?

## Querschnitt (einmal pro Projekt)

- **Probe / Untersuchungsobjekt:** Wie heißt es, welche Kennungen gibt es (Hersteller, intern, final)? Wer vergibt sie, wie sind sie aufgebaut?
- **Serien:** Was bildet eine Serie (Collection)? Was soll die Tabelle der Serie pro Probe zeigen?
- **Ablauf sichtbar:** Soll jede Probe zeigen, in welchem Schritt sie steht und was als Nächstes kommt?
- **Personen:** Wer führt Schritte aus, muss das je Schritt erfasst werden?
- **Normen und Richtlinien:** Welche Normen bestimmen Werte oder Auswahllisten (ISO, DIN, ASTM, Hausverfahren)?
- **Dateien:** Rohdaten, bereinigte Daten, Auswertungen, Fotos: was davon gehört zu welchem Schritt?
- **Auswertung:** Gibt es Skripte oder Programme, die die Daten später lesen sollen (Parser)?

## Stichwort-Nachfragen

| Stichwort im Gespräch | Nachfragen |
|---|---|
| DMS, Dehnungsmessstreifen, Sensor | Typ und Hersteller (Inventar oder je Probe)? k-Faktor? Anzahl je Probe fest oder wechselnd? Lage: Abstand zu Naht/Kerbe, Abstand zum Rand, Seite, Ausrichtung zur Last? Klebstoff, Aushärtung? Bei wechselnder Anzahl: Lagen besser als Datei/Zeichnung statt fester Felder? |
| Prüfmaschine, Prüfstand, Lastrahmen | Welche Maschine (Inventar)? Regelung (Kraft/Weg)? Kraftmessdose und Kalibrierstand? Lastprogramm als Datei? Frequenz, Lastverhältnis R, Abbruchkriterien? |
| Schweißnaht, Fügen | Nahtart (Stumpfstoß, Kehlnaht, …)? Bewertung nach Norm (z. B. ISO 5817 Bewertungsgruppe)? Nachbehandlung (Schleifen, Richten)? Wer hat geschweißt, Prozessdaten vorhanden? |
| Messverstärker, Datenerfassung | Gerät (Inventar)? Abtastrate, Kanäle, Aufzeichnungsmodus? Dateiformat der Rohdaten? |
| Kamera, Foto, Video, Zeitraffer | Gerät (Inventar)? Was wird dokumentiert, wie viele Bilder? Belichtung/Auflösung nötig oder egal? |
| Mikroskop, Bruchfläche | Licht/REM/digital? Vergrößerung? Was wird ausgewertet (Rissausgang, Rastlinien)? |
| 3D-Scan, Geometrie | Scanner und Software (Inventar)? Was wird abgeleitet (Verzug, Versatz, Nahtgeometrie)? Export-Format? |
| Messen an Positionen | Wie viele Positionen, fest benannt? Mittelwert erfassen oder berechnen? Je Position ein Feld (wenige, fest) oder Datei (viele, wechselnd)? |
| Temperatur, Ofen, Klima | Sollwert, Istwert, Toleranz? Verlauf als Datei? Gerät (Inventar)? |
| Material, Werkstoff, Charge | Werkstoff nach Norm? Charge/Lieferant? Zeugnis als Datei? Gibt es das Material schon im Inventar? |
| Kalibrierung | Was wird kalibriert, wie oft, wer? Gültig bis? Am Gerät im Inventar oder je Versuch? |
| Software, Skript, Auswertung | Name und Version? Eingabe- und Ausgabedateien? Soll das Skript selbst abgelegt werden? |
| Randomisierung, Reihenfolge | Wie wird zugeordnet (Skript, Los)? Was soll das vermeiden (Bias)? Reihenfolge als Feld? |
| Abbruch, Ergebnis, Status | Feste Auswahl der Abbruchgründe? Wer entscheidet? Was passiert mit Durchläufern? |
