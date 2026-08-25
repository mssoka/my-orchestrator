You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1/project-context.md if you need project conventions. The repo is Packet-Plumber (Odin), a sim-core + raylib-view architecture: core/ is pure sim (no I/O, integer math, deterministic per-tick hashes), app/ is the raylib presentation layer, harness/ drives demos + goldens. Golden discipline is strict: goldens are blessed artifacts; shifts must trace to documented causes. Never modify any file in the worktree — read-only.

--- DIFF ---
The canonical diff under review is at: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/diff.patch
Read it. It is the complete diff for PR #44 (reviewed sha 23e1704eae1abed8cdcdb635d85dd4ec30d8aca2, base v2), saved by Perkins as the canonical bytes. You review exactly these bytes.

--- SPEC / CONTEXT ---
Spec file: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/spec-context.md — read it (job briefing + story 5.5 card + arch pins [E1]/[E2]/[E10]/[E27]/[E29] + lens-guards LOCKED list + implementer claims). Section 4 lens-guards lists LOCKED items — do not file findings on locked items. Section 5's implementer claims are claims to verify, not truth.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

This is an input-surface diff: trace press/release ordering, drag vs click thresholds, popover/tray hit-test overlap, selection state across mode transitions (Run/placing/Game_Over), demolish key gating, dead-selection guards after a junction batch, replay determinism of the fast-path. For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- Write ONLY the JSON array to this exact file path (use your file-writing tool): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.5-demolish-input/r1/edge.json
- Then reply with exactly one word: done
- Do not print the JSON in chat. Do not create or modify any other files. Do not fix anything.
- Empty array [] is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

The repository worktree (read-only for you) is at: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.5-demolish-input-r1
