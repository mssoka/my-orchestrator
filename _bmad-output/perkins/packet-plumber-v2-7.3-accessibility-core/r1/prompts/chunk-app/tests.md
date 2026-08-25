You are reviewing a code diff from PR #72 of solarity-services/Packet-Plumber (base branch v2; title "Story 7.3: accessibility core — colorblind palettes, reduced-motion, UI scaling, captions, settings panel"). This is REVIEW ROUND 1.

The diff was chunked by file group (big-diff policy). YOUR CHUNK: the `app/` tree (19 files — input intents, settings state, the settings panel, palette/pulse/seam render code, main loop wiring).
Read it FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/chunk-app.patch (1891 lines, unified format). These exact bytes are the review target.
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
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing in the worktree). Classify as FULL / PARTIAL / NONE coverage. Behaviour changes to trace: (1) three colorblind palette modes + palcheck oracle extension incl. the negative leg (a too-close pair must FAIL); (2) reduced-motion static pulse + crisis readability; (3) UI scaling x1.00/1.25/1.50 across HUD surfaces incl. hit-tests; (4) captions for every 7.2 alert kind; (5) settings panel open/navigate/activate on keyboard+controller+touch incl. chip+row taps; (6) settings persistence save/load/corrupt-file defaults; (7) 25/25 input-parity scenarios under every a11y mode; (8) the 5 new a11y goldens.

Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80-89% OR P2 gap
- note: P3 gap

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 >=90%, overall >=80%
- CONCERNS: P0 100%, P1 80-89%, overall >=80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": ""tests"",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/chunk-app/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".
