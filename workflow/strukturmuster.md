# Strukturmuster für Abläufe mit vielen Schritten

Grundlage für Schritt 4 (`04_struktur.md`). Gilt für jeden Agenten. Stand der Recherche: 2026-11-04 (Quellen unten).
Es gibt **keine Vorgabe „möglichst flach“** mehr. Ziel ist eine Struktur, die man in openBIS **übersichtlich lesen**
kann: im Hierarchie-Graphen einer Probe, in der Tabelle einer Serie und im Formular eines Schritts.

## Warum Graphen unübersichtlich werden

In openBIS gibt es zwei Arten, Objekte zu verbinden:

| Verbindung | wird angezeigt | typisch für |
|---|---|---|
| **Eltern/Kind** (`parents`/`children`) | im Hierarchie-Graphen und in der Hierarchie-Tabelle | Herkunft und Reihenfolge: „ist entstanden aus“, „folgt auf“ |
| **Feld vom Typ OBJECT** (in openBIS „Sample“-Property) | als Link im Formular, **nicht** im Graphen; Typ des Ziels wird geprüft | Bezüge: „wurde benutzt“ (Gerät, Hilfsstoff, Protokoll, Person) |

Unübersichtlich wird ein Graph vor allem durch **Knoten mit vielen Verbindungen**, weniger durch Tiefe:

1. **Geteilte Inventar-Objekte als Eltern.** Prüfmaschine, Kamera, Klebstoff hängen als Eltern an den Schritten *aller*
   Proben. Jeder Graph enthält diese Knoten, und über sie sind alle Proben miteinander verbunden.
2. **Sterne.** Viele Schritte direkt an der Probe zeigen nicht, in welcher Reihenfolge sie stattfanden.
3. **Lange Ketten aus Einzelschritten.** Zwölf Objekte hintereinander sind lesbar, aber lang (Modell auf dev1).

Eine Kette, in der jeder Knoten genau einen Vorgänger und einen Nachfolger hat, ist dagegen leicht zu lesen, auch wenn
sie tief ist.

## Muster

| # | Muster | So sieht es aus | Gut, wenn … | Nachteil | Quelle |
|---|---|---|---|---|---|
| M1 | **Prozesslinie** | Probe → Schritt → Schritt → … (Eltern/Kind) | die Reihenfolge wichtig ist und jeder Schritt auf dem vorigen aufbaut | jeder Knoten mehr verlängert den Weg zurück zur Probe | openBIS-Doku: Schritte können miteinander verknüpft werden („chaining steps“) [1][2] |
| M2 | **Probe als Mittelpunkt** | Probe mit allen Schritten als Kindern | Schritte unabhängig voneinander sind (Messungen an derselben Probe) | Reihenfolge nicht sichtbar, Stern bei vielen Schritten | openBIS-Doku: Probe ist Elternteil des Schritts [1] |
| M3 | **Zustände des Materials** | Blech → (Schweißen) → Probe → (Versuch) → Bruchstücke | das Material sich ändert, geteilt oder weiterverarbeitet wird | nur sinnvoll, wo wirklich neue Proben entstehen | W3C PROV: Entität → Aktivität → Entität [3]; CRC 1394: Lebenslauf der Probe über Eltern/Kind [4]; BAM Data Store Days: Ablauf als gerichteter Graph [5] |
| M4 | **Bezüge als Felder** | Gerät, Hilfsstoff, Protokoll als OBJECT-Feld im Schritt | viele geteilte Inventar-Objekte vorkommen | im Graphen unsichtbar; „wo wurde Gerät X benutzt?“ nur über die Suche | **BAM-Standard:** `CREEP_TEST` verlinkt Prüfmaschine, Sensoren, Probe so (`bam_masterdata/datamodel/v0/creep_test/object_types.py:14`); openBIS-Forum: OBJECT-Felder prüfen Typ und Anzahl, erscheinen nicht im Graphen [6][7] |
| M5 | **Schritte bündeln** | mehrere Ablaufschritte am selben Arbeitsplatz = ein Objekt, je Schritt eine Sektion | Gerät, Zeitraum, Person und Dateien zusammengehören | einzelne Schritte haben kein eigenes Objekt | BAM Data Store Days: „so knapp wie möglich, so reproduzierbar wie nötig“ [5] |
| M6 | **Übersicht in Tabellen** | Collection-Tabelle je Serie (Spalten = wichtigste Felder); Hierarchie-Tabelle | man viele Proben vergleicht | ersetzt nicht den Weg einer einzelnen Probe | openBIS-Doku: Objekte in Collections, weil sie eine Tabelle geben [8]; Graph und Tabelle lassen sich nach Ebenen und Typen filtern [9] |
| M7 | **Protokoll als Vorlage** | SOP/Protokoll im Inventar, Schritt daraus angelegt | ein Ablauf oft gleich wiederholt wird | ein weiterer geteilter Knoten, wenn als Elternteil verlinkt (dann besser M4) | openBIS-Doku: Protokolle als Eltern bzw. Vorlage von Schritten [1][2] |

