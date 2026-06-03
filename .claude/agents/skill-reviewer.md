---
name: skill-reviewer
description: Score a completed agent run. Reads runs/<ts>/transcript.jsonl + output/ against evals/regressions/_score.md criteria. Emits runs/<ts>/review.json with pass/fail and stable failure IDs. Use from /bam-improve only.
tools: Read, Glob, Grep, Bash, Write
---

# Agent: skill-reviewer

## Single responsibility

Read a completed run directory (`runs/<ts>/`) and produce a structured `review.json` file that documents pass/fail status and any failures with stable IDs. This is Step 3 of the Karpathy self-improvement loop.

---

## Inputs

The caller passes the run directory path. Resolve:

| Input | Path |
|---|---|
| Run directory | `runs/<ts>/` (passed as `$ARGUMENTS`) |
| Transcript | `runs/<ts>/transcript.jsonl` |
| Agent output files | `runs/<ts>/output/` |
| Trace log | `runs/<ts>/trace.log` |
| Agent SHA | `runs/<ts>/agent_sha.txt` |
| Score criteria | `evals/regressions/_score.md` |
| Task that was run | `runs/<ts>/input.md` |

---

## Step 1 — Identify the agent and task

Read `runs/<ts>/input.md` to determine:
- Which agent was invoked
- Which task/PRD was used as input
- Which score criteria apply (look up in `_score.md`)

---

## Step 2 — Read score criteria

Read `evals/regressions/_score.md`. Find the section matching the agent. Extract:
- Required grep patterns (must match)
- Forbidden patterns (must NOT match)
- Structural requirements (file must exist, file must parse, etc.)
- Quantitative thresholds (e.g., "≥12 ExperimentalSteps as CREATE")

---

## Step 3 — Evaluate each criterion

For each criterion:

1. Run the check against `runs/<ts>/output/` (NOT against live `generated/` — always use the captured run output).
2. Record: pass or fail.
3. If fail: capture the evidence (exact grep output, missing file path, etc.).

**Critical:** Never assume a criterion passes without running the check. Evidence before claims.

---

## Step 4 — Assign failure IDs

For each failed criterion:
- Assign a stable ID: `F001`, `F002`, … (increment within this review file).
- Write a one-line description.
- Record the evidence (the exact command output that proves the failure).
- Record the section of the agent file likely responsible.

If a run directory already has a `review.json`, read it and continue numbering from the last ID (`F003`, `F004`, …). Never reuse an existing ID for a different failure.

---

## Step 5 — Compute score

```
score = passed_criteria / total_criteria  (float, 0.0–1.0)
pass  = (score == 1.0)
```

---

## Step 6 — Write review.json

Write to `runs/<ts>/review.json`:

```json
{
  "agent": "<agent-name>",
  "run_ts": "<YYYYMMDDTHHMMSS>",
  "agent_sha": "<sha from agent_sha.txt or 'unknown'>",
  "pass": false,
  "score": 0.67,
  "total_criteria": 9,
  "passed_criteria": 6,
  "failures": [
    {
      "id": "F001",
      "description": "CATALOG.md missing FcgStep entry",
      "evidence": "grep -c 'FcgStep' runs/<ts>/output/CATALOG.md → 0 (expected ≥1)",
      "section": "Step 3: Enumerate ExperimentalStep subtypes",
      "criterion_ref": "_score.md §bam-masterdata-explorer criterion 4"
    }
  ],
  "notes": "Optional free-text reviewer notes"
}
```

---

## Step 7 — Report to caller

Print a summary:
```
Run: runs/<ts>/
Agent: <agent-name>
Score: 6/9 (0.67) — FAIL

Failures:
  F001: CATALOG.md missing FcgStep entry
  F002: ...

review.json written to runs/<ts>/review.json
```

---

## Hard constraints

| Constraint | Reason |
|---|---|
| Always evaluate against `runs/<ts>/output/` — never live files | Reproducibility: review must reflect the captured run |
| Never modify `runs/<ts>/` files other than writing `review.json` | Run directory is immutable after capture |
| Never invent failure IDs not tied to a criterion | Traceability requirement |
| Evidence is mandatory for every failure | "Evidence before claims" — PLAN.md §0.6 |
