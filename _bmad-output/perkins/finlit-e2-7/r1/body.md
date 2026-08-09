## 🤖 Perkins automated review — round 1 of 3
**Job:** finlit-e2-7 · **Reviewed sha:** `4cd9aa7` · **Reviewers:** 7/7 completed
**Verification:** 10/10 findings confirmed against the code — 0 rejected as false-positive, 0 kept as [unverified]

> ⚠️ Reviewed `4cd9aa7`, head now `96d9516` (two docs-only commits: badge-out + memlog) — a fresh round will follow on the new head.


### Blockers (0)

None.

### Warnings (3)

1. **Transient sub-120px hit window for NEW GAME during pop-in before the proxy wraps** — `game/scripts/street.gd:756-778`. `_open_popup` retires the proxy (`_hide_touch_proxies`), and the 110px reset button stays live through the pop-in tween (scale 0.9 ≈ 99px effective) and the settle loop before `_reset_proxy.wrap()`. Disclosed in the PR body as an accepted trade-off — flagged for the record, not a blocker. Fix: `reset.disabled = true` (or MOUSE_FILTER_IGNORE) until the wrap completes.
2. **Dominant button press dispatch (`_on_dominant_pressed`) is never exercised by any test** — `game/scripts/street.gd:388`; 0 hits in `test_economy.gd`. AC3 makes `dominant_action()` the single source for text, enabled, AND press dispatch, but only the label is pinned — a swapped match arm would pass the suite. Add a scene stage driving the press per action (FIND_WORK / FIX / WORK_SHIFT) asserting the correct handler fires.
3. **Advisory test gate: CONCERNS** — P0 (A29 rules + scene enforcement incl. real-input routing + negative control) is fully covered; P1 sits at ~80–89% for the two gaps above (press dispatch, WORK SHIFT cooldown state). Driving those lifts the gate to PASS.

### Notes (6)

- Theme `min_touch_size` constants (`street_theme.tres:84-85`) are written and pinned but consumed by no runtime code — the PR body discloses this as deliberate ("design surface, not enforcement"). Either drop the mirror or read it via `theme.get_constant` so it drives sizing.
- `_shift_ready()` (street.gd:382) — the shared cooldown gate — has no test asserting its output or the button's disabled-on-cooldown state.
- Defensive `id < 0` skip in `oldest_damaged_repairable` (touch_targets.gd:75-77) is unreachable in the suite — every fixture carries an id; add an id-less damaged asset fixture.
- Committed review artifact `_bmad-output/reviews/e2-7-adversarial.md` describes the pre-fix commit: its headline FIX-doctrine finding is refuted by shipped `street.gd:711` (`fix.disabled = fix_cost > 0 and ...`). Re-baseline the committed reviews against head.
- Story Task 3.3 and the committed reviews cite `await reset.resized`; shipped code uses a bounded 300-frame `process_frame` poll instead (street.gd:762-771) — the unbounded-hang hazard they describe is absent. Docs lag the implementation.
- `first_upgradeable` (touch_targets.gd:84-91) lacks the missing-id `continue` guard that `oldest_damaged_repairable` has — asymmetric; latent since ids are always present today.

### Reviewer agreement

- **Transient sub-120px NEW GAME window** (edge + acceptance) — both lenses independently traced the same `_open_popup` → settle-loop → `wrap()` window; see Warning 1.

### Verdict

**Verdict:** READY TO MERGE

0 blockers; all gates re-run by Perkins in the round worktree: 295 checks / 0 failures (exit 0), `--import` clean, `--quit-after 600` clean. The A29 confirmation ask stands as the PR's open question — the four rules are implemented as proposed and await your ack; each is a one-line constant change if ruled differently.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
