# Briefing: righttenantry-refcheck-privacy-draft

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-privacy-draft` worktree, branch `refcheck-privacy-draft`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-quick-dev** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). Self-review before lavish: **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter** (docs lens: GDPR accuracy, internal contradictions), max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** off (legal-copy deliverable, lavish review gates the PR).

## Mission

Draft the **referee-data privacy content** for the `/privacy` page — the section rc1-2's attestation card links to ("How we handle referee data ↗"). USER RULING (2026-08-01): write the content NOW; it remains a **draft pending counsel review** (launch-gating per the counsel pack — mark it as such, don't block on it).

The privacy page lives at `server/src/legal/privacy_view.gleam` + `server/src/legal/privacy_sections/`. Match the existing page's structure, voice, and section pattern.

## What the section must cover (ground every claim in these sources — no invented practices)

Spec of record: `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` — especially **§9.2 (objection), §9.3 (retention), §9.4 (fraud signals honesty), §9.5 (disclaimers), AD-2, AD-6, AD-10, AD-14, AD-16**.

1. **What we collect about referees** — name + contact trio (email/phone) as listed by the applicant; the structured form answers once given.
2. **How it's used** — contacting the referee to complete a short structured reference for a specific rental application; per-slot question sets; no marketing, no unrelated use.
3. **The forewarning + Art 14 notice** — the applicant attests referees expect contact (AD-2; wording is attestation/acknowledgement, NEVER "consent" as the legal basis claim); the first contact (T0 invite) carries the Art 14 notice, incl. the right to object (AD-6/legal thread).
4. **Objection (Art 21)** — any objection (form decline, SMS STOP, flagged reply) stops all contact immediately, permanently, on every channel; an evidence record is kept for this purpose (and only this purpose) even if the application is deleted (§9.2).
5. **Fraud-prevention processing (honesty per AD-10)** — phone line-type lookup (Twilio Lookup), IP/User-Agent comparison signals; signals are shown to the landlord as context, never used for automated rejection.
6. **Retention & erasure** — referee data follows the application's retention schedule (`retention_due_at`, CASCADE sweep per §9.3); how a referee requests erasure/contact.
7. **Who processes it** — Twilio (SMS + lookup), Resend (email) as processors; no sale of data.

## Review loop (lavish — BEFORE the PR opens)

Legal copy is a DOCS deliverable: when drafted + self-reviewed, render the section via the **lavish** skill and post the review URL in your final message. Do NOT open the PR until the user's verdict comes back through Gru/Silas.

## Acceptance

- New referee-data section on `/privacy`, matching page conventions; every practice claim traceable to the architecture (no promised feature that isn't in RC design — the contact engine is RC2/RC3, so phrase as the system's design, and include the "draft pending counsel review" marker per the page's existing conventions if one exists, else an HTML comment); lavish URL delivered.
- After user approval: commit on `refcheck-privacy-draft`, push, `gh pr create --base develop` titled "docs: referee-data privacy section (refcheck counsel pack, draft)" . **Never merge.**
- `make test` green (SSR render of the privacy page covered if the repo has such a test pattern).

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — **STAGING** Supabase per the field notes; production is off-limits).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-privacy-draft working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger note righttenantry-refcheck-privacy-draft "lavish review posted: <url>"` when the review goes up
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-privacy-draft in-review "PR <url>"` when the PR opens (after approval), and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-privacy-draft <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-privacy-draft" --body "<one-line>"`
- Final message: summary, files changed, lavish URL, coverage checklist (7 points above), open questions.

## Dispatch parameters

- repo: RightTenantry
- repo_root: /Users/moses/code/RightTenantry
- slug: righttenantry-refcheck-privacy-draft
- base: develop
