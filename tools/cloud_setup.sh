#!/bin/bash
# Prepare a cloud session (Claude Code on the web) for this repo. Called by the SessionStart hook in
# .claude/settings.json on every start/resume; exits at once outside the cloud (CLAUDE_CODE_REMOTE is
# "true" only on the cloud VM). Run it by hand with --force, e.g. in a multi-repo session where repo
# hooks do not run.
#
#   - bam-masterdata next to this repo (../bam-masterdata): shallow clone of main if missing
#   - Python deps for tools/ (export_spec.py imports bam_masterdata) and notebook checks:
#     bam-masterdata editable, pybis==1.37.4, nbformat
#
# Never blocks the session: problems are printed (the hook output lands in Claude's context) and the
# script exits 0. No openBIS access and no credentials here - see CLOUD.md for the handover files.

[ "$CLAUDE_CODE_REMOTE" = "true" ] || [ "$1" = "--force" ] || exit 0

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
BMD="$(dirname "$ROOT")/bam-masterdata"
BMD_URL="https://github.com/BAMresearch/bam-masterdata.git"

if [ ! -d "$BMD/.git" ]; then
  if ! git clone --quiet --depth 1 "$BMD_URL" "$BMD" 2>/tmp/bmd_clone.err; then
    echo "cloud_setup: could not clone bam-masterdata to $BMD:"
    sed 's/^/  /' /tmp/bmd_clone.err
    echo "  -> attach BAMresearch/bam-masterdata to the session, then: bash tools/cloud_setup.sh --force (CLOUD.md)"
    exit 0
  fi
fi
echo "cloud_setup: bam-masterdata $(git -C "$BMD" rev-parse --short HEAD) ($(git -C "$BMD" log -1 --format=%cs)) at $BMD"

# Skip the install when a previous start already did it (resume, cached environment).
if python -c "import bam_masterdata, pybis, nbformat" 2>/dev/null; then
  echo "cloud_setup: python deps present (pybis $(python -c 'import pybis; print(pybis.__version__)' 2>/dev/null))"
  exit 0
fi

pip_install() { python -m pip install --quiet --disable-pip-version-check "$@"; }
# Ubuntu 24.04 system Python refuses plain installs (PEP 668); retry with the override in the throwaway VM.
# pybis pinned exactly: bam-masterdata only asks for ~=1.37.4, the notebook generator targets 1.37.4 APIs.
DEPS=(-e "$BMD" "pybis==1.37.4" nbformat)
if pip_install "${DEPS[@]}" || pip_install --break-system-packages "${DEPS[@]}"; then
  echo "cloud_setup: installed bam-masterdata (editable), pybis 1.37.4, nbformat"
else
  echo "cloud_setup: pip install failed - tools/export_spec.py and notebook checks will not run"
fi
exit 0
