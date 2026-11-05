# Arbeiten mit Cloud-Agenten (Claude Code, Mistral Vibe, …)

Cloud-Sessions laufen auf einer VM des Anbieters, **außerhalb des BAM-Netzes**. Daraus folgt eine feste Aufteilung:

- **Cloud-Agent:** alles, was nur Dateien braucht (PRD → Anforderungen → Design → Gap-Report → Klassen → Spec, Notebook, Parser).
- **Mensch im BAM-Netz:** alles, was die openBIS-Instanz berührt (Inventar lesen, Objekte anlegen). Kein lokaler Agent nötig.

Die beiden Seiten tauschen **committete Dateien** aus. Der Agent bekommt nie Zugangsdaten oder einen Netzweg zur Instanz.

**Hauptweg seit 11/2026:** das Brücken-Notebook `notebooks/openbis_bruecke.ipynb` (Lesen, Prüfen, Trockenlauf, Anlegen), gesteuert
über `projects/<name>/project.yaml` und `structure.json`. Ablauf: `workflow/README.md`, Schritte 3, 7, 8. Masterdaten legt auf
den offiziellen Instanzen der Admin an (Schritt 6, Antrag). Die Browser-Skripte unten sind der Weg ohne Python im BAM-Netz bzw.
für Instanzen, auf denen du selbst Admin bist (dev1).

```
  BAM-Netz (Mensch, ELN-Tab)                       Cloud-Session (Agent)
  ─────────────────────────                        ─────────────────────
  openbis_inventory.js ──► live/<inst>_inventory.json ──►  Inventar-MD, Design, Gap-Report
                                                           Klassen, spec.json, demo_series.json
  openbis_apply.js  ◄────────── spec.json  ◄──────────────┘
  openbis_demo.js   ◄────────── demo_series.json
        │
        └──► <stem>/apply_report_<datum>.json ──► Agent prüft, was angelegt/übersprungen wurde
```

## Einrichtung (einmalig)

1. **Repo verbinden:** Claude GitHub App auf `PGW-BAM/BAM-Datastore_Import_Agent` installieren (claude.ai/code → Onboarding).
2. **Umgebung:** Netzwerkzugriff **Trusted** reicht (GitHub, PyPI). Zusätzlich unter *Allowed domains* für die Doku:
   `bamresearch.github.io` (bam-masterdata-Doku, erreichbar) und `datastore.bam.de` (Wiki; aus der Cloud derzeit nicht
   erreichbar, „upstream dial failed“). Die openBIS-Instanzen (`dev1.…`, `playground.…`) **nicht** freigeben und **kein**
   openBIS-Token als Variable oder Secret hinterlegen. Das wäre erst nach Freigabe durch die BAM-IT ein Thema.
3. **Session-Start:** Der SessionStart-Hook in `.claude/settings.json` ruft `tools/cloud_setup.sh` auf. Das Skript
   - klont `bam-masterdata` nach `../bam-masterdata` (shallow, gepinnter Release `BMD_REF`, derzeit `v0.17.0`), falls es fehlt,
   - installiert `bam-masterdata` (editable), `pybis==1.37.4`, `nbformat` und `pyyaml`,
   - meldet SHA und Stand. Lokal (Windows) beendet es sich sofort, weil `CLAUDE_CODE_REMOTE` dort nicht `true` ist.

### bam-masterdata

Der Klon läuft über den GitHub-Proxy der Cloud-VM. Lehnt der Proxy ein nicht angehängtes Repo ab, meldet das Skript es beim Start.
Dann `BAMresearch/bam-masterdata` als **zweites Repo** an die Session hängen und `bash tools/cloud_setup.sh` ausführen
lassen. In Sessions mit mehreren Repos laufen Repo-Hooks nicht.

Lokal liegt `bam-masterdata` ebenfalls unter `../bam-masterdata` (`/bam-sync`). Damit Agents dort ohne Rückfrage lesen dürfen,
gehört in die eigene `.claude/settings.local.json`:

```json
{ "permissions": { "additionalDirectories": ["C:/Users/<du>/repos/bam-masterdata"] } }
```

## Übergabe 1 (Browser-Variante): Inventar rein

Mit Python im BAM-Netz stattdessen: Brücken-Notebook, Teil 1 (`workflow/03_ist_stand.md`).

Wann: vor `/bam-analyze-prd` für eine neue Instanz oder wenn sich die Instanz geändert hat.

