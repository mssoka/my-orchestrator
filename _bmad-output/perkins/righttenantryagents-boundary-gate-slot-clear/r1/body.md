## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantryagents-boundary-gate-slot-clear
**Reviewed sha:** `062c3ff` (head unchanged at post)
**Reviewers:** 7/7 completed (edge retried once — first pane spun 16+ min with no output; retry succeeded with `[]`)
**Verification:** 8/11 reviewer findings survived code re-verification — 3 discarded as false-positive/prompt-artifact (all blind)

### Blockers (0)

None.

### Warnings (1)

**W1 — Regression tests model an unreachable window; the clean verdict stamp derives from the SAME slot whose write the test claims is "lost"** · `codebase` · `tests/unit/test_gate_state_marshalling.py:468-477` (+ final mirror `:583-597`)

The clean stamp (`passed=True`) is written by `_emit_review_telemetry` as `passed=review.passed`, where `review` is the non-`None` result of `_read_review(callback_context.state[review_key])` (`compliance_enforcement.py:376-386, :360-364`). A lost/empty slot makes `_read_review` return `None` → `_emit_failed_review_rollup` stamps `passed=False` (`:251-291`). So in production a clean stamp **requires** the slot to have held a clean review — in which case the gate (reading `ctx.session.state`) also sees it and returns, never reaching finalize. The "clean stamp + lost slot write" combo the test manufactures is therefore **unreachable via the real telemetry path**; the test hand-seeds `live[STATE_COMPLIANCE_REVIEW_VERDICT] = {passed: True, …}` directly to create it.

The fix is still correct per-attempt **hygiene** (slot authoritative; a stale dirty review from a prior attempt can't survive) and ships either way — but the new comments + `_multi_attempt_judge_run_node` docstring over-claim a "rescue a clean verdict from a lost write" harm that cannot occur. **Recommended:** keep the pop; re-scope the comments/docstring to the real guarantee ("the slot is authoritative per-attempt — a stale dirty review can never survive into the next attempt's slot"), and optionally add a test that drives the *reachable* window (dirty/failed-rollup stamp on a genuinely-lost write) and asserts the honest fail-close path.

### Notes (7)

- **N1 — Cross-check confirmed present** · `blind` (resolved) · `boundary_compliance_remediation.py:324-345` / `final_compliance_remediation.py:272-291` — the `review is None` cross-check the pop relies on is real and correct in both finalize guards (both directions + the W2 `passed AND violation_count==0` hardening). Not a defect; confirmation the fix's premise holds.

- **N2 — Comment mechanism framing** · `acceptance` · `agent.py:584-596`/`:676-686` — the output_key **write-skip** reachability is real and verified in-codebase (`anonymizer.py:307`, `pii_reviewer.py` before-callback, `LlmAgent._save_output`). The new comments frame the trigger as a "state-prop failure / state-view divergence"; an empirical harness on the pinned `google-adk==2.2.0` did not reproduce that divergence. Out of scope to re-derive the #172 base premise; the comments could name the write-skip mechanism but are consistent with the existing #173 comments.

- **N3 — Carry-forward (#173 r2): stamp slot `STATE_COMPLIANCE_REVIEW_VERDICT` not in `state_init._COMPLIANCE_REVIEW_KEYS`** · `security` · `state_init.py:55-62` — a reused `InMemorySession` (tests/dev) could carry a prior invocation's clean stamp. Production (Vertex/Database) is safe (ADK trims `temp:` keys). Defense-in-depth only; pre-existing, not introduced by this delta. Independent follow-up.

- **N4 — Gate asymmetry verified CORRECT** · `architecture` · `agent.py:596,686` — both gates pop the exact key their judge writes + their finalize reads; `STATE_FINAL_OUTPUT` (the scrubber-mutated v4 payload) is rightly **not** popped. `output_key="verification_compliance_review"` / `"final_compliance_review"` match the popped constants.

- **N5 — All four re-judge loops now clear** · `architecture` · `agent.py:264,596,686` + `pii_reviewer.py` before-callback — this PR brings the two compliance gates in line with the established clear-before-re-judge pattern (inline-branch + anonymizer loops already did). No loop re-judges without clearing.

- **N6 — Suite-count nit (briefing, not the PR)** · `codebase` — integration run is `34 passed + 15 xfailed` (the 15 are model-access xfails), not "11"; unit `2051` is exact. Green either way.

- **N7 — Advisory test gate: PASS** · `tests` — `test_gate_state_marshalling.py` 20/20 (18 + 2 new); full unit `2051 passed`; ruff clean. Negative control empirically bites (see independent checks).

### Reviewer Agreement

No formal multi-source finding survived (the 3 blind findings on the cross-check/reachability theme were rejected). Three single-source findings (W1, N2, N1) form a complementary thematic cluster on comments/cross-check accuracy — kept separate.

### Perkins independent checks (every load-bearing lens-guard)

1. **Both gates pop the RIGHT key** ✅ — boundary `STATE_VERIFICATION_COMPLIANCE_REVIEW` (`agent.py:596`); final `STATE_FINAL_COMPLIANCE_REVIEW` (`agent.py:686`); `output_key`s + `_AGENT_REVIEW_KEY` match; `STATE_FINAL_OUTPUT` correctly untouched.
2. **Regression test drives the REAL path + negative control bites** ✅ — `_run_*_compliance_gate` loops run through `_DivergentCtx` (real scrub + real finalize + real cross-check); only judge state-writes + repair stubbed. **Neutralized both pops → the 2 new tests FAILED; restored → 20/20 green.** Not a `simulate.form_body`-style mask.
3. **#173 invariants hold** ✅ — cross-check both directions, `ctx.session.state` reads, W2 `passed AND violation_count==0` hardening, producer-path stamp tests — all green; nothing regressed by the 2-line delta.
4. **No other gate-loop re-judges without clearing** ✅ — all 4 re-judge loops clear (inline-branch `:264`, anonymizer via `pii_reviewer` before-callback, boundary `:596`, final `:686`).
5. **Reachability claim** ⚠️ partially confirmed / overtaken — the output_key write-skip is real (`anonymizer.py:307`, `pii_reviewer.py`), but the relevant *clean stamp + lost write* window is **unreachable** (the stamp's `passed=review.passed` derives from the slot via `_read_review`). The fix is correct hygiene either way → ships. See W1.

### Verdict: READY TO MERGE

0 blockers. The fix is correct per-attempt slot hygiene, both keys are right, all #173 invariants hold, and the negative control bites. The one warning (W1) is non-blocking doc/test-fidelity — the test models an unreachable window and the comments over-claim a harm that can't occur, but the pop is correct hygiene regardless and the briefing sanctions shipping either way. Suggested follow-up: tighten the comments/docstring to the real guarantee and (optionally) add a test for the reachable fail-close window.

---

Address findings and push, or reply with questions. Round 2 follows on the next push (or on request).
