## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-v2-4.3-network-health · **Reviewed sha:** 8659070 · **Reviewers:** 7/7 completed (3 chunk waves)
**Verification:** 33/76 lens findings survived code re-verification (10 discarded as false-positive, 33 folded by multi-source dedupe) — every surviving finding re-read against the worktree at the sha.

**Local verification (ground truth, CI billing-blocked):** `odin test core` 153/153 green (incl. all E16/E17/E30 + no-soft-lock + restart-clean pins) · lint 6/6 gates · `harness run` 20/20 demos PASS (incl. in-run ODN-11 replay gate for both new demos) · drift-check 139/139 mutations rejected · `odin build app` clean · golden re-bless mechanically re-verified: all 18 pre-existing `.log.bin` differ in exactly the 8 catalog_hash header bytes (same lengths), all pre-existing `.t1` shift ONLY via the catalog_hash fold (zero semantic lines), zero old T2 PNGs touched; the two new manifests freeze post-terminal exactly (win: Run_Won tick 3000, frozen 3001–3040; lose: Run_Lost tick 452, frozen 453–480). LOG_VERSION stays 3 (flagged) — scope guard honored.

### Blockers (0)

### Warnings (12)

**Reviewer-agreement set (multi-source, highest confidence):**

1. **Meter card backdrop paints over the HUD title every frame** *(edge + architecture + codebase)* — `app/main.odin:713,776` | `app/render/health.odin:35-39`. The title (x 12..~705, y 10..32) is drawn before `draw_health_meter`; the card backdrop (x 410..870, y 0..52, alpha 240) washes out its right half whenever the meter is live. No golden covers the app HUD. Fix: lay out the card clear of the title (or draw backdrop first) and capture it.

