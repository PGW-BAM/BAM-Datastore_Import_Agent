# Wöhlerversuche an Schweißverbindungen / S-N tests on welded joints

**FB 7.2 · Prüfpunkt B · Struktur bestätigen / Checkpoint B · Confirm the structure**

> Markdown-Fassung der Prüfseite. Mit Auswahl und Antworttext: `review/struktur.html` herunterladen und im Browser öffnen. Hier antworten Sie direkt im Chat. / Markdown version of the review page; for buttons and the reply text, download `review/struktur.html` and open it in a browser. Here, reply directly in the chat.

## 1 Welche Struktur soll es werden? / Which structure should it be?

Empfohlen / recommended: **E**. Unten ausgearbeitet / worked out below: **E**. Muster und Quellen: `workflow/strukturmuster.md`.

| | Variante / Variant | Objekte je Probe | Ebenen | neue Typen | Geräte als Eltern |
|---|---|---|---|---|---|
| E | Prozesslinie, Geräte als Felder / Process line, instruments as fields **(empfohlen / recommended)** | 4 | 3 | 2 | 3 |
| A | Flach, Schritte gebündelt / Flat, steps grouped | 4 | 1 | 2 | 9 |
| C | Alles an der Probe / Everything on the specimen | 1 | 0 | 1 | 9 |
| D | Kette wie bisher auf dev1 / Chain as before on dev1 | 13 | 12 | 16 | – |

### E Prozesslinie, Geräte als Felder / Process line, instruments as fields (empfohlen / recommended)

Dieselben vier Objekte wie A, aber als Linie in Ablauf-Reihenfolge: Probe → 3D-Scan → Ermüdungsversuch → Bruchflächenanalyse (M1, M5). Die sechs Geräte und Hilfsstoffe des Ermüdungsversuchs stehen als Link-Felder in seinem Formular, nicht als Eltern (M4), so wie im BAM-Standard beim Kriechversuch. 3D-Scan und Bruchflächenanalyse sind Standard-Schritte ohne Link-Feld; ihre drei Geräte bleiben Eltern.

*The same four objects as A, but as a line in workflow order: specimen → 3D scan → fatigue test → fracture surface analysis (M1, M5). The six instruments and auxiliary materials of the fatigue test are link fields in its form, not parents (M4), as in the BAM standard's creep test. 3D scan and fracture surface analysis are standard steps without a link field; their three instruments stay parents.*

Aufbau / build-up: Probe → 3D-Scan & Nahtanalyse → Zyklischer Ermüdungsversuch → Bruchflächenanalyse

- ＋ Im Graphen einer Probe nur eine Linie aus 4 Kästen, in der Reihenfolge des Ablaufs / *The graph of a specimen is just a line of 4 boxes, in workflow order*
- ＋ Geräte und Hilfsstoffe sind anklickbare Links im Formular; openBIS prüft, dass dort ein Gerät steht / *Instruments and auxiliary materials are clickable links in the form; openBIS checks that an instrument is entered there*
- ＋ Inventar-Objekte verbinden im Graphen nicht mehr alle Proben miteinander / *Inventory objects no longer connect all specimens with each other in the graph*
- ＋ Gleiche Objekte und Felder wie A, nur 2 neue Objekttypen / *Same objects and fields as A, only 2 new object types*
- – Der Graph einer Maschine zeigt nicht mehr, welche Proben auf ihr liefen / *The graph of a machine no longer shows which specimens ran on it*
- – Vom Bruchbild zurück zur Probe sind es 3 Verknüpfungen statt 1 / *From the fracture image back to the specimen it takes 3 links instead of 1*
- – 5 neue Link-Felder zu beantragen; die Prüfmaschine nutzt das Standard-Feld INSTRUMENT / *5 new link fields to request; the testing machine uses the standard field INSTRUMENT*
- – Scanner, Makro-Kamera und Mikroskop bleiben Eltern (Standard-Schritte haben kein Link-Feld) / *Scanner, macro camera and microscope stay parents (standard steps have no link field)*

