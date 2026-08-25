You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r4/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only (ODN-9/10); RNG owned by Run_State, cosmetic randomness from the app-owned second stream (ODN-15/ODN-9); arena discipline (ODN-18); events, not callbacks (ODN-14); no globals/singletons (ODN-13); errors are values; JSON is for catalogs only (fail-fast, embedded via `#load`); raylib immediate-mode inside BeginDrawing/EndDrawing; the golden harness renders with the software renderer (rlsw) so T2 pixels are bit-identical. THIS PR'S OWN SURFACE (diff vs base v2) MUST NOT TOUCH `core/` OR `data/` — it is a view-polish story (ODN-1 view purity). NOTE: the branch CONTAINS #63's core/data changes (flow, pipe_tiers, core tests) — that is #63's own approved content, part of base v2, NOT this PR's authored surface; judge only the 7.1-authored delta.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/lens-diff.patch (2058 lines, textual hunks only — PR #64 of solarity-services/Packet-Plumber, base branch `v2`, story 7.1 "visual juice"). These exact bytes are the review target — never re-fetch or regenerate the diff. ROUND CONTEXT: this is ROUND 4, a fold-delta verification round. Round 3 APPROVED sha 5c482df (0 blockers). The head d9db462 = 5c482df PLUS the implementing minion's held-back r2 non-blocking fold set, pushed by choice after approval. The EXACT round delta (git-verified by the dispatching orchestrator: 7 files, +42/-23) is saved at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/fold-delta.patch (199 lines — read it too; it is the round's primary review surface). Declared fold set (commit d9db462 message, matches the delta exactly): W-A route-glow halo via band_width (assist.odin, both sites) · W-C click=focus camera re-home (new on_node_selected hook + effect_pipe_selected re-target; last_sel deliberately untouched on nav paths) · W-B palcheck consts trimmed to roofs + header fixed · N-A draw_packets header · N-B draw_bundles fiber comment · N-G on_cancel after executor mutations · N-J ci-local gate-count strings. The PR's binary surface (105 files: 74 re-blessed + 2 new juice golden PNGs, 9 sprite PNGs, style-gate artifacts, juice.t1/juice.log.bin) is summarized at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/golden-manifest.txt — byte-identical to the r3 set (zero golden churn in the fold). Do NOT re-derive golden bytes, do NOT eyeball any PNG, and do NOT run the test suite (Perkins ran tools/ci-local.sh at the reviewed sha: 10/10 gates green, 32/32 demos — /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/ci-local.log) — review CODE and DOCS.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r4 — a checkout at exactly the reviewed sha (d9db462a7cb7bedaa57ca062c5b3b630469b11b6). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins r4 briefing (the round guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/spec/perkins-briefing-r4.md
- Job briefing (the implementing minion's spec — hard requirements + acceptance list): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/spec/job-briefing.md
- Story 7.1 card (Given/When/Then contracts): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/spec/story-7.1.md
- Look-book canon INCLUDING the §6 amendment (§2 palette hexes are the exact 2D target): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/spec/look-book-v1.md
- Current PR body (the claims under audit — NOTE: updated after r3 with a Review-trail section): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/spec/pr-body.md
- Fold commit message (the delta's declaration): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/spec/fold-commit-msg.txt
- No GitHub issue exists for this job (verified r1; see spec/NOTE.md).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [PERKINS MECHANICAL STAMPS — r4, ALREADY VERIFIED; do not re-derive, do not re-file]: (1) The fold delta is EXACTLY the declared set: git diff 5c482df..d9db462 = 7 files, +42/-23 (app/input/exec.odin, app/input/input.odin, app/main.odin, app/render/assist.odin, app/render/view.odin, harness/palcheck.odin, tools/ci-local.sh) — no other changes, no golden churn (golden manifest byte-identical to r3's). (2) #63 containment holds: merge-base(HEAD, v2) = ebd02cb = v2 tip; the diff vs v2 is the 7.1 work only, ZERO core/ or data/ files in the authored surface. (3) tools/ci-local.sh --mac Perkins-run at d9db462: 10/10 gates GREEN — gate 4 golden harness 32/32 demos (the fold introduced ZERO golden drift — same goldens as r3, still green), gate 5 palcheck all-green incl. the B1 canary (host play-marking 92px), gates 1-3/6-10 green. (4) T1/replay byte-identity: the fold touches no .t1/.log.bin/manifest files; gate 9 green (live == replay). (5) r1 B1/B2 held: all 9 sprites' content_bbox == PIL top-down alpha bbox EXACTLY (re-verified r4; sidecar stores xywh, PIL reports xyxy — equivalent); view_compute (main.odin:269) precedes start_run (:274). (6) Folds code-verified: W-A — committed-bundle glow halo now band_width(tier,count)+6*scale (assist.odin:425), IDENTICAL to the selection-halo formula (view.odin:804); candidate halo width*2.2+6*scale == band_width(tier, count=1) (assist.odin:442) — the missed 5th consumer now uniform. W-B — HOUSE_BODIES/HOST_BODY deleted, zero references remain repo-wide; header now roofs-accurate. W-C — exec.odin:418 fires on_node_selected on EVERY junction click; effect_pipe_selected (main.odin:811) and new effect_node_selected (:819) call camera_set_selection unconditionally (which updates last_sel_* + camera targets); banner-nav divergence documented in-code (main.odin:688-690, 1178-1180). N-G — on_cancel now fires AFTER the executor mutations + swallow latch (exec.odin:48-64). (7) The PR body was updated post-r3: "10/10 gates" + a Review-trail section documenting the #63 re-bless cause chain and the fold set (this resolves r3's W-3); the body STILL claims the juice golden shows "the health meter" (line 65) while the demo runs health OFF (r2 N-I half — carries). (8) PR state: mergeable=MERGEABLE, headRefOid == the reviewed sha. You MAY challenge a stamp only with concrete quoted evidence.
- [CARRY-FORWARD SET — tracked findings still present, carried to the NEXT story by the minion's DECLARED choice (recorded in the r4 briefing: "carry to the next story by the minion's declared choice"); do NOT re-file them, do NOT block on them]: r3: W-1 SLA-row/tray 4px press-order overlap · W2 press/release chrome straddle · W-4 selection-halo zero coverage · W-5 sprites.json three unenforced homes · N-1 palcheck count_exact double-scan · N-2 banner-rect fabricated one-row crisis · N-3 sprite_target_w stale doc name · N-4 juice.dem read error swallowed · N-5 palcheck third camera-transform copy · N-6 file-scope fails mutable · N-7 bbox res field ignored · N-8 gate-5 label drift · N-9 lane standard/best-effort unpinned · N-10 B1 invariant no automated pin · N-11 PR-body click-coverage overclaim. r2 leftovers: W-D palcheck normalize dup · W-E/W-F/W-G/W-H/W-I coverage cluster (focus-zoom camera, on_cancel exit, boot-order fit, class-ghosting — unpinned) · W-K puck canaries aggregate · W-L advisory gate CONCERNS · N-C gen_sprites CREAM/DC_VENT unused · N-D banner-focus empty-map click no exit · N-E SLA 2px (subsumed by r3 W-1) · N-F look-book "targeting main" · N-H palcheck discards catalog bools · N-K "health on" substring key · N-L chrome geometry two homes · N-M doorstep 25-slot no-wrap unpinned · r1 leftovers (crisis card_w/line_h dup, doorstep kx/ky dup, banner_y dup app+harness, camera_update restates fit formula, parity-hook pin deferred to 7.3). A NEW defect in the same code, or a fold that made one of these WORSE, IS a new finding — file those.
- [VISION CAVEAT — this round runs WITHOUT native vision]: pixel claims verified MECHANICALLY only. Aesthetic judgment calls are DEFERRED to a kimi-vision re-check — NOT findings, do not block on them, do not fake them.
- [THE HARD BLOCKER CLASSES]: (a) View purity — the View reads ONLY snapshots; no new snapshot fields without documented reason; replay byte-identical [E10]. (b) Canon application, not redesign: §2 palette hexes + §6 amendment; never-color-alone (shape/icon/outline companions). (c) Chrome idiom matches the 5.5 popover. (d) Camera-fit: wider/taller reveals more map. (e) Goldens: deliberate re-blesses only, documented — accept the mechanical stamps. For THIS round add: (f) fold integrity — the delta must be exactly the declared set, each fold must land correctly, and the r3-APPROVED core must be untouched (stamped; challenge only with quoted evidence).
- [NO SCOPE CREEP]: no a11y MODES (7.3), no audio implementation (7.2 — audio DEMOS are pre-existing base content), no mechanics/balance changes, no core/snapshot changes in the 7.1-authored surface, no asset regeneration beyond gen_sprites.py. A violation = blocker. (#63's core/data content is BASE, not this PR's authored surface.)
- [CI note]: GitHub Actions on #64 is org-billing-blocked — NOT a signal. The local suite is ground truth (10/10 green, Perkins-run at the reviewed sha).
- [What NOT to re-litigate]: the r3 APPROVED verdict (merged tree green, B1/B2 held); the user-approved style-gate verdicts (top-down, painted shading, contact shadows, focus-zoom camera model); the 5.5 popover chrome; the look-book canon itself (final — apply, don't judge); the glm-5.3 fallback (operational, not canon); r1/r2/r3 held-clean ground (canon application, ODN-1 view purity, chrome idiom, never-color-alone, golden discipline — mechanically verified); #63's own approved content; the fallback-model caveat (operational).
- The base is `v2`. Files NOT in the diff are read-only context.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check — ROUND 4 EMPHASIS, the fold's behavior changes and their pins: (1) W-A halo change: MECHANICAL FACT — gate 4 was green at r3 (old formula) AND at r4 (new formula) against the SAME golden bytes, therefore NO golden frame pins the glow halo; the folded change is visually unpinned (same family as the carried W-4 selection-halo gap — if you file it, it is a NEW gap for the glow halo specifically, not a re-file of W-4). (2) W-C camera re-home: the fold added NO tests; palcheck's banner-rect check and goldens run with sel=-1; the click-re-home path (on_node_selected/effect_pipe_selected → camera_set_selection) runs in NO committed artifact — classify. (3) N-G on_cancel ordering: pinned anywhere (parity/input tests that assert effect ordering)? (4) The carried W-L advisory gate said CONCERNS — refresh the gate ONLY if the fold materially changed the coverage picture (it adds two unpinned behavior changes; judge whether that moves the gate). Do NOT re-file the carried W-E..W-I cluster, W-4, W-K, N-9, N-10, N-11 — they are recorded. Your value is the FOLD's deltas, not re-derivation. Test level mix (unit/integration/E2E): flag mismatches as findings.

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
  "source": "tests",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r4/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".
