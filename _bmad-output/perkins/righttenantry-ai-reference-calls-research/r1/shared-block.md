# Shared review brief — Perkins round 1, PR #540 (solarity-services/RightTenantry)

You are one of 7 parallel review lenses in an automated Perkins PR review, run per the
`code-review` skill's reviewer definitions. Read this entire block, then follow the
lens-specific brief that pointed you here.

## Context

- **PR under review:** https://github.com/solarity-services/RightTenantry/pull/540
  — a **documentation-only research deliverable**: 10 new markdown files under
  `_bmad-output/planning-artifacts/research/` (a domain-research report plus its
  supporting thread docs). **No code changes.** Calibrate your lens accordingly.
- **Reviewed sha:** afdfcd6a27eeb2790ce8d5c32ebb251cafc50046

## Inputs

- **Canonical diff (review THESE bytes):**
  `/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/diff.patch`
  — read it first; it is the exact `gh pr diff` output every lens reviews.
- **Repository (read-only verification access):** a detached worktree at exactly the
  reviewed sha:
  `/Users/moses/.herdr/worktrees/RightTenantry/perkins-ai-reference-calls-research-r1`
  You may read files and run read-only commands (ls, grep, git log/show) there to verify
  the diff's claims against the actual repository. **Never edit, write, or commit
  anything inside the worktree.**
- **Project conventions:** read `AGENTS.md` and `CLAUDE.md` at the worktree root.
- **Spec (what this PR is meant to do):**
  1. The original job briefing:
     `/Users/moses/code/_bmad-output/briefings/righttenantry-ai-reference-calls-research.md`
  2. GitHub issue #535 — run: `gh issue view 535 --repo solarity-services/RightTenantry`
  Read both before judging.

## Output contract

Write ONE valid JSON array to the output file named in your lens brief
(e.g. `.../r1/edge.json`). The file content must be ONLY the JSON array — no prose,
no markdown fencing, no preamble. Each element must match this schema exactly:

```json
{
  "source": "<the source value assigned to you in your lens brief>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```

- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, reply with ONE line (lens name + finding count) and stop.
  Do not fix anything. Do not comment on the PR.

## ACCURACY MANDATE — this is the most important instruction in this brief

NO claim you make will be taken at face value. Every finding you emit will be
independently re-verified against the actual codebase before it reaches the report.
Findings that fail verification are DISCARDED SILENTLY — they will not appear in the
report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume
  from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them,
  you have not verified the issue and the finding does not belong in your output. A
  finding without locatable evidence is a hallucination — drop it before it leaves
  your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you
  have not actually verified the issue. Either verify it and report it crisply, or do
  not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values
  accuracy over volume — an empty array is a fine and honest answer when nothing is
  wrong.
