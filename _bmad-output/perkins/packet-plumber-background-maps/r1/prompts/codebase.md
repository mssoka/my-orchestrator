You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-background-maps-r1/project-context.md (project conventions). Key invariants: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats live in the view (ODN-10); arrays/slices only in core, never map iteration (ODN-9/10); events, not callbacks (ODN-14); no globals/singletons (ODN-13); errors are values; JSON is for catalogs only (fail-fast, embedded via `#load`); raylib immediate-mode inside BeginDrawing/EndDrawing; the golden harness renders with the rlsw SOFTWARE renderer (bit-identical pixels, no GPU); goldens re-bless only deliberately + cause-documented; §10.4 — no transcendentals (no libm) in the rasterized path. THIS PR'S SURFACE (story 7.4 / canon D9): the procedural land/ocean/parks background map — `app/render/map.odin` (new generator), the map pass + seed threading in `app/render/view.odin` + `app/main.odin`, water/coast/park palette tokens (`app/render/palette.odin` + `data/palette.json`), harness palcheck map gates, the harness `map-preview` dev tool, a deliberate full T2 golden re-bless (76 PNGs), and the canon folds (stories-v2.md Story 7.4, decision-log D9, look-book-v1.md §2+§7). It must NOT touch `core/` or any sim logic.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/diff.patch (1050 lines — PR #67 of solarity-services/Packet-Plumber, base `v2`, story 7.4 "procedural land/ocean/parks background map (canon D9)"). These exact bytes are the review target — never re-fetch or regenerate the diff. 76 of the 90 files are re-blessed golden PNGs (binary "diff --git" markers, no hunks); the 14 code/doc files carry the real hunks. A code-only extract (same hunks, PNG headers stripped) exists at /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/diff-code.patch for convenience — the full diff.patch remains canonical. Do NOT eyeball PNGs as evidence in either direction; pixel claims are covered by the mechanical stamps below.

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-background-maps-r1 — a checkout at exactly the reviewed sha (2773dd2a6d10631148ef75295c33a79c8ef8e6c9). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Perkins r1 briefing (the round guards — your charter): /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/spec/perkins-briefing-r1.md
- Job briefing (the implementing minion's spec — hard requirements + acceptance + scope guard): /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/spec/job-briefing.md
- PR body (the claims under audit): /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/spec/pr-body.md
- Canon (in the worktree, as amended by this PR): /Users/moses/.herdr/worktrees/packet-plumber/perkins-background-maps-r1/_bmad-output/planning-artifacts/art-renders/look-book-v1.md (§2 palette + §7 amendment), /Users/moses/.herdr/worktrees/packet-plumber/perkins-background-maps-r1/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md (the 2026-08-18 D9 entry), /Users/moses/.herdr/worktrees/packet-plumber/perkins-background-maps-r1/_bmad-output/planning-artifacts/sprints/stories-v2.md (§Story 7.4).
- No GitHub issue exists for this job (verified; see /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/spec/NOTE.md + /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/spec/issues.json).

--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [PERKINS MECHANICAL STAMPS — r1, ALREADY VERIFIED BY THE DISPATCHER; do not re-derive, do not re-file]:
  (1) Delta exactness: merge-base(HEAD, v2) = af05b1a = the v2 tip (the #65 merge). The diff is EXACTLY 90 files: the 76 goldens PNGs + 14 code/doc files (app/render/map.odin NEW, app/render/view.odin, app/render/palette.odin, app/main.odin, data/palette.json, harness/goldens.odin, harness/main.odin, harness/map_preview.odin NEW, harness/overlay.odin, harness/palcheck.odin, harness/run.odin, stories-v2.md, decision-log.md, look-book-v1.md). Zero non-PNG golden churn (.t1/.log.bin byte-identical); core/ untouched; nothing outside app/, harness/, data/palette.json, goldens/, _bmad-output/.
  (2) tools/ci-local.sh --mac Perkins-run at 2773dd2: 10/10 gates GREEN (/Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/ci-local.log) — gate 4 golden harness (T1 hashes + T2 software pixels + replay gate) PASS on the re-blessed tree; gate 5 palcheck (incl. the NEW map gates) PASS. GitHub Actions on #67 is org-billing-blocked + a GitHub incident day — NOT a signal; the local suite is ground truth.
  (3) The FNV-1a-64 identity pin is REAL and non-vacuous: an INDEPENDENT Python reimplementation of the generator (/Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/verify_map_pin.py) reproduces MAP_IDENTITY_PIN = 0xADC46DEEF414FD5A for the seed-7 cells EXACTLY — the pin binds every generator constant (thresholds, cell sizes, hash constants, enum values, pass order); any change breaks gate 5. Seed sensitivity: seed 8 → 0xFAB598CC7A81A345 ≠ seed 7. Same-seed stability: the generator is a pure function of (seed, dims) + the palcheck h1==h2 leg runs live.
  (4) STYLE FIDELITY (the user's lavish verdict is CANON — verify mechanical fidelity only): the shipped code rendering seed 1234 (`tools/harness.sh map-preview 1234`, rlsw) is BYTE-IDENTICAL to the approved gate artifact candidate B (/Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/lavish-gate/candidates/b-seed1234.png): 0/921,600 pixels differ. What shipped IS what the user approved ("Map style verdict: pick B (seed 1234)" — gate page /Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/lavish-gate/index.html). The verdict is quoted verbatim in the PR body + look-book §7 + decision-log.
  (5) The re-bless fold-only proof (goldens/juice/30000ms.png, v2 vs HEAD): 61.6% of pixels changed; the changed set is EXACTLY the old cream background → water/park/coast/grid-over-water + alpha-BLEND EDGE pixels (HUD text antialiasing, translucent pipe glow — they blend with the backdrop, which changed); sprite-core exact colors (puck LED green, ink text, roofs) are 100% byte-identical. The sim/sprites did not move — only the world under them.
  (6) PRESENTATION-ONLY (ODN-1): app/render/map.odin imports only `vendor:raylib`; it writes ONLY View fields (map_cells/map_seed/map_gen_w/map_gen_h); the seed flows read-only from state.seed at all 5 draw_world call sites (app/main.odin:420, harness/goldens.odin:71, harness/overlay.odin:110, harness/palcheck.odin:253, harness/map_preview.odin:108); core/ diff is empty; palette.json is deliberately NOT hashed (core/catalog.odin:984 — "palette is cosmetic and deliberately NOT hashed — it must not bind replay").
  (7) DOCS-NUMBERS RECONCILIATION (do NOT file "docs stats mismatch the code" without this math): the gate stats "~52% land / ~28% water / ~8% parks at seed 1234" are SCREEN-pixel approximations of the approved render (world-rect pure-color counts 49.1% land / 27.2% water / 8.5% park + ~14% overlay coverage: grid lines, sprites, HUD). The CELL shares at seed 1234 are land 58.3% / water 30.9% / park 9.6% / coast 1.3% — BOTH describe the SAME image (verified: candidate B's pixel composition matches the cell shares exactly once overlay coverage is accounted). The MAP_LAND_LEVEL comment ("0.46 measured only ~40-49% world land; 0.38 → ~65-70%") counts NON-WATER landmass (69.2% at 1234) — consistent. These are informal-but-faithful approximations, not defects.
  (8) The `if len(rest) ... { usage() }` fall-through WITHOUT exit in harness/main.odin is the PRE-EXISTING file convention (replay/palcheck/stats-check identical — 12 sites); map-preview follows it. Not a new defect of this PR.
  (9) The palcheck map oracle (section 1d) scans the BLESSED golden goldens/juice/30000ms.png (load_frame — the actual re-blessed bytes, not a synthetic re-render) with floor counts + margin (water>200K vs measured ~460K incl. margins; land>150K vs ~246K; park>50K vs ~87K; coast>4K vs ~7.4K) — a real presence oracle: a removed/broken map collapses all four at once.
  (10) Scope guard: the `harness map-preview <seed>` dev tool is harness-side and EXPLICITLY sanctioned by the round charter ("the new dev tool (harness map-preview <seed>) is harness-side"); it is declared "Not a CI gate" in the PR body. ffloor/fceil have no pre-existing duplicates in app/render (checked).
- [VISION CAVEAT — this round runs WITHOUT native vision]: pixel claims verified MECHANICALLY only (done — see stamps). Aesthetic judgment calls are DEFERRED — NOT findings. The user's lavish verdict is canon.
- [THE HARD BLOCKER CLASSES — from the round charter]: (a) presentation-only `[ODN-1]` broken — the map perturbs the sim / T1/replay shift (stamped clean ✓); (b) seeded+deterministic broken — pins vacuous (stamped: pin reproduces independently ✓); (c) the palcheck map oracle is not real (stamped: scans the blessed golden ✓); (d) style fidelity — what ships != what was approved (stamped: byte-identical ✓); (e) re-bless unsound — cause chain / fold-only violated, .t1/.log.bin churn (stamped ✓); (f) canon folds inconsistent with the doctrine reframe #61 (read them; they align); (g) scope creep — core/, sim, gameplay, minimap, camera, terrain-gated placement (stamped: absent — their ABSENCE is CORRECT). Challenge a stamp only with concrete quoted evidence.
- [What NOT to re-litigate]: the user's lavish verdict (pick B); the 7.1/7.4 sprite + view ground (approved); the look-book canon; the fallback-model caveat; the billing-blocked CI; the 5.11-types roster (a sibling round, in flight).
- The base is `v2`. Files NOT in the diff are read-only context.

--- YOUR LENS ---
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
(6) Docs folds: stories-v2.md Story 7.4 card structure vs sibling story cards (read Story 7.1/7.2 cards); decision-log D9 entry format vs the log's other entries; look-book §7 amendment vs the §7.1 amendment's shape. Your `source` value is "codebase".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. determinism, coupling, coverage-gap, canon>",
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
/Users/moses/code/_bmad-output/perkins/packet-plumber-background-maps/r1/codebase.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens codebase complete — N findings written".
