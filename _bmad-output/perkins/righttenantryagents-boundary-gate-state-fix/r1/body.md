## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantryagents-boundary-gate-state-fix
**Reviewed sha:** `39443b2` (head unchanged at review time)
**Reviewers:** 7/7 completed (blind · edge · acceptance · security · architecture · codebase · tests) — 0 failed
**Verification:** 9/10 unique findings survived code re-verification — 1 discarded as false-positive (28 raw findings deduped to 10). All blocker/warning claims independently re-verified against the worktree at `39443b2` + the installed `google-adk==2.2.0`.

**Independent Perkins checks (beyond the lenses):**
- **ADK state-view semantics — CONFIRMED correct.** The cheatsheet documents `ctx.session.state` as the cross-agent read convention; an empirical repro against real ADK 2.2.0 shows `ctx.state._value` (a reference to `session.state` captured at `Context` construction) goes stale when `session.state` is reassigned during a child `run_node`, while `ctx.session.state` re-reads the live attribute. The fix's `ctx.session.state` reads are correct and complete for the child-`output_key` slots.
- **Fail-closed invariant holds both directions.** Genuinely-missing judge (no stamp) → aborts; clean stamp + None review → does not abort; dirty/wrong-judge stamp → aborts.
- **Negative control passes.** Reverting the fix's reads + finalize calls to `ctx.state` makes 7/16 new tests fail (incl. clean-verdict + genuinely-missing). The tests are real, not tautological.
- **#169 is model-name-only** (`git show --stat fb98f8f` touches only deployment/terraform/README/env/config). The `ctx.state` read predates #169 (introduced in `cb8eb4c` / #156). Latent, not a regression — the model change raised the clean-verdict rate and exposed it.
- **No other child-`output_key` `ctx.state` reads remain in the gates** (remaining `ctx.state` reads are `STATE_PIPELINE_ERROR`, node-local). `scrub_boundary_violations`/`apply_repairs` still take `ctx.state` — explicitly out of scope (dirty path, works in prod).
- **Full unit suite: 2041 passed / 1 FAILED** (not the claimed 2042 green) — see Blocker 1. Ruff clean. Integration `test_loop_stop_aborts_pipeline_and_downstream_agents_skip` + 6 others pass.

### Blockers (1)

