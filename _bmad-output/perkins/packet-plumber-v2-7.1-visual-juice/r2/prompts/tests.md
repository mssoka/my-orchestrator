You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r2/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only (ODN-9/10); RNG owned by Run_State, cosmetic randomness from the app-owned second stream (ODN-15/ODN-9); arena discipline (ODN-18); events, not callbacks (ODN-14); no globals/singletons (ODN-13); errors are values; JSON is for catalogs only (fail-fast, embedded via `#load`); raylib immediate-mode inside BeginDrawing/EndDrawing; the golden harness renders with the software renderer (rlsw) so T2 pixels are bit-identical. THIS PR MUST NOT TOUCH `core/` OR `data/` AT ALL — it is a view-polish story (ODN-1 view purity).

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/lens-diff.patch (1945 lines, textual hunks only — PR #64 of solarity-services/Packet-Plumber, base branch `v2`, story 7.1 "visual juice"). These exact bytes are the review target — never re-fetch or regenerate the diff. ROUND CONTEXT: this is ROUND 2 — the diff contains the original 7.1 implementation PLUS the fix commit cb3bf2d ("7.1 Perkins r1: the B1 sprite-crop fix + the boot-camera fit + the review fold set") responding to Perkins r1 (2 blockers, 7 warnings, 9 notes). The PR's binary surface (76 golden PNGs, 9 sprite PNGs + sprites.json, style-gate artifacts, juice.t1/juice.log.bin) is summarized at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/golden-manifest.txt. Do NOT re-derive golden bytes, do NOT eyeball any PNG, and do NOT run the test suite (Perkins ran tools/ci-local.sh at the reviewed sha: 10/10 gates green) — review CODE and DOCS.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r2 — a checkout at exactly the reviewed sha (cb3bf2de25aaf7076652a41edccfdc7c116235c4). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins r2 briefing (the round guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/spec/perkins-briefing-r2.md
- Job briefing (the implementing minion's spec — hard requirements + acceptance list): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/spec/job-briefing.md
- Story 7.1 card (Given/When/Then contracts): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/spec/story-7.1.md
- Look-book canon INCLUDING the §6 amendment (§2 palette hexes are the exact 2D target): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/spec/look-book-v1.md
- Current PR body (the r2 claims under audit): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/spec/pr-body.md
- No GitHub issue exists for this job (verified r1; see spec/NOTE.md).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [PERKINS MECHANICAL STAMPS — r2 fix audit, ALREADY VERIFIED; do not re-derive, do not re-file]: (1) sprites.json content_bbox == PIL top-down alpha bbox for all 9 sprites EXACTLY; bbox-window alpha fill 76.3-93.3% (the correct regime; r1's broken crop held 24-38%); wall-band pixels (body-hex shade 0.62) + puck greys + LEDs now PRESENT in the juice goldens while the r1 golden had ZERO walls (negative control at dbed6a3); the palcheck play-marking canary is 0/22 rows inside the r1 (broken) window vs 22/22 in the r2 window — the gate provably bites a B1-class crop. (2) Boot order: view_compute (main.odin:269, static balance dims) now precedes start_run (274) whose camera_set_fit reads valid world dims, then snaps; camera_update derives from the snapped state — B2's chain holds. (3) The 76-PNG re-bless: all 76 changed vs r1, juice.t1/juice.log.bin byte-identical to r1, ZERO non-juice .t1/.log.bin in the diff (T1/replay identity holds at file level). (4) tools/ci-local.sh at the reviewed sha: 10/10 green (Perkins-run, r2/ci-local.log). You MAY challenge a stamp only with concrete quoted evidence.
- [CARRY-FORWARD SET — already tracked from r1, do NOT re-file]: crisis card_w/line_h constants duplicated (crisis.odin); doorstep kx/ky math duplicated at two view.odin sites; banner_y rule duplicated app<->harness (harness copy pre-existing); camera_update restates view_compute's fit formula; parity-hook pin for banner/SLA clicks deferred to 7.3; sprites.json loader failure-mode tests deferred. These are recorded; new findings only.
- [VISION CAVEAT — this round runs WITHOUT native vision]: pixel claims verified MECHANICALLY only. Aesthetic judgment calls are DEFERRED to a kimi-vision re-check — NOT findings, do not block on them, do not fake them.
- [THE HARD BLOCKER CLASSES]: (a) View purity — the View reads ONLY snapshots; no new snapshot fields without documented reason; replay byte-identical [E10]. (b) Canon application, not redesign: §2 palette hexes + §6 amendment (top-down buildings, roof carries the read, painted shading + flat contact shadows allowed); never-color-alone (shape/icon/outline companions). (c) Chrome idiom matches the 5.5 popover (translucent warm cards + hairline, render-package-owned layout, single-source rects shared with hit-tests). (d) Camera-fit: wider/taller reveals more map. (e) Goldens: deliberate re-blesses only, documented — accept the mechanical stamps.
- [NO SCOPE CREEP]: no a11y MODES (7.3), no audio (7.2), no mechanics/balance changes, no core/snapshot changes, no asset regeneration beyond gen_sprites.py. A violation = blocker.
- [CI note]: GitHub Actions is org-billing-blocked + a GitHub incident — NOT a signal. The local suite is ground truth (10/10 green, Perkins-run).
- [What NOT to re-litigate]: the user-approved style-gate verdicts (top-down, painted shading, contact shadows, focus-zoom camera model — the two-tone roof + contact shadow IS the approved design); the 5.5 popover chrome; #62's golden fold; the look-book canon itself (final — apply, don't judge); the glm-5.3 fallback (operational, not canon); r1's held-clean ground (canon application, ODN-1 view purity, chrome idiom, never-color-alone, golden discipline — all verified mechanically in r1).
- The base is `v2`. Files NOT in the diff are read-only context.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check: the NEW palcheck gate (what does it actually pin — and what does it NOT: which §2 hexes are gated, is the zoomed lane read real, could it pass with a broken sprite crop of a DIFFERENT sprite); the on_cancel camera-home exit (any committed test?); the boot-order fix (pinned anywhere?); the doorstep 5x5 fan; the camera ease; note which surfaces remain goldens-blind (app-layer). The r1 advisory gate said FAIL (P0 camera coverage) reclassified to warning by charter; the PR claims the palcheck gate closes W2 — judge whether it closes the RIGHT gap. Test level mix (unit/integration/E2E): flag mismatches.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80%; CONCERNS: P0 100%, P1 80–89%, overall ≥80%; FAIL: P0 <100%, or P1 <80%, or overall <80%. Your `source` value is "tests".

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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r2/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".