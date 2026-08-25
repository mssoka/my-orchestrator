#!/usr/bin/env python3
"""Generate the 7 Perkins lens prompts for packet-plumber-v2-ux-font-resize r1 (single wave, 869-line diff)."""
import os

OUT = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-ux-font-resize/r1"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-ux-font-resize-r1"
SHA = "91f7730"

SPEC_BLOCK = f"""  - Perkins briefing (your charter + lens-guards): {OUT}/spec/perkins-briefing-r1.md
  - Job briefing (the original spec — user report + acceptance): {OUT}/spec/job-briefing.md
  - Implementation spec (the minion's frozen spec — in the diff AND the worktree at _bmad-output/implementation-artifacts/spec-v2-ux-font-resize.md): {OUT}/spec/spec-v2-ux-font-resize.md
  - PR body (acceptance evidence — golden inventory + contrast table + min-clamp derivation + Decisions & rationale): {OUT}/spec/pr-body.md
  - Changed-file inventory at the sha: {OUT}/changed-files.txt"""

SCOPE = """v2 UX font+resize — USER REPORT 2026-08-15 (ruling-grade): "the font is hard to read" + "i cant seem to be able to resize the window. prototype could". TWO defects, ONE PR. Part 1 — the font: v2 rendered the raylib DEFAULT bitmap font (illegible on the light canvas); replaced with a bundled Open Sans Regular (SIL OFL 1.1, assets/fonts/open_sans_regular.ttf + OFL.txt) loaded ONCE at init by BOTH the app (app/main.odin, after InitWindow) and the harness (harness/goldens.odin render_setup) via the shared rnd.load_hud_font() (rl.LoadFontEx at base size 64 + BILINEAR filter; fallback rl.GetFontDefault on invalid load); all HUD text routes through rl.DrawTextEx(font, …, spacing 1) — the app's draw_text (main.odin) and the render package's draw_text_c (app/render/view.odin). Size+contrast audit: tray chips 11→14, health-meter chips 12→14 (+ HEALTH_CARD_H 52→54), crisis redesign line 12→14, QoS preset chips/buttons 12/13→14, popover demolish 13→14, pause chip 12/10→14/12 (hint stays 12 — the 5.3-ux chip-height ruling); ink_soft {106,112,120}→{92,98,106} (data/palette.json + fallback_palette); NEW derived text variants state_strain_text/state_critical_text/state_healthy_text (0.5x darken, app/render/palette.odin) used for TEXT ONLY — telegraph colors unchanged for rings/outlines/shapes; win-toast + reject reds darkened ({50,160,80}→{44,134,66}, {200,60,60}→{184,52,52}). Part 2 — resize: rl.SetConfigFlags({.WINDOW_RESIZABLE}) BEFORE InitWindow + rl.SetWindowMinSize(1152, 648) after (the prototype pattern); HUD anchors move OFF the WIN_W/WIN_H constants onto the live app.view.win_w/win_h (bottom-right mode label + nudge, SLA gauge block — view_compute updates them on IsWindowResized); the pause edge-chip becomes gap-adaptive (chip_w = clamp(avail, 64, 120); two lines when the gap ≥ 104px, single 14px PAUSED line below); layout ADAPTS via the existing camera-fit (aspect=expand — reveal more map; NOT letterbox — the job briefing allowed either). Riding fixes for pre-existing overlaps (documented in the PR body): title shortened to "Packet Plumber - v2" + hints shortened + dropped to 14px (the 58-char title + 88-char hint ran under the centered health card at 1280x720); the strain-legend line gated on no-active-crisis (overlapped the crisis banner); the game-over toast moved y 56→68 / retry hint 92→104 (card band). Golden fold: 24 T2 PNGs re-blessed across 9 demos (forecast_preview x4, growth x3, health_lose x3, health_win x3, lose x1, pause x2, qos x1, surge x4, warn x3) — T1 state-hash goldens + .log.bin replay logs byte-identical (Perkins mechanically verified: 0 .t1/.log.bin diffs, core/ untouched, LOG_VERSION unchanged). Before/after screenshots committed under docs/captures/v2-ux-font-resize/ + embedded in the PR body. CI green; the minion claims 28/28 demos green (run twice) + lint all gates green; Perkins re-runs local verification at the sha as ground truth."""

