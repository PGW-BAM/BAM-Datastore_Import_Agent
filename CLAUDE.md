@AGENTS.md

## Nur für Claude Code

- Die Befehle `/bam-sync`, `/bam-analyze-prd`, `/bam-generate-types`, `/bam-generate-parser` und die Agenten
  unter `.claude/agents/` sind Abkürzungen für die Schritte 1 und 4–6. Wenn sie und eine Karte unter
  `workflow/` sich widersprechen, gilt die Karte.
- `/bam-generate-notebook` ist durch das allgemeine Brücken-Notebook (`notebooks/openbis_bruecke.ipynb`)
  plus `structure.json` ersetzt (Schritt 8).
- Der SessionStart-Hook (`.claude/settings.json`) ruft `tools/cloud_setup.sh --hook` auf. In Sessions mit mehreren
  Repos läuft er nicht: dann `bash tools/cloud_setup.sh`.
- Einstieg: `/bam-weiter [projekt]` (gleiche Anleitung wie der Skill `.agents/skills/bam-weiter/` für andere Agenten).
