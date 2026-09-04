# Perkins r1 — viscomm(gauge): gauges telegraph, not snap

**Reviewed sha:** `7114bf3238e9f5c43a89733e52255dbf0ae1dcde` (canonical diff verified byte-equal to HEAD)
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests) — zero failed layers
**Verification:** 22/22 reviewer findings survived code re-verification — 0 discarded as false-positive; deduped to 13
**Model:** zai-coding-cn/glm-5.3 · **Pixel verification: MECHANICAL ONLY** (byte/hash/capture-diff + palcheck pixel scans). Aesthetic verdicts (easing feel, ghost flash quality, 0.4 s cadence) are DEFERRED for the k3 re-check — never faked.

## Independent re-verification (Perkins, this round)

| Claim | Result |
|---|---|
| `odin test app/render` / `app` / `core` | **94 / 48 / 261 — all green** (note: PR body says 91/46 — see W4) |
| Golden byte-identity (unfed gauge reads raw) | **49 demos green, zero golden diffs** — re-run in a fresh detached worktree |
| Palcheck §6 draw-path legs | **all green** (unfed raw, mid-ease EASE16-predicted edge, chunk ghost, reduced-motion snap, pool twin) |
| **Mutation leg (re-run by Perkins):** `gauge_read` eased return := raw | **RED confirmed** — palcheck §6 FAILS ×2 (health mid-ease 181 px vs ~213 predicted, raw 182; pool 45 vs ~54, raw 44) + `odin test app/render` FAILS; restored → all green; worktree left `git status --porcelain` EMPTY |
| Diff ↔ HEAD integrity | exact match (modulo index lines) |

The easing gates are **mutation-real, not vacuous** — the r1/r2 lesson held.

## Verdict: ✅ APPROVE (0 blockers)

The core contract — eased display, raw truth, deterministic tick-driven phase, golden byte-identity by construction — is independently re-verified at every layer, and the draw-path gates genuinely fail under an easing bypass. The surviving findings are durability/documentation debt on secondary surfaces: worth a small follow-up, none merge-blocking.

### WARNINGS (6)

**W1. PR body claims deferrals are recorded in deferred-work.md — no gauge entries exist** [`blind`,`acceptance`,`architecture`,`codebase`] — `_pr_body…md:95-98` + `_bmad-output/implementation-artifacts/deferred-work.md`
The two known-limitation pins (loop→feed call-site pin; SLA text draw-path pin) live only in PR prose; the register still holds only the two pre-existing entries. **Fix:** append both deferrals in the existing entry shape.

**W2. SLA eased display numbers lack a draw-path mutation leg** [`tests`] — `app/main.odin:2279,2289`
Deleting either `gauge_read` call in `draw_sla_gauges` keeps unit, wiring, golden, and palcheck gates green — the strobe silently returns on the text surfaces. The bars carry real draw-path legs (re-verified above); the SLA readouts rely on the feed-side pin only. Disclosed as deferred in the PR body, but the deferral isn't durably recorded (W1). **Fix:** move the eased-readout formatting into `app/render` and palcheck it, or pin from an app-package test.

**W3. Terminal gauge snap (r1 game-over-freeze fix) ships unpinned** [`tests`] — `app/main.odin:617`
The `gauge_reset` lives inline in main's fixed-timestep loop, unreachable by the pullback-style wiring tests — deleting it passes every gate. **Fix:** extract the terminal transition into a seam proc and pin it with the `pullback_test_app` fixture (arm mid-ease → drive → expect unseeded).

**W4. PR body verification counts stale vs shipped tree (91/46 claimed; 94/48 actual)** [`blind`,`acceptance`,`codebase`] — `_pr_body…md:33-35`
The r1 fold added 11 render tests (83+11=94) and 2 wiring tests (46+2=48) but never refreshed the numbers — they contradict the PR's own r1-fold commit message. **Fix:** update to 94/48 (or annotate as pre-fold).

**W5. PR body self-contradiction: "Roster cap 8" vs shipped 16 SLA slots** [`blind`,`acceptance`,`codebase`] — `_pr_body…md:62-64` vs `:86` + `app/render/gauge.odin:96`
The Decisions bullet states cap 8 as shipped while the same body's r1 section and the code ship `[16]Gauge_Ease`. **Fix:** rewrite the bullet to the 16-slot roster headroom.

**W6. Advisory test gate: CONCERNS** [`tests`] — P0 (byte-identity/unfed contract) 100%; P1 ≈80% (terminal snap, SLA draw seam, pool ghost leg unpinned); overall ≈83%.

### NOTES (7)

**N1.** `gauge_test.odin` stale cap-8 comments (`:29-30`, `:299-300`) vs the 16 asserted at `:301` [`blind`,`architecture`,`codebase`]
**N2.** Chunk-ghost draw block duplicated health/visibility (`health.odin:86-94` / `visibility.odin:110-120`) — extract a shared helper [`architecture`]
**N3.** `gauge_wiring_test.odin:24` imports render via `../app/render`; every sibling uses `./render` [`architecture`,`codebase`]
**N4.** Pool-bar chunk-ghost draw block unpinned — add a 6(e) chunk leg mirroring 6(c) [`tests`]
**N5.** `CHUNK_SLA_MS` wiring never exercised (0 references outside gauge.odin) [`tests`]
**N6.** Loop→`feed_drop_sites` call site unpinned (pre-existing `debug_surface_smoke` class — needs headless app-drive) [`tests`]
**N7.** `pool_fill_pct` boundary clamps (packets > cap, cap ≤ 0) untested [`tests`]

### Reviewer Agreement
W1 (4 lenses), W4 (3), W5 (3), N1 (3), N3 (2) — all multi-source findings verified against the tree by Perkins.

### Recommended follow-up (non-blocking)
One small debt-PR: the deferred-work.md entries (W1), the PR-body refresh (W4+W5), the terminal-seam extraction + pin (W3), and the SLA/pool-ghost draw legs (W2, N4) — the same shape as this round's own r1 fold.

— Perkins (automated round, glm-5.3; aesthetic re-check pending k3's return)
