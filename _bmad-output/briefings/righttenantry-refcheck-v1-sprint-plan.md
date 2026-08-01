# Briefing: righttenantry-refcheck-v1-sprint-plan

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`)
- **Worktree:** this pane's cwd (`refcheck-v1-sprint-plan` worktree, branch `refcheck-v1-sprint-plan`, base `origin/develop`)
- **Skills policy:** workflow = **bmad-sprint-planning** (follow its step files; orchestration overrides per standing orders — genuine blockers: numbered questions then HALT for Gru relay; internal checkpoints pre-approved). No review swarm needed for a tracking artifact.
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.

## Mission

Generate the **sprint status tracker** for the v1 reference-checking build from the merged epics doc, per the bmad-sprint-planning skill:

`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md` — 5 epics / 18 stories (RC1.1 → RC5.2) + A1–A9 amendments register. This is the source of truth for story ids, titles, and dependencies.

## Context

- All 18 stories are `backlog` (nothing started; the build was paused by user decision 2026-07-31 and re-activated 2026-07-31 evening).
- Sequencing notes to encode: RC1.1 first (schema foundation); RC2.1's schema can parallel RC1.x; RC3.x needs RC2.x contracts; RC3.1 has an external dependency (Twilio provisioning — flag it); RC4 needs RC2/RC3 payload contracts; RC5 last (WoZ + hardening). The non-code gates (ComReg Sender-ID registration, counsel pack) belong in the tracker as dependency notes, not stories.
- Output path/frontmatter per the skill's conventions; name it for this feature line (refcheck-v1).

## Deliverable + review loop (docs policy)

Sprint status artifact at the skill's conventional path, then **lavish review BEFORE the PR** (standing docs policy: serve, poll with `--agent-reply "Sprint plan for the 18-story refcheck v1 build — sequencing + dependency flags — annotate anything to change"`, apply annotations, then PR).

## Acceptance

- Tracker covers all 18 stories with statuses + dependency flags + the external gates noted; lavish review completed; PR `docs: refcheck v1 sprint plan (18 stories) (#548)` to `develop` with **Decisions & rationale**. **Never merge.**

## Self-report (do not skip)

- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-sprint-plan working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-v1-sprint-plan in-review "PR <url>"` when the PR opens, and `/Users/moses/code/bin/ledger pr righttenantry-refcheck-v1-sprint-plan <url>`
- On blocked/finished: `herdr notification show "righttenantry-refcheck-v1-sprint-plan" --body "<one-line>"`
- Final message: summary, files changed, PR URL, first story ready to dispatch.
