You are reviewer **tests** in a Perkins round-2 fix-audit.

First read /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/_shared_context.md in full. Then read the delta at /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/r1-to-r2-delta.patch. Your worktree (read code here): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r2.

## YOUR LENS
Test-coverage analysis of the delta (it is ~90% new tests). For each NEW test, is it REAL (asserts meaningful state, not tautological)? Specifically verify: honeypot_filled_stop_post_does_not_object_test asserts row+evidence state (not just 200); focus_seconds_reported_flows_into_the_result_test is a real POST→result read; the channel_check test is a real CHECK-violation assertion. Classify coverage of the r1 findings as FULL/PARTIAL/NONE. Emit the advisory gate (PASS/CONCERNS/FAIL) as one finding.

## OUTPUT
Write ONLY a JSON array to the file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/tests.json
Follow the OUTPUT CONTRACT in the shared context exactly. Source value MUST be "tests". Then stop.