### A Flach, Schritte gebündelt / Flat, steps grouped

Die Probe trägt alles, was sie beschreibt. Drei Schritt-Objekte hängen direkt an der Probe (M2, M5); Geräte und Hilfsstoffe sind Eltern der Schritte.

*The specimen holds everything that describes it. Three step objects hang directly on the specimen (M2, M5); instruments and auxiliary materials are parents of the steps.*

Aufbau / build-up: Probe ← 3D-Scan & Nahtanalyse · Zyklischer Ermüdungsversuch · Bruchflächenanalyse

- ＋ Nur 4 Objekte je Probe, alle eine Ebene unter der Probe / *Only 4 objects per specimen, all one level below it*
- ＋ Geräte hängen an dem Schritt, bei dem sie benutzt werden (PRD §5) / *Instruments hang on the step where they are used (PRD §5)*
- ＋ Nur 2 neue Objekttypen zu beantragen / *Only 2 new object types to request*
- – Die 9 Geräte und Hilfsstoffe hängen als Eltern an den Schritten aller Proben: Im Graphen ist jede Probe über sie mit allen anderen verbunden, das wird schnell unübersichtlich / *The 9 instruments and auxiliary materials are parents of the steps of every specimen: in the graph every specimen is connected to all others through them, which quickly gets confusing*
- – Die Reihenfolge der Schritte ist im Graphen nicht zu sehen (Stern statt Linie) / *The order of the steps is not visible in the graph (a star instead of a line)*
- – Die Schritte 07–11 haben kein eigenes Objekt, sondern je eine Sektion im Formular „Zyklischer Ermüdungsversuch“ / *Steps 07–11 have no object of their own but one section each in the “Cyclic fatigue test” form*

### C Alles an der Probe / Everything on the specimen

Es gibt nur das Objekt Probe. Alle Werte stehen in Sektionen der Probe, alle Dateien hängen an ihr (M5 bis zum Ende gedacht).

*There is only the specimen object. All values are in sections of the specimen, all files are attached to it (M5 taken all the way).*

Aufbau / build-up: Probe

- ＋ Ein Objekt je Probe: alles auf einer Seite / *One object per specimen: everything on one page*
- ＋ Am wenigsten anzulegen und zu beantragen / *Least to create and to request*
- – Widerspricht dem PRD: Geräte sollen am Versuchsschritt verlinkt werden (§5) / *Contradicts the PRD: instruments are to be linked to the test step (§5)*
- – Man sieht nicht mehr, bei welchem Schritt welches Gerät, welche Person und welcher Zeitraum dazugehört / *You can no longer see which instrument, person and time span belong to which step*
- – Ein sehr langes Formular, Dateien aller Schritte an einem Objekt / *A very long form, files of all steps on one object*

### D Kette wie bisher auf dev1 / Chain as before on dev1

So ist das Modell auf der Übungsinstanz dev1 bisher aufgebaut: Probe → Schritt 1 → … → Schritt 12 (M1 mit Einzelschritten), jeder Schritt ein eigener Typ, Geräte als Eltern.

*This is how the model on the test instance dev1 is built so far: specimen → step 1 → … → step 12 (M1 with single steps), every step a type of its own, instruments as parents.*

Aufbau / build-up: Probe → Vorqualitätsprüfung der Schweißnaht → Anfasen / Schleifen → 3D-Scan der Probe → Nahtanalyse (GOM) → Serienzuordnung (Randomisierung) → Geometrie vor Einbau → DMS-Applikation → Messverstärker / Prüfstand → Einbaubeanspruchung → Zyklischer Ermüdungsversuch → Auswertung → Bruchflächenanalyse

