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
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria (the job briefing's Deliverables 1-6 and Acceptance 1-3)
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

THE HARD GUARDS (from the review briefing — verify each, a violation is a BLOCKER):
1. never-color-alone [ODN-1]: every state/machine must be readable WITHOUT color (icon+shape for packets, icon+outline for node states), and the a11y palette modes must restyle EVERY view surface (map tokens, lanes, ghost, pipe tiers, route marks, packet class colors) with the class-color remap at DRAW time. A surface that stays color-only under deutan/protan/tritan = blocker.
2. Presentation-only discipline: the diff must be view-lane only — core/ untouched, no LOG_VERSION, no catalog (packet_types.json) edits; the packet class colors must remap at draw time, never in the catalog.
3. Input parity: the settings panel must be reachable/operable on keyboard + controller + touch (the briefing flags chip+row taps for verification).
4. Reduced-motion: flagged effects (the PULSE16 ring pulse + crisis-outline swell) must go static, and crisis telegraphy must survive on static channels.
5. Settings persistence: versioned binary, checksum-guarded, defaults on failure.
Do NOT re-litigate user rulings (the x1.00/1.25/1.50 knob steps, the modal pause-on-open panel, static-pulse choice, Machado 2009 derivation methodology, binary-over-JSON settings) — those are settled; only verify the code matches them.

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": ""acceptance"",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1/chunk-rest/acceptance.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens acceptance complete — N findings written".
