# Wöhlerversuche an Schweißverbindungen / S-N tests on welded joints

**FB 7.2 · Prüfpunkte C und D · Antrag prüfen und senden / Checkpoints C and D · Review and send the request**

> Markdown-Fassung der Prüfseite. Mit Auswahl und Antworttext: `review/antrag.html` herunterladen und im Browser öffnen. Hier antworten Sie direkt im Chat. / Markdown version of the review page; for buttons and the reply text, download `review/antrag.html` and open it in a browser. Here, reply directly in the chat.

## Das beantragen Sie / What you request

- neue Objekttypen / new object types: 2
- neue Felder / new fields: 38
- neue Auswahllisten / new choice lists: 6
- ergänzte Begriffe / added terms: 4

## Neue Objekttypen / New object types

- **Zyklischer Ermüdungsversuch / Cyclic fatigue test** (`EXPERIMENTAL_STEP.MECHANICAL_TEST.CYCLIC_FATIGUE_TEST`)
- **Geschweißte Ermüdungsprobe / Welded fatigue specimen** (`SAMPLE.WELDED_FATIGUE_SPECIMEN`)

## Neue Felder / New fields

| Code | Name | Typ |
|---|---|---|
| `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_WELD_TOE` | DMS-Abstand zum Nahtübergang [mm] / Strain gauge distance to weld toe [mm] | REAL |
| `FATIGUE.STRAIN_GAUGE_DISTANCE_TO_EDGE` | DMS-Abstand zum Probenrand [mm] / Strain gauge distance to edge [mm] | REAL |
| `FATIGUE.STRAIN_GAUGE_APPLICATION_TIME` | Zeitpunkt der DMS-Applikation / Time of strain gauge application | TIMESTAMP |
| `FATIGUE.STRAIN_GAUGE` | Dehnungsmessstreifen (DMS) / Strain gauge | OBJECT |
| `FATIGUE.STRAIN_GAUGE_ADHESIVE` | DMS-Klebstoff / Strain gauge adhesive | OBJECT |
| `FATIGUE.CRACK_DETECTION_AGENT` | Rissprüfmittel / Crack detection agent | OBJECT |
| `FATIGUE.MONITORING_CAMERA` | Überwachungskamera / Monitoring camera | OBJECT |
| `FATIGUE.MEASURING_AMPLIFIER` | Messverstärker / Measuring amplifier | OBJECT |
| `FATIGUE.SAMPLING_FREQUENCY` | Abtastfrequenz [Hz] / Sampling frequency [Hz] | INTEGER |
| `FATIGUE.RECORDING_MODE` | Aufzeichnungsmodus / Recording mode | CONTROLLEDVOCABULARY |
| `FATIGUE.RECORDED_CHANNELS` | Erfasste Kanäle / Recorded channels | VARCHAR |
| `FATIGUE.PRELOAD_FORCE` | Vorspannkraft [kN] / Preload force [kN] | REAL |
| `FATIGUE.BEACH_MARKS_ACTIVE` | Rastlinien (Markerlasten) aktiv / Beach marks (marker loads) active | BOOLEAN |
| `FATIGUE.TERMINATION_REASON` | Abbruchgrund / Termination reason | CONTROLLEDVOCABULARY |
| `FATIGUE.CYCLES_GROSS` | Bruttoschwingspielzahl / Gross number of cycles | INTEGER |
| `FATIGUE.CYCLES_NET` | Nettoschwingspielzahl / Net number of cycles | INTEGER |
| `FATIGUE.CYCLES_TO_10_PERCENT_STRAIN_GAUGE_DROP` | Zyklen bis 10 % DMS-Abfall je DMS / Cycles to 10 % strain gauge drop per strain gauge | MULTILINE_VARCHAR |
| `FATIGUE.NEXT_STEP` | Nächster Schritt / Next step | CONTROLLEDVOCABULARY |
| `FATIGUE.MANUFACTURER_DESIGNATION` | Herstellerbezeichnung (Original-ID) / Manufacturer designation (original ID) | VARCHAR |
| `FATIGUE.SOURCE_SHEET` | Herkunftsblech / Source sheet | VARCHAR |
| `FATIGUE.TARGET_QUALITY_LEVEL` | Angestrebte Bewertungsgruppe (ISO 5817) / Target quality level (ISO 5817) | CONTROLLEDVOCABULARY |
| `FATIGUE.INITIAL_ANGULAR_DISTORTION` | Winkelverzug initial [°] / Initial angular distortion [°] | REAL |
| `FATIGUE.INITIAL_EDGE_MISALIGNMENT` | Kantenversatz initial [mm] / Initial edge misalignment [mm] | REAL |
| `FATIGUE.WAS_STRAIGHTENED` | Wurde gerichtet / Was straightened | BOOLEAN |
| `FATIGUE.ANGULAR_DISTORTION_AFTER_STRAIGHTENING` | Winkelverzug nach dem Richten [°] / Angular distortion after straightening [°] | REAL |
| `FATIGUE.EDGE_MISALIGNMENT_AFTER_STRAIGHTENING` | Kantenversatz nach dem Richten [mm] / Edge misalignment after straightening [mm] | REAL |
| `FATIGUE.WELD_POST_TREATMENT_NOTES` | Nahtüberhöhungs-Bearbeitung / Schleifhinweise / Weld reinforcement treatment / grinding notes | MULTILINE_VARCHAR |
| `FATIGUE.ISO_5817_ANNEX_C_RATING` | Bewertungsgruppe ISO 5817 Anhang C / Quality level ISO 5817 Annex C | CONTROLLEDVOCABULARY |
| `FATIGUE.LOAD_LEVEL` | Lastniveau / Load level | CONTROLLEDVOCABULARY |
| `FATIGUE.TEST_ORDER` | Prüfreihenfolge / Test order | INTEGER |
| `FATIGUE.THICKNESS_POS_1` | Dicke Position 1 [mm] / Thickness position 1 [mm] | REAL |
| `FATIGUE.THICKNESS_POS_2` | Dicke Position 2 [mm] / Thickness position 2 [mm] | REAL |
| `FATIGUE.THICKNESS_POS_3` | Dicke Position 3 [mm] / Thickness position 3 [mm] | REAL |
| `FATIGUE.WIDTH_POS_1` | Breite Position 1 [mm] / Width position 1 [mm] | REAL |
| `FATIGUE.WIDTH_POS_2` | Breite Position 2 [mm] / Width position 2 [mm] | REAL |
| `FATIGUE.WIDTH_POS_3` | Breite Position 3 [mm] / Width position 3 [mm] | REAL |
| `FATIGUE.MEAN_THICKNESS` | Mittlere Dicke [mm] / Mean thickness [mm] | REAL |
| `FATIGUE.MEAN_WIDTH` | Mittlere Breite [mm] / Mean width [mm] | REAL |

Dateien zum Senden / files to send: `request/issue.md`, `request/mail.txt`, `request/masterdata.xlsx`.

## Ihre Antwort / Your reply

Schreiben Sie im Chat „C freigegeben“ oder eine Liste der Änderungen, je Teil eine Zeile. / Write “C approved” in the chat, or a list of changes, one line per part.

Teile / Parts: neue Typen · neue Felder · Auswahllisten · Wiederverwendung

Nach dem Senden / after sending: „D gesendet: <Link des Issues>“.

