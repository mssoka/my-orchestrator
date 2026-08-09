# Briefing: righttenantry-form-nojs-submit-fix

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-nojs-submit-fix` worktree, branch `form-nojs-submit-fix`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission

Fix the **no-JS submit blocker** found by the #564 post-merge audit (user ruled: `fix it`).

**The bug:** the no-JS fallback renders the form's only submit button **DISABLED unconditionally** (`review_consent.gleam:117` — since PR #97, predates this wave). A real user with JavaScript disabled cannot submit an application at all. The spec's progressive-enhancement requirement is explicit: **the SSR no-JS fallback must submit.**

**Context:** develop's form is now a stepper (JS) with the single long form as the no-JS fallback. The attestation radio (RC1.2) already posts without JS per its ACs. The likely defect pattern: SSR renders the button `disabled` and JS enables it — invert correctly: SSR must render an ENABLED button (no-JS works out of the box); if JS needs it disabled for its own flow, JS may disable it on init (progressive enhancement, not progressive requirement).

**Also fold in (same audit, mechanical):** `generate-fixtures.sh` is missing `mkdir -p` — it re-breaks preflight at the new `.pi/skills` path on every existing checkout (post-migration debris from #564). One-line fix.

## Acceptance

- **Real-browser evidence, JS DISABLED** (Chromium with JavaScript disabled): the long form renders with an ENABLED submit; a full valid submission (incl. attestation radio choice, per RC1.2's no-JS AC) posts and persists; validation errors re-render server-side correctly.
- **Real-browser evidence, JS ENABLED:** the stepper flow is unregressed (step gating + final submit still work; the JS may own disabling where its flow requires).
- `generate-fixtures.sh` runs clean at the `.pi/skills` path on a fresh checkout simulation.
- All suites green: `make test`, `make test-integration` (docker test DB), the `.pi/skills/form-bug-hunt` scenario suite unbroken.
- Commit on `form-nojs-submit-fix`, push, `gh pr create --base develop` titled "fix: no-JS fallback can actually submit (+ fixtures mkdir -p)" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only (`make test-db-up`; `dot_env` trap per the stepper shard; timing trap — sleeps before scripted submits).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-form-nojs-submit-fix working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-form-nojs-submit-fix in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-form-nojs-submit-fix <url>`
- On blocked/finished: `herdr notification show "righttenantry-form-nojs-submit-fix" --body "<one-line>"`
- Final message: summary, files changed, PR URL, JS-disabled + JS-enabled browser evidence, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-form-nojs-submit-fix
- base: develop
- pr_review: true
