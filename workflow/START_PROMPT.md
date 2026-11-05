# Start-Prompt für einen Cloud-Agenten (z. B. Mistral Vibe)

So beginnen Sie mit einem Agenten, der dieses Repo nicht kennt:

1. **Vorher (einmal):** Die Mistral GitHub App muss für `PGW-BAM` installiert sein. Offene Pull Requests mit dem
   aktuellen Stand nach `main` mergen.
2. Mistral Vibe im Browser öffnen, neue Sitzung mit dem Repo `PGW-BAM/BAM-Datastore_Import_Agent` (Basis-Zweig `main`).
3. Einen der beiden Texte unten als erste Nachricht einfügen und abschicken.

Läuft eine Sitzung ab (Mistral: nach 3 h ohne Antwort), zuerst den Pull Request der alten Sitzung mergen, sonst fehlt
ihr Stand. Dann in einer neuen Sitzung den Text „Projekt fortsetzen“ einfügen. Der Agent macht bei `STATUS.md` weiter.

Mehr braucht der Prompt nicht: Alles Weitere (Setup, Tests, Regeln, Begrüßung, Interview, Prüfpunkte, Ton) steht in
`AGENTS.md` und im Skill `.agents/skills/bam-weiter/SKILL.md`. Regeln ändern Sie dort, nicht im Prompt.

## Neues Projekt

```text
Du arbeitest im Repo https://github.com/PGW-BAM/BAM-Datastore_Import_Agent (Zweig main).
Lies zuerst AGENTS.md und folge dann Schritt für Schritt .agents/skills/bam-weiter/SKILL.md, beginnend mit „Start“.
Ich möchte einen neuen Laborablauf im BAM Data Store abbilden.
```

## Projekt fortsetzen

```text
Du arbeitest im Repo https://github.com/PGW-BAM/BAM-Datastore_Import_Agent (Zweig main).
Lies zuerst AGENTS.md und folge dann Schritt für Schritt .agents/skills/bam-weiter/SKILL.md, beginnend mit „Start“.
Ich möchte das Projekt <projektname> fortsetzen.
```

Wenn der Pull Request noch nicht gemergt ist, in beiden Texten `main` durch den Zweig der alten Sitzung ersetzen.
