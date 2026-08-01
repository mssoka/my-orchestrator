# Briefing: righttenantry-refcheck-v1-architecture

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-v1-architecture` worktree, branch `refcheck-v1-architecture`, base `origin/develop`)
- **GitHub issue:** #548 (read it + comments, incl. the 2026-07-29 gate amendment)
- **Skills policy:** workflow = **bmad-architecture** (follow its step files; orchestration overrides per standing orders — step-01 clarify: ask numbered questions then HALT for Gru relay; internal approval checkpoints pre-approved). Review pass (optional): **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).

## Mission

Produce the **v1 feature architecture** for AI reference-checking (landlord-facing side) as a NEW planning artifact:

`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`

Addendum style — cross-reference the canonical `_bmad-output/planning-artifacts/architecture.md`; do NOT rewrite it. No code changes. Planning artifact + PR only.

## Required reading (in this order)

1. `gh issue view 548 --repo solarity-services/RightTenantry --comments`
2. `_bmad-output/planning-artifacts/research/heist-535/architecture.md` — **the core input**: handoff schema (`ReferenceCallResult v1` full JSON), outcome & lifecycle semantics, repo placement, `acknowledgement_record` guidance, retention/redaction policy
3. `_bmad-output/planning-artifacts/research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md` — synthesis (consent-flow outline, phased framework, risk register)
4. `_bmad-output/planning-artifacts/research/heist-535/legal.md` — skim; design the legal flags IN (Art 14 notice vehicle, Art 21 objection logging, GDPR retention vs DPC delete-after-tenancy, Art 22 decision-support-only)
5. Canonical docs: `architecture.md`, `prd.md` (context, conventions)
6. Code recon (read-only): `supabase/migrations/` (application ref trios already exist — `landlord_ref_*`/`employer_ref_*` in initial schema, `character_ref_*` in `20260420000001`; `acknowledgement_record` + rename migration `20260422000001`), `server/src/application/application_detail_handler.gleam`, `server/src/ai/contract_v4.gleam`, whatever outbound email/SMS infra exists today

## v1 scope — DECIDED, do not re-litigate

- **No voice.** No Twilio, no telephony, no RightTenantryAgents changes. Voice = v2 (RightTenantryAgents#168).
- v1 lands entirely in THIS repo:
  1. **Capture + attestation:** reference details in the application flow (trio fields largely exist — verify against current schema; design any gaps) + `reference_contact_attestation` as a new `record_type` on `acknowledgement_record`. Acknowledgement/attestation framing — NEVER "consent" (the 2026-04-22 rename repudiated consent-as-basis; lawful basis is Art 6(1)(f); Perkins already corrected this once).
  2. **Written-first referee collection:** email + SMS invite → structured referee web form → 2–3 reminders (48h) → applicant co-nudge (T+24h) → landlord warm handoff with attempt log (T+96h) → `unreachable` verdict. Objection/STOP short-circuits ALL contact on every channel (Art 21 evidence logged). Wrong/invalid contact → applicant-correction loop, ONE cycle, then `unreachable`.
  3. **`reference_call` table + full status lifecycle** per heist-535/architecture.md §Lifecycle states, with `attempt_count`, `next_attempt_at`, terminal reasons, `retention_class`, `purge_after`. Exact columns, indexes, RLS policies, enum values, migration shape (follow existing migration conventions).
  4. **Data/API surface for landlord display** (screen design is the UX workstream's job, running in parallel — you define the data contract only): per-reference status, structured summary, fraud signals, attempt log, manual-fallback hooks.
  5. **`ReferenceCallResult v1` storage with `channel: "form"`** — full schema per heist-535/architecture.md; the `form_session` fraud-signals block is in scope; voice-only fields documented as v2-reserved.
- **Re-score integration:** document the additive v5 `reference_call_results[]` field as the forward contract (design-only, per the repo's additive-contract convention v3→v4); implementation deferred to v2.

## Design questions YOU decide (record rationale + rejected alternatives; halt ONLY if genuinely blocking)

- Form delivery: new public tokenized route vs existing handoff/anonymizer patterns — follow repo conventions. Token expiry, one-time vs resumable.
- Outbound email/SMS: what infra exists today; what v1 reuses; ComReg Sender-ID registration flagged as a launch dependency (not resolved here).
- Wizard-of-Oz path (founder-placed calls): does an internal minimal affordance to record a manual outcome belong in v1? Decide + record.
- Referee form content: question set mapping to the schema's `verification` block (tenancy period/rent record/condition/would-rent-again/notice/deposit + free text), grounded in the research.
- Fraud v1 for the form channel: `form_session` signals (completion time, IP/device vs applicant, geo) — what is collectible with current infra, honestly scoped.

## Acceptance

- Artifact at the exact path above; every decision carries rationale + rejected alternatives; legal flags each get an explicit designed-in section; open questions listed (numbered) if any.
- Commit on `refcheck-v1-architecture`, `git push -u origin refcheck-v1-architecture`, `gh pr create --base develop` titled "docs: v1 reference-checking feature architecture (#548)" with a **Decisions & rationale** section. **Never merge.**

## Env/bootstrap

Gru applied standard bootstrap (`_bmad` copied, `.env` symlinked). Env is read-only; commit nothing from it. Docs task — do NOT run the app, migrations, or tests.

## Verify

Artifact exists at the path; markdown renders; internal doc links resolve; no code files touched (`git diff --stat` shows only the new artifact).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-architecture working` at start (`clarifying` if you halt with questions)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-architecture in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-v1-architecture <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-v1-architecture" --body "<one-line>"`
- Final message: summary, files changed, PR URL, open questions.
