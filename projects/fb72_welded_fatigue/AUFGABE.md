# Ihre Aufgabe: Playground einmal auslesen

Projekt `fb72_welded_fatigue` · Schritt 3 · vom Agenten am 2026-11-04

**Wo:** Rechner im BAM-Netz (VPN) · **Dauer:** etwa 10 Minuten beim ersten Mal, danach 1 Minute
**Warum:** Der Agent muss wissen, welche Typen, Properties und Geräte es auf `playground.datastore.bam.de` wirklich gibt und wie
dort Ihr Space und die Equipment-Projekte heißen. In `project.yaml` stehen noch die Pfade von dev1. Das Lesen ändert
nichts in openBIS.

## So geht es

1. Einmalig einrichten, falls noch nicht geschehen (Details: `workflow/MENSCH.md`):

   ```bash
   git clone https://github.com/PGW-BAM/BAM-Datastore_Import_Agent.git
   cd BAM-Datastore_Import_Agent
   python -m venv .venv
   .venv\Scripts\activate
   pip install pybis==1.37.4 pyyaml
   ```

2. Auf den Arbeitszweig wechseln (nur nötig, solange die neuen Werkzeuge noch nicht auf `main` sind):

   ```bash
   git fetch origin
   git checkout claude/quirky-archimedes-134r67
   ```

3. Lesen. Der Befehl fragt nach Token oder Benutzername/Passwort und lädt das Ergebnis selbst hoch:

   ```bash
   python tools/bruecke.py fb72_welded_fatigue lesen --zweig claude/quirky-archimedes-134r67
   ```

   Erwartet: eine Zeile `gelesen: … Object-Types, … Objekte in 3 Projekten` und `git: hochgeladen`. Dass die Projekte aus
   `project.yaml` auf dem Playground noch nicht passen, ist in Ordnung: Der Export enthält auch die Liste aller Projekte,
   die Sie sehen dürfen. Daraus sucht der Agent die richtigen heraus.

## Danach

Schreiben Sie im Chat „erledigt“, oder was schiefging (Ausgabe einfügen, ohne Token/Passwort).
Hilfe zur Einrichtung und bei Fehlern: `workflow/MENSCH.md`.
