# Verification Report — refcheck fixes #611 / #612 / #613 / #615 (re-run)

- **Job:** `righttenantry-refcheck-verification-rerun` (RESPAWN of `righttenantry-refcheck-local-test`)
- **Base verified:** `develop` @ `ce999eb` — the full fix line merged: #610, #612, #616, #618
- **Sandbox:** local Docker Postgres (`rt-refcheck-verification-rerun-dev-db`, port 54335) + server on `:4100`
  (gitignored `server/.env` copy — Resend/Twilio/Stripe/AI blanked; GoTrue auth via Supabase as-is)
- **Run at:** 2026-08-14, 19:01–20:2x
- **Result:** **4/4 fix areas PASS** — no regressions, no new bugs surfaced

## Summary table

| # | Fix area | PR | Result | Evidence |
|---|----------|-----|--------|----------|
| #611 | edit-trio keystrokes keyed by `reference_call_id` | #616 | **PASS** | live keystroke-hold ×2 (correct + substitute), DB persisted NEW contact, client pin test green |
| #612 | em-dash exemptions removed | #614 | **PASS** | lint clean (125 files), zero em-dashes in shipped copy strings, live toast copy dash-free |
| #613 | "Viewing held" stepper label | #618 | **PASS** | every user-facing surface live-verified, zero stray "Viewed" labels, trigger still fires on viewed |
| #615 | toast visible during consent window | #618 | **PASS** | DOM geometry + screenshot: toast z 2147483001 > banner 2147483000, no overlap, success toast path proven |

## #611 — edit-trio keystrokes (stale-save fix) — PASS

**What was re-verified:** the correct-details AND substitute edit-trio inputs are keyed by
`reference_call_id` (stable), not ref slot — typed edits survive re-render and Save persists the
NEW contact, never the stale one.

**Fixture:** 5 applications seeded through the REAL `/apply/:code` form (multipart + PDFs,
unique emails, timing-honest `_form_loaded_at`), walked to `viewed` via PATCH (the RC2.3 trigger
minted `landlord_ref` + `employer_ref` calls per app), then per-scenario call states set via SQL.

**Live proof (panel-correct):**
1. Opened `RefcheckCorrect Fixture` → employer_ref in `awaiting_correction` (amber pill
   "Contact details didn't work" + "Correct details" button).
2. Typed `new.employer.ref@fixture.test` into the trio → **value held at +2s and +4s** (the
   original bug snapped back within ~150ms on every render).
3. Save & resend → **DB: `status=queued`, `corrected_email=new.employer.ref@fixture.test`,
   `correction_cycles=1`** — the NEW contact persisted. (Original bug: OLD contact persisted
   with a success toast while `correction_cycles` incremented.)
4. Re-armed `awaiting_correction`, repeated with `typed.new@fixture.test` → held again, saved →
   DB `corrected_email=typed.new@fixture.test`. Reproduced twice, both passed.

**Live proof (panel-substitute):**
1. Opened `RefcheckSubstitute Fixture` → landlord_ref terminal `objected` ("Declined contact"
   pill + "Substitute referee" button).
2. Typed `FIXTURE New Sub Referee` / `new.sub@fixture.test` / `0879998888` → **all three held
   at +2s**.
3. Save & send invite → **DB: NEW `landlord_ref` row created (`queued`,
   `contact_name='FIXTURE New Sub Referee'`, `contact_email='new.sub@fixture.test'`,
   `substituted_at` set) while the old objected row stays terminal.** Panel shows the new
   "FIXTURE New Sub Referee — Queued" row.
   (Original bug: substitute could never submit a new referee at all.)

**Pin test:** `refcheck_trio_keystroke_lands_in_field_test` present and green — client suite
576 passed, 0 failures (includes the negative-control that reverting the fix makes red).

**Code-level confirmation:** `client/src/components/reference_panel.gleam` `view_edit_trio`
passes `call.reference_call_id` as the trio inputs' message key at all three call sites
(lines 1110/1117/1124); testids stay slot-based per the PR's note.

## #612 — em-dash exemptions removed — PASS

**What was re-verified:** the `SPEC_VERBATIM_OWNERS` exemption mechanism is gone and no
user-facing string ships an em-dash (U+2014).

- `scripts/lint_em_dash.py` — **clean, 125 files scanned** (the authoritative scan; the
  docstring confirms the former owner-name exemption list is removed — the only remaining
  carve-out is developer-facing log/telemetry args).
