# Lens: Acceptance Auditor (source: `acceptance`) — Perkins RC3.5 r1

Read and follow `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/lens-prompts/_shared_context.md` first (inputs, invariants, output contract). Then apply this lens.

## YOUR LENS — spec/acceptance auditor
Audit the diff against the spec and context docs (the round briefing, job briefing, story spec, and the architecture AD-4/AD-6/AD-14/AD-15/§4.6/§8.3). Identify:
- Violations of specific acceptance criteria (AC1–AC8 in the story spec).
- Deviations from spec intent.
- Missing implementation of specified behavior.
- Contradictions between spec constraints and actual code.
- Scope drift — changes not asked for by the spec.

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Pay particular attention to:
- AC1 infra (Cloud Run Job arm in `docker-entrypoint.sh`, `reference-checks-job.tf`, 15-min scheduler in `scheduler.tf`, shared-secret manual-fire route).
- AC2 the guarded update shape (`WHERE id AND status AND attempt_count=$n`).
- AC3 exactly-once + the no-duplicate-T0 test (is it REAL?).
- AC4 co-nudge gate + taken-over skip.
- AC5 T+96 warm handoff (fires AFTER the guarded advance; attempt log rendered) + T+144 silent terminal.
- AC6 terminal-state respect (objected sticky).
- AC7 failure path (failed + Sentry + NO landlord notification) + per-tick liveness log.
- AC8 no-op without Twilio keys.

Note: the story spec item 7 says the manual-fire handler should thread `sentry_client.Disabled` ("manual runs don't escalate"). Check whether the implementation matches.

## OUTPUT
Write ONLY your JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/acceptance.json`
Use `"source": "acceptance"`. Then stop.
