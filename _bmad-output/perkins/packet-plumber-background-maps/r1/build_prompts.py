#!/usr/bin/env python3
# Builds the 7 lens briefs for perkins r1 (packet-plumber-background-maps).
R = "/Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-background-maps-r1"

SHARED_HEAD = """You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read {WT}/project-context.md (project conventions). Key invariants: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats live in the view (ODN-10); arrays/slices only in core, never map iteration (ODN-9/10); events, not callbacks (ODN-14); no globals/singletons (ODN-13); errors are values; JSON is for catalogs only (fail-fast, embedded via `#load`); raylib immediate-mode inside BeginDrawing/EndDrawing; the golden harness renders with the rlsw SOFTWARE renderer (bit-identical pixels, no GPU); goldens re-bless only deliberately + cause-documented; §10.4 — no transcendentals (no libm) in the rasterized path. THIS PR'S SURFACE (story 7.4 / canon D9): the procedural land/ocean/parks background map — `app/render/map.odin` (new generator), the map pass + seed threading in `app/render/view.odin` + `app/main.odin`, water/coast/park palette tokens (`app/render/palette.odin` + `data/palette.json`), harness palcheck map gates, the harness `map-preview` dev tool, a deliberate full T2 golden re-bless (76 PNGs), and the canon folds (stories-v2.md Story 7.4, decision-log D9, look-book-v1.md §2+§7). It must NOT touch `core/` or any sim logic.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: {R}/diff.patch (1050 lines — PR #67 of solarity-services/Packet-Plumber, base `v2`, story 7.4 "procedural land/ocean/parks background map (canon D9)"). These exact bytes are the review target — never re-fetch or regenerate the diff. 76 of the 90 files are re-blessed golden PNGs (binary "diff --git" markers, no hunks); the 14 code/doc files carry the real hunks. A code-only extract (same hunks, PNG headers stripped) exists at {R}/diff-code.patch for convenience — the full diff.patch remains canonical. Do NOT eyeball PNGs as evidence in either direction; pixel claims are covered by the mechanical stamps below.

--- WORKTREE (your verification source) ---
{WT} — a checkout at exactly the reviewed sha (2773dd2a6d10631148ef75295c33a79c8ef8e6c9). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins r1 briefing (the round guards — your charter): {R}/spec/perkins-briefing-r1.md
- Job briefing (the implementing minion's spec — hard requirements + acceptance + scope guard): {R}/spec/job-briefing.md
- PR body (the claims under audit): {R}/spec/pr-body.md
- Canon (in the worktree, as amended by this PR): {WT}/_bmad-output/planning-artifacts/art-renders/look-book-v1.md (§2 palette + §7 amendment), {WT}/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md (the 2026-08-18 D9 entry), {WT}/_bmad-output/planning-artifacts/sprints/stories-v2.md (§Story 7.4).
- No GitHub issue exists for this job (verified; see {R}/spec/NOTE.md + {R}/spec/issues.json).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [PERKINS MECHANICAL STAMPS — r1, ALREADY VERIFIED BY THE DISPATCHER; do not re-derive, do not re-file]:
  (1) Delta exactness: merge-base(HEAD, v2) = af05b1a = the v2 tip (the #65 merge). The diff is EXACTLY 90 files: the 76 goldens PNGs + 14 code/doc files (app/render/map.odin NEW, app/render/view.odin, app/render/palette.odin, app/main.odin, data/palette.json, harness/goldens.odin, harness/main.odin, harness/map_preview.odin NEW, harness/overlay.odin, harness/palcheck.odin, harness/run.odin, stories-v2.md, decision-log.md, look-book-v1.md). Zero non-PNG golden churn (.t1/.log.bin byte-identical); core/ untouched; nothing outside app/, harness/, data/palette.json, goldens/, _bmad-output/.
  (2) tools/ci-local.sh --mac Perkins-run at 2773dd2: 10/10 gates GREEN ({R}/ci-local.log) — gate 4 golden harness (T1 hashes + T2 software pixels + replay gate) PASS on the re-blessed tree; gate 5 palcheck (incl. the NEW map gates) PASS. GitHub Actions on #67 is org-billing-blocked + a GitHub incident day — NOT a signal; the local suite is ground truth.
  (3) The FNV-1a-64 identity pin is REAL and non-vacuous: an INDEPENDENT Python reimplementation of the generator ({R}/verify_map_pin.py) reproduces MAP_IDENTITY_PIN = 0xADC46DEEF414FD5A for the seed-7 cells EXACTLY — the pin binds every generator constant (thresholds, cell sizes, hash constants, enum values, pass order); any change breaks gate 5. Seed sensitivity: seed 8 → 0xFAB598CC7A81A345 ≠ seed 7. Same-seed stability: the generator is a pure function of (seed, dims) + the palcheck h1==h2 leg runs live.
  (4) STYLE FIDELITY (the user's lavish verdict is CANON — verify mechanical fidelity only): the shipped code rendering seed 1234 (`tools/harness.sh map-preview 1234`, rlsw) is BYTE-IDENTICAL to the approved gate artifact candidate B ({R}/lavish-gate/candidates/b-seed1234.png): 0/921,600 pixels differ. What shipped IS what the user approved ("Map style verdict: pick B (seed 1234)" — gate page {R}/lavish-gate/index.html). The verdict is quoted verbatim in the PR body + look-book §7 + decision-log.
  (5) The re-bless fold-only proof (goldens/juice/30000ms.png, v2 vs HEAD): 61.6% of pixels changed; the changed set is EXACTLY the old cream background → water/park/coast/grid-over-water + alpha-BLEND EDGE pixels (HUD text antialiasing, translucent pipe glow — they blend with the backdrop, which changed); sprite-core exact colors (puck LED green, ink text, roofs) are 100% byte-identical. The sim/sprites did not move — only the world under them.
  (6) PRESENTATION-ONLY (ODN-1): app/render/map.odin imports only `vendor:raylib`; it writes ONLY View fields (map_cells/map_seed/map_gen_w/map_gen_h); the seed flows read-only from state.seed at all 5 draw_world call sites (app/main.odin:420, harness/goldens.odin:71, harness/overlay.odin:110, harness/palcheck.odin:253, harness/map_preview.odin:108); core/ diff is empty; palette.json is deliberately NOT hashed (core/catalog.odin:984 — "palette is cosmetic and deliberately NOT hashed — it must not bind replay").
  (7) DOCS-NUMBERS RECONCILIATION (do NOT file "docs stats mismatch the code" without this math): the gate stats "~52% land / ~28% water / ~8% parks at seed 1234" are SCREEN-pixel approximations of the approved render (world-rect pure-color counts 49.1% land / 27.2% water / 8.5% park + ~14% overlay coverage: grid lines, sprites, HUD). The CELL shares at seed 1234 are land 58.3% / water 30.9% / park 9.6% / coast 1.3% — BOTH describe the SAME image (verified: candidate B's pixel composition matches the cell shares exactly once overlay coverage is accounted). The MAP_LAND_LEVEL comment ("0.46 measured only ~40-49% world land; 0.38 → ~65-70%") counts NON-WATER landmass (69.2% at 1234) — consistent. These are informal-but-faithful approximations, not defects.
  (8) The `if len(rest) ... {{ usage() }}` fall-through WITHOUT exit in harness/main.odin is the PRE-EXISTING file convention (replay/palcheck/stats-check identical — 12 sites); map-preview follows it. Not a new defect of this PR.
  (9) The palcheck map oracle (section 1d) scans the BLESSED golden goldens/juice/30000ms.png (load_frame — the actual re-blessed bytes, not a synthetic re-render) with floor counts + margin (water>200K vs measured ~460K incl. margins; land>150K vs ~246K; park>50K vs ~87K; coast>4K vs ~7.4K) — a real presence oracle: a removed/broken map collapses all four at once.
  (10) Scope guard: the `harness map-preview <seed>` dev tool is harness-side and EXPLICITLY sanctioned by the round charter ("the new dev tool (harness map-preview <seed>) is harness-side"); it is declared "Not a CI gate" in the PR body. ffloor/fceil have no pre-existing duplicates in app/render (checked).
- [VISION CAVEAT — this round runs WITHOUT native vision]: pixel claims verified MECHANICALLY only (done — see stamps). Aesthetic judgment calls are DEFERRED — NOT findings. The user's lavish verdict is canon.
- [THE HARD BLOCKER CLASSES — from the round charter]: (a) presentation-only `[ODN-1]` broken — the map perturbs the sim / T1/replay shift (stamped clean ✓); (b) seeded+deterministic broken — pins vacuous (stamped: pin reproduces independently ✓); (c) the palcheck map oracle is not real (stamped: scans the blessed golden ✓); (d) style fidelity — what ships != what was approved (stamped: byte-identical ✓); (e) re-bless unsound — cause chain / fold-only violated, .t1/.log.bin churn (stamped ✓); (f) canon folds inconsistent with the doctrine reframe #61 (read them; they align); (g) scope creep — core/, sim, gameplay, minimap, camera, terrain-gated placement (stamped: absent — their ABSENCE is CORRECT). Challenge a stamp only with concrete quoted evidence.
- [What NOT to re-litigate]: the user's lavish verdict (pick B); the 7.1/7.4 sprite + view ground (approved); the look-book canon; the fallback-model caveat; the billing-blocked CI; the 5.11-types roster (a sibling round, in flight).
- The base is `v2`. Files NOT in the diff are read-only context.
"""

