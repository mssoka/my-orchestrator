# Briefing: righttenantry-self-employed-sweep

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`self-employed-sweep` worktree, branch `self-employed-sweep`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission (user-approved bundle, 2026-08-04 — completes the self-employed coherence fix started in #573)

Four items, all user-ruled:

1. **Referee-slot path (Documents step).** The required upload slot currently reads *"Employer reference for <name>"* with helper *"a letter or email from your manager or HR confirming you work there — on letterhead if you can get it."* Same sole-trader incoherence on a REQUIRED path. Relabel to **"Employer / business reference"** and amend the helper to include the self-employed path: *"— or from a client, accountant, or business contact if you're self-employed."* (Match the tone of the ruling sentence; find every instance of the slot label/helper incl. per-co-applicant variants.)
2. **Audit PDF unify.** The audit PDF's data line now says *'Employer / business name'* but its AI-evidence section still prints *'Employer name:'* — unify to **'Employer / business name:'** so the landlord sees one field, one label.
3. **Landlord checklist sweep.** `tenant-vetting-checklist.typ` (landlord-facing) still says *'an employer'* — amend to cover the self-employed path (same doctrine: employer, or client/accountant/business contact for the self-employed).
4. **Invite checklist sentence — scoping tweak (user-approved amendment).** The sentence shipped in #573 (*"A written reference from your employer — or from a client, accountant, or business contact if you're self-employed."*) drops the working-scoping so students/unemployed may read it as mandatory. Amend to: **"A written reference from your employer, if you're working — or from a client, accountant, or business contact if you're self-employed."** Apply on ALL checklist surfaces (invite email, daft auto-reply, form-header prep block) — keep uniform per the W1a doctrine.

**Out of scope:** the refcheck referee QUESTION SETS (employer-ref slot's structured questions) — the v1 refcheck design; do not touch.

## Acceptance

- All four items land; `rg -i "manager or HR|an employer\b"` over checklist/vetting surfaces clean or justified; audit PDF prints one label end-to-end.
- Copy assertions updated; tests green: `make test`, `make test-integration` (docker test DB).
- Real-browser screenshot evidence: Documents step slot for a self-employed applicant + one checklist render with the scoped sentence.
- Commit on `self-employed-sweep`, push, `gh pr create --base develop` titled "fix: self-employed coherence sweep — referee slot, audit PDF, vetting checklist, scoped invite line" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-self-employed-sweep working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-self-employed-sweep in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-self-employed-sweep <url>`
- On blocked/finished: `herdr notification show "righttenantry-self-employed-sweep" --body "<one-line>"`
- Final message: summary, files changed, PR URL, surfaces covered, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-self-employed-sweep
- base: develop
- pr_review: true
