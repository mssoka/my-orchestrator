# Perkins briefing — round 1: righttenantryagents-boundary-gate-slot-clear

- **PR:** https://github.com/solarity-services/RightTenantryAgents/pull/174 (targets `develop`)
- **Reviewed sha:** `062c3fff63c8f70ee188bbde94b386d54acbe78f` (short `062c3ff`; commit "fix(compliance): clear review slot per-attempt in both gates (#172 residual)")
- **repo_root:** `/Users/moses/code/RightTenantryAgents`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantryAgents/perkins-boundary-gate-slot-clear-r1` — detached at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantryagents-boundary-gate-slot-clear.md` (the pinned Perkins finding) + issue #172 context (closed by #173). No new issue.
- **prior_findings:** the #173 rounds' consolidated.json files (`_bmad-output/perkins/righttenantryagents-boundary-gate-state-fix/r1/` + `/r2/`) — this is a residual follow-up on the SAME code path; the #173 invariants carry forward. Reference them for context; this round's fix-audit target is the delta.
- **Owner (for `bin/perkins-token`):** `solarity-services`
- **Model:** zai-coding-cn/glm-5.2 (kimi quota down — the sanctioned review fallback).

## What the PR does (review scope)

**Residual of #172 (closed by #173):** the multi-attempt stale-dirty-review case. #173's defensive cross-check lives **inside `if review is None:`** (`boundary_compliance_remediation.py:324-371`, mirror `final_compliance_remediation.py:271-301` — read current line numbers), and the gate loop **never clears the review slot between attempts** (only `JUDGE_META` is popped). So in a multi-attempt re-judge, a prior dirty review can survive in the slot; if a clean attempt's `output_key` write is lost (state-prop failure) while its stamp lands, `finalize` reads the stale dirty review (non-None) → skips the cross-check → fail-closes on stale data → drops a clean verdict.