SHARED_TAIL = """
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{{
  "source": "{SRC}",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. determinism, coupling, coverage-gap, canon>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}}

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
{OUT}/{LENS}.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens {LENS} complete — N findings written".
"""

LENSES = {
"blind": None,  # special: isolation contract, built separately

"edge": """--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. ROUND 1 EMPHASIS:
(1) map_generate/map_ensure (app/render/map.odin): n <= 0 early return vs a View with stale map_cells from a LARGER prior world (len(v.map_cells) != n → delete+make — but what if the new n is SMALLER and equals the old len? walk it); world dims change without seed change (map_gen_w/h guards); the scratch masks on context.temp_allocator — who guarantees a temp arena exists at EVERY map_draw call site (app frame loop vs harness paths vs map-preview)? map_cells owned by context.allocator at generate time — allocator mismatch if generated under different contexts (harness vs app); the [dynamic] growth path (make with len=n — can it grow/realloc mid-life?).
(2) ffloor/fceil (app/render/view.odin): documented "for non-negative f32" — walk where off_x/off_y/scale could go negative (palcheck's zoomed lane read sets off_x/off_y manually — read those lines; window SMALLER than world → scale fits so off >= 0 by construction — verify by reading view_setup); i32 overflow at extreme scale; fceil(f32(t) < f) for values beyond 2^24 (f32 integer precision).
(3) The span-fill loops in map_draw: row_bot <= row_top skip (zero-height rows at scale < 1); sx1 > sx0 guard; a world px mapping to zero screen columns; y in 0..<h with v.world_h fractional (world dims are f32 — i32(v.world_h) truncation).
(4) harness/map_preview.odin: strconv.parse_uint rejection path; rest[0]/rest[1] indexing after the usage() fall-through (NOTE stamp 8 — the convention is pre-existing; assess only whether the NEW code adds a path BEYOND it); delete(out) then reassign — double-free or leak paths; InitWindow/CloseWindow + LoadImageFromScreen failure (ExportImage ok=false handled — read it); the settle loop u64(1)..=600 with clear(&state.events).
(5) palcheck section 3: map_cells_hash FORCES regen — walk the View reuse across sections (the same `view` var used by earlier sections — is it in a state where forcing regen corrupts a later section? read run_palcheck's flow top to bottom).
Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing. Your `source` value is "edge".""",

"acceptance": """--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

The spec of record is the JOB BRIEFING (hard requirements 1-6 + acceptance 1-3 + scope guard) + the Perkins r1 charter guards. For each finding, reference the violated requirement in `detail` (quote the exact phrase from the spec when possible). ROUND 1 EMPHASIS: hard req 1 (deterministic, seeded, presentation-only — no snapshot fields, no LOG_VERSION bump, replay byte-identical, T1 unshifted); hard req 2 (the generator: noise-driven landmasses + coastlines + park blobs, LOW-contrast terrain, placement NOT terrain-gated — read app/render/map.odin + verify the terrain constants vs the claim); hard req 3 (render order + tokens: map under everything, snap grid subtle per canon, palette from look-book tokens, palcheck gate covers water/park); hard req 4 (the lavish gate BEFORE the PR — the verdict verbatim in the PR body: check it appears verbatim + the approved style is what shipped); hard req 5 (full T2 re-bless deliberate + cause-documented; T1+replay byte-identical proven in the PR); hard req 6 (canon folds: story card + D9 decision-log entry in the same PR). Acceptance 1-3 (verdict verbatim; same-seed identity pinned + replay byte-identical + T1 unshifted + ci-local 10/10 claimed in the PR — the stamps confirm); the PR body's generator-design documentation duty (noise type, seed derivation, palette extension, re-bless cause chain, citations). Also audit the D9 canon-fold text for faithfulness: look-book §7 + decision-log say "Terrain does NOT gate placement in v1; terrain-aware growth + a possible real-geography map are named follow-ups" — the job briefing demands real geography be FLAGGED, not silently dropped; verify the fold records it. Your `source` value is "acceptance".""",

"security": """--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

CONTEXT: this is an offline deterministic Odin game — no network, no auth, no user accounts. The realistic surfaces in this diff: (1) harness/map_preview.odin — a CLI dev tool taking `<seed>` (strconv.parse_uint) and an optional OUTPUT PATH passed to rl.ExportImage (arbitrary-path file write from a CLI arg — assess realistically for a local dev tool, not a web service); (2) data/palette.json loading via palette_load (JSON parse of a committed catalog — fail-fast conventions; what happens on malformed JSON); (3) the deterministic-noise integer math (map_hash — u64 overflow wraparound is BY DESIGN in mixing functions, not an integer-overflow vulnerability). Calibrate severity to an offline game's threat model — do not file web-app findings that have no attacker here. Your `source` value is "security".""",

"architecture": """--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

ROUND 1 EMPHASIS:
(1) ODN-1 layering: map.odin lives in app/render and writes only View state — assess the seed THREADING choice: `seed: u64` appended to draw_world's signature (now 10 params) vs alternatives (holding the seed in the View at render_setup). Read the 5 call sites; is threading consistent with how tick/era/health flow?
(2) Cache lifecycle: map_cells owned by context.allocator, regenerated on seed/world change, scratch on temp arena — read map_generate's allocator comments; is the ownership split clean per the project's allocator discipline (read how neighboring View fields / harness Render_Ctx manage memory)?
(3) The 4-pass generator (land noise → water dilation → park noise → assemble): complexity vs the problem; the park_seed = seed ~ MAP_HASH_DELTA decorrelation trick; is the pass structure readable/maintainable per project norms?
(4) Span-fill rendering (per-row run coalescing with ffloor/fceil shared boundaries): soundness of the no-hairline-gap claim; deterministic f32 math per §10.4; contrast with how draw_bundles/draw_nodes span the world.
(5) The palcheck additions: MAP_IDENTITY_PIN as a re-blessable constant (the project's pin discipline — compare drift-check/golden conventions); the map gates in section 1d — floor counts with margin; is the pin re-bless workflow consistent with how other pins/goldens are blessed (read harness/goldens.odin + palcheck conventions)?
(6) The harness map_preview tool duplicating the juice fixture (juice_scene lifted from demos/juice.dem?) — read demos/ to see whether the fixture duplication is deliberate (like-for-like candidates) or drift-prone (a second copy of the scene that can rot). Your `source` value is "architecture".""",

"codebase": """--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

ROUND 1 EMPHASIS:
(1) draw_world signature change: find EVERY caller in the repo (grep app/ harness/ demos/ tools/) — the stamp lists 5; confirm no sixth caller broke and that default args ({}, -1, -1) match each caller's intent.
(2) app/render/map.odin naming + style vs its siblings (view.odin, palette.odin, sprites.odin): proc naming (snake_case), constant naming (UPPER_SNAKE), comment voice/voice-consistency, package conventions; Map_Kind enum style vs other enums in the codebase.
(3) ffloor/fceil vs existing helpers — core:math floor/ceil exist? Why hand-rolled (read the §10.4 no-transcendentals rule in project-context.md/docs; libm floor/ceil are they banned in the rasterized path?); duplicate definitions anywhere else?
(4) The harness map-preview verb: does it follow main.odin's verb-dispatch conventions (read the replay/palcheck/stats-check verbs); strings.clone/clone_to_cstring usage vs codebase patterns; render_setup/rc usage consistent with run_demo.
(5) palette tokens: data/palette.json keys vs palette.odin jcol reads vs fallback_palette vs look-book §2 table — all four consistent (hex → RGB quads)? Check ink_faint etc. neighbors for the file's formatting conventions (aligned columns).
(6) Docs folds: stories-v2.md Story 7.4 card structure vs sibling story cards (read Story 7.1/7.2 cards); decision-log D9 entry format vs the log's other entries; look-book §7 amendment vs the §7.1 amendment's shape. Your `source` value is "codebase".""",

"tests": """--- YOUR LENS ---
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check (adapted to this repo's test topology: `odin test core` unit tests + the harness gates — lint/goldens/palcheck/drift-check/preview-check/stats-check/input-parity — are the test system; there is no per-file unit framework for app/render):
- The generator's behaviours: same-seed identity (palcheck §3 pin — traced ✓), same-seed stability (h1==h2 ✓), seed sensitivity (h3!=h1 ✓) — what about WORLD-RESIZE regeneration (map_gen_w/h guard) and the multi-seed-in-one-process stale-cache regression the PR body says the pin caught? Is there a leg that would catch a NON-TOTAL generator today (walk what h1/h2/h3 actually pin)? What about the park/coast interior-only invariants, the land-share range, the span-fill no-gap property (covered by the 76 golden T2 byte-compares?), and the map-preview tool itself (declared not-a-gate — is anything exercising its parse/failure paths)?
- The palcheck 1d oracle: floor counts on ONE frame (goldens/juice/30000ms.png) — is one frame enough for an every-frame feature? (Reason about it: the map is seed-static per run; the juice demo's seed pins the map — so one frame does bound the map; assess.)
- The re-bless itself: T1 manifests + replay logs byte-identical is PROVEN how in the repo's gates (gate 4 + git-diff absence) — traceable ✓ per stamps.
- The seed threading at call sites: goldens re-blessed = the T2 system test; app-layer draw (app/main.odin:420) has no golden — same as pre-existing behavior (the app layer was never golden-captured) — assess whether that's a gap THIS PR created or the pre-existing topology.
Test level mix: flag mismatches as findings. Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"; severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages; recommended_fix: what would raise the gate.
Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80%; CONCERNS: P0 100%, P1 80–89%, overall ≥80%; FAIL: P0 <100%, or P1 <80%, or overall <80%. Your `source` value is "tests".""",
}

