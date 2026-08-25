# Bug Hunt Report — reference_checks (round 2, on clean develop)

- **Job:** `righttenantry-refcheck-bughunt2`
- **Base:** `develop` @ `7675c81` (post-#620, the #619 SEO metadata merge) — repo otherwise quiet
- **Sandbox:** local Docker Postgres (`rt-refcheck-bughunt2-dev-db`, port 54337) + server on `:4101`
  (gitignored `server/.env` copy — Resend/Twilio/Stripe/AI/PostHog blanked; Supabase GoTrue kept for login)
- **Run at:** 2026-08-15, 00:5x–01:2x local
- **Result:** **5/5 regression scenarios PASS** (round-1 verification re-applied and held), **1 NEW bug filed** (#621)
- **Perkins:** `pr_review: 0` — no PR. Deliverables: this report + runlog + preserved suite + issues.

## Summary

| # | Scenario | Result | Notes |
|---|----------|--------|-------|
| 1 | `panel-renders` | **PASS** | card/rows/pills/attempt-log all render; 2 YAML fixes applied (see below) |
| 2 | `panel-correct` | **PASS** | #611 keystroke-hold + save-persists re-verified live; DB `queued \| corrected_email \| correction_cycles=1` |
| 3 | `panel-substitute` | **PASS** | #611 substitute flow re-verified; new row + terminal old row confirmed at DB |
| 4 | `panel-export` | **PASS** | #615 toast-over-banner + RC4.4 export; 156-char payload; dash-free copy |
| 5 | `referee-form-complete` | **PASS** | full 11-question walk → review → submit → thank-you; `form_completed` at DB |
| 6 | `taken-over-reminder-hint` | **FAIL** | **NEW BUG — filed as #621** |

## Issues filed

### #621 — taken-over reference row still promises a "Next reminder" that will never arrive (priority:low)

The reference panel's attempt-log cadence hint keys only on `status == ContactInitiated` and ignores the
taken-over flag (`client/src/components/reference_panel.gleam` `view_attempt_log` → `has_next_reminder`).
After the landlord takes over a `contact_initiated` check ("You're handling this one — automated messages
stopped"), the row still renders **"Next reminder in ~2 days if there's no reply"** — but the sweep that
would send that reminder explicitly excludes taken-over rows (`sweep_due_reference_calls.sql`: `AND
rc.taken_over_at IS NULL`). The hint is a promise the system cannot keep.

- **Severity:** low (misleading state copy; no data/consent/money impact). Genuine survivor — round 1 never
  exercised takeover × cadence-hint.
- **Repro:** fixture app → employer_ref `contact_initiated` with 1 attempt → expand → overflow → Take over
  manually → confirm → hint persists. Verified twice (pre-fix-layout run + clean re-seeded run).
- **Evidence:** DOM geometry (taken-over row innerText contains both the takeover label and the reminder
  hint) + screenshot uploaded to the bug-hunt-screenshots release (embedded in the issue).
- **Scenario:** `reference_checks/taken-over-reminder-hint.yaml` — drives the exact flow and fails on
  current develop. Suggested fix for the bosses: gate `has_next_reminder` on the taken-over flag
  (`ContactInitiated if not taken_over(call)`).

## Probed, NOT bugs (documented so round 3 doesn't re-file)

| Probe | Result |
|-------|--------|
| Invalid form token | 404 card "This link doesn't look right." — never reveals token validity. Designed. |
| Expired token + resend | "This link has expired." + resend form; with Resend blanked the honest-failure page renders ("Couldn't send the link…") with brand-voice copy. Correct degraded behavior. |
| Decline flow | decline page → Confirm decline → "Understood."; DB `refused` + terminalized. |
| Stop flow (Art 21) | stop page → Confirm stop → "Done."; DB `objected` + `terminal_reason=objection_web`. |
| Wrong-person flow | "Not the right person?" → "Let us know" → DB `awaiting_correction` + `contact_invalid` — coherent with the correct-details surface. |
| Re-substitute an already-replaced row | 409 → generic "That reference has moved on since you looked. Refresh…" toast. Designed (r2 W7 — never silently drop). |
| Rapid double-click on Start-confirm | Busy guard held — exactly 1 invite after one sweep tick. No double-send. |
| Unicode/emoji/long inputs (191-char name) in substitute trio | Held at +2s; persisted; rendered. No truncation issues. |
| Mobile 375px breadcrumb with long name | Overhang measured, but the OL is `overflow-x-auto` scrollable (scrollWidth 436 > clientWidth 343) — standard mobile pattern, NOT clipping. False positive. |
| "Viewing held" copy sweep (advisory W1) | 0 stray "Viewed"/"VIEWED" on leaderboard + detail + stepper + audit trail; 5× "Viewing held". Clean. |
| #619 SEO metadata | `/guides/rtb-registration` renders the verbatim title + meta description. Live. |
| Taken-over queued row export affordance (RC4.4 W4) | Renders attempt log + export on taken-over queued rows. Holds. |
| Cadence boundary (4 batches) | Pill flips to "Reminder sent", hint disappears, log shows all 4 batches (co-nudge correctly labeled "Applicant asked to nudge"). Correct. |
| Completed-row expansion | Full key-facts summary + free-text block + export render on `form_completed`. Correct. |
| Empty-attempts `contact_initiated` row | Renders gracefully (correction event only + "Next reminder" hint). Correct. |
| Reference-form timing gate | Sub-500ms answers silently drop with a fake advance (AD-15 abuse posture) — designed; bots learn nothing. |
| Reference-form completion re-open | "This reference was already completed." terminal state; no re-submit path. Designed. |

## Scenario-suite fixes (suite-artifact, round-1 convention)

- `panel-renders`: "Attempt log" asserts as rendered text **"ATTEMPT LOG"** — the title is CSS-uppercased
  (`uppercase tracking-widest`), so `document.body.innerText.includes("Attempt log")` is false.
- `panel-correct` / `panel-substitute`: added the row **expand** step before opening the correct/substitute
  trio (the affordance lives in the row detail); toast assertions now poll
  `[data-testid="toast-message"]` (toasts render with `role="status"`, NOT `role="alert"` — the skill
  guide's `[role=alert]` is stale); panel-correct's final check is the Queued pill (the corrected email is
  proven at the DB layer, not re-displayed in the queued row body).
- `panel-export`: toast selector fix; payload channel check is `/SMS/i` (uppercase in the batch-merged line).
- `referee-form-complete`: continues are **id-scoped** to `[data-question="<id>"]` (desktop `data-current`
  never advances in place — the JS `showOnly` stepper is mobile-only); `a_tenancy_from` (YYYY-MM) is
  required even when "ongoing" is checked; rent-amount input testid is `reference-input-a_rent_amount`.
- `panel-substitute`: final pill assertion scoped to the row carrying the new referee name (two
  landlord_ref rows share the slot testid after substitution).

## Smells & untested gaps

- **Skill-doc drift (not an app bug):** the bug-hunt SKILL.md / verification guide document toasts under
  `[role=alert]`; the app renders them with `role="status"` + `data-testid="toast-message"`. Scenarios and
  the doc disagree; the skill doc should be updated.
- **Sweep-not-running-in-sandbox:** the RC3.5 cadence sweep is Cloud-Scheduler-driven; the local sandbox
  must fire it via `POST /api/v1/internal/reference-checks` (INTERNAL_SECRET). Documented in the runlog;
  fixtures re-arm rows (`next_attempt_at = now()`) so one manual tick sends everything due.
- **Untested (needs infra or sacrificial accounts):** session expiry mid-form, real outbound email delivery
  (Resend/Twilio blanked in sandbox), real GoTrue token rotation, multi-landlord cross-session concurrency
  on the same application, the 20-vacancy cap + free-tier counter edges (outside reference_checks scope).
- **Note on #617/#568 (analytics attribution) and #587 (auto-reminder):** not touched; no duplicates filed.

## Verdict

Round-1's five scenarios re-created, fixed, and re-run as a regression gate: **all five hold on develop
@ 7675c81** — no regressions from the #610/#612/#616/#618/#619 line. The expanded hunt found **one genuine
survivor (#621: taken-over reminder hint)**, plus a batch of probed-not-bugs documented above so round 3
doesn't re-hunt them.
