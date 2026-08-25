## 🤖 Perkins automated review — round 1 (cap lifted — loop until approved)

**Job:** packet-plumber-v2-5.5-demolish-input · **Reviewed sha:** `55d1b66` · **Reviewers:** 7/7 completed
**Verification:** 16/16 findings confirmed against the code — 0 discarded as false-positive (one blind-lens sub-claim — that the `!` leg masks parity failures — was dropped; the `&&` chain stop-on-fails)

**Orchestrator spot-checks (run by Perkins, not trusted from the PR body):**
- **Diff IS the delta** — `gh pr diff 59` is hash-identical to `git diff e07265b..55d1b66`; one commit; `core/`, `data/`, `goldens/`, `demos/` untouched.
- **Local suite (ground truth; GH Actions is billing-blocked — not a signal):** `tools/ci-local.sh --mac` **9/9 gates green** — 184 core tests, 29 demos byte-identical, 24 parity scenarios, gate-9 CLI leg.
- **The pins bite (mutation-verified in the review worktree, reverted after):**
  - pad X mapping dropped → `input_parity_demolish_btn_node` FAILS (pad leg: 0 commands vs 1, hash divergence, selection left set).
  - `popover_demolish_hit` deadened → BOTH button scenarios FAIL (mouse+touch lose the demolish command; the pad-leg divergence is caught by the equality check).
  - `./bin/harness input-parity bogus` exits exactly 2; the `[ -x ]` guard covers the 127→`!`→0 class.
- **Parity [FORGE #6] is real:** pad X (`RIGHT_FACE_LEFT`) → the shared `Demolish` intent; `Node_Select` mirrors the dpad cursor (junction → select, terminal → clear — `click_select`'s rule, E2 mirrored); all three devices ride the ONE executor branch with the placing/drag re-check; the parity equality check forces the pad leg to emit the same `Cmd_Demolish_Node{1}` — no per-device command production. E10 holds: existing commands only, no `LOG_VERSION` bump, replay byte-identical (29 demos green). The 2.3 `demolish_bundle`/`demolish_node` goldens carry the E1/E27 T1+T2 pins.

### Blockers (0)

None.

### Warnings (3)

1. **Gate-9 negation leg greens on ANY non-zero exit, not only the claimed usage exit 2** *(blind + edge + security)* — `ci.yml:126-128` / `ci-local.sh:63`. The comment contracts "rejected (usage exit 2)" but `! ./bin/harness input-parity bogus` accepts any non-zero — a crash on the arg path false-greens. The fold's letter is satisfied (bogus arg does exit 2; `[ -x ]` kills 127); this is hardening of a negative-control pin. *Fix: capture and assert the exact code (`rc=$?; [ $rc -eq 2 ]`).*
2. **Demolish-while-placing / mid-drag inertness has no scripted pin** *(tests)* — `app/input/exec.odin:146`. AC#1's "disabled while placing" gate exists and matches the old semantics, but no scenario presses X/DEL in either state — deleting the gate passes all 24 scenarios. Same class as 5.4's W1-r4. *Fix: a parity scenario pressing X while placing + mid-drag, asserting zero commands.*
3. **Advisory test gate: CONCERNS** *(tests)* — P0 fully covered (the new positive pins bite — mutation-verified above); P1 ~85-89% on the two unpinned legs (warnings 2 + note 1 below).

### Notes (7)

1. **The mirror's terminal→clear branch (E2 mirror) is pinned by no scenario** *(acceptance + tests)* — a mirror that SELECTS terminals passes all 24 scenarios (`pad_cursor_wrap` parks on terminal node 0 but asserts `pad_node` only). *Fix: assert `sel_node == -1` with the cursor parked on a terminal.*
2. **`pipe_demolish_btn_center` re-derives the anchor math the N2-r4 fold single-sourced** *(blind + architecture + codebase)* — a third copy of the formula (fixture constants; `build_scenarios` holds no topology to delegate with). Drift fails loudly — maintainability debt only.
3. **Every dpad step forces `sel_pipe = -1`** *(blind + architecture)* — a mouse/touch pipe selection (QoS panel open) dies on any incidental pad nudge. Consistent with the "dpad cursor IS the pad's select" design, but the mixed-input side effect is unflagged in the decision log.
4. **The "swallowed — no re-select" release frames in scenarios 23/24 are vacuous** *(acceptance)* — post-demolish the button center is 250px+ from the nearest live node (snap_radius 36, fixture nodes 12 tiles apart), so a dropped swallow latch stays green.
5. **`poll.odin` `RIGHT_FACE_LEFT → .X` adapter never exercised** *(tests)* — by design (parity scripts semantic buttons); documented blind spot.
6. **The mirror re-implements `click_select`'s junction/terminal rule** *(architecture)* — two copies of the rule; the repo's ONE-copy discipline suggests a shared helper.
7. **ui_hook wiring by scenario-name string matching** *(architecture)* — three scattered sites per scenario; a rename silently drops the hook.

### Reviewer agreement

Warnings 1 (3 lenses) and the notes 1–3 (2–3 lenses each) are the multi-source, highest-confidence findings — all fold-forward candidates, none blocking.

**Verdict:** READY TO MERGE

_The delta is clean: parity is real, the pins bite (mutation-verified), no new deltas. Approved — the 3 warnings + 7 notes are fold-forward candidates for the next input-surface story. I re-review automatically on any new sha._
