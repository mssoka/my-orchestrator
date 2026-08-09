# Briefing: righttenantry-form-save-resume-f3

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-save-resume-f3` worktree, branch `form-save-resume-f3`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true` — automated review rounds will fire on your PR; address verdicts per the relay messages.

## Mission

Ship **follow-up C** of the ruled application-form completion plan: **F3 save-and-resume**. The spec of record:

`_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md` — read the Generated Solutions table (F3 row), Solution Analysis, Recommended Solution (Wave 1 build pack), Risk Mitigation (draft data-protection row especially), and the E2 reminder row (your continue-link CTA completes it).

Context: W0+1a shipped (PR #556); follow-up B (stepper, F1) ships ahead of you — its PR adds section-at-a-time navigation; your "save on section change" should hook the seam its minion documented (check its PR description + merge state of `form-stepper-f1` before designing the save trigger; if it is not merged yet, build against the current 8-section DOM and note the integration point).

## Requirements

1. **Draft persistence** — email-keyed draft table; save on section change (debounced; no per-keystroke writes). Migration is allowed on the **local/dev DB only** — never prod/staging.
2. **Magic continue link** — "Email me a link to continue" on the form; tokenized link via the existing Resend email path; restores draft state into the SSR form.
3. **Expiry + erasure** — drafts expire at vacancy close; an erasure path exists (GDPR surface per the spec's risk table).
4. **No documents in drafts** — files are only ever transmitted at the final POST; drafts carry field values only.
5. **Complete the E2 seam** — reminder stage-2 CTA becomes the continue-link (see Seams).

## Seams (left by the W0 minion, PR #556 — use, don't rebuild)

- Swap the one-visit line at the `F3-SEAM` comment in `form_view.gleam` (`view_prep_block`) — the "you can save and continue later" promise becomes true with your ship; make the copy say so.
- Reminder stage-2 CTA is a single `application_url` param in `email_client.build_reminder_stage2_html` — point it at your continue-link.
- Stable anon id + `application_form_section_*` events already exist — resume-vs-abandon reads should need no new plumbing; add only what the spec's Success Metrics require (drafts created / resumed / resume→submit).

## Acceptance

- Full journey works: start form → leave → magic link → state restored → submit; draft expiry + erasure verified; no file data in the draft table (schema-verifiable); reminder stage-2 carries the continue-link.
- `make test` and `make test-integration` (docker test DB) green; new behavior covered (draft round-trip, token auth on the link, expiry sweep, erasure).
- Commit on `form-save-resume-f3`, push, `gh pr create --base develop` titled "feat: application save-and-resume (F3) + reminder continue-link" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Do NOT run migrations against anything but a local/dev DB; do NOT touch prod.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-form-save-resume-f3 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-form-save-resume-f3 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-form-save-resume-f3 <url>`
- On blocked/finished: `herdr notification show "righttenantry-form-save-resume-f3" --body "<one-line>"`
- Final message: summary, files changed, PR URL, migration notes, expiry/erasure evidence, E2 seam completion, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-form-save-resume-f3
- base: develop
- pr_review: true
