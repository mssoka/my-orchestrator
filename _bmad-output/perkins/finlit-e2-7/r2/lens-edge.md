You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Godot 4.7.1 / GDScript children's financial-literacy game ("finlit") at /Users/moses/code/kids-finlit-game. Pure rules live in RefCounted modules (FinLitTouchTargets); UI logic in game/scripts/street.gd. Tests are bare-runner SceneTree scripts: godot --headless --path game --script res://tests/test_economy.gd (currently 295 checks / 0 failures). The touch-proxy is an invisible Control that enlarges a small target's hit area to a role floor; the dominant bottom-center button is rule-driven.

--- DIFF ---
Read the file /Users/moses/code/_bmad-output/perkins/finlit-e2-7/r2/diff.patch — the canonical diff for PR #11 ("feat: e2-7 touch-target rules (A29 minute-one working rules)", base main). Review exactly these bytes. Never re-fetch or regenerate the diff.

--- SPEC / CONTEXT ---
- /Users/moses/code/_bmad-output/briefings/finlit-e2-7.md (the job briefing — acceptance criteria)
- /Users/moses/.herdr/worktrees/kids-finlit-game/perkins-e2-7-r2/_bmad-output/implementation-artifacts/stories/e2-7-touch-target-rules.md (the story)

--- WORKTREE (read-only verification) ---
/Users/moses/.herdr/worktrees/kids-finlit-game/perkins-e2-7-r2 — verify any claim against the real files here. Do not modify anything.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE OUTPUT CONTRACT: Write ONLY your JSON array to /Users/moses/code/_bmad-output/perkins/finlit-e2-7/r2/edge.json (no prose, no markdown fencing, no preamble in the file). Then stop. Do not derive this path — it is given.
