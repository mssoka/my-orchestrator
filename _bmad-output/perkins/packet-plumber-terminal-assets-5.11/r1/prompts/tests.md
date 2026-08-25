You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-terminal-assets-5.11-r1/project-context.md (project conventions). Key invariants: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); arrays/slices only in core, never map iteration (ODN-9/10); events, not callbacks (ODN-14); no globals/singletons (ODN-13); errors are values; JSON is for catalogs only (fail-fast, embedded via `#load`); raylib immediate-mode inside BeginDrawing/EndDrawing; the golden harness renders with the software renderer (rlsw) so T2 pixels are bit-identical; goldens re-bless only deliberately + documented. THIS PR'S SURFACE is art + sprite-pipeline DATA ONLY (assets/sprites + the sheet-loader mirror in app/render/sprites.odin + tools/gen_sprites.py + the blend provenance sources) — it must NOT touch `core/`, `data/`, draw wiring, the Terminal_Role enum, caps, or growth (those belong to story 5.11 the CODE story, deliberately not this PR).

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/diff.patch (252 lines — PR #65 of solarity-services/Packet-Plumber, base `v2`, story 5.11 art job "terminal assets": two new terminal sprites, small-biz + campus). These exact bytes are the review target — never re-fetch or regenerate the diff. Three files are binary (pp-scene-light-vista.blend, small_biz.png, campus.png — "Binary files differ" markers only); do NOT eyeball PNGs and do NOT byte-grep the .blend (it is Zstandard-compressed — string-grep evidence on it is INVALID; its object inventory is covered by a mechanical stamp below).

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-terminal-assets-5.11-r1 — a checkout at exactly the reviewed sha (7b9aaa45c6105c042aeb959835cceb54d80ddfec). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins r1 briefing (the round guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/perkins-briefing-r1.md
- Job briefing (the implementing minion's spec — hard requirements + acceptance list + scope guard): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/job-briefing.md
- Story 5.11 card (the code story this art job feeds — Given/When/Then + touch points; NOTE: the card's code work is NOT this PR): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/story-5.11.md
- Look-book canon (§2 palette tokens, §1 building language): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/look-book-v1.md
- Art direction + amendments: /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/art-direction-v1.md, /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/art-direction-amendments.md
- PR body (the claims under audit): /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/pr-body.md
- No GitHub issue exists for this job (verified; see /Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/spec/NOTE.md).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [PERKINS MECHANICAL STAMPS — r1, ALREADY VERIFIED; do not re-derive, do not re-file]: (1) Delta exactness: merge-base(HEAD, v2) = 0fd8870 = v2 tip (the #64 merge); the diff is EXACTLY 7 files (+139/−7): the .blend binary, pp_lib.py (+56), app/render/sprites.odin, assets/sprites/campus.png (new), assets/sprites/small_biz.png (new), assets/sprites/sprites.json, tools/gen_sprites.py (+57) — no other changes. (2) ZERO churn: goldens/ untouched; the 9 canon sprite PNGs byte-identical (empty git diff); core/ + data/ untouched. (3) Manifest: order = base order + [small_biz, campus] appended (base prefix intact); content_bbox existing 9 entries byte-identical, 2 added. ALL 11 manifest bboxes == PIL alpha bbox EXACTLY. Width ladder: house 88 < small_biz 120 < campus 154; campus 154×103 is the largest terminal footprint (host 126×91, dc 146×83). (4) tools/ci-local.sh --mac Perkins-run at 7b9aaa4: 10/10 gates GREEN (/Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/ci-local.log) — gate 4 goldens byte-stable (NO re-bless), gate 5 palcheck green. GitHub Actions on #65 is org-billing-blocked + a GitHub incident — NOT a signal; the local suite is ground truth. (5) Palette mechanics: shipped sprites derive exactly from the declared tokens — small_biz: roof #6E6148 exact-px present, panel = roof×0.90, cream sign #FFF6E6 exact; campus: hall roof #6E3026 exact, wing roofs = roof×0.90, quad #A8C878 exact, cream tower #FFF6E6 exact. BODY hexes (#9C8C6C, #A8503C) appear 0× in the sprites — occluded by the roof overhang in the top-down camera, the SAME behavior as the canon houses (harness/palcheck.odin header: "the steep camera occludes the wall band, body hexes never enter the sprites"). NOT a defect. (6) LAVISH GATE FIDELITY (the user's aesthetic verdict is CANON — do not re-judge it; verify only mechanical fidelity, which holds): the gate artifact (/Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/lavish-gate/terminal-assets-5.11.html + trio.png + map-moment.png) records the verbatim verdict "APPROVE — ship these two shapes as shown"; the PR body quotes it verbatim. Connected-component analysis of trio.png: house blob 89×90, small_biz blob 122×88, campus blob 158×95 — ratio-consistent with the shipped sprites (88×89 / 120×87 / 154×103, ±3%), same token palettes per panel; map-moment.png contains both new shapes (campus-roof ~19.3k px, small-biz-roof ~8.7k px, quad present). What shipped == what was approved. (7) Blend provenance: headless-Blender object listing of the .blend shows SmallBiz* (12 objects, incl. a second scene instance SmallBiz2) + Campus* (11 objects: hall/wings/pavilion/quad/tower, clean naming) — the canon blend carries the new models. (8) Loader contract: sprites.odin arrays are [SPRITE_COUNT=11]; files list 11 entries in manifest order; sprites_parse_boxes REJECTS len(order) != SPRITE_COUNT (whole sheet falls back to primitives — never a guessed bbox); bbox value-range checks (0..256, non-degenerate); sprite_index_building is COMMENT-ONLY changed (no draw wiring); no Terminal_Role/caps/growth changes anywhere (core/ + data/ diffs empty). (9) palcheck scope: gate 5 scans blessed goldens + a zoomed live frame — the NEW sprites are loaded but drawn by NO role, so they cannot appear in palcheck's frames; the palette stamp (5) is the mechanical equivalent for them. NOT a defect of this PR (story 5.11's wiring brings them into golden/palcheck scope).
- [KNOWN NITS — real but note-grade, already weighed; file only if you found something BEYOND them]: pp_lib.py lines 631-633 have THREE blank lines where house style is two; sprites.json lacks a trailing newline (PRE-EXISTING — the base file also lacks it).
- [CARRY-FORWARD SET — 7.1 r4's 3W/7N leftovers (incl. W-5 "sprites.json three unenforced homes") are NEXT-STORY fodder by the minion's declared choice; do NOT re-file them; this PR is not their fixer]. A NEW defect in the same code, or a change that made one of them WORSE, IS a new finding — file those.
- [VISION CAVEAT — this round runs WITHOUT native vision]: pixel claims verified MECHANICALLY only (bbox math, palette/pixel comparisons, silhouette metrics — done, see stamps). Aesthetic judgment calls are DEFERRED — NOT findings, do not block on them, do not fake them. The user's lavish APPROVE is canon.
- [THE HARD BLOCKER CLASSES — from the round charter]: (a) the delta is NOT exactly the declared set (stamped clean ✓); (b) golden churn / re-bless (stamped clean ✓); (c) canon + never-color-alone broken — the capacity ladder must live in the GEOMETRY (bbox widths 88→120→154, distinct silhouettes; stamped ✓); (d) lavish fidelity — what ships != what was approved (stamped ✓); (e) scope creep — draw wiring, enum, caps, growth, economy, other tiers (stamped clean ✓ — their ABSENCE is CORRECT). Challenge a stamp only with concrete quoted evidence.
- [What NOT to re-litigate]: the user's lavish APPROVED verdict; the 7.1 sprite pipeline (4-round approved — this job extends it); the look-book canon (apply, don't judge); the fallback-model caveat; the billing-blocked CI.
- The base is `v2`. Files NOT in the diff are read-only context.

--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Happy-path-only coverage where error handling is implied
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings. ROUND 1 EMPHASIS: the repo's test surface is the LOCAL gate suite (tools/ci-local.sh — 10 gates, Perkins-run green at the reviewed sha; see $R/ci-local.log) + harness/ goldens (gate 4: T1 hashes + T2 software pixels + replay) + palcheck (gate 5). Trace THIS diff's behavior changes: (1) loader now loads 11 sprites + parses the extended manifest — which gate pins it (gate 4 would catch a load failure via fallback-to-primitives pixel drift? does any gate distinguish "loaded small_biz" from "fell back"?); (2) the new manifest entries + bbox values — pinned by anything (goldens don't draw them; palcheck doesn't scan them — stamp 9)? Is an unpinned manifest data change a coverage gap, and at what severity for an art-data PR whose charter says wiring+goldens arrive in story 5.11 (the card's own golden requirement: "a T2 frame with all three types visible" — 5.11's, not this PR's)? (3) gen_sprites.py new builders — reproducibility pinned anywhere? Weigh the charter: this PR's DELIVERABLE is data + pipeline; judge coverage against what the PR claims to guarantee (byte-stable canon, parse-clean manifest, green suite), not against story 5.11's future wiring.

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
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, coverage-gap, canon>",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-terminal-assets-5.11/r1/tests.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens tests complete — N findings written".
