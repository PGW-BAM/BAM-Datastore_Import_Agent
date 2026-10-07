# Aufräumen Altbestand auf dev1 (FB 7.2) – Checkliste

Stand 06.10.2026. **Bereits erledigt (wiederherstellbar):** 197 Alt-Objekte und 2 Alt-Collections wurden in den
openBIS-Papierkorb verschoben (Papierkorb-Einträge 7 und 8, Grund „Legacy FB 7.2 model (12-step chain) replaced by flat
structure /FB_72/WELDED_FATIGUE …“).

Die folgenden Schritte sind **unwiderruflich** und werden bewusst nicht von einem Agenten ausgeführt.
Reihenfolge einhalten – openBIS lässt Typen erst löschen, wenn kein Objekt (auch nicht im Papierkorb) sie nutzt.

## 1. Papierkorb leeren (ELN → Utilities/Trashcan, oder Admin-UI)
- [ ] Eintrag 7 (197 Objekte) endgültig löschen
- [ ] Eintrag 8 (Collections `SERIE_1_BUTT_WELD`, `SERIE_1_CRUCIFORM_WELD`) endgültig löschen
- [ ] Einträge 1, 2, 4, 6 stammen nicht aus diesem Lauf – nur nach Prüfung löschen

## 2. Leere Projekte löschen (Admin-UI)
- [ ] `/FB_72/CYCLIC_FATIGUE_TESTS`
- [ ] `/FB_72/CATALOG`

## 3. Alt-Masterdaten löschen (Admin-UI → Types)
Ersatz siehe `gap-report.md` → Abschnitt LIVE-ONLY.
- [ ] Objekttypen (16): `TEST_SPECIMEN`, `PRE_QUALITY_CHECK`, `CHAMFERING_GRINDING`, `SPECIMEN_RECORDING`, `WELD_ANALYSIS`,
      `SERIES_ASSIGNMENT`, `TEST_SETUP_GEOMETRY`, `MONITORING_APPLICATION`, `AMPLIFIER_TEST_BENCH_SETTINGS`,
      `INSTALLATION_STRESS_MEASUREMENT`, `CYCLIC_FATIGUE_TEST`, `DATA_EVALUATION`, `FRACTURE_SURFACE_ANALYSIS`,
      `STRAIN_GAUGE_TYPE`, `CONSUMABLE_TYPE`, `INSTRUMENT_DUMMY`
- [ ] Collection-Typ: `TEST_SERIES`
- [ ] Dataset-Typen (17): `REWORK_PROTOCOL`, `SPECIMEN_PHOTOS`, `3D_SCAN_RAW`, `WELD_ANALYSIS_EVAL`, `RANDOMIZATION_CODE`,
      `STRAIN_GAUGE_POSITION_DRAWING`, `SETUP_PHOTO`, `BENDING_MOMENT_RAW`, `RAW_CONVERSION_SCRIPT`, `LOAD_PROGRAM_EXCEL`,
      `FATIGUE_MESS_RAW`, `MONITORING_IMAGES`, `EVALUATION_PLOTS`, `CLEANED_DATA_TABULAR`, `MACRO_FRACTURE_PHOTOS`,
      `MICROSCOPE_CRACK_IMAGES`, `BEACH_MARK_EVALUATION_EXCEL`
- [ ] Vokabulare (6): `WELD_GEOMETRY`, `ISO_5817_CLASS`, `WELD_ANALYSIS_RATING`, `STOP_REASON`, `DATA_RECORDING_MODE`, `STEP_STATUS`
- [ ] Danach verwaiste Property-Typen der Alt-Typen (z. B. `WELD_GEOMETRY_PROP`, `STOP_REASON_PROP`, `STEP_ORDER`, `STATUS`,
      `SPECIMEN_THICKNESS_POS_1_3` …). **Nicht** löschen: `OPERATOR` (wird vom Standard genutzt) – nur das Label
      „Operator / Ausführende Person“ auf „Operator“ zurücksetzen.

## 4. Kontrolle
- [ ] `/FB_72/WELDED_FATIGUE` unverändert: 1 Protokoll, 8 Proben, 10 Schritte; Inventar in `/MATERIALS/7_2_*` vorhanden
- [ ] Live-Inventur erneut laufen lassen (`/bam-analyze-prd …` Schritt 3) → LIVE-ONLY sollte leer sein
