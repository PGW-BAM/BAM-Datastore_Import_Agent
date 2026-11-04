# Was Sie selbst tun

Der Agent arbeitet in der Cloud, ohne Zugang zu openBIS und ohne Sie nach außen zu vertreten. Für die folgenden
Dinge braucht er Sie. Wenn es so weit ist, steht die Aufgabe in `projects/<name>/AUFGABE.md` und gleichzeitig im
Chat, mit allem, was Sie kopieren müssen.

| Aufgabe | Schritt | Wo | Aufwand |
|---|---|---|---|
| Fragen beantworten (Interview) | 2 | Chat | je Runde ein paar Minuten |
| Freigeben (◆ A, B, C, E) | 2, 4, 5, 8 | Prüfseite lesen (`review/<seite>.html` im Browser oder `review/<seite>.md` direkt auf GitHub), dann im Chat: „A freigegeben“ / „A approved“, Ihre Änderungen oder der Text von der Prüfseite | Lesen |
| openBIS lesen | 3, 7 | BAM-Netz: `python tools/bruecke.py <name> lesen` bzw. `pruefen` | 1 Minute |
| Antrag senden (◆ D) | 6 | Browser (GitHub-Issue) + Mail an datastore@bam.de | 5 Minuten |
| Trockenlauf und Anlegen | 8 | BAM-Netz: `… trockenlauf`, nach Freigabe `… anlegen` | 2 Minuten |

Danach schreiben Sie im Chat „erledigt“ (oder was schiefging). Der Agent holt sich die Ergebnisse aus dem Repo.

## Einmal einrichten (Rechner im BAM-Netz)

```bash
git clone https://github.com/PGW-BAM/BAM-Datastore_Import_Agent.git
cd BAM-Datastore_Import_Agent
python -m venv .venv
.venv\Scripts\activate              # Windows   (Linux/macOS: source .venv/bin/activate)
pip install pybis==1.37.4 pyyaml    # für das Notebook zusätzlich: pip install jupyter
```

Voraussetzungen: VPN bzw. BAM-Netz, git mit Schreibrecht auf das Repo (`git push` muss gehen).

Anmeldung bei openBIS: Der Befehl fragt nach einem Token oder, wenn Sie nichts eingeben, nach Benutzername und
Passwort. Nichts davon wird gespeichert. Wer nicht jedes Mal tippen will, setzt für die Sitzung die
Umgebungsvariable `OPENBIS_TOKEN` (Personal Access Token). Der Token gehört nie in eine Datei im Repo oder in den Chat.

## Jedes Mal

```bash
cd BAM-Datastore_Import_Agent
.venv\Scripts\activate
python tools/bruecke.py <name> <aktion> --zweig <zweig>   # aktion: lesen | pruefen | trockenlauf | anlegen
```

Den genauen Befehl gibt Ihnen der Agent in `AUFGABE.md` und im Chat. Cloud-Agenten arbeiten auf eigenen Zweigen und
öffnen Pull Requests. Am einfachsten: den Pull Request mergen, dann läuft alles auf `main`, ohne `--zweig`. Sonst
wechselt `--zweig <zweig>` vorher auf den Zweig des Agenten. Die nächste Agenten-Sitzung starten Sie auf `main` bzw. auf
diesem Zweig (`CLOUD.md` → „Zweige“).

Der Befehl holt zuerst den neuesten Stand (`git pull`), arbeitet, und lädt dann **nur** die Ergebnisdateien von
`projects/<name>/` hoch (`git commit` + `git push`). Mit `--ohne-git` passiert das nicht.

| Aktion | liest | schreibt in openBIS | legt ins Repo |
|---|---|---|---|
| `lesen` | Masterdaten, eigenes Projekt, Equipment-Projekte | nein | `inventory_<instanz>.json` |
| `pruefen` | wie `lesen` | nein | + `delivery_check.md` |
| `trockenlauf` | wie `lesen` | nein | + `reports/dryrun_<datum>.json` |
| `anlegen` | wie `lesen` | **ja**, nur was fehlt; fragt vorher nach „ja“, verweigert bei Lücken | + `reports/apply_<datum>.json` |

Lieber mit Ansicht? Das Notebook `notebooks/openbis_bruecke.ipynb` macht dasselbe Zelle für Zelle. In der ersten Zelle
`PROJECT` auf den Projektnamen aus `AUFGABE.md` setzen. Danach selbst
`git add projects/<name>`, `git commit`, `git push`.

## Antrag senden (◆ D)

Am einfachsten über die Prüfseite `projects/<name>/review/antrag.html`: Dort stehen Titel, Text, Betreff und Mail zum
Kopieren, sobald Sie oben alles mit „passt“ bestätigt haben. Ohne Prüfseite:

1. https://github.com/BAMresearch/bam-masterdata/issues → **New issue**: Titel und Text aus `projects/<name>/request/issue.md`
   einfügen, `request/masterdata.xlsx` anhängen, absenden.
2. Den Link des Issues in `request/mail.txt` einsetzen und die Mail an datastore@bam.de schicken.
3. Im Chat: „D gesendet“ und den Issue-Link.

## Wenn etwas schiefgeht

| Meldung | Was tun |
|---|---|
| `git pull ging nicht` | Lokale Änderungen im Repo. `git status` zeigt sie; behalten: committen, sonst `git checkout -- <datei>`. |
| `git push ging nicht` | Der Commit ist lokal gespeichert. `git pull`, dann `git push`. |
| Anmeldung scheitert, Zeitüberschreitung | VPN an? Instanz in `project.yaml` richtig (`https://playground.datastore.bam.de`)? |
| `Teil 2 meldet Lücken` / `Nicht angelegt` | So gewollt: `delivery_check.md` zeigt, was fehlt. Schreiben Sie im Chat „erledigt“, der Agent klärt es. |
| sonst etwas | Kopieren Sie die Ausgabe in den Chat (ohne Token oder Passwort). |
