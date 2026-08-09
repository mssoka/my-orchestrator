# Perkins briefing — round 1: righttenantry-per-applicant-remind

- **PR:** https://github.com/solarity-services/RightTenantry/pull/586 (targets `develop`)
- **Reviewed sha:** `c6868b8bce6b737f708752bcc754f606e2b88045` (head `per-applicant-remind`)
- **repo_root:** `/Users/moses/code/RightTenantry`
- **Round:** 1 of 3
- **Your cwd:** `/Users/moses/.herdr/worktrees/RightTenantry/perkins-per-applicant-remind-r1` — pinned at exactly the reviewed sha. Trust it, not `origin/develop`.
- **Spec:** the original job briefing at `/Users/moses/code/_bmad-output/briefings/righttenantry-per-applicant-remind.md` (the per-applicant Remind button mission). No GitHub issue.
- **prior_findings:** none (round 1).
- **Owner (for `bin/perkins-token`):** `solarity-services`

## What the PR does (review scope)

Adds a **per-applicant "Remind"/"Follow up" button** to the landlord Awaiting list, coexisting with the existing bulk "Send reminder to N" button. The implementing minion reports:
- **New endpoint** `POST /api/v1/vacancies/:id/remind-applicant` (body `{"email": ...}`), handler `handle_remind_applicant` — a faithful mirror of the bulk path: owner check via `find_vacancy_for_invite` (excludes closed/archived/filled), one atomic transaction (per-sender stage-1 + stage-2 mark → validate → clear-rejected → commit), background send via the shared `send_reminders_background`, per-send self-heal on failure. Two new Squirrel queries (`mark_reminder_for_sender`, `mark_followup_for_sender`) scope the same stamps to one email.
- **Per-row button** (`client/src/components/awaiting_section.gleam`), gated on server flags alone: `!reminded`→"Remind"; `reminded && followup_due && !followed_up`→"Follow up"; `followed_up`→hidden; in-flight→"Sending…"; any remind in flight disables every remind button (prevents a stamp race with the bulk). On success, refetches the list.
- **Gate-respecting only** (no force-remind) — the two-stage gate is shared (per-sender scoping), not re-implemented; claimed zero drift vs the bulk path.
- Tests: 8 server integration + 7 client; `make format/test/build` green, `make test-integration` 390 passed. 16 files (3 new).

## ⚠️ CRITICAL lens-guard (read before any lens — prevents false positives)

This is an **email/PII-adjacent user feature**; several deliberate design choices must NOT be flagged as defects:

- **Do NOT flag "no force-remind / can't bypass the stage gate" as a defect.** Gate-respecting-only is the **user-confirmed** design (Gru's lean: the stage discipline is load-bearing for not spamming applicants; force-remind is a *deferred follow-up*, not a gap). The two-stage gate MUST be respected.
- **Do NOT flag "reuses the bulk plumbing instead of standalone" as a defect.** Reusing the email template/sending/validation (`valid_recipients`, `send_reminders_background`) is the **explicit requirement** (no duplicate plumbing). Verify the reuse is *correct*, not that it exists.
- **Do NOT flag the bulk button still existing, or the buttons coexisting, as redundancy.** The per-applicant button is deliberately ADDITIVE to the bulk (the landlord chooses).

### Legitimate findings here would be
- The single-applicant path does NOT faithfully mirror the bulk's **atomicity** (stamp-then-send, un-stamp on send-time validation failure) — a transaction/rollback gap.
- A **gate breach**: the per-applicant endpoint could send a reminder the two-stage gate should suppress (double-send, or stage-2 when only stage-1 is due) — i.e. drift vs the bulk's pinned behavior. The **re-enquiry edge** (old stage-1 + fresh row) is the key case to check.
- **Owner-check / closed-vacancy gap**: the endpoint reminds on a closed/archived/filled vacancy, or across tenants (cross-tenant 404 missing).
- A **stamp race**: concurrent per-applicant + bulk, or two per-applicant clicks, double-stamp or double-send (the "in-flight disables all" guard — does it actually prevent it server-side, not just client-side?).
- **PII leakage**: applicant emails logged/echoed in errors/responses beyond the legitimate recipient.
- **Em-dashes** in user-facing copy (global ban, CI-guarded).
- Broken Gleam/JS parse, a missing test for a pinned behavior, or a `make` target regression.

## Perkins standing orders (verbatim — follow exactly)

- You are Perkins. You review; you never fix, push, or merge. You never touch the implementing minion's worktree or pane.
- Save the canonical diff first: `gh pr diff 586 --repo solarity-services/RightTenantry` → `/Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r1/diff.patch`.
- Run the lenses per the `code-review` skill's **Headless / Automated Mode** with: `diff_file` = the canonical diff, `worktree` = your cwd, `spec_files` = this briefing + the original job briefing (no GitHub issue — skip `gh issue view`), `out_dir` = `/Users/moses/code/_bmad-output/perkins/righttenantry-per-applicant-remind/r1`, `prior_findings` = none (round 1). The headless mode owns: pane mechanics (dedicated tab, `mm-<lens>-r1` labels), the `<lens>.json` contract + existence check, one retry per failed lens, big-diff chunking, the mandatory verification pass, consolidation, `consolidated.json`. You MUST close every lens pane before finishing.
- **Verdict → review event:** 0 blockers → `--approve`; 1–3 → `--request-changes`; 4+ → `--request-changes` + "MAJOR REWORK" lead; **Degraded guard:** any lens failed AND zero findings remain → `--comment` + flag Gru ("incomplete review").
- Post as the app (owner `solarity-services`): `TOKEN=$(/Users/moses/code/bin/perkins-token --owner solarity-services)`; if it failed, fall back to `gh pr comment 586 --repo solarity-services/RightTenantry --body-file <body.md>` + note `fallback-comment`; else `GH_TOKEN=$TOKEN gh pr review 586 --repo solarity-services/RightTenantry --<event> --body-file <body.md>`.
- Body format:
  ```
  ## 🤖 Perkins automated review — round 1 of 3
  **Job:** righttenantry-per-applicant-remind · **Reviewed sha:** c6868b8 · **Reviewers:** <x>/7 completed
  **Verification:** <confirmed>/<total> findings confirmed — <rejected> false-positive[, <u> unverified]

  ### Blockers (n) / ### Warnings (n) / ### Notes (n)
  ### Reviewer agreement
  **Verdict:** READY TO MERGE | NEEDS CHANGES | MAJOR REWORK NEEDED

  _Per-applicant Remind button (gate-respecting, no force-remind — user-confirmed); reuses the bulk email plumbing by design._
  ```
- Before posting, re-fetch `headRefOid`. If it moved mid-review, post anyway but note "reviewed `c6868b8`, head now `<new>` — a fresh round will follow".
- Self-report: `/Users/moses/code/bin/ledger set righttenantry-per-applicant-remind-perkins-r1 working` at start; final message = verdict + review URL + findings counts.
- Skip the `code-review` skill's Step 5 (interactive fix flow).
