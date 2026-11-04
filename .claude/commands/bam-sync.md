---
description: Make sure bam-masterdata is at the pinned release (BMD_REF in tools/cloud_setup.sh). Run before any analysis. Never pulls a moving branch.
---

# /bam-sync: bam-masterdata at the pinned release

`bam-masterdata` lives next to this repo: `../bam-masterdata` (relative to the repo root). It is pinned to
one release, `BMD_REF` in `tools/cloud_setup.sh` (currently `v0.17.0`). All catalogs and specs in this repo
are built against that release. See `workflow/01_standard.md`.

Behaviour (run from the repo root):
1. Read the pin: `grep -o 'BMD_REF:-[^}]*' tools/cloud_setup.sh` → e.g. `v0.17.0`.
2. If `../bam-masterdata/` does NOT exist: `bash tools/cloud_setup.sh --force` (clones the pinned tag,
   installs the Python packages). If the clone fails in a cloud session: STOP and point to `CLOUD.md`.
3. Else:
   - `git -C ../bam-masterdata status --porcelain` non-empty: STOP and report the modified files.
   - `git -C ../bam-masterdata describe --tags --exact-match` ≠ pin: report it. Do not switch silently;
     ask the operator (switching changes catalog citations). To switch: remove the folder and run step 2.
4. Print SHA and date: `git -C ../bam-masterdata rev-parse HEAD`, `git -C ../bam-masterdata log -1 --format="%ci"`.

Moving to a newer release is a deliberate change: bump `BMD_REF`, rebuild the catalog
(`python tools/build_catalog.py`), re-export the specs of active projects and compare.

## Anti-patterns (DO NOT DO)
- Do NOT `git pull` a branch (`main`, `dev`) into `../bam-masterdata`: the pin is a release tag
- Do NOT run `git reset --hard` or `git push --force`
- Do NOT vendor or copy bam-masterdata source into this repo
- Do NOT add bam-masterdata as a git submodule
- Do NOT hardcode a machine-specific path (`C:\Users\...`): always `../bam-masterdata`
