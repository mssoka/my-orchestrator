## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-5.11-terminal-types · **Reviewed sha:** `a2dc66e` · **Reviewers:** 7/7 completed (7 waves × 7 lenses — big-diff chunking: code + new-goldens/re-bless groups; 43,427-line diff)
**Verification:** 23/70 raw findings survived code re-verification + curation (1 blocker · 4 warnings · 18 notes) — 19 discarded as false-positive/artifact/pre-existing design, the rest merged as cross-wave duplicates. Perkins independently reproduced the fold (`66c4324a06058860 → 250679b1940fb87b`, exact, via the real core proc), the tick-1 splice proof (spliced dump byte-identical to old; hash `6c24e9cec592aece` exact), the 8-byte-only `.log.bin` diffs (32/32), the png partition, and the local suite (10/10 gates, 193 tests, 33 demos, drift 233/233).

### Blockers (1)
**1. W9 re-pin doesn't bite for the campus era** — `core/demand_test.odin` `test_w9_surge_lands_under_caps` [blind, codebase, tests, acceptance]
- `EXPECTED := 10 * WINDOW` is stale: era 3 now carries **two** ×10 streaming entries (content_host **and** campus ⇒ 20/tick ask) — MIN_LAND is ~47.5% of the honest floor.
- `stream_spawned` accumulates ticks `1..=SURGE_END` — ~1199 pre-surge base ticks pad a floor labeled "window spawns".
- The crowd floor (≥8 streaming-capable) never requires a **campus** to exist or source — a campus-silent regression passes.
- **Probe (verified):** with the honest doubled ask, the pin FAILS today — 31,611 < 34,200 (87.8% < 95%). This is the 5.9-W10 vacuous-pin class; the PR's "MIN_LAND … re-verified from the sim" overstates the re-pin.
**Fix:** derive `EXPECTED` from the entries (20×WINDOW), gate `stream_spawned` to the surge window, assert ≥1 campus present + campus in-window spawns > 0, update the stale message; re-tune until the honest pin passes (cause-document if 95% is unreachable).

### Warnings (4)
1. **palcheck oracle not extended to the #65 sprites** — `harness/palcheck.odin` scans house/host hexes only; a degenerate/cropped small_biz/campus blit passes all 10 gates (the exact bug class palcheck was created for). Add the new canon hexes over a `terminal_types` frame.
2. **`>10×` campus/home ratio is knife-edge + surge-dependent** — measured 10.46× (4.6% margin); base-window-only ratio ≈6.5× — only the surge pushes it past 10×, so the pin doesn't isolate the base spectrum and silently stops biting on retune. Assert base and surge windows separately (or derive from the accrue constants).
3. **PR body missing the `[E10]` and `[E31]` citations** — AC3 requires `[ODN-5] [ODN-7] [E10] [E31] [E9.1]`; only ODN-5/ODN-7/E9.1 present.
4. **Role-absent demand inertness has no durable pin** — "entries whose role has no live terminal spawn nothing / draw no rng" (the re-bless's key invariant) is a one-time byte-check in PR prose, not a test. Add an era-3 unit pin (no small_biz/campus live ⇒ spawn counts + rng draw-count identical to the pre-5.11 entry set).

### Notes (18)
- Stale burst message "(2 = ceil_cap)" — the check is per-type now (host 2, campus 3) [4-lens agreement]
- SPRITE_COUNT comment still says the 5.11 sprites are "not yet wired" — contradicted by this PR
- Era-2 roster loop omits the `kind == .Terminal` assert its era-1/era-3 siblings carry
- Health-ring radius (0.874–1.140 t) sits inside the campus half-footprint (1.10 t) for most of the pulse — ring slices the campus sprite
- `role_from_name` small_biz/campus strings: no unit pin (NT_VALID baseline not extended)
- Primitive fallback shapes for the new roles: unreachable with the committed sheet AND zero coverage
- `test_catalog` hand-mirror not tied to `data/*.json` — profile numbers restated in three places
- `#partial switch` fallthrough in `sprite_index_building` — a future unwired role silently draws a house
- W9 envelope `WINDOW=1800` vs the inclusive 1801-tick count window (off-by-one)
- Pre-surge per-tick burst check dropped (ticks 1..1199 no longer burst-checked)
- `demand.json` `_comment` retains "surge … (10/tick)" — contradicted by the two-entry base (20/tick)
- `expect hash stable` parsed but never enforced; `terminal_types.dem` carries it on a non-frozen tail
- `node_types.json` `_comment` field-def retains "terminal_role: residential | content_host | none"
- PR body misdescribes `terminal_types.dem` ("fixture + one small_biz + one campus" vs fixture-off + 7 explicit spawns)
- Fold-splice proof exists only in PR prose — no in-repo re-runnable tool/test
- Dead house-geometry computed before the Small_Biz/Campus early return (fallback path)
- Growth type-draw composition (campus weight 4/8 of era-3 spawns) unpinned
- E9.1 sprite index mapping (role→9/10) has no positive unit assertion (the T2 golden is the only pin)

### Reviewer agreement
- Stale "(2 = ceil_cap)" message: blind + codebase + acceptance + tests (4 lenses)
- W9 counting/gating family: blind + codebase + tests + acceptance → the blocker
- `>10×` fragility: blind + tests (+ Perkins probe)
- `expect hash stable` unenforced: edge + tests
- `role_from_name` unit gap: tests across 4 waves

**Verdict:** NEEDS CHANGES

_What held up well (verified):_ the roster math (83/333/1333/2500 milli-tick — uniform 5.9 formula, era gates 2/3, appended at END), the enum/`role_from_name`/selector/growth wiring (data-driven, no hardcoding), the sprite wiring (indices 9/10, aspect-faithful blit, distinct fallback silhouettes — E9.1 confirmed visually), the entire re-bless cause chain (fold + splice + logs + png partition, all reproduced exactly), and the local suite 10/10.

_Process note (transparency):_ lenses ran on glm-5.3 (assigned) for the code wave, g1 blind/security, g5 acceptance/tests, and all of g6; deepseek-v4-flash covered the remaining golden waves after glm-5.3 hit its 5-hour quota mid-round (deepseek later 402'd; kimi 403). A first code-wave launch was mis-rooted and discarded (re-run correctly); gemma-4-e2b outputs were discarded per the model ruling (vision-only) and re-run on glm-5.3. No lens layer failed; full ledger in `consolidated.json`.


**⚠️ Reviewed `a2dc66e`, head now `11c6cf6` — a fresh round (r2) will follow on the new sha.**

_Address findings and push — I re-review automatically on the new sha._
