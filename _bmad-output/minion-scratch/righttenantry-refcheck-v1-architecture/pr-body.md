## Summary

v1 feature architecture for AI reference-checking (landlord-facing, written-first, no voice) as a **new addendum** to the canonical `architecture.md`. Closes the design side of #548's v1 scope per the 2026-07-29 gate amendment. Planning artifact only — no code changes.

**Artifact:** `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`

16 architecture decisions (AD-1…AD-16) covering: `reference_call` table + full lifecycle enum (voice states v2-reserved), `reference_contact_attestation` as a new `record_type` on `acknowledgement_record`, tokenized referee form at `/reference/:token` (dsar/erase capability-token pattern), the T0→T+144h contact cadence swept by a Cloud Run Job, objection/STOP short-circuit with a durable `reference_objection_log`, one-cycle applicant-correction loop, Wizard-of-Oz `channel: "manual"`, honestly-scoped fraud signals, landlord display data contract with server-computed hooks, and the v5 `reference_call_results[]` re-score field as design-only forward contract.

## Decisions & rationale

Load-bearing calls a fresh reviewer should not re-litigate:

- **Acknowledgement, never consent.** Attestation rides `acknowledgement_record` (the `guarantor_attestation` precedent); lawful basis stays Art 6(1)(f). The 2026-04-22 rename repudiated consent-as-basis; Perkins r1 already corrected this once. (AD-2)
- **Lifecycle enum is the full heist-535 superset**, voice states inert but present — v2 adds no enum churn and no semantic re-interpretation of v1 rows. (AD-1)
- **The sweep owns every send, including T0**; all transitions are guarded UPDATEs with sticky terminals and atomic attempt-log appends (repo precedent: `claim_shortlist_notification.sql`). Added at gate review — seven writers touch one row. (AD-14)
- **Corrected contacts live in `corrected_email/phone`**; the `contact_*` snapshot is immutable. Fraud joins and sends use the *effective* contact. (AD-7)
- **Wizard-of-Oz is in v1** with `channel: "manual"` — the gate amendment makes v1 the cohort pitch-test delivery vehicle; recording founder calls as `"form"` would corrupt funnel metrics. (AD-8)
- **Fraud v1 honestly scoped:** pure-DB reuse signals + Twilio line-type + `form_session` (completion time, IP/UA match). Added applicant-submission IP/UA capture (two bounded columns) — the comparator did not exist anywhere in the schema; Art 13 notice update flagged for counsel. Geo/fingerprint/coached-score deferred with null/unknown contract. (AD-10)
- **RLS: no policies written** — repo convention is service-role-only + auto-enabled RLS (`20260512175704`); the addendum says so rather than inventing a divergent posture. (§4.4)
- **Scheduled work = Cloud Scheduler → Cloud Run Job** (terraform + docker-entrypoint); the shared-secret HTTP route is manual-fire only. Gate review caught the briefing-era misdescription of the house pattern. (§5.4)
- **Amendments to heist-535 explicitly registered** (§6.4): `channel` +"manual", `outcome` +"unreachable"/"form_completed"/"manual_recorded", fraud flag `referee_contact_invalid` supersedes `referee_number_wrong` — so the v2 consumer team amends their copy instead of discovering drift.
- **Objection evidence written at objection time** to FK-free `reference_objection_log` — survives CASCADE, single owner, no erasure-time snapshot step. (§9.2)

- **Landlord-facing validity note (§9.5, added in human review):** every written-channel result carries a server-rendered `display_disclaimer` — written response ≠ verbal confirmation; the landlord should still endeavour to call the referee — worded as provenance framing, never invalidating (the feature stands by its collection + fraud screening). `ai_disclaimer` precedent; per-channel (voice downgrades it in v2).

**Rejected alternatives** are recorded per-AD in the artifact (one-time burn tokens, referee accounts, email-only v1, v1-slim schema, landlord-side correction, trigger-on-submission, LLM summarisation in v1, and more).

**Flagged for legal review (launch-gating, not build-gating):** §11 Q5 counsel pack — Annex III 5(b)/Art 6(3) memo, Art 14 notice + LIA wording, controller/processor map, Art 13 update for the new IP/UA capture, `attestation_on_file: false` display posture. §11 Q4 — referee free-text display with "unmoderated" affordance.

## Review process

Built with `bmad-architecture` (headless run): repo recon → memlog → draft → reviewer gate (deterministic lint clean; two independent review lenses — rubric/adversary + codebase reality-check — as parallel subagents). Gate found 3 high + 2 medium holes (status↔outcome mapping, immutable-snapshot vs correction-loop, mutation-ownership, fraud-signal collectibility, webhook/security envelope) plus factual corrections; all amendments applied and recorded in the memlog.

## Open questions (in the artifact, §11)

1. ComReg SMS Sender-ID registration — lead time/owner; **hard launch dependency** for the SMS leg.
2. Twilio account/IE number provisioning (billing owner).
3. Inbound SMS webhook included in v1 as designed — flagged for review.
4. Free-text display posture (counsel).
5. Counsel pack (counsel; launch-gating).

## Verification

`git diff --stat` shows only the new artifact; internal doc links resolve; markdown + mermaid render; no code files touched.

🤖 Generated with [pi](https://github.com/earendil-works/pi-coding-agent) (bmad-architecture minion)
