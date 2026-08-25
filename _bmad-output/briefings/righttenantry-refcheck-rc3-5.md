# Briefing: righttenantry-refcheck-rc3-5

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, base `develop`).
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion. Perkins: **ON** (production server code + infra). Self-review: bmad-review-edge-case-hunter (cadence races, exactly-once, idempotency, terminal-state respect).
- **Model policy:** **`zai-coding-cn/glm-5.2`** (kimi down this cycle; proven capable. Production code — frontier-preferred, but quota forces glm-5.2; redirect to kimi if it refreshes).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code + Terraform; round on the glm-5.2 fallback while kimi is down).

## Mission

Story **RC3.5: The Sweep — Cadence Engine + Cloud Run Job.** The refcheck sprint continues (rc3-1…rc3-4 merged). rc3-5 ships the **15-minute sweep** that owns every reference-check send + transition: humane chasing, **exactly-once**, self-healing after downtime, never silently dead. It's the engine that actually *fires* the reminders on cadence (rc3-2's templates + helpers are the payload; this is the scheduler/driver).

## Carry-forwards (read the merged work)
- **rc2-1** — `reference_call` schema: `next_attempt_at`, the `attempts` JSONB log, `attempt_count`, `correction_cycles`, `taken_over_at` (A7), `result`/`fraud_signals`. The sweep reads + transitions these.
- **rc3-2** — message templates + send helpers (stop-link, **no-op without Twilio keys**). The sweep SENDS via these.
- **rc3-4** — the exit routes + terminal states the sweep MUST respect: `objected` (sticky, AD-6 — blocked, never re-sent), `refused`/`awaiting_correction`/`form_completed`. A taken-over row (`taken_over_at IS NULL` check) is skipped entirely.
- **rc3-3** — the referee form + `draft_answers` (A2) — the sweep's "form opened? draft exists?" checks + the `partial` terminal from abandoned drafts.

## The story (acceptance — from the epic RC3.5 + arch)

1. **Infra:** a `reference-checks` Cloud Run Job — new `docker-entrypoint.sh` entry, `deployment/terraform/reference-checks-job.tf`, a **15-min Cloud Scheduler** entry in `scheduler.tf` (house pattern, same env-gating as retention/digest), + a shared-secret `POST /api/v1/internal/reference-checks` manual-fire route.
2. **The tick:** for rows with `next_attempt_at <= now()` AND `taken_over_at IS NULL`: compute the due step from the attempt log — **T0 invite / T+24h applicant co-nudge / T+48h reminder 1 / T+96h reminder 2 + landlord warm-handoff (with attempt log) / T+144h terminal `unreachable`** — send via rc3-2 helpers, and apply transition + atomic attempt-append + next-step as **ONE guarded update** (AD-4, AD-14).
3. **Co-nudge gate:** fires only when the form was never opened AND no draft exists (A2); taken-over rows skipped entirely.
4. **T+96h:** reminder 2 + the `reference_unreachable` warm-handoff notification (attempt log rendered); T+144h terminal transition is **silent** (no duplicate terminal notification, §8.3).
5. **Terminals:** abandoned form w/ saved answers → `partial` (result structured from `draft_answers`, unanswered null, confidence capped medium); zero answers → `unreachable`; failed correction cycle → `unreachable` + `reference_unreachable` notification (§4.6).
6. **Failure:** a row that can't process → `failed` (`outcome` NULL + `terminal_reason`), Sentry captures, **no landlord notification** (§4.6).
7. **Liveness (AD-15):** per-tick completion log; any job failure → Sentry.

**Files:** `server/src/reference_checks/sweep.gleam` + sql · `docker-entrypoint.sh` · `deployment/terraform/reference-checks-job.tf` + `scheduler.tf` · `server/src/router.gleam` (internal route).

## Source material (read)
1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — story RC3.5 (full AC).
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — AD-4 (guarded atomic update), AD-14 (state transitions), AD-15 (liveness/abuse), AD-6 (objection stickiness), A2 (draft_answers), A7 (taken_over_at), §4.6 (result mapping), §8.3 (no-duplicate-terminal), §9 (retention).
3. **rc3-2 (merged)** — the send helpers/templates; rc2-1 schema; rc3-4 terminal states.

## Constraints (RT-specific)
- **Exactly-once + idempotent** — re-runs after downtime MUST NOT double-send (no-duplicate-T0 across a retry is a required test). Self-healing after downtime.
- **Respect rc3-4 terminals** — objected (sticky/blocked), refused, awaiting_correction, form_completed; taken-over rows skipped.
- **No-op without Twilio keys** (rc3-2's posture) — the sweep still runs + transitions; SMS just doesn't send until keys are provisioned (external gate).
- **No em-dashes** in any user-facing copy (RT CI ban) — the attempt-log render in the warm-handoff notification.
- **Terraform** — the job + scheduler follow the house pattern (retention/digest precedent); migrations only against local docker test DB.

## Verify
- Fake-clock server tests per cadence step (T0/T+24/T+48/T+96/T+144); guarded-update race test; **no-duplicate-T0 across retry**; terminal-state respect (objected/taken-over skipped); partial vs unreachable from drafts; failed-row path.
- `make test-server` green; `make tf-plan-staging` clean (infra applies).
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip — and DO set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set righttenantry-refcheck-rc3-5 working` at start (`clarifying` if you halt)
- `bin/ledger set righttenantry-refcheck-rc3-5 in-review "PR <url>"` + **`bin/ledger pr righttenantry-refcheck-rc3-5 <url>`** when PR opens
- `herdr notification show "refcheck-rc3-5" --body "<one-line>"` on finish
- Final message: the sweep + infra summary, the cadence steps, test results, whether rc3-6 (verified webhooks) is the natural next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc3-5 · base: develop
- model: zai-coding-cn/glm-5.2 · pr_review: 1 · github_issue: 548