- ＋ Bekannt: so arbeiten Sie bisher / *Familiar: this is how you work so far*
- ＋ Die Reihenfolge der Schritte steckt in den Verknüpfungen / *The order of the steps is in the links*
- – 12 Ebenen: vom Bruchbild zurück zur Probe sind es 12 Verknüpfungen / *12 levels: from the fracture image back to the specimen it takes 12 links*
- – 16 neue Objekttypen und 17 Datei-Typen zu beantragen / *16 new object types and 17 file types to request*
- – Nicht standardisierte Typen auf der Instanz, widerspricht P6 (Standard zuerst) / *Non-standard types on the instance, contradicts P6 (standard first)*

## 2 So ist Ihr Projekt aufgebaut / How your project is built

`/FB_72/WELDED_FATIGUE` → Serie 1 – Stumpfstoß / Series 1 – butt weld (`SERIES_1_BUTT_WELD`), Serie 1 – Kreuzstoß / Series 1 – cruciform weld (`SERIES_1_CRUCIFORM_WELD`)

- **Probe / Specimen** `S1B-01`
- **3D-Scan & Nahtanalyse / 3D scan & weld analysis** `S1B-01-SCAN` ← Probe / Specimen · Schritte / steps 03, 04 · ZEISS GOM ATOS 5
- **Zyklischer Ermüdungsversuch / Cyclic fatigue test** `S1B-01-TEST` ← 3D-Scan & Nahtanalyse / 3D scan & weld analysis · Schritte / steps 07–11 · DMS HBM LY11-6/120 / Strain gauge HBM LY11-6/120, Klebstoff HBM X60 / Adhesive HBM X60, Risslumineszenz-Set (MR Chemie) / Crack luminescence set (MR Chemie), Luxonis OAK-4D-Pro, IMC-Messverstärker / IMC measuring amplifier, Servohydraulische Prüfmaschine / Servo-hydraulic testing machine
- **Bruchflächenanalyse / Fracture surface analysis** `S1B-01-FRACTURE` ← Zyklischer Ermüdungsversuch / Cyclic fatigue test · Schritte / steps 12 · Makro-Kamera / Macro camera, Digitalmikroskop / Digital microscope

## 3 Wo landet welcher Ablaufschritt? / Where does each workflow step go?

