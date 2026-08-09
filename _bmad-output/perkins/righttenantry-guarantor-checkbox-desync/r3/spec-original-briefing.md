# Briefing: righttenantry-guarantor-checkbox-desync

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`guarantor-checkbox-desync` worktree, branch `guarantor-checkbox-desync`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start (form-stepper-f1, form-save-resume-f3, form-resume-progress-fix shards are directly relevant); badge-out shard per standing orders.
- **Perkins:** `pr_review: true`.

## Mission (user-reported bug, screenshot-verified sequence)

Fix the **guarantor checkbox state desync**. The user's sequence on the upgraded form:

1. Fill the form (never rented before checked), reach the Guarantor step, do NOT check "I have a guarantor".
2. Submit → **6 guarantor validation errors** (name/relationship/phone/email/income/employer) — the server believes a guarantor was declared.
3. Error re-render dumps them at the Guarantor step with the checkbox **CHECKED FOR THEM** and all six fields expanded with per-field errors.

**Suspected mechanism (verify, don't assume):** checkbox conditional state desyncs between the visible DOM and the draft/aggregation payload — an earlier check persisted `guarantor=true` via the debounced save; unchecking visually never cleared the persisted state; the POST aggregates the stale flag; server validation follows the flag; re-render paints the posted (stale) state. Same state-derivation family as the resume green-lies.

## Requirements

1. **Root fix:** conditional checkbox state round-trips like every other field — unchecking clears persisted/aggregated state immediately; restore re-derives the visible checkbox from the draft; server-side conditional-required validation keys off the ACTUAL posted checkbox (unchecked + empty guarantor fields = valid, no errors).
2. **Class hunt:** every conditional checkbox/toggle in the form (guarantor, pets/smoke variants if conditional, co-applicant toggles, "add another income source", address-cluster toggle) gets the same round-trip audit — fix any sibling desyncs found, list them in the PR.
3. **NEW bug-hunt scenario (user order):** add a permanent scenario to `.pi/skills/form-bug-hunt`'s suite covering this class: conditional checkbox check → uncheck → submit → assert NO conditional-required errors and the checkbox reflects the user's actual last action on any re-render; plus a check → fill-partial → submit variant (must error correctly and KEEP the checked state). Name it clearly (e.g. `conditional-checkbox-desync`).
4. Error re-render fidelity: when guarantor errors DO legitimately fire (checked + empty fields), the re-render keeps the checkbox checked (that part of the user's evidence was correct behavior — preserve it).

## Acceptance

- The user's exact sequence replayed in a **real browser** (Chromium, mobile viewport): never-rented + check-then-uncheck guarantor + submit → **no guarantor errors**, submits clean; checkbox never self-marks.
- The inverse: checked + empty fields → correct 6 errors, re-render keeps checked state (regression-preserved).
- New scenario passes in the form-bug-hunt suite; all suites green: `make test`, `make test-integration` (docker test DB).
- Commit on `guarantor-checkbox-desync`, push, `gh pr create --base develop` titled "fix: conditional-checkbox state desync (guarantor self-marking) + bug-hunt scenario" with **Decisions & rationale** + the class-audit list. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits). Local Docker DB only (`make test-db-up`; timing trap — sleeps before scripted submits).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-guarantor-checkbox-desync working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-guarantor-checkbox-desync in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-guarantor-checkbox-desync <url>`
- On blocked/finished: `herdr notification show "righttenantry-guarantor-checkbox-desync" --body "<one-line>"`
- Final message: summary, files changed, PR URL, class-audit findings, scenario name, browser evidence, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-guarantor-checkbox-desync
- base: develop
- pr_review: true
