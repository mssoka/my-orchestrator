# Briefing — righttenantry-refcheck-verification-rerun (verification re-run over reference_checks)

- **Job id:** `righttenantry-refcheck-verification-rerun`
- **Repo:** RightTenantry · **Base:** `develop` · **Slug:** `refcheck-verification-rerun`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (investigate + run workflow — a hands-on
  verification session, NOT feature development).
- **Perkins:** `pr_review: 0` — **no PR expected.** This job ships a verification report +
  running log, not a code change.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` AND the original hunt's
  shard `/Users/moses/code/_bmad-output/field-notes/righttenantry-refcheck-local-test.md`
  at start (its three lessons are LOAD-BEARING for this run); badge-out your own
  field-notes shard per standing orders.
- **NO-PR COMPLETION SIGNAL (mandatory):** no watcher tracks a no-PR job. When you are
  done, you MUST run `herdr notification show "<job-id>" --body "<one-line result
  summary>"` — that is the ONLY way the bosses learn you finished. Then
  `ledger set <job-id> done`.
- **Base:** `develop` @ **ce999eb** — the FULL refcheck fix line is now merged:
  #610 (607 follow-up), #612 (em-dash exemptions removed), **#616** (#611 stale-save
  fix), **#618** (#613 "Viewing held" label + #615 toast layering). This re-run
  VERIFIES those fixes hold; it does not re-hunt from scratch.

## Mission — verify the #611/#612/#613/#615 fixes hold, end-to-end, over the reference_checks scenarios

This is the **RESPAWN** of `righttenantry-refcheck-local-test` (user ruling,
2026-08-14): the original hunt filed #611/#612/#613/#615; all four are now merged.
Re-run the reference_checks verification against the FIXED develop and prove each fix
holds. Deliverable: a verification report (what was re-verified, PASS/FAIL per fix
area, evidence where the fix is visual) + running log. NO PR.

**Re-verify each fix area (the issue IS the spec — read #611/#612/#613/#615):**

1. **#611 — edit-trio keystrokes (stale-save fix, PR #616):** the edit-trio inputs
   (correct + substitute) are keyed by `reference_call_id` (stable), NOT ref slot.
   Scenario: type edits in a row → reorder/refetch the list → Save persists the NEW
   contact, never the stale one. `panel-correct` + `panel-substitute` scenarios must
   PASS. (Perkins-verified at the sha — this run confirms it live.)
2. **#612 — em-dash exemptions removed:** the `no_em_dash_test` scan is clean; all
   spec-verbatim strings are re-composed dash-free. Grep the user-facing copy.
3. **#613 — "Viewing held" stepper label:** the `viewed` status renders the new
   unambiguous label on EVERY user-facing surface (stepper stop, backward-confirm
   modal, audit trail, shared pill, detail-page pill); no stray user-facing "Viewed"
   label survives. Marking a viewing still triggers the reference calls.
4. **#615 — toast visibility during the consent window:** the "Attempt log copied"
   toast is VISIBLE while the consent banner is up (the toast stack moved top-right,
   one z-step above the banner); the consent banner stays visible + clickable.
   Evidence style: DOM geometry + screenshot (the original evidence artifact is in
   `_bmad-output/implementation-artifacts/refcheck-613-615-evidence/` — re-confirm,
   don't re-litigate the 320×480 corner trade-off, which was user-approved).

**Test-infra re-application (the original hunt's scenario-suite fixes are NOT in git —
re-apply them):** the `reference_checks` scenario suite lives under
`.pi/skills/bug-hunt/scenarios/reference_checks/` and is UNTRACKED (the original
minion authored it in its worktree, which was swept). Re-create it from
`.pi/skills/bug-hunt/SKILL.md` + `guides/scenario-format.md`, applying the field-notes
lessons:
- **Stacked-forms trap:** the referee form renders ALL question forms stacked in the
  DOM (one visible) — EVERY click/fill must be scoped to
  `[data-question][data-current="true"]`; an unscoped `reference-continue` click
  silently re-submits the FIRST (identity) form. Treat "page didn't advance" as a
  selector bug before a server bug.
- **Timing gates:** refcheck + apply POSTs are timing-gated (floor 500ms/2s,
  stale-cap) — sleep ≥2–3s AFTER the page renders BEFORE submitting; a rejected
  submission leaves `_form_loaded_at` stale, so reload fresh instead of retrying.
- **Sandbox:** `:4000` may be sibling-owned — run `:4100` via a gitignored
  `server/.env` copy, blanking Resend/Twilio/AI; `seed-refcheck-fixture.py` must
  resolve applications by the submit's OWN unique email; use `--no-sweep` fixtures
  (the global sweep claims all due rows).
- The original hunt fixed `referee-form-complete.yaml` (scoped selectors) +
  `panel-renders` + `panel-export` scenarios and re-ran them PASS — re-derive the
  same scoping so the suite passes on the fixed app.

**Wrap:** verification report — per fix area: exercised, result (PASS/FAIL), evidence
(screenshots where visual). If a merged fix REGRESSED or a new bug surfaces, file a
GitHub issue (righttenant label) + flag it loudly in your final message — the fixes
are fresh and the bosses will want to know immediately.

**Scope guard:** verification + local environment setup ONLY. No production changes,
no feature edits, no commits to `develop`. If you hit a real bug, log it and flag —
the bosses decide.

## Dispatch parameters

```
repo: RightTenantry
repo_root: /Users/moses/code/RightTenantry
slug: refcheck-verification-rerun
base: develop
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 0
```
