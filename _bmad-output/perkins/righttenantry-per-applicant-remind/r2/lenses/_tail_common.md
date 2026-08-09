

--- SPEC / CONTEXT ---
This is ROUND 2 of 3 for PR #586 ("Add per-applicant Remind button to the Awaiting list", targeting develop). Round 1 (sha c6868b8) APPROVED with 0 blockers, 4 warnings, 1 note. Since then the user folded W1 + W3 into the PR pre-merge (single new commit b48b581, "Fold review W1 + W3 into per-applicant remind" — the ONLY change since r1). W2 and N1 were deliberately deferred to a tracked follow-up, NOT part of this PR.

PRIOR-ROUND FINDINGS — read /Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r1/consolidated.json for the full record:
- W1 [policy-gate]: `ApiReturnedApplicantReminder` omitted from `msg_triggered_policy_reaccept` allowlist (bulk sibling `ApiReturnedReminder` is listed) → FOLDED IN. Confirm the new allowlist arm is correct and complete.
- W2 [duplication]: `handle_remind_applicant` copy-pastes ~110 lines of `handle_remind_applicants` scaffolding → DELIBERATELY DEFERRED follow-up. Do NOT re-raise as a blocker; a note is acceptable only with NEW evidence.
- W3 [coverage-gap]: request-validation 400 branches (require_json, decode, empty email, invalid email) untested → FOLDED IN. Confirm the 3 new tests genuinely exercise the branches and bite (not tautologies).
- W4 [coverage-gate]: advisory gate CONCERNS (P0 100%, P1 ~87.5%) → evaluate whether W3's new tests lift the gate to PASS.
- N1 [duplication]: awaiting-refetch block duplicated between bulk and per-applicant response handlers → DELIBERATELY DEFERRED follow-up. Do NOT re-raise as must-fix.

ROUND-2 FOCUS (the fold-in, commit b48b581; the diff above is the full PR — the fold-in hunks are the 1-line client.gleam allowlist addition and the 3 new integration tests):
1. W1 fold-in: is the allowlist arm correct (pattern matches the Msg variant), complete, and does it actually route a policy-reaccept 428 to the reaccept modal (not an error toast)?
2. W3 fold-in: do the 3 new tests exercise the real 400 branches (malformed body / decode failure, empty email, invalid email), assert the right things, and fail if the branch broke?
3. No-regression: did the fold-in touch anything else (gate-respecting logic, bulk path, atomicity, client handling)?

CRITICAL LENS-GUARD (deliberate user-confirmed decisions — do NOT flag as defects):
- Do NOT flag "no force-remind / can't bypass the stage gate" — gate-respecting-only is the confirmed design; force-remind is a deferred follow-up.
- Do NOT flag "reuses the bulk plumbing instead of standalone" — reusing valid_recipients / send_reminders_background / the template is the explicit requirement. Verify the reuse is correct, not that it exists.
- Do NOT flag W2 (copy-paste/dedup) as a must-fix blocker, and do NOT flag N1 (refetch duplication) as a must-fix — both deliberately deferred, tracked follow-ups.
- Do NOT flag the bulk button coexisting with the per-row button — the per-applicant button is deliberately ADDITIVE.

Legitimate r2 findings WOULD be: the W1/W3 fold-in is incorrect or incomplete (allowlist arm wrong/missing/not firing the modal; tests don't bite or test the wrong branch); the fold-in introduced a regression (gate breach, atomicity gap, broken bulk path, broken client handler); a NEW issue in the b48b581 hunks; a parse/test regression.

WORKTREE (the reviewed checkout at sha b48b581 — verify all claims against these files): /Users/moses/.herdr/worktrees/RightTenantry/perkins-per-applicant-remind-r2

Full specs (read with your read tool):
- Round briefing: /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-per-applicant-remind-r2.md
- Original job briefing (the spec with acceptance criteria): /Users/moses/code/_bmad-output/briefings/righttenantry-per-applicant-remind.md
- Prior round findings: /Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r1/consolidated.json (and the r1 lens outputs in the same r1/ directory)
- The fold-in commit, if useful: git -C /Users/moses/.herdr/worktrees/RightTenantry/perkins-per-applicant-remind-r2 show b48b581

Test status at this sha (verified by Perkins): server unit 1221 passed; integration 393 passed (includes the 3 new validation tests); client 463 passed.

--- YOUR LENS ---
