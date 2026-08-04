# Application-Form Completion: Pre-Deploy Baseline (2026-08-04)

*Snapshot frozen before the upgraded form deploys. The "before" number for the 13/08 retro. Sources: production DB (read-only via deployment/db.sh) + PostHog EU project 173329.*

## The vacancy

| Field | Value |
|---|---|
| Property | 70 Meadowgate |
| Vacancy ID | `3a548801-5a82-421b-8faa-1a6fbc31ad7f` |
| Status | Closed (auto-closed; closes_at was 2026-08-13) |
| Listing source | Daft.ie (sole source) |

## The funnel (best available data)

| Stage | Count | Source | Note |
|---|---|---|---|
| 📧 Daft enquiries (tracked) | 66 | `inbound_email_sender_state` view | Tracking began ~Jul 1 (#556 migration); pre-July enquiries invisible |
| 📝 Applications submitted | 8 | `application` table (all have `submitted_ip_text` = real submissions) | Span May 29 – Jul 15; all later `auto_closed` by the vacancy-close sweep |
| ❌ Email overlap (enquiries ∩ applications) | **0** | Cross-join query | Applications predate the tracking view; same daft source, timing gap |
| 📊 Completion rate | **~11%** (8 of ≥74 known) | Derived | True denominator is unknown (early enquiries untracked) |

## Why the "66 → 8" was never a real funnel

The `inbound_email_sender_state` view was created by the #556 reminder-series migration (~July 1). The 8 applicants started arriving May 29 — five weeks before tracking existed. Their enquiry emails were never backfilled into the view, so the cross-reference returns zero matches. **The 66 and the 8 are from the same daft source but different time windows** — not two independent cohorts.

## What this means

1. The 66 ARE real, unconverted daft leads (enquired post-July, never applied) — the re-activation email targets them correctly.
2. The true enquiry count is higher than 66 (May–June enquiries are invisible).
3. The "before" completion rate is ~11% at best estimate — the real number could be lower (if the invisible enquiries push the denominator up).

## The "after" measurement (starts at deploy)

The upgraded form (stepper + instrumentation + save-resume + attestation) carries PostHog events that fire from the first applicant:
- `application_form_section_entered` / `_completed` per `data-section-id` — per-section drop-off
- `application_confirmation_viewed` — real submit count (deduped)
- `application_form_section_abandoned` — best-effort unload exit

Consent rate: **92%** (327 opt-ins / 356 pageviews over 30d) — the data will be reliable.

## The new vacancy

| Field | Value |
|---|---|
| Vacancy ID | `72a0c549-a3f9-4b97-8f7c-c4955d0eff73` |
| Status | Active |
| Closes | 2026-09-03 |
| Applications | 0 (clean cohort — no blind spots from day one) |

The retro compares: **this baseline (~11%, imprecise)** vs **new-vacancy PostHog funnel (precise, per-section)**.
