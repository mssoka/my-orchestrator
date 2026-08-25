# righttenantry-demo-bulk-invite-guard

## Task

Demo-mode bulk invite must not attempt sends. User report + ruling
(2026-08-24): in RT demo mode, bulk invite → "send email" produced
"2 sent. 1 email didn't look right. Check and try that again." — an
attempted-send flow with a validation error. User ruling, verbatim:
"it should just say this is demo, not sent." Demo mode = NO real
sends and NO send-shaped errors; an explicit demo notice instead.

## Repro (as reported)

Demo mode → bulk invite → click send email → "2 sent. 1 email didn't
look right. Check and try that again." (2 appeared sent, 1 failed
validation.)

## Expected (user-ruled)

Demo mode → bulk invite → send email → a clear demo notice, e.g.
"Demo mode — invites are not sent." NO send attempt, NO validation
errors, NO fake partial-success counters. Non-demo behavior
unchanged (real sends + validation stay exactly as-is).

## Rules (hard)

1. The guard lives at the SEND path (service/action level), not just
   the button label — a demo-mode caller hitting the endpoint/service
   directly must get the same demo notice (defense in depth).
2. Find how demo mode is flagged in this codebase (env/config/seed
   marker) and use THE canonical check — don't invent a second demo
   detector. Note the mechanism in the PR body.
3. The validation-error path for real mode is untouched (real users
   still get "1 email didn't look right" with per-recipient detail —
   if the current message lacks WHICH email failed, that's a separate
   improvement; flag it, don't fix it here).
4. Tests: demo-mode bulk-invite send → demo notice, zero send
   attempts (assert the mailer is never called); real-mode path
   unchanged (existing tests green).

## Acceptance

- Demo: notice shown, no sends, no validation errors.
- Real mode: unchanged behavior + existing suite green.
- PR body shows the demo-mode detection mechanism + both paths.
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-demo-bulk-invite-guard
- base: develop (RT convention; main if no develop)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- note: dublin-rents-q2-2026 (p349) is in flight on the same repo —
  different surface (email/invite vs data posts); parallel-safe, Silas
  coordinates merge order