BLIND = """You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

ISOLATION CONTRACT — this is a BLIND review: the ONE file named below is the ONLY thing you may read. Reading anything else (repository files, specs, docs, prior reviews, PNGs) invalidates your lens. Do not explore any directory. Do not open any other file. Your tools are to be used ONLY on this file:

1. The diff (read it FIRST and IN FULL): {R}/diff.patch (1050 lines, unified format; PR #67 of solarity-services/Packet-Plumber, base branch v2; title "story 7.4: procedural land/ocean/parks background map (canon D9)"; ROUND 1, a fresh PR). These exact bytes are the review target. 76 of the 90 files are binary golden PNGs (re-blessed screenshots) — they appear only as "diff --git" headers with no hunks; you cannot and must not read them; claims about their CONTENT are out of your reach (claims about their PRESENCE/paths are in scope).

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed — e.g. counts, orders, thresholds, comments claiming something the hunks contradict)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself (e.g. a comment claiming ~65-70% land while a doc hunk claims ~52%; a constant renamed in one hunk but not another; the pin constant vs the code that computes it)
- Changes that don't match their claimed purpose (the hunks claim: a PRESENTATION-ONLY seeded map generator in the view layer, palette tokens, harness seed threading, a map-identity palcheck pin, a map-preview dev tool, a deliberate 76-PNG golden re-bless, and three canon docs folds — verify the hunks stay inside that story; anything that smells like sim/gameplay change is a finding)

Context you may infer from the diff itself only: this is an Odin-language game (raylib app layer `app/`, deterministic sim core `core/` — NOT touched by this diff) plus a harness (golden-image + palcheck gates). The `source` value for your findings is "blind".
"""

import os
for lens, body in LENSES.items():
    if lens == "blind":
        text = BLIND.format(R=R) + SHARED_TAIL.format(SRC="blind", OUT=R, LENS=lens)
    else:
        text = SHARED_HEAD.format(R=R, WT=WT) + "\n" + body + "\n" + SHARED_TAIL.format(SRC=lens, OUT=R, LENS=lens)
    with open(os.path.join(R, "prompts", lens + ".md"), "w") as f:
        f.write(text)
    print(lens, len(text.splitlines()), "lines")
