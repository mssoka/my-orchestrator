---
title: "Epics & Stories: AI Reference-Checking v1 (written-first, no voice)"
status: draft
date: 2026-07-30
altitude: feature
addendum_to: _bmad-output/planning-artifacts/epics.md
github_issue: 548
author: Moses + epics minion (bmad-create-epics-and-stories, orchestrated run)
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics', 'step-03-create-stories', 'step-04-final-validation']
inputDocuments:
  - '_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md'
  - '_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md'
  - '_bmad-output/planning-artifacts/refcheck-pitch-copy-deck-2026-07-29.md'
  - '_bmad-output/planning-artifacts/epics.md'
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/planning-artifacts/architecture.md'
  - 'GitHub issue #548 (+ 2026-07-29 gate amendment)'
---

# RightTenantry — Epic Breakdown: AI Reference-Checking v1

## Overview

This document is the **feature-specific epic and story breakdown** for AI
reference-checking v1 (landlord-facing, written-first, no voice), decomposing the
requirements fixed by the [feature architecture](architecture-reference-checking-v1-2026-07-29.md)
(16 ADs — the data contract) and the [UX design](ux-reference-checking-v1-2026-07-29.md)
(the flows + §15 decisions record) into implementable, individually dispatchable stories.

It is an **addendum to the canonical [epics.md](epics.md)** — it follows that document's
conventions (DB-to-UI vertical slices, Given/When/Then acceptance criteria, theme/design
baked into every UI story) and does not rewrite it. Canonical epics 1–9 stand unchanged.
Requirement IDs use the `RC` prefix so they never collide with canonical FR/NFR/AR/UX-DR
numbering.

