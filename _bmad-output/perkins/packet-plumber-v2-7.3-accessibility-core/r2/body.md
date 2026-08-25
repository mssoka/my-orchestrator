## 🤖 Perkins automated review — round 2 of 3

**Job:** packet-plumber-v2-7.3-accessibility-core · **Round:** 2 (loop-until-APPROVED)
**Reviewed sha:** `217f6a8ec03d7b75914fd005f15bc8de4e248ec8` (head of `v2-7.3-accessibility-core`, base `v2`)

**Reviewers:** 7/7 per chunk × 2 chunks (14/14 lens outputs landed; 6 chunk-rest lenses re-dispatched once on the sanctioned `glm-5.3` fallback after kimi k3's billing 403 mid-wave — no lens failed twice).
**Verification:** 100/100 lens findings survived code re-verification (0 discarded as false-positive), deduped → 40 unique. Fix audit: **5 of 6 r1 blockers verified FIXED, 1 regressed** (B2). Mechanical gates re-run by Perkins: `tools/ci-local.sh --mac` **10/10**; gate 2 = 205 core + 12 settings + 11 hud + 2 oracle tests green; palcheck poison → FAIL (exit 1, restored); goldens byte-verified pure-presentation (`.log.bin`/`.t1` identical to juice; no pre-existing golden touched; no `core/`, no LOG_VERSION, no catalog edits); vision-read (qwen3.8-27b) on the ×1.50 crisis golden **PASS**.

### r1 fix audit (the round's bar: each fix BITES)

| r1 blocker | verdict |
|---|---|
| B1 keyboard panel surface | ✅ **FIXED** — S/arrows/Enter collected; modal emit drives the panel; S-ownership coherent (no silent lane reassign — phase-2 blocked while open + executor `sel_pipe` gate); parity row-1 assertion bites |
| B2 touch scale cycle | ❌ **STILL PRESENT (regressed)** — see blocker 1: the tap path is now a *no-op*; a touch-only player cannot change palette or scale **at all** |
| B3 settings persistence coverage | ✅ **FIXED** — 12 real tests, full failure matrix, green in gate 2 |
| B4 ×1.50 banner occlusion | ✅ **FIXED** — clamp + proportional text; unit-pinned incl. never-engages-≤1.25; geometry re-derived (banner 375–905 vs forecast 920 @×1.50, 15px gutter); vision-verified |
| B5 QoS action-row mis-hit | ✅ hit-side **FIXED** (all rects scale, single-source, 10–15px gaps @×1.25/1.50) — but the rework left the draw loop raw → **new blocker 2** |
| B6 test gate | ✅ **FIXED locally** — oracle poison/clean legs ship and bite; 4 binaries in gate 2; (workflow drift → warning 5) |

### BLOCKERS (4)

1. **`still present since round 1 (B2, regressed)` — delta-0 activate is a NO-OP on the palette + scale rows: touch row-taps, mouse row-clicks, keyboard Enter and pad A can never change them** · `app/main.odin:796` + `app/input/exec.odin:72` + `app/settings.odin:149` · [perkins, architecture, edge, tests]
   `settings_click` passes `delta=0`; Enter and pad A emit `Settings_Activate{delta=0}`; `cycle_scale/cycle_palette(cur, 0) == cur` (the shipped test even pins "a zero delta holds the step"). Touch has no ±gesture, so palette+scale are **unreachable for a touch-only player** — worse than r1's one-way ratchet. The PR claim "a touch-only player can always get back (150% → 100%)" is false as shipped; so is the in-code comment "a delta-0 tap advances". Perkins probe (temp test, deleted): both expects **FAILED** — the step and mode did not change. *Fix: normalize `delta==0 → +1` for the cycle rows at the adjust site (or make the cycles advance on 0), and pin the tap path.*
2. **QoS manual editor: weight values render INSIDE the [−] buttons at ×1.25/×1.50 — the B5 rework scaled the hit rects but left the draw loop raw** · `app/qos_panel.odin:351,361` · [edge, acceptance, codebase, blind, architecture]
   Draw loop: `x := QOS_PANEL_X + 8 + lane * 96` raw, value at raw `x+44`, raw font 14 — while `qos_nudge_rect` scales through `hud()`. At ×1.25 the minus rect spans 50–75 and the value draws at 64 (inside it); at ×1.50 lanes 1–2 values land on/near the previous lane's [+]. "Chrome stays legible at each step" fails on the exact surface B5 reworked. *Fix: derive label/value positions from the same scaled rects.*
3. **`linear_to_srgb` is mathematically wrong in BOTH the committed derivation script and the palcheck simulator — it divides instead of multiplies and branches at the forward threshold** · `tools/derive_a11y_palettes.py:40` + `harness/palcheck.odin:45` · [blind, perkins]
   Shipped: `c / 12.92 if c <= 0.04045`; correct inverse: `c * 12.92 if c <= 0.0031308 else 1.055·c^(1/2.4) − 0.055`. Dark linear outputs crush to ~0 instead of their true sRGB values (linear 0.02 → 0, not 43). The derivation record does not implement the claimed Machado sRGB↔linear pipeline, and the oracle measures separation in the same wrong space — the pinned min sim-dists (51.3/54.7/43.0) and the CI separation guarantee are computed under a broken codec. *Fix both files, re-verify separation, re-derive/re-bless if values move.*
4. **Advisory test gate: FAIL** · [tests ×2 chunks]
   P0: the delta-0 activate path is a live no-op **and** unpinned; modal world-input suppression + the S-ownership gate unpinned. P1 ≈80% (persistence FULL, hud helpers FULL, oracle negative legs landed); parity remains blind to app-side adjust effects — which is exactly how blocker 1 escaped CI green. Overall ~78%.

### WARNINGS (16) — new, then carried

- **QoS preset chips double-scale their x offset** — 3rd chip overflows the panel card +48px @×1.25, +126px @×1.50 (`w` computed scaled, then `i*(w+4)` re-scaled through `hud()`); hit==draw so still clickable [acceptance, codebase]
- **QoS draw-side leftovers**: lane proportion bar raw (`QOS_PANEL_X+118`, raw h/width math) collides with the scaled lane label @×1.25+; queue-depth label unscaled [edge, acceptance, codebase]
- **S is a dead key while the panel is open with a pipe selected** (opened via chip tap / pad Y); footer "S / tap chip to close" false in that state — Esc/Y/B still close, never trapped [blind, architecture, edge, acceptance, codebase]
- **Settings hit-test semantics in three hand-synced copies** (app `settings_click`, the parity twin, the documented single-source rule); the parity twin models no adjust — the blind spot behind blocker 1 [architecture, blind]
- **`.github/workflows/ci.yml` gate 2 still runs only `odin test core`** — the 4-binary gate is local-only; ci-local.sh's own header says the workflow is the spec; remote CI will skip 25 of the new tests when Actions unblocks [codebase]
- **Harness `banner_y` raw vs the app's hud-scaled placement** — the ×1.50 golden under-pins the app's banner position (y=70 golden vs y=105 app with health on) [edge]
- **Audio row never persisted** though `effect_settings_adjust`'s comment claims every change lands in the settings file [blind]
- **Modes never restyle `host_body/host_roof/router_body/router_dark/router_led`** — the spec's frozen Always clause lists "roofs/host/router tones" [blind, edge, acceptance]
- **hud_test's zero-scale pin is vacuous** — it re-implements the guard inline instead of calling `view_compute` [blind, tests]
- **Modal suppression / S-ownership / pause-on-open untested** [tests]
- *still present since round 1:* SLA row pitch+rect unscaled; draw_hud y anchors; popover height/text; parity never under a11y mode/scale; ×1.25 unpinned + 1152×648 AC never exercised (goldens.odin now *supports* `scale 125` — dead path); muted-captions contract unpinned

### NOTES (20)

Phase-1 buffer `[10]Key` holds 10 of 11 collectible keys; forecast/health backdrops clip the top edge @×1.25+ (raw `y=10`); node-health card has no x-clamp; `input.odin:59` says `SETTINGS_ROWS`; "byte-for-byte untouched" is value-true/byte-false (whitespace + `_comment`); 6 hand-synced juice scene copies (incl. juice's own duplicated 100ms line); `Demo.a11y_palette` u8 ordinal coupling; derive script wired into no gate; Machado matrices+thresholds duplicated script↔oracle; gate-2 label understates; + carried: threshold-by-color-value, `roofs_set` before validation, spec doc drift, dead code (`strings` import, `PALETTE_MODE_COUNT`, derive helpers), `_pr_body.md` tracked, "// 16. pause" comment, no presence scans for reduced/scale goldens (+ parser error legs), placing-armed + panel mouse dead, pulse-seam duplication, additive checksum.

### Reviewer agreement

Blocker 1: **4 sources** (perkins probe + 3 lenses) — probe-confirmed with a failing test. Blocker 2: **5 lenses** independently. S-dead-key: 5 lenses. Parity-under-a11y-modes: 5 lenses. Preset/QoS scale leftovers: 3 lenses.

### Verdict

**MAJOR REWORK — REQUEST CHANGES (4 blockers).** The r1 architecture held and 5 of 6 fixes genuinely landed, but B2 regressed into a hard input-dead surface for touch players, the B5 rework introduced a draw-side twin of the bug it fixed, and the CVD derivation math is wrong in a way its own oracle shares. None of these are reachable by the current CI — which is itself part of the finding.

_Address findings and push — I re-review automatically on the new sha._
