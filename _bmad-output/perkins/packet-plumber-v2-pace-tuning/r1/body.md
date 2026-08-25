## 🤖 Perkins automated review — round 1

**Job:** packet-plumber-v2-pace-tuning · **Reviewed sha:** `9ab2f02` · **Reviewers:** 7/7 completed
**Verification:** 47/48 findings confirmed against the code — 1 discarded as false-positive

**Method note:** the full diff is 80,030 lines (202 files); `gh pr diff` exceeds GitHub's 20k-line API cap, so the canonical diff was reconstructed byte-exact from git (`merge-base 8639d5f → 9ab2f02`, stats match the PR: +39263/−38890). The **code chunk** (2,265 lines: `core/`, `app/`, `data/`, root) ran the full 7-lens wave; the **goldens chunk** (179 files, 77,765 lines) was verified **mechanically** per this round's lens-guards: `tools/ci-local.sh --mac` re-run on the reviewed sha = **10/10 gates GREEN**, including gate 4 (45 demos T1+T2+replay, bit-for-bit) and gate 10 (input parity).

**Hard blocker bar (no gameplay-semantics change): CLEAN.** No routing, serialization, packet-contract, or LOG_VERSION touches. Diff surface = pace knob (30→120) + lockstep-scaled constants (tolerances ×4, exit margin 40→160) + spawn-cadence consts migrated to balance.json. The surge's ~2.6× packet-multiplicativity dimming checks out as the units-anchored design (accrue ÷ bandwidth — the test table 83/1333/333/2500 → 20/333/83/625 is the exact ÷4), and the W9/W10 re-derivations are honestly self-anchored to topology+catalog rather than magic numbers.

### Blockers (0)

None.

### Warnings (10)

1. **New fail-fast branches untested** — `core/catalog.odin:818-831`: the two new knobs' rejection paths (missing key / non-integer / <1) have zero `bal_rows`; the raised radius floor (must now exceed 4) is also unpinned. These knobs are the user's fun-test iteration surface — every sibling balance rule has rows. *(tests, acceptance, blind)*
2. **`packet_bandwidth` still loads via lenient `jint` with silent default 30** — `core/catalog.odin:813`. A missing key silently reverts the entire 4× pace, right beside the two new keys that fail fast on missing. The one knob the user will hand-edit deserves strict loading. *(architecture, codebase, edge, security, blind)*
3. **Pace iteration isn't single-knob in practice** — tolerances (`packet_types.json` 2000/1200) + `exit_margin_ms` 160 must hand-scale in lockstep across 2 files, but the PR body invites "one-line knob (150/180/240)" edits, which would silently shift breach difficulty on the next tune. *(acceptance)*
4. **Surge window-boundary pins weakened** (`==1` → `<=1`, ×4) — no director-level window discrimination remains (relies on the pure-function `set_piece_active` pin). *(tests, blind)*
5. **W6 zero-drop relaxed to a ratio** (`res_drops < uplink_drops`) with contradictory staging comments (3 vs 1 sink drops; stale "each residential: 2 wide drops" line vs the mixed 2/1 wiring). *(tests, blind)*
6. **E29 stuck-mixture / waiting-0 pin now vacuous** — Red from the first stuck packet makes the mixture unobservable; re-stage on a campus like `node_health_test` did. *(blind)*
7. **`replay_error` guard deleted** from `test_sla_delivery_accounting` — nothing in the pace shift requires dropping it; the sibling test retains it. *(tests, blind)*
8. **Load-bearing staging comments contradict the shipped code** — crisis "1/tick" vs 0.5/tick loops; "3/tick" vs 5/tick; sla 1750 ms/35-tick/8th-delivery vs pinned 1300/26/2nd-cumulative; "~3 ticks" vs the 4-tick cadence; W9's "14600 vs raw-accrual 12900" is impossible per its own clamp formula. The "measured, never guessed" audit trail is corrupted exactly where the next tuner will look. *(blind, acceptance, codebase, tests)*
9. **`wire_path_test` Balance literal omits the new knobs** (0 interval → modulo-by-zero trap at `growth.odin:450` if growth is ever enabled there; breaks the mirror-balance.json convention its sibling follows). *(blind, codebase, architecture, edge)*
10. **Engine credit-calibration comments still teach ÷30 math** (`core/flow.odin:606-610`) at the shipped knob 120. *(codebase)*

### Notes (7)

- Unused `import "core:fmt"` (`core/warnings_test.odin:23`) — dead debug leftover. *(blind, codebase, acceptance)*
- No-op `_ = s` (`core/health_test.odin:403`). *(blind, codebase)*
- `demos/*.dem` headers still document pre-tuning arithmetic (deleted const + 2 s cadence; bandwidth-30 transit math) — will mislead future golden-diff debugging. *(architecture, codebase)*
- Clamp-honest pick-interval formula hand-rolled twice in `demand_test` (3 copies incl. the engine's) — drift risk. *(codebase)*
- New derived-bound test formulas divide by `accrue` with no zero floor (accrue==0 panics rather than fails). *(edge)*
- PR body's "same 3.2× headroom" is false by its own table (2.9× → 3.6×; 3.2× is the transit ratio). *(blind)*
- Advisory test gate: **CONCERNS** (P0 100%, P1 ≈81%) — driven by warnings 1/4/5; all transit/credit/SLA/growth/crisis/health pins FULL. *(tests)*

### Reviewer agreement

Highest-confidence (multi-source): **W2** lenient pace-knob default (5 lenses) · **W9** zeroed knobs in the app fixture (4) · **W1** untested fail-fast branches (3) · **W8** contradictory staging comments (4) · **W4/W5/W7** weakened/removed pins (2 each) · unused-import note (3).

**Verdict: READY TO MERGE**

0 blockers. The one hard bar of this round — no gameplay-semantics leakage — is mechanically clean, CI is 10/10 green on the reviewed sha, and the re-bless is replay-gate-proven. The 10 warnings are quality/robustness items (several directly serve the planned fun-test tuning round — especially W2/W3); they are merge-non-blocking but recommended before or with the follow-up tune.

_Address findings and push — I re-review automatically on the new sha. The loop runs until an APPROVED verdict._
