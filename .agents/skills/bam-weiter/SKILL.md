---
name: bam-weiter
description: Ein BAM-Data-Store-Projekt unter projects/ fortsetzen oder neu anlegen. Prüft das Setup, liest STATUS.md, arbeitet den nächsten Workflow-Schritt ab, hält an Prüfpunkten an und gibt dem Menschen seine Aufgabe als AUFGABE.md. Nutzen, wenn jemand "weiter", "Projekt fortsetzen", "neues Projekt", "Interview" oder einen Projektnamen nennt.
---

# Projekt fortsetzen

1. Setup: `bash tools/cloud_setup.sh` (idempotent, schnell; legt `../bam-masterdata` an und installiert Pakete).
2. Regeln lesen: `AGENTS.md` im Repo-Wurzelverzeichnis. Sie gelten ohne Ausnahme.
3. Projekt bestimmen: Name aus der Nachricht, sonst `ls projects/` und nachfragen. Neues Projekt:
   `cp -r templates projects/<name>` und mit der Person `project.yaml` ausfüllen.
4. `projects/<name>/STATUS.md` lesen. Liegt dort eine `AUFGABE.md`, ist der Mensch dran: sie zeigen und fragen, ob
   sie erledigt ist. Erledigt: Ergebnisdateien prüfen (`git pull`), `AUFGABE.md` löschen, weiter.
5. Nächsten offenen Schritt nehmen, Karte `workflow/0N_*.md` öffnen, abarbeiten: Eingabe → Tun → Prüfen → Stopp.
6. Am Stopp: Prüfseite erzeugen, wo es eine gibt (`AGENTS.md` → „Prüfseiten“), und den Prüfpunkt im Chat zur Freigabe stellen, oder die Aufgabe für den Menschen nach `workflow/AUFGABE_VORLAGE.md`
   schreiben und im Chat zeigen. `STATUS.md` fortschreiben, committen, pushen.
7. Immer bevor du auf eine Antwort wartest: committen und pushen (Sitzungen können ablaufen). Läuft die Arbeit auf
   einem eigenen Zweig, nenne ihn der Person: Pull Request mergen (bevorzugt, dann gilt `main`) oder `--zweig` nutzen.