1. Im BAM-Netz das ELN der Instanz öffnen und anmelden (z. B. https://dev1.datastore.bam.de).
2. DevTools → Konsole: Inhalt von `tools/openbis_inventory.js` einfügen, dann
   ```js
   const inv = await inventory();
   copy(JSON.stringify(inv, null, 1));
   ```
   Das Skript macht nur `search*`-Aufrufe und ändert nichts.
3. Zwischenablage als `generated/live/<instanz>_inventory.json` speichern (z. B. `dev1_inventory.json`) und committen.
   Ohne lokales git geht das auch per GitHub-Weboberfläche („Add file → Create new file“).
4. In der Cloud-Session: `/bam-analyze-prd …`. Schritt 3 der Pipeline schreibt aus der JSON-Datei
   `generated/live/<instanz>_inventory.md` (Vergleich mit dem Standard, Altbestand) statt die Instanz abzufragen.

Inhalt der JSON: Instanz, Zeitpunkt, Server-Info, Vokabulare mit Termen, Property-Typen, Object-/Collection-/Dataset-Typen
mit zugewiesenen Properties (Sektion, Pflicht), Projekte, Collections mit Typ. Keine Objektinhalte, keine Personendaten außer
dem, was in Typbeschreibungen steht.

## Übergabe 2 (Browser-Variante, nur mit Admin-Rechten): Spec raus

Auf den offiziellen Instanzen legt der Admin die Masterdaten an (`workflow/06_antrag.md`); Objekte legt das Brücken-Notebook an.

Wann: nach dem menschlichen Review von `design.md` und `gap-report.md` und nach `/bam-generate-types`.

Der Agent erzeugt und committet:

| Datei | Inhalt | Erzeugt durch |
|---|---|---|
| `generated/<stem>/datamodel/*.py` | PR-fähige bam-masterdata-Klassen (nur CREATE) | `/bam-generate-types` |
| `generated/<stem>/spec.json` | Soll-Zustand: `vocabularies`, `extensions`, `object_types` | `python tools/export_spec.py generated/<stem>/datamodel > generated/<stem>/spec.json` |
| `generated/<stem>/demo_series.json` | Objekt-Layout: Space, Projekt, Collections, Inventar, SOP, Proben, Schritte | Agent aus `design.json` |
| `generated/<stem>/sop_workflow_plan.txt` | Text für das SOP-/Ablaufplan-Objekt | Agent |
| `notebooks/<stem>_provisioning.ipynb` | Alternative für Betreiber mit pyBIS | `/bam-generate-notebook` |

Anwenden im BAM-Netz (ELN-Tab, DevTools-Konsole), **immer zuerst als Trockenlauf**:

```js
// 1. Masterdaten: Inhalt von tools/openbis_apply.js einfügen
const SPEC = /* Inhalt von generated/<stem>/spec.json */;
const plan = await applySpec(SPEC, { dryRun: true });   // prüfen: create*, skipped, conflicts
const done = await applySpec(SPEC, { dryRun: false });

// 2. Objekte: Inhalt von tools/openbis_demo.js einfügen
const DEMO = /* Inhalt von generated/<stem>/demo_series.json */;
const SOP_TEXT = `/* Inhalt von generated/<stem>/sop_workflow_plan.txt */`;
const r0 = await provisionDemo(DEMO, SOP_TEXT, { dryRun: true });
const r1 = await provisionDemo(DEMO, SOP_TEXT, { dryRun: false });

copy(JSON.stringify({ date: new Date().toISOString(), instance: location.origin, masterdata: done, objects: r1 }, null, 1));
```

Beide Skripte legen nur an, was fehlt. Sie ändern oder löschen nichts Bestehendes und melden Abweichungen als `conflicts` bzw.
`droppedProps`. Den Bericht als `generated/<stem>/apply_report_<JJJJ-MM-TT>.json` committen, dann kann der Agent in der nächsten
Session prüfen, was angelegt oder übersprungen wurde. Unwiderrufliche Schritte (Papierkorb leeren, Typen löschen) bleiben
Handarbeit nach Checkliste (`CLEANUP_<instanz>.md`).

## Andere Cloud-Agenten

Alles Wesentliche steht in `AGENTS.md`, das die meisten Agenten von selbst lesen. Plattformunabhängig gilt: als Erstes
`bash tools/cloud_setup.sh`, Netz für `github.com`, `pypi.org`, `files.pythonhosted.org` (Doku: `bamresearch.github.io`),
openBIS nie freigeben. Die Übergaben laufen über `AUFGABE.md`, `tools/bruecke.py` und das Repo, egal welcher Agent.

**Mistral Vibe im Browser („Vibe Code Web“)**, Stand 11/2026 nach https://docs.mistral.ai/vibe/code/vibe-code-web/get-started
und den Unterseiten Sandbox environment, Sessions, Limits and lifecycle, GitHub repositories and permissions; noch nicht
selbst ausprobiert:

| Thema | Vibe Code Web | Folge für dieses Repo |
|---|---|---|
| Anleitung | dasselbe Agenten-Gerüst wie die Vibe-CLI: liest `AGENTS.md` und Skills aus `.agents/skills/` | Einstieg Skill `bam-weiter`, Regeln aus `AGENTS.md` |
| Setup | Standard-Linux-Image mit git, gängigen Sprachen und Paketmanagern. Eigene Setup-Skripte, Secrets und Umgebungsvariablen gibt es noch nicht (geplant) | der Agent ruft `bash tools/cloud_setup.sh` selbst auf; wir brauchen keine Secrets |
| Netz | ausgehendes Internet, von Mistral verwaltet; keine eigene Allowlist | Klon von bam-masterdata und PyPI sollten gehen; openBIS ist ohnehin nur im BAM-Netz erreichbar |
| GitHub | Mistral GitHub App; ein Projekt umfasst Repos **eines** Besitzers (hier `PGW-BAM`). bam-masterdata (öffentlich) wird per https geklont, nicht angehängt | GitHub App für `PGW-BAM` installieren und das Repo auswählen |
| Ergebnis | jede Sitzung arbeitet auf einem Zweig und öffnet einen Pull Request gegen den Basis-Zweig | siehe „Zweige“ unten |
| Lebensdauer | höchstens 24 h, Abbruch nach 3 h ohne Antwort; eine beendete Sitzung lässt sich **nicht** fortsetzen | Zustand nach jedem Schritt und jeder Interview-Runde committen und pushen; eine neue Sitzung macht bei `STATUS.md` weiter |
| Kontingent | kostenlos 2 Sitzungen am Tag, bezahlt 100; Modell Mistral Medium 3.5 | |

**Zweige (alle Plattformen).** Cloud-Agenten arbeiten auf eigenen Zweigen und liefern Pull Requests. Am einfachsten
bleibt der gemeinsame Stand auf `main`:
1. An jedem Stopp (Prüfpunkt oder `AUFGABE.md`) pusht der Agent. Du prüfst den Pull Request und mergst ihn.
2. `tools/bruecke.py` läuft dann ohne `--zweig` auf `main` und lädt die Ergebnisse dorthin hoch.
3. Die nächste Agenten-Sitzung startest du auf `main`. Sie findet `STATUS.md` und die Ergebnisse vor.
Ohne Merge geht es auch: Dann nennt `AUFGABE.md` den Zweig (`--zweig`), und die nächste Sitzung muss auf genau diesem
Zweig starten.

**Claude Code im Web:** wie oben beschrieben (Hook, Netz „Trusted“ plus Doku-Domains).

## Was in der Cloud nicht mitkommt

| Lokal vorhanden | In der Cloud | Umgang |
|---|---|---|
| `runs/` (gitignored) | jede Session startet leer | Runs für `/bam-improve` gezielt committen (`git add -f runs/<ts>`) oder lokal auswerten |
| `presentation/poster/input/` (BAM-Vorlage, gitignored) | fehlt | Poster-Arbeit außerhalb der Cloud-Session |
| `.claude/settings.local.json`, `~/.claude/` | nicht gelesen | Projektweite Regeln in `.claude/settings.json`, Wissen in `CLAUDE.md`/`.claude/` |
| Lokale Plugins (claude-mem, Playwright, Chrome) | nicht geladen | Entscheidungen in Repo-Dateien festhalten |
| Browser mit BAM-Netz | keiner | siehe Übergaben oben |

## Später: direkter Zugriff

Soll der Agent die Instanz selbst erreichen, gibt es zwei Wege. Beide setzen eine Freigabe durch die BAM-IT voraus:

- **Self-hosted Environment:** Die Cloud-Session läuft auf einem Runner im BAM-Netz. Der Netzweg ist intern, Daten verlassen
  das Netz nur Richtung Anthropic-API.
- **Freigabe von außen:** dev1 für die Egress-Adressen des Anbieters öffnen, dazu ein kurzlebiges, auf dev1 beschränktes Token
  als Network-Secret. Das ist der riskantere Weg und wird für Produktivinstanzen nicht empfohlen.
