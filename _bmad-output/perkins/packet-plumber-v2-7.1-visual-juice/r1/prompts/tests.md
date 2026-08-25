You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r1/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only (ODN-9/10); RNG owned by Run_State, cosmetic randomness from the app-owned second stream (ODN-15/ODN-9); arena discipline (ODN-18); events, not callbacks (ODN-14); no globals/singletons (ODN-13); errors are values; JSON is for catalogs only (fail-fast, embedded via `#load`); raylib immediate-mode inside BeginDrawing/EndDrawing; the golden harness renders with the software renderer (rlsw) so T2 pixels are bit-identical. THIS PR MUST NOT TOUCH `core/` OR `data/` AT ALL — it is a view-polish story (ODN-1 view purity).

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/lens-diff.patch (1504 lines, textual hunks only — PR #64 of solarity-services/Packet-Plumber, base branch `v2` @ post-#62/#63 merge head, story 7.1 "visual juice": the lavish-gated top-down sprite direction, tier-band pipes with inset QoS lanes, focus-zoom camera, filter/focus + alerts-as-nav chrome, doorstep queues, the new juice T2 golden + 74 deliberate re-blesses). These exact bytes are the review target — never re-fetch or regenerate the diff. The PR's binary surface (76 golden PNGs, 9 sprite PNGs, 19 style-gate PNGs, the new juice.t1/juice.log.bin manifests) is summarized — with Perkins' MECHANICAL byte/pixel verification stamps — at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/golden-manifest.txt. Do NOT re-derive golden bytes, do NOT eyeball any PNG, and do NOT run the test suite (Perkins is running tools/ci-local.sh at the reviewed sha; the minion reports 9/9) — review CODE and DOCS.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r1 — a checkout at exactly the reviewed sha (dbed6a3a38385bde63eef0e34cbf7f997b519ed1). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins briefing (the r1 guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/spec/perkins-briefing-r1.md
- Job briefing (the implementing minion's spec — hard requirements + acceptance list): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/spec/job-briefing.md
- Story 7.1 card (Given/When/Then + edge-case contracts are CONTRACTS, not guidance): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/spec/story-7.1.md
- Look-book canon INCLUDING the §6 amendment this PR adds (§2 palette hexes are the exact 2D target): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/spec/look-book-v1.md
- PR body (the claims under audit — canon citations, re-bless list, chrome/camera notes, renderer findings): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/spec/pr-body.md
- No GitHub issue exists for this job (verified; see spec/NOTE.md).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [VISION CAVEAT — this round runs WITHOUT native vision]: pixel claims are verified MECHANICALLY only (byte/hash comparisons, pixel-diff tooling — already stamped in golden-manifest.txt: the re-bless set == the PR's claimed 74+2 list exactly; sampled old-vs-new pixel diffs are 8.0–9.7% frame-wide (99% vertical spread) matching the "~7–9% frame-wide but bounded" claim; NO existing .t1/.log.bin appears in the diff (only NEW juice ones) so the replay/T1 byte-identity surface holds at file level; all new PNGs valid). Do NOT re-derive these. Aesthetic judgment calls (is it pretty, does the style feel right) are DEFERRED to a kimi-vision re-check — NOT findings, do not block on them, do not fake them.
- [THE ONE HARD BLOCKER CLASS — canon application + view purity]: (a) the View reads ONLY snapshots — polish must never perturb the sim; no new snapshot fields without documented reason; replay byte-identical [E10]. (b) Canon application, not redesign: look-book §2 palette hexes + §6 amendment (TRUE TOP-DOWN buildings — roof carries the read; flat solid colors; the §6 refinement ALLOWS painted shading + flat contact shadows, superseding the earlier no-drop-shadows line); node health states readable; never-color-alone (shape/icon/outline companions). (c) Chrome idiom must MATCH the 5.5 demolish popover (translucent warm cards + hairline border, layout owned by the render package, single-source rects shared with the app's hit-tests) — not a second language. (d) Camera-fit: wider/taller screens reveal more map. (e) Goldens: new T2 juiced golden + re-blesses ONLY where juice provably changes pixels, each listed with before/after — mechanically verified, accept the stamp.
- [NO SCOPE CREEP]: no a11y MODES (7.3), no audio (7.2), no mechanics/balance changes, no core/snapshot changes, no asset regeneration beyond the committed gen_sprites.py pipeline (the look-book is final). A violation = blocker.
- [CI note]: GitHub Actions on this PR is org-billing-blocked + a GitHub incident — NOT a signal. The local suite is ground truth (Perkins runs it; minion reports 9/9).
- [Lane awareness]: base is v2 with #62 (deliberate 29-frame golden fold) + #63 (5.10 narrow-access + its 88-file re-bless) already merged. Verify this branch builds on that ground cleanly (no golden collision: e.g. a golden claimed re-blessed here that #63 already moved).
- [What NOT to re-litigate]: the user-approved style-gate verdicts (Phase A — lavish-approved, including top-down, painted shading, contact shadows, focus-zoom camera model); the 5.5 popover chrome (approved + merged); #62's golden fold; the 5.9/5.10 catalog work; the look-book canon itself (final — apply, don't judge); the kimi→glm vision fallback ruling (operational, not canon).
- The base is `v2`. Files NOT in the diff are read-only context.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check (adapted to this repo's testing model: `odin test` unit tests for core, the golden-image harness `harness/` for scripted T1 determinism + T2 visual pins, tools/ci-local.sh 9 gates): the NEW view behaviors — focus-zoom camera easing (2.3x/2.6x, the 1.5x lane-detail threshold, resize-during-ease), class-focus ghosting, alerts-as-nav banner click, SLA row click focus, doorstep queue fan, lane-stripe LOD — which of these are pinned by COMMITTED automated verification vs verified only by a disposable scratch replica + programmatic pixel-scan that was NOT committed (the PR admits this for hint-vs-full lane stripes, class-focus ghosting, sprite presence — the 5.3 lesson says goldens cannot see app-layer surfaces)? Is the new juice.dem T2 golden actually registered in the harness and does ci-local gate it (the new-golden registration is IN the diff — harness/goldens.odin)? Does anything pin the sprites.json loader's failure modes (missing/invalid sidecar)? Does anything pin never-color-alone mechanically (the contract is baseline for 7.3)? Weigh honestly: view-only code in a golden-harness repo — what CAN be pinned vs what reasonably can't; classify severity by the repo's own bar (the 5.3 lesson made app-layer verification explicit — was that bar met or dodged here?).

Test level mix (unit/golden/manual): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%

Your `source` value is "tests".

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r1/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".
