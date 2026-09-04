## 🤖 Perkins automated review — round 3

**Job:** packet-plumber-v2-mechanics-the-box · **Reviewed sha:** 0431813 · **Reviewers:** 6/7 completed
**Verification:** 21/21 findings confirmed against the code — 0 discarded as false-positive, 0 kept as [unverified]

> **MAJOR REWORK NEEDED** is driven by the golden-corpus findings (B2/B3) — the economy code itself came through the rework well. Details below.
>
> **MEGA-DIFF disclosure:** the canonical diff for this round is the 1,449-line delta `git diff ad8afca..0431813` (`gh pr diff` stays API-capped on the ~92k PR; r1 verified the 91,477L bulk mechanically). The delta = the rework 7208ec5 (17 files, +327/−81), the post-rebase re-render 0431813 (27 T2 PNGs), and inherited #106 merge movement (view.odin, look_l1_test, palcheck §8, zoom refactor). Full 7-lens wave on the delta; committed-golden analysis done blob-vs-blob (machine-independent).
>
> **Degraded-lens disclosure:** blind failed 3× (1302 at boot, 1302 launch-burst, then a mid-turn process death after reading the full diff — no output); re-dispatched once per protocol, then degraded to 6/7. Findings are plentiful and the verdict rests on Perkins-verified blockers, so the degraded guard does not force a comment-only review.

### Fix audit (r1 → r3)

| r1 finding | r3 status |
|---|---|
| **B1 segfault** `odin test app/input` | ✅ **FIXED, independently verified**: 13/13 green at this sha; bug class swept — all 5 Input fixtures wire `.state`, the app wires it in start_run, no unwired construction site exists (incl. on the merged render lane) |
| **B2 advisory gate** | ⚠️ still open — segfault resolved, rows landed (W5/N10), but the new wrap-bound row is vacuous (B1), ruling-1 wiring untested (B4) |
| W1 silent place refusal | ✅ fixed in code (`last_reject`/`reject_tick`); the place branch's test is still missing (W2) |
| W2 pre-commit previews | ✅ fixed (`box_check_draw`/`box_check_place` public gates); box-on coverage gap (W1) |
| W3 crisis-stall vacuity | ✅ fixed — real 4.2 surge crisis fires (the `crises ≥ 1` vacuity gate passes in my run); automation gap (W3), semantics (N1) |
| W4 stats leak | ✅ fixed (`delete(rec.box.pieces)`) |
| W5 resplice invariant | ✅ fixed (net-zero same-spool row) |
| W6 dead-stock row | ❌ **not done — and the body claims it was "pinned"** (W4) |
| W7 input-parity | ✅ fixed (manifests re-blessed `e4a7a49e`→`f97e41f5`, 27/27) |
| W8 era-1 unreachable | ✅ resolved by user ruling 1 — implementation verified; wiring untested (B4) |
| N1 orphan frames | ✅ fixed (deleted; 4 frames = 4 captures) |
| N2 floor pin | ✅ fixed **and mutation-proven this round**: the new exact-clamp pin catches the u64 wrap (interval 18446744071562068368 ≠ exact clamp 100) that r1's `>=` pin provably passed |
| N3 palcheck environmental | superseded by ruling 2 (CI structural subset green) |
| N7 advance duplication | ✅ fixed (hoisted once in `box_apply_edit`) |
| N10 unpriceable pass-through | ✅ fixed (row added) |
| N8 short-name dup / N9 dead lookup / N11 stats rows / N12 era-guard row | ❌ still open — and the body claims two of them fixed (W4) |

### Blockers (4)

1. **The new 2^40 wrap-bound rejection row is dead-on-arrival — and it joined a table that has been passing vacuously.** `check_reject_balance` omits the `crises` source (added to `Catalog_Sources` before `balance`), so all 79 balance rows "reject" with `crises.json: invalid JSON` and return through the non-balance trivial branch. Proven two ways: replacing the row's expected rule with a nonsense string keeps the suite 297/297 green, and instrumenting the helper shows every row rejecting in `crises.json`. Independently, the row could never match even with a working helper: `jint_strict` returns i32 (2^40 overflows to "clock keys must be integers") and `di = 2^40` exactly does not trip `> (1<<40)`. A gate that cannot fail pins nothing — the PR's whole balance fail-fast surface, including its 6 box-clock rows, is unpinned. [acceptance, codebase, edge; Perkins-mutation-proven]
2. **11 of #106's 27 conflicted goldens were resolved by keeping stale PR-side bytes.** #106 changed 27 goldens; the re-render commit rewrote 27, but only 16 overlap #106's set (+11 sibling beats). For the 11 (a11y_protan/30000, a11y_reduced/30000, a11y_scale/30000, a11y_tritan/30000, advance_block_sla/15000, health_lose/21000, juice/30000, qos_emphasis/12000, sla/01000, surge/30000, warn/45000): the committed bytes are byte-identical to the pre-rebase `ad8afca` tree and differ from #106's own re-bless in 921600/921600 pixels — the merged render lane's pulse is absent. On either blessing machine the byte-exact local gate (the ruling-2 merge ground truth) is red for these demos: the gate table's "harness run 50/50 demos green" is impossible as committed. The commit message's "resolved by re-rendering … 27" is false for these 11. [architecture; Perkins blob-forensics]
3. **`goldens/a11y_reduced/30000ms.png` is a uniform solid-black frame blessed as a golden** (min=0, max=0) — present at `ad8afca` too, so the merged build's content (warm paper, per #106's version of the same beat) fails it. A black golden gates nothing and likely masks a real reduced-motion render failure at that beat. [architecture]
4. **Advisory test gate: FAIL — the ruling-1 wiring has zero coverage.** No row references `app_start_era()` or `advance_gate_enabled`: a revert of the era-1 start or the live 6.2 advance gate ships green, on the PR's flagship user-facing behavior. Aggravating gaps feeding the rubric: `box_check_*` never exercised box-on (ghost-vs-commit lockstep unpinned), the place-refusal toast branch untested (the draw-side has a row), the crisis-stall vacuity gate manual-only. [tests]

