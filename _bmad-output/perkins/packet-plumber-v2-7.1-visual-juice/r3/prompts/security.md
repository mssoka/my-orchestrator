You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r3/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only (ODN-9/10); RNG owned by Run_State, cosmetic randomness from the app-owned second stream (ODN-15/ODN-9); arena discipline (ODN-18); events, not callbacks (ODN-14); no globals/singletons (ODN-13); errors are values; JSON is for catalogs only (fail-fast, embedded via `#load`); raylib immediate-mode inside BeginDrawing/EndDrawing; the golden harness renders with the software renderer (rlsw) so T2 pixels are bit-identical. THIS PR'S OWN SURFACE (diff vs base v2) MUST NOT TOUCH `core/` OR `data/` — it is a view-polish story (ODN-1 view purity). NOTE: the rebased branch CONTAINS #63's core/data changes (flow, pipe_tiers, core tests) — that is #63's own approved content, now part of base v2, NOT part of this PR's authored surface; judge only the 7.1-authored delta (the diff you are given).

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/lens-diff.patch (1944 lines, textual hunks only — PR #64 of solarity-services/Packet-Plumber, base branch `v2`, story 7.1 "visual juice"). These exact bytes are the review target — never re-fetch or regenerate the diff. ROUND CONTEXT: this is ROUND 3. The head 5c482df is the REBASE of the 7.1 work onto v2 tip ebd02cb (#63 "narrow capacity_units 5→10" landed mid-r2 and caused r2's one blocker: 15 binary golden conflicts + T2 drift on the merged tree) plus the golden re-bless made ON the merged tree. MECHANICAL FACT (git-verified by the dispatching orchestrator): app/, harness/, tools/, assets/, demos/ are byte-identical to the code r2 reviewed (cb3bf2d) — ZERO code folds landed this round; the only textual deltas vs r2 are stories-v2.md §5.10's status-line hunk (#63's own, arrived via the rebase) and the T1 golden manifests' catalog-hash churn (excluded from this lens-diff; byte-identical to base v2). The PR's binary surface (105 files: 74 re-blessed + 2 new juice golden PNGs, 9 sprite PNGs, style-gate artifacts, juice.t1/juice.log.bin) is summarized at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/golden-manifest.txt. Do NOT re-derive golden bytes, do NOT eyeball any PNG, and do NOT run the test suite (Perkins ran tools/ci-local.sh at the reviewed sha: 10/10 gates green, 32/32 demos) — review CODE and DOCS.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.1-visual-juice-r3 — a checkout at exactly the reviewed sha (5c482df8ed819b6a78f646f27a251c0a081d12ef). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins r3 briefing (the round guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/spec/perkins-briefing-r3.md
- Job briefing (the implementing minion's spec — hard requirements + acceptance list): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/spec/job-briefing.md
- Story 7.1 card (Given/When/Then contracts): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/spec/story-7.1.md
- Look-book canon INCLUDING the §6 amendment (§2 palette hexes are the exact 2D target): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/spec/look-book-v1.md
- Current PR body (the claims under audit): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/spec/pr-body.md
- No GitHub issue exists for this job (verified r1; see spec/NOTE.md).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [PERKINS MECHANICAL STAMPS — r3 fix audit, ALREADY VERIFIED; do not re-derive, do not re-file]: (1) r2's blocker (the post-#63 lane collision) is FIXED: merge-base(HEAD, v2) = ebd02cb (= v2 tip — the branch contains #63); the diff vs v2 is the 7.1 work only, ZERO core/ or data/ files; tools/ci-local.sh at the reviewed sha is 10/10 GREEN including gate 4 (golden harness: T1 hashes + T2 software pixels + replay — the r2 scratch-merge drift of 6 demos at 218–12,311 px/frame is dead) and gate 5 palcheck (roofs, host play-marking B1 canary 92px, puck LEDs 50px, puck tone 1441px, banner-rect agreement 1041px, zoomed lane stripes 4598px — all green); T1/replay identity holds at file level (the only .t1/.log.bin entries in the diff vs v2 are the ADDITIONS goldens/juice.t1 + goldens/juice.log.bin — zero modifications of existing manifests). (2) r1 B1/B2 remain fixed: all 9 sprites' content_bbox == PIL top-down alpha bbox EXACTLY (re-verified r3); view_compute (main.odin:269) precedes start_run (:274). (3) The #63 re-bless cause chain is documented in commit 5c482df's message (catalog change → catalog_hash shift → every T1 manifest + affected T2 frames re-blessed on the rebased base; the 15 conflicted PNGs resolve to the juiced frames) — each link consistent with the stamps. You MAY challenge a stamp only with concrete quoted evidence.
- [CARRY-FORWARD SET — r2's tracked findings, ALL still present (zero code folds — mechanically proven by the empty cb3bf2d..5c482df code diff); do NOT re-file them]: W-A assist route-glow halo still pre-band formula (app/render/assist.odin:425/442) · W-B palcheck header overclaims + dead HOUSE_BODIES/HOST_BODY consts (harness/palcheck.odin:7-29) · W-C last_sel_* not updated by banner-focus detours (app/main.odin:1160-1178, 687-689) · W-D palcheck normalize duplicates goldens.odin flip+swizzle (harness/palcheck.odin:77-93) · W-E/W-F/W-G/W-H/W-I coverage cluster (focus-zoom camera model, on_cancel exit, boot-order fit, class-ghosting — all unpinned) · W-K puck canaries aggregate not per-sprite (harness/palcheck.odin:148-149) · W-L advisory gate CONCERNS · N-A draw_packets stale header (view.odin:601-604) · N-B stale fiber/pooled-core comment (view.odin:216-237) · N-C gen_sprites CREAM/DC_VENT unused (tools/gen_sprites.py:40,42) · N-D banner-focus empty-map click no exit (main.odin:406-410) · N-E SLA row 2px overlap (main.odin:1247-1255) · N-F look-book "targeting main" nit · N-G on_cancel fires before placement branch (input/exec.odin:48-62) · N-H palcheck discards catalog bools (palcheck.odin:196-206) · N-I PR-body nits (health-meter claim, 9/9-vs-10) · N-J ci-local "9 gates" strings (tools/ci-local.sh:4-30) · N-K "health on" substring key (palcheck.odin:161-165) · N-L chrome geometry two homes · N-M doorstep 25-slot no-wrap unpinned · r1 leftovers (crisis card_w/line_h dup, doorstep kx/ky dup, banner_y dup app↔harness, camera_update restates fit formula, parity-hook pin deferred to 7.3). These are RECORDED and carry to r4 regardless of what you do. A fold that made one WORSE, or a NEW defect in the same code, IS a new finding — file those.
- [VISION CAVEAT — this round runs WITHOUT native vision]: pixel claims verified MECHANICALLY only. Aesthetic judgment calls are DEFERRED to a kimi-vision re-check — NOT findings, do not block on them, do not fake them.
- [THE HARD BLOCKER CLASSES]: (a) View purity — the View reads ONLY snapshots; no new snapshot fields without documented reason; replay byte-identical [E10]. (b) Canon application, not redesign: §2 palette hexes + §6 amendment (top-down buildings, roof carries the read, painted shading + flat contact shadows allowed); never-color-alone (shape/icon/outline companions). (c) Chrome idiom matches the 5.5 popover (translucent warm cards + hairline, render-package-owned layout, single-source rects shared with hit-tests). (d) Camera-fit: wider/taller reveals more map. (e) Goldens: deliberate re-blesses only, documented — accept the mechanical stamps.
- [NO SCOPE CREEP]: no a11y MODES (7.3), no audio (7.2), no mechanics/balance changes, no core/snapshot changes in the 7.1-authored surface, no asset regeneration beyond gen_sprites.py. A violation = blocker. (#63's core/data content is BASE, not this PR's authored surface.)
- [CI note]: GitHub Actions is org-billing-blocked + a GitHub incident — NOT a signal. The local suite is ground truth (10/10 green, Perkins-run at the reviewed sha).
- [What NOT to re-litigate]: the user-approved style-gate verdicts (top-down, painted shading, contact shadows, focus-zoom camera model — the two-tone roof + contact shadow IS the approved design); the 5.5 popover chrome; the look-book canon itself (final — apply, don't judge); the glm-5.3 fallback (operational, not canon); r1/r2 held-clean ground (canon application, ODN-1 view purity, chrome idiom, never-color-alone, golden discipline — mechanically verified); #63's own approved content; the fallback-model caveat (operational).
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

This is an offline deterministic game — calibrate: the real surfaces here are file I/O and parsing at trust boundaries (the #load-embedded sprites.json parse, os.read_entire_file_from_path on the demo file inside palcheck, texture path construction, the harness CLI arg surface), integer-coercion hazards in the parse (f32(n) from json.Integer — negative/huge values), and anything that could crash or corrupt state in CI. Do not invent web-app findings that have no surface here. Your `source` value is "security".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "security",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.1-visual-juice/r3/security.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens security complete — N findings written".
