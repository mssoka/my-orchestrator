## 🤖 Perkins automated review — round 2 of 3 (rebase re-review)

**Job:** finlit-e2-7 · **Reviewed sha:** `64cc487` · **Reviewers:** 7/7 completed
**Verification:** 9/9 findings confirmed against the code — 0 rejected as false-positive, 0 kept as [unverified]

> ⚠️ This PR **merged (d488473) while round 2 was in flight** — the merge consumed exactly the reviewed sha, so this audit applies to the merged content. A formal review can't be posted on a merged PR, so here it is as a comment for the record.

### Rebase content-preservation audit — PASSED (the three things r2 had to establish)

1. **Content preservation (highest priority): the rebase was content-preserving; the r1 approval carries.**
   - `touch_targets.gd` + `touch_proxy.gd`: **byte-identical** between r1-approved `4cd9aa7` and `64cc487` (empty `git diff`).
   - `street.gd` delta = **only e2-1's additive playtest tooling** (`_playtest` wiring, `_record()` calls, `PlaytestChip`, `RerollTapProbe`); the 4 deleted lines are lambda rewrites that preserve their original emits. **Zero e2-7 touch-target hunks were modified by the conflict resolution.**
   - `street.tscn` delta = only e2-1's `PlaytestChip` label.
   - All six invariants verified present and semantically identical: 160/120px floors, `FIND WORK > FIX oldest-damaged-first > BUY/UPGRADE > WORK SHIFT`, `_on_dominant_pressed` → `dominant_action()`, `_shift_ready()` gate, the **bounded 300-frame** `process_frame` proxy-wrap poll (not the unbounded `await reset.resized`), viewport-clamped `touch_proxy_rect`.
   - **Suite re-run in the round worktree: 295 checks / 0 failures (exit 0), `--import` clean** — identical count to r1, scene regressions green with e2-1's scene in tree.
2. **e2-1 interaction hunt — no semantic conflicts.** `PlaytestSession` is a pure observer (JSONL recorder, no input interception, no state mutation) — proxy/dominant-button tap routing is untouched; `capture.gd` is a standalone rig that never co-runs; the shared regions (`_on_reset_pressed`, `_show_leaderboard`, `_ready`, name/lottery lambdas) merged additively with e2-7 behavior intact; the `RerollTapProbe` exists only under `--playtest` and changes nothing in normal play.
3. **Fix audit (r1's findings):** all 3 warnings + 6 notes **still present, none worsened by the rebase** — W1 (transient sub-120px NEW GAME window, disclosed trade-off), W2 (dominant press dispatch untested), W3 (advisory gate CONCERNS, P1 ≈86%), N1 (theme mirrors unconsumed, disclosed), N2 (`_shift_ready` untested), N3 (id-less branch unexercised), N4 (committed review artifacts still pin the pre-fix commit — 285 vs 295 checks), N5 (docs still cite the unbounded await), N6 (`first_upgradeable` missing-id guard).

### Blockers (0)

None.

### Warnings (4)

1. **Transient sub-120px hit window for NEW GAME during pop-in before the proxy wraps** — `game/scripts/street.gd:832-852` [edge + acceptance, carry-forward r1 W1]. Disclosed in the PR body as an accepted trade-off; unchanged by the rebase.
2. **Dominant button press dispatch (`_on_dominant_pressed`) is never exercised by any test** — `game/scripts/street.gd:417` [tests, carry-forward r1 W2]. AC3's single-source claim is pinned for the label only; a swapped match arm would pass the suite.
3. **Advisory test gate: CONCERNS** — [tests, carry-forward r1 W3]. P0 100%; P1 ≈86% pending the two gaps above.
4. **Touch floors hardcoded in 4 places** — `touch_targets.gd:17-18` / `street_theme.tres:84-85` / `street.tscn:211` / `street.gd:607` [architecture, new]. Partially disclosed in the PR body (theme mirrors deliberate, "design surface, not enforcement"); drift risk is mitigated by the combined-minimum scene pins.

### Notes (9)

- `first_upgradeable` lacks the missing-id `continue` guard that `oldest_damaged_repairable` has [edge + blind — third independent sighting; r1 N6].
- Touch proxy emits `pressed` on press-down only — no drag-off cancel (the wrapped Button cancels on drag-off; the proxy does not). Arguably intentional for touch responsiveness — flagged for the record [edge, new].
- Asset-card OPEN button (170×130) size not enforced by any test [acceptance, new; meets floors today].
- Asset-card FIX disabled branch (unpaid + unaffordable legacy repair) never exercised — the existing test is the free-repair regression pin, not a tautology [codebase, demoted from warning].
- Theme `min_touch_size` mirrors consumed by no runtime code (disclosed design surface) [r1 N1].
- `_shift_ready()` cooldown output untested [r1 N2].
- Defensive `id<0` skip in `oldest_damaged_repairable` unreachable in the suite [tests, r1 N3].
- Committed review artifacts describe the pre-fix commit (`f7140c6`, 285 checks vs 295 on head) [blind, r1 N4].
- Story Task 3.3 + `touch_proxy.gd` docstring cite `await reset.resized`; shipped code uses the bounded 300-frame poll — docs lag implementation, no hang hazard [r1 N5].

### Reviewer agreement

- Transient sub-120px NEW GAME window — edge + acceptance traced the same `_open_popup` → settle-loop → `wrap()` window (r1 W1 carry-forward).
- `first_upgradeable` guard asymmetry — edge + blind independently (r1 N6, third sighting).

### Verdict

**Verdict:** READY TO MERGE

0 blockers; the rebase was content-preserving (r1's approval carries) and e2-1's tooling coexists without runtime conflict. All gates re-run by Perkins in the round worktree: 295 checks / 0 failures (exit 0), `--import` clean. The A29 confirmation ask stands as the PR's open question — the four rules are implemented as proposed and await your ack; each is a one-line constant change if ruled differently.

_Findings are advisory (r1 carry-forwards, none worsened). Since the PR has merged, address the two P1 test gaps (dominant press dispatch, cooldown state) and the docs drift at your convenience — they belong to the e2-7 follow-up or e3-5/e3-13 A29 re-implementation. After round 3, the human takes over._
