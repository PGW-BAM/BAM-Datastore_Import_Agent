# Schritt 6: Antrag an den Admin

**Ziel:** Ein fertiges, geprüftes Paket, das der Admin ohne Rückfragen bearbeiten kann. Der offizielle Weg laut
bam-masterdata (https://bamresearch.github.io/bam-masterdata/howtos/extend_masterdata/): erst ein Issue, dann
ein PR auf den Zweig `dev` oder eine `masterdata.xlsx` am Issue.

| | |
|---|---|
| Eingabe | `gap-report.md` (freigegeben, ◆ C), `design.json`, `requirements.json` |
| Ausgabe | `datamodel/*.py`, `datamodel/extend.json`, `spec.json`, `request/issue.md`, `request/mail.txt`, `request/masterdata.xlsx`, `request/checker.log` |
| Zugang | keiner (Agent); Admin danach |
| Prüfpunkt | ◆ **D**: die Person sendet |

Nur nötig, wenn es NEU, ERWEITERN oder NACHZIEHEN gibt. Gibt es nur GERÄT FEHLT, weiter mit Schritt 8.

## Tun

1. **Klassen für NEU** in `datamodel/object_types.py` und `datamodel/vocabularies.py`. Basisklassen aus v0
   importieren, z. B. `from bam_masterdata.datamodel.v0.object_types import Sample`. Vorlage und Regeln: Agent
   `.claude/agents/masterdata-extender.md`, Beispiel `generated/welded_fatigue_v2/datamodel/`.
2. **ERWEITERN** als `datamodel/extend.json` (Vokabular, Beleg, neue Begriffe).
3. **Import-Test und Soll-Zustand:** `python tools/export_spec.py projects/<name>/datamodel > projects/<name>/spec.json`
4. **Antragspaket bauen** (Excel, checker, Issue-Text, Mail, `request.json`):
   ```bash
   python tools/build_request.py <name>        # -> projects/<name>/request/
   ```
   Ziel des checker: 0 Fehler. Warnungen entweder beheben (z. B. Sektionen in Title Case ohne Ziffern) oder im Issue
   erklären. Bekannte Warnungen aus dem Standard selbst: `$ANNOTATIONS_STATE is deprecated`, `EXPERIMENTAL_STEP.MECHANICAL_TEST
   has the same properties as EXPERIMENTAL_STEP`. `issue.md` und `mail.txt` sind Entwürfe: Begründungen aus dem PRD
   schärfen, Mapping-Notizen (BFO/IAO) ergänzen, falls möglich. Vorlagen: `templates/request/`. In `project.yaml`
   gehören dafür `title`, `title_en`, `division` und `summary_en`.
5. **Prüfseite** erzeugen und zeigen:
   ```bash
   python tools/render_review.py <name> antrag    # -> projects/<name>/review/antrag.html
   ```
   Sie fasst den Antrag in einfacher Sprache zusammen (neue Typen, Felder, Listen, was nur nachgezogen wird, was
   wiederverwendet wird, checker), mit „passt / ändern“ je Teil. Erst wenn alles passt, öffnet sich dort der Teil
   „Antrag senden“ mit Titel, Issue-Text, Betreff und Mail zum Kopieren und einem Link auf ein neues Issue.
6. `STATUS.md`: Schritt 6 „wartet auf C“, nach Freigabe „wartet auf D“; `AUFGABE.md` verweist auf die Prüfseite.

## Prüfen

- [ ] Import-Test grün (`export_spec.py` läuft durch)
- [ ] checker: 0 Fehler, jede Warnung behoben oder erklärt
- [ ] Jede Zeile im Issue hat eine Begründung aus dem PRD
- [ ] Beschreibungen `English//Deutsch`, Sektionen Title Case ohne Ziffern, `mandatory`/`section` gesetzt
- [ ] Jede neue Property hat `property_label_de`, jeder neue Begriff `label_de` (in openBIS dann „English//Deutsch“)
- [ ] Der Antrag ist so kurz wie möglich (nichts, was NUTZEN wäre)

## Stopp

◆ **C**: Die Person prüft die Prüfseite und gibt frei („C freigegeben“ / „C approved“) oder nennt Änderungen.

◆ **D**, Mensch (Teil „Antrag senden“ der Prüfseite):
1. Issue in https://github.com/BAMresearch/bam-masterdata/issues anlegen (Text aus `issue.md`, `masterdata.xlsx` anhängen).
   Optional selbst einen PR: Fork, Branch `<issue-nr>-<thema>`, Ziel `dev`.
2. Issue-Link in `mail.txt` eintragen und an datastore@bam.de senden.
3. Im Chat melden: „D gesendet“ mit Issue-Link. Der Agent trägt „wartet auf Admin seit <Datum>, Issue <Link>“ in
   `STATUS.md` ein.