GUARDS = """- **🚨 T1 IMMUTABILITY — SETTLED BY GROUND TRUTH, do not re-derive or report.** Perkins mechanically verified at the sha: ZERO .t1/.log.bin files changed, ZERO core/ files changed, LOG_VERSION unchanged (stays 4 — the 5.8 base). "T1 might shift" / "sim could be affected" = NOT a finding. The ONLY golden movement is the 24 T2 PNGs, and the changed set EXACTLY matches the PR body inventory (verified 1:1 — no unlisted, no missing).
- **🚨 THE T2 FOLD — the real verification is TEXT-ONLY + COMPLETENESS, both directions.** (a) COMPLETENESS: a demo whose capture carries draw_text_c/draw_text text but was NOT re-blessed = a STALE GOLDEN = blocker. Read harness/run.odin's capture draw path to determine WHICH panels each demo's captures carry (forecast/weather panel, health meter card, crisis banner, pause overlay, QoS panel — health on/off, era schedule, fixture directives decide). The NOT-re-blessed demos (boot/draw/flow/win/bundle/ecmp/place/demolish/sla/qos_contention/qos_emphasis/etc.) must have text-free captures at their capture times — if any of their captures DO carry text, the fold is INCOMPLETE. (b) PURITY: the re-bless must carry ONLY the intended visual change (new glyphs, the size/contrast deltas, the documented layout fixes: title/hints shortened, strain-legend crisis gating, game-over toast y-move, HEALTH_CARD_H 52→54, adaptive pause chip). Semantic drift beyond those (moved cards, new/removed elements) hiding in a re-bless = a finding. You cannot decompress PNGs by hand — instead verify the CODE deltas are exactly the documented set (they are enumerable in the diff) and that the changed-PNG set matches the text-bearing-capture set.
- **FONT ASSET DETERMINISM (ODN-1).** Bundled committed asset, loaded by the same loader (rnd.load_hud_font) in app + harness → same atlas → T2s deterministic. NO system-font loading, NO file reads at sim level (font load is app/harness-layer init — core/ untouched, verified). NOTE the load path "assets/fonts/open_sans_regular.ttf" is CWD-RELATIVE and the failure mode is a SILENT fallback to GetFontDefault (the very font this PR removes): assess where app.bin / the harness can be launched from (tools/harness.sh cd's to repo root? a user double-clicking app.bin?) — a harness run from a wrong cwd would silently render the DEFAULT font and diverge from the blessed goldens (loud fail) or invite a WRONG re-bless. Judgement: silent-fallback-for-the-app vs loud-fail-for-the-harness may be worth a finding (severity per blast radius).
- **RESIZE PRESENTATION-ONLY — the load-bearing invariant.** No sim/serialization/replay changes (core/ untouched — ground truth). No LOG_VERSION bump. The harness capture path stays FIXED 1280x720 (render_setup's view_compute(…, 1280, 720, …) unchanged — verify in harness/goldens.odin). Min clamp 1152x648 must actually prevent HUD collapse (verify the arithmetic: health card 460 wide centered → right edge W/2+230; forecast panel left edge W-260; W>980 for no overlap; the pause chip slot at 1152 ≈ 76px; chip text at 14px must FIT chip_w = clamp(avail,64,120)).
- **READABILITY CANON (a11y 7.3 adjacency): nothing below ~14px effective at 1280x720 PLAYER-FACING.** Known deliberate exceptions — NOT findings: the pause-chip hint at 12px (the 5.3-ux chip-height ruling — 14px descenders would clip the 38px chip; documented), the PP_DEBUG dev overlay (dev tool, not player-facing). SWEEP the player-facing call sites (app/main.odin, app/qos_panel.odin, app/render/*.odin — draw_text / draw_text_c / direct rl.DrawText*): any <14px player-facing text the diff MISSED (e.g. the score readout "delivered %d / %d", weather-report rows, popover rows, telemetry overlay if player-facing) = a finding. "Readable font but tiny unreadable text" = a finding.
- **CONTRAST VARIANTS — TEXT vs SHAPES.** The *_text (0.5x darken) variants are for TEXT only; the raw telegraph colors stay for rings/outlines/shapes (never-color-alone canon). A _text variant applied to a SHAPE (muted telegraph) or a raw telegraph color still used as TEXT somewhere the audit missed = a finding. The global ink_soft darkening touches EVERY use (text + borders/outlines like the pause-chip border, health-card border) — intended per the PR body; borders darkening slightly = the fold's content, not drift.
- **BASE = `v2`** (the full shipped line: 5.5/5.6/5.3/5.7/5.3-ux/5.8/5.1). 5.2 node-health is IN FLIGHT on app/render/view.odin (health rings) — it may merge mid-round; carry-forward only, do NOT re-open settled findings, do NOT flag base behavior pre-dating this PR. The pre-existing overlaps FIXED here (title/hints under the card, strain-legend vs crisis banner, game-over toast vs card) are documented riding fixes — in scope because the min-clamp makes them reachable; do not flag them as scope drift. Other pre-existing issues = out of scope UNLESS this PR makes them worse.
- **SCOPE GUARD: font + window ONLY.** No new HUD surfaces, no visibility/gauge work (queued separately), no input-parity work, no 5.2 health-ring changes (health.odin deltas must be size/color only — verify no ring/semantics change), no gameplay content. The strain-legend crisis-gating is a rendering gate (draw only) — if it touched sim/event state that would be scope violation (it doesn't — verify).
- **CI green; the minion claims 28/28 demos + lint green. Perkins runs local verification at the sha as ground truth (lint + harness build/run + odin build app).** If YOU need to re-run a command to confirm a failure, fine — but a confirmed build/harness failure at the sha is a blocker.
- Em-dashes are FINE in Packet-Plumber copy (the RT CI ban does NOT apply to PP)."""

