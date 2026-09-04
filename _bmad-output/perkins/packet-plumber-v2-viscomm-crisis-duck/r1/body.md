# Perkins round 1 — viscomm(crisis): desaturate the non-involved network (audit finding C)

**Verdict: NEEDS CHANGES** — 1 blocker, 4 warnings, 13 notes.

Reviewed sha `d0bf930` (detached worktree). Model `zai-coding-cn/glm-5.3`, 7 lenses × 2 chunks (big-diff policy: c1-docs 1997 ln / c2-code 1145 ln; the chore commit covered mechanically — see below). 48 raw findings → 40 survived verification (8 rejected as false/chunk-artifacts, then deduped to 18 groups). Pixel/aesthetic reads are MECHANICAL only (non-k3 round — the vision caveat); the aesthetic verdict is deferred for the k3 re-check.

## Independent verification runs (this round, in the detached worktree)

| check | result |
|---|---|
| `odin test app` / `app/render` / `core` | 48/48 · **100**/100 · 261/261 (PR table says 99 — stale, note) |
| `tools/harness.sh palcheck` | all green (§7 desat pins included) |
| `tools/harness.sh run` | **49/49 demos green** — mechanically proves the inert byte-identity contract (43 calm demos byte-identical) + the 6 re-blessed crisis frames |
| `tools/lint.sh` / `tools/ci-local.sh --native` | all gates green · 13/13 |
| Chore commit 8c482ec verbatim fold | **10/10 files byte-identical** vs the main-checkout sources (deferred-work.md delta = this PR's own later additions) |
| Mutation leg 1 — factor bypass (`desat_f := 0`) | **RED**: 6 palcheck §7 failures (crisis renders fully saturated) → restore GREEN, porcelain clean |
| Mutation leg 2 — over-broad predicate | **RED**: 4 §7 failures |
| Mutation leg 3 — W3 amber flip | **RED**: `route_tie_inline_load_default_is_pinned` — `got {255,176,46,235} want {186,94,232,235}` (exact bytes; the once-vacuous default is genuinely pinned now) |
| Mutation leg 4 — **Dublin block recede deleted** | **NO FAILURE — full corpus 49/49 green** ← the blocker below |

The core desat mechanism is real and strongly gated: the pure factor, the involvement chain, the mix math, the reduced-motion pin, and the never-recede telegraph contract all verified on disk, and the sprite-path recede is pinned three ways (unit purity pins, §7 draw-path legs, the 6 goldens).

## BLOCKER (1)

### B1 — The Dublin street-block recede is mutation-vacuous: no gate can fail when it is deleted
`app/render/dublin.odin:360-366` · sources: tests ×2 + Perkins probe

The PR's recede family includes "the Dublin street blocks", but nothing anywhere renders Dublin blocks under an active **zone** crisis: the only Dublin-map demo (`dublin_board.dem`) captures at 30s/90s where the crisis is pool-only (factor 0 by the carve-out), and the juice/a11y scenes are procedural (sprite path — §7's fixture included). **Perkins probe: deleting the block recede keeps the full corpus green (49/49) and every unit test green.** Per this project's mutation doctrine (a claimed surface that cannot be made to fail any gate is a blocker — the font-r4/spawn-feel class), a shipped recede behavior with zero gating is a blocker even though the code looks correct.

**Fix:** one §7-style leg with `map_source = Dublin` + an active `Saturated_Bundle` row, pixel-scanning a non-involved street block for the receded alpha twin (RED-then-GREEN: delete the recede → the leg fails). The inert line-alpha edge (`dublin.odin:365`, note N2) suggests scanning the block fill, not the frontage line.

## WARNINGS (4)

- **W1 — 6th re-blessed golden undocumented.** `git diff --stat` shows exactly 6 golden PNGs changed; the PR table lists 5 — `goldens/a11y_scale/65000ms.png` (same juice-scene cause; the demo IS the juice scene at ×1.50) has no cause row. 7 independent lenses. Fix: add the row.
- **W2 — New test leaks its Catalogs.** `crisis_packet_involvement_chain` deletes sources but never `pp.catalogs_destroy` — the sibling convention (spawn_fx_test ×7) is violated; `odin test` prints `+++ leak 17B [catalog.odin:…]`. Fix: one defer line.
- **W3 — `scan_col` x-bounds gap.** `harness/palcheck.odin:944` guards `yi` but indexes `px[… + cx]` unguarded (scan_box checks both axes). Latent OOB read on fixture/camera drift. Fix: mirror scan_box's guard.
- **W4 — Advisory test gate: CONCERNS.** P1 ≈ 85%: the core path is exemplary, but the Dublin surface (B1) is uncovered, the halo/router-ring/glint recedes are golden-pinned only, and the fan-stub recede is unreachable with the wire flags off.

## NOTES (13)

N1 verify-table says 99/99, suite is 100 (6 new tests, not 5) · N2 the Dublin frontage-edge recede scales a **line** alpha — inert under the rlsw line-alpha trap (in-repo canon: spawn_fx.odin:449, view.odin:670); redraw as a thin fill or drop · N3 the unreachable primitive-fallback building recede exceeds the spec's closed recede list and diverges from the sprite path (wash/chip twins only there) · N4 fan-stub recede flag-gated off in every shipped config · N5 router-ring/family-wash/glint recedes have no named pin (goldens carry them) · N6 §7 toggles `view.reduced_motion` outside the save/defer set · N7 the desat contracts doc block attaches to `CRISIS_DESAT_MIX`, orphaning `draw_crisis_banner`'s doc ~200 lines from its proc · N8 the basis-switch pin's fixture is single-row (the narrated two-row dip is only weakly discriminated) · N9 per-packet `pipe_slot` re-resolution is the pre-existing pattern · N10 folded ARCHITECTURE-SPINE.md is a raw `{name}` template (verbatim-preserved; belongs to the egress-qos backlog) · N11 folded gauge spec links into an ephemeral `.herdr/worktrees/…` path · N12 deferred-work.md mixes absolute/relative `source_spec` paths (pre-existing entry) · N13 purity comment "NO app-fed View state" vs the `v.reduced_motion` read — wording precision (settings flag, harness-visible).

## Rejected on verification (8)

"Ships only docs" (chunk artifact — the code exists, tested + mutated here), "W3 test missing" (it ships; the flip leg failed it with exact bytes), "fold = scope drift" (the chore is spec-mandated + verbatim-verified), "duplicated SLA/pool formulas" and "dead `cur := raw`" (phantoms of the folded r1 *review-diff artifact*, not the tree), "halo fix unpinned" (the goldens were re-blessed FOR the halo delta — mutating the blend fails juice@65s), the self-retracted premise-850 quibble, and the "W3 test rides this diff" attribution flag (that's the issue-#101 fold design).

## What would clear it

B1's one fixture leg (RED-then-GREEN) + W1's table row + W2's defer + W3's guard are all small, localized, and none touch the shipped render path's behavior on blessed configs. The mechanism itself is solid work — the fold advisories (W3 jcol pin especially) are genuinely closed.
