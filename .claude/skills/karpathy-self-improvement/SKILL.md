# Karpathy Self-Improvement Loop

## Type: Rigid

Follow this skill exactly. Do not adapt or abbreviate the steps.

## Overview

A disciplined 7-step loop for iteratively improving agent prompts using observed run data. Encoded from PLAN.md §0.6. Applied by the `/bam-improve` command.

**Core principle:** Every change to an agent's instructions must be justified by a specific, logged failure from a real run. No speculative tightening.

---

## The 7 Steps

### Step 1 — Run

Execute the target agent against a task:

```bash
# Example: running bam-masterdata-explorer
# The transcript is captured automatically if PostToolUse hook is active.
# If not, the /bam-improve command handles capture manually.
```

Capture to `runs/<timestamp>/`:
- `input.md` — the task description / slash command invocation
- `transcript.jsonl` — every tool call + result, one JSON object per line
- `output/` — all files the agent wrote (copied, not symlinked)
- `trace.log` — stdout/stderr
- `agent_sha.txt` — `git hash-object .claude/agents/<agent>.md` or file mtime if no git

### Step 2 — Persist

Ensure `runs/<timestamp>/` is complete before proceeding. The timestamp MUST be ISO-8601 (`YYYYMMDDTHHMMSS`).

```
runs/
  20260601T143022/
    input.md
    transcript.jsonl
    output/
      CATALOG.md          # for bam-masterdata-explorer runs
      gap-report.md       # for gap-analyzer runs
      ...
    trace.log
    agent_sha.txt
```

Never overwrite an existing run directory. Use a new timestamp.

### Step 3 — Score / Annotate

Invoke the `skill-reviewer` agent on the run directory:

```
Input:  runs/<ts>/
Output: runs/<ts>/review.json
```

`review.json` schema:
```json
{
  "agent": "bam-masterdata-explorer",
  "run_ts": "20260601T143022",
  "agent_sha": "abc123...",
  "pass": false,
  "score": 0.67,
  "failures": [
    {
      "id": "F001",
      "description": "CATALOG.md missing FcgStep entry",
      "evidence": "grep -c FcgStep output/CATALOG.md → 0",
      "section": "Step 3: Enumerate ExperimentalStep subtypes"
    }
  ]
}
```

Failure IDs are stable across sessions (`F001`, `F002`, …). Never reuse an ID for a different failure.

Human annotators may edit `review.json` directly before Step 4.

### Step 4 — Critique → Diff

Invoke the `prompt-surgeon` agent:

```
Input:  runs/<ts>/review.json  +  .claude/agents/<agent>.md
Output: runs/<ts>/proposed.diff  (unified diff format)
        runs/<ts>/rationale.md   (per-hunk: failure-ID → rationale)
```

**Surgical Changes rule (MUST enforce):**
- Every hunk in `proposed.diff` MUST cite a failure ID from `review.json`.
- Hunks not tied to a logged failure MUST be rejected.
- "Allowed APIs" and "Anti-patterns" sections of agent files are FROZEN — `prompt-surgeon` MUST refuse to touch them.

### Step 5 — Approve

Render the diff for human review:

```bash
cat runs/<ts>/proposed.diff
```

Also show `runs/<ts>/rationale.md` so the reviewer understands the mapping.

Human approves or rejects. **No automated approval.** If rejected, record the rejection reason in `runs/<ts>/rejection.md` and stop.

### Step 6 — Apply + Version

If approved:

```bash
git apply runs/<ts>/proposed.diff
```

Then commit:
```bash
git add .claude/agents/<agent>.md
git commit -m "improve(<agent>): address failures F001,F002 from run <ts>

Failure-to-hunk mapping: runs/<ts>/rationale.md
Run directory: runs/<ts>/
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Bump the version comment at the top of the agent file (`# v1.0 → # v1.1`).

### Step 7 — Regress

Re-run all regression tasks:

```bash
# Run each task file under evals/regressions/*.task.md
# and compare outputs against _score.md criteria
```

**Monotone score requirement:** The total score across all regression tasks must not decrease. If any regression score drops, revert the applied diff via `git revert HEAD` and record the regression in `runs/<ts>/regression-failure.md`.

---

## Surgical Changes Rule (detailed)

From PLAN.md §0.6 and §3.4:

1. **Failure-anchored**: Every proposed change traces to a specific failure ID.
2. **Minimal scope**: Change only the section of the agent file that caused the failure. Never refactor unrelated sections.
3. **Protected sections**: These sections in agent `.md` files are NEVER modified via this loop:
   - `## Allowed APIs` / `### Allowed APIs`
   - `## Anti-patterns` / `### Anti-patterns`
   - `### 0.2 Allowed pyBIS APIs`
   - `### 0.3 Anti-patterns`
   These are governed by Phase 0 evidence (PLAN.md), not run data.
4. **One diff, one run**: A `proposed.diff` is tied to exactly one run directory. Never aggregate failures from multiple runs into a single diff without explicit human approval.

---

## Anti-patterns

| Pattern | Why it's wrong |
|---|---|
| Proposing "tightening" without a failure ID | Speculative — makes the agent harder to maintain |
| Editing "Allowed APIs" section based on run data | That section is frozen; changes require updating PLAN.md first |
| Applying diff without human review | Removes the human-in-the-loop safety |
| Skipping Step 7 (regression) | Drift — improvements in one area silently break others |
| Reusing a failure ID for a different failure | Breaks traceability |
| Auto-approving in batch without per-hunk review | The Surgical Changes rule exists to prevent compound errors |

---

## Traceability Contract

Every improvement to an agent file must be traceable to:
- A run directory (`runs/<ts>/`)
- A failure ID in `review.json`
- A hunk in `proposed.diff` with a matching rationale entry

This chain makes the improvement history auditable: given any version of an agent file, you can find which failure caused which change.
