You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.10-narrow-access-r1/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); events, not callbacks (ODN-14); determinism is the project spine; catalogs are DATA, single-source, fail-fast at load (ODN-5) — balance values are playtest-tunable data, never code.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/lens-diff.patch (514 lines, unified format, PR #63 of solarity-services/Packet-Plumber, base branch v2 @ 1d7f442, story 5.10 "narrow as the residential access tier" — narrow capacity_units 5 -> 10). These exact bytes are the review target — never re-fetch or regenerate the diff. The PR also re-blessed 88 golden files; their summarized surface is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/golden-manifest.txt — Perkins has ALREADY byte-verified the re-bless mechanically (all 31 .log.bin differ ONLY at bytes 17..24, the 8-byte catalog_hash field 7dbddfc189670ba0 -> 66c4324a06058860; all 33 .t1 manifests changed only the catalog_hash line + per-tick hash lines, counts == the ticks header; boot's era-0 tick-1 with the old hash spliced at bytes 33..40 re-hashes to the OLD golden exactly — fold-only byte-proven; the PNG set is exactly the 15 cause-documented frames, all in the 6 narrow-pipe demos). Do NOT re-derive golden bytes and do NOT run the test suite (Perkins ran tools/ci-local.sh: 9/9 gates green at the reviewed sha, incl. the golden harness T1/T2/replay gate) — review CODE.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.10-narrow-access-r1 — a checkout at exactly the reviewed sha (421a1a36704654cc14d6dc26cb10031722a49c9d). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins briefing (the r1 guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/spec/perkins-briefing-r1.md
- Job briefing (the implementing minion's spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/spec/job-briefing.md
- Story 5.10 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/spec/stories-v2.md — the section "### Story 5.10 — Narrow as residential access (the access tier)" at line 751 (its Given/When/Then + hard requirements are CONTRACTS, not guidance).
- Design spec (the traffic model): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/spec/spec-traffic-model.md — Thread 1 "Narrow as residential access" at line 76.
- Architecture canon: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/spec/odin-architecture-v1.md — ODN-5 catalog single-source + fail-fast, ODN-10 integer-only state paths, E10 replay byte-identity, the E-contract glossary.

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [THE ONE HARD BLOCKER CLASS — the tier change is EXACTLY what the card pins, nothing more]: narrow `capacity_units` 5 -> 10 in `data/pipe_tiers.json` (catalogs [ODN-5], data-driven). Headroom math (Perkins-verified from live data): cap_fraction_permille 500 x residential throughput 5 = 2.5 u/s; post 10/2.5 = 4.0x (4000 permille, the top of the card's ~3-4x band), pre 5/2.5 = 2.0x. UNTOUCHED (verify by diff, not trust): the routing-cost ladder (20/10/5), span rules (clean_span 8 / max_span 10; `span_exceeds_tier` contract), every other tier (standard 15, wide 40), cost_per_tile (5/12/30), the 2026-08-13 capacity-cost ruling. NO cost/span/other-tier changes, NO new terminal types (5.11), NO group bias (5.12), NO UI, no LOG_VERSION bump (no new commands). A violation of the untouched list = a blocker.
- [The honest-signal pins must BITE (non-vacuous)]: (a) W10 re-pinned to NARROW access legs — a single residential sourcing at its cap over two narrow hops shows ZERO drops at its own access lane, no E9 shed, transit <= email's 500 ms tolerance, delivered > 0, sourcing >= ~50 emails (the 5.9 vacuous-pin discipline); (b) the NEW test_w11_aggregation_congests_shared_link — 6+6 homes each on its OWN narrow drop aggregate onto ONE shared standard uplink; drops > 0 at the shared bundle, ZERO at any narrow access bundle, both classes deliver. A vacuous or trivially-true pin is blocker-class.
- [core/flow.odin hunk is COMMENT-ONLY] — verify no behavior change hides in it.
- [Re-bless discipline — Perkins-verified mechanically]: do not re-derive golden bytes. Flag only code paths that could hide semantic drift in a FUTURE re-bless.
- [Re-pins are structural, not golden re-blesses]: crisis/health/sla collateral re-pins (first_stream_drop bundle 0->2, health grace 380->200 in-test, exact tick windows re-read) are cause-commented and must preserve test INTENT — flag a re-pin that silently WEAKENS a test's contract (e.g. an assertion that no longer distinguishes the behavior it was built to pin).
- [Lane awareness]: the sibling 7.1-visual-juice (VIEW lane) re-blesses T2 frames on top of this branch's PRE-juice frames. Flag any finding whose fix would force extra golden churn beyond the documented set.
- [What NOT to re-litigate]: the spec-traffic-model Section B ruling; 5.9's accumulator design (just approved); the 2026-08-13 capacity-cost ruling; the 4.1 honest-traffic doctrine; the 7.1 style-gate canon; prior approved rounds' ground; the health E16 "drain RATE, never grace values" contract.
- The base is `v2`. Files NOT in the diff are read-only context.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Context: this is an offline deterministic game (pure sim core + raylib view + a file-based golden harness); the diff is a data value change, comment edits, and test fixtures. Attack surface is minimal — judge accordingly, but check the real boundaries present: catalog JSON load (fail-fast contract), file paths used by tests/harness, any format-string or allocation edge in the new test code. Your `source` value is "security".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
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

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.10-narrow-access/r1/security.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens security complete — N findings written".