| Nr. | Schritt / Step | Objekt / Object | Sektion / Section | Geräte, Dateien |
|---|---|---|---|---|
| 00 | Probe (Identität) / Subject (identity) | Probe / Specimen | Allgemeine Informationen / General Information + Probenidentifikation / Specimen Identification |  |
| 01 | Vorqualitätsprüfung der Schweißnaht / Pre-quality check of the weld | Probe / Specimen | Vorqualitätsprüfung / Initial Quality Check | Probenfotos / Specimen photos |
| 02 | Anfasen / Schleifen / Chamfering / grinding | Probe / Specimen | Anfasen und Schleifen / Chamfering And Grinding | Nachbearbeitungsprotokoll (PDF) / Post-processing report |
| 03 | 3D-Scan der Probe / 3D scan of the specimen | 3D-Scan & Nahtanalyse / 3D scan & weld analysis |  | ZEISS GOM ATOS 5, 3D-Scan-Rohdaten / 3D scan raw data |
| 04 | Nahtanalyse (GOM) / Weld analysis (GOM) | 3D-Scan & Nahtanalyse / 3D scan & weld analysis | Nahtanalyse / Weld Analysis | GOM software (text in SCAN step), Auswerte-Export / Evaluation export |
| 05 | Serienzuordnung (Randomisierung) / Series assignment (randomisation) | Probe / Specimen | Serienzuordnung / Series Assignment | Randomisierungs-Skript / Randomisation script |
| 06 | Geometrie vor Einbau / Geometry before installation | Probe / Specimen | Geometrie vor Einbau / Geometry Before Installation | Caliper (no inventory object/link; named in SOP only) |
| 07 | DMS-Applikation / Strain gauge application | Zyklischer Ermüdungsversuch / Cyclic fatigue test | DMS-Applikation / Strain Gauge Application | DMS HBM LY11-6/120 / Strain gauge HBM LY11-6/120, Klebstoff HBM X60 / Adhesive HBM X60, Risslumineszenz-Set (MR Chemie) / Crack luminescence set (MR Chemie), Luxonis OAK-4D-Pro, DMS-Positionszeichnung / Strain gauge position drawing, Aufbaufoto / Setup photo |
| 08 | Messverstärker / Prüfstand / Measuring amplifier / test rig | Zyklischer Ermüdungsversuch / Cyclic fatigue test | Messverstärker und Prüfstand / Measuring Amplifier And Test Rig | IMC-Messverstärker / IMC measuring amplifier, Servohydraulische Prüfmaschine / Servo-hydraulic testing machine |
| 09 | Einbaubeanspruchung / Installation stress | Zyklischer Ermüdungsversuch / Cyclic fatigue test | Einbaubeanspruchung / Installation Stress | IMC-Messverstärker / IMC measuring amplifier, Biegemoment-Rohdaten (IMC .raw) / Bending moment raw data |
| 10 | Zyklischer Ermüdungsversuch / Cyclic fatigue test | Zyklischer Ermüdungsversuch / Cyclic fatigue test | Zyklischer Ermüdungsversuch / Cyclic Fatigue Test | Servohydraulische Prüfmaschine / Servo-hydraulic testing machine, Lastprogramm (Excel) / Load programme, Mess-Rohdaten (IMC .raw) / Measurement raw data, Monitoring-Bilder (Zeitraffer) / Monitoring images (time-lapse) |
| 11 | Auswertung / Evaluation | Zyklischer Ermüdungsversuch / Cyclic fatigue test | Auswertung / Evaluation | Bereinigte Messdaten (CSV/HDF5) / Cleaned measurement data, Auswerteplots / Evaluation plots, Konvertierungsskript / Conversion script |
| 12 | Bruchflächenanalyse / Fracture surface analysis | Bruchflächenanalyse / Fracture surface analysis |  | Makro-Kamera / Macro camera, Digitalmikroskop / Digital microscope, Makrofotos / Macro photos, Mikroskopbilder Rissausgang / Microscope images of crack origin, Rastlinien-Auswertung (Excel) / Beach-mark evaluation |
| P5 | Ablaufstatus / Workflow status | Probe / Specimen | Ablaufstatus / Workflow Status |  |

## 4 Welche Felder bekommt jedes Objekt? / Which fields does each object get?

### Zyklischer Ermüdungsversuch / Cyclic fatigue test (`EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST`)

