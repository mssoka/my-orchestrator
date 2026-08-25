## 🤖 Perkins automated review — round 2 of 3 (fix-audit)

**Job:** righttenantryagents-boundary-gate-state-fix
**Reviewed sha:** `b1ebd96` (r1 was `39443b2`, CHANGES_REQUESTED)
**r1 audit:** 1/1 blockers FIXED, 2/2 warnings FIXED ✅
**Reviewers:** 7/7 (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 12/12 reviewer findings survived code re-verification — 0 discarded. Fix-audit run first against r1/consolidated.json.

---

### Fix audit (prior round → this sha)

| r1 finding | sev | status |
|---|---|---|
| **B1** telemetry event `compliance.review_unparseable` renamed to `review_unparsable` (broke test + BQ/Sentry contract) | blocker | ✅ **FIXED** |
| **W1** verdict-stamp producer path untested (cross-check tests seed the slot by hand) | warning | ✅ **FIXED** |
| **W2** cross-check trusts `passed` alone, ignoring `violation_count` | warning | ✅ **FIXED** |

- **B1** — `compliance_enforcement.py:239` restored to `compliance.review_unparseable` (matches parent `4e0146f:179`); the test at `test_verification_compliance_judge.py:492` asserts the restored name; `pyproject.toml:101` adds `unparseable` to the codespell ignore-list. **No other stable token was renamed** by the sed — `compliance.repair_unparsable` (`:435`) is a *separate* frozen token that was always spelled `unparsable` in the parent (`4e0146f:356`), and `coerce_json_state.unparsable` / `compliance_repair.unparsable` are unchanged.
- **W1** — 5 *real* producer-path tests added; they drive the actual `log_boundary_compliance_review` / `log_final_compliance_review` callbacks (not hand-seeded stamps) and assert all six stamp fields off the judge's own ctx.
- **W2** — both `finalize_*_gate` guards now require `passed is True AND violation_count == 0`; clean (0 violations) still does **not** abort, and an inconsistent stamp (`passed=True`, `violation_count>0`) now aborts. Both gates covered.

**Core fix (state-view reads) unchanged + still correct** — every gate read still uses `ctx.session.state`; the three `ctx.state.get(STATE_PIPELINE_ERROR)` reads are node-local early-exits (correct); the `scrub_boundary_violations(ctx.state,…)` call is the out-of-scope r1 note. The three load-bearing invariants all hold.

**Suite:** `uv run pytest tests/unit -q` → **2049 passed, 10 warnings**. `ruff check .` clean. `uv run --group lint codespell` clean.

The 6 r1 notes carry forward unchanged (out of r2's B1/W1/W2 scope) — none worsened.

---

### Blockers
_None._

### Warnings
_None._

### Notes

> The lead note (⚠️) is the only one worth a real follow-up; the rest are nits. None block merge.

1. ⚠️ **Defensive cross-check only guards `review is None` — a stale *dirty* review from a prior attempt can still beat a clean stamp on a re-judge** *(blind + edge — reviewer agreement)* — `boundary_compliance_remediation.py:324-371` (mirror in `final_compliance_remediation.py:271-301`). The cross-check lives inside `if review is None:`, and the gate loop never clears the review slot between attempts (only `JUDGE_META` is popped). So in a multi-attempt gate where a prior dirty attempt left a dirty review in the slot **and** the final clean attempt's `output_key` write is lost to a state-prop failure while its stamp lands, finalize reads the stale dirty review (non-None) → skips the cross-check → fail-closes on stale data, dropping the clean verdict (the #172 harm, residual multi-attempt case). **Code-structure gap confirmed by two independent lenses; reachability of the triggering window is unverified** (stamp + output_key ride the same child→parent merge), and it's pre-existing since r1 (r2 only added `violation_count` to the condition). All three stated load-bearing invariants still hold. **Cheap fix:** clear the review slot before each re-judge so a lost final write yields `None` and hits the existing cross-check.

2. **`STATE_COMPLIANCE_REVIEW_VERDICT` missing from `state_init._COMPLIANCE_REVIEW_KEYS` entry-clearing** *(edge)* — `state_init.py:55-61,236-238`. The pipeline clears the compliance review/repair slots at entry "so a stale review from a previous invocation must never be read as this run's verdict" — but the new stamp key isn't in that list. Extends r1 note #2. Production (Vertex/Database) is safe (ADK trims `temp:` keys from persisted deltas); InMemory (tests/dev) reused sessions could leak. Fix: add the key to the clearing list.

3. **Stamp's `parseable` field is write-only dead state; the prop-failure warning hardcodes `review_parseable: False` though the triggering stamp always has `parseable=True`** *(blind + architecture)* — `compliance_enforcement.py:164`; guards read only `passed`/`violation_count`; warning extra at `boundary:339-346`. No `get("parseable")` reader anywhere in `tenant_scorer/`. Fix: drop the field, or log `verdict.get("parseable")`.

4. **r1's imprecise `ctx.state` comment re-asserted in new r2 comment lines** *(acceptance + architecture, carry-forward)* — `agent.py:594-597,670-676`. ADK 2.2.0 wraps `session.state` by reference, not a copy; "snapshot taken at construction" is imprecise (the divergence is a *reassignment* of `session.state` mid-run). Fix: reword per r1 note #3.

5. **Final gate lacks the dirty-stamp (`passed=False`) fail-close test the boundary gate has** *(codebase)* — `test_gate_state_marshalling.py:298-321,381-426`. The W2 hardening itself is tested for both gates; the dirty-stamp direction runs the same fall-through as the tested no-stamp case, so risk is low. Fix: mirror the boundary-gate dirty-stamp tests with `judge_kind='final'`.

---

**Verdict:** ✅ **READY TO MERGE**

All of r1's actionable findings (1 blocker, 2 warnings) are correctly fixed and verified, the core state-marshalling fix is intact, and the suite + linters are green. The 5 new notes are non-blocking defense-in-depth / state-hygiene / doc / coverage nits; none warrant another round.

_Address findings and push, or ack and merge — relaying to the implementing minion via the review relay._
