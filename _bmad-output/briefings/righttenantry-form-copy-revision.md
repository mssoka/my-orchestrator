# Briefing: righttenantry-form-copy-revision

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-copy-revision` worktree, branch `form-copy-revision`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (orchestration overrides per standing orders). Review pass: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes.
- **Model policy:** `deepseek-v4-flash` (kimi walled).
- **Perkins:** `pr_review: true`.

## Mission (user-ruled exact copy + global em-dash ban)

Two changes, both user-specified verbatim:

### 1. Replace the "Before you start" checklist items with this EXACT copy (em-dashes removed)

The user provided the final copy. Use it VERBATIM on ALL checklist surfaces (form-header prep block, invite email, daft auto-reply):

1. `A written reference from your current or previous landlord (a photo, scan or PDF is fine). First time renting? A character reference from someone who knows you works instead.`
2. `A written reference from your employer if you're working, or from a client, accountant, or business contact if you're self-employed.`
3. `A guarantor (someone 18+ with a steady, verifiable income who can back your application) if you haven't rented before, or you're a student or unemployed.`
4. `A name, phone number and email address for each referee.`
5. `About 15 minutes, once you have the documents.`
6. `Complete applications are reviewed first. You don't have to finish in one visit. Once your email is in, your answers save as you go, and you can email yourself a link to pick up where you left off.`

### 2. Student trigger note — replace with this EXACT copy

`As a student, you'll need a guarantor: someone 18+ with a steady, verifiable income who agrees to back you. We'll ask for their details in the Guarantor step.`

Apply the same shape for the other trigger notes (never-rented, unemployed) — no em-dashes.

### 3. GLOBAL: no em-dashes anywhere in form/email/copy

**Zero em-dashes (`—`, `\u2014`, `&mdash;`, `&mdash;`) in any user-facing string.** Grep ALL form copy, email templates, trigger notes, confirmation pages, error messages — replace every em-dash with a comma, colon, parenthesis, or sentence break as appropriate to the context. The user's stance is absolute: **no em-dashes.**

`rg "\u2014|&mdash;|--"` over `server/src/notification/`, `server/src/application/form_copy.gleam`, `server/src/application/form_sections/`, `server/src/application/form_pages.gleam` — clean every hit in a USER-FACING string (code comments can keep their dashes; only user-visible copy must be em-dash-free).

## Acceptance

- All 6 checklist items + the student trigger note replaced verbatim on all surfaces.
- `rg "\u2014|&mdash;"` over user-facing copy = ZERO hits (or justified in the PR).
- Copy assertions updated; `make test` green.
- Commit on `form-copy-revision`, push, `gh pr create --base develop` titled "fix: before-you-start copy revision + global em-dash ban" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap. Local Docker DB only.

## Self-report

- `bin/ledger set righttenantry-form-copy-revision working` at start
- `bin/ledger set righttenantry-form-copy-revision in-review "PR <url>"` when PR opens
- `herdr notification show "righttenantry-form-copy-revision" --body "<one-line>"` on finish
- Final message: summary, files changed, PR URL, em-dash grep proof, open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-form-copy-revision
- base: develop
- pr_review: true
