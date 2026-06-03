---
description: Sync bam-masterdata repo. Run before any analysis. Fetches latest main branch from BAMresearch/bam-masterdata (no force, no reset).
---

# /bam-sync — Sync bam-masterdata

Behaviour:
1. If `C:\Users\pgerards\repos\bam-masterdata\` does NOT exist:
   - Run: `git clone https://github.com/BAMresearch/bam-masterdata.git C:\Users\pgerards\repos\bam-masterdata`
2. Else:
   - Run: `git -C C:\Users\pgerards\repos\bam-masterdata status --porcelain`
   - If the output is non-empty (local changes exist): STOP and report which files are modified. Do NOT pull. Ask the operator to stash or commit first.
   - If clean: `git -C C:\Users\pgerards\repos\bam-masterdata fetch --all && git -C C:\Users\pgerards\repos\bam-masterdata pull --ff-only origin main`
3. Print the resolved commit SHA: `git -C C:\Users\pgerards\repos\bam-masterdata rev-parse HEAD`
4. Print the commit date: `git -C C:\Users\pgerards\repos\bam-masterdata log -1 --format="%ci"`

## Anti-patterns (DO NOT DO)
- Do NOT run `git reset --hard` or `git push --force`
- Do NOT vendor or copy bam-masterdata source into this repo
- Do NOT add bam-masterdata as a git submodule
