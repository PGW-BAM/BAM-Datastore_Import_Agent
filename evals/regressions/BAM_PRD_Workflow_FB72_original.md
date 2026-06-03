# Product Requirements Document (PRD): Automated openBIS Masterdata Extension (Workflow FB 7.2)

## 1. Kontext & Zielsetzung
**Ziel:** Generierung von Python-Code zur Erweiterung des zentralen BAM-Datenmodells (`bam-masterdata`) für den Prüfstand-Workflow des Fachbereichs 7.2 (Zyklische Ermüdungsprüfungen / Wöhlerlinien).
**Rolle des Agenten:** Agiere als Experte für das BAM-openBIS-Masterdata-Framework. Erzeuge sauberen, deklarativen, klassenbasierten Python-Code, der direkt über einen Pull Request in das bestehende Repository integriert werden kann.
**Sprachvorgabe:** Alle Labels, Beschreibungen (`description`) und Sektionen MÜSSEN strikt im BAM-zweisprachigen Format `"English//Deutsch"` (getrennt durch ein doppeltes Slash ohne Leerzeichen) ausgeführt werden.

## 2. Globale Entwicklungs-Richtlinien & Framework-Constraints
Der Coding-Agent muss sich strikt an die Architekturprinzipien des `bam-masterdata`-Repositories halten:
1. **Kein roher pyBIS-Code:** Es dürfen keine imperativen API-Aufrufe (wie `o.create_sample_type()`) generiert werden. Alle Definitionen erfolgen deklarativ über Python-Klassen, die von `ObjectType`, `ExperimentalStep` oder `VocabularyTypeAssignment` erben.
2. **Wiederverwendung vor Neukonstruktion (Reuse Policy):** Vor der Erstellung eines neuen Objekttyps muss geprüft werden, ob die BAM-Basisstruktur dies bereits abdeckt:
   * Für Prüfstände/Maschinen ist zwingend die existierende Klasse `TestingMachine` (`TESTING_MACHINE`) zu nutzen.
   * Für Laborgeräte (Kameras, Mikroskope, 3D-Scanner) ist die existierende Klasse `Instrument` (`INSTRUMENT`) zu nutzen.
3. **Schlanke Datenhaltung (Lean Property Rule):** Komplexe mathematische Matrizen (z. B. das Lastprogramm oder die tabellarische Auswertung der Rastlinien) werden **nicht** als diskrete Property-Felder angelegt. Diese werden stattdessen als Datei-Uploads (Excel/CSV) behandelt. Die Klassen enthalten hierfür lediglich beschreibende Metadaten.
4. **Strukturierung:** Jedes `PropertyTypeAssignment` muss ein klares `property_label`, eine zweisprachige `description` sowie eine organisatorische `section` (für die openBIS-Benutzeroberfläche) enthalten.

## 3. Datenmodell & Architektur-Spezifikation

### Phase 1: Kontrollierte Vokabulare (VocabularyTypeAssignment)
Erstelle die folgenden neuen Vokabulare, falls diese im BAM-Standard noch nicht existieren:
* **`WELD_GEOMETRY`**
  * Terms: `BUTT_WELD` ("Butt weld//Stumpfstoß"), `CRUCIFORM_WELD` ("Cruciform weld//Kreuzstoß")
* **`ISO_5817_FAT_CLASS`** (Spezifisch für HCF-Relevanz / IIW FAT-Klassen)
  * Terms: `C56` ("FAT Class C56//FAT Klasse C56"), `B90` ("FAT Class B90//FAT Klasse B90"), `B125` ("FAT Class B125//FAT Klasse B125")
* **`LOAD_LEVEL`** (Für die Lastniveaus der Wöhlerlinie)
  * Terms: `HIGH` ("High Load//Hohes Lastniveau"), `MEDIUM` ("Medium Load//Mittleres Lastniveau"), `LOW` ("Low Load//Niedriges Lastniveau")
* **`FATIGUE_STOP_REASON`**
  * Terms: `FRACTURE` ("Total Fracture//Totalbruch"), `RUN_OUT` ("Target Cycles Reached (Run Out)//Zyklenzahl erreicht (Durchläufer)"), `CRACK` ("Crack Detected//Riss detektiert")

### Phase 2: Haupt-Probentyp (ObjectType)
Erstelle einen spezifischen Probentyp für geschweißte Ermüdungsproben, der von `ObjectType` erbt:
* **Klassenname:** `WeldedFatigueSpecimen`
* **Code:** `SPECIMEN.WELDED_FATIGUE` (Prefix: `SPEC.WELD`)
* **Properties & Zuordnungen:**
  * `original_id` (VARCHAR, Section: "Material Details"): Originalbezeichnung des Herstellers.
  * `sheet_origin` (VARCHAR, Section: "Material Details"): Herkunftsblech der Probe (wichtig zur Vermeidung von Bias bei der Serienzuordnung).
  * `weld_geometry` (CONTROLLEDVOCABULARY `WELD_GEOMETRY`, Section: "Weld Details", Mandatory=True)
  * `iso_fat_class` (CONTROLLEDVOCABULARY `ISO_5817_FAT_CLASS`, Section: "Weld Details"): FAT-Klasse (C56, B90, B125).
  * `load_level` (CONTROLLEDVOCABULARY `LOAD_LEVEL`, Section: "Test Planning"): Zugeordnetes Lastniveau für die Wöhlerlinie.

