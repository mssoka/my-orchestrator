# Running Log — righttenantry-refcheck-bughunt2 (round 2 bug hunt)

Chronological log (2026-08-15, local times). All browser work ran in agent-browser session
`rt-refcheck-bughunt2` (dedicated — the default session is shared machine-wide).

## 00:5x — Boot & recon
- Worktree confirmed at `7675c81` (develop HEAD post-#620) on branch `rt-refcheck-bughunt2`; clean status.
- Read field-notes (stacked-forms + timing-gate lessons load-bearing), the bug-hunt SKILL.md + guides, and the
  re-creation spec (`refcheck-verification-rerun-report.md`). `reference_checks` suite confirmed absent (twice-swept).
- Surveyed the surface: panel testids (`refcheck-row-<slot>`, `refcheck-expand-<slot>`, `refcheck-status-<slot>`,
  `refcheck-correct/substitute-open-<slot>`, `refcheck-edit-{name,email,phone}-<slot>`, `refcheck-edit-save/cancel-<slot>`,
  `refcheck-export-<slot>`, `refcheck-confirm-*-yes/no-<slot>`, overflow/menu), the referee-form routes
  (`/reference/:token`, `/answer`, `/decline`, `/stop`, `/wrong-person`, `/resend`) and testids, the
  reference_call_status enum, and the exact copy strings for verification.

## 00:55–01:00 — Sandbox bring-up
- New DB container `rt-refcheck-bughunt2-dev-db` (Postgres 16-alpine, port 54337 — free) + full migration chain
  via `TEST_DB_PORT=54337 bash scripts/reset-test-db.sh` (DB `righttenantry_test`).
- Gitignored `server/.env` copy (PORT=4101, DATABASE_URL→local, external services blanked, Supabase GoTrue kept).
- `make build` from the worktree (server built; pre-existing unused-import warnings only). Server live on `:4101`.
- Seeded the 5-app fixture via the round-1 seed script (my own copy in /tmp/refcheck-bughunt2/) — 5 applications
  through the real multipart `/apply/:code` form, PATCH-walked to `viewed`, per-scenario call states via SQL.
  Verified all 10 reference_call rows (renders in-flight/queued, correct awaiting_correction, substitute objected,
  export 2-attempt in-flight, form-complete token live).

## 01:00–01:10 — Phase 1: suite re-creation + regression run (5 scenarios)
- Authored all 5 scenarios at `.pi/skills/bug-hunt/scenarios/reference_checks/` with the round-1 lessons
  embedded (scoped selectors, timing gates, native `.click()` fallback, clipboard stub).
- **panel-renders PASS** — 2 rows, correct pills ("Invitation sent"/"Queued"), attempt log renders on expand.
  Found: the "Attempt log" title is CSS-uppercased → innerText "ATTEMPT LOG" (scenario fix).
- **panel-correct PASS** — awaiting_correction amber pill → Correct details trio → typed email **held at +2s**
  (#611 regression proof) → Save & resend → toast → pill flips to Queued; DB `queued | new.employer.ref@fixture.test |
  correction_cycles=1`. Found: toasts render `role="status"` + `data-testid="toast-message"`, NOT `[role=alert]`
  (skill-doc drift); corrected email is not re-displayed in the queued row body (DB is the persistence proof).
- **panel-substitute PASS** — objected pill → Substitute trio **starts EMPTY** (r4 N18) → all three fields held
  at +2s → Save & send invite → 3 rows, new "FIXTURE New Sub Referee — Queued"; DB shows the new
  `queued | substituted_at=t` row while the old objected row stays terminal.
- **panel-export PASS** — 2-attempt in-flight row → export with clipboard stub → 156-char payload
  (`Invitation sent (email + SMS)` batch-merged), toast "Attempt log copied…" (dash-free #612 copy).
- **referee-form-complete PASS** — drove /reference/:token: landing → start → identity (Yes) → 10 answers
  (radios, tenancy from+ongoing, rent amount, free text) → review (11 rows) → 3s → submit → thank-you;
  DB `form_completed | form_completed`. Two execution discoveries: (a) desktop `data-current` NEVER advances in
  place — the JS `showOnly` stepper is mobile-only; id-scoped `[data-question="<id>"]` continues are the
  correct pattern; (b) `a_tenancy_from` (YYYY-MM) is required even when "ongoing" is set (a 400 surfaced this;
  the inline error "This one needs an answer to continue." rendered correctly).

## 01:10–01:20 — Phase 2: expanded hunt (new probes)
- **Invalid token**: 404 card, no validity leak. PASS (designed).
- **Expired token + resend**: "This link has expired." → resend → honest-failure page with Resend blanked,
  brand-voice copy. PASS (designed).
- **Decline / stop / wrong-person**: all three exit flows drive cleanly; DB `refused` /
  `objected+objection_web` / `awaiting_correction+contact_invalid`. PASS (designed).
- **Double-submit on Start-confirm**: busy guard held; exactly 1 attempt after one manual sweep tick
  (the sweep is Cloud-Scheduler-driven in prod; fired manually via the INTERNAL_SECRET-gated endpoint here).
- **Unicode/long/emoji trio (191-char name)**: held at +2s, saved, rendered. PASS. A re-substitute of an
  already-replaced row 409s with the generic "has moved on" toast — designed (r2 W7).
- **Mobile 375px**: document has no horizontal scroll; the long-name breadcrumb overhang is a scrollable
  `overflow-x-auto` trail (scrollWidth 436 > clientWidth 343) — FALSE POSITIVE, not a bug.
- **"Viewing held" sweep (W1)**: 0 stray "Viewed" on leaderboard/detail/stepper/audit. PASS.
- **#619 metadata**: `/guides/rtb-registration` title + description verbatim. PASS.
- **Take-over queued row → export (RC4.4 W4)**: log + export render on taken-over queued rows. PASS.
- **Cadence boundary (4 batches)**: pill "Reminder sent", no hint, 4 correctly-labeled log lines. PASS.
- **Completed-row expansion**: full key-facts summary + free-text + export. PASS (initial "empty body" was my
  own click no-op — the agent-browser trap, not an app bug).
- **Empty-attempts contact_initiated row**: renders gracefully. PASS.
- **taken-over-reminder-hint — BUG**: taken-over `contact_initiated` row STILL shows
  "Next reminder in ~2 days if there's no reply" while the sweep excludes taken-over rows
  (`sweep_due_reference_calls.sql` `taken_over_at IS NULL`). Filed **#621** (priority:low) with screenshot
  (bug-hunt-screenshots release) + scenario `taken-over-reminder-hint.yaml`.

## 01:20–01:30 — Clean re-run (re-migrated DB, fresh fixture)
- `reset-test-db.sh` + fresh seed (new vacancy `963777d95b46`, fresh form token). Server restarted (stale pool).
- Re-ran all 6 scenarios against the fixed YAMLs:
  - panel-renders PASS, panel-correct PASS (toast selector verified), panel-substitute PASS,
    panel-export PASS, referee-form-complete PASS (id-scoped continues; thank-you + `form_completed`).
  - taken-over-reminder-hint **FAIL as designed** — bug #621 re-confirmed on the clean fixture
    (taken-over row innerText contains the reminder promise).
- Scenario YAML fixes applied (suite-artifact; listed in the report).

## 01:30 — Close-out
- Suite + seed script preserved at `_bmad-output/implementation-artifacts/bug-hunt-suites/reference_checks/`.
- Report + this runlog at `_bmad-output/implementation-artifacts/refcheck-bughunt2-{report,runlog}.md`.
- Field-notes shard written. Branch committed + pushed (`rt-refcheck-bughunt2`); **no PR** (Perkins 0).
- No-PR completion signal fired.

## Fixture state left behind (local sandbox only)
- Vacancy `Refcheck Verification Flat` (short_code `963777d95b46`), 5 fixture applications + reference calls,
  in container `rt-refcheck-bughunt2-dev-db` (port 54337). Server on `:4101`.
- `server/.env` is a gitignored copy — safe to leave; harmless to remove.
