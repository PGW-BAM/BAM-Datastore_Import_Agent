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
4. **Excel** für den Admin:
   `bam_masterdata export_to_excel --python-path projects/<name>/datamodel --export-dir projects/<name>/request`
   (enthält nur NEU; ERWEITERN steht im Issue-Text).
5. **checker:**
   `bam_masterdata checker --file-path projects/<name>/datamodel --mode individual 2>&1 | sed 's/\x1b\[[0-9;]*m//g' > projects/<name>/request/checker.log`
   Ziel: 0 Fehler. Warnungen entweder beheben (z. B. Sektionen in Title Case ohne Ziffern) oder im Issue erklären. Bekannte
   Warnungen, die aus dem Standard selbst kommen: `$ANNOTATIONS_STATE is deprecated`, `EXPERIMENTAL_STEP.MECHANICAL_TEST
   has the same properties as EXPERIMENTAL_STEP`.
6. **Issue-Text** `request/issue.md` nach `templates/request/issue.md`: was, warum, Auswirkung, Python oder Excel,
   Tabelle je Klasse mit Begründung aus dem PRD, NACHZIEHEN als eigener Abschnitt, vorgeschlagenes Label
   (`semver:minor` für neue Typen), checker-Ergebnis, kurze Mapping-Notizen (BFO/IAO), falls möglich.
7. **Mail** `request/mail.txt` nach `templates/request/mail.txt`: an datastore@bam.de, kurz, verweist auf das Issue.
8. `STATUS.md`: Schritt 6 „wartet auf D“.

## Prüfen

- [ ] Import-Test grün (`export_spec.py` läuft durch)
- [ ] checker: 0 Fehler, jede Warnung behoben oder erklärt
- [ ] Jede Zeile im Issue hat eine Begründung aus dem PRD
- [ ] Beschreibungen `English//Deutsch`, Sektionen Title Case ohne Ziffern, `mandatory`/`section` gesetzt
- [ ] Der Antrag ist so kurz wie möglich (nichts, was NUTZEN wäre)

## Stopp

◆ **D**, Mensch:
1. Issue in https://github.com/BAMresearch/bam-masterdata/issues anlegen (Text aus `issue.md`, `masterdata.xlsx` anhängen).
   Optional selbst einen PR: Fork, Branch `<issue-nr>-<thema>`, Ziel `dev`.
2. Issue-Link in `mail.txt` eintragen und an datastore@bam.de senden.
3. In `STATUS.md`: „D gesendet (Datum), Issue <Link>, wartet auf Admin“.
