# /bam-improve

Run the Karpathy self-improvement loop on a BAM agent.

## Usage

```
/bam-improve <agent-name> [--runs N]
```

Examples:
```
/bam-improve bam-masterdata-explorer
/bam-improve gap-analyzer --runs 3
/bam-improve prd-requirements-extractor
```

`--runs N` (default: 1) — number of most-recent runs to review. When N > 1, the worst-scoring run drives the diff proposal.

## Pre-requisites

- [ ] At least one completed run exists in `runs/` for the target agent.
- [ ] `evals/regressions/_score.md` exists with criteria for the target agent.
- [ ] The agent file `.claude/agents/<agent>.md` is committed (so `git apply` produces a clean diff).

## Pipeline (7 steps — see `.claude/skills/karpathy-self-improvement/SKILL.md`)

### Step 1 — Identify runs

```bash
ls -d runs/*/  | sort -r | head -N
```

Filter to runs where `runs/<ts>/input.md` mentions the target agent. If no matching run exists, stop and print:
> "No runs found for `<agent>`. Run the agent against a task first, then call `/bam-improve`."

### Step 2 — Persist check

Verify each candidate run has:
- `transcript.jsonl`
- `output/` (non-empty)
- `trace.log`
- `agent_sha.txt`

Skip runs with missing files and warn.

### Step 3 — Score (invoke skill-reviewer)

For each candidate run that lacks a `review.json`:
```
Invoke: skill-reviewer
Input:  runs/<ts>/
```

If `--runs N > 1`: pick the run with the lowest `score` from all `review.json` files as the driver for Step 4.

### Step 4 — Critique → diff (invoke prompt-surgeon)

```
Invoke: prompt-surgeon
Input:  runs/<driver-ts>/   (worst-scoring or only run)
```

Produces:
- `runs/<driver-ts>/proposed.diff`
- `runs/<driver-ts>/rationale.md`

### Step 5 — Render for approval

Print:

```
════════════════════════════════════════════════════════
  Proposed improvements for: <agent>
  Based on run: runs/<driver-ts>/
  Score: <N>/<total> (<pct>%)
════════════════════════════════════════════════════════

<contents of runs/<driver-ts>/rationale.md>

════ DIFF ════════════════════════════════════════════
<contents of runs/<driver-ts>/proposed.diff>
══════════════════════════════════════════════════════

Apply this diff? (y/n)
```

Wait for user confirmation. **Never auto-apply.**

### Step 6 — Apply + commit (on approval)

```bash
git apply runs/<driver-ts>/proposed.diff
git add .claude/agents/<agent>.md
git commit -m "improve(<agent>): address failures from run <driver-ts>

Failures addressed: <comma-separated IDs>
Rationale: runs/<driver-ts>/rationale.md
Run directory: runs/<driver-ts>/
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Bump version comment at top of agent file (`# v1.0` → `# v1.1`).

If `git apply` fails (no git repo, merge conflict, etc.):
- Print the diff and instructions to apply manually.
- Do NOT edit the agent file directly with Edit tool (bypasses audit trail).

### Step 7 — Regress

Re-run the pipeline against all regression tasks under `evals/regressions/*.task.md`:

For each `*.task.md`:
1. Read the task.
2. Invoke the relevant agents as specified in the task file.
3. Evaluate outputs against `evals/regressions/_score.md`.
4. Record scores in `runs/<driver-ts>/regression-results.md`.

**Monotone score check:**

Compare total score against the baseline recorded in `runs/<driver-ts>/review.json`.

- If all scores ≥ baseline: print "Regression suite passed. Improvement committed."
- If any score drops: `git revert HEAD --no-edit` and print:
  > "Regression detected in <task>: score dropped from <old> to <new>. Diff reverted. Investigate before re-applying."

## Anti-patterns

| Wrong | Right |
|---|---|
| Auto-applying without user confirmation | Always wait for explicit `y` |
| Editing agent `.md` directly with Edit tool | Use `git apply` for auditability |
| Running `/bam-improve` without any prior runs | Run the agent first, then improve |
| Skipping Step 7 (regression) | Monotone score is mandatory |
| Accepting a diff that touches Allowed APIs section | `prompt-surgeon` should have rejected this; flag it |

## Architecture note

This command implements Steps 1-7 of the **Karpathy self-improvement loop** defined in `.claude/skills/karpathy-self-improvement/SKILL.md`. The loop requires two agents:

| Agent | Role | Step |
|---|---|---|
| `skill-reviewer` | Scores run against criteria | Step 3 |
| `prompt-surgeon` | Proposes minimal diff from failures | Step 4 |

The human remains in the loop at Step 5 (approval). The loop is designed to be run iteratively: improve → regress → improve → regress until the regression suite is fully green.
