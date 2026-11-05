#!/bin/bash
# Prepare a cloud agent session for this repo. Idempotent, about one second when everything is there.
#
#   bash tools/cloud_setup.sh          any agent, any cloud sandbox (Mistral Vibe, Codex, ...): just run it
#   bash tools/cloud_setup.sh --hook   Claude Code SessionStart hook (.claude/settings.json): does nothing
#                                      outside Claude's cloud VM (CLAUDE_CODE_REMOTE != true), e.g. on a laptop
#   --force                            accepted for older instructions, same as no option
#
#   - bam-masterdata next to this repo (../bam-masterdata): shallow clone of the PINNED release if missing
#   - Python deps for tools/ (export_spec.py imports bam_masterdata) and notebook checks:
#     bam-masterdata editable, pybis==1.37.4, nbformat, pyyaml
#
# The pin lives in one place: BMD_REF below (override with BMD_REF=<tag> bash tools/cloud_setup.sh).
# All committed catalogs/specs are built against it; bump it on purpose, then rebuild the catalog.
#
# Never blocks the session: problems are printed (the hook output lands in the agent's context) and the
# script exits 0. No openBIS access and no credentials here - see CLOUD.md and workflow/README.md.

if [ "$1" = "--hook" ] && [ "$CLAUDE_CODE_REMOTE" != "true" ]; then exit 0; fi

BMD_REF="${BMD_REF:-v0.17.0}"
ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
BMD="$(dirname "$ROOT")/bam-masterdata"
BMD_URL="https://github.com/BAMresearch/bam-masterdata.git"
ERR="$(mktemp)"

if [ ! -d "$BMD/.git" ]; then
  if ! git clone --quiet --depth 1 --branch "$BMD_REF" "$BMD_URL" "$BMD" 2>"$ERR"; then
    echo "cloud_setup: could not clone bam-masterdata $BMD_REF to $BMD:"
    sed 's/^/  /' "$ERR"
    echo "  -> attach BAMresearch/bam-masterdata to the session, then: bash tools/cloud_setup.sh (CLOUD.md)"
    exit 0
  fi
fi
HAVE="$(git -C "$BMD" describe --tags --exact-match 2>/dev/null || git -C "$BMD" rev-parse --short HEAD)"
echo "cloud_setup: bam-masterdata $HAVE ($(git -C "$BMD" log -1 --format=%cs)) at $BMD"
if [ "$HAVE" != "$BMD_REF" ]; then
  echo "cloud_setup: WARNING - expected pinned $BMD_REF, found $HAVE. Not touching an existing checkout;"
  echo "  catalog citations may not match. To switch: remove $BMD and rerun."
fi

# Skip the install when a previous start already did it (resume, cached environment).
if python -c "import bam_masterdata, pybis, nbformat, yaml" 2>/dev/null; then
  echo "cloud_setup: python deps present (pybis $(python -c 'import pybis; print(pybis.__version__)' 2>/dev/null))"
  exit 0
fi

pip_install() { python -m pip install --quiet --disable-pip-version-check "$@"; }
# Ubuntu 24.04 system Python refuses plain installs (PEP 668); retry with the override in the throwaway VM.
# pybis pinned exactly: bam-masterdata only asks for ~=1.37.4, the bridge notebook targets 1.37.4 APIs.
DEPS=(-e "$BMD" "pybis==1.37.4" nbformat pyyaml)
if pip_install "${DEPS[@]}" || pip_install --break-system-packages "${DEPS[@]}"; then
  echo "cloud_setup: installed bam-masterdata (editable), pybis 1.37.4, nbformat, pyyaml"
else
  echo "cloud_setup: pip install failed - tools/export_spec.py and notebook checks will not run"
fi
exit 0