| Sektion / Section | Feld / Field | Typ | Pflicht | neu |
|---|---|---|---|---|
| Allgemeine Informationen / General Information | Name | Text |  |  |
| Allgemeine Informationen / General Information | Experiment completed | Ja / Nein |  |  |
| Allgemeine Informationen / General Information | Startdatum / Start date | Datum und Uhrzeit |  |  |
| Allgemeine Informationen / General Information | Enddatum / End date | Datum und Uhrzeit |  |  |
| Allgemeine Informationen / General Information | OPERATOR | Text |  |  |
| Versuchsdetails / Experimental Details | EXPERIMENTAL_STEP.EXPERIMENTAL_GOALS | Text, mehrzeilig |  |  |
| Versuchsdetails / Experimental Details | EXPERIMENTAL_STEP.EXPERIMENTAL_DESCRIPTION | Text, mehrzeilig |  |  |
| Versuchsdetails / Experimental Details | EXPERIMENTAL_STEP.EXPERIMENTAL_RESULTS | Text, mehrzeilig |  |  |
| Versuchsdetails / Experimental Details | EXPERIMENTAL_STEP.SPREADSHEET | formatierter Text |  |  |
| Referenzen / References | References | Text, mehrzeilig |  |  |
| Referenzen / References | Publication | Text, mehrzeilig |  |  |
| Zusätzliche Informationen / Additional Information | Notes | Text, mehrzeilig |  |  |
| DMS-Applikation / Strain Gauge Application | DMS-Abstand zum Nahtübergang [mm] / Strain gauge distance to weld toe [mm] | Zahl |  | neu |
| DMS-Applikation / Strain Gauge Application | DMS-Abstand zum Probenrand [mm] / Strain gauge distance to edge [mm] | Zahl |  | neu |
| DMS-Applikation / Strain Gauge Application | Zeitpunkt der DMS-Applikation / Time of strain gauge application | Datum und Uhrzeit |  | neu |
| DMS-Applikation / Strain Gauge Application | Dehnungsmessstreifen (DMS) / Strain gauge | Verweis auf ein Objekt |  | neu |
| DMS-Applikation / Strain Gauge Application | DMS-Klebstoff / Strain gauge adhesive | Verweis auf ein Objekt |  | neu |
| DMS-Applikation / Strain Gauge Application | Rissprüfmittel / Crack detection agent | Verweis auf ein Objekt |  | neu |
| DMS-Applikation / Strain Gauge Application | Überwachungskamera / Monitoring camera | Verweis auf ein Objekt |  | neu |
| Messverstärker und Prüfstand / Measuring Amplifier And Test Rig | Messverstärker / Measuring amplifier | Verweis auf ein Objekt |  | neu |
| Messverstärker und Prüfstand / Measuring Amplifier And Test Rig | Prüfmaschine oder Messgerät / Testing Machine or Measurement Device | Verweis auf ein Objekt |  |  |
| Messverstärker und Prüfstand / Measuring Amplifier And Test Rig | Abtastfrequenz [Hz] / Sampling frequency [Hz] | ganze Zahl |  | neu |
| Messverstärker und Prüfstand / Measuring Amplifier And Test Rig | Aufzeichnungsmodus / Recording mode | Auswahl |  | neu |
| Messverstärker und Prüfstand / Measuring Amplifier And Test Rig | Erfasste Kanäle / Recorded channels | Text |  | neu |
| Einbaubeanspruchung / Installation Stress | Vorspannkraft [kN] / Preload force [kN] | Zahl |  | neu |
| Zyklischer Ermüdungsversuch / Cyclic Fatigue Test | Rastlinien (Markerlasten) aktiv / Beach marks (marker loads) active | Ja / Nein |  | neu |
| Zyklischer Ermüdungsversuch / Cyclic Fatigue Test | Abbruchgrund / Termination reason | Auswahl |  | neu |
| Auswertung / Evaluation | Bruttoschwingspielzahl / Gross number of cycles | ganze Zahl |  | neu |
| Auswertung / Evaluation | Nettoschwingspielzahl / Net number of cycles | ganze Zahl |  | neu |
| Auswertung / Evaluation | Zyklen bis 10 % DMS-Abfall je DMS / Cycles to 10 % strain gauge drop per strain gauge | Text, mehrzeilig |  | neu |

### Geschweißte Ermüdungsprobe / Welded fatigue specimen (`SAMPLE.WELDED_FATIGUE_SPECIMEN`)