**The fix (two lines):** pop the compliance-review slot at the top of each attempt in BOTH gates:
- Boundary: `_run_boundary_compliance_gate` pops `STATE_VERIFICATION_COMPLIANCE_REVIEW` before `ctx.run_node(judge)`.
- Final: `_run_final_compliance_gate` pops `STATE_FINAL_COMPLIANCE_REVIEW` — **NOT `STATE_FINAL_OUTPUT`** (a briefing-error correction: `STATE_FINAL_OUTPUT` is the audited v4 payload the scrubber mutates; popping it would empty the reviewer's `{final_output}` placeholder — the minion documented this asymmetry in inline comments).

This makes the slot authoritative-per-attempt: a lost write → `None` → the existing cross-check catches it.

**Regression test:** drives the REAL path — the actual `_run_*_compliance_gate` loops through the production state-view divergence (`_DivergentCtx`); real scrub + real finalize + real cross-check; only the judge's state-writes + repair pass stubbed. The minion claims: neutralized pops → both new tests FAIL (stale dirty review `passed: False` survives alongside the clean stamp, finalize bypasses the cross-check, fail-closes); restored → pass. The inverse (genuinely-missing judge still fail-closes) is asserted. Suite: 2051 unit + 11 integration, ruff clean.

**Reachability finding (secondary):** the minion claims the window is REAL, not theoretical — ADK skips the `output_key` write on empty chunks / schema-validation-fail / tool-call-only responses (documented at `anonymizer.py:313`, `pii_reviewer.py:248`) while the judge's `after_agent_callback` (which stamps the verdict) always fires. Verify this claim.

## ⚠️ CRITICAL lens-guards (read before any lens — prevents false positives)

Production ADK agent code. The diagnosis is PINNED (Perkins' own finding from the #173 review) — review the FIX, don't re-derive the bug.

- **THE SLOT-KEY CORRECTNESS IS LOAD-BEARING.** Verify BOTH gates pop the RIGHT key: `STATE_VERIFICATION_COMPLIANCE_REVIEW` (boundary) + `STATE_FINAL_COMPLIANCE_REVIEW` (final) — and that the briefing's originally-named `STATE_FINAL_OUTPUT` was correctly NOT popped (popping it would empty the reviewer's `{final_output}` placeholder). A wrong key = the fix is inert (or worse, breaks the reviewer). Trace the constants + their consumers.
- **THE REGRESSION TEST MUST DRIVE THE REAL PATH — no mask** (the #599 r2 lesson, explicitly carried into this briefing). Verify the test: (a) exercises the actual `_run_*_compliance_gate` loops through the production state-view divergence, (b) its negative control genuinely bites (neutralizing the pops makes it FAIL — the stale-dirty-review-wins scenario), (c) it does NOT bypass the real wiring (no `simulate.form_body`-style shortcut), (d) the inverse (genuinely-missing judge fail-closed) is real.
- **THE #173 INVARIANTS MUST STILL HOLD** (carry-forward): single-attempt `review is None` cross-check (both directions: clean stamp + None → no abort; missing judge → abort), the `ctx.session.state` state-view reads, the `passed AND violation_count==0` W2 hardening, the producer-path tests. The delta should be the two pops + tests ONLY.
- **No OTHER gate-loop re-judges without clearing its review slot** — grep the gate code for other loops that call `ctx.run_node(judge)`/re-judge without a slot pop (the briefing's verify item).
- **The reachability claim** (ADK skips `output_key` writes on empty-chunk/schema-fail/tool-call-only while the stamp always fires) — verify against the cited code (`anonymizer.py:313`, `pii_reviewer.py:248`) + the ADK semantics (adk-cheatsheet). If the claim is wrong, it's a note (the slot-clear is correct hygiene regardless — the briefing says ship it either way), not a blocker.
- **Suite claims** (2051 unit + 11 integration, ruff clean) — verify real.
- **Do NOT re-open the #173 findings** (all fixed + verified in r2) — carry-forward markers only.

### Legitimate findings here would be
- **A wrong slot key popped** (e.g. `STATE_FINAL_OUTPUT` popped after all, or the boundary key mismatched) — the fix is inert or harmful.
- **The regression test masks the fix** (bypasses the real path; the negative control doesn't bite) — the #599 r2 failure mode, a blocker.
- **A #173 invariant regressed** by the delta (cross-check, state-view reads, W2 hardening, producer tests).
- **Another gate-loop re-judges without clearing** its review slot.
- **A Python test failure** or ruff breakage.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 174 --repo solarity-services/RightTenantryAgents` → `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-slot-clear/r1/diff.patch`. Every lens reviews these identical bytes.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff just saved, `worktree` = your cwd (the detached round worktree), `spec_files` = this briefing + the job briefing (+ the #173 round briefings/consolidated.json for context), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantryagents-boundary-gate-slot-clear/r1`, `prior_findings` = none for this PR (the #173 rounds are CONTEXT, not prior findings of this PR). Headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), `<lens>.json` output contract + existence check, one retry per failed lens, verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`). Mint first, then review — never run gh with an empty GH_TOKEN:
  1. `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)` — **capture STDOUT ONLY. NEVER append `2>&1`**.
  2. Check for an EMPTY token, NOT `$?`: `if [ -z "$TOKEN" ]` → fall back to `gh pr comment 174 --repo solarity-services/RightTenantryAgents --body-file <body.md>`, note `fallback-comment`.
  3. Otherwise: `GH_TOKEN=$TOKEN gh pr review 174 --repo solarity-services/RightTenantryAgents --<event> --body-file <body.md>`.
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `<old>`, head now `<new>` — a fresh round will follow".
- Body format: `## 🤖 Perkins automated review — round 1 of 3` / **Job:** righttenantryagents-boundary-gate-slot-clear / **Reviewed sha:** 062c3ff / **Reviewers:** <x>/7 / **Verification:** <confirmed>/<total>… / ### Blockers (n) / ### Warnings (n) / ### Notes (n) / **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED / the "Address findings and push…" footer.
- Self-report: `/Users/moses/code/bin/ledger set righttenantryagents-boundary-gate-slot-clear-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Close out: leave the worktree in place for Silas (removing your own cwd mid-close-out is the footgun); close all lens panes. Silas owns the round row status.
- Skip the `code-review` skill's Step 5 (interactive fix flow) entirely — fixing is the implementing minion's job, triggered by the review relay.
