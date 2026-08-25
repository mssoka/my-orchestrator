# Perkins briefing — round 1: righttenantryagents-boundary-gate-state-fix

- **PR:** https://github.com/solarity-services/RightTenantryAgents/pull/173 (targets `develop`)
- **Reviewed sha:** `39443b2cca4add0611b9f437ac7ec362f6d9a2ef` (short `39443b2`; commit "fix(compliance): read gate judge output via ctx.session.state (#172)")
- **repo_root:** `/Users/moses/code/RightTenantryAgents`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-boundary-gate-state-fix-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantryagents-boundary-gate-state-fix.md` (Beacon's pinned diagnosis) + GitHub issue #172 (`gh issue view 172 --repo solarity-services/RightTenantryAgents --json title,body,comments`).
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **Model:** zai-coding-cn/glm-5.2 (kimi quota down — the sanctioned review fallback; rc3-3 r2 ran a full 8-pane round to APPROVED on it).

## What the PR does (review scope)

**Production ADK agent code (google-adk==2.2.0).** Fix for issue #172: the boundary + final compliance gates read a child agent's `output_key` via `ctx.state`, but a child's `output_key` write lands on the **live `ctx.session.state`** and is absent from the pipeline node's `ctx.state` snapshot → `ctx.state.get(...)` returns `None` right after `ctx.run_node(judge)` → the gate fail-closes to a **non-retryable `COMPLIANCE_VIOLATION` on a CLEAN verdict** (judge ruled `passed=true, 0 violations`), dropping the vetting (no analysis, no score) as `AiAnalysisTerminalFailure`.

**The fix (mirroring the existing repair-key convention):**
- Boundary + final gates read the judge review + `STATE_FINAL_OUTPUT` off `ctx.session.state`; `finalize_*_gate(ctx.session.state)`.
- Defensive cross-check: judge telemetry stamps each run's verdict to a temp slot (read off the judge's own ctx — the independent witness); `finalize_*_gate` cross-checks a `None` review against it so a clean verdict is never silently dropped.
- `STATE_PIPELINE_ERROR` `ctx.state` reads left untouched (node-local, correct).
- 16 new tests in `tests/unit/test_gate_state_marshalling.py` (drives the real gates through `ctx.run_node` with a divergent fake ctx forcing the production state-view split); 2042 unit tests green + relevant integration + ruff clean.
- #169-regression finding claimed: **latent, not a regression** (the `ctx.state` reads came from `3c1ea0b2` 2026-07-21; #169 is model-name-only; the model change raised the clean-verdict rate → latent fail-close became P0).

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

This is **production agent code on a paying-user path**. The diagnosis is PINNED (Beacon's, confirmed against the code + production logs) — review the FIX, don't re-derive the bug.

- **THE LOAD-BEARING INVARIANT: the genuinely-missing-judge fail-closed path MUST still hold.** The fix's defensive cross-check must NOT weaken the fail-closed-on-missing-review behavior for a judge run that genuinely never happened. Verify: with NO judge telemetry row (genuinely missing), `finalize_*_gate` STILL aborts (fail-closed); with telemetry saying `passed=true` (clean), a contradicting `None` review does NOT abort. Both directions must hold — this is the briefing's required inverse regression test.
- **The state-view semantics are THE bug — verify them against the adk-cheatsheet.** Read the `adk-cheatsheet` skill's state-management section (`ctx.state` vs `ctx.session.state`; when a child `output_key` is visible through each) and confirm the fix's `ctx.session.state` reads are CORRECT + COMPLETE per the documented ADK semantics — not just "matches the minion's claim." A wrong view in the other direction (or a missed spot) is a blocker.
- **No OTHER `ctx.state.get` reads of child-`output_key` state remain in the gates** — grep `ctx.state` across the gate code + the finalizer callbacks; any remaining read of a child's `output_key` through `ctx.state` is the same bug, unfixed.
- **`STATE_PIPELINE_ERROR` reads untouched** — verify `:252/:268` still read `ctx.state` (they're node-local, correct) and the fix didn't accidentally change them.
- **The defensive cross-check must be an INDEPENDENT witness** — it reads the judge's OWN telemetry ctx, not the gate's (buggy) read; a cross-check coupled to the gate's own read couldn't fire. Verify the telemetry slot is genuinely written by the judge's callback + read independently.
- **The regression tests must be REAL, not tautological** — 16 tests driving the real gates through `ctx.run_node` with a divergent fake ctx; validate the negative control (reverting the fix makes them fail — the minion claims this was validated) + the genuinely-missing-judge inverse test exists + passes.
- **The #169-latent claim** — git blame the reads: they should predate #169 (`3c1ea0b2`, 2026-07-21); #169 (`fb98f8f`) should be model-name-only. If the blame shows #169 touched the reads, that's a real regression finding.
- **ADK API surface** — the fix touches `ctx.run_node`, `finalize_*_gate` signatures (widened to `State | dict`), telemetry slots. Verify against the installed `google-adk==2.2.0` (your cwd has it) — no API misuse, no signature breakage.
- **Do NOT flag the pinned diagnosis itself** (the bug's existence is confirmed; the PR is the fix).
- **Do NOT re-litigate** the "do not touch the scrub/repair path" scoping — the minion explicitly left `scrub_boundary_violations(ctx.state, ...)` + `apply_repairs(ctx.state, ...)` untouched as out-of-scope; verify that's true (they still pass their existing tests) rather than demanding they be changed.

### Legitimate findings here would be
- **The fail-closed path is weakened** — a genuinely-missing judge no longer aborts (the cross-check masks it), OR the clean-verdict path still fails closed (the fix is incomplete).
- **A missed state-view spot** — another child-`output_key` read through `ctx.state` in the gates/finalizers, or a `ctx.session.state` read that should be `ctx.state` (the pipeline-error flag).
- **The cross-check is coupled** to the gate's own read (can't independently witness) or reads a slot the judge doesn't write.
- **A regression test is tautological** — doesn't reproduce the split, or the inverse (missing-judge) case isn't covered.
- **The #169 blame claim is wrong** — #169 actually touched the reads.
- **ADK API misuse** against google-adk==2.2.0 (signature/type breakage).
- **A Python test failure** (minion reports 2042 unit green — verify they're real, not skipped/tautological).

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 173 --repo solarity-services/RightTenantryAgents` → `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing + issue #172, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1`, `prior_findings` = none (round 1). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`** (cache warnings on stderr corrupt the token).
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 173 --repo solarity-services/RightTenantryAgents --body-file <body.md>`, note `fallback-comment` in your ledger note + final message.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 173 --repo solarity-services/RightTenantryAgents --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantryagents-boundary-gate-state-fix / **Reviewed sha:** 39443b2 / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantryagents-boundary-gate-state-fix-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
