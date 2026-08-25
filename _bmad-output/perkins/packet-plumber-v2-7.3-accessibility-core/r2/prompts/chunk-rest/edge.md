You are reviewing a code diff from PR #72 of solarity-services/Packet-Plumber (base branch v2; title "Story 7.3: accessibility core — colorblind palettes, reduced-motion, UI scaling, captions, settings panel"). This is REVIEW ROUND 2 (a FIX-AUDIT round): round 1 filed 6 blockers at sha 3fa0703; the implementer reworked and pushed sha 217f6a8ec03d7b75914fd005f15bc8de4e248ec8 (the reviewed sha). Perkins (the orchestrator) has ALREADY audited the 6 r1 blocker fixes personally — your job is NEW findings in the diff, not re-arguing the r1 fixes or their design.

The diff was chunked by file group (big-diff policy). YOUR CHUNK: everything outside `app/` and `goldens/` (21 files — harness palcheck/parity/goldens/demo/run + the a11y oracle test, tools/ci-local.sh + the palette derivation script, data/palette.json modes tables, the 5 a11y demo scripts, the spec/stories docs, _pr_body.md, .gitignore)
Read it FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r2/chunk-rest.patch (1439 lines, unified format). These exact bytes are the review target.
The PR also adds 20 new golden files (5 new a11y demos' T2 PNG frames + .t1 state-hash manifests + .log.bin replay logs) — binary/large, already byte-verified MECHANICALLY by the orchestrator (state hashes + replay logs byte-identical to juice.dem; no pre-existing golden touched). The surface summary is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r2/golden-manifest.txt — read it, do not re-derive it.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r2/project-context.md (Odin + raylib; ODN-1 pure core; ODN-10 integer-only sim; ODN-11 binary versioned save/log; arena discipline; intent-layer input parity doctrine).

--- SPEC / CONTEXT (read ALL of these) ---
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r2/spec/perkins-briefing-r2.md — the round-2 review briefing, incl. the lens-guards (what Perkins already verified about the r1 fixes) and the standing orders (what NOT to re-litigate: the r1 6-blocker fixes themselves, the user rulings — the ×1.00/1.25/1.50 knob steps, the modal pause-on-open panel, reduced-motion static pulse, Machado 2009 derivation, binary-over-JSON settings — and the applied canon: 7.1 light-canvas, D9, wire-aesthetics).
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r2/spec/job-briefing.md — the original job briefing (mission, deliverables, acceptance criteria).
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r2/spec/pr-body.md — the PR body incl. the "r1 → r2 rework" section (each fix + its claimed proof).
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/consolidated.json — the ROUND-1 findings (6 blockers + 8 warnings + 18 notes). Treat it as carry-forward context: the 6 blockers were reworked this round (Perkins audited); the warnings/notes were NOT required to be fixed — if you re-derive one of them independently you may file it, marked "still present since round 1" in the title.
- The reviewed worktree is rooted at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r2 — you have read-only access to it. Verify the diff's claims against the actual files. Do NOT modify anything. Do NOT run builds or tests (the orchestrator owns the mechanical gates).

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate. Pay special attention to the r1→r2 rework hunks (settings cycle helpers, the crisis_card_width clamp, the QoS rect scaling, the phase-1 key collection changes) — new code paths born in r2 deserve the closest tracing.

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
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract: ONLY the JSON array written to the file below. `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble — beware raw control characters inside strings; escape them properly) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r2/chunk-rest/edge.json
Then stop.
