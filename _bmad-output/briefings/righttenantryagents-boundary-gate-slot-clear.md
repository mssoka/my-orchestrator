# Briefing: righttenantryagents-boundary-gate-slot-clear

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** RightTenantryAgents (`/Users/moses/code/RightTenantryAgents`, base `develop` @ `9d066bc` — **#173 is merged; branch off the fixed code**). Python + ADK.
- **What:** a residual multi-attempt edge case that #173's defensive cross-check does NOT cover (flagged by Perkins during #173's review). Carry the finding verbatim — it is pinned.

## Mission

Close the residual #172-family harm: the boundary/final compliance gates can still fail-close on a **stale dirty review** from a prior attempt, dropping a clean verdict. #173 fixed the single-attempt `review is None` case; this fixes the **multi-attempt stale-non-None** case.

## Root cause (Perkins finding — confirmed against code structure by two lenses)

#173's defensive cross-check lives **inside `if review is None:`** (`tenant_scorer/callbacks/boundary_compliance_remediation.py:324-371`, mirror in `final_compliance_remediation.py:271-301`). The gate loop **never clears the review slot between attempts** — only `JUDGE_META` is popped. So in a multi-attempt re-judge:

1. A prior *dirty* attempt leaves a dirty review in the slot.
2. The final *clean* attempt's `output_key` write is **lost to a state-prop failure** while its **stamp lands**.
3. `finalize` reads the **stale dirty review (non-None)** → **skips the cross-check** → fail-closes on stale data → drops the clean verdict (the #172 harm, multi-attempt path).

Reachability of the triggering window (stamp + output_key ride the same child→parent merge) is **unverified**; the structure allows it. Pre-existing since r1 (#173 didn't introduce it). All three load-bearing invariants still hold.

## The fix (cheap — Perkins' recommendation)

**Clear the review slot before each re-judge**, so a lost final write yields `None` and falls into the *existing* cross-check:
- Boundary gate loop (`tenant_scorer/callbacks/boundary_compliance_remediation.py`): `ctx.session.state.pop(STATE_VERIFICATION_COMPLIANCE_REVIEW, None)` at the top of each attempt, before `ctx.run_node(judge)`.
- Final gate mirror (`tenant_scorer/callbacks/final_compliance_remediation.py`): `ctx.session.state.pop(STATE_FINAL_OUTPUT, None)` analogously.

This makes the slot authoritative-per-attempt: the only way `finalize` sees a review is the current attempt's write — a lost write → `None` → the existing cross-check catches it. (Read line numbers from the current code; Perkins' `324-371` / `271-301` may have shifted post-#173.)

## Regression test (REQUIRED — do NOT mask it)

A test that simulates the **stale-dirty-slot + lost-final-write** window and asserts the clean verdict is **not** dropped (scoring proceeds). **Drive the real path** — do NOT bypass via a `simulate.form_body`-style mask (that was the r2 lesson on #599: an inert fix hidden by a test that skipped the real wiring). The test must exercise the actual slot-clear + cross-check path.

Also assert the inverse still holds: a genuinely-missing judge run still fail-closes correctly (the #173 invariant — don't regress it).

## Reachability check (secondary — informs severity, doesn't block the fix)

Perkins flagged the triggering window as unverified. While you're in the code, confirm whether the stamp + output_key can actually split across the child→parent merge in a multi-attempt gate (i.e., is the lost-write-while-stamp-lands window reachable, or theoretical?). Note the finding in the PR — but **the slot-clear is correct hygiene regardless** (a stale review slot between attempts is a latent bug either way), so ship the fix either way.

## Skills (REQUIRED reading before editing ADK code)

- **`adk-cheatsheet`** — MUST READ. The `ctx.state` vs `ctx.session.state` semantics (and the multi-attempt state-merge behavior) are this bug's substrate.
- **`adk-dev-guide`** — code-preservation rules.
- Self-review: `bmad-review-verification-gap` — explicitly check that the regression test drives the real path and doesn't mask the fix (the r2/#599 lesson).

## Verify
- The review slot is cleared before each re-judge in **both** gates; the single-attempt `None` case (#173) still works; the genuinely-missing-judge fail-closed path still holds.
- Regression test green (driving the real path); existing compliance tests green; ruff clean.
- grep confirms no other gate-loop that re-judges without clearing its review slot.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.** Note "residual of #172 (closed by #173)" in the PR.

## Self-report (do not skip)
- `bin/ledger set righttenantryagents-boundary-gate-slot-clear working` at start
- `bin/ledger set righttenantryagents-boundary-gate-slot-clear in-review "PR <url>"` when PR opens
- `herdr notification show "boundary-gate-slot-clear" --body "<one-line>"` on finish
- Final message: the slot-clear summary, the reachability finding, the regression test, PR URL.

## Dispatch parameters
- repo: RightTenantryAgents · repo_root: /Users/moses/code/RightTenantryAgents · slug: boundary-gate-slot-clear · base: develop
- model: zai-coding-cn/glm-5.2   (kimi down; small, pinned fix + the adk skills guide the subtlety)
- pr_review: 1   (production agent code; Perkins on the glm-5.2 fallback)
- github_issue: (none — note "residual of #172")
