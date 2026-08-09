# Perkins briefing — round 1: righttenantry-refcheck-rc2-3

- **PR:** https://github.com/solarity-services/RightTenantry/pull/591 (targets `develop`)
- **Reviewed sha:** `109ec5db89858af69c778d89b9b2dd6ef1117b5b` (head `refcheck-rc2-3`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc2-3-r1` — pinned at exactly the reviewed sha.
- **Spec:** the job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc2-3.md` + the story spec. No GitHub issue.
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

Story RC2.3: trigger reference-check creation on `viewed` + manual start/skip APIs. The implementing minion reports:
- **FR-RC3 (auto-create on viewed):** a post-commit sibling to `maybe_send_shortlist_notification` fires on the transition INTO `viewed` and auto-creates queued `reference_call` rows — landlord-ref OR character-ref (when `never_rented_before`) + employer-ref, skipping no-contact slots, suppressed when the applicant declined attestation (`reference_contact_choice = 'declined'`), allowed for pre-v1. Nothing is sent (the sweep owns that, RC3.5). Post-commit fail-open (matches the shortlist-notification neighbour).
- **FR-RC4 (manual control + A6):** three authenticated landlord API arms — start (whole-app), `:slot/skip`, `:slot/re-enable`. Skip handles both queued→skipped and create-skipped-before-trigger (reserves the slot against the auto-trigger); re-enable re-arms `next_attempt_at = now()`.
- **Idempotency:** `INSERT ... ON CONFLICT DO NOTHING` against the live-slot partial unique index — double-clicks, re-marks, and manual-after-auto are all silent no-ops.
- **Key decision:** NO migration — the briefing's `ADD VALUE 'skipped'` step was stale; RC2.1 already added it and `event_type` is TEXT. Verified on disk first.
- Tests: `make format/test/build` green; 1222 unit + 410 integration (incl. 13 new DB-level AC pins: slot selection, no-contact skip, declined suppression, pre-v1, idempotency, skip/re-enable transitions, pre-excluded-slot respect, lifecycle audits).

## ⚠️ CRITICAL lens-guard (read before any lens — prevents false positives)

Several decisions are deliberate + briefing/architecture-driven and must NOT be flagged as defects:
- **Do NOT flag "no migration."** The `skipped` enum was already added by RC2.1; the minion correctly verified on disk before skipping the migration (ground-truth-first — the briefing was stale). A redundant `ADD VALUE 'skipped'` would FAIL (value already exists). The NO-migration is correct.
- **Do NOT flag the post-commit fail-open trigger design.** It matches the established shortlist-notification neighbour pattern (fire-and-forget post-commit; manual-start API is the recoverable fallback). This is the briefing-mandated design.
- **Do NOT flag the idempotency (`INSERT ... ON CONFLICT DO NOTHING`) as "silently dropping."** It's deliberate — double-clicks, re-marks, and manual-after-auto SHOULD be no-ops (the slot unique index + the conflict clause enforce it). This is the correct semantics.
- **Do NOT flag "nothing is sent (no SMS/email in this story)."** Correct — RC2.3 is the TRIGGER + manual-control story; the actual sending is RC3.5 (the sweep engine). RC2.3 creates queued rows; it doesn't send.

### Legitimate findings here would be
- The auto-create does NOT fire on the viewed transition (the hook is missing/wrong/in the wrong place), OR fires on the WRONG transition.
- A **slot-selection bug**: wrong slots created (e.g., creates employer-ref when it shouldn't, or misses the landlord-ref when never_rented_before should use character-ref).
- A **suppression gap**: auto-creates rows when `reference_contact_choice = 'declined'` (the hard rule).
- A **no-contact skip gap**: creates a row for a slot with no contact data.
- The manual start/skip/re-enable APIs are **NOT owner-checked** (cross-tenant access), OR the transitions are wrong (e.g., skip doesn't reserve the slot against the auto-trigger; re-enable doesn't re-arm).
- An **idempotency gap**: double-clicks or re-marks create duplicate rows (the INSERT ON CONFLICT isn't actually enforced).
- A regression to existing application/reference flows.
- **Em-dashes** in user-facing copy (RT global ban, CI-guarded).
- Broken Gleam/JS parse, a `make` target regression, or a test that doesn't actually pin the behavior.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge.
- Save the canonical diff first: `gh pr diff 591 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-3/r1/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the job briefing + the story spec, `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc2-3/r1`, `prior_findings` = none (round 1). Headless mode owns pane mechanics (dedicated tab, `mm-<lens>-r1`), `<lens>.json` + existence check, one retry per failed lens, big-diff chunking, verification pass, consolidation, `consolidated.json`. Close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings → `--comment` + flag Gru.
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; on failure fall back to `gh pr comment 591 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 591 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** righttenantry-refcheck-rc2-3 · **Reviewed sha:** 109ec5d · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _RC2.3 trigger story: auto-create on viewed + manual start/skip APIs; post-commit fail-open + idempotent INSERT ON CONFLICT (deliberate); no migration (skipped enum already in RC2.1)._
  ```
- Before posting, re-fetch `headRefOid`. If it moved, post anyway + note "reviewed `109ec5d`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-3-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5.
