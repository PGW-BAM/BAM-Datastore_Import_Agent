# Befunde & Entscheidungen (Lauf vom 06.10.2026)

Was die Pipeline beim Neu-Durchlauf gefunden hat, wer was entschieden hat und wo es belegt ist.
Grundlage für Folie 9 und für Rückfragen im Vortrag.

## 1. Befunde der Agenten / Skripte

| # | Befund | Auswirkung | Behoben durch | Beleg |
|---|---|---|---|---|
| B1 | Katalog v1 fand nur **direkte** Unterklassen (`grep class X(ObjectType)`) | 8 vorhandene Gerätetypen (Kamera, Messverstärker, …) als „UNCONFIRMED“ markiert; Gefahr von Doppelanlage | `tools/build_catalog.py` (AST, volle Vererbung, byte-identisch reproduzierbar) | `generated/CATALOG.md` |
| B2 | Generierter Code v1 nutzte `VocabularyTypeAssignment` (existiert nicht) und falschen Import für `ExperimentalStep` | Code war **nie importierbar**; Selbstprüfung prüfte nur Syntax | Extender-Vorlage korrigiert, Pflicht-Importtest gegen das echte Paket | `.claude/agents/masterdata-extender.md` |
| B3 | PRD v1 verlangte zweisprachige Labels/Sektionen | Widerspruch zum Standard (0 von 1 786 Sektionen zweisprachig) | PRD v2 Prinzip P8: Beschreibungen `EN//DE`, Labels/Sektionen englisch | `BAM_PRD_Workflow_FB72_v2.md` |
| B4 | `bam-masterdata` 33 Commits weiter (u. a. `Sample`, `MechanicalTest`, Kriechversuch-Modul, `instruments.py`) | Gap-Report v1 veraltet, Zeilennummern falsch | Fast-Forward + neuer Katalog @ `d7a871b` | `generated/catalog.json` |
| B5 | Auf dev1 existierte ein eigenes FB-7.2-Modell (16 Typen, 6 Vokabulare, 17 Dateitypen) | Fachlich reich, aber 12er-Kette, keine Namensräume, `"EN / DE"`, kein `$NAME` | Klasse **LIVE-ONLY** im Gap-Analyzer, alles migriert | `generated/live/dev1_inventory.md` |
| B6 | dev1 ist gegenüber dem Standard veraltet (BAM-Standort-Vokabulare fehlen; `DESCRIPTION` einzeilig) | 6 geerbte Felder können nicht zugewiesen werden | Apply-Skript überspringt & meldet statt zu raten | Ausgabe `openbis_apply.js` |
| B7 | dev1 verlangt Pflichtfelder (Hersteller, Maximallasten, E-Akte beim SOP) | Erste Anlage scheiterte transaktional (nichts halb angelegt) | Pflichtfelder vorab abgefragt; Ablaufplan als `GENERAL_PROTOCOL` statt `SOP` | `tools/openbis_demo.js` |
| B8 | Code-Kollision: `LUXONIS_OAK_4D_PRO` war ein Alt-Dummy | Neue Versuche hätten auf ein Objekt im Papierkorb gezeigt | Trockenlauf hat es gezeigt → eigener Code `…_CAM` | Trockenlauf-Ausgabe |
| B10 | `bam-masterdata` (`CollectionType.add`) verlangt Pflichtfelder auch beim reinen **Aktualisieren** vorhandener Objekte | Parser muss `$NAME`/`BAM_OE` der Probe mitsenden; auf dev1 (ohne `BAM_OE`) „Next step“ vorerst manuell | Parser-Option `update_specimen=False`; Upstream-Issue vorschlagen | `generated/welded_fatigue_v2/parsers/README.md` |
| B9 | Messwerte „an 3 Positionen“ lagen live in **einem** REAL-Feld | Nicht abbildbar / nicht auswertbar | je Position ein Feld + Mittelwert | `design.md` §3.1 |

## 2. Entscheidungen

| Entscheidung | Von | Begründung |
|---|---|---|
| Flache Struktur: Probe + SCAN/TEST/FRACTURE, Tiefe 1 | Fachbereich (Rückfrage) | Ablauf sichtbar über Sektionsnummern + „Next step“; 4 statt 13 Objekte |
| Stumpf-/Kreuzstoß als Erweiterung von `WELDING.WELD_TYPE` | Fachbereich | Hinweis Agent: fachlich eher Stoßart → im PR mit Schweiß-Gruppe abstimmen |
| ISO 5817 Anhang C: **C63**, B90, B125 (nicht C56) | Fachbereich | Korrektur gegenüber Altmodell |
| Zwei ISO-5817-Listen (B/C/D und C63/B90/B125) | Agent | verschiedene Wertebereiche, sonst ungültige Kombinationen |
| Codes `S1B-NN` / `S1C-NN` mit führender Null | Agent/Koordination | eindeutig je Serie, korrekte Sortierung (Altbestand: S1-1, S1-10, S1-2 …) |
| Neue Property-Codes im Namensraum `FATIGUE.` | Agent | keine Kollision mit Alt-Codes anderen Datentyps |
| Wiederverwendung `EXPERIMENTAL_STEP.WELDMENT_TYPE`, `DEFECT_DESCRIPTION`, `ALIAS`, `$NAME` | Agent | Reuse-first; verbindet Probe mit Schweißprozess-Daten |
| Altbestand → Papierkorb (nicht endgültig gelöscht) | Fachbereich + Sicherheitsregel | endgültiges Löschen ist unwiderruflich → Admin / Fachbereich |

## 3. Offene Punkte

1. **PR an `bam-masterdata`**: `generated/welded_fatigue_v2/datamodel/README.md` (2 Typen, 6 Vokabulare, 4 Terme). Abstimmung mit Schweiß-Gruppe (WELD_TYPE) und FB 5.x (`MechanicalTest`).
2. **dev1 mit Standard synchronisieren** (Admin): BAM-Standort-Vokabulare, `DESCRIPTION` mehrzeilig, `MECHANICAL_TEST`.
3. **Aufräumen** (unwiderruflich, Fachbereich/Admin): `generated/welded_fatigue_v2/CLEANUP_dev1.md`.
4. Kosmetik in der ELN: Typ-Anzeigenamen („Sample.welded Fatigue Specimen“) und das Alt-Label „Operator / Ausführende Person“ über ELN-Einstellungen bzw. nach dem Aufräumen anpassen.
5. Upstream-Issue an `bam-masterdata`: Pflichtfeld-Prüfung beim Update vorhandener Objekte (Code gesetzt) überspringen (B10).
6. Notebook `notebooks/welded_fatigue_v2_provisioning.ipynb` ist syntaktisch geprüft, aber **noch nicht gegen openBIS ausgeführt** (braucht euren Token).
7. Bisher nicht erfasst (nicht im PRD v2): Bearbeiter*in / Datum für die Probenschritte 01–06 – bei Bedarf als Felder ergänzen.