Die Muster lassen sich kombinieren. Häufig gut lesbar: **M1 + M4 + M5 + M6** – eine kurze Prozesslinie aus
gebündelten Schritten, Geräte und Hilfsstoffe als Felder, die Serie als Tabelle. M3 kommt dazu, wo aus einer Probe neue
Proben entstehen (Zuschnitt, Bruchstücke, Schliffe).

## Entscheidungshilfe

1. **Wie wird es später gelesen?** Den Weg *einer* Probe verfolgen → M1/M3. *Viele* Proben vergleichen → M6.
   Beides ist fast immer nötig.
2. **Eltern/Kind nur für Herkunft und Reihenfolge.** „Ist entstanden aus“ und „folgt auf“ sind Eltern/Kind.
   „Wurde benutzt“ ist ein Feld (M4), außer die Person will ausdrücklich im Graphen sehen, welche Proben ein Gerät hatte.
3. **Wenige Knoten pro Probe.** Schritte bündeln, wo Gerät, Zeitraum, Person und Dateien zusammengehören (M5).
4. **Keine Knoten mit vielen Verbindungen im Graphen einer Probe.** Geteilte Inventar-Objekte nicht als Eltern, wenn es mehr
   als ein, zwei sind.
5. **Tiefe ist erlaubt**, wenn sie eine Linie ist. Abzweigungen nur, wo der Ablauf sich wirklich verzweigt.
6. **Standard zuerst** (Regel 7): Gibt es im Standard schon OBJECT-Felder oder Typen für die Bezüge, diese nehmen.
7. **PRD-Entscheidungen gelten.** Steht im PRD etwas anderes (z. B. „Geräte als Eltern“), ist eine abweichende Variante
   ein Vorschlag und braucht die Zustimmung der Person (Nachteil in der Variante nennen).

## Was der Agent daraus macht

- Für jedes Projekt 2–4 Varianten aus diesen Mustern bilden (`design.json` → `variants`), eine empfehlen und die
  verwendeten Muster in der Kurzbeschreibung nennen („Prozesslinie, Geräte als Felder (M1, M4, M5)“).
- Zu jeder Variante angeben, wie der Graph einer Probe aussieht (Objekte je Probe, Ebenen, geteilte Knoten).
- Ein bisheriges Modell (falls vorhanden) als Vergleich zeigen.

## Quellen

Erreichbar aus der Cloud war nur `bamresearch.github.io`; die übrigen Seiten wurden über die Websuche ausgewertet und
sollten bei Bedarf im BAM-Netz gegengelesen werden.

1. openBIS Data Modelling (protocol, sample, equipment als Eltern eines Schritts; Schritte nacheinander verknüpfen):
   https://openbis.readthedocs.io/en/latest/user-documentation/advance-features/openbis-data-modelling.html
2. openBIS General Overview / Lab Notebook (Schritte untereinander und mit Inventar verknüpfen; Protokolle als Vorlage):
   https://openbis.readthedocs.io/en/latest/user-documentation/general-users/general-overview.html,
   https://openbis.readthedocs.io/en/7.x/user-documentation/general-users/lab-notebook.html
3. W3C PROV über ELIXIR RDMkit „Data provenance“: https://rdmkit.elixir-europe.org/data_provenance
4. Rejiba et al., „Towards Defect Phase Diagrams: From Research Data Management to Automated Workflows“, Adv. Eng. Mater.
   (2025), arXiv:2511.01942: https://arxiv.org/abs/2511.01942
5. BAM Data Store Days 2025, Block I (Ablauf als gerichteter Graph; „as minimal as possible while keeping reproducibility
   maximized“): https://bamresearch.github.io/datastoredays25-group2/block_1
6. openBIS-Forum, „OBJECT properties not displayed in the hierarchical graph“:
   https://community.openbis.ch/t/object-properties-not-displayed-in-the-hierarchical-graph/669
7. openBIS-Forum, „Make object property a link“ (20.10.7.2):
   https://community.openbis.ch/t/version-20-10-7-2-how-does-make-object-property-a-link-work/258
8. openBIS Data Modelling 20.10 (Objekte in Collections für die Tabellenansicht):
   https://unlimited.ethz.ch/display/openBISDoc2010/openBIS+Data+Modelling
9. openBIS „Visualise relationships“ (Graph nach Ebenen und Typen kürzen; Hierarchie-Tabelle):
   https://openbis.ch/index.php/docs/user-documentation-before19-06-4/additional-functionalities/visualise-relationships/
10. Empa „Tips for Experiments“ (Eltern/Kind in Experimental Steps, Hierarchie-Graph):
    https://scientificit.empa.ch/documentation/openbis/getting-started/users/experiments/
11. Plass et al., „Using OpenBIS as Virtual Research Environment“, Data Science Journal 22 (2023) 44:
    https://datascience.codata.org/articles/10.5334/dsj-2023-044
12. BAM pyBIS Workshop, Teil 2 (Eltern/Kind zwischen Schritten anlegen):
    https://bamresearch.github.io/bam-pybis-workshop/part2-advanced_features/
