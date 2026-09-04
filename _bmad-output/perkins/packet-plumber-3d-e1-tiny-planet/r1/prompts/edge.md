You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- INPUTS (read these exact files) ---
- DIFF (canonical — review exactly these bytes; read it in full, paging with offset/limit): /Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e1-tiny-planet/r1/diff.patch
- WORKTREE (checkout at exactly the reviewed state; every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber-3d/perkins-e1-r1
- SPEC 1 (job briefing): /Users/moses/code/_bmad-output/briefings/packet-plumber-3d-e1-tiny-planet.md
- SPEC 2 (merged epic — section "E1 — Tiny Planet & Connect Verb"; its stories E1.1–E1.5 and test contracts ARE the acceptance criteria): /Users/moses/.herdr/worktrees/packet-plumber-3d/perkins-e1-r1/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/epics.md
- CONTEXT (GDD — art-direction and camera sections, referenced by the briefing): /Users/moses/.herdr/worktrees/packet-plumber-3d/perkins-e1-r1/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-3d-2026-09-04/gdd.md

--- PROJECT CONVENTIONS ---
none

Read the DIFF file first in full, then the spec files, then verify claims against the WORKTREE as your lens requires.

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

FILE-OUTPUT CONTRACT (headless): write ONLY your final JSON array to this exact path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-3d-e1-tiny-planet/r1/edge.json
Then stop. Do not print the JSON to chat; the file is the deliverable.

Output contract:
- Return ONLY the JSON array in the file. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
