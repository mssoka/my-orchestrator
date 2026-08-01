# Briefing: righttenantry-refcheck-rc2-1

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-rc2-1` worktree, branch `refcheck-rc2-1`, base `origin/develop`)
- **GitHub issue:** #548 (v1 arc; sprint tracker: `_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`)
- **Skills policy:** workflow = **bmad-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Implement **Story RC2.1: `reference_call` + `reference_objection_log` Schema** EXACTLY as specced in:

`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` § Story RC2.1 (lines ~263–298) — its Acceptance Criteria, Files/areas, and Verify are the contract.

Design context (read for the why): `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` §4.1 (schema) **as amended by the epics doc's A-register** (A1 no `correction_token` · A2 `draft_answers` · A6 `'skipped'` status · A7 `taken_over_at` · A8 four notification types · §6.4 outcome additions). A sibling minion builds RC1.1 (application attestation/capture) in parallel on a different branch — `shared/src/shared/application.gleam` and the `consent_type` enum are THEIRS; stay in your files.

## The contract (from the story)

1. Enums: `reference_call_status` (incl. `'skipped'`, A6) + `reference_call_outcome` (incl. `'unreachable'`, `'form_completed'`, `'manual_recorded'`, §6.4) per architecture §4.1 as amended.
2. `reference_call` table per §4.1 as amended: immutable `contact_*` snapshot, `corrected_email`/`corrected_phone`, attempt accounting (`attempt_count`, `next_attempt_at`, `attempts` JSONB, `correction_cycles`), `form_token` + `form_token_expires_at`, `form_opened_at`/`submitted_at`, **`draft_answers` JSONB** (A2), **`taken_over_at`** (A7), `channel`, `result`/`fraud_signals` JSONB, objection fields, `retention_class`/`purge_after` — and **NO `correction_token`** (A1). `ref_slot`/`owner_label`/`channel`/`retention_class` = TEXT+CHECK (owned deviation §4.1); `status`/`outcome` = PG enums; `updated_at` via existing trigger-function pattern.
3. Indexes: live-row partial unique on `(application_id, ref_slot, owner_label)` excluding every TERMINAL status **but NOT excluding `'skipped'`** (A6); unique partial on `form_token`; sweep/application/contact-phone/purge indexes per §4.1.
4. `reference_objection_log` per §4.1 — **no foreign keys** (must survive parent deletions), purge index, `retention_class` default `'objection_evidence'`.
5. Companion migration: four `notification_type` values — `reference_completed`, `reference_unreachable`, `reference_objected`, `reference_declined` — via `ALTER TYPE ... ADD VALUE` (precedent `20260423100001`) (FR-RC15, A8).
6. Code: `server/src/reference_checks/` module with Squirrel SQL + `sql.gleam` CRUD primitives; `shared/src/shared/reference_call.gleam` types + JSON codecs with status/outcome round-trip tests. RLS auto-enabled with **zero policies** (repo convention §4.4).

**Files/areas:** `supabase/migrations/YYYYMMDDHHMMSS_create_reference_call.sql` (house header-comment style) + the notification-type migration · `server/src/reference_checks/sql.gleam` + `server/src/reference_checks/sql/` · `shared/src/shared/reference_call.gleam`

**Verify:** migration applies from reset; Squirrel codegen succeeds; shared codec round-trip tests green.

## Acceptance + PR

All story ACs pass with evidence; commit on `refcheck-rc2-1`, push, `gh pr create --base develop` titled "feat: RC2.1 reference_call + reference_objection_log schema (#548)" with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase; production off-limits). Migrations run against local/dev only.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-1 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-rc2-1 <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-rc2-1" --body "<one-line>"`
- Final message: summary, files changed, PR URL, verify evidence, open questions.