**B1 — Accidental telemetry rename breaks a test + a stable event-name contract** `[blind, edge, acceptance, codebase, tests]`
`tenant_scorer/callbacks/compliance_enforcement.py:239` · `tests/unit/test_verification_compliance_judge.py:491`
The PR renamed `"compliance.review_unparseable"` → `"compliance.review_unparsable"` (dropped the `e`). Parent (`develop` `4e0146f:179`) had the correct spelling; the diff hunk `@@-176,7+236,7@@` changed it. `test_unparseable_review_emits_failed_rollup` now **fails** (suite is 2041/2042, not 2042 green), and the structured event name is a documented BigQuery/Sentry query contract (issue #172's own evidence greps `compliance.review_completed`). This is an unrelated drive-by edit, not part of the state-marshalling fix.
**Fix:** restore the `e` — `"compliance.review_unparseable"`. One character; nothing else.

### Warnings (2)

**W1 — The verdict-stamp producer path is untested** `[blind, tests, acceptance]`
`tests/unit/test_gate_state_marshalling.py:164` vs `compliance_enforcement.py:284,359`
The defensive cross-check's entire value rests on the stamp being written by the judge's own callback. The new tests verify the cross-check's *read/decide* logic by **seeding** `STATE_COMPLIANCE_REVIEW_VERDICT` into the state dict; none drive `log_boundary_compliance_review` / `_emit_review_telemetry` / `_emit_failed_review_rollup` and assert the stamp actually lands with the right `judge_kind`/`passed`/`violation_count`. A bug in the stamp *write* path would be invisible — the independent witness could be silently absent in production while every test stays green.
**Fix:** add a test that runs the real after-callback on a clean and a dirty review and asserts the stamp. The now-failing `test_unparseable_review_emits_failed_rollup` is a natural place to also assert the `passed=False` stamp.

**W2 — Cross-check trusts the stamp's `passed` alone, ignoring its own `violation_count`** `[security]`
`boundary_compliance_remediation.py:334` · `final_compliance_remediation.py:278`
`finalize_*_gate` skips the abort whenever `verdict.get("passed") is True`, without consulting `verdict["violation_count"]`. `_stamp_review_verdict` writes both from one review, so today `passed=True` ⇒ `violation_count=0` — but the guard is brittle: a future `coerce`/model change yielding `passed=True` with non-empty violations, combined with a `None` review, would skip the halt and ship unaudited prose. Defense-in-depth gap on a safety path.
**Fix:** require `passed is True AND violation_count == 0` before skipping the abort. Cheap.

### Notes (6)

- **N1 — `STATE_PIPELINE_ERROR` write now bypasses the `State._delta`/event flush** `[acceptance, architecture]` — `agent.py:632,716`. *(The lenses' "error invisible to the terminal envelope" **blocker is rejected** as a false positive: `build_response_envelope(ctx.state)` reads `STATE_FINAL_OUTPUT` — a cross-node write — reliably, since the pipeline ships success envelopes; a global `ctx.state` staleness would break the whole pipeline, not just the error path, and `test_loop_stop_aborts_pipeline_and_downstream_agents_skip` passes.)* The real, narrow effect: the flag is absent from the node's event delta, so it isn't reconstructed from event history on session rewind/replay — mitigated by `rerun_on_resume=True`. Optional: also set it on `ctx.state` for resumption fidelity, or document it as invocation-local.
- **N2 — Verdict-stamp slot is never cleared** `[blind, architecture, edge]` — `agent.py:626,713`. Unlike `STATE_COMPLIANCE_JUDGE_META` (popped in `finally`), the stamp is write-only. `temp:` scoping trims it from event deltas so it doesn't persist on Database/Vertex session services (production-safe); within one invocation last-write-wins is correct. The "invocation-local" guarantee is by prefix convention, not cleanup. Optional: pop it in the same `finally` blocks.
- **N3 — Fix's inline comment states the wrong mechanism** `[codebase]` — `agent.py:594-597`. "`ctx.state` snapshot taken at construction" is imprecise: in ADK 2.2.0 `ctx.state._value` holds a *reference* to `session.state` (`context.py:181-185`), not a copy; the divergence arises when `session.state` is reassigned during a child run. Rewording would prevent future confusion.
- **N4 — Boundary scrub/repair + inline branch still operate on `ctx.state`** `[architecture, codebase]` — `agent.py:615,535,268`. Out of scope per the PR (minion intentionally left it; dirty-path only, works in prod, existing tests pass). Track as a follow-up audit, not a change here.
- **N5 — `read_review_verdict` docstring/impl drift** `[blind]` — `compliance_enforcement.py:169-188`. Docstring promises `None` for "malformed shape"; impl returns any dict with a matching `judge_kind`. Behavior is safe (finalize re-checks `passed`), pure doc drift.
- **N6 — `_judge_kind` is stringly-typed with an implicit `else`→`'final'`** `[architecture]` — `compliance_enforcement.py:211-212`. A typo'd/new review key would silently satisfy the final gate's cross-check. Narrow today; optionally raise on unknown keys.

### Reviewer Agreement
**5 independent lenses** (blind, edge, acceptance, codebase, tests) independently flagged the `review_unparseable`→`review_unparsable` typo — the highest-confidence finding in the report.

**Verdict: NEEDS CHANGES** — one blocker (an accidental one-character telemetry rename that breaks an existing test + the event-name contract). The core state-marshalling fix is correct, the fail-closed invariant holds both directions, and #169 is confirmed model-name-only. Restore the `e`, address the stamp-producer test gap (W1) if you agree, and this should clear r2.

---
*Automated by Perkins (round 1 of 3). Findings consolidated in `_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1/consolidated.json`. Address findings and push; a fresh round will re-review the new head.*
