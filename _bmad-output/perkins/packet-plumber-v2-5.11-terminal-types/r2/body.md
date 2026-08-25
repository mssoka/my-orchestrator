## 🤖 Perkins automated review — round 2 (cap lifted — loop until approved)
**Job:** packet-plumber-v2-5.11-terminal-types · **Reviewed sha:** `11c6cf6` (the post-#67 rebase head) · **Reviewers:** 7/7 completed (7 waves × 7 lenses on the canonical diff)
**Verification:** 39/61 raw findings confirmed against the code — 22 discarded as false-positive (re-bless-mechanics, wrong-metric, and no-evidence classes; full list in the round artifacts) · dedupe → 25 distinct

**Round-2 scope:** this round audited the REBASE DELTA (`a2dc66e → 11c6cf6`, 92 files) plus a full fix-audit of every r1 finding against the fresh tree. Delta verdict: **clean** — every delta file is either a pure #67 import (byte-identical to v2: ~78 re-blessed pngs, map/palette/harness) or canonical 5.11 content (view.odin merged cleanly: #67 map hunks + 5.11 sprite hunks). Zero scope creep. The rebuilt harness frames verified: pixel probe on the new `terminal_types` goldens shows all three class sprites present and growth placing the new types (~2× small_biz, ~3.3× campus pixels at 30 s). All 32 pre-existing `.log.bin` differ from v2 in exactly the 8-byte `catalog_hash` field — the fold re-bless is byte-partitioned exactly as cause-documented. Local suite re-run by Perkins: 10/10 gates green (193 tests).

### Blockers (1)
- **[B1 — still present since round 1]** W9 re-pin doesn't bite for the campus era (`core/demand_test.odin:521-522,543-546,596`). `EXPECTED := 10*WINDOW` is stale vs the doubled era-3 streaming ask (content_host **and** campus entries ×10 ⇒ 20/tick; MIN_LAND ≈ 47.5% of the honest floor); `stream_spawned` pads ~1199 pre-surge ticks into a window-only floor; the crowd floor never requires a campus to exist or source. Perkins probe re-run on this tree: honest floor 34200 vs actual **31611 (87.8% < 95%)** — the honest pin FAILS today, so the committed pin passes a campus-silent regression. *Fix:* derive EXPECTED from the entries, window-gate the counter, assert ≥1 campus sourcing, fix the stale message, re-tune until the honest pin passes.

### Warnings (4 — all still present since round 1)
1. **palcheck not extended to the #65 sprites** (`harness/palcheck.odin`) — no small_biz/campus canon hexes in the presence scan; a cropped blit of the new canon shapes passes every gate. The fix is mechanical (r2 pixel probe counts the canon colors in the `terminal_types` frames directly).
2. **`>10x` campus/home ratio is knife-edge** (`core/demand_test.odin:479`) — 10.46× with surge (4.6% margin), ~6.5× base-only; the pin doesn't isolate the base spectrum.
3. **PR body missing the `[E10]` and `[E31]` citations** (AC3 enumerates both; only ODN-5/ODN-7/E9.1 present).
4. **Role-absent demand inertness ("draws no rng") has no durable era-3 pin** — the invariant that keeps the 32 pre-existing goldens fold-only is PR-prose-verified only.

### Notes (20)
18 r1 notes carry forward unchanged (all re-verified on the fresh tree): stale `(2 = ceil_cap)` burst message; SPRITE_COUNT "not yet wired" comment; era-2 roster loop missing the Terminal-kind assert; health-ring radius inside the campus half-footprint; `role_from_name` strings unpinned; fallback shapes unreachable + zero coverage; test_catalog hand-mirror in 3 places; `#partial` fail-open role→sprite switch; W9 WINDOW off-by-one; pre-surge burst check dropped; `demand.json` "10/tick" stale comment; `expect hash stable` parsed-never-enforced; `node_types.json` stale role list; PR-body misdescribes `terminal_types.dem` (it's `fixture off` + 7 explicit spawns); fold-splice proof is prose-only (no re-runnable tool); dead house geometry on the fallback path; growth type-draw composition unpinned; sprite-index mapping lacks a positive unit assert.
**New this round (2):** `test_terminal_class_profiles` header says "One terminal per role … the only candidate" but spawns two residentials (email dst pick has two candidates); `test_growth_e31_validity` header still says "10 windows" after the PR bumped the assertion to 20.

### Reviewer agreement
Cross-wave agreement concentrated on the PR-body/dem misdescription (blind + architecture + edge, two waves), the stale burst message (4 lenses), the inertness-pin and fold-prose gaps (tests lenses, four waves), and B1's window-gating flaw (edge + Perkins probe).

**Verdict:** NEEDS CHANGES

_Delta is clean and the finding set held — the blocker is the known carry-forward (B1), whose fix lands next; address it and push, and I'll re-review automatically on the new sha._
