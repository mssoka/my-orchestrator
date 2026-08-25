# Briefing: righttenantry-refcheck-rc3-4

- **Repo:** RightTenantry (`/Users/moses/code/RightTenantry`, remote: `solarity-services/RightTenantry`)
- **Worktree:** standard minion worktree off `develop` (develop has rc3-1 sms_client + rc3-2 templates + rc3-3 form session, all merged). PR targets `develop`.
- **Workflow:** **bmad-create-story** → **bmad-dev-story**. Fresh minion (learning-loop pattern). Perkins: **ON** (code — referee-facing exit routes + result structuring). Self-review: **bmad-review-edge-case-hunter** (objection stickiness vs late events, guarded double-submit, wrong-person no-resend, result determinism).
- **Model policy:** **`zai-coding-cn/glm-5.2`** — kimi is down this cycle (quota 403); glm-5.2 is the proven capable fallback (rc3-3 r2 ran an 8-pane round to APPROVED on it). This is production server code that would normally take the frontier tier (kimi), but quota forces glm-5.2 now; Gru will redirect to kimi if it refreshes mid-job.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out shard per standing orders.
- **Perkins:** ON (code; round runs on the glm-5.2 fallback while kimi is down).

## Mission

Story **RC3.4: Form Completion & Exit Routes — Submit, Decline, Objection, Wrong Person.** The sprint's rc3-1/2/3 are merged; **rc3-4 is next.** rc3-3 shipped the referee form *session* (`/reference/:token` — open, answer, autosave, resume). rc3-4 ships **everything that happens when the referee finishes or bails**: the submit path with deterministic result structuring, plus the three honest exit routes (decline / objection / wrong-person), their notifications, and the thank-you screen. Every exit is honoured instantly and truthfully.

## ⚠️ MANDATORY: register every new route in ALL the registries (the rc3-3 lens-guard is watching)

rc3-4 adds new POST routes (submit, decline, object, wrong-person, and the `/reference/:token/stop` arm rc3-3 stubbed). Each must be registered in **every** registry — exactly the AD-3 discipline rc3-3 applied:
- `middleware.is_public_path` (no auth — referee has no login)
- **the CSRF registry** — rc3-3's Perkins round ran a **csrf-registry-completeness lens-guard**; any new public POST route missing from the CSRF allowlist is a guaranteed blocker. Add every rc3-4 POST route.
- `middleware.redact_token_route` (token redaction in Sentry/access-log/CSP) — rc3-3 added the `/reference` arm; rc3-4's sub-routes ride it, but verify.

Treat registry completeness as a first-class acceptance item, not an afterthought.

## Also carry forward: scan the rc3-3 r2 review before starting

Before implementing, read the **rc3-3 Perkins r2 findings**
(`_bmad-output/perkins/righttenantry-refcheck-rc3-3/r2/consolidated.json` if present,
else the r1) for any advisory touching `form_handler.gleam`, `result.gleam`, or
`notification_dispatch.gleam` — the exact files rc3-4 extends. Fold in anything
relevant. (rc3-3 r2 was APPROVED, 0 blockers, so likely light — but check.)

## The story (acceptance — from the epic RC3.4 + architecture)

1. **Submit (completed form POST):** validation passes → structured, deterministic
   `ReferenceCallResult v1` (AD-9): `schema_version:"refcall-v1"`, `channel:"form"`,
   the `verification` block with per-slot variants (A9), `free_text_signals` verbatim,
   deterministic `ai_summary` with completeness-derived `confidence`, and the
   `compliance` block. A **guarded** `UPDATE ... WHERE status='contact_initiated'`
   transitions the row to `form_completed` (AD-14). `result` + denormalised
   `fraud_signals` written; `purge_after` stamped from the application's
   `retention_due_at` when set; audit terminal entry written. A second POST to the
   same token → branded "already completed" page — **one submission only** (AD-3).

2. **Notifications:** `reference_completed` / `reference_declined` / `reference_objected`
   (types exist since RC2.1) dispatch through the existing dispatcher (respecting
   `notification_preference`) with copy per **UX §7.9 verbatim**.

3. **Decline route** (in every message + landing screen): referee declines (optional
   one-line reason, **never required**) → row terminates `refused` (A8) with a result
   per §4.6 (outcome + attempts, null `verification`); `reference_declined` fires;
   confirmation copy per UX §10.2; all messages stop.

4. **Objection route** ("don't contact me"): **AD-6 applies** — status `objected`
   (**sticky**: a later bounce or sweep tick CANNOT move it, AD-14), `next_attempt_at`
   NULL, all future sends blocked, and a `reference_objection_log` row written **at
   objection time** by the objection handler **alone** (single writer; Art 21 evidence,
   survives parent deletions). `reference_objected` notification fires.

