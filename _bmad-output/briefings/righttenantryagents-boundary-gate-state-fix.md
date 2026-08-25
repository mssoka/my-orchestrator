# Briefing: righttenantryagents-boundary-gate-state-fix

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** RightTenantryAgents (`/Users/moses/code/RightTenantryAgents`, remote `solarity-services/RightTenantryAgents`, base `develop`). Python + **ADK** (`google-adk==2.2.0`).
- **Issue:** [#172](https://github.com/solarity-services/RightTenantryAgents/issues/172) — Beacon triage, confidence-high. **Carry Beacon's diagnosis verbatim — it is pinned; do not re-derive.**

## Mission

Fix a state-marshalling bug where the **boundary compliance gate fail-closes (non-retryable `COMPLIANCE_VIOLATION`) on a CLEAN verdict**, aborting scoring and emitting `AiAnalysisTerminalFailure`. The compliance judge rules `passed=true, 0 violations`, but the gate reads `None` for the review one call later and halts. This drops vettings — no analysis, no score.

## Root cause (Beacon's diagnosis — confirmed against the code)

Cross-agent state is read through the wrong view. The codebase convention (documented in comments at `tenant_scorer/agent.py:263` and `:396`) is that a child agent's `output_key` write lands on **`ctx.session.state`** (the raw session dict), NOT the `ctx.state` wrapper — so a `ctx.state.get(...)` immediately after `ctx.run_node(...)` returns `None`.

Confirmed divergence in `tenant_scorer/agent.py`:
- `:588` — the judge's `after_agent_callback` **writes** `STATE_COMPLIANCE_JUDGE_META` via `ctx.session.state` ✅ (correct).
- `:594` — `_run_boundary_compliance_gate` **reads** `STATE_VERIFICATION_COMPLIANCE_REVIEW` via `ctx.state.get(...)` ❌ (the bug — returns `None`).
- `:620` — `finalize_boundary_gate(ctx.state)` passes the wrong view into the finalizer ❌.
- `:404 / :436 / :475-477` — the repair keys (`STATE_COMPLIANCE_REPAIR_REQUEST/_RESULT/_META`) are **already** handled via `ctx.session.state` ✅ — this is the template the gate should mirror.
- `_run_final_compliance_gate` (the parallel final gate, ~`:661/:673/:680` + `finalize_final_gate(ctx.state)` at ~`:694`) has the **same** bug — fix both gates.
- `finalize_boundary_gate` lives in `tenant_scorer/callbacks/boundary_compliance_remediation.py`; the callback `_read_review` in `tenant_scorer/callbacks/compliance_enforcement.py`.

This is **not** a compliance false-positive and **not** a real violation — there is no protected-ground content. It is a state-propagation bug. Distinct from the older `RT-PROD-C` / #156 family (that escalated a *real* flagged violation; this escalates a verdict the judge ruled *clean*).

## The fix

**Primary — align the reads with the documented convention (mirror the repair-key treatment):**
- `tenant_scorer/agent.py:594` — read `STATE_VERIFICATION_COMPLIANCE_REVIEW` via `ctx.session.state.get(...)` instead of `ctx.state.get(...)`.
- Apply the same to the final gate's parallel reads (~`:661/:673/:680`) and `STATE_FINAL_OUTPUT`.
- `:620` and ~`:694` — pass `ctx.session.state` into `finalize_boundary_gate(...)` / `finalize_final_gate(...)`.
- Do NOT touch the `STATE_PIPELINE_ERROR` reads at `:252/:268` (those are correct on `ctx.state` — the pipeline-error flag is set/read within the same view).

**Defensive hardening (Beacon's secondary — so a `None` read can't silently drop a clean analysis):** `finalize_boundary_gate` / `finalize_final_gate` currently treat a `None`/unparseable review slot as halt-worthy. Gate that behind a cross-check: if the per-attempt telemetry row `compliance.review_completed` for this `run_id`/`attempt` says `passed=true` (clean), a contradicting `None` is a state-prop failure, not a compliance verdict — do **not** abort scoring. Fail-closed-on-missing-review stays correct for a *genuinely* missing judge run.

## Regression question (check, don't block on it)

`develop` HEAD is the `#169` (model-flash / `compliance-guard-hardening`) merge — Beacon flags this as "post-#169." `git blame` line `:594` and the final-gate reads: did #169 introduce or touch the `ctx.state` read? If yes, it's a regression (note it in the PR); if the read predates #169, the bug was latent and #169 just exposed it. Either way the fix is the same.

## Skills (REQUIRED reading before editing ADK code)

- **`adk-cheatsheet`** — MUST READ. The `ctx.state` vs `ctx.session.state` semantics (and when a child `output_key` is visible through each) are exactly this bug. Confirm the fix against the cheatsheet's state-management section.
- **`adk-dev-guide`** — code-preservation rules + the spec-driven workflow.
- Self-review: `code-review` skill (or `bmad-review-edge-case-hunter`) on the state-view change — specifically that the genuinely-missing-judge fail-closed path still holds.

## Regression test (REQUIRED)

Add an integration test that drives the **boundary** gate through `ctx.run_node(judge)` on a **clean** verdict (`passed=true`, `violations=[]`) and asserts `finalize_boundary_gate` does **NOT** set `STATE_PIPELINE_ERROR` and scoring proceeds. Plus the inverse: a **genuinely missing** judge run still fail-closes correctly. Cover the **final** gate analogously.

## Blast-radius check (secondary — if Sentry/BigQuery creds are available)

Beacon's P0 concern: if the `ctx.state` read is *consistently* `None` (not a delta-merge race), every post-#169 vetting reaching the boundary gate fails-closed → no vettings complete. Grep the last 7 days of `AiAnalysisTerminalFailure` / `COMPLIANCE_VIOLATION` envelopes (Sentry `RT-PROD-J`; BigQuery invocation logs) to size the blast radius + identify any failed vettings that need re-processing. Use the `sentry-cli` skill if helpful. Don't block the fix on this — the fix proceeds regardless; this informs severity + recovery.

## Verify

- The boundary **and** final gates no longer fail-close on a clean verdict; the genuinely-missing-judge fail-closed path still works.
- Regression tests green; existing compliance tests green; `make` test target green (check the repo's test command — pytest).
- No other `ctx.state.get` reads of child-`output_key` state remain in the gates (grep to confirm).
- After user approval: commit, push, open PR targeting `develop`. **Never merge.** Link/closes #172.

## Acceptance
- `ctx.session.state` reads in both gates + finalize calls; defensive cross-check added; regression test green; blast-radius noted if checked.
- PR description carries the root cause + the #169-regression finding + "closes #172."

## Self-report (do not skip)
- `bin/ledger set righttenantryagents-boundary-gate-state-fix working` at start
- `bin/ledger set righttenantryagents-boundary-gate-state-fix in-review "PR <url>"` when PR opens
- `herdr notification show "boundary-gate-state-fix" --body "<one-line>"` on finish
- Final message: fix summary, the #169-regression finding, test added, blast-radius if checked, PR URL.

## Dispatch parameters
- repo: RightTenantryAgents · repo_root: /Users/moses/code/RightTenantryAgents · slug: boundary-gate-state-fix · base: develop
- model: zai-coding-cn/glm-5.2   (kimi down; production ADK code — frontier-preferred, but the diagnosis is pinned + the adk skills guide the subtlety, so glm-5.2 is adequate)
- pr_review: 1   (production agent code; Perkins on the glm-5.2 fallback)
- github_issue: 172
