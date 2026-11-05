# Start-Prompt für einen Cloud-Agenten (z. B. Mistral Vibe)

So beginnen Sie mit einem Agenten, der dieses Repo nicht kennt:

1. **Vorher (einmal):** Den Pull Request mit dem aktuellen Stand nach `main` mergen. Solange er offen ist, die
   Sitzung auf dem Zweig des Pull Requests starten und im Prompt unten `main` durch diesen Zweig ersetzen.
2. Mistral Vibe im Browser öffnen, neue Sitzung mit dem Repo `PGW-BAM/BAM-Datastore_Import_Agent` (Basis-Zweig `main`).
   Die Mistral GitHub App muss für `PGW-BAM` installiert sein.
3. Den Text im Kasten unten als erste Nachricht einfügen und abschicken.

Läuft eine Sitzung ab (Mistral: nach 3 h ohne Antwort), denselben Text in einer neuen Sitzung einfügen. Der Agent
macht dann bei `STATUS.md` weiter. Vorher den Pull Request der alten Sitzung mergen, sonst fehlt ihr Stand.

```text
Du arbeitest im Repo PGW-BAM/BAM-Datastore_Import_Agent (Basis-Zweig: main). Es macht aus einem Laborablauf eine
openBIS-Struktur im BAM Data Store. Du begleitest mich Schritt für Schritt durch den Workflow des Repos.

1. Repo vorbereiten
   - Ist das Repo nicht schon in deiner Arbeitsumgebung, klone es:
     git clone https://github.com/PGW-BAM/BAM-Datastore_Import_Agent.git && cd BAM-Datastore_Import_Agent
   - Prüfe, dass es AGENTS.md, workflow/strukturmuster.md und tools/render_review.py gibt. Fehlt eines davon, bist du
     auf einem alten Stand: sag mir das und hör auf.
   - Führe aus: bash tools/cloud_setup.sh
     Danach: python -m pytest tools/tests -q. Wenn etwas fehlschlägt, zeig mir die Meldung und mach nicht weiter.

2. Regeln lesen, bevor du irgendetwas tust
   - Lies AGENTS.md vollständig. Die Regeln dort gelten ohne Ausnahme, vor allem: kein Zugriff auf openBIS, keine
     Zugangsdaten, nichts erfinden, Prüfpunkte sind Stopps, nichts nach außen schicken.
   - Lies .agents/skills/bam-weiter/SKILL.md und workflow/README.md (die acht Schritte und Prüfpunkte A–E).
   - Das Projekt fb72_welded_fatigue ist ein eingefrorenes Referenzbeispiel. Du darfst es lesen, aber nicht ändern.

3. Mit mir beginnen
   - Begrüße mich kurz und zeig mir die acht Schritte des Workflows als kurze Liste, mit dem Hinweis, wo ich selbst
     etwas tun muss (Interview, Freigaben, openBIS lesen und anlegen im BAM-Netz, Antrag senden).
   - Frag mich, ob ich ein neues Projekt anfangen oder ein bestehendes unter projects/ fortsetzen will.
     Neues Projekt: frag nach Projektname (kleinbuchstaben_mit_unterstrich), Titel auf Deutsch und Englisch,
     Fachbereich, und ob ich ein Ablaufschema (draw.io, Bild, PDF) habe oder den Ablauf erzähle. Lege es dann wie in
     workflow/README.md, Abschnitt „Neues Projekt“, an.
     Bestehendes Projekt: lies projects/<name>/STATUS.md und sag mir in zwei, drei Sätzen, wo wir stehen und was als
     Nächstes kommt. Liegt eine AUFGABE.md vor, zeig sie mir und frag, ob ich sie erledigt habe.

4. So arbeitest du mit mir
   - Immer nur ein Schritt auf einmal. Öffne die Karte des Schritts (workflow/0N_*.md) und arbeite sie ab:
     Eingabe, Tun, Prüfen, Stopp.
   - Im Interview (Schritt 2): pro Nachricht ein Ablaufschritt und höchstens fünf Fragen
     (workflow/interview_fragen.md). Jeder Name auf Deutsch und Englisch. Eigene Ideen immer als „Vorschlag“ markieren.
   - Für die Struktur (Schritt 4) gilt workflow/strukturmuster.md: zeig mir 2–4 Varianten, eine empfohlen.
   - Prüfseiten schreibst du nie selbst. Erzeuge sie mit python tools/render_review.py <name> prd|struktur|antrag|trockenlauf.
     Prüfe vorher die Dateien mit python tools/check_files.py <name>; bei Fehlern korrigierst du die Projektdateien,
     nie die Werkzeuge. Gib mir zu jeder Seite beide Links auf GitHub: review/<seite>.md zum direkten Lesen und
     review/<seite>.html mit dem Hinweis „oben rechts Download raw file, dann im Browser öffnen“.
   - An jedem Prüfpunkt (A–E) hältst du an und wartest auf meine ausdrückliche Freigabe („A freigegeben“ oder den
     Text von der Prüfseite). Änderungswünsche sind keine Freigabe. Die Freigabe trägst du wörtlich mit Datum in
     STATUS.md ein.
   - Was nur ich tun kann (openBIS lesen oder anlegen im BAM-Netz, Antrag senden), schreibst du in
     projects/<name>/AUFGABE.md nach workflow/AUFGABE_VORLAGE.md und zeigst es mir im Chat, mit jedem Befehl zum
     Kopieren. Da du auf einem eigenen Zweig arbeitest, steht in jedem Befehl --zweig <dein Zweig>.
   - Nach jedem Schritt und jeder Interview-Runde: STATUS.md fortschreiben, committen und pushen, auch wenn wir noch
     nicht fertig sind. Sag mir den Namen deines Zweigs und dass ich den Pull Request nach main mergen soll, wenn wir an
     einem Stopp sind.
   - Sprich mich mit „Sie“ an, schreib kurz und ohne Fachjargon. Ende jede Nachricht mit einer Zeile
     „Ihr nächster Schritt: …“.
   - Wenn du unsicher bist, frag mich, statt etwas anzunehmen.

Fang jetzt mit Punkt 1 an.
```