- Grepped every copy surface for em-dashes in string VALUES (comments excluded):
  `client/src/copy.gleam`, `server/src/reference_checks/form_copy.gleam`,
  `server/src/application/form_copy.gleam`, `application_detail_handler.gleam`,
  `status_stepper.gleam`, `status_pill.gleam`, `toast.gleam` — **zero em-dashes in shipped
  strings**. The single remaining U+2014 in `application_detail_handler.gleam:667` is a
  `wisp.log_error` server-log line (never user-facing; the user-facing error is
  "Failed to read current status", dash-free).
- **Live:** the OQ-5 export toast rendered as "Attempt log copied. Paste it into your
  records or a message." and the viewed-stop hint rendered "Mark when you've carried out the
  viewing. Reference checks start here." — both #612-listed strings, both dash-free.
- Server unit tests green: **1512 passed, 0 failures** (refcheck copy tests included).

## #613 — "Viewing held" stepper label — PASS

**What was re-verified:** the `viewed` status renders the unambiguous label on EVERY
user-facing surface; no stray user-facing "Viewed" label survives; marking a viewing still
triggers the reference calls.

| Surface | Result |
|---------|--------|
| Stepper stop (current + non-current) | "Viewing held" (vision + DOM verified) |
| `label_for_slug_opt` table → backward-confirm modal | "Move RefcheckRenders Fixture back to **Viewing held**?" (live) |
| Audit trail cards | "Moved to Viewing held" (live, ×2 entries) |
| Shared status pill (leaderboard rows) | "Viewing held" on all 5 fixture rows (live) |
| Detail-page uppercase pill | "VIEWING HELD" (vision-verified on screenshot) |
| Native `title` hint on viewed stop (non-current) | `Mark when you've carried out the viewing. Reference checks start here.` (live; omitted when current per spec) |
| Stray "Viewed"/"VIEWED" user-facing labels | **0** (DOM scan on detail + leaderboard) |
| Reference-check trigger on viewed transition | Calls minted for all 5 fixture apps on the `viewed` walk; re-transition approved→viewed re-ran the idempotent trigger (no error) |

Stepper flow exercised live: `viewed → approved → viewed → shortlisted` with the
backward-confirm modal at each backward step. The longer label's layout (leaderboard track
widened, `whitespace-nowrap`) holds — no overflow observed at 1280px.

## #615 — toast visibility during the consent window — PASS

**What was re-verified:** the toast stack moved top-right below the header
(`fixed top-20 right-4 z-[2147483001]`), one z-step above the consent banner
(`2147483000`); the banner stays visible + clickable.

**Live DOM geometry eval (consent banner up, success toast fired):**
```json
{"toastText":"✓ | Attempt log copied. Paste it into your records or a message. | ✕",
 "toastVisible":true,
 "toastBox":{"top":80,"bottom":152},          // top-right below the in-flow header
 "toastZ":"2147483001",
 "bannerZ":"2147483000",
 "toastOverlapsBanner":false}
```
- Success path proven by stubbing `navigator.clipboard.writeText` (headless has no clipboard
  permission — the un-stubbed path fires the failure toast, which is also a valid visibility
  proof; the success toast text + 156-char clipboard payload confirm the real export ran).
- Banner still up and interactive during the toast (no dismiss, no re-layer).
- Screenshot `615-toast-visible-over-banner.png` (vision-verified): toast card top-right,
  consent banner bottom, no overlap.
- The 320×480 corner trade-off is NOT re-litigated (user-approved in the original evidence).

## Scenario suite re-application

The `reference_checks` suite was re-created from `SKILL.md` + `guides/scenario-format.md` at
`.pi/skills/bug-hunt/scenarios/reference_checks/` (5 scenarios — `panel-renders`,
`panel-correct`, `panel-substitute`, `panel-export`, `referee-form-complete`), applying the
original hunt's field-note lessons: scoped `[data-question]` selectors (stacked-forms trap),
timing gates (sleep before submits, reload-don't-retry), and the fixture protocol
(unique-email resolution, `--no-sweep` style future `next_attempt_at`). The fixture itself is
`/tmp/refcheck-verification-rerun/seed-refcheck-fixture.py` (local sandbox tooling — not a
repo deliverable, matching the original's untracked status).

## Verdict

**All four merged fixes hold on `develop` @ ce999eb.** No regressions found, no new bugs
surfaced, no issues filed. The fixes are safe to carry forward.
