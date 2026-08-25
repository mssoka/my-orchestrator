# Briefing — righttenantry-refcheck-613-615 (issues #613 + #615 — bug-hunt UX fallout: stepper label + toast layering)

- **Job id:** `righttenantry-refcheck-613-615`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-613-615`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (user-facing UX + consent-compliance surface; consistent
  with the 612 precedent).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr righttenantry-refcheck-613-615 <url>` yourself — the pr field does NOT
  self-populate from a status note.
- **Base:** `develop` @ ba605ba. Sibling PR #616 (`refcheck-611-panel-persist`) may
  merge while you work — disjoint areas; rebase onto origin/develop if it lands first.
- **CI NOTE:** GitHub Actions billing may be blocked at the account level — if your
  PR's CI is red/not-started, that is NOT a code failure. Run the FULL local suite
  green (`make test-all`) before opening the PR; Perkins verifies locally.

## Mission — fix issues #613 and #615 in ONE PR (read both issues in full first — the issues ARE the spec)

### Part 1 — #613: stepper 'Viewed' label is ambiguous (priority: low)

**The bug:** the application status stepper shows `Submitted → Reviewing → Shortlisted
→ Viewed → Approved`, but bare "Viewed" reads as "application opened" — when it
actually means "the viewing with the applicant was carried out" (RC2.2 amendment A5).
The transition INTO `viewed` is the reference-check trigger (it mints the queued
reference calls), so a landlord misreading the label either never marks it or marks
it accidentally.

**The fix:**
1. Relabel the stepper status so it unambiguously conveys the viewing was carried
   out — candidate wording "Viewing held" (you may refine; pick ONE term and use it
   everywhere the status is user-facing). Add/extend a tooltip or aria hint that says
   marking it triggers the reference checks, if the stepper supports hints cheaply.
2. **Scope guard:** LABEL AND USER-FACING COPY ONLY. Do NOT touch the DB enum
   (`20260808120000_add_viewed_application_status.sql` stays `viewed`), do NOT touch
   the refcheck trigger logic, do NOT touch `vacancy.viewed_at` (unrelated ad-view
   counter). Grep for other user-facing renderings of the status word so no surface
   is left half-renamed; internal/log/migration identifiers keep `viewed`.

### Part 2 — #615: toasts hidden behind cookie-consent banner (priority: medium)

**The bug:** the consent banner (`server/priv/static/consent.js`:393 —
`position:fixed; bottom:16px; z-index:2147483000`) renders above the toast stack
(`client/src/components/toast.gleam` — `fixed bottom-4 right-4 z-50`). While the
banner is up, every toast fires and is DOM-present but visually hidden — including
the refcheck "Attempt log copied" confirmation (OQ-5).

**The fix (constraint-driven — you pick the mechanism, document the choice in the PR):**
1. Toasts must be VISIBLE during the consent window. Options include (a) raising the
   toast layer's stacking above the banner, or (b) repositioning toasts out of the
   banner's area (e.g. top-right). 
2. **Hard constraint:** the consent banner must remain visible AND clickable at all
   times — do not cover it with toasts, do not dismiss/move it. Consent UX is
   compliance-adjacent; if your approach risks obscuring the banner's interactive
   area even transiently, choose the other approach.
3. Re-run the bug-hunt evidence style: a DOM+screenshot-level check that the
   `reference_checks/panel-export` "Attempt log copied" toast is visible while the
   consent banner is up (playwright/evidence pattern used by the bug-hunt is fine).

**Acceptance:**

1. One PR, `Fixes #613` + `Fixes #615` in the body; PR body names the chosen toast
   approach + rationale in two lines.
2. Stepper shows the new unambiguous label everywhere the status renders
   user-facing; copy tests pin the new wording; grep proves no stray user-facing
   "Viewed" status label remains.
3. Toast visibility during the consent window proven (test or evidence artifact);
   banner still visible + clickable (test or evidence artifact).
4. Full `make test-all` green locally; Perkins verifies locally (CI billing may be
   blocked — not your failure).

**Scope guard:** the two fixes above only. No other copy sweep, no stepper-order
changes, no consent-banner logic changes beyond what layering requires, no #611
input-path work (that's PR #616's).

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-613-615
base: develop
model: deepseek/deepseek-v4-flash
github_issue: 613
pr_review: 1
```
