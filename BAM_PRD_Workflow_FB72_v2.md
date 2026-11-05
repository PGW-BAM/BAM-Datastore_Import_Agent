# PRD v2: Wöhlerversuche an Schweißverbindungen (FB 7.2 Ingenieurbau)

> Input für die Agenten-Pipeline (`/bam-analyze-prd`). Beschreibt **was** der Fachbereich dokumentieren will —
> **nicht**, welche openBIS-Typen schon existieren. Das entscheidet die Pipeline (REUSE / EXTEND / CREATE / LIVE-ONLY).
> Vorgänger: `BAM_PRD_Workflow_FB72.md` (v1, 12 Schritt-Typen als Kette).
> Geändert 2026-11-04 nach ◆ B („B freigegeben (Variante E)“): P1 (Prozesslinie statt flach) und §5 (Geräte als Link-Felder
> statt als Eltern). Muster und Quellen: `workflow/strukturmuster.md`.

---

## 1. Ziel

Zyklische Ermüdungsversuche (Wöhlerlinien / S-N-Kurven) an geschweißten Proben (Stumpfstoß, Kreuzstoß) sollen in
openBIS (BAM Data Store) so dokumentiert werden, dass

1. **jede Probe von der Eingangsprüfung bis zur Bruchfläche nachvollziehbar** ist,
2. **pro Prüfserie auf einen Blick** sichtbar ist, welche Probe in welchem Ablaufschritt steht und **was als Nächstes kommt**,
3. jeder Messwert und jede Datei einen **eindeutigen Ort** hat („wo gehört was hin"),
4. die Daten später **maschinell auswertbar** sind (Wöhlerlinie aus der Serientabelle, Parser für IMC-Rohdaten).

## 2. Strukturprinzipien (verbindlich)

| # | Prinzip | Bedeutung |
|---|---|---|
| P1 | **Prozesslinie** | Space → Projekt → Collection (= Prüfserie) → Objekte. Die Objekte einer Probe bilden **eine Linie in Ablauf-Reihenfolge** (Eltern → Kind): Probe → 3D-Scan & Nahtanalyse → Zyklischer Ermüdungsversuch → Bruchflächenanalyse. Eltern/Kind nur für Herkunft und Reihenfolge, keine Abzweigungen ohne fachlichen Grund. Alle Objekte einer Serie liegen **in der Serien-Collection**. |
| P2 | **Flache Typ-Hierarchie** | Neue Typen erben direkt von einer existierenden BAM-Basisklasse; keine eigenen Zwischenebenen. So wenige neue Typen wie möglich. |
| P3 | **Probendaten an die Probe** | Eigenschaften, die die Probe beschreiben (Verzug, Geometrie, Nahtbewertung, Lastniveau), sind Properties der Probe → die Collection-Tabelle ist die Versuchsmatrix. |
| P4 | **Tätigkeiten mit Gerät/Datei = Versuchsschritt** | Ein eigenes Schritt-Objekt nur dort, wo Gerät(e), Zeitraum, Bearbeiter*in und Dateien zusammengehören. Mehrere Ablaufschritte am selben Arbeitsplatz werden in **einem** Objekt mit **nummerierten Sektionen** zusammengefasst. |
| P5 | **Ablaufplan sichtbar** | Sektionen tragen die Schrittnummer („07 DMS-Applikation"). Jede Probe hat ein Feld **„Nächster Schritt"** (geordnete Auswahlliste 01–12 + abgeschlossen). Ein SOP-Objekt „Ablaufplan" im Projekt beschreibt alle Schritte und die Ablageorte. |
| P6 | **Reuse-first** | Geräte, Hilfsstoffe, Standard-Schritte, Collection- und Dataset-Typen aus `bam-masterdata` wiederverwenden. Live bereits vorhandene, nicht standardisierte Typen werden **nicht** weiterverwendet, sondern in den Standard überführt. |
| P7 | **Lean Properties** | Tabellen (Lastprogramm, Rastlinien, Messreihen) sind **Dateien**, keine Properties. |
| P8 | **Sprache nach BAM-Konvention** | Beschreibungen (`description`) zweisprachig `"English//Deutsch"` (ohne Leerzeichen um `//`); `property_label` und Sektionsnamen englisch wie im übrigen `bam-masterdata` (Stand 10/2026: 0 von 1786 Sektionen zweisprachig). |

## 3. Versuchsablauf (unverändert, 12 Schritte)

| Nr. | Schritt | Erfasste Daten | Geräte / Material | Dateien |
|---|---|---|---|---|
| 01 | Vorqualitätsprüfung der Schweißnaht | Winkelverzug initial [°], Kantenversatz initial [mm], wurde gerichtet (ja/nein), Winkelverzug nach Richten [°], Kantenversatz nach Richten [mm], grobe Nahtfehler (Text) | – | Probenfotos |
| 02 | Anfasen / Schleifen | Dokumentation von Nahtüberhöhungs-Bearbeitung / Schleifhinweisen (Text) | – | Nachbearbeitungsprotokoll (PDF) |
| 03 | 3D-Scan der Probe | – | ZEISS GOM ATOS 5 | 3D-Scan-Rohdaten |
| 04 | Nahtanalyse (GOM) | Bewertungsgruppe nach ISO 5817 Anhang C (C63, B90, B125) | GOM-Software | Auswerte-Export |
| 05 | Serienzuordnung (Randomisierung) | Zuordnung zur Prüfserie, Lastniveau (hoch/mittel/niedrig), Prüfreihenfolge, Herkunftsblech (Bias-Vermeidung) | – | Randomisierungs-Skript |
| 06 | Geometrie vor Einbau | Dicke und Breite an je 3 Positionen [mm], Mittelwerte [mm] | Messschieber | – |
| 07 | DMS-Applikation | DMS-Abstand zum Nahtübergang [mm], DMS-Abstand zum Rand [mm], Zeitpunkt der Applikation | DMS HBM LY11-6/120, Klebstoff HBM X60, Risslumineszenz-Set (MR Chemie), Kamerasystem Luxonis OAK-4D-Pro | DMS-Positionszeichnung, Aufbaufoto |
| 08 | Messverstärker / Prüfstand | Abtastfrequenz [Hz], Aufzeichnungsmodus (Vollsignal / Peak-Counter / Peak-Valley), erfasste Kanäle | IMC-Messverstärker, servohydraulische Prüfmaschine | – |
| 09 | Einbaubeanspruchung | Vorspannkraft [kN] (Biegemoment bei 0,0 kN) | IMC | Biegemoment-Rohdaten (IMC .raw) |
| 10 | Zyklischer Ermüdungsversuch | Rastlinien (Markerlasten) aktiv, Abbruchgrund (Totalbruch / Riss detektiert / Durchläufer (Zyklenzahl erreicht) / manueller Stopp) | Prüfmaschine | Lastprogramm (Excel), Mess-Rohdaten (IMC .raw), Monitoring-Bilder (Zeitraffer) |
| 11 | Auswertung | Bruttoschwingspielzahl, Nettoschwingspielzahl, Zyklen bis 10 % DMS-Abfall je DMS (Text) | – | bereinigte Messdaten (CSV/HDF5), Auswerteplots, Konvertierungsskript |
| 12 | Bruchflächenanalyse | – | Makro-Kamera, Digitalmikroskop | Makrofotos, Mikroskopbilder Rissausgang, Rastlinien-Auswertung (Excel) |

## 4. Probe

Geschweißte Ermüdungsprobe, Kennungen: Herstellerbezeichnung (Original-ID), interne Bezeichnung, finale
Serienbezeichnung (z. B. `S1-01`), Herkunftsblech. Nahtgeometrie: **Stumpfstoß** oder **Kreuzstoß**
(fachliche Vorgabe: als Erweiterung des bestehenden BAM-Schweißnaht-Vokabulars `WELDING.WELD_TYPE`, Begriffe
`BUTT_WELD` „Butt weld//Stumpfstoß", `CRUCIFORM_WELD` „Cruciform weld//Kreuzstoß").
Angestrebte Bewertungsgruppe nach ISO 5817 (B, C, D).

## 5. Inventar (Geräte & Hilfsstoffe)

Geräte und Hilfsstoffe werden **einmal im Inventar** angelegt und vom Versuchsschritt, in dem sie benutzt werden, über
ein **Link-Feld** (Typ OBJECT) verlinkt: nicht als Eltern und nicht als Freitext. So erscheinen sie im Formular des Schritts
als anklickbarer Link, aber nicht im Graphen der Probe. Es gibt keine projekt-eigenen Katalog-Typen für DMS oder Klebstoffe.

## 6. Prüfserie

Eine Prüfserie = eine Collection (z. B. „Serie 1 – Stumpfstoß", „Serie 1 – Kreuzstoß"). Die Collection-Tabelle zeigt
pro Probe: Serienbezeichnung, Nahtgeometrie, Lastniveau, Prüfreihenfolge, Bewertungsgruppe, nächster Schritt,
Schwingspielzahl, Abbruchgrund (Letztere über den Versuchsschritt).

## 7. Lieferumfang der Pipeline

1. `generated/<stem>/requirements.json` und `gap-report.md` (REUSE / EXTEND / CREATE / LIVE-ONLY)
2. `generated/<stem>/datamodel/` — PR-fähige `bam-masterdata`-Klassen nur für CREATE; EXTEND als PR-Anleitung
3. Provisionierung auf der Übungsinstanz dev1 (Masterdaten + Demo-Serie), Notebook für die Wiederholung
4. Parser-Gerüst für Schritt 10/11 (IMC-Rohdaten → Versuchsschritt)
