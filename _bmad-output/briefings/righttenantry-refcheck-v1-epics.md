# Briefing: righttenantry-refcheck-v1-epics

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-v1-epics` worktree, branch `refcheck-v1-epics`, base `origin/develop`)
- **GitHub issue:** #548 (design PRs #550/#551/#552 all MERGED — this is the build-plan step)
- **Skills policy:** workflow = **bmad-create-epics-and-stories** (follow its step files; orchestration overrides per standing orders — step-01 clarify: ask numbered questions then HALT for Gru relay; internal approval checkpoints pre-approved). Review pass (optional): **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Produce the **v1 epic + story breakdown** for AI reference-checking (landlord-facing side) as a NEW planning artifact:

`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`

Feature-specific addendum in the style of `epics.md` (DB-to-UI vertical slices, theme/design baked in); cross-reference the canonical `epics.md` — do NOT rewrite it. Docs only; PR to `develop`.

## Required reading (in this order)

1. `gh issue view 548 --repo solarity-services/RightTenantry --comments` (scope + the 2026-07-29 gate amendment)
2. `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` — **the data contract**: 16 ADs, `reference_call` lifecycle, cadence sweep, attestation, objection log, WoZ `channel: "manual"`, §9.5 `display_disclaimer`, §11 open questions
3. `_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md` — **the flows**: three actors + edge states + §15 decisions record (all 11 OQs decided)
4. `epics.md` (conventions: slice shape, story format, sizing) + `prd.md` (framing) + `architecture.md` (system canon)
5. Skim `_bmad-output/planning-artifacts/refcheck-pitch-copy-deck-2026-07-29.md` §5–6 (gate-2 instrument + WoZ ops) — context for the WoZ epic, NOT app scope

## Scope — DECIDED, do not re-litigate

- **v1 = this repo only, no voice.** Epics cover: reference capture + `reference_contact_attestation` · written-first collection (capability-token form, email/SMS via existing Resend domain + RTenantry Sender ID, T0→T+144h cadence sweep job, objection/STOP short-circuit + `reference_objection_log`, one-cycle applicant-correction loop) · `reference_call` lifecycle + landlord reference panel (status, structured summary, fraud signals, attempt log, warm handoff, §9.5 `display_disclaimer` per channel) · WoZ manual channel (founder records outcomes) · form-channel fraud signals (`form_session` block, applicant IP/UA capture with Art 13 update).
- **Out of scope (mark as dependencies, NOT stories):** ComReg Sender-ID registration (ops), Irish counsel pack / DPIA update (external), v5 re-score + voice channel (v2 = RightTenantryAgents#168), localized forms (v2).
- Every story must be dispatchable to a minion: clear acceptance criteria, files/areas touched, verify steps. Size stories so each fits one focused job.

## Acceptance

- Artifact at the exact path above; epics are DB-to-UI slices with correct UX/legal baked in (attestation wording, objection short-circuit, Art 14 first-contact notice, §9.5 disclaimer are IN the stories, not bolt-ons); dependencies section lists the non-code gates; story count/sizing sanity-checked against the architecture ADs.
- Commit on `refcheck-v1-epics`, `git push -u origin refcheck-v1-epics`, `gh pr create --base develop` titled "docs: v1 reference-checking epics & stories (#548)" with a **Decisions & rationale** section. **Never merge.**

## Env/bootstrap

Gru applied standard bootstrap (`_bmad` copied, `.env` symlinked). Env is read-only. Docs task — do NOT run the app or tests.

## Verify

Artifact exists at the path; markdown renders; internal links resolve; `git diff --stat` shows only the new artifact.

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-epics working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-epics in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-v1-epics <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-v1-epics" --body "<one-line>"`
- Final message: summary, files changed, PR URL, epic/story counts, open questions.
