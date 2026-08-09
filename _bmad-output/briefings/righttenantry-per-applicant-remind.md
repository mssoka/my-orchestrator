# Briefing: righttenantry-per-applicant-remind

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (RT uses develop → main; PR targets develop)
- **Workflow:** quick-dev. Perkins: **ON** (code change, PII-adjacent — sends reminder emails; r1 fires on PR open).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code + email/PII-adjacent; one round).

## Mission

The landlord dashboard's "Awaiting" section (applicants invited but not yet applied) currently has ONE header button: **"Send reminder to N"** — it reminds ALL eligible applicants in the vacancy at once. The problem: the pool mixes stale invites (days ago) with fresh ones (today), and a landlord doesn't want to nag someone just invited. **Add a per-applicant "Remind" button** so the landlord can selectively remind individuals — coexisting with the existing bulk button.

## Current implementation (already mapped by Gru — read these, don't re-discover)

- **Awaiting list endpoint:** `GET /api/v1/vacancies/:id/awaiting` → `handle_get_awaiting` in `server/src/vacancy/vacancy_handler.gleam` (~line 399). Returns per-applicant: `email, name, invited_at, reminded, followed_up, followup_due`. **The per-applicant data already flows to the client** — the frontend can render a per-row button from this.
- **Awaiting SQL:** `server/src/vacancy/sql/list_awaiting_for_vacancy.sql` — the pool (invited, not applied), with two-stage reminder flags (`reminder_sent_at`, `second_reminder_sent_at`).
- **Bulk remind handler:** `handle_remind_applicants` in `server/src/inbound_email/inbound_handler.gleam` (~line 508), routed at `server/src/router.gleam:525`. Does an atomic transaction: `mark_reminders_for_vacancy` (stage 1) + `mark_followup_reminders_for_vacancy` (stage 2) → stamps + returns recipients → sends emails → clears rejected stamps. Stage 1 = never-reminded; stage 2 = stage-1 series completed ≥2 days ago.
- **The two-stage reminder system** (stage 1: doc-gathering nudge; stage 2: deadline follow-up). Per-email gate lives in the `inbound_email_sender_state` view.

## The change

### 1. Backend: single-applicant remind endpoint
Add a new endpoint, e.g. `POST /api/v1/vacancies/:id/awaiting/:email/remind` (or a body/param variant — match the codebase's routing conventions) that reminds ONE applicant (by email + vacancy). It must:
- **Reuse the email-sending logic + template + validation** (`valid_recipients`, the resend path) from the bulk handler — do NOT duplicate the email plumbing.
- **Respect the two-stage gates for that individual** — send the reminder that's NEXT-DUE for that applicant: stage 1 if never reminded; stage 2 if stage-1 series completed + `followup_due`. If both stages already sent, the endpoint returns a clear "already fully reminded" response (the frontend will have hidden the button, but the server is the source of truth).
- **Atomic stamp+send** for the single recipient (same transactional discipline as the bulk handler — stamp then send, un-stamp on send-time validation failure).
- Same owner-check + `find_vacancy_for_invite` (no reminders on closed/archived/filled vacancies) as the bulk handler.

### 2. Frontend: per-row "Remind" button
In the Awaiting list rendering, add a **per-applicant "Remind" button** on each row, alongside the existing header "Send reminder to N" bulk button. Gate it on the applicant's state:
- Show "Remind" (stage 1) when `!reminded`.
- Show "Follow up" (stage 2) when `reminded && followup_due && !followed_up`.
- Hide/disable when `followed_up` (both stages sent — nothing more to send).
The button calls the new single-applicant endpoint; on success, update that row's flags (optimistic or re-fetch — match the existing list's refresh pattern).

### 3. Keep the bulk button
The header "Send reminder to N" stays — the per-applicant button is ADDITIVE. (The landlord chooses: bulk for convenience, per-applicant for selectivity.)

## Design question (surface in your self-report, don't block)
Should the per-applicant button let the landlord **force-remind** (bypass the stage gate, e.g. re-nudge someone already at stage 1), or strictly respect the next-due gate? Gru's lean: **respect the gate** (no accidental double-send; the stage discipline is load-bearing for not spamming applicants). Implement gate-respecting; if you think force-remind is warranted, note it as a follow-up option, not the default.

## Constraints
- Reuse the existing email template/sending — no duplicate plumbing.
- Atomic stamp+send (transactional, un-stamp on failure) — same discipline as bulk.
- Owner check + no-remind-on-closed/filled vacancy (server-side defence).
- No em-dashes in any user-facing copy (global ban, CI-guarded).
- Respect the two-stage reminder discipline (don't let the per-applicant button spam).

## Acceptance
- New single-applicant remind endpoint, reusing the email logic, gate-respecting, atomic.
- Per-row "Remind"/"Follow up" button in the Awaiting list, gated on applicant state.
- Bulk button unchanged + coexisting.
- `gleam test` / `make test-server` passes; add tests for the new endpoint (single-applicant stamp+send, gate-respecting, owner-check, no-remind-on-closed).
- No em-dashes in copy.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-per-applicant-remind working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-per-applicant-remind in-review "PR <url>"` when PR opens
- `herdr notification show "per-applicant-remind" --body "<one-line>"` on finish
- Final message: the new endpoint + route, the per-row button behavior, the gate-respecting logic, the design-question answer, PR URL.

## Dispatch parameters
- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-per-applicant-remind
- base: develop
