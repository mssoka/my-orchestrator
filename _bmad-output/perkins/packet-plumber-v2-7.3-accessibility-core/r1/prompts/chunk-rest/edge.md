You are reviewing a code diff from PR #72 of solarity-services/Packet-Plumber (base branch v2; title "Story 7.3: accessibility core — colorblind palettes, reduced-motion, UI scaling, captions, settings panel"). This is REVIEW ROUND 1.

The diff was chunked by file group (big-diff policy). YOUR CHUNK: everything except `app/` and `goldens/`: harness/ (palcheck oracle, parity, demo runner), tools/derive_a11y_palettes.py, data/palette.json, demos/a11y_*.dem, _bmad-output spec+canon-fold docs, _pr_body.md, .gitignore.
Read it FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/chunk-rest.patch (1355 lines, unified format). These exact bytes are the review target.
The PR also adds 20 new golden files (5 new a11y demos' T2 PNG frames + .t1 state-hash manifests + .log.bin replay logs) — binary/large, already byte-verified MECHANICALLY by the orchestrator (state hashes + replay logs byte-identical to juice.dem; no pre-existing golden touched). The surface summary is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/golden-manifest.txt — read it, do not re-derive it.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r1/project-context.md (Odin + raylib; ODN-1 pure core; ODN-10 integer-only sim; ODN-11 binary versioned save/log; arena discipline; intent-layer input parity doctrine).

--- SPEC / CONTEXT (read ALL of these) ---
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/spec/perkins-briefing-r1.md — the review briefing, incl. the LENS-GUARDS section (the never-color-alone invariant ODN-1; presentation-only discipline: core/ untouched, no LOG_VERSION, no catalog edits; what NOT to re-litigate — user rulings on the scaling knob, settings panel modal, reduced-motion static pulse, derivation methodology; what to flag for verification).
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/spec/job-briefing.md — the original job briefing (mission, deliverables, acceptance criteria).
- /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/spec/pr-body.md — the PR body with Decisions & rationale.
- /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r1/project-context.md — project conventions (ODN-1 pure core, ODN-10 integer-only sim, ODN-11 binary save/log, arena discipline, input parity doctrine).
- The reviewed worktree is rooted at /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r1 — you have read-only access to it. Verify the diff's claims against the actual files. Do NOT modify anything.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (files, settings load/save), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

Mission-relevant edge classes to trace especially: the settings binary (~/.pp-settings.bin) load path on corrupt/truncated/wrong-version/zero-length files; the UI-scale knob at each step (x1.00/x1.25/x1.50) on hit-tests vs draw rects; reduced-motion combined with each colorblind mode; the settings panel open during a crisis; palette mode absent tokens (partial tables fall back to canon base).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard; discard handled ones silently. No editorializing.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": ""edge"",
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

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/chunk-rest/edge.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens edge complete — N findings written".