### Phase 3: Prozessschritte (ExperimentalStep)
Erstelle die folgenden Prozessschritte als Klassen, die von `ExperimentalStep` erben. Verwende für alle das `generated_code_prefix="EXP.[KURZNAME]"`:

1. **`PreQualityCheckWeld`** (`EXPERIMENTAL_STEP.PRE_QUALITY_CHECK_WELD`):
   * *Properties:* `initial_angular_distortion` (REAL, Winkelverzug [°]), `initial_edge_misalignment` (REAL, Kantenversatz [mm]), `was_straightened` (BOOLEAN, Wurde gerichtet?).
2. **`ChamferingGrinding`** (`EXPERIMENTAL_STEP.CHAMFERING_GRINDING`):
   * *Properties:* `weld_modifications` (MULTILINE_VARCHAR, Dokumentation gezielter Schweißnahtverstärkungen oder Schleifhinweise).
3. **`SpecimenRecording`** (`EXPERIMENTAL_STEP.SPECIMEN_RECORDING`):
   * *Properties:* Verknüpfung zum GOM-Scanner via BAM-Standard `Instrument`.
4. **`WeldAnalysis`** (`EXPERIMENTAL_STEP.WELD_ANALYSIS`):
   * *Properties:* Verknüpfung der Probe mit der ermittelten `ISO_5817_FAT_CLASS` (Dropdown C56, B90, B125).
5. **`SeriesAssignment`** (`EXPERIMENTAL_STEP.SERIES_ASSIGNMENT`):
   * *Beschreibung:* Dokumentiert die zeitliche Randomisierung und Zuteilung zur Prüfserie (Collection).
6. **`TestSetupGeometry`** (`EXPERIMENTAL_STEP.TEST_SETUP_GEOMETRY`):
   * *Properties:* `avg_thickness` (REAL, Durchschnittliche Proben-Dicke [mm]), `avg_width` (REAL, Durchschnittliche Proben-Breite [mm]) basierend auf den Messschieber-Messungen.
7. **`MonitoringApplication`** (`EXPERIMENTAL_STEP.MONITORING_APPLICATION`):
   * *Properties:* Objekt-Links (`data_type="OBJECT"`) zu den verwendeten BAM-Katalogen für DMS-Typen (`STRAIN_GAUGE_TYPE`) und Verbrauchsmaterialien (`CONSUMABLE_TYPE`), sowie die finalen reellen Abstände (`measured_dms_distance_weld`, `measured_dms_distance_edge`).
8. **`AmplifierSettings`** (`EXPERIMENTAL_STEP.AMPLIFIER_SETTINGS`):
   * *Properties:* `sampling_frequency` (INTEGER), `recording_mode` (VARCHAR/ControlledVocabulary für Peak-Valley etc.). Verknüpfung zur Prüfmaschine (`TestingMachine`) und dem IMC-Messverstärker (`Instrument`).
9. **`InstallationStressMeasurement`** (`EXPERIMENTAL_STEP.INSTALLATION_STRESS_MEASUREMENT`):
   * *Beschreibung:* Erfassung des Biegemoments bei 0.0 kN vor Versuchsstart (Einbaubeanspruchung).
10. **`CyclicFatigueTest`** (`EXPERIMENTAL_STEP.CYCLIC_FATIGUE_TEST`):
    * *Properties:* `marker_loads_active` (BOOLEAN, Rastlinien aktiv?), `stop_reason` (CONTROLLEDVOCABULARY `FATIGUE_STOP_REASON`). 
    * *Hinweis:* Keine dedizierten Lastfelder. Das Lastprogramm wird als Excel-Datei an diesen Schritt angehängt.
11. **`FatigueDataEvaluation`** (`EXPERIMENTAL_STEP.FATIGUE_DATA_EVALUATION`):
    * *Properties:* `cycles_gross_final` (INTEGER), `cycles_net_final` (INTEGER), `cycles_dms_deviation_10` (MULTILINE_VARCHAR, Zyklen bis 10% Abfall je DMS).
12. **`FractureSurfaceAnalysis`** (`EXPERIMENTAL_STEP.FRACTURE_SURFACE_ANALYSIS`):
    * *Beschreibung:* Lichtmikroskopische und makroskopische Auswertung der Bruchfläche. Verknüpfung zu Kamera und Digitalmikroskop über das BAM-Standard `Instrument`.

## 4. Ausgabe-Anforderung an den Agenten
Generiere den vollständigen Python-Code aufgeteilt in logische Blöcke (entsprechend der Struktur im `bam_masterdata/datamodel` Ordner). Kommentiere den Code ausführlich, sodass ersichtlich ist, welche Klassen neu hinzukommen und an welchen Stellen bestehende BAM-Klassen referenziert werden.
