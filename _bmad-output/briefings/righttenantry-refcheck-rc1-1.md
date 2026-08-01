# Briefing: righttenantry-refcheck-rc1-1

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-rc1-1` worktree, branch `refcheck-rc1-1`, base `origin/develop`)
- **GitHub issue:** #548 (v1 arc; sprint tracker: `_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`)
- **Skills policy:** workflow = **bmad-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Review pass before PR: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Implement **Story RC1.1: Attestation & Capture Schema + Submission Write Path** EXACTLY as specced in:

`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` § Story RC1.1 (lines ~193–224) — its Acceptance Criteria, Files/areas, and Verify are the contract.

Design context (read for the why, not to re-litigate): `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (AD-2 attestation, AD-10 fraud-comparator capture, amendment A4 `reference_contact_choice`) and UX §5 for the choice semantics. A sibling minion builds RC2.1 (`reference_call` schema) in parallel on a different branch — stay in YOUR files (below); shared-file collisions are unlikely but if you must touch a file it might own (`shared/src/shared/reference_call.gleam` is THEIRS), don't.

## The contract (from the story)

1. Migration 1: `ALTER TYPE consent_type ADD VALUE IF NOT EXISTS 'reference_contact_attestation'` (precedent: `20260420000003`).
2. Migration 2: `application.submitted_ip_text TEXT` (bounded 64), `application.submitted_user_agent TEXT` (bounded 512), `application.reference_contact_choice TEXT` nullable `CHECK (IN ('attested','declined'))` (A4).
3. Submission transaction: write client IP (via `request_helpers.client_ip`, bounded) + UA (bounded) to the new columns (AD-10); when choice = attested, `insert_acknowledgement_records` gains its fourth write — `reference_contact_attestation` row with current `policy_version`, same transaction (AD-2); declined writes NO row and submits normally; `reference_contact_choice` always set to match.
4. Missing choice at submission → validation FAILS (explicit choice required, no silent skip/default).
5. **Vocabulary constraint (AD-2 §3.2):** attestation/acknowledgement wording ONLY — the word "consent" never appears in relation to this record in code, copy, or comments.

**Files/areas:** `supabase/migrations/YYYYMMDDHHMMSS_*` (two migrations) · `server/src/application/application_handler.gleam` (~1779 `insert_acknowledgement_records` + submission capture) · `server/src/application/sql.gleam` + `server/src/application/sql/` · `shared/src/shared/application.gleam` (new fields + codecs)

**Verify:** migrations apply cleanly from reset; server tests cover attested / declined / missing-choice paths; `make test-server` and `make test-shared` green.

## Acceptance + PR

All story ACs pass with evidence; commit on `refcheck-rc1-1`, push, `gh pr create --base develop` titled "feat: RC1.1 attestation & capture schema + submission write path (#548)" with **Decisions & rationale**. **Never merge.** After merge Gru updates the sprint tracker (or you do per the skill's convention — note which in your final message).

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase; production off-limits). Migrations run against local/dev only.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc1-1 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc1-1 in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-rc1-1 <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-rc1-1" --body "<one-line>"`
- Final message: summary, files changed, PR URL, verify evidence, open questions.
