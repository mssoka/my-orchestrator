# Briefing: righttenantry-guarantor-autofill-fix

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`guarantor-autofill-fix` worktree, branch `guarantor-autofill-fix`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders). Review pass: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes.
- **Model policy:** `deepseek-v4-flash` (kimi walled until 08-08T21:57Z).
- **Perkins:** `pr_review: true`.

## Mission (user-reported bug)

The Guarantor step's fields **don't accept browser autofill** — the browser suggests entries (name, phone, email) but clicking them does NOT populate the fields. All other form sections accept autofill normally. The guarantor fields are the exception.

**Likely cause:** the guarantor fields may be missing standard `autocomplete` attributes (e.g., `autocomplete="given-name"`, `autocomplete="tel"`, `autocomplete="email"`), OR the fields may have a non-standard input type / JS event handler that intercepts and swallows the autofill event, OR the conditional-show/hide mechanism (the guarantor section expands/collapses based on the checkbox) may interfere with the browser's autofill targeting.

**Investigate:** compare the guarantor section's field HTML (`server/src/application/form_sections/guarantor.gleam`) against a working section (e.g., `references.gleam` or `work_income.gleam`) — what's different about the input attributes, event handlers, or the show/hide mechanism?

## Requirements

1. **Root cause:** identify WHY the guarantor fields reject autofill while sibling sections accept it. Common culprits: missing `autocomplete` attributes, non-standard `<input type>`, JS that clears fields on focus/change, the conditional expand/collapse resetting field state.
2. **Fix:** guarantor fields accept browser autofill like every other section. Add standard `autocomplete` attributes where missing (name → `given-name`/`family-name`, phone → `tel`, email → `email`, income → `transaction-amount`, employer/business name → `organization`).
3. **Don't break the conditional logic:** the guarantor fields still show/hide based on the checkbox / required-cohort policy (the #577 fix). Autofill must work WITHIN the expanded state.
4. **Audit:** check ALL form sections for missing `autocomplete` attributes while you're there — if the guarantor is missing them, siblings might be too. Fix any found.

## Acceptance

- Guarantor fields accept browser autofill (real-browser verification: Chromium autofill popup populates the fields on click).
- All form sections have appropriate `autocomplete` attributes (grep proof).
- Conditional show/hide unregressed (guarantor hidden when not required; visible when required).
- `make test` + `make test-integration` green.
- Commit on `guarantor-autofill-fix`, push, `gh pr create --base develop` titled "fix: guarantor fields accept browser autofill + autocomplete attribute audit" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap. Local Docker DB only.

## Self-report

- `bin/ledger set righttenantry-guarantor-autofill-fix working` at start
- `bin/ledger set righttenantry-guarantor-autofill-fix in-review "PR <url>"` when PR opens
- `herdr notification show "righttenantry-guarantor-autofill-fix" --body "<one-line>"` on finish
- Final message: root cause, files changed, PR URL, autofill evidence, audit findings.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-guarantor-autofill-fix
- base: develop
- pr_review: true
