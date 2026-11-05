---
name: bam-weiter
description: Ein BAM-Data-Store-Projekt unter projects/ fortsetzen oder neu anlegen. Prüft das Setup, liest STATUS.md, arbeitet den nächsten Workflow-Schritt ab, hält an Prüfpunkten an und gibt dem Menschen seine Aufgabe als AUFGABE.md. Nutzen, wenn jemand "weiter", "Projekt fortsetzen", "neues Projekt", "Interview", "Laborablauf im Data Store" oder einen Projektnamen nennt.
---

# Projekt fortsetzen oder anfangen

Diese Anleitung ersetzt einen langen Start-Prompt: Was hier steht, gilt in jeder Sitzung, auch wenn die erste
Nachricht nur ein Satz ist (`workflow/START_PROMPT.md`).

## Start

1. Repo: Ist `PGW-BAM/BAM-Datastore_Import_Agent` nicht in der Arbeitsumgebung, klonen
   (`git clone https://github.com/PGW-BAM/BAM-Datastore_Import_Agent.git`) und hineinwechseln.
   Fehlt `AGENTS.md`, `workflow/strukturmuster.md` oder `tools/render_review.py`, ist der Stand alt: der Person das
   sagen und aufhören.
2. Setup: `bash tools/cloud_setup.sh` (idempotent, schnell; legt `../bam-masterdata` an und installiert Pakete),
   danach `python -m pytest tools/tests -q`. Schlägt etwas fehl: Meldung zeigen und nicht weitermachen.
3. Regeln lesen: `AGENTS.md` vollständig, dann `workflow/README.md` (acht Schritte, Prüfpunkte A–E). Die Regeln gelten
   ohne Ausnahme. `projects/fb72_welded_fatigue` ist ein eingefrorenes Referenzbeispiel: lesen ja, ändern nein.
4. Begrüßen: kurz, dann die acht Schritte als kurze Liste, jeweils mit dem Hinweis, wo die Person selbst etwas tut
   (Interview, Freigaben, openBIS lesen und anlegen im BAM-Netz, Antrag senden; `workflow/MENSCH.md`).
5. Projekt bestimmen: Name aus der Nachricht, sonst `ls projects/` und fragen: neues oder bestehendes Projekt?
   - **Neu:** nach Projektname (kleinbuchstaben_mit_unterstrich), Titel auf Deutsch und Englisch, Fachbereich und
     danach fragen, ob es ein Ablaufschema gibt (draw.io, Bild, PDF) oder ob die Person den Ablauf erzählt. Dann
     `cp -r templates projects/<name>` und `project.yaml` mit der Person ausfüllen.
   - **Bestehend:** `projects/<name>/STATUS.md` lesen und in zwei, drei Sätzen sagen, wo wir stehen und was als
     Nächstes kommt. Liegt eine `AUFGABE.md` vor, ist der Mensch dran: sie zeigen und fragen, ob sie erledigt ist.
     Erledigt: `git pull`, Ergebnisdateien prüfen, `AUFGABE.md` löschen, weiter.

## Arbeiten

6. Immer nur ein Schritt auf einmal: Karte `workflow/0N_*.md` öffnen und abarbeiten: Eingabe → Tun → Prüfen → Stopp.
   - Interview (Schritt 2): pro Nachricht ein Ablaufschritt und höchstens fünf Fragen (`workflow/interview_fragen.md`).
     Jeder Name auf Deutsch und Englisch. Eigene Ideen immer als „Vorschlag“ markieren.
   - Struktur (Schritt 4): nach `workflow/strukturmuster.md` 2–4 Varianten zeigen, eine empfohlen.
7. Am Stopp: Prüfseite erzeugen, wo es eine gibt (`AGENTS.md` → „Prüfseiten“: erst `tools/check_files.py`, dann
   `tools/render_review.py`, nie selbst schreiben), beide Links nennen und den Prüfpunkt im Chat zur Freigabe stellen.
   Oder die Aufgabe für den Menschen nach `workflow/AUFGABE_VORLAGE.md` schreiben und im Chat zeigen, mit jedem Befehl
   zum Kopieren (auf eigenem Zweig mit `--zweig <zweig>`). Weiter erst nach ausdrücklicher Freigabe; sie wörtlich mit
   Datum in `STATUS.md` eintragen.
8. Nach jedem Schritt und jeder Interview-Runde, immer bevor du auf eine Antwort wartest: `STATUS.md` fortschreiben,
   committen und pushen (Sitzungen können ablaufen). Läuft die Arbeit auf einem eigenen Zweig, nenne ihn der Person
   und sag ihr an jedem Stopp, dass sie den Pull Request nach `main` mergen soll.

## Im Chat

- Die Person mit „Sie“ ansprechen, kurz schreiben, ohne Fachjargon (openBIS-Codes nur, wenn sie danach fragt).
- Jede Nachricht endet mit einer Zeile „Ihr nächster Schritt: …“.
- Unsicher? Fragen statt annehmen.
