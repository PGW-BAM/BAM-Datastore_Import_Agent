# Wöhlerversuche an Schweißverbindungen / S-N tests on welded joints

**FB 7.2 · Prüfpunkt E · Trockenlauf freigeben / Checkpoint E · Approve the dry run**

> Markdown-Fassung der Prüfseite. Mit Auswahl und Antworttext: `review/trockenlauf.html` herunterladen und im Browser öffnen. Hier antworten Sie direkt im Chat. / Markdown version of the review page; for buttons and the reply text, download `review/trockenlauf.html` and open it in a browser. Here, reply directly in the chat.

**Noch kein Trockenlauf.** Im BAM-Netz: `python tools/bruecke.py fb72_welded_fatigue trockenlauf`. Bis dahin nur der Plan aus `structure.json`. / No dry run yet; only the plan from `structure.json`.

## Wohin / Where

- Instanz / instance: `https://playground.datastore.bam.de`
- Projekt / project: `/FB_72/WELDED_FATIGUE`
- Collections: `SERIES_1_BUTT_WELD`, `SERIES_1_CRUCIFORM_WELD`

## Objekte / Objects

| Objekt | Typ | Eltern / Parents | Status |
|---|---|---|---|
| ZEISS GOM ATOS 5 `GOM_ATOS_5` | Messgerät / Measuring Instrument | – | noch nicht geprüft |
| Digitalmikroskop / Digital microscope `DIGITAL_MICROSCOPE_01` | Messgerät / Measuring Instrument | – | noch nicht geprüft |
| Kamerasystem Luxonis OAK-4D-Pro / Luxonis OAK-4D-Pro camera system `LUXONIS_OAK_4D_PRO_CAM` | Eine generische Kamera für Video- oder Fotoaufnahmen / A generic camera  device for recording video or photos | – | noch nicht geprüft |
| Makro-Kamera / Macro camera `MACRO_CAMERA_01` | Eine generische Kamera für Video- oder Fotoaufnahmen / A generic camera  device for recording video or photos | – | noch nicht geprüft |
| IMC-Messverstärker / IMC measuring amplifier `IMC_AMPLIFIER_01` | Messverstärker / Measuring Amplifier | – | noch nicht geprüft |
| Servohydraulische Prüfmaschine / Servo-hydraulic testing machine `SERVOHYDRAULIC_RIG_01` | Maschine zur Durchführung von mechanischen Prüfungen an Probekörpern oder Bauteilen / Machine for performing mechanical tests on specimens or components | – | noch nicht geprüft |
| DMS HBM LY11-6/120 (120 Ohm) / Strain gauge HBM LY11-6/120 (120 Ohm) `DMS_HBM_LY11_6_120` | Hilfsstoff / Auxiliary Material | – | noch nicht geprüft |
| Klebstoff HBM X60 / Adhesive HBM X60 `ADHESIVE_HBM_X60` | Hilfsstoff / Auxiliary Material | – | noch nicht geprüft |
| Risslumineszenz-Set / Crack luminescence set `CRACK_LUMINESCENCE_SET` | Hilfsstoff / Auxiliary Material | – | noch nicht geprüft |
| Ablaufplan / Workflow plan `WORKFLOW_PLAN` | GENERAL_PROTOCOL | – | noch nicht geprüft |
| S1B-01 `S1B-01` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1B-02 `S1B-02` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1B-03 `S1B-03` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1B-04 `S1B-04` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1B-05 `S1B-05` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1B-06 `S1B-06` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1C-01 `S1C-01` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1C-02 `S1C-02` | Geschweißte Ermüdungsprobe / Welded fatigue specimen | – | noch nicht geprüft |
| S1B-01 · 03-04 3D-Scan & Nahtanalyse / 3D scan & weld analysis `S1B-01-SCAN` | Experimenteller Schritt (allgemein) / Experimental Step (generic) | S1B-01, ZEISS GOM ATOS 5 | noch nicht geprüft |
| S1B-01 · 07-11 Zyklischer Ermüdungsversuch / Cyclic fatigue test `S1B-01-TEST` | Zyklischer Ermüdungsversuch / Cyclic fatigue test | S1B-01, DMS HBM LY11-6/120 (120 Ohm) / Strain gauge HBM LY11-6/120 (120 Ohm), Klebstoff HBM X60 / Adhesive HBM X60, Risslumineszenz-Set / Crack luminescence set, Kamerasystem Luxonis OAK-4D-Pro / Luxonis OAK-4D-Pro camera system, IMC-Messverstärker / IMC measuring amplifier, Servohydraulische Prüfmaschine / Servo-hydraulic testing machine | noch nicht geprüft |
| S1B-01 · 12 Bruchflächenanalyse / Fracture surface analysis `S1B-01-FRACTURE` | Experimenteller Schritt (allgemein) / Experimental Step (generic) | S1B-01, Makro-Kamera / Macro camera, Digitalmikroskop / Digital microscope | noch nicht geprüft |
| S1B-02 · 03-04 3D-Scan & Nahtanalyse / 3D scan & weld analysis `S1B-02-SCAN` | Experimenteller Schritt (allgemein) / Experimental Step (generic) | S1B-02, ZEISS GOM ATOS 5 | noch nicht geprüft |
| S1B-02 · 07-11 Zyklischer Ermüdungsversuch / Cyclic fatigue test `S1B-02-TEST` | Zyklischer Ermüdungsversuch / Cyclic fatigue test | S1B-02, DMS HBM LY11-6/120 (120 Ohm) / Strain gauge HBM LY11-6/120 (120 Ohm), Klebstoff HBM X60 / Adhesive HBM X60, Risslumineszenz-Set / Crack luminescence set, Kamerasystem Luxonis OAK-4D-Pro / Luxonis OAK-4D-Pro camera system, IMC-Messverstärker / IMC measuring amplifier, Servohydraulische Prüfmaschine / Servo-hydraulic testing machine | noch nicht geprüft |
| S1B-03 · 03-04 3D-Scan & Nahtanalyse / 3D scan & weld analysis `S1B-03-SCAN` | Experimenteller Schritt (allgemein) / Experimental Step (generic) | S1B-03, ZEISS GOM ATOS 5 | noch nicht geprüft |
| S1B-03 · 07-11 Zyklischer Ermüdungsversuch / Cyclic fatigue test `S1B-03-TEST` | Zyklischer Ermüdungsversuch / Cyclic fatigue test | S1B-03, DMS HBM LY11-6/120 (120 Ohm) / Strain gauge HBM LY11-6/120 (120 Ohm), Klebstoff HBM X60 / Adhesive HBM X60, Risslumineszenz-Set / Crack luminescence set, Kamerasystem Luxonis OAK-4D-Pro / Luxonis OAK-4D-Pro camera system, IMC-Messverstärker / IMC measuring amplifier, Servohydraulische Prüfmaschine / Servo-hydraulic testing machine | noch nicht geprüft |
| S1B-04 · 03-04 3D-Scan & Nahtanalyse / 3D scan & weld analysis `S1B-04-SCAN` | Experimenteller Schritt (allgemein) / Experimental Step (generic) | S1B-04, ZEISS GOM ATOS 5 | noch nicht geprüft |
| S1B-04 · 07-11 Zyklischer Ermüdungsversuch / Cyclic fatigue test `S1B-04-TEST` | Zyklischer Ermüdungsversuch / Cyclic fatigue test | S1B-04, DMS HBM LY11-6/120 (120 Ohm) / Strain gauge HBM LY11-6/120 (120 Ohm), Klebstoff HBM X60 / Adhesive HBM X60, Risslumineszenz-Set / Crack luminescence set, Kamerasystem Luxonis OAK-4D-Pro / Luxonis OAK-4D-Pro camera system, IMC-Messverstärker / IMC measuring amplifier, Servohydraulische Prüfmaschine / Servo-hydraulic testing machine | noch nicht geprüft |
| S1B-05 · 03-04 3D-Scan & Nahtanalyse / 3D scan & weld analysis `S1B-05-SCAN` | Experimenteller Schritt (allgemein) / Experimental Step (generic) | S1B-05, ZEISS GOM ATOS 5 | noch nicht geprüft |

## Ihre Antwort / Your reply

Schreiben Sie im Chat „E freigegeben“ oder eine Liste der Änderungen, je Teil eine Zeile. / Write “E approved” in the chat, or a list of changes, one line per part.

Teile / Parts: Instanz, Space und Projekt · Objekte und Eltern · Fehlende Werte

