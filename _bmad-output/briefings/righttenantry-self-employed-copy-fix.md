# Briefing: righttenantry-self-employed-copy-fix

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`self-employed-copy-fix` worktree, branch `self-employed-copy-fix`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission (user-reported, screenshot-verified)

Fix the self-employed coherence bug — two parts, user-ruled 2026-08-04:

1. **Checklist copy.** Current: *"A written reference from your employer, if you're employed or self-employed."* — incoherent for sole traders (a reference from themselves?). Replace with the user's ruling: **"A written reference from your employer — or from a client, accountant, or business contact if you're self-employed."** Apply on EVERY checklist surface: invite email (`server/src/notification/email_client.gleam` ~:261), the daft auto-reply, and the form-header prep block — grep for "written reference from your employer" and "employer, if you" to catch all instances; the W1a doctrine was one checklist everywhere, keep it uniform.
2. **Field label.** Work & Income's `Employer name *` (required when status = employed OR self-employed, `common.gleam:40`) → relabel to **"Employer / business name"** (stays required for both: employed → employer; self-employed → trading name). Check for sibling labels elsewhere in the flow (review/confirmation page, landlord-facing application detail) and keep them consistent.

**Out of scope:** the refcheck referee-slot design (employer-ref question set) — separate track, do not touch. Any scoring reads of the employer field: verify the label change doesn't alter the field NAME/id the scorer keys on (label-only change; if the scorer surfaces the label anywhere landlord-facing, note it in the PR).

## Acceptance

- Self-employed applicant sees coherent copy on all checklist surfaces + the relabeled field; employed path unchanged.
- Copy assertions updated (`rg "written reference from your employer"` clean or justified); tests green: `make test`, `make test-integration` (docker test DB).
- Real-browser screenshot evidence: Work & Income step with Self-employed selected (new label) + one checklist email render.
- Commit on `self-employed-copy-fix`, push, `gh pr create --base develop` titled "fix: self-employed coherence — referee copy + employer/business label" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-self-employed-copy-fix working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-self-employed-copy-fix in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-self-employed-copy-fix <url>`
- On blocked/finished: `herdr notification show "righttenantry-self-employed-copy-fix" --body "<one-line>"`
- Final message: summary, files changed, PR URL, surfaces covered, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-self-employed-copy-fix
- base: develop
- pr_review: true
