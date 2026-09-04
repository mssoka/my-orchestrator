## v2 mechanics — The Box: capped typed build economy

Implements the ratified mechanics record ([mechanics-quinn 2026-08-27](https://github.com/solarity-services/packet-plumber/blob/v2/_bmad-output/implementation-artifacts/mechanics-quinn-2026-08-27.md) — all 7 rulings USER-adopted; this PR implements, never re-litigates). **The Box, capped per era, refilled by tempo**: typed pieces — 1G/40G/100G routers, standard/fiber spools — against an era ceiling; draws drain spools 1/tile; placements spend a held piece; promotion is a swap (teardown refunds fully, so place-cheap-then-promote costs the same as place-big-first); refill dots restore-TO-cap on a known clock spine, accelerated by deliveries, clamped [floor, base]; era advance raises caps + shifts the spool mix.

**Box-off runs are byte-identical to the pre-change sim** (the `box_enabled` run-setup flag — the growth/health/advance-gate pattern; the delegate path IS the old code). No new commands; LOG_VERSION stays 6.

### Staged commits (L1→L5 per the briefing)

| Commit | Stage |
|---|---|
| `abe9b1c` feat(box) L1-L3 core | the Box + the Cap + the material grammar (rulings 2-6) |
| `c88d306` test(box) | the behavior suite + the economy gates that can fail (record Q8) |
| `a94e840` feat(box) L4-L5 | app wiring, box_spine golden demo, stats B-row, econ-check verb |
| `ad8afca` review(box) r1 | the mandatory step-04 swarm (adversarial + edge + verification-gap) |

### Tuned numbers (L1 staging → L5 sim-tuned; evidence below)

| Era | basic | mid | high | standard spool | fiber spool |
|---|---|---|---|---|---|
| 1 Foundations | 6 | 0 | 0 | 240 | 0 |
| 2 Email & Web | 8 | 0 | 0 | 240 | 0 |
| 3 Streaming Surge | 10 | 3 | 2 | 240 | 360 |

Clock: base dot 2400 ticks (120 s @ 20 Hz), floor 600 (30 s), acceleration 1 tick per delivery (interval = clamp(base − deliveries, floor, base)). The floor is the no-soft-lock guarantee and is never gated on performance; the base interval is the ceiling — a stalled run rides the spine, never slower (**record Q7: the crisis→slower-dots death spiral is structurally impossible; the crisis-stall scenario pins interval ∈ [floor, base]**).

Era-2's original fiber grant (120) moved to era 3 during review: mid/wide unlock at era 3, so era-2 fiber was unspendable dead stock — the loader now REJECTS caps for not-yet-introduced tiers/spools at load (fail-fast), which is what caught it.

### L5 calibration evidence (`harness econ-check`; deterministic, real catalogs, greedy-expansive bot: expansion → terminal wiring → cannibalize-and-redeploy)

```
scenario      ticks  draws  places  refusals  episodes  first_no  dots  interval[min,max]  min_stock  deliveries  dots-in-refusal  piece-starved
era1-calm      6000     58       9         0         0         0     2  [2394,2396]        41          16           0  false
era2-brush    12000    152       9       719         1       962     5  [2384,2400]         6          41           1  false
era3-slope    24000     20      10         0         0         0    10  [2327,2400]       216          92           0  true
crisis-stall  24000     20      10         0         0         0    10  [2327,2400]       216         104           0  true
econ-check: all scenario verdicts hold
```

- **era1-calm**: zero refusals — the era-1 kit is felt-not-counted (ruling 7's fat caps).
- **era2-brush**: the ceiling speaks in ONE episode (a burst, never spam), self-resolving as the dot lands mid-shortage (dots-in-refusal = 1) — ruling 7's authored brush, first-"no" on greedy-safe play.
- **era3-slope**: the bind is two-sided — the bot exhausts its 10-basic kit (piece-starved = true) exactly as the record frames Era 3 ("every draw is material off the board"); fiber 360 + wide draws carry the mix shift (rulings 6+7).
- **crisis-stall**: intervals never leave [floor, base] under the stressed seed — Q7 holds.

Bot-model caveat (honest scope): the proxy bot's reachable-work model saturates (E31 attach spawns + 14-tile standard reach); the doctrine-level cadence gets its final tuning at the fun-test gate against real play. The core gates (brush-frequency, first-no, mutation legs) pin the MECHANISM: delete-the-cap and drop-the-floor turn them RED (pinned in `core/box_test.odin`).

### Gates (local — the merge ground truth per the CI billing-block note)

| Gate | Result |
|---|---|
| `odin test core` | 295/295 green (15 new box tests incl. the Q8 gates + mutation legs) |
| `odin test app` | 51/51 green (incl. the box refusal-toast pin) |
| `harness run` | **50/50 demos green** (incl. the new `box_spine` golden: drain → dot → era-advance restore) |
| `drift-check` | 360/360 mutations rejected |
| `fold-check` | PASS — the legacy T1 shift is the catalog_hash fold alone (bytes 33..40 proven) |
| `stats-check` | boot + box_spine live == replay byte-identical (box B/J rows included) |
| `econ-check` | all scenario verdicts hold |
| `palcheck` | **pre-existing local red** — see disclosure |

### Re-bless inventory (disclosed per harness doctrine)

ALL `.t1` manifests + `.log.bin` + T2 PNGs re-blessed (`harness save`): the catalog content change (eras box rows, balance box block, pipe_tier spool tags) folds `catalog_hash` into every T1; `fold-check` proves the box-off tick-1 shift is that fold ALONE (8 bytes at the catalog_hash offset, byte-proven by dump diff). New: `goldens/box_spine*` (4 T2 beats + t1 + log). T2 PNGs additionally shifted because **this machine's rlsw render differs from the environment that produced the committed goldens** — see disclosure.

### Decisions & rationale

- **No new commands / no LOG_VERSION bump** (saves disposable per record Q6 — flagged for user confirmation): the promotion "swap" is demolish+place (lifetime cost = place-big-first by construction); pipe modernize resplices spools. Same-spool resplices (mid↔wide) price NET-ZERO and never refuse on a short spool (a net-free upgrade refusing would be a false "no").
- **`Box_Charge_Snapshot`**: refunds/charges price from PRE-apply snapshots — post-apply slot look-ups skip dead entities and fall back to slot 0 (the review's stock-corruption catch; tests now demolish non-zero ids).
- **Refill schedule is fixed at dot-fire time**: the player can always read when the next dot lands (the known worst case); deliveries set the NEXT interval.
- **Refunds are unclamped; refills clamp at cap** — full-teardown-refund is an explicit ruling; "no banking" governs refills only.
- **Era box caps cross-checked at load** (non-decreasing per type across eras = ruling 3's "advance raises the cap"; dead-stock caps reject).
- **Golden-stability**: box sections serialize absent-when-disabled; box-off runs write zero bytes; the app gates the tray counts/HUD line on box_enabled so legacy visuals are untouched.

### Disclosures / flags

1. **APP_ERA: the shipped app starts at era 3** (pre-existing `APP_ERA` constant from the 4.1 forecast slice). The Box's era 1–2 tutorial arc (the authored brushes) is unreachable in the shipped app until the start era drops to 1. Design-level — flagged to Gru for the user (mechanics-quinn record); NOT changed unilaterally.
2. **T2/palcheck environment drift (pre-existing, proven not-caused-here)**: re-blessing the PRISTINE base commit on this machine reproduces `palcheck: 61 FAILED` exactly (committed base goldens score 32) and `save juice` on base ≠ committed juice — the committed goldens come from a different render environment (CI or prior toolchain state). T1 (deterministic sim hashes) is green everywhere on both base and this branch. The LOOK calm-at-green gates need a human decision on the golden source of truth (local re-bless vs CI render) — same environmental instability the congestion-read-a1 lane documented.
3. **Saves/compat (record Q6)**: v2 is a dev build — NO migration system built; existing saves with free-built unlimited webs are disposable. Confirm.
4. **Sally's full legibility polish lane** (brush feedback framing, first-"no" moment) remains a follow-up job per the briefing — this PR ships the minimal glanceable HUD line + tray counts only.

🤖 Generated with the orchestration heist — reviewed by the step-04 swarm (blind hunter / edge-case hunter / verification-gap), Perkins to follow.

