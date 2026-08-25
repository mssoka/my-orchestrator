# Running Log — righttenantry-refcheck-verification-rerun

Chronological log of the verification re-run (2026-08-14). All times local.

## 19:55 — Boot & recon
- Worktree confirmed at `ce999eb` (develop HEAD, the full fix line: #610/#612/#616/#618 merged).
- Read the original hunt's field-notes shard (`righttenantry-refcheck-local-test.md`) — the
  stacked-forms, timing-gate, and sandbox lessons are load-bearing.
- Confirmed `reference_checks` scenario suite absent (untracked, swept) — re-creation required.
- Read issues #611/#612/#613/#615 + PRs #616/#618 for the exact fix specs.
- Static on-disk confirmation of all four fixes before any browser work:
  - #611: `view_edit_trio` passes `call.reference_call_id` at all 3 `text_input` sites.
  - #612: `lint_em_dash.py` clean (125 files); no em-dashes in `copy.gleam` string values.
  - #613: "Viewing held" in stepper/pill/leaderboard; no stray "Viewed".
  - #615: toast at `fixed top-20 right-4 z-[2147483001]`.

## 19:56–20:02 — Sandbox bring-up
- Started `rt-refcheck-verification-rerun-dev-db` (Postgres 16-alpine, port 54335 — free).
- Applied the full migration chain via `reset-test-db.sh` pointed at the container.
- Wrote gitignored `server/.env` (DATABASE_URL → local Postgres, PORT=4100, ENV=development,
  Resend/Twilio/Stripe/AI/PostHog/Meta/Sentry blanked; SUPABASE GoTrue + SECRET keys kept).
- `make build-client` (bundle built, PostHog key injected from root .env), server compiled
  (one pre-existing unused-import warning), server live on :4100 with all external services
  disabled.

## 20:03–20:07 — Fixture authoring + seeding
- Mapped the API contracts: login (JSON → session + csrf cookies), vacancy create
  (`status: "active"`, lowercase property_type), status update is **PATCH**
  (`/api/v1/vacancies/:id/applications/:id/status` — the first fixture attempt used POST and
  404'd; fixed), apply form is **multipart** (415 on urlencoded — fixed with a multipart
  builder + reportlab PDFs for the mandatory landlord/employer ref docs).
- `seed-refcheck-fixture.py` (in /tmp): login → vacancy "Refcheck Verification Flat" →
  5 applications submitted via the real form (unique emails `refcheck-<tag>-<hex>@fixture.test`,
  `_form_loaded_at` 5s in the past) → resolved each by ITS OWN email → PATCH walk to
  `viewed` (RC2.3 trigger minted landlord_ref + employer_ref per app) → SQL state setup per
  scenario (awaiting_correction / objected / in-flight×2 / form_token).
- Verified all 10 reference_call rows in the expected states.

## 20:07–20:12 — #615 verification (browser, consent banner up)
- Logged in via agent-browser (dedicated `--session refcheck-verification-rerun` — the
  default session is shared machine-wide). Confirmed `#rt-consent-banner` up, no consent
  choice.
- Open export app → expanded employer_ref (in-flight, 2 attempts) → clicked Export with
  clipboard stubbed → measured: **toast visible, z 2147483001, banner z 2147483000,
  toastOverlapsBanner false**. Success toast text + 156-char clipboard payload confirmed.
- Screenshot captured (vision-verified: toast top-right, banner bottom, no overlap).

## 20:12–20:15 — #613 verification
- Detail page: stepper shows ✓Submitted → ✓Reviewing → ✓Shortlisted → **Viewing held** →
  Approved; 3× "Viewing held" on page, 0 stray "Viewed".
- Leaderboard: shared pill "Viewing held" on all 5 rows, 0 stray.
- Stepper walk: viewed → approved (confirm modal) → back to viewed (modal:
  "Move RefcheckRenders Fixture back to **Viewing held**?") → back to shortlisted. Audit
  trail logged "Moved to Viewing held" both times.
- Viewed-stop title hint when non-current: "Mark when you've carried out the viewing.
  Reference checks start here."
- Note: `agent-browser click @ref` silently no-ops on Lustre buttons (the Rule-7 / field-notes
  trap) — used the native `.click()` eval fallback throughout; both refs and eval worked for
  the stepper tabs once the right element was targeted.

## 20:15–20:20 — #611 verification (both surfaces)
- panel-correct: awaiting_correction row → Correct details → typed new email → **held at
  +2s/+4s** (×2 runs) → Save → DB `queued | <new email> | correction_cycles=1`.
- panel-substitute: objected row → Substitute referee → typed all 3 fields → **all held** →
  Save & send invite → DB shows a NEW queued landlord_ref row with the typed contact
  (`substituted_at` set), old objected row untouched; panel shows the third row.
- Screenshots: `611-panel-correct-keystrokes-hold.png` (trio open, typed email in field),
  `611-panel-substitute-new-row.png` (3 rows incl. "FIXTURE New Sub Referee — Queued").

## 20:20–20:26 — referee-form-complete + #612
- Read the live form token from the fixture report; drove `/reference/:token` in a fresh
  session: identity → all 10 answer questions (radios/month/rent/free_text) → scoped
  per-question Continues → review screen → slept 3s → "Send my reference" →
  "Thank you. That's everything." DB: landlord_ref `form_completed`, outcome set, result
  payload present. (The eval loop died on the final navigation — expected, the page
  redirected to the review screen.)
- #612: lint clean (125 files); grepped all copy sources for em-dashes in string values —
  zero; the one remaining U+2014 is a server log line. Live toast + hint copy dash-free.

## 20:26 — Test suites + close-out
- Server unit tests: **1512 passed, 0 failures** (541 skipped — integration).
- Client tests: **576 passed, 0 failures** (incl. the #611 trio keystroke pin test).
- Evidence + report written to `_bmad-output/implementation-artifacts/refcheck-verification-rerun-*`.
- Scenario suite re-created at `.pi/skills/bug-hunt/scenarios/reference_checks/` (5 scenarios).
- No PR (verification job); no commits made; worktree clean of tracked changes.

## Fixture state left behind (local sandbox only)
- Vacancy `Refcheck Verification Flat` (short_code in `/tmp/refcheck-fixture-report.json`),
  5 fixture applications, 10 reference calls — all in the Docker container
  `rt-refcheck-verification-rerun-dev-db` (port 54335). Server on :4100.
- Sandbox `server/.env` is a gitignored copy — safe to leave; harmless to remove.