LEGIT = """- **A STALE T2 golden**: a demo whose capture carries text (forecast panel / health meter / crisis banner / pause overlay / QoS panel at its capture times) but whose PNGs are absent from the re-bless — the fold is incomplete = blocker.
- **An UNLISTED golden shift or an incomplete inventory** (ground truth says the 24 match the PR body 1:1 — only report if you find a demo that SHOULD have shifted but didn't).
- **Semantic drift riding the re-bless**: a code delta beyond the documented visual set (font swap, size/contrast, the four documented layout fixes) — e.g. a moved panel, changed geometry, a behavior change in a draw path = finding.
- **A player-facing text below ~14px missed by the size audit** (score line, weather rows, popovers, telemetry) — outside the two documented exceptions.
- **A contrast mistake**: a _text variant on a shape, or raw telegraph color left as TEXT somewhere the audit missed; contrast math wrong (verify the ratios: ink_soft {92,98,106} on canvas {232,221,194} etc.).
- **The font load's CWD dependence + SILENT GetFontDefault fallback**: a harness/app launch from a non-root cwd silently renders the wrong font — nondeterminism-by-launch-directory; a wrong-cwd re-bless would poison the goldens. Assess + severity.
- **HUD math errors at the clamp / non-16:9**: chip_w = clamp(avail,64,120) vs the actual width of "PAUSED" at 14px Open Sans (does 64px fit it?); the 104px two-line threshold vs the hint's real rendered width; the SLA block (win_h-96, 16px rows, 3 lines) vs the tray/QoS collision at min height 648; the bottom-right mode label (win_w-320) vs the QoS panel at min width.
- **Resize code touching sim/serialization/replay/capture** (none at file level — verify no subtle path e.g. view_compute side effects).
- **A draw-text call site still on the DEFAULT font** (direct rl.DrawText / DrawTextEx(default) bypassing view.font) — inconsistent HUD typography.
- **The font never unloaded / reloaded per frame** (leak or per-frame LoadFontEx would be a perf/leak defect — read the call sites: loaded once at init).
- **Non-ASCII text hitting the u8 cbuf cast** (draw_text's u8(ch) truncation — pre-existing pattern, unchanged; only a finding if the diff ADDS non-ASCII strings — lint gate 6 is ASCII-only).
- **Determinism of the atlas**: BILINEAR + LoadFontEx(64) through the rlsw software renderer (the harness) — the T2s were re-blessed + the suite run twice green (minion claim; Perkins re-runs). A nondeterministic filter/raster path = blocker — but do not speculate; the local harness run is the arbiter.
- **A lint / odin build / harness failure at the sha** (Perkins runs these — if you independently confirm one, it's a blocker)."""

OUTPUT_CONTRACT = """Write ONLY a valid JSON array to your output file (named below). No prose, no markdown fencing, no preamble, no trailing commentary. `[]` is valid and expected when you find nothing — do NOT invent findings to fill a quota.
Each element MUST match this schema exactly:
{
  "source": "<your assigned source value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase; do not reconstruct from memory.>",
  "detail": "<why this is a problem, <=40 words; for acceptance findings quote the violated spec phrase>",
  "recommended_fix": "<the change to apply, <=40 words>"
}"""