2. **Strain legend paints over the crisis banner when a crisis is active with health on** *(edge + codebase)* — `app/main.odin:787-789` | `app/render/crisis.odin:37-43`. With the meter live the banner drops to y≈58..122 (x 420..870); the legend line (y 76..90, x 12..~770) draws after it, crossing the banner during the surge. Fix: anchor the legend below the banner (or right-stack) when health is on. *(Cross-PR: in-flight #42 fixes a different, adjacent HUD overlap — these two are in THIS diff.)*

3. **Grace chips render an active countdown for HEALTHY classes** *(acceptance)* — `app/render/health.odin:78`. Grace arms FULL at first demand and the chip condition reads only `grace_left > 0`, so every demand-bearing class shows "grace 20s" from tick 1 with zero breach — visible in the blessed T2s (health_win 75s: both classes healthy, both chips showing). A countdown must start on breach ENTER. Fix: gate the chip on `breach[c] && grace_left > 0`.

4. **balance.json `health` block uses truncating/wrapping `jint`** *(blind + edge + acceptance + security + codebase)* — `core/catalog.odin:714-736`. `"window_ticks": 4294967496` wraps to 200 and passes 1..10000; decimals truncate silently — against the block's own fail-fast claim, and inconsistent with `jint_strict` on the packet_types health fields in this same story. Fix: strict int + i64 range check pre-cast, plus wrapped-value reject rows.

5. **No upper bound on drain cap/severity — validation-legal data can empty the meter in one tick** *(security)* — `core/catalog.odin:729-734`. Cap ≥ 100 makes the first post-grace drain tick pass `meter_pct <= drain` → instant Run_Lost, breaking E16 "never instant" by data alone. Fix: upper-bound the cap (and severity) with fail-fast rows.

6. **`expect hash stable` is parsed but never enforced** *(edge)* — `harness/demo.odin:118,250-251` (no consumer in run.odin). A barrier regression + `harness save` would silently bless a non-frozen tail. Fix: enforce in run_demo or drop the directive.

7. **E30 exit-band hysteresis unpinned; the "band" assertion is a tautology** *(edge + tests)* — `core/health_test.odin:245-251`. `grace_left > 0 || grace_left == 0` can never fail; no test pins that a ratio inside (27,30] keeps the latch. Fix: craft a windowed ratio inside the band and assert the latch holds, then exits at ≤ 27.

8. **E16 below-cap drain rate (1/tick) never asserted** *(tests)* — `core/health_test.odin:416`. Every rate assertion demands delta == 2; the email-alone band at 1/tick runs unasserted. Fix: assert delta == 1 through the email-only post-grace band.

9. **Surge-win gate negative branches never execute with the gate enabled** *(tests ×2 waves)* — `core/health_test.odin:541-563` | `core/win_lose.odin:62-65`. The below-threshold test dies via the meter at ~255 (its own comment), so the `uptime < threshold` branch and the E24 `total == 0` guard never run with `surge_done` latched. Fix: craft a below-threshold surge end with the meter alive, and a zero-completion surge end.

10. **Health-on + active-crisis layout branch rendered in zero goldens** *(tests)* — `harness/goldens.odin`. health_lose dies pre-surge and health_win is AC-E13-silent, so the banner-offset branch (where warning #2 lives) has no blessed frame. Fix: a capture inside the surge window with the meter live.

11. **Advisory test gate: CONCERNS (P0 100%, P1 ~83%)** *(tests)* — all P0 paths pinned and green; P1 gaps are items 7–9 + the missing recharge reject row. Close them to reach PASS.

12. **`health.win_uptime_pct` is dead data — win threshold dual-sourced** *(acceptance + architecture + codebase)* — `core/catalog.odin:234` | `core/win_lose.odin:62-66`. Loaded, validated, hash-folded (shifts every golden on tune) but never read; the real threshold is run-setup `surge_win_pct` (app const 90 + demo 90). Fix: consume it as the default when run setup leaves the threshold unset, or drop it until it has a consumer.

### Notes (21)

The rest are non-blocking, mostly data-edge semantics and test-quality nits:

- **Data-edge semantics:** severity-0 class swallows `Grace_Expired` (drain==0 gate, `core/health.odin:329-344`, shipped severities 1/2); recharge==0 emits unchanged `Meter_Changed` forever and can never refill (`core/health.odin:346-354`); exit margin ≥ tolerance clamps the exit threshold to 0 (`core/health.odin:242`); `surge_done` never resets on a re-activation (latent — shipped data has exactly one one-shot surge); ring allocation = classes × window with an uncapped roster (crafted-data OOM); `tick % window` has no runtime zero-guard (load-time validation only).
- **Spec-artifact drift:** the frozen spec's `Boundaries` section contradicts its own change log in 4 places (grace 200 vs 400, 15 vs 16 routers, byte-identical logs vs 8-byte re-bless, no-drops vs 489) — the code implements the corrected values everywhere; amend the artifact.
- **Test-quality nits:** absent-when-disabled never unit-asserted (golden-level evidence exists — Perkins re-verified the fold); serialization byte-scan pin can false-match an unrelated u32==100; recharge<0 validation branch has no reject row; `check_ok` never asserts parsed health values; recovery paths (recharge/refill/exit) have golden coverage only at unit level; comment rot in health_test (grace 50/10/200/300 vs actual 400/300, ~260 vs ~5 breach); same-tick win/lose collision pinned by mechanism only (the spine order is compile-visible).
- **App/harness nits:** Game_Over win copy keys on the session flag, not the fired condition (unreachable in the shipped session); banner_y offset formula duplicated app + harness (drift risk); Game_Over screen has no automated coverage; `parse_demo` new rejection branches untested; `win goal` u64→u32 silent truncation (carried 1.4 behavior); health_win.dem header ECMP figure (125 vs 75 u/tick).
- **Design note for playtest:** the GDD MVP lose row (uptime < 90% through the surge → fail) has no dedicated terminal — but with shipped tolerances a sub-90% window implies a streaming breach → meter drain → Run_Lost, so the gap is practically unreachable. Confirm at playtest.

### Reviewer agreement

The multi-source set is warnings 1–5, 7, 12 (2–5 independent lenses each, all code-anchored and re-verified). No lens disagreement on the terminal-event barrier, drain semantics, retry cleanliness, or the golden re-bless — the load-bearing guards all hold, verified locally at the sha.

**Verdict:** READY TO MERGE

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
