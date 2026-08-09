# Briefing: righttenantry-draft-grace-period

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`draft-grace-period` worktree, branch `draft-grace-period`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission (user ruling 2026-08-03: "I like the grace")

Close the draft-loss gap between vacancy close and landlord extension. Today `delete_expired_application_drafts` (retention job) hard-deletes drafts the moment a vacancy is `closed` OR `closes_at` is past — so a landlord who buys the pay-to-extend SKU *after* the sweep finds every applicant's draft destroyed (tokens dead, journey gone), even though the webhook restores the vacancy + applications.

**The change:** drafts get a **7-day grace** after vacancy close before hard deletion. Within grace, an extension (webhook reopens the vacancy, restores auto-closed applications) resurrects the full save-resume journey — token works, draft intact. After grace, deletion proceeds exactly as today.

1. `server/src/retention/sql/delete_expired_application_drafts.sql` — gate deletion on the close being **older than 7 days** (both branches: manual `status='closed'` and time-based `closes_at` past). Define "closed at" carefully for the manual branch (no closes_at in the past necessarily — check what marks the close moment; `updated_at` on the vacancy row is fragile, look for a closed_at/closed-via timestamp or the audit trail; if none exists, use `GREATEST(closes_at, now())`-style derivation and DOCUMENT the choice in the PR).
2. Grace applies regardless of `closed_via` (auto vs manual) — kinder and simpler.
3. Copy check: any user-facing "your draft is kept until the vacancy closes" line stays TRUE during grace (the draft exists but the form/resume renders the closed page while closed — that's already the behavior; after extension it works again). Fix copy only if a sentence becomes false.
4. Spec/arch note: the F3 spec said "expires at vacancy close" — this amends it to "expires 7 days after vacancy close (extension grace)". Note the amendment in the PR body.

## Acceptance

- Integration tests (docker test DB): draft on a vacancy closed 3 days ago SURVIVES the sweep; closed 8 days ago is DELETED; vacancy closed-then-extended within grace → resume via token → draft intact → submit works.
- All suites green: `make test`, `make test-integration`, scenario suite unbroken.
- Commit on `draft-grace-period`, push, `gh pr create --base develop` titled "feat: 7-day draft grace after vacancy close (extension resurrects save-resume)" with **Decisions & rationale** incl. the close-moment derivation choice. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only (`make test-db-up`).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-draft-grace-period working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-draft-grace-period in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-draft-grace-period <url>`
- On blocked/finished: `herdr notification show "righttenantry-draft-grace-period" --body "<one-line>"`
- Final message: summary, files changed, PR URL, grace-window test evidence, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-draft-grace-period
- base: develop
- pr_review: true