### Warnings (4)

1. **box_check_draw/box_check_place untested box-on** — the new public pre-commit seam restates `box_validate`'s pricing; no row pins check==charge agreement, so ghost-vs-commit drift ships green. [tests]
2. **Place-refusal toast branch untested** — the era-3 bind is piece-side (the PR's own evidence), making placement refusals the flagship "no"; the r1-W1 fix's branch has no row while the draw-side does. [tests]
3. **Crisis-stall gate manual-only** — the reworked Q7 vacuity gate lives in the `econ-check` verb, wired into no automated suite. [tests]
4. **PR-body disclosure accuracy** — "W6 the dead-stock load rejection pinned": no such row exists; "one router short-name helper": the inline mapping still appears twice (app/main.odin ~2447, ~2502); "the dead post-apply lookup removed": `slot, _ := node_slot(...)` is still discarded in `box_charge`; the L5 econ evidence table is stale vs the shipped build (era2-brush first_no 962 in the body vs 36 from the shipped econ-check; crisis-stall reshaped to 6000 ticks/seed 42). r1 praised this PR's honesty — the rework section now over-claims. [Perkins-mechanical]

### Notes (6)

- **dots_post_crisis** counts dots from the first crisis *activation* (including while active), not "after the last crisis resolved" as commented — the gate still detects the death spiral, weaker than documented. [edge, acceptance, architecture, codebase — 4-lens agreement]
- **data/demand.json** `_comment` still says "the app runs era 3 from tick 1" — stale pre-ruling prose in shipped data. [acceptance]
- **palcheck §8 routed legs (d)/(e)** index `pipe_congestion[ps8]` without the `testing_lvl_ok` guard the sibling legs use — a broken fixture panics instead of failing clean. [edge]
- **`save --skip-raster`** silently blesses T1-only — a half-bless footgun of exactly the class that produced blocker 2. [edge]
- **Corpus raster-convention split** (mechanism behind blocker 2): 116/117 committed goldens carry the PR machine's R/B-swapped convention (bg 200,226,237 = the palette paper 237,226,200 with R↔B swapped) while #106's lane bytes are warm-correct — two blessing machines blessed the two lanes; settle the corpus on one machine in the re-bless. [architecture; Perkins census]
- **ci-local.sh** still runs the full raster suite vs ci.yml's blind subset — sanctioned by ruling 2 (local = ground truth), informational parity note only. [tests]

### Reviewer agreement

- **Vacuous wrap-bound row / dead balance table** — 3 lenses (edge, acceptance, codebase), then mutation-proven by Perkins.
- **Golden-corpus cluster (stale resolutions, black frame, convention split)** — architecture, then blob-verified by Perkins.
- **dots_post_crisis semantics** — 4 lenses.

### Gates re-run by Perkins at 0431813 (local = merge ground truth)

| Gate | Perkins re-run | PR claim |
|---|---|---|
| `odin test core` | ✅ 297/297 (×3 incl. post-mutation restore) | 297/297 |
| `odin test app` | ✅ 51/51 | 51/51 |
| `odin test app/input` | ✅ **13/13** (r1 blocker independently cleared) | 13/13 |
| `odin test harness` | ✅ 2/2 | green |
| `econ-check` | ✅ all verdicts hold — real crisis fires, vacuity gate bites | holds |
| `drift-check` | ✅ 360/360 rejected | 360/360 |
| `input-parity` | ✅ 27/27 (manifests re-blessed) | 27/27 |
| `stats-check box_spine` | ✅ byte-identical (970,725 B — unchanged: no sim-economy bytes touched by the fix-delta) | identical |
| `palcheck --structural` | ✅ all structural legs green | green |
| `fold-check` | not re-run — `git diff ad8afca..0431813 -- data/ core/catalog.odin` is EMPTY; nothing to fold, r1's proof stands | — |
| mutation: delete-the-cap (production site) | ✅ RED ("no brush observed") → restore GREEN | claimed |
| mutation: drop-the-floor (production site) | ✅ RED via the **hardened** pin (wrap caught) → restore GREEN | claimed |
| `harness run` full T2 | ❌ not reproducible on any machine as committed — see blocker 2 | "50/50 demos green" |

CI note: Actions show the billing-block signature (5s / zero logs) — note-only per standing ruling; not a gate.

**Verdict: MAJOR REWORK NEEDED**

_The rework itself is good: both r1 blockers' fixes verify independently, the three rulings are implemented as ruled, every mutation leg still bites, and the hardened floor pin now catches what the old one provably couldn't. What's broken is the golden corpus: eleven rebase conflicts resolved by keeping stale bytes, one black frame blessed as a gate, a corpus split across two raster conventions — the local gate this ruling-2 world depends on cannot pass as committed — plus a vacuous rejection row riding a dead table and a body that over-claims three fixes. Re-render the 11 on the golden machine, re-bless one convention, fix the helper line and the body, add the ruling-wiring rows — and this lands. Push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