| Sektion / Section | Feld / Field | Typ | Pflicht | neu |
|---|---|---|---|---|
| Allgemeine Informationen / General Information | Name | Text | ja |  |
| Allgemeine Informationen / General Information | Alternative Name | Text |  |  |
| Allgemeine Informationen / General Information | DESCRIPTION | Text, mehrzeilig |  |  |
| Allgemeine Informationen / General Information | SAMPLE_ID_NUMBER | ganze Zahl |  |  |
| Allgemeine Informationen / General Information | MANUFACTURER | Text |  |  |
| Allgemeine Informationen / General Information | BARCODE_EXTERNAL | Text |  |  |
| Allgemeine Informationen / General Information | SUPPLIER | Text |  |  |
| Eigenschaften / Properties | PHYSICAL_STATE | Auswahl |  |  |
| BAM-Informationen / BAM Information | BAM_OE | Auswahl | ja |  |
| BAM-Informationen / BAM Information | Verantwortliche Person / Responsible person | Verweis auf ein Objekt |  |  |
| BAM-Informationen / BAM Information | CO_RESPONSIBLE_PERSON | Verweis auf ein Objekt |  |  |
| BAM-Informationen / BAM Information | BAM_ROOM | Auswahl |  |  |
| BAM-Informationen / BAM Information | BAM_FLOOR | Auswahl |  |  |
| BAM-Informationen / BAM Information | BAM_HOUSE | Auswahl |  |  |
| BAM-Informationen / BAM Information | BAM_LOCATION | Auswahl |  |  |
| BAM-Informationen / BAM Information | BAM_LOCATION_COMPLETE | Auswahl |  |  |
| Zusätzliche Informationen / Additional Information | Notes | Text, mehrzeilig |  |  |
| Ablaufstatus / Workflow Status | Nächster Schritt / Next step | Auswahl |  | neu |
| Probenidentifikation / Specimen Identification | Herstellerbezeichnung (Original-ID) / Manufacturer designation (original ID) | Text |  | neu |
| Probenidentifikation / Specimen Identification | Herkunftsblech / Source sheet | Text |  | neu |
| Probenidentifikation / Specimen Identification | Art der Schweißverbindung / Type of weld | Auswahl |  |  |
| Probenidentifikation / Specimen Identification | Angestrebte Bewertungsgruppe (ISO 5817) / Target quality level (ISO 5817) | Auswahl |  | neu |
| Vorqualitätsprüfung / Initial Quality Check | Winkelverzug initial [°] / Initial angular distortion [°] | Zahl |  | neu |
| Vorqualitätsprüfung / Initial Quality Check | Kantenversatz initial [mm] / Initial edge misalignment [mm] | Zahl |  | neu |
| Vorqualitätsprüfung / Initial Quality Check | Wurde gerichtet / Was straightened | Ja / Nein |  | neu |
| Vorqualitätsprüfung / Initial Quality Check | Winkelverzug nach dem Richten [°] / Angular distortion after straightening [°] | Zahl |  | neu |
| Vorqualitätsprüfung / Initial Quality Check | Kantenversatz nach dem Richten [mm] / Edge misalignment after straightening [mm] | Zahl |  | neu |
| Vorqualitätsprüfung / Initial Quality Check | Beschreibung der Defekte / Defect description | Text, mehrzeilig |  |  |
| Anfasen und Schleifen / Chamfering And Grinding | Nahtüberhöhungs-Bearbeitung / Schleifhinweise / Weld reinforcement treatment / grinding notes | Text, mehrzeilig |  | neu |
| Nahtanalyse / Weld Analysis | Bewertungsgruppe ISO 5817 Anhang C / Quality level ISO 5817 Annex C | Auswahl |  | neu |
| Serienzuordnung / Series Assignment | Lastniveau / Load level | Auswahl |  | neu |
| Serienzuordnung / Series Assignment | Prüfreihenfolge / Test order | ganze Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Dicke Position 1 [mm] / Thickness position 1 [mm] | Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Dicke Position 2 [mm] / Thickness position 2 [mm] | Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Dicke Position 3 [mm] / Thickness position 3 [mm] | Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Breite Position 1 [mm] / Width position 1 [mm] | Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Breite Position 2 [mm] / Width position 2 [mm] | Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Breite Position 3 [mm] / Width position 3 [mm] | Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Mittlere Dicke [mm] / Mean thickness [mm] | Zahl |  | neu |
| Geometrie vor Einbau / Geometry Before Installation | Mittlere Breite [mm] / Mean width [mm] | Zahl |  | neu |

## 5 Serientabelle / Series table

Spalten / columns: Serienbezeichnung / Series designation · Nahtgeometrie / Weld geometry · Lastniveau / Load level · Prüfreihenfolge / Test order · Bewertungsgruppe / Quality level · Nächster Schritt / Next step · Schwingspielzahl / Number of cycles · Abbruchgrund / Termination reason

