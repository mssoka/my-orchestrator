# Briefing: righttenantry-refcheck-rc2-2

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (RT uses develop → main; PR targets develop). Develop is current (has prior refcheck rc1-1/rc1-2/rc2-1 + #586).
- **Workflow:** **bmad-create-story** (generate the rc2-2 story spec from the epics) → **bmad-dev-story** (implement it). The story file doesn't exist yet — create it first, then dev. Perkins: **ON** (code, full-stack slice; r1 fires on PR open).
- **Model policy:** unset — pi default.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; one round).

## Mission

Resume the RT Reference-Checking v1 sprint (issue #548) at **story RC2.2: `viewed` Application Status, End to End.** The sprint paused after rc1-1/rc1-2/rc2-1 (3/18 done); rc2-2 is next per the sequencing note.

## The story (acceptance criteria — from the epics doc)

**Story RC2.2: `viewed` Application Status, End to End**

> As a landlord, I want to mark that the viewing has been carried out, so that the application reflects where it really is — and reference checks know when they may start.

**Acceptance Criteria:**

1. **Migration:** `ALTER TYPE application_status ADD VALUE 'viewed' AFTER 'shortlisted'` succeeds when the migration runs.
2. **Shared type codec:** the shared `ApplicationStatus` type — `Viewed` encodes/decodes as `"viewed"` across shared, server (`parse_status` in `application_detail_handler.gleam`, including the 400 message), and client. Round-trips cleanly.
3. **Status stepper:** the application detail page progression is **Submitted → Reviewing → Shortlisted → Viewed → Approved** (Reject unchanged). Rank logic updated. `viewed` gets a status-pill style in the house semantic set — **navy** (in-progress, between amber shortlisted and teal approved).
4. **Filters/leaderboard:** leaderboard rows and any status filters render `viewed` without breaking.

## Source material (read — the spec + patterns)

1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — the rc2-2 story + acceptance criteria (quoted above) + the full epic context.
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — the data contract (AD-13 maps to rc2-2/rc2-3 — the `viewed` status lifecycle).
3. **The prior refcheck stories for PATTERNS** (how rc1-1/rc1-2/rc2-1 did migration + type + codec + UI — match their conventions): rc1-1 (#557, attestation schema + write path), rc2-1 (#558, reference_call + objection_log schema). Read their commits/diffs for the established migration + codec + pill conventions to follow.
4. **`_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`** — the status-pill semantic set (the navy "viewed" pill lives in the house style).
5. The sprint tracker: `_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml` — update rc2-2 to in-progress → done as you work.

## Flow

1. **Create the story spec** (bmad-create-story) at `_bmad-output/implementation-artifacts/` — the rc2-2 story file with full context (the acceptance criteria above + the architecture/UX refs + the prior-story patterns). Update the sprint-status tracker: rc2-2 → in-progress.
2. **Dev the story** (bmad-dev-story): implement migration + shared type + server codec + client stepper/pill + filters. Follow the prior refcheck stories' conventions exactly.
3. **Test:** migration test, codec round-trip (shared/server/client), stepper render with `viewed`, status-filter + leaderboard render. `make test-server` + `make test-integration` green.
4. **Update the tracker:** rc2-2 → done (or review) on completion.

## Constraints (RT-specific — these APPLY here, unlike PP)
- **No em-dashes in any user-facing copy** (RT global ban, CI-guarded). The status-pill labels, the stepper, any copy — em-dash-free.
- Follow the established application_status conventions (the existing Submitted/Reviewing/Shortlisted/Approved/Reject set — `viewed` slots in after Shortlisted).
- The navy "viewed" pill must match the house semantic set (amber shortlisted → **navy viewed** → teal approved).
- Migration is additive (`ADD VALUE`) — don't touch existing status values.

## Acceptance
- The 4 acceptance criteria met (migration, codec, stepper+pill, filters/leaderboard).
- Story spec file created + sprint-status tracker updated.
- `make test-server` + `make test-integration` green.
- No em-dashes in copy.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-2 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc2-2 in-review "PR <url>"` when PR opens
- `herdr notification show "refcheck-rc2-2" --body "<one-line>"` on finish
- Final message: the migration + codec + stepper/pill + filters summary, test results, the story-spec path, PR URL, + whether rc2-3 (the trigger APIs) is the natural next dispatch.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc2-2 · base: develop