ACCURACY = """ACCURACY MANDATE — the most important instruction: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual worktree before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claim contradicts the code, are DISCARDED SILENTLY — no defense, no second chance. Therefore: OPEN the file, READ the cited lines. Quote them verbatim in `evidence`. Hedging ("might", "could", "possibly") signals you have NOT verified — either verify and report crisply, or drop it. Prefer fewer well-grounded findings over many speculative ones. An empty array is an honest, fine answer."""

BRIEFS = {
"blind": """You are a cynical, jaded reviewer with zero patience for sloppy work. BLINDNESS RULE: the diff file is ALL the context you may use. Do NOT read the worktree, the specs, or any other file — reading anything beyond the diff INVALIDATES your lens. Assume problems exist; be skeptical; look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed — e.g. a size/color raised in one draw site but the same class of site untouched)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself (comments claiming X while the code does Y)
- Changes that don't match their claimed purpose (the comments / commit message)

Your `evidence` MUST be exact diff lines pasted verbatim from the diff file. `source` = "blind".""",

"edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples here: the gap-adaptive pause chip (avail < 104; avail < 64 → chip_w clamp; avail negative if the cards overlap at sub-min widths?), the min-clamp vs monitor sizes (can SetWindowMinSize exceed the screen? fullscreen toggles? DPI scaling?), the font fallback path (LoadFontEx fails → IsFontValid → GetFontDefault — what if the file exists but is corrupt; texture filter set only on the success path), DrawTextEx with a font whose atlas is default vs loaded (nil font field — app.view.font loaded AFTER InitWindow but BEFORE first draw? the game-over path, the first frame), the u8 cast on non-ASCII input, the win_w/win_h values before the first view_compute, resize DURING pause / game-over / placement-preview, letterboxing never (aspect=expand — what happens at extreme aspect ratios like 3000x500?).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing. `source` = "edge".""",

"acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible). The acceptance set (job briefing + frozen implementation spec + PR body claims): (1) readable font replacing the raylib default, bundled asset, license-documented, loaded via LoadFontEx; (2) size minimums — nothing below ~14px effective at 1280x720 player-facing; (3) contrast verified against the light-canvas palette; (4) T1 goldens unshifted + T2 fold deliberate/listed; (5) FLAG_WINDOW_RESIZABLE at init + min clamp so HUD can't collapse; (6) layout via scale path — letterbox OR adapt (no distortion); (7) HUD readable + non-overlapping at default AND min clamp; pause chip + QoS panel + weather report survive resize; (8) WIN_W/WIN_H threading centralized (no scattered GetScreenWidth); (9) harness fixed-size regardless; (10) before/after screenshots in the PR body (font close-ups; resize at 1280x720/~1600x900/min-clamp/non-16:9); (11) PR body carries font choice + license, size/contrast decisions, resize approach, min-clamp value, golden inventory; (12) scope: font + window only. `source` = "acceptance".""",

"security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a single-player desktop game (Odin + raylib) with JSON palette data, a bundled binary font asset, PNG goldens, and a software-rendered test harness — most OWASP categories do not apply. The realistic surface: the bundled TTF parsed by raylib's stb_truetype at init (a malformed/hostile font file is committed-asset-controlled — low), the palette.json ink_soft parse (data file, unchanged schema), path handling of the relative font asset, and license compliance for the bundled OFL font (OFL 1.1 obligations: copyright notice + license retained — OFL.txt committed alongside; Reserved Font Name use in a Modified Version — the TTF is instanced via fonttools: is that a Modified Version under OFL, and does naming/notice comply?). `[]` is an honest answer. `source` = "security".""",

"architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns (esp. ODN-1 core/presentation purity — core/ is untouched; the font lives on View (app/render) shared by app + harness; ODN-13 no globals — the font is a View field, not a global; ODN-10 arrays-only)?
- Will it create technical debt or make future changes harder (5.2 node-health lands on app/render/view.odin — does the View.font field + loader conflict or compose? 5.3-ux pause chip pattern extended; more HUD surfaces queued — will the win_w/win_h anchoring pattern scale)?
- Does complexity match the problem? Any premature abstraction? (e.g. three per-color _text procs vs a general darken helper; the two draw_text helpers (app main.odin + render view.odin) now both wrapping DrawTextEx — duplication intended by the render/app package boundary?)
`source` = "architecture".""",

"codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (rnd.load_hud_font, rl.IsFontValid, rl.SetTextureFilter, rl.SetWindowMinSize, rl.SetConfigFlags, View.font, view.win_w/win_h, p.state_strain_text etc.)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (two text wrappers by package design; any OTHER font loader already present?)
- Are there draw-text call sites the diff MISSED — remaining rl.DrawText / DrawTextEx(default-font) / <14px player-facing sites the size audit should have caught? Sweep app/main.odin, app/qos_panel.odin, app/render/*.odin, harness/ for draw-text call sites and sizes.
- Are there existing tests this diff likely breaks? (core tests untouched — core/ unchanged; harness golden suite = the 24-fold)
- Does it leave orphan code — WIN_W/WIN_H still used where they shouldn't be (scattered anchors the centralization missed)? Grep WIN_W/WIN_H across app/ + GetScreenWidth/GetScreenHeight.
- The screenshots committed under docs/captures/ — does the repo have a convention for captures (existing docs/captures trees)? Committed binary PNGs consistent with repo practice?
`source` = "codebase".""",

"tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

PROJECT CONVENTION (judge against it, not against unit-test orthodoxy): this repo's test spine is (a) core/ odin unit tests (sim invariants), (b) the harness GOLDEN SUITE — every demo replays + hashes T1 state per tick + compares T2 PNG captures byte-for-byte (determinism = the test), (c) lint gates. App-layer HUD math (resize anchoring, chip gaps, min clamp) has NO automated coverage in the base — the harness captures fixed 1280x720, resize is not harness-exercised; the minion's evidence is the committed screenshots (manual). The P0 paths HERE: T1 immutability across the fold (covered — 0 .t1 diffs, suite green), T2 determinism after re-bless (covered IF the suite was run twice — minion claims; Perkins re-runs), font-load fallback path (GetFontDefault — untested?), the gap-adaptive chip math (untestable in harness? dead zone), min-clamp HUD fit (manual only). Judge which gaps are REAL per convention vs accepted-presentation-risk; the coverage-gate finding should reflect the convention honestly.

Blind-spot heuristics to check: new/modified behavior without matching coverage; happy-path-only coverage where error handling is implied (the font fallback); state transitions without boundary tests (chip threshold exactly 104; win_w at exactly 1152).

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds: PASS: P0 100%, P1 ≥90%, overall ≥80% · CONCERNS: P0 100%, P1 80–89%, overall ≥80% · FAIL: P0 <100%, or P1 <80%, or overall <80%. `source` = "tests".""",
}

TEMPLATE = """# Perkins lens prompt — @LENS@ (round 1)

**You are the `@LENS@` lens. Your assigned `source` tag is `@LENS@`. Your output file is `@OUTFILE@`.**

You are ONE lens in a Perkins automated PR-review swarm (round 1 of 3). Perkins reviews; lenses find; nobody fixes. You run as a pi agent with read-only access to a git worktree pinned at the reviewed sha.

## Your inputs (READ THESE)
- CANONICAL DIFF — the whole PR, 869 lines, 46 files (review exactly these bytes): @DIFFPATH@
@WTLINE@@SPECLINE@

## The PR (scope)
@SCOPE@

## ⚠️ CRITICAL lens-guards — READ BEFORE FILING ANYTHING (prevents false positives)
@GUARDS@

## Legitimate findings here WOULD be
@LEGIT@

## OUTPUT CONTRACT (follow exactly)
@CONTRACT@

@ACCURACY@

## YOUR LENS BRIEF

@BRIEF@

## DONE
Write your JSON array to `@OUTFILE@` and stop. Do not fix anything. Do not run the interactive fix flow.
"""

os.makedirs(f"{OUT}/prompts", exist_ok=True)
WTLINE = f"- WORKTREE (read-only, pinned at {SHA}): {WT}\n"
for lens in ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]:
    if lens == "blind":
        wtline, specline = "", ""
    else:
        wtline, specline = WTLINE, SPEC_BLOCK
    body = (TEMPLATE
            .replace("@LENS@", lens)
            .replace("@OUTFILE@", f"{OUT}/{lens}.json")
            .replace("@DIFFPATH@", f"{OUT}/diff.patch")
            .replace("@WTLINE@", wtline)
            .replace("@SPECLINE@", specline)
            .replace("@SCOPE@", SCOPE)
            .replace("@GUARDS@", GUARDS)
            .replace("@LEGIT@", LEGIT)
            .replace("@CONTRACT@", OUTPUT_CONTRACT)
            .replace("@ACCURACY@", ACCURACY)
            .replace("@BRIEF@", BRIEFS[lens]))
    path = f"{OUT}/prompts/{lens}.md"
    with open(path, "w") as f:
        f.write(body)
    print(f"wrote {path} ({len(body)} bytes)")