**Scope (decided upstream — issue #548, 2026-07-29 gate amendment — not re-litigated):**
v1 lands entirely in this repo. Reference capture + `reference_contact_attestation`;
written-first collection (capability-token form, email + SMS, T0→T+144h cadence sweep,
objection/STOP short-circuit, one-cycle correction loop); `reference_call` lifecycle +
landlord reference panel (status, structured summary, fraud signals, attempt log, warm
handoff, §9.5 `display_disclaimer`); WoZ `channel: "manual"`; form-channel fraud signals.
No voice, no Twilio telephony calls, no RightTenantryAgents changes; the v5 re-score field
is a documented forward contract only (AD-12).

## Amendments Register (decisions applied on top of the design docs)

The 2026-07-30 clarify round (answered 2026-07-31, Moses) resolved contradictions between the
feature architecture and the UX spec, plus one new directive. Each amendment records what
changes, where the originals disagree, and why. These bind every story below; a future
reconciliation pass should fold them back into the architecture addendum (its §6.4 register
pattern) and the UX spec.

| # | Amendment | Supersedes | Rationale |
|---|---|---|---|
| A1 | **Correction & substitution are landlord-driven**: the landlord contacts the applicant, edits the slot's trio inline (audit-logged), re-triggers. No `correction_token` column, no applicant tokenized correction/substitution routes in v1. `corrected_email`/`corrected_phone` still record the effective contact; the `contact_*` snapshot stays immutable. | Architecture AD-7/§5.7/AD-11 hook semantics | UX OQ-3 (§15) was explicitly decided by Moses at review; the architecture was finalized the same day without acknowledging the cut. UX §14/§17 defer self-serve to v2. |
| A2 | **Referee form has server-side autosave + `partial` in v1**: `draft_answers` JSONB column, per-answer PUT, resume-at-next-question, abandoned-with-answers terminates as `partial` (confidence capped medium), form-opened/in-progress suppresses the T+24h co-nudge. `partial` becomes v1-active (it is already in both enums and in the live-row index's terminal exclusion list). | Architecture AD-3 ("no draft persistence"; `partial` v2-reserved) | UX §6.5/§8.4 designed and reviewed the autosave/partial flow; abandoned-form answers have real value; the UX co-nudge conditions (§4.3) require it. |
| A3 | **Form link TTL is 10 days** (`form_token_expires_at`), terminal states still close the link sooner. | Architecture AD-3 (30 days) | UX OQ-4 (§15) decided 10 days and the approved invite copy already says "expires in 10 days" (§6.2). |
| A4 | **Attestation choice is recorded per application**: nullable `application.reference_contact_choice TEXT CHECK IN ('attested','declined')` written at submission; the `acknowledgement_record` row is written only on `attested`; pre-v1 applications stay NULL. The payload exposes it so the panel can distinguish "declined" (Off state) from "pre-v1" (counsel posture, §11 Q5). | Architecture AD-2's `attestation_on_file`-only exposure | UX §5.3's explicit Yes/No radio makes "declined" a real, common state the panel and counsel must distinguish from "never saw the choice". |
| A5 | **Trigger is the viewing, not the shortlist**: new `application_status` value `'viewed'` (added `AFTER 'shortlisted'`); entering `viewed` auto-creates the `reference_call` rows. Manual "start now" remains for pre-viewing checks. Panel pre-trigger copy reads "Starts automatically when you mark the viewing as done." | Architecture AD-13 (shortlist trigger); UX OQ-1 | User directive 2026-07-31: the natural step after shortlisting is arranging the viewing; checking references before the applicant has even viewed is premature. Also *strengthens* the Art 6(1)(f) necessity limb (landlord intent is strongest post-viewing). |
| A6 | **`'skipped'` added to `reference_call_status`** (landlord excludes a reference at/before trigger; re-enable transitions back to `queued`). Treated as live for the slot unique index. | Architecture AD-1 enum | UX §4.2/§7.4 mandate the "Skipped by you" state with re-enable. |
| A7 | **Warm-handoff takeover is modelled as `taken_over_at TIMESTAMPTZ`**, distinct from AD-8's record-manual: the sweep skips taken-over rows, the form link stays live, a late completion still guarded-transitions to `form_completed` and notifies (UX §8.6). | Fills a gap (architecture has no takeover state; UX §7.7 requires one) | UX §7.7/§8.6 designed takeover-with-late-completion; AD-14's sticky terminals + sweep-owned sends need an explicit rule for it. |
| A8 | **Form decline uses `refused` (v1-active terminal)** and notifies via a fourth new enum value `reference_declined`; `objected` stays the STOP/hard-objection path. | Architecture AD-1 (`refused` marked v2-reserved) and §8.3 (three notification values) | UX OQ-8 + §6.6 put a decline route in every v1 message; §7.9 has distinct declined vs objected notification copy. |
| A9 | **Per-slot `verification` variants** (employer: `employment_period`, `role_confirmed`, `salary_confirmed`, `would_rehire`; character: `relationship`, `known_duration`, `character_statement`) are emitted by the deterministic structurer alongside the landlord-shaped fields. | Architecture §6.2's landlord-shaped profile | UX OQ-2 (§15) decided per-slot variants; v2's consumer must match (extends the §6.4 amendments register). |

## Requirements Inventory

### Functional Requirements

FR-RC1: Applicant makes an explicit attestation choice (radio pair, required, no default) in the References section of the application form; "Yes" writes a `reference_contact_attestation` row to `acknowledgement_record` (current `policy_version`) inside the existing `insert_acknowledgement_records` transaction (AD-2; wording is attestation/acknowledgement, never "consent")
FR-RC2: Application submission captures the applicant's IP and User-Agent into bounded columns (`application.submitted_ip_text` 64, `application.submitted_user_agent` 512) as the comparator for form-session fraud signals (AD-10; Art 13/privacy-policy update is a counsel-pack dependency)
FR-RC3: When the landlord marks the viewing as carried out (application status transitions to the new `viewed` status — see Amendments register A5), the system auto-creates `reference_call` rows (`status: queued`, `next_attempt_at: now()`, nothing sent) for the primary applicant's landlord-ref slot (or character-ref when `never_rented_before`) and employer-ref slot, skipping slots with no contact data; auto-create is suppressed when the applicant declined the attestation (`reference_contact_choice = 'declined'`) (AD-13 as amended)
FR-RC4: Landlord can manually start a check for a non-shortlisted application and skip/re-enable individual references before trigger (AD-13 manual hook; UX §7.4 queued-state overflow actions)
FR-RC5: A 15-minute sweep (Cloud Run Job + Cloud Scheduler + shared-secret manual-fire route) owns every send in the cadence — T0 invite (email + SMS carrying the Art 14 notice), T+24h applicant co-nudge, T+48h reminder 1, T+96h reminder 2 + landlord warm-handoff notification with attempt log, T+144h terminal `unreachable` (silent) — applying transition + attempt append + next-step as one guarded update per row (AD-4, AD-14)
FR-RC6: A referee completes the structured form at public capability-token route `GET/POST /reference/:token` (~288-bit token, registered in all three places: `redact_token_route`, `is_public_path`, router arm); resumable until submitted, one submission, explicit expiry; expired/used/terminal tokens get branded pages with no dead ends (AD-3, UX §8.5)
FR-RC7: Per-slot question sets (previous-landlord 11 questions, employer 8, character 5) map 1:1 onto the `ReferenceCallResult` `verification` block incl. per-slot variants (employer: `employment_period`, `role_confirmed`, `salary_confirmed`, `would_rehire`; character: `relationship`, `known_duration`, `character_statement` — UX OQ-2); as-stated checks pre-fill from application data
FR-RC8: Wrong contact (email bounce, SMS delivery failure, referee-side "wrong person") moves the row to `awaiting_correction` and surfaces the landlord-driven correction flow: the landlord confirms details with the applicant on their own channel, edits the slot's trio inline (audit-logged), and saving re-triggers the invite — exactly one correction cycle; a second failure converts to `unreachable` and logs the `referee_contact_invalid` fraud-lens signal; the original `contact_*` snapshot is never overwritten (AD-7 as amended by UX OQ-3 — applicant self-serve links are v2, §6.4)
FR-RC9: Any referee objection (form decline-with-objection, SMS STOP via verified inbound webhook, flagged email reply) immediately sets outcome `objected`, nulls `next_attempt_at`, blocks all future messages on every channel, writes a `reference_objection_log` row at objection time (Art 21 evidence, single writer, survives parent deletions), and is sticky against any later event (AD-6, §9.2)
FR-RC10: After `objected`/`unreachable`, the landlord can substitute a different referee by editing the slot's trio to the new referee (audit-logged; the applicant's verbal/message confirmation is the forewarning the attestation evidences): a new `reference_call` row is created for the slot (prior row retained as history; the landlord never edits data on a live, in-flight check) (AD-6 substitution path as amended by UX OQ-3, AD-11 hook)
FR-RC11: An internal shared-secret route records manual (Wizard-of-Oz / landlord-reported) outcomes on a live row — outcome, `verification` fields, free-text summary, notable quotes — closing it as `manual_recorded` with `result.channel: "manual"` (AD-8)
FR-RC12: Fraud signals populate per AD-10's honesty table: `contact_reused_within_application`, `contact_duplicate_of_applicant`, `contact_reused_across_applications` (pure DB), `line_type`/`voip_or_burner` (Twilio Lookup at row creation), `form_session.completion_seconds`, `form_session.ip_matches_applicant`, `form_session.device_fingerprint_match` (UA compare, labelled weak); `geo_vs_claimed_property` emits `"unknown"`, `coached_answer_score` null, `voice_matches_other_reference` absent; signals never auto-reject and are display/confidence content only (AD-10, §9.4)
FR-RC13: `GET /api/v1/vacancies/:vid/applications/:aid` gains `reference_calls[]` — ref_slot, owner_label, status, outcome, attempt_count, next_attempt_at, attempts log, `result` (internal-only fields stripped), server-rendered per-channel `display_disclaimer` (§9.5), computed hooks (`can_record_manual`, `can_substitute_referee`, `can_retry`) — plus `attestation_on_file` per application (AD-11)
FR-RC14: Landlord reference panel on application detail (v3 right column, below Applicant Information, above Audit Trail): lifecycle states with honest terminal copy, structured summary + "Worth knowing" fraud block (clues-not-verdicts), attempt log with clipboard export, warm handoff, "What this tells you" explainer (UX §7)
FR-RC15: Four new `notification_type` values (`reference_completed`, `reference_unreachable`, `reference_objected`, `reference_declined` — the form-decline path, per UX OQ-8/§7.9) dispatched per landlord `notification_preference`; the T+96h warm handoff IS the unreachable-path notification — no duplicate terminal notifications; a late completion after warm-handoff takeover reuses `reference_completed` (§8.3 as amended, UX §7.9)
FR-RC16: Lifecycle events write `audit_log` rows (entity_type `reference_call`): created, terminal transitions with outcome, objected with channel, substitution (old + new ids), manual record, correction requested/applied (AD-16)
FR-RC17: Retention integrates with the application schedule: `retention_class` + `purge_after` on `reference_call`/`reference_objection_log`; application-level CASCADE sweep is the v1 enforcement path; referee data follows `retention_due_at` (§9.3)
FR-RC18: Every new mutation path is authenticated: Twilio `X-Twilio-Signature` on `webhooks/twilio-sms`, svix verification on `webhooks/resend-events`; `/reference/*` POSTs get the `/apply`-class abuse posture (token-gated, timing validation, honeypot) (AD-15)

### NonFunctional Requirements

NFR-RC1: Referee form SSR load under 2 seconds on 3G, no-JS submission possible (inherits canonical NFR1; the referee is a first-class anonymous user like the applicant)
NFR-RC2: WCAG 2.1 AA on all new surfaces — referee form carries the same priority as the tenant form: one-question-per-screen, 44px touch targets, `aria` progress, visible amber focus ring, no paste-blocking, no session timeout (UX §12; canonical NFR23–29)
NFR-RC3: No duplicate sends, ever — the sweep's guarded updates make duplicate T0 invites impossible even across retries/downtime; a silently dead sweep is a critical observability event (Sentry capture + per-tick completion log) (AD-14, AD-15)
NFR-RC4: All webhook and public-route failures fail loudly to Sentry; webhook signature verification failures are captured (AD-15)
NFR-RC5: Idempotent terminal transitions — sticky terminals survive out-of-order webhooks (bounce after STOP leaves `objected` untouched) (AD-14)
NFR-RC6: Referee/applicant messaging is service-shaped only: zero promotional content in any referee communication (ePrivacy discipline, UX §6.1)
NFR-RC7: English-only referee surfaces in v1 (localised forms deferred per architecture §12; recorded as a copy constant, not schema)

### Additional Requirements (from the feature architecture)

- AR-RC1: One migration for `reference_call` + `reference_objection_log` + `reference_call_status`/`reference_call_outcome` enums + all indexes (live-row partial unique index, token indexes, sweep index, contact-phone index, purge indexes); a second tiny migration adds `'reference_contact_attestation'` to the `consent_type` enum; a third adds `application.submitted_ip_text`/`submitted_user_agent` + `application.reference_contact_choice` (A4); a fourth adds `'viewed'` to `application_status` `AFTER 'shortlisted'` (A5) (AD-2, AD-10, §4.3, Amendments register)
- AR-RC2: `ref_slot`, `owner_label`, `channel`, `retention_class` are TEXT+CHECK (owned deviation, contract-mirrored); `status`/`outcome` are PG enums; `updated_at` via the existing trigger pattern; RLS auto-enabled with zero policies per repo convention (§4.1, §4.4)
- AR-RC3: `notification/sms_client.gleam` — minimal Twilio REST helper (send + delivery-status), the only new external dependency; `reference_lookup` module for Twilio Lookup line-type at row creation; both no-op without keys (AD-5, §7.2)
- AR-RC4: `reference-checks` Cloud Run Job: new `docker-entrypoint.sh` entry + `deployment/terraform/scheduler.tf` entry (house pattern), module split per `verification_reminder` (job entry + logic + sql) (§5.4)
- AR-RC5: Shared-package types + JSON codecs for `reference_calls[]` payload entries per the canonical compilation-boundary convention; internal-only fields (`form_token`, `objection_detail.payload_ref`, raw IPs/UAs) stripped at the API boundary and redacted from logs (§4.2 as amended — no `correction_token` in v1, AD-11)
- AR-RC6: Mutation discipline on `reference_call`: guarded `UPDATE ... WHERE status=<expected>`; sticky terminals; atomic `attempts = attempts || $1::jsonb` appends; sweep owns all sends (AD-14)
- AR-RC7: `ReferenceCallResult v1` stored as `result` JSONB with `schema_version: "refcall-v1"` embedded; v1 emits `channel: "form"`/`"manual"`; v2-reserved fields absent (never placeholder); `fraud_signals` denormalised to its own column; terminal-no-content rows still get a result (outcome + attempts, null verification) (AD-9, §6, §4.6)
- AR-RC8: Deterministic server-side structuring — form answers map directly onto the `verification` block; `ai_summary` is a deterministic rendering, `confidence` derives from answer completeness; no LLM pass in v1 (AD-9)
- AR-RC9: Audit-on-status-change convention extended to `reference_call` (AD-16); Art 14 required-content list is architecture-mandated copy in T0 invite, form header, and every reminder footer (§5.1, §9.1)
- AR-RC10: One test module per new server module, per canonical structure convention (§13)
- AR-RC11: §9.5 `display_disclaimer` is server-rendered per channel (written channels get the call-encouragement note; v2 voice will downgrade it) — a data field, not a design afterthought (AD-11, §9.5)

### UX Design Requirements

UX-RC1: Attestation card at the end of the References section — `view_consent_block` anatomy, radio pair (required, no default, explicit Yes/No), copy verbatim from UX §5.3, privacy link, inline validation with scroll-to-error, `data-testid`s `ref-attestation`, `ref-attestation-yes`, `ref-attestation-no` (UX §5.3)
UX-RC2: References-section framing copy (§5.2) and Yes-path confirmation-page line (§5.4), verbatim
UX-RC3: Referee form — public SSR like `/apply`, mobile-first one-question-per-screen with progress ("Question 4 of 11"), single scrolling `max-w-[48rem]` page on desktop, landing screen carrying the second Art 14 moment + both escape routes (wrong person, decline) before any question, thank-you screen, branded expired/used/terminal pages (§8.5) with a self-serve "send me a new link" when the check is still open (UX §6.5, §8.5)
UX-RC4: Referee message copy verbatim — invitation email (full Art 14 block) + SMS (short notice + STOP), reminders 1–2, applicant co-nudge, decline/objection/wrong-person confirmations; Sender ID `RTenantry`; from `references@righttenantry.ie` (UX §6.2–6.6, §10.2, OQ-6/OQ-11)
UX-RC5: Reference panel chrome — "Reference Checks ({n})" v3 card, state-tracking sub-line, per-row status pill + timestamp + expand chevron + `⋯` overflow (context actions per state), `data-testid`s `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`, `refcheck-expand-{slot}`, `refcheck-overflow-{slot}` (UX §7.1–7.3)
UX-RC6: State-by-state panel content verbatim — Off (attestation declined), Queued, Invitation sent/Reminder sent/Form opened, Reference received (expanded first view), Partially completed, Contact details didn't work, Couldn't be reached, Declined to take part, Declined contact (no route-around affordance), Skipped by you, Something went wrong (UX §4.2, §7.4)
UX-RC7: Completed-reference detail — headline pull-quote (amber left border), key-facts definition table (unanswered = "Not answered", never hidden), up to 3 notable quotes, "Worth knowing" block (amber `border-l-2`, header + per-signal innocent-explanation copy verbatim from §7.5), confidence line ("Confidence: {level} · AI-generated summary — verify before relying on it."), free-text flagged as unmoderated referee text (§7.4–7.5, §9.3)
UX-RC8: Attempt log — Audit Trail timeline language, `role="list"` with `<time datetime>`, clipboard-only export with toast ("Attempt log copied — paste it into your records or a message.") (UX §7.6, OQ-5)
UX-RC9: Warm handoff — inline confirmation (never modal), referee contact chips + attempt-log export on confirm, automated contact ceases gracefully, "You're handling this one" label, late completion still lands (UX §7.7, §8.6)
UX-RC10: "What this tells you" collapsible explainer, collapsed by default, copy verbatim incl. the written-only honesty paragraph (UX §7.8)
UX-RC11: Landlord notifications copy verbatim (received / unreachable / declined / objected / late completion after handoff), brand voice, no exclamation marks (UX §7.9, §10.3)
UX-RC12: Responsive behaviour per UX §11 (panel stacks at position 8 on mobile; referee-form thumb targets are full-width rows; free text `resize-y` with counter)
UX-RC13: Accessibility per UX §12 (radiogroup aria, panel `role="region"`, rows `aria-expanded`/`aria-controls`, status pills never colour-only, "Worth knowing" text-first)
UX-RC14: Design-system alignment per UX §13 — reused components only (`view_form_section`, `view_form_field`, `view_consent_block` anatomy, v3 card, timeline, contact chips, hero-narrative amber treatment, existing notifications/skeletons); button hierarchy (one amber primary per context; destructive never filled); colour semantics (received=teal, waiting=slate, reminder/opened=navy, needs-attention=amber, declined/objected=slate never red); brand voice throughout

### FR Coverage Map

| FR | Epic | Story | Description |
|----|------|-------|-------------|
| FR-RC1 | RC1 | 1.1, 1.2 | Attestation choice recorded at submission |
| FR-RC2 | RC1 | 1.1 | Applicant IP/UA capture at submission |
| FR-RC3 | RC2 | 2.3 | Auto-create checks on `viewed` transition |
| FR-RC4 | RC2, RC4 | 2.3, 4.3 | Manual start + skip/re-enable |
| FR-RC5 | RC3 | 3.2, 3.5 | Cadence sweep owns all sends |
| FR-RC6 | RC3 | 3.3 | `/reference/:token` form session |
| FR-RC7 | RC3 | 3.3, 3.4 | Per-slot question sets → `verification` block |
| FR-RC8 | RC3, RC4 | 3.6, 3.7, 4.3 | Wrong-contact → one landlord-driven correction cycle |
| FR-RC9 | RC2, RC3 | 2.1, 3.4, 3.6 | Objection short-circuit + evidence log |
| FR-RC10 | RC4 | 4.3 | Referee substitution (landlord-driven) |
| FR-RC11 | RC5 | 5.1 | WoZ `channel: "manual"` recording |
| FR-RC12 | RC1, RC3 | 1.1, 3.7 | Fraud signals, honestly scoped |
| FR-RC13 | RC4 | 4.1 | Detail payload `reference_calls[]` |
| FR-RC14 | RC4 | 4.2, 4.3, 4.4 | Landlord reference panel |
| FR-RC15 | RC4 | 4.4 | Reference notifications |
| FR-RC16 | RC2–RC5 | every writer story + 5.2 | `audit_log` lifecycle entries |
| FR-RC17 | RC2, RC5 | 2.1, 5.2 | Retention columns + erasure integration |
| FR-RC18 | RC3 | 3.3, 3.6 | Verified webhooks + abuse posture |

## Epic List

### Epic RC1: Applicant Attestation & Reference Capture
Aisling reaches the References section of the application form, reads a plain-language explanation of what referee contact means, and makes an explicit Yes/No attestation choice — recorded honestly, with the fraud-comparator capture (IP/UA) taken at submission.
**FRs covered:** FR-RC1, FR-RC2
**UX-DRs covered:** UX-RC1, UX-RC2, UX-RC13, UX-RC14

### Epic RC2: Reference-Check Foundation & Viewing Trigger
The `reference_call` table and full lifecycle exist, the application gains the `viewed` status, and marking a viewing as carried out auto-creates the checks for the primary applicant's references — the system knows who to chase and when to start.
**FRs covered:** FR-RC3, FR-RC4 (API), FR-RC9 (evidence table), FR-RC16 (creation audit), FR-RC17 (retention columns)
**ARs covered:** AR-RC1, AR-RC2, AR-RC6

### Epic RC3: Written-First Collection Engine
Colm gets an email + SMS with the Art 14 notice, taps through a 5-minute no-login form that saves as he goes, gets reminded on a humane cadence — and every exit (decline, objection, wrong person, unreachable) is honoured instantly and truthfully.
**FRs covered:** FR-RC5, FR-RC6, FR-RC7, FR-RC8 (detection + signal), FR-RC9, FR-RC12, FR-RC18
**ARs covered:** AR-RC3, AR-RC4, AR-RC6, AR-RC7, AR-RC8, AR-RC9, AR-RC10
**UX-DRs covered:** UX-RC3, UX-RC4, UX-RC12, UX-RC13, UX-RC14

### Epic RC4: Landlord Reference Panel & Workflow
Niamh watches each reference move through its lifecycle on the application detail page, reads the structured summary and honestly-framed fraud signals, exports the attempt log, takes over manually, corrects bad details, and substitutes referees — the "already being handled" workspace.
**FRs covered:** FR-RC4 (UI), FR-RC8 (landlord correction), FR-RC10, FR-RC13, FR-RC14, FR-RC15
**ARs covered:** AR-RC5, AR-RC11
**UX-DRs covered:** UX-RC5, UX-RC6, UX-RC7, UX-RC8, UX-RC9, UX-RC10, UX-RC11, UX-RC12, UX-RC13, UX-RC14

### Epic RC5: Manual Channel & Launch Hardening
The founder records Wizard-of-Oz manual outcomes into the same data shape the automation produces, and the feature is verified end-to-end for retention, erasure, audit coverage, and observability before launch.
**FRs covered:** FR-RC11, FR-RC16, FR-RC17
**ARs covered:** AR-RC7, AR-RC9, AR-RC10

**Epic dependency note:** RC1 and RC2 are independent and can run in parallel. RC3 depends on RC2 (rows to sweep, tokens on rows) and uses RC1's capture (fraud comparator). RC4 depends on RC2 and exposes what RC3 produces; RC4.1 (payload) can start once RC2.1 lands. RC5 depends on RC2 and slots in last. Within each epic, stories are ordered so each builds only on earlier ones.

---

<!-- Stories: step-03 appends one `## Epic RCn` section per epic below this line. -->

## Epic RC1: Applicant Attestation & Reference Capture

Aisling reaches the References section of the application form, reads a plain-language
explanation of what referee contact means, and makes an explicit Yes/No attestation
choice — recorded honestly, with the fraud-comparator capture (IP/UA) taken at submission.

### Story RC1.1: Attestation & Capture Schema + Submission Write Path

As a platform,
I want the attestation enum value, the application capture columns, and the submission-time writes,
So that the applicant's explicit choice and the form-session fraud comparator are recorded as evidence.

**Acceptance Criteria:**

**Given** the migration for AD-2 runs
**When** it applies
**Then** `ALTER TYPE consent_type ADD VALUE IF NOT EXISTS 'reference_contact_attestation'` succeeds (the `20260420000003` one-enum-addition precedent)
**And** a second migration adds `application.submitted_ip_text TEXT` (bounded 64), `application.submitted_user_agent TEXT` (bounded 512), and `application.reference_contact_choice TEXT` nullable with `CHECK (reference_contact_choice IN ('attested','declined'))` (A4)

**Given** an applicant submits an application
**When** the submission transaction runs
**Then** the client IP (via `request_helpers.client_ip`, bounded) and User-Agent header (bounded) are written to the new capture columns (AD-10)
**And** when the applicant chose "attested", `insert_acknowledgement_records` gains its fourth write: a `reference_contact_attestation` row with the current `policy_version`, in the same transaction (AD-2)
**And** `reference_contact_choice` is set to `'attested'` or `'declined'` to match the explicit choice; a declined choice writes NO attestation row and the application submits normally

**Given** a submission without an attestation choice
**When** validation runs
**Then** submission fails validation (explicit choice is required — no silent skip, no default)

**Given** the wording constraint (AD-2 §3.2)
**When** any code, copy, or comment names this record
**Then** it uses attestation/acknowledgement vocabulary — the word "consent" never appears in relation to it

**Files/areas:** `supabase/migrations/YYYYMMDDHHMMSS_*` (two migrations) · `server/src/application/application_handler.gleam` (`insert_acknowledgement_records`, ~1779; submission capture) · `server/src/application/sql.gleam` + `server/src/application/sql/` · `shared/src/shared/application.gleam` (new fields on the type + codecs)

**Verify:** migrations apply cleanly from reset; server tests cover attested / declined / missing-choice paths; `make test-server` and `make test-shared` green

### Story RC1.2: Attestation UI — the References Section Choice

As an applicant,
I want to choose explicitly whether my referees may be contacted, and to understand what that means,
So that my decision is informed, honest, and free of pressure.

**Acceptance Criteria:**

**Given** the References section of the application form
**When** the section renders
**Then** the framing copy from UX §5.2 appears above the first referee field group, verbatim
**And** the attestation card renders at the end of the section with the `view_consent_block` anatomy: heading "Contacting your referees", body copy, privacy link ("How we handle referee data ↗"), and a radio pair — "Yes — my referees expect to be contacted" / "No — don't contact my referees automatically" — all verbatim from UX §5.3 including the anti-coercion footer

**Given** the attestation card
**When** it renders
**Then** the radio pair is required with no default selection, `role="radiogroup"` + `aria-required`, help text via `aria-describedby`, and `data-testid`s `ref-attestation`, `ref-attestation-yes`, `ref-attestation-no`

**Given** no option selected at submit
**When** validation runs
**Then** the form scrolls to the card with "Choose one option to continue." (UX §5.3)

**Given** a "Yes" submission
**When** the confirmation page renders
**Then** it carries the added line from UX §5.4, verbatim (the No path shows no such line)

**Given** the form is SSR
**When** JS is unavailable
**Then** the choice still posts with the submission and persists per Story RC1.1

**Files/areas:** `server/src/application/form_sections/` (references section) · `server/src/application/form_pages.gleam` · `server/src/application/form_copy.gleam` · `server/src/application/form_fields.gleam` · `server/src/application/application_handler.gleam` (field plumbing)

**Verify:** server form tests (choice required, posted value plumbed); SSR render check of the card in both states; `make test-server` green

## Epic RC2: Reference-Check Foundation & Viewing Trigger

The `reference_call` table and full lifecycle exist, the application gains the `viewed`
status, and marking a viewing as carried out auto-creates the checks for the primary
applicant's references — the system knows who to chase and when to start.

### Story RC2.1: `reference_call` + `reference_objection_log` Schema

As a platform,
I want the reference-call lifecycle table and the objection evidence log with their types and indexes,
So that all collection work has a system of record built on the agreed contract.

**Acceptance Criteria:**

**Given** the migration runs
**When** it applies
**Then** `reference_call_status` and `reference_call_outcome` enums are created per architecture §4.1 **as amended**: status includes `'skipped'` (A6); outcome includes `'unreachable'`, `'form_completed'`, `'manual_recorded'` (architecture §6.4)
**And** `reference_call` is created per §4.1 as amended — columns include the immutable `contact_*` snapshot, `corrected_email`/`corrected_phone`, attempt accounting (`attempt_count`, `next_attempt_at`, `attempts` JSONB, `correction_cycles`), `form_token` + `form_token_expires_at`, `form_opened_at`/`submitted_at`, **`draft_answers` JSONB** (A2), **`taken_over_at TIMESTAMPTZ`** (A7), `channel`, `result`/`fraud_signals` JSONB, objection fields, `retention_class`/`purge_after` — and **no `correction_token`** (A1)
**And** `ref_slot`, `owner_label`, `channel`, `retention_class` are TEXT+CHECK (owned deviation, §4.1); `status`/`outcome` are PG enums; `updated_at` uses the existing trigger-function pattern

**Given** the indexes
**When** the migration applies
**Then** the live-row partial unique index on `(application_id, ref_slot, owner_label)` excludes every terminal status (`'skipped'` is NOT excluded — a skipped row still occupies its slot, A6)
**And** unique partial indexes exist for `form_token`; plus sweep, application, contact-phone, and purge indexes per §4.1

**Given** `reference_objection_log`
**When** the migration applies
**Then** it is created per §4.1 with **no foreign keys** (must survive both parent deletions), its purge index, and `retention_class` default `'objection_evidence'`

**Given** the notification contract (FR-RC15, A8)
**When** the migration applies
**Then** a companion migration adds the four new `notification_type` values — `reference_completed`, `reference_unreachable`, `reference_objected`, `reference_declined` — via `ALTER TYPE ... ADD VALUE` (the `20260423100001` precedent), so every later emitting story has its types

**Given** the schema exists
**When** server + shared code is generated
**Then** a `server/src/reference_checks/` module exists with Squirrel SQL + `sql.gleam` CRUD primitives, and `shared/src/shared/reference_call.gleam` carries the types + JSON codecs with status/outcome round-trip tests
**And** RLS is auto-enabled with zero policies (repo convention §4.4 — no policy content is written)

**Files/areas:** `supabase/migrations/YYYYMMDDHHMMSS_create_reference_call.sql` (house header-comment style) · `server/src/reference_checks/sql.gleam` + `server/src/reference_checks/sql/` · `shared/src/shared/reference_call.gleam`

**Verify:** migration applies from reset; Squirrel codegen succeeds; shared codec round-trip tests green

### Story RC2.2: `viewed` Application Status, End to End

As a landlord,
I want to mark that the viewing has been carried out,
So that the application reflects where it really is — and reference checks know when they may start.

**Acceptance Criteria:**

**Given** the migration runs
**When** it applies
**Then** `ALTER TYPE application_status ADD VALUE 'viewed' AFTER 'shortlisted'` succeeds

**Given** the shared `ApplicationStatus` type
**When** codecs round-trip
**Then** `Viewed` encodes/decodes as `"viewed"` across shared, server (`parse_status` in `application_detail_handler.gleam`, incl. the 400 message), and client

**Given** the application detail page
**When** the status stepper renders
**Then** the progression is Submitted → Reviewing → Shortlisted → **Viewed** → Approved (Reject unchanged), rank logic updated, and `viewed` has a status-pill style in the house semantic set (navy — in-progress between amber shortlisted and teal approved)
**And** leaderboard rows and any status filters render `viewed` without breaking

**Given** a landlord clicks Viewed
**When** the status PATCH succeeds
**Then** the status updates, an `audit_log` status-change entry is written per the existing convention, and the UI reflects the new step

**Files/areas:** `supabase/migrations/` · `shared/src/shared/application.gleam` · `server/src/application/application_detail_handler.gleam` · `client/src/components/status_stepper.gleam` · `client/src/components/status_pill.gleam` · `client/src/components/leaderboard_view.gleam` · `client/src/copy.gleam`

**Verify:** `make test-shared`, `make test-server`, `make test-client` green; manual: stepper shows Viewed and PATCH accepts it

### Story RC2.3: Trigger on Viewed + Manual Start / Skip APIs

As the platform,
I want reference checks auto-created when a viewing is marked done — and manual control before that moment,
So that chasing starts at the right time, only for applicants the landlord is genuinely pursuing.

**Acceptance Criteria:**

**Given** an application transitions INTO `viewed`
**When** the status update succeeds (hook in `apply_status_update`, same position as `maybe_send_shortlist_notification`)
**Then** `reference_call` rows are created `queued` with `next_attempt_at = now()` for the primary applicant's landlord-ref slot (or character-ref when `never_rented_before`) and employer-ref slot, skipping slots with no contact data — and **nothing is sent** (the sweep owns all sends, AD-14)
**And** row creation carries the immutable `contact_*` snapshot from the application trios

**Given** the trigger fires twice (double-click, re-marking viewed)
**When** rows already exist
**Then** no duplicates are created (guarded `INSERT ... ON CONFLICT DO NOTHING` against the live-slot partial unique index)

**Given** `reference_contact_choice = 'declined'` on the application
**When** the trigger fires
**Then** no rows are created (feature off for this application, A4); pre-v1 applications (NULL choice) DO trigger (AD-2)

**Given** a non-viewed application with reference data and no declined choice
**When** the landlord-facing start-check API is called (per slot or whole application)
**Then** rows are created exactly as the auto-trigger would (manual hook, AD-13 as amended)

**Given** a `queued` row
**When** the skip API is called
**Then** a guarded transition moves it to `skipped`; re-enable moves `skipped → queued` with `next_attempt_at = now()` (A6); both write `audit_log` entries

**Given** any row creation or skip/re-enable
**When** it commits
**Then** `audit_log` rows are written (entity_type `reference_call`, event `created` / `skipped` / `re-enabled`, AD-16)
**And** creation-time fraud signals are NOT yet populated (Story RC3.7 wires them)

**Files/areas:** `server/src/application/application_detail_handler.gleam` (hook) · `server/src/reference_checks/trigger.gleam` + sql · `server/src/router.gleam` (authenticated landlord API arms)

**Verify:** server tests — correct rows per slot flavour, idempotency, declined suppression, pre-v1 allowed, skip/re-enable guards; `make test-server` green

## Epic RC3: Written-First Collection Engine

Colm gets an email + SMS with the Art 14 notice, taps through a 5-minute no-login form
that saves as he goes, gets reminded on a humane cadence — and every exit (decline,
objection, wrong person, unreachable) is honoured instantly and truthfully.

### Story RC3.1: SMS Client + Twilio Lookup (Infrastructure Slice)

As the platform,
I want a minimal Twilio SMS client and a line-type lookup module behind config,
So that collection messages and fraud signals have their single new dependency isolated and safely optional.

**Acceptance Criteria:**

**Given** `server/src/notification/sms_client.gleam`
**When** an SMS is sent
**Then** it goes through the Twilio REST API with delivery-status callback URL config, mirroring `email_client.gleam`'s shape (AD-5)
**And** without Twilio keys configured, the client no-ops with a log line (the "shortlist email skipped" precedent) — never crashes a caller

**Given** the `reference_lookup` module
**When** a line-type lookup runs for a phone number
**Then** it returns the Twilio Lookup line type (mobile / landline / voip / unknown) and no-ops without keys

**Given** configuration
**When** the server starts
**Then** Twilio env vars (account SID, auth token, sender ID `RTenantry`, status-callback base URL) load through the existing config mechanism; secrets are never committed

**Given** a Twilio API failure
**When** it occurs
**Then** Sentry captures it with context

**Files/areas:** `server/src/notification/sms_client.gleam` · `server/src/reference_checks/lookup.gleam` · `server/src/config.gleam`

**Verify:** one test module per new module (mocked HTTP per existing patterns); no-op path verified without keys; `make test-server` green

### Story RC3.2: Message Templates & Send Helpers

As a referee,
I want clear, honest messages that tell me who is asking, why, and what my rights are,
So that I can trust the link — or decline it — with full information.

**Acceptance Criteria:**

**Given** the copy deck (UX §10.2, verbatim)
**When** templates render with fixture data
**Then** the invitation email carries the full Art 14 block — controller identity (`{landlord_display_name}`), RightTenantry as processor, source (the applicant), purpose + legitimate-interest basis, retention in plain terms, rights including objection, notice URL (UX §6.2; required content list per architecture §5.1/§9.1)
**And** the invitation SMS carries the short notice + notice link + "Reply STOP to opt out" (UX §6.3)
**And** reminders 1–2 (§6.4) and the applicant co-nudge (§10.1) render verbatim, each carrying the decline route and notice link

**Given** sending config
**When** a message is sent
**Then** email goes from `references@righttenantry.ie` (existing verified transactional domain, OQ-11) and SMS from sender ID `RTenantry` (OQ-6)
**And** no message contains any promotional content (ePrivacy service-message discipline, UX §6.1)

**Given** the send helpers (`send_invite`, `send_reminder`, `send_co_nudge`)
**When** the sweep calls them
**Then** each returns a per-channel outcome (delivered / bounced / failed + detail) shaped for the row's attempt log

**Files/areas:** `server/src/reference_checks/messages.gleam` (+ templates) · `server/src/notification/email_client.gleam` (reuse) · `server/src/notification/sms_client.gleam` (RC3.1)

**Verify:** unit tests render every template with fixtures asserting each Art 14 required element; copy matches the UX deck verbatim; `make test-server` green

### Story RC3.3: Referee Form Session — Open, Answer, Autosave

As a referee,
I want to open the link and answer one question at a time with my progress saved,
So that I can finish in minutes on my phone without an account — or step away and resume.

**Acceptance Criteria:**

**Given** the route registration checklist (AD-3)
**When** `/reference/:token` ships
**Then** it is registered in all three places — `middleware.redact_token_route` (Sentry/access-log/CSP redaction), `middleware.is_public_path`, router arms — and the token is ~288-bit with the unique partial index from RC2.1

**Given** a valid token on a live row
**When** `GET /reference/:token` runs
**Then** the first GET stamps `form_opened_at` (AD-10), and the landing screen renders per UX §6.5 — the second Art 14 moment plus both escape routes (wrong person, decline) before any question
**And** questions follow the per-slot sets (previous-landlord 11, employer 8, character 5 — UX §6.5 tables), one per screen on mobile with progress ("Question 4 of 11"), single `max-w-[48rem]` page on desktop, as-stated checks pre-filled from application data

**Given** a referee answering
**When** each answer is given
**Then** it persists to `draft_answers` (A2) — `PUT /reference/:token/answer` with JS, equivalent per-question POST without JS (SSR never requires JS)
**And** re-opening the link resumes at the next unanswered question (resumable until submitted, AD-3 as amended)

**Given** an unknown, expired, or terminal token
**When** the page is requested
**Then** the branded pages per UX §8.5 render with distinct truthful copy (expired / already completed / declined / landlord handling) — no dead ends
**And** an expired link on a still-open check offers "Send me a new link" (re-sends to the contact on file, audit-logged)
**And** link TTL is 10 days from invitation (`form_token_expires_at`, A3)

**Given** the abuse posture (AD-15)
**When** POSTs arrive
**Then** the honeypot field and submission-timing validation apply (the `/apply`-class posture)

**Files/areas:** `server/src/reference_checks/form_handler.gleam` + `form_pages.gleam` · `server/src/middleware.gleam` · `server/src/router.gleam`

**Verify:** server tests — token states, autosave, resume, TTL/expiry pages, resend-link, honeypot/timing rejection; SSR render checks; `make test-server` green

### Story RC3.4: Form Completion & Exit Routes — Submit, Decline, Objection, Wrong Person

As a referee,
I want to submit my reference — or decline, object, or flag wrong details — and then be left alone,
So that taking part is my choice and stopping is instant.

**Acceptance Criteria:**

**Given** a completed form POST
**When** validation passes
**Then** the `ReferenceCallResult v1` is structured deterministically (AD-9): `schema_version: "refcall-v1"`, `channel: "form"`, the `verification` block including per-slot variants (A9), `free_text_signals` verbatim, deterministic `ai_summary` with completeness-derived `confidence`, and the `compliance` block — and a guarded `UPDATE ... WHERE status='contact_initiated'` transitions the row to `form_completed` (AD-14)
**And** `result` + denormalised `fraud_signals` are written, `purge_after` is stamped from the application's `retention_due_at` when set, and the audit terminal entry is written
**And** a second POST to the same token gets the branded "already completed" page — one submission only (AD-3)

**Given** the notifications this story emits (types exist since RC2.1)
**When** `form_completed` / `refused` / `objected` occur
**Then** `reference_completed` / `reference_declined` / `reference_objected` dispatch through the existing dispatcher (respecting `notification_preference`) with copy per UX §7.9 verbatim

**Given** the decline route (in every message + landing screen)
**When** a referee declines (optional one-line reason, never required)
**Then** the row terminates as `refused` (A8) with a result per §4.6 (outcome + attempts, null `verification`), the `reference_declined` notification fires, the confirmation copy per UX §10.2 renders, and all messages stop

**Given** the objection route ("don't contact me")
**When** a referee objects
**Then** AD-6 applies: status `objected` (sticky — a later bounce or sweep tick cannot move it, AD-14), `next_attempt_at` NULL, all future sends blocked, and a `reference_objection_log` row written **at objection time** by the objection handler alone; the `reference_objected` notification fires

**Given** the wrong-person route
**When** a referee says the details are wrong
**Then** the row moves to `awaiting_correction` — never a re-send to the same details (AD-7) — and the landlord sees the "Contact details didn't work" state (RC4)

**Given** the thank-you screen
**When** a submission completes
**Then** it renders per UX §6.5 verbatim, identical for every completion path (a referee is never told the landlord took over, UX §8.6)

**Files/areas:** `server/src/reference_checks/form_handler.gleam` · `server/src/reference_checks/result.gleam` (structuring) · `server/src/notification/notification_dispatch.gleam`

**Verify:** server tests per path — guarded double-submit, objection stickiness vs late events, per-slot structuring, §4.6 mapping; `make test-server` green

### Story RC3.5: The Sweep — Cadence Engine + Cloud Run Job

As the platform,
I want a 15-minute sweep that owns every send and transition,
So that chasing is humane, exactly-once, self-healing after downtime — and never silently dead.

**Acceptance Criteria:**

**Given** the infrastructure
**When** it deploys
**Then** a `reference-checks` Cloud Run Job exists: new `docker-entrypoint.sh` entry, `deployment/terraform/reference-checks-job.tf`, and a 15-minute Cloud Scheduler entry in `scheduler.tf` (house pattern with the same environment gating as retention/digest), plus the shared-secret `POST /api/v1/internal/reference-checks` manual-fire route

**Given** rows with `next_attempt_at <= now()` and `taken_over_at IS NULL` (A7)
**When** a tick processes a row
**Then** it computes the due step from the attempt log — T0 invite / T+24h applicant co-nudge / T+48h reminder 1 / T+96h reminder 2 + landlord warm-handoff notification with attempt log / T+144h terminal `unreachable` — sends via the RC3.2 helpers, and applies transition + atomic attempt append + next-step computation as ONE guarded update (AD-4, AD-14)
**And** the co-nudge fires only when the form was never opened and no draft exists (A2); a taken-over row is skipped entirely

**Given** the cadence reaches T+96h
**When** reminder 2 goes out
**Then** the `reference_unreachable` warm-handoff notification fires with the attempt log rendered — and the T+144h terminal transition is silent (no duplicate terminal notification, §8.3)

**Given** an abandoned form with saved answers at T+144h
**When** the sweep terminates the row
**Then** it becomes `partial` (A2): the result is structured from `draft_answers` (unanswered fields null), confidence capped at medium
**And** an abandoned form with zero answers becomes `unreachable`; a failed correction cycle becomes `unreachable` with the `reference_unreachable` notification (§4.6)

**Given** a system failure during a tick
**When** a row cannot be processed
**Then** it terminates `failed` with `outcome` NULL + `terminal_reason`, Sentry captures it, and no landlord notification fires (§4.6)

**Given** liveness (AD-15)
**When** every tick completes
**Then** a per-tick completion log is emitted and any job failure hits Sentry

**Files/areas:** `server/src/reference_checks/sweep.gleam` + sql · `docker-entrypoint.sh` · `deployment/terraform/reference-checks-job.tf` + `scheduler.tf` · `server/src/router.gleam` (internal route)

**Verify:** server tests with a fake clock per cadence step; guarded-update race test; no-duplicate-T0 test across a retry; `make test-server` green

### Story RC3.6: Verified Webhooks — Resend Events + Twilio SMS

As the platform,
I want bounce, delivery-failure, and STOP signals to flow into the lifecycle through verified webhooks only,
So that bad contact triggers the correction path and objections are honoured instantly — and nobody can forge either.

**Acceptance Criteria:**

**Given** `webhooks/resend-events`
**When** a svix-verified bounce/complaint event arrives (the `inbound_email/svix.gleam` verifier pattern)
**Then** the row moves to `awaiting_correction` (AD-7 as amended): guarded transition, audit `correction requested`, landlord-visible state

**Given** `webhooks/twilio-sms`
**When** an `X-Twilio-Signature`-verified delivery-failure status arrives
**Then** the same correction path applies
**And** a verified inbound STOP/reply applies AD-6: `objected` terminal, `reference_objection_log` row, sticky against any later event (a bounce arriving after STOP changes nothing)

**Given** a request with an invalid or missing signature
**When** either webhook receives it
**Then** no state mutates, the request is rejected, and Sentry captures the verification failure (AD-15)

**Files/areas:** `server/src/reference_checks/webhooks.gleam` (+ Twilio signature verification) · `server/src/router.gleam`

**Verify:** server tests — signature failure, out-of-order events, sticky-terminal cases; `make test-server` green

### Story RC3.7: Fraud-Signals Module

As a landlord,
I want honest fraud signals on each reference,
So that I have clues about provenance — never fabricated detections, never verdicts.

**Acceptance Criteria:**

**Given** the `fraud.gleam` module (AD-10)
**When** it computes signals
**Then** it produces exactly the AD-10 table: `contact_reused_within_application`, `contact_duplicate_of_applicant`, `contact_reused_across_applications` (pure DB), `line_type` / `voip_or_burner` (Twilio Lookup), `form_session.completion_seconds` / `ip_matches_applicant` / `device_fingerprint_match` (UA compare, labelled weak)
**And** `geo_vs_claimed_property` emits `"unknown"`, `coached_answer_score` is null, `voice_matches_other_reference` is absent — never fabricated (AD-10 honesty rule)

**Given** the wiring
**When** rows are created
**Then** the pure-DB checks run at creation and the line-type lookup runs before the first send (wired into the RC2.3 trigger path; rows created before this story keep nulls honestly)
**And** the DB checks re-run at submission (contacts can change via the correction loop) and `form_session` computes at submission from `form_opened_at` → `submitted_at` + client-reported focus time, referee IP/UA server-captured, compared against `application.submitted_ip_text` / `submitted_user_agent`
**And** `referee_contact_invalid` is recorded when a correction cycle fails (wired into the RC3.5/RC4.3 paths; supersedes `referee_number_wrong`, architecture §6.4)

**Given** the storage boundary
**When** signals persist
**Then** they land in `result.fraud_signals` (authoritative) and the denormalised column, and raw IPs/UAs never leave the server (internal-only, §4.2)
**And** no signal ever auto-rejects or alters a score (AD-10, §9.4)

**Files/areas:** `server/src/reference_checks/fraud.gleam` · wiring into `trigger.gleam`, `form_handler.gleam`, `sweep.gleam`

**Verify:** unit tests per signal including innocent-reuse fixtures (a letting agent legitimately appearing across applications must not be styled as fraud); `make test-server` green

## Epic RC4: Landlord Reference Panel & Workflow

Niamh watches each reference move through its lifecycle on the application detail page,
reads the structured summary and honestly-framed fraud signals, exports the attempt log,
takes over manually, corrects bad details, and substitutes referees — the "already being
handled" workspace.

### Story RC4.1: Detail Payload Extension (Backend Contract)

As the client app,
I want `reference_calls[]` in the application detail payload with server-computed hooks and disclaimers,
So that the panel renders from one stable contract and never re-derives state rules.

**Acceptance Criteria:**

**Given** `GET /api/v1/vacancies/:vid/applications/:aid`
**When** the application has reference data
**Then** the payload gains `reference_calls[]` per architecture §8.1: `reference_call_id`, `ref_slot`, `owner_label`, `status`, `outcome`, `attempt_count`, `next_attempt_at`, the attempt log, the stored `result`, and the hooks object
**And** internal-only fields are stripped at the boundary — `form_token`, `objection_detail.payload_ref`, raw IPs/UAs inside `fraud_signals.form_session` (§4.2)

**Given** each entry
**When** it serialises
**Then** `display_disclaimer` is server-rendered per channel (§9.5): written-channel results carry the call-encouragement note (calibration copy per §8.1; provenance framing, never invalidation), and the hooks are computed per §8.2 — `can_record_manual` any non-terminal, `can_substitute_referee` terminal `objected`/`unreachable`, `can_retry` `failed`

**Given** the application itself
**When** the payload builds
**Then** it carries `attestation_on_file` and `reference_contact_choice` (A4) plus the referee trios, so the panel can render the Off state and the pre-trigger state without extra fetches

**Given** the compilation boundary
**When** types are defined
**Then** they live in the shared package with JSON codecs (snake_case unbroken DB → JSON → Gleam, canonical AR21) and round-trip tests

**Files/areas:** `server/src/application/application_detail_handler.gleam` + sql · `shared/src/shared/application_detail.gleam` + `shared/src/shared/reference_call.gleam`

**Verify:** server tests with explicit stripping assertions; shared round-trip tests; `make test-server` and `make test-shared` green

### Story RC4.2: Reference Panel (Status & Summary)

As a landlord,
I want to see each reference's status and read completed summaries with honest framing,
So that I always know exactly where things stand — including when a state tells me nothing about the applicant.

**Acceptance Criteria:**

**Given** the application detail page (v3 layout)
**When** the panel renders
**Then** it sits in the right column below Applicant Information, above Audit Trail (mobile: position 8), per UX §7.1–7.3: "Reference Checks ({n})" heading, state-tracking sub-line per §10.3 **as amended** (pre-trigger: "Starts automatically when you mark the viewing as done.", A5), and the collapsed-by-default "What this tells you" explainer (§7.8 verbatim)
**And** `data-testid`s `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`, `refcheck-expand-{slot}`, `refcheck-overflow-{slot}` are present

**Given** every lifecycle state
**When** rows render
**Then** state content matches UX §4.2/§7.4 verbatim: Off (attestation declined — referee contact chips, no re-ask affordance), pre-trigger queued, Invitation sent / Reminder sent / Form opened (mini timeline + what-happens-next), Reference received, Partially completed ("answered {m} of {n}", confidence capped medium), Contact details didn't work, Couldn't be reached, Declined to take part, Declined contact (no route-around suggestion), Skipped by you, Something went wrong
**And** status-pill colours follow §13 semantics — received teal, waiting slate, reminder/opened navy, needs-attention amber, declined/objected slate **never red**

**Given** a completed reference, expanded (default on first view)
**When** the detail renders
**Then** it shows the headline pull-quote (amber left border), the key-facts definition table with "Not answered" for unanswered fields (never hidden, never guessed), up to 3 notable quotes, the "Worth knowing" block when ≥1 signal (§7.5: header + per-signal copy verbatim, amber `border-l-2`, innocent explanation + suggested action), the free-text unmoderated flag (§9.3), and the confidence line verbatim

**Given** accessibility & loading
**When** the panel loads and is operated by keyboard/screen reader
**Then** skeleton shimmer shows during load; the card is `role="region"` with `aria-label="Reference checks"`; rows are buttons with `aria-expanded`/`aria-controls`; status is never colour-only

**Files/areas:** `client/src/components/reference_panel.gleam` (new) · application detail page wiring · `client/src/copy.gleam` · shared types from RC4.1

**Verify:** `make test-client` green; visual check against UX §7 wireframes; state matrix rendered for all 12 states

### Story RC4.3: Row Actions — Start, Skip, Take Over, Correct, Substitute

As a landlord,
I want to control each check — start early, skip, take over, fix details, swap referees,
So that automation never traps me and a dead end always has a next step.

**Acceptance Criteria:**

**Given** a pre-trigger row
**When** the landlord opens its `⋯` overflow
**Then** "Start this check now" asks once, inline (§7.4 confirm copy), and starts the check via the RC2.3 API; "Skip this reference" excludes it (and can be re-enabled)

**Given** an in-flight row
**When** "Take over manually" is chosen
**Then** the inline confirmation per §7.7 renders (never a modal); on confirm the row gets `taken_over_at` (A7) — the sweep stops sending, referee contact chips + attempt-log export render inline, the label reads "You're handling this one" — and the form link stays live: a late completion still transitions to `form_completed`, updates the panel, and notifies (§8.6)

**Given** an `awaiting_correction` row
**When** the correction UI renders
**Then** the inline edit-trio wireframe per §8.3 shows with the applicant's contact chips; "Save & resend" is audit-logged, writes `corrected_email`/`corrected_phone` (snapshot immutable, A1), updates the application trio, sets `correction_cycles = 1`, and re-queues the row (`queued`, `next_attempt_at = now()`)
**And** a second failure converts the row to `unreachable` with the `referee_contact_invalid` signal (AD-7; wired by RC3.7)

**Given** a terminal `objected` or `unreachable` row
**When** the landlord substitutes a referee (`can_substitute_referee`)
**Then** the same inline edit captures the NEW referee trio, a new `reference_call` row is created for the slot (prior row retained as history), and the audit entry carries old + new row ids (AD-16)

**Given** any action endpoint
**When** it runs
**Then** it is ownership-checked and guarded on the row's expected pre-state (AD-14), and manual actions are hidden entirely in the Off (declined) state

**Files/areas:** `client/src/components/reference_panel.gleam` + `client/src/api/` · `server/src/reference_checks/actions_handler.gleam` · `server/src/router.gleam`

**Verify:** server tests per transition incl. correction-cycle counting and substitution history; client tests; `make test-server` / `make test-client` green

### Story RC4.4: Attempt Log, Export & Notification Completeness

As a landlord,
I want the full attempt history and trustworthy notifications,
So that I have evidence for my records and never miss a state change.

**Acceptance Criteria:**

**Given** a started row
**When** the attempt log expands
**Then** the timeline per UX §7.6 renders in the Audit Trail's visual language (`role="list"`, `<time datetime>`), covering every send, form-opened, correction, takeover, substitution, and terminal event
**And** "Export attempt log" copies a plain-text version (reference, timeline, outcome, signals) to the clipboard with the verbatim toast (OQ-5) — no file download in v1

**Given** the notification surface (types since RC2.1; dispatch wired per emitting story)
**When** this story completes
**Then** every reference event has its UX §7.9 copy verbatim — including the late-completion-after-handoff variant, which reuses `reference_completed` — and a preference-matrix test proves realtime/daily/off behaviour per landlord `notification_preference`
**And** a no-duplicate-terminals test proves the T+96h warm handoff is the only unreachable-path notification (§8.3)

**Files/areas:** `client/src/components/reference_panel.gleam` · `server/src/notification/notification_dispatch.gleam` + templates · `server/src/reference_checks/` emit points

**Verify:** preference-matrix and no-duplicate tests; `make test-server` green

## Epic RC5: Manual Channel & Launch Hardening

The founder records Wizard-of-Oz manual outcomes into the same data shape the automation
produces, and the feature is verified end-to-end for retention, erasure, audit coverage,
and observability before launch.

### Story RC5.1: WoZ Manual Outcome Recording (Internal Route)

As the founder,
I want to record a manual reference outcome into the same structure the automation produces,
So that cohort Wizard-of-Oz delivery lives in the system of record, not a spreadsheet.

**Acceptance Criteria:**

**Given** the shared-secret route `POST /api/v1/internal/reference-checks/record-manual`
**When** a valid payload arrives (outcome, `verification` block fields, free-text summary, notable quotes)
**Then** a live row closes as `manual_recorded` (guarded transition, `next_attempt_at` NULL), and `result` is written with `channel: "manual"` — founder-written `ai_summary`, `form_session: null`, DB fraud signals only (AD-8, §6.2)
**And** the `reference_completed` notification fires and the audit entry records the manual record (AD-16)

**Given** the same route
**When** called for landlord-reported manual contact (the warm-handoff "I called them myself" loop-back)
**Then** it records identically (AD-8)

**Given** an invalid call
**When** the row is already terminal, the payload is malformed, or the secret is wrong
**Then** the route rejects (409 / 400 / 401), no state mutates, and misuse is captured to Sentry

**Files/areas:** `server/src/reference_checks/manual_handler.gleam` · `server/src/router.gleam` · `server/src/reference_checks/result.gleam`

**Verify:** server tests per path incl. terminal-row rejection; `make test-server` green

### Story RC5.2: Retention, Audit & Observability Hardening

As the platform,
I want the feature verified against retention, erasure, audit, and liveness obligations,
So that launch has no compliance gaps and no silent failure modes.

**Acceptance Criteria:**

**Given** retention (§9.3)
**When** an application reaches erasure
**Then** its `reference_call` rows are deleted by the application-level CASCADE sweep, `purge_after` was stamped at every terminal transition, and `reference_objection_log` rows survive (no FK) with their own `retention_class`/`purge_after`
**And** DSAR/erasure flows handle referee data per the existing patterns, verified and documented in the story PR

**Given** audit coverage (AD-16)
**When** each lifecycle event fires
**Then** a test matrix proves `audit_log` rows exist for: created, every terminal transition with outcome, `objected` with channel, substitution (old + new ids), manual record, correction requested/applied, skipped/re-enabled

**Given** observability (AD-15)
**When** the sweep and webhooks run
**Then** the per-tick completion log and Sentry-on-failure are verified, webhook verification failures are captured, and the Cloudflare rate-rule question for the new public paths is documented as a deploy checklist item in the PR

**Given** the canonical test convention
**When** the story completes
**Then** every new `server/src/reference_checks/` module has its test module and `make test-server` is fully green

**Files/areas:** `server/src/retention/` (integration verification) · `server/src/reference_checks/` tests · deploy checklist in the story PR

**Verify:** full `make test-server` green; audit/retention test matrices pass; checklist present in PR

---

## Build Notes for Dispatching Gru

- **Suggested dispatch order:** RC1.1 + RC2.1 in parallel → RC1.2, RC2.2, RC2.3 → RC3.1 → RC3.2 → RC3.3 → RC3.4 → RC3.5 → RC3.6 → RC3.7 → RC4.1 → RC4.2 → RC4.3 → RC4.4 → RC5.1 → RC5.2. RC4.1 may start as soon as RC2.1 lands; RC4 stories otherwise follow RC3.
- **Story count sanity vs the architecture:** 18 stories against 16 ADs + 9 amendments — each AD has exactly one home (AD-1→RC2.1, AD-2→RC1, AD-3→RC3.3, AD-4→RC3.5, AD-5→RC3.1, AD-6→RC3.4/3.6, AD-7→RC3.6/4.3, AD-8→RC5.1, AD-9→RC3.4/5.1, AD-10→RC1.1/3.7, AD-11→RC4.1, AD-12→dependencies only, AD-13→RC2.2/2.3, AD-14→every writer story, AD-15→RC3.3/3.5/3.6/5.2, AD-16→every writer story + RC5.2).
- **Non-code gates (launch, not build):** ComReg Sender-ID registration should start NOW in parallel; Twilio provisioning needed by RC3.1's first integration test; counsel pack is launch-gating.
- **Canonical cross-references:** [epics.md](epics.md) (conventions), [architecture.md](architecture.md) (system canon), [architecture-reference-checking-v1-2026-07-29.md](architecture-reference-checking-v1-2026-07-29.md) (data contract), [ux-reference-checking-v1-2026-07-29.md](ux-reference-checking-v1-2026-07-29.md) (flows + copy), [prd.md](prd.md) (decision-support posture), [refcheck-pitch-copy-deck-2026-07-29.md](refcheck-pitch-copy-deck-2026-07-29.md) §5–6 (WoZ ops context), issue #548.

## Dependencies (non-code gates — NOT stories)

- **ComReg SMS Sender-ID registration** for `RTenantry` — hard launch dependency; unregistered Sender IDs arrive labelled "Likely Scam" (2025-07-03 regime). Ops task; should start immediately in parallel with the build (architecture §11 Q1).
- **Twilio account + IE number provisioning** — billing owner Moses; the build's first SMS integration test needs it (§11 Q2). Code no-ops without keys.
- **Irish counsel pack / DPIA update** — Annex III 5(b)/Art 6(3) classification memo; Art 14 notice + LIA wording; controller/processor map; **Art 13/privacy-policy update for the new applicant-submission IP/UA capture (AD-10)**; display posture for `attestation_on_file: false` on pre-v1 applications (AD-2); free-text display posture (§9.3/§11 Q4). Launch-gating, not build-gating.
- **Cloudflare rate rules for the new public paths** — deploy-time checklist item, not a code decision (AD-15).

## v2+ (documented forward contracts — NOT stories)

- Voice channel (Twilio IE1 + ConversationRelay, retry worker, transcript structuring, re-score with `reference_call_results[]`) → RightTenantryAgents#168, evidence-gated per the 2026-07-29 amendment.
- v5 re-score implementation (AD-12 — v1 only stores rows in the shape the contract consumes).
- Localised referee forms/messages (§12).
- Applicant self-serve correction/substitution signed-link surface (UX §14 hook — confirmed v2 at 2026-07-31 clarify; v1 is landlord-driven per UX OQ-3).
- Co-applicant employer-ref auto-triggering (AD-13 revisit condition).
- Per-row `purge_after` sweep (§9.3 — v1 enforcement is application-level CASCADE).
