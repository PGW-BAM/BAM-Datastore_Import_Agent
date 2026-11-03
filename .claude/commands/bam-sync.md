---
description: Sync bam-masterdata repo. Run before any analysis. Fetches latest main branch from BAMresearch/bam-masterdata (no force, no reset).
---

# /bam-sync — Sync bam-masterdata

`bam-masterdata` lives next to this repo: `../bam-masterdata` (relative to the repo root). This holds
locally and in cloud sessions, where `tools/cloud_setup.sh` clones it at session start (see `CLOUD.md`).

Behaviour (run from the repo root):
1. If `../bam-masterdata/` does NOT exist:
   - Run: `git clone https://github.com/BAMresearch/bam-masterdata.git ../bam-masterdata`
   - If the clone fails in a cloud session: STOP and point the operator to `CLOUD.md` → "bam-masterdata"
2. Else:
   - Run: `git -C ../bam-masterdata status --porcelain`
   - If the output is non-empty (local changes exist): STOP and report which files are modified. Do NOT pull. Ask the operator to stash or commit first.
   - If clean: `git -C ../bam-masterdata fetch --all && git -C ../bam-masterdata pull --ff-only origin main`
3. Print the resolved commit SHA: `git -C ../bam-masterdata rev-parse HEAD`
4. Print the commit date: `git -C ../bam-masterdata log -1 --format="%ci"`

## Anti-patterns (DO NOT DO)
- Do NOT run `git reset --hard` or `git push --force`
- Do NOT vendor or copy bam-masterdata source into this repo
- Do NOT add bam-masterdata as a git submodule
- Do NOT hardcode a machine-specific path (`C:\Users\...`) — always `../bam-masterdata`
