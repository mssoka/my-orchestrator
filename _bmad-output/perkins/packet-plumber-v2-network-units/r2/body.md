## 🤖 Perkins automated review — round 2

**Job:** packet-plumber-v2-network-units · **Reviewed sha:** `1cb1b4b` · **Reviewers:** 7/7 completed
**Verification:** 17/20 findings confirmed against the code — 3 discarded as false-positive

### Fix audit (r1 findings @48c0e82 → this head)

| r1 | status | evidence |
|---|---|---|
| **B1** queue-row util%/count glyph collision | ✅ **FIXED — mechanically proven** | fontTools on the shipped TTF (600/1000-em advance) + new constants (pitch 104, bar 64, util_r px+416): count-digit ink [351.2, 359.7], `"100%"` first-ink 373.8 → **12.95 px clearance** vs r1's −4.8/−5.0 px overlap. The commit comment's figures verified to ±1 px. KYLE re-read rides the PR as minion evidence; the font math is definitive. |
| **W1** derived 67/100/267 ladder | ⏸️ **HELD by design** | Untouched this fold, escalated to the user — per the round briefing, not re-litigated. Merge still wants the user's ladder ruling. |
| **W2** tx-ring zero direct tests | ✅ **FIXED** | `bundles_test` +98 lines: exact-W expiry, slot-reuse stale-check, same-tick duplicate class, rebuild reset, no-write, bounds — all green. |
| **W3** predicate swap undiscriminated | ✅ **FIXED** | 89/90-boundary + cap-0 + carried-saturated-at-util-0 discrimination pins + amber-boundary pin. The old `carried>=cap` predicate is provably dead. |
| **W4** advisory gate CONCERNS | ✅ **LIFTED → PASS** | tests-lens re-triage: P0 100%, the r1 P1 gaps closed. |
| N1, N2, N4, N5, N6, N8, N9, N12 | ✅ **FIXED** | zero-cap→no-rate (pinned), 112px comments, catalog-driven headers/predicates, stream v2 marker, self-consistent CSV fixture (util 16 / tx 7500 re-verified), dead proc removed (grep: 0 refs), re-step class documented + pinned, Bundles doc corrected. |
| N3 (node_health stale comment) | ⚠️ **still present** | …and a second, older stale instance found at `node_health.odin:~40` (pre-PR `"util 150% (load 120 / 80 u)"`). Note-level, carried. |
| N7 (bps-tier pins) | ⚠️ **still present** | opportunistic note, unchanged. |
| N10, N11 | ➖ carried | spec-interpretations; no fix required, documented. |

### Round-level verification (not assumed — run on this head)

- **13/13 local CI gates PASS** (`tools/ci-local.sh --mac`, native) — incl. gate 4 (golden T1 hashes + T2 software pixels + replay gate) and gate 12 (**stats live==replay byte-identical**: pause 376,621 B, qos_contention 72,869 B).
- **Zero golden movement**: harness 48/48 demos green; `git status` clean on `goldens/` + `data/`; no data-file bytes in the diff. MM-pace held — `transit_ticks(120,15)==8` pinned; SIM_TIME_SCALE named.
- **E9/E22 unchanged** (6 packets / 512 pool; balance.json untouched). **LOG_VERSION untouched**; the tx ring has 0 references in `state_writer`/`state_hash` (derived, replay-rebuildable).
- The fix commit does not touch the honest-util path — r1's formula verification stands; measured-window pins green.

### Blockers (0)

None.

### Warnings (1)

- **W5 — NEW (fix-commit): queue-row measure/draw twins diverge at `amber_pct==0`** [blind, edge, acceptance, architecture, codebase, tests] — `noc_overlay.odin:598-606 vs :771`. The `amber_pct > 0` guard exists only in the measure pass; the draw loop's `p.util_pct < u32(amber_pct)` never skips at amber 0 (u32), so measure counts only queued pipes (the new test pins exactly this) while draw renders **every** pipe — violating the file's own "MUST agree row-for-row" scroll-clamp contract. Latent: shipped catalog pins amber=70 (fail-fast validated); only a catalog tune to 0 manifests it. The PIPES twins got the guard on both sides; QUEUES got it on one. Fix: mirror the guard at the draw site.

### Notes (9)

- **N13** [blind, architecture, codebase] — the shipped implementation-spec artifact still lists the **removed** `line_rate_bytes_per_tick` and a stale 4-param `util_pct_window` signature (code has 3 params) — the artifact contradicts this very fold.
- **N14** [codebase] — PR body r2-fold header cites sha `8a6f3f5`, which does not exist in git (the fix commit is `1cb1b4b`; stale pre-amend sha).
- **N3+** [blind, codebase] — *still present since round 1* — node_health stale trace-format comments, now at two spots (`:~40` and `:~108`).
- **N15** [blind] — select-readout row-count comment still says "offered + carried"; the rows are rate/util + tx/q/dropped (count of 4 is right, names stale).
- **N16** [blind] — `bundle_tx_window` lacks `bundle_tx_record`'s ring-length guard (harmless under the rebuild sizing invariant; parity nit).
- **N17** [tests] — spawn_fx shadow-clone: `sfx_hash` rides `state_writer`, which excludes the tx ring — the unit round-trip can't see ring-clone corruption (the clone itself is present and correct).
- **N18** [tests] — the stats stream v2 header marker text is unpinned by any test.
- **N7-carry** — *still present since round 1* — sub-Kbps/bps formatter tiers unpinned (opportunistic).
- **GATE** — Advisory test gate: **PASS**.

### Reviewer agreement

- W5 amber=0 measure/draw divergence — **6/7 lenses** (highest-confidence signal; independently confirmed by orchestrator code-read).
- N13 spec-artifact drift — 3 lenses. N3+ node_health comments — 2 lenses.

Rejected as false-positive: tick-0 ring-sentinel collision ×2 (unreachable — both callers increment the tick before stepping; r1's rejection re-verified) and a font-metrics counterclaim (the 8.156 px figure contradicts this pipeline twice over — raw advance is 10.8 px and MeasureTextEx at spacing 1 gives `"100%"` = 46.2 px; collision-freedom holds under every reading).

**Verdict:** READY TO MERGE

_All r1 blockers/warnings are fixed or lifted; the one new finding (W5) is a latent, catalog-tune-gated display-contract nit that does not block. W1 (the derived 67/100/267 ladder) stands untouched by design and awaits the user's ruling at merge. Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
