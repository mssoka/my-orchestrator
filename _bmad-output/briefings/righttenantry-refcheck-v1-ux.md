# Briefing: righttenantry-refcheck-v1-ux

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-v1-ux` worktree, branch `refcheck-v1-ux`, base `origin/develop`)
- **GitHub issue:** #548 (read it + comments, incl. the 2026-07-29 gate amendment)
- **Skills policy:** workflow = **bmad-ux** (follow its step files; orchestration overrides per standing orders — step-01 clarify: ask numbered questions then HALT for Gru relay; internal approval checkpoints pre-approved). Review pass (optional): **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).

## Mission

Produce the **v1 UX specification** for AI reference-checking (landlord-facing side) as a NEW planning artifact:

`_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`

Feature-specific UX doc (repo convention: `ux-application-detail-*.md`). No code changes. Planning artifact + PR only.

## Required reading (in this order)

1. `gh issue view 548 --repo solarity-services/RightTenantry --comments`
2. `_bmad-output/planning-artifacts/research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md` — synthesis; especially the written-first hybrid consent flow (three doors — v1 ships the FORM door only) and completion benchmarks
3. `_bmad-output/planning-artifacts/research/heist-535/architecture.md` — `ReferenceCallResult v1` schema (`verification` block = the referee form's question spine; `fraud_signals.form_session`), lifecycle states, outcome semantics (objection short-circuit, applicant-correction loop, warm handoff)
4. `_bmad-output/planning-artifacts/research/heist-535/fallback.md` — industry practice on referee-facing forms/reminders (Xref/RefNow/Goodlord patterns)
5. UX/brand canon: `_bmad-output/planning-artifacts/ux-design-specification.md`, `brand-identity-and-design-system.md`, `ux-application-detail-v3.md` (the screen this feature extends)
6. Legal UX obligations (skim `research/heist-535/legal.md`): Art 14 notice content + timing (first contact), objection/STOP visibility, recording N/A in v1 (no voice), Art 22 decision-support framing in landlord-facing copy

## v1 scope — DECIDED, do not re-litigate

- **No voice anywhere.** No "speak to the AI now" door, no call-booking UI. Voice = v2.
- Three actors, three flows:
  1. **Applicant (application form):** reference details capture UX + the `reference_contact_attestation` wording (plain-language, acknowledgement NOT consent — lawful basis is legitimate interest; the words must evidence Art 13 transparency, e.g. "my referees expect to be contacted"). Decline branch: feature stays off for that application, landlord uses the current manual flow — design that state honestly, no dark patterns.
  2. **Referee (written-first collection):** email + SMS invite copy (Art 14 notice in first contact: who/why/retention/rights + objection route) → structured web form (question set mapped to the schema's `verification` block: identity/relationship, tenancy period as-stated check, rent amount confirmation, payment record, property condition, would-rent-again, notice, deposit, free text) → 2–3 reminders (48h) → decline/objection paths → thank-you + what-happens-next. Mobile-first; a busy stranger completes it in <5 min.
  3. **Landlord (application detail):** reference panel — per-reference lifecycle status (queued → contacted → reminded → form_completed | unreachable | declined | objected…), structured summary + notable signals, fraud-signal display (decision-SUPPORT framing, never auto-verdict styling), attempt log, applicant co-nudge trigger/state, warm-handoff (manual fallback) UI with attempt-log export, expectation-setting copy (what form verification does/doesn't prove).
- Edge states to design explicitly: applicant won't attest; referee declines; referee objects (hard stop, landlord sees "referee declined contact"); wrong contact → applicant-correction prompt (one cycle); partial/abandoned form; expired link.

## Constraints

- Follow the brand system + existing UX spec's components/patterns; the application-detail v3 doc is the host surface.
- Copy is part of the deliverable (invite email/SMS, form questions, attestations, landlord-facing states) — write real copy, not lorem.
- The architecture workstream runs in parallel on the data contract — design against heist-535/architecture.md's schema/lifecycle; where you need a data decision, note it as a numbered open question rather than inventing one.

## Acceptance

- Artifact at the exact path above; all three flows + edge states covered with real copy; brand-consistent; legal obligations mapped to specific UI moments; open questions numbered.
- Commit on `refcheck-v1-ux`, `git push -u origin refcheck-v1-ux`, `gh pr create --base develop` titled "docs: v1 reference-checking UX spec (#548)" with a **Decisions & rationale** section. **Never merge.**

## Env/bootstrap

Gru applied standard bootstrap (`_bmad` copied, `.env` symlinked). Env is read-only; commit nothing from it. Docs task — do NOT run the app or tests.

## Verify

Artifact exists at the path; markdown renders; internal doc links resolve; no code files touched (`git diff --stat` shows only the new artifact).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-ux working` at start (`clarifying` if you halt with questions)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-ux in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-v1-ux <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-v1-ux" --body "<one-line>"`
- Final message: summary, files changed, PR URL, open questions.
