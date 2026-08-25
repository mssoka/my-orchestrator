You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the reviewed worktree.

--- PROJECT CONVENTIONS ---
Read AGENTS.md at the repository root. It is the project's agent contract: C++-first (Blueprints only where unavoidable, documented); determinism spine discipline — all state-affecting sim math is integer (ODN-10), the sim owns its PRNG (PP::FRng, ODN-9; never FMath::Rand/FRandomStream in sim state paths), no TMap/TSet iteration in sim state paths, serialization is explicit little-endian field-by-field (ODN-11, never raw memcpy of structs), every spine change re-runs tests/build/spine-check + the UE-side PacketPlumber.* automation tests, replay-equality (same seed+action log → byte-identical state hash); fixed 20 Hz tick (ODN-2); golden discipline (never re-bless to dodge a mismatch); CI has engine-free gates (format/spine/static — must be green now) and engine-gated gates (build/headless/probe/golden — activate when UE 5.8 is installed; the engine is NOT installed yet, that is a documented manual user step, NOT a defect).

--- DIFF ---
The canonical diff is saved at /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-bootstrap/r1/diff.patch (unified diff, 46 files, 2872 diff lines — the PR is a NEW repo, so all files are additions). Read it from that exact file. These are the exact bytes under review; never regenerate or re-fetch the diff.

--- SPEC / CONTEXT ---
Read these spec documents, in order:
1. /Users/moses/code/_bmad-output/briefings/packet-plumber-ue-bootstrap.md — the original job briefing (mission, deliverables, acceptance, canon: the Odin GDD + routing canon [RR] + determinism rules [ODN-*] carry over as requirements; do NOT re-decide design).
2. /Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-ue-bootstrap-r1.md — the review briefing (r1 lens-guards: the ONE hard blocker class — the determinism spine port must be carried as REQUIREMENTS — what to verify, what NOT to re-litigate: the user's 4 lavish rulings, the game design, the engine choice).
3. /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-bootstrap/r1/pr.json — PR title/body (the "Decisions & rationale" D1–D5 and the staged engine-gated acceptance items).

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.
--- OUTPUT ---
Write ONE valid JSON array to the file /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-bootstrap/r1/edge.json (full absolute path stated here — do not derive it, do not write anywhere else), then stop. Each element must match this schema exactly:
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
- The file /Users/moses/code/_bmad-output/perkins/packet-plumber-ue-bootstrap/r1/edge.json must contain ONLY the JSON array. No prose, no markdown fencing, no preamble. Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