## 6 Auswahllisten / Choice lists

- **Hilfsstofftyp / Auxiliary Material Types** (`AUXILIARY_MATERIAL_TYPE`, ergänzt / extended): Schleifmittel / Abrasive · Klebstoff / Adhesive · Reinigungsmittel / Cleaner · Flussmittel / Flux · Schmierstoff / Lubricant · Poliermittel / Polishing Agent · Rasierklinge / Razorblade · Lot / Solder · Lösungsmittel / Solvent · Schweisszusatz / Welding Additive · **Dehnungsmessstreifen (DMS) / Strain gauge** · **Rissprüfmittel / Crack detection agent**
- **Arten von Schweißverbindungen / Types of welds** (`WELDING.WELD_TYPE`, ergänzt / extended): fillet weld · groove weld · plug weld · spot weld · surfacing weld · tack weld · **Stumpfstoß / butt weld** · **Kreuzstoß / cruciform weld**
- **Geordnete Ablaufschritte des Schweißnaht-Ermüdungsprogramms / Ordered workflow steps of the welded fatigue test programme** (`WELDED_FATIGUE_WORKFLOW_STEP`, neu): **01 Vorqualitätsprüfung / 01 Pre-quality check** · **02 Anfasen / Schleifen / 02 Chamfering / grinding** · **03 3D-Scan / 03 3D scan** · **04 Nahtanalyse / 04 Weld analysis** · **05 Serienzuordnung / 05 Series assignment** · **06 Geometrie vor Einbau / 06 Geometry before installation** · **07 DMS-Applikation / 07 Strain gauge application** · **08 Messverstärker / Prüfstand / 08 Measuring amplifier / test rig** · **09 Einbaubeanspruchung / 09 Installation stress** · **10 Zyklischer Ermüdungsversuch / 10 Cyclic fatigue test** · **11 Auswertung / 11 Evaluation** · **12 Bruchflächenanalyse / 12 Fracture surface analysis** · **Abgeschlossen / Done**
- **Bewertungsgruppen für Unregelmäßigkeiten nach ISO 5817 / Quality levels for imperfections according to ISO 5817** (`WELDING.ISO_5817_QUALITY_LEVEL`, neu): **B** · **C** · **D**
- **Bewertungsgruppen für schwingend beanspruchte Konstruktionen nach ISO 5817 Anhang C / Quality levels for fatigue-loaded structures according to ISO 5817 Annex C** (`WELDING.ISO_5817_ANNEX_C_RATING`, neu): **C63** · **B90** · **B125**
- **Lastniveau einer Probe innerhalb einer Ermüdungsprüfserie / Load level of a specimen within a fatigue test series** (`FATIGUE.LOAD_LEVEL`, neu): **Hoch / High** · **Mittel / Medium** · **Niedrig / Low**
- **Aufzeichnungsmodus des Messverstärkers in Ermüdungsversuchen / Data recording mode of the measuring amplifier in fatigue tests** (`FATIGUE.RECORDING_MODE`, neu): **Vollsignal / Full signal** · **Peak-Counter / Peak counter** · **Peak-Valley / Peak-valley**
- **Grund für den Abbruch eines Ermüdungsversuchs / Reason for terminating a fatigue test** (`FATIGUE.TERMINATION_REASON`, neu): **Totalbruch / Total fracture** · **Riss detektiert / Crack detected** · **Durchläufer / Run-out** · **Manueller Stopp / Manual stop**

## Ihre Antwort / Your reply

Schreiben Sie im Chat „B freigegeben“ (Variante E) oder eine Liste der Änderungen, je Teil eine Zeile. / Write “B approved” (Variante E) in the chat, or a list of changes, one line per part.

Teile / Parts: Variante · Aufbau · Zuordnung der Schritte · Felder je Objekt · Serientabelle · Auswahllisten · Begriffe

