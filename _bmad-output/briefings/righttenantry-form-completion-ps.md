# Briefing: righttenantry-form-completion-ps

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`form-completion-ps` worktree, branch `form-completion-ps`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-cis-problem-solving** (follow its step files; orchestration overrides per standing orders — step-01 clarify: numbered questions then HALT for Gru relay, lavish session when practical; internal checkpoints pre-approved). Review pass (optional): **bmad-review-adversarial-general** / **bmad-review-edge-case-hunter**, max 10 panes, badge out all.
- **Model policy:** unset — pi default (you and any mega-minions).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## The problem (Moses, verbatim-ish)

A live founder-run vacancy (70 Meadowgate, Gorey, €2,050/mo, posted 19/05/2026, closes 13/08/2026) is attracting daft.ie applicants who do NOT complete the RightTenantry application form:

- **66 invited — not yet applied** (dashboard state: "Everyone reminded" already sent)
- **8 applied** (all scored; 2 shortlisted) — an ~11% invite→completion rate
- Applicants are motivated (they're hunting accommodation in a scarcity market) yet still don't finish. WHY?

## Mission

Run a CIS problem-solving session (with Moses — interactive, halt for his input per the overrides) to diagnose the invite→completion drop-off and produce an options analysis + recommendation. His seed hypotheses (test, don't assume):

1. **Daunt factor:** the full field list visible at once scares people off
2. **Progressive disclosure:** page-at-a-time flow (with or without progress indication) as the alternative
3. Open beyond these: what else could explain motivated renters bouncing? (Consider: daft.ie browsing context / low per-listing intent, mobile-first applicants, trust in an unknown site asking for employer+landlord+character ref trios AND per-adult proof documents (mandatory since the 2026-04-20 migration), the daft email handoff flow, reminder-channel fatigue, form length vs perceived stakes "just to get a viewing")

## Evidence to ground it (read first)

- Screenshot of the live dashboard (66/8/2 funnel state): `/Users/moses/Desktop/Screenshot 2026-07-31 at 16.15.55.png` (copy into your evidence notes)
- The form implementation: `client/src/` application form components + `shared/src/shared/application.gleam` (field list, order, mandatory rules, document uploads) — INSPECT the real thing, count fields/pages, note what's mandatory
- Prior research: `_bmad-output/planning-artifacts/research/ux-tenant-application-form-research-2026-03-28.md` and `technical-daft-applicant-handoff-research-2026-03-28.md`
- Sprint history on form simplification: `_bmad-output/planning-artifacts/sprint-change-proposal-2026-04-19-application-form-document-simplification.md`, `...-2026-04-02-personal-statement.md`, `...-2026-04-19-household-income-and-co-applicants.md`
- Read-only production DB funnel queries are ALLOWED (aggregates only — counts, timestamps, step-level drop-off if instrumentable; NO PII beyond aggregates). Precedent: the U1 resolution.

## Deliverable

`_bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md` — root-cause analysis (evidence-weighted, honest about what's unmeasurable today), the options space (incl. progressive-disclosure variants AND non-form options: pre-form value framing, daft-side expectations, document-deferral, save-and-resume, reminder redesign), a recommendation with an **experiment plan** (what to change first, what to measure, decision dates) — then **lavish review BEFORE the PR** (standing policy: serve, poll, apply annotations, then PR to `develop`).

## Acceptance

- Analysis grounded in the REAL form (field counts, mandatory audit) + the 66/8 funnel + prior research; options beyond the seed two; recommendation with measurable experiment; Moses's session inputs incorporated (this is a session WITH him — halt for his rulings at the skill's checkpoints).
- Lavish review loop completed, then PR `docs: application-form completion problem-solving (#form-completion)` to `develop` with **Decisions & rationale**. **Never merge.**

## Env/bootstrap

Standard bootstrap applied (`_bmad` copied, `.env` symlinked — read-only). DB access is READ-ONLY, aggregates only, per the mission. Do NOT run migrations or modify production anything.

## Verify

Artifact exists; markdown renders; lavish session completed with feedback applied; `git diff --stat` shows only the new artifact (plus evidence copies).

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-form-completion-ps working` at start (`clarifying` when you halt)
- `/Users/moses/code/bin/ledger set righttenantry-form-completion-ps in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-form-completion-ps <url>`
- On blocked/finished: `herdr notification show "righttenantry-form-completion-ps" --body "<one-line>"`
- Final message: summary, files changed, PR URL, top-3 suspected causes, open questions.
