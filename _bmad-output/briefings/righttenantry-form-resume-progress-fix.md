# Briefing: righttenantry-form-resume-progress-fix

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-resume-progress-fix` worktree, branch `form-resume-progress-fix`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start (form-stepper-f1 + form-save-resume-f3 shards are directly relevant); badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission (user-reported bug, verbatim evidence)

Fix the stepper's **green progress indicator lying after a save-resume restore**. The user replayed this sequence on the upgraded form (screenshots reviewed by Gru):

1. Resume via continue-link → dropped at Step 3, "Welcome back" banner — Steps 1–2 show **white** even though their data was restored from the draft.
2. Back to Step 2 (data present) → **Step 3 turned green while completely empty** (every field blank).
3. Step 1 (data present: name/email/phone) showed **white**.

## Diagnosis (verify, don't assume)

The completed-set is **visit-based, not completeness-based**: seeding nothing on restore (white lies), and marking the current step complete unconditionally on navigation-leave (green lies). Root fix: **derive per-step completeness from actual field content** —

1. **On restore:** compute each step's completeness from the restored draft values (required fields filled) and seed the green state accordingly.
2. **On leave:** mark green only if the step's required fields are actually filled (mirror the same completeness rule the step-gating validation uses — reuse, don't duplicate).
3. Empty-visit-and-leave must NEVER turn a step green.

Likely surfaces: `server/priv/static/` stepper/draft JS + the resume seeding path; tests in `scripts/js-tests/form_stepper.test.js`, `form_draft_wiring.test.js`, `form_draft.test.js`.

## Acceptance

- The user's exact 4-step sequence replayed in a **real browser** (Chromium, mobile viewport): resume → restored-complete steps green ON ARRIVAL; visit-and-leave an empty step → stays white; filled-then-left → green.
- js-tests for: restore-seeding (complete vs partial vs empty sections), leave-gating (empty step cannot go green).
- All suites green: `make test`, `make test-integration` (docker test DB), the e2e scenario suite (`.pi/skills/form-bug-hunt`) unbroken.
- Commit on `form-resume-progress-fix`, push, `gh pr create --base develop` titled "fix: stepper progress reflects restored-draft completeness (resume green-lies)" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only (`make test-db-up`; `dot_env` trap per the stepper shard).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-form-resume-progress-fix working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-form-resume-progress-fix in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-form-resume-progress-fix <url>`
- On blocked/finished: `herdr notification show "righttenantry-form-resume-progress-fix" --body "<one-line>"`
- Final message: summary, files changed, PR URL, browser evidence of the 4-step replay, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-form-resume-progress-fix
- base: develop
- pr_review: true
