## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-7.1-visual-juice · **Reviewed sha:** dbed6a3 · **Reviewers:** 7/7 completed
**Verification:** 26/29 findings confirmed against the code — 2 discarded as false-positive, 1 kept as [unverified]

**Vision caveat honored:** this cycle ran without native vision — every pixel claim below was verified **mechanically** (byte/pixel comparisons, not eyeballs). Aesthetic verdicts are deferred, not faked.

**Mechanical ground truth (Perkins-run at dbed6a3):** `tools/ci-local.sh --mac` **9/9 green** · re-bless set == your claimed 74+2 list exactly (per-demo counts match) · sampled old-vs-new pixel diffs 8.0–9.7% frame-wide (99% vertical spread) == the "~7–9% frame-wide, bounded" claim · no existing `.t1`/`.log.bin` touched (replay-identity surface clean) · no `core/`/`data/` files in the diff; camera/focus state is App-owned (`main.odin:160-173`) — **[ODN-1] view purity holds** · look-book §2 hexes land exactly everywhere (gen_sprites.py, palette fallbacks, `data/palette.json`) with a correct standard sRGB→linear conversion.

### Blockers (2)

**B1 — Sprite bbox y is bottom-up (Blender) but consumed top-down (raylib): every sprite renders mis-cropped; house bodies never appear.** `app/render/sprites.odin:sprite_blit` + `tools/gen_sprites.py:content_bbox`. Mechanically proven: the flip formula `res − y − h` matches a top-down PIL alpha-bbox of all 9 committed PNGs **exactly** (y: 113,113,113,113,110,111,109,102,95), so the sidecar y is Blender-convention; `sprite_blit` uses it unflipped. The as-drawn src window holds 24–38% alpha fill vs the correct window's 77–96% (house: 30/88 content rows). Cross-check: `goldens/juice/30000ms.png` — the "7-house neighborhood" — contains **zero** house-BODY hex pixels (tol ±8) while roof hexes appear (~150–280 px each): the bodies are cropped out; only roof-fragment slivers render. The goldens deterministically blessed the broken render, and the scratch "sprite presence" scan checked presence, not crop. Fix: emit top-down y in `content_bbox` (and regenerate sprites.json), or flip at parse. All 76 goldens change again → re-bless with the cause chain (the 4.3 discipline).

**B2 — First boot captures the camera fit while `view.world_w = 0` — the map renders displaced half a screen until the first selection change.** Boot order: `start_run` (`main.odin:261`) → `camera_set_fit` (`main.odin:575`) reads `world_w/2 = 0` **before** `view_compute` (`main.odin:272`). First frame: `sel == last_sel`, so `camera_set_selection` never fires, and `camera_update` overrides `view_compute`'s correct offsets every frame (`off = win/2 − cam·scale`, cam=(0,0)). Resize doesn't heal it; selecting anything (then deselecting) or restarting does. This violates the camera-fit contract (briefing req 5, card Given/When/Then). Fix: compute the view before `start_run` at boot (or re-run `camera_set_fit` once the world dims are valid).

### Warnings (7)

1. **×2.2 tier-band formula restated in 4 sites** [architecture, codebase] — `view.odin:290,668,799` + `crisis.odin:143`. Canon constant, 4-way drift risk; extract one helper.
2. **App-layer surfaces have zero committed verification** [tests] — camera easing, class-focus ghosting, lane-LOD branches never execute under any committed gate (`goldens.odin:65` captures at fit, no focus); the scratch pixel-scan demonstrably missed B1. The §2 palette is an objective oracle — commit a palette-presence scan gate.
3. **Alerts-as-nav zoom with no prior selection has no exit** [edge] — ESC with nothing selected doesn't change `sel`, the `sel != last_sel` diff never fires, camera stays zoomed (`main.odin:405-407`, `input/exec.odin:430-431`).
4. **Doorstep fan wraps at 15 slots; a bundle can queue 18** (3 lanes × `lane_queue_packets` 6) — packets stack at identical pixels at deep queues (`view.odin:642-650,688-694`).
5. **SLA focused-row chip idiom** [acceptance, blind] — opaque fill vs the 5.5 translucent-card chrome; hit rect (x12,w720) narrower than the drawn chip (x8,w740) (`main.odin:1250,1383`).
6. **Banner/SLA hit-tests precede `popover_click`** [codebase, blind] — where rects overlap, the popover-first swallow breaks (`main.odin:716-723`).
7. **[unverified] Advisory test gate** [tests] — lens-calibrated FAIL (P0: camera coverage); reclassified per this round's charter (view-polish scope; the card's contracted golden exists and CI is 9/9). Treat as CONCERNS.

### Notes (9)

Comment drift in `draw_packets` header (still "lane-order pile") · crisis `card_w/line_h` duplicated (rect itself shared ✓) · doorstep fan math duplicated ×2 · `banner_y` duplicated app↔harness (harness copy pre-dates this PR) · `camera_update` restates the fit formula (currently consistent) · `sprites_load` partial-failure leak + ignored bool (guarded fallback; once-at-init) · sprites.json bbox parse checks structure not value ranges, comment overclaims · no parity-hook pin for the new clicks · sprites.json loader failure modes untested.

### Reviewer agreement
×2.2 duplication (architecture+codebase) · SLA chip (acceptance+blind) · doorstep fan dup (architecture+codebase) · banner_y dup (architecture+codebase) · card constants (blind+architecture) · sprites_load leak (blind+edge) · popover ordering (codebase+blind). Highest-confidence set — B1+B2 were single-lens but independently mechanically proven by Perkins.

**Verdict:** NEEDS CHANGES

The canon, view purity, chrome idiom, never-color-alone and golden discipline all hold at the mechanical level — but B1 (the sprite canon renders broken, proven in pixels) and B2 (camera-fit broken on cold boot) must be fixed. Both are small, surgical fixes; expect a full 76-frame re-bless after B1.

_Address findings and push — I re-review automatically on the new sha._