5. **Wrong-person route:** referee says details are wrong → row moves to
   `awaiting_correction` — **never a re-send to the same details** (AD-7); the landlord
   sees the "Contact details didn't work" state (surfaced in RC4).

6. **Thank-you screen:** renders per **UX §6.5 verbatim**, **identical for every
   completion path** (a referee is never told the landlord took over, UX §8.6).

## Source material (read)
1. **`_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md`** — story RC3.4 (the full AC above).
2. **`_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`** — AD-9 (deterministic result), AD-14 (guarded transitions + objection stickiness), AD-6 (objection short-circuit + evidence log), AD-7 (wrong-person no-resend), AD-3 (one submission + route registration), A8 (`refused` decline), A9 (per-slot variants), §4.6 (result mapping), §9.2 (objection log).
3. **`_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`** — §7.9 (notification copy, verbatim), §6.5 (thank-you screen), §8.6 (referee never told of takeover), §10.2 (confirmation copy).
4. **rc3-3 (merged #596)** — the `/reference/:token` form session this completes; the `/reference/:token/stop` route rc3-3 stubbed for rc3-4 to own. Read `spec-rc3-3-...md` + the merged form session code.
5. **rc2-1 (merged)** — `reference_call` status/outcome enums, `reference_objection_log` schema, the four `notification_type` values, the token partial index.
6. **`server/src/middleware.gleam`** (the registries — public path, CSRF, redact_token_route) + `server/src/notification/notification_dispatch.gleam` (the dispatcher rc3-4 emits through).
7. **`_bmad-output/implementation-artifacts/sprint-status-refcheck-v1.yaml`** — rc3-4 → in-progress → done/review.

## Flow
1. **bmad-create-story** — rc3-4 spec (the four exit routes + result structuring + the route-registry checklist). Update the tracker (rc3-3 → done if Silas hasn't; rc3-4 → in-progress).
2. **bmad-dev-story** — `form_handler.gleam` exit routes (submit/decline/object/wrong-person), `result.gleam` (deterministic ReferenceCallResult v1), notification dispatch, thank-you screen, and the full route-registry registration. Apply the rc3-3 r2 carry-forward if any.
3. **Test:** per-path server tests — guarded double-submit, **objection stickiness vs a late bounce/sweep event**, decline (refused + null verification), wrong-person (awaiting_correction, no resend), per-slot result structuring (AD-9), §4.6 mapping, notification dispatch per preference, thank-you identical across paths, **CSRF/public-path/redact registration for every new route**. `make test-server` + `make test-integration` green.
4. **Update tracker:** rc3-4 → review/done.

## Constraints (RT-specific)
- **No em-dashes in user-facing copy** (RT CI-guarded ban) — notification copy, thank-you screen, confirmation pages.
- **SSR never requires JS** — the exit routes work as plain POSTs (decline/object/wrong-person reachable without JS).
- **Objection stickiness is load-bearing** — AD-6/AD-14. A late event (bounce, sweep tick, second submission) MUST NOT un-object or move an objected row. This is the hardest edge case; lean on bmad-review-edge-case-hunter here.
- **`reference_objection_log` single writer** — only the objection handler writes it, at objection time.
- The referee-facing copy is truthful + plain (the referee is doing the applicant a favour).

## Acceptance
- The four exit routes ship: submit (deterministic result + guarded transition + double-submit guard), decline (`refused`), objection (sticky + evidence log), wrong-person (`awaiting_correction`, no resend) — + notifications (§7.9 verbatim) + thank-you (§6.5, identical across paths).
- Every new route registered in **all** registries (public path + CSRF + redact).
- `make test-server` + `make test-integration` green. No em-dashes in copy.
- After user approval: commit, push, open PR targeting `develop`. **Never merge.**

## Self-report (do not skip)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-4 working` at start (`clarifying` if you halt)
- `/Users/moses/code/bin/ledger set righttenantry-refcheck-rc3-4 in-review "PR <url>"` when the PR opens
- `herdr notification show "refcheck-rc3-4" --body "<one-line>"` on finish
- Final message: the four exit routes + result structuring summary, route-registry registration confirmed, test results, story-spec path, PR URL, + whether rc3-5 (sweep cadence engine) is the natural next.

## Dispatch parameters
- repo: RightTenantry · repo_root: /Users/moses/code/RightTenantry · slug: righttenantry-refcheck-rc3-4 · base: develop
- model: zai-coding-cn/glm-5.2
- pr_review: 1  (Perkins ON; round runs on the glm-5.2 fallback while kimi is down)
- github_issue: 548
