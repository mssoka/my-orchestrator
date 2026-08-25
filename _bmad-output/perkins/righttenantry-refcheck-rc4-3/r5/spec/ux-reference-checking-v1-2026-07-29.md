# UX Design — Reference Checking v1 (Written-First)

**Author:** Sally (UX) — via orchestration minion `righttenantry-refcheck-v1-ux`
**Date:** 2026-07-29
**Status:** Draft — review rounds 1–2 applied (lavish, 2026-07-29; all open questions decided, §15)
**Issue:** [#548](https://github.com/solarity-services/RightTenantry/issues/548) (incl. the 2026-07-29 gate amendment: design + v1 build proceed in parallel with the concierge cohort)
**Host surface:** `ux-application-detail-v3.md` (application detail, right column)
**Builds on:** `research/heist-535/architecture.md` (`ReferenceCallResult v1` schema + lifecycle), `research/heist-535/fallback.md` (industry completion patterns), `research/heist-535/legal.md` (GDPR/ePrivacy/AI Act obligations), `research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md` (synthesis), `brand-identity-and-design-system.md`, `ux-design-specification.md`
**Scope boundary:** UX specification only. No code changes. Voice is v2 and appears nowhere in this spec except §14 (forward contract).

---

## 1. Context

Niamh shortlists Aisling at 9pm. The analysis says Aisling looks strong — but the strongest signal in screening is the one Niamh currently has to chase herself: the previous landlord on the phone, confirming the rent was paid and the flat came back clean. That chase is 1–2 hours per reference, spread over days of phone tag, and under time pressure it gets skipped — which can invalidate landlord insurance and, post-2026 reforms, turns a wrong choice into a 6-year commitment.

The research (heist-535) settled the shape of the answer: the entire referencing industry collects references **written-first** — email/SMS with a structured web form, automated reminders, and an applicant co-nudge — at 85–98% self-reported completion. Voice AI is the v2 differentiator; the form is the completion engine. v1 ships the form door only.

Three actors, three flows:

1. **Applicant** — gives reference details (already mandatory on the application form) and makes a plain-language **attestation** that their referees expect contact. Declining is honest and costless: the feature stays off for that application and the landlord uses today's manual flow.
2. **Referee** — a busy stranger who owes us nothing. Gets an email + SMS, opens a mobile form with no login, confirms ~10 facts about the applicant in under 5 minutes, gets thanked and left alone. Can decline, object (hard stop), or tell us the details are wrong.
3. **Landlord** — watches per-reference progress on the application detail page, reads a structured summary with fraud signals framed as decision support (never verdicts), nudges the applicant when things stall, and takes over manually with an exported attempt log when automation exhausts.

The emotional job, per the brand: Niamh should feel the problem is *already being handled* — the moment after it's solved, not the chase itself.

---

## 2. v1 Scope (decided — not up for re-litigation)

| In scope (v1) | Out of scope (v2+) |
|---|---|
| Reference details capture UX + `reference_contact_attestation` wording | Any voice UI ("speak now", call booking, call scheduling) |
| Referee invite (email + SMS) with Art 14 notice | Telephony, recordings, transcripts |
| Structured referee web form (per-slot question sets) | AI-call disclosure copy (Art 50) — no AI interacts with the referee in v1 |
| 2 reminders (48h cadence) + applicant co-nudge | Automated re-score with reference evidence (v5 contract — §14 forward note) |
| Landlord reference panel: lifecycle, summary, fraud signals, attempt log, warm handoff | landdirect folio checks, voice-printing, deepfake signals |
| Decline / objection / wrong-contact / partial / expired-link states | Localised referee forms (v1 is English) |

Data contract: this spec designs against `ReferenceCallResult v1` in `research/heist-535/architecture.md` — `channel: "form"`, the `verification` block as the form's question spine, `fraud_signals.form_session`, and the lifecycle `queued → contact_initiated → … → form_completed | partial | unreachable | refused | objected`. Where a data decision is needed, it is a numbered open question in §15, not an invention.

---

## 3. Design Principles (this feature)

1. **The referee is doing us a favour.** Every referee-facing surface is designed for a busy stranger at 21:30 on a phone: no login, no account, single-tap answers, under 5 minutes, and a graceful exit at every step. Completion benchmarks (Xref ~98%, RefNow 88%) come from exactly this respect.
2. **Honest doors, no dark patterns.** The applicant can decline automatic contact; the referee can decline or object. Every decline path is as easy to find as the happy path, and every terminal state is shown to the landlord truthfully — never a silent gap that reads as laziness.
3. **Signals are clues, not verdicts.** Fraud signals and AI summaries are decision *support*. Nothing auto-rejects, nothing styles a signal as a guilty verdict, and every signal carries its innocent explanation. "Not verified" ≠ "fraudulent" (research: RTB gaps, agent-landlords, shared connections all produce innocent mismatches).
4. **Refusal is never the applicant's demerit.** A referee who declines, objects, or can't be reached says nothing about the applicant. Landlord-facing copy states this explicitly at exactly those moments (it is also the re-score rule in the architecture).
5. **Columns keep their meaning (v3).** Left = the applicant's story; right = the landlord's workspace. Reference *checking* is workflow — triggers, nudges, handoffs — so the panel lives in the right column, and completed summaries expand inside it rather than duplicating a second surface.
6. **The notice is the product.** The Art 14 privacy notice isn't a footer link — it's how a stranger decides we're legitimate. First-contact copy carries it in plain language.

---

## 4. Actors, Lifecycle & Timeline

### 4.1 Protagonists (journeys in §5–§7)

- **Niamh** — landlord, one vacancy, 60+ applications, decides from her couch.
- **Aisling** — applicant, organised, has told her referees to expect contact.
- **Colm** — Aisling's previous landlord, mid-50s, answers messages after dinner.
- **Sarah** — Aisling's HR manager (employer referee), completes forms between meetings.

### 4.2 Per-reference lifecycle (landlord-facing labels)

Architecture states on the left; what the landlord sees on the right.

| Architecture state | Landlord label | Meaning |
|---|---|---|
| `off` (attestation declined) | **Off — contact directly** | Applicant chose manual contact; feature does nothing for this application |
| `queued` | **Queued** | Waiting to start (auto-starts on shortlist; see D2) |
| `contact_initiated` | **Invitation sent** | Email + SMS delivered |
| `reminded` (×1–2) | **Reminder sent** | Reminder n of 2 sent |
| (form opened, unsubmitted) | **Form opened** | Referee opened the link — progress signal, still waiting |
| `form_completed` | **Reference received** | Structured summary available |
| `partial` | **Partially completed** | Some answers captured; unanswered fields shown as "Not answered" |
| `awaiting_correction` | **Contact details didn't work** | Wrong contact / bounced; landlord confirms new details with the applicant, edits, re-triggers — one cycle |
| `unreachable` | **Couldn't be reached** | Sequence exhausted; warm handoff offered |
| `refused` (polite decline) | **Declined to take part** | Referee used the decline route |
| `objected` (STOP / "don't contact me") | **Declined contact** | Hard stop on every channel, logged as objection |
| `skipped` | **Skipped by you** | Landlord excluded this reference before/at trigger |
| `failed` | **Something went wrong** | System failure; retry available; never styled as applicant's problem |

### 4.3 Default timeline (per reference)

| T | Event |
|---|---|
| T+0 | Invitation email + SMS (Art 14 notice carried) |
| T+24h | If form never opened: **applicant co-nudge** email ("a quick word from you helps") |
| T+48h | Reminder 1 (email + SMS) |
| T+96h | Reminder 2 — final ("last message from us") |
| T+144h | No completion → `unreachable`; warm handoff surfaces on the panel |

Cadence values decided at review (2026-07-29, §15): co-nudge T+24h-if-unopened, reminders T+48h/T+96h, unreachable T+144h. They remain configuration, not copy constants. Reminders stop the instant the form is completed, declined, or objected. A form *in progress* (opened with saved answers) suppresses the nudge email but not reminders.

---

## 5. Flow 1 — Applicant: Reference Capture & Attestation

### 5.1 Where it lives

The existing application form's **References** section (landlord / employer / character trios — mandatory since Apr 2026). v1 changes nothing about the fields; it adds context copy at the top of the section and the attestation block at the bottom.

### 5.2 Section framing (new)

Above the first referee field group:

> **Your references**
> Give details for people who know you as a tenant, employee, or personally. If you're happy for us to, we'll check these references for the landlord — see the choice at the end of this section.

### 5.3 The `reference_contact_attestation` block

**Placement:** end of the References section, as a slightly elevated card (same treatment as `view_consent_block`, the existing GDPR block).

**This is an acknowledgement, not consent.** It records Art 13 transparency (the applicant knows what will happen and has told their referees) — the lawful basis for contact is legitimate interest. The word "consent" appears nowhere.

**Wireframe:**

```
┌─────────────────────────────────────────────────────────────┐
│  Contacting your referees                                   │
│                                                             │
│  RightTenantry can check your references for the landlord.  │
│  We'll email and text each referee a short, secure form     │
│  (about 5 minutes) asking them to confirm the details       │
│  you've given us. We contact them only about this           │
│  application, we tell them you gave us their details, and   │
│  they can decline or ask us to delete their data at any     │
│  time. How we handle referee data ↗                         │
│                                                             │
│  ○  Yes — my referees expect to be contacted                │
│     They've agreed to act as my referees and know they'll   │
│     hear from RightTenantry.                                │
│                                                             │
│  ○  No — don't contact my referees automatically            │
│     The landlord will see my references and can contact     │
│     them directly instead.                                  │
│                                                             │
│  Either choice is fine. It changes how references are       │
│  checked, not how your application is shown.                │
└─────────────────────────────────────────────────────────────┘
```

| Element | Spec |
|---|---|
| Choice control | Radio pair, **required**, no default selection. An explicit choice (not an opt-out checkbox) — honest data, no assumed-yes dark pattern |
| "Yes" path | Attestation recorded as a new `record_type` value `reference_contact_attestation` on the existing `acknowledgement_record` table (per architecture thread) |
| "No" path | Feature off for this application; application submits normally; landlord sees the honest "Off — contact directly" state (§7.4). No re-ask, no nag interstitial, no score treatment |
| Privacy link | "How we handle referee data ↗" → privacy notice, referee section |
| Validation | Standard form pattern: inline on blur/submit-scroll; if unanswered at submit, scroll to block with "Choose one option to continue" |
| `data-testid` | `ref-attestation`, `ref-attestation-yes`, `ref-attestation-no` |

**Copy rationale:** "my referees expect to be contacted" is the evidentiary sentence — it records that the applicant has *forewarned* the referee (the single biggest completion lever in the industry, and the Art 13 transparency fact). The trailing line ("changes how references are checked, not how your application is shown") is the anti-coercion promise, and it is true: refusal is never scored against the applicant.

### 5.4 Post-submit confirmation (tenant confirmation page)

One added line under the existing "Application received" content, only on the Yes path:

> "We'll contact your referees shortly — a quick word from you that we're legitimate makes a real difference."

This pre-seeds the co-nudge (§6.6) before it's ever needed.

### 5.5 Journey A — Aisling applies (climax beat: the attestation)

1. Aisling fills the form on her phone, reaches References, enters Colm (previous landlord), Sarah (employer), and a character referee.
2. She reads the attestation card. She already told Colm and Sarah she'd list them — **she picks "Yes" and feels she's done right by them, not sold them out.** The sentence "they can decline or ask us to delete their data at any time" is what makes the choice comfortable.
3. Confirmation page: she messages Colm — "you'll get a text from RightTenantry about me, it's legit." The system never had to ask her to.

---

## 6. Flow 2 — Referee: Written-First Collection

### 6.1 Channel strategy

Both channels at T+0 (email carries the full Art 14 notice; SMS carries the short version + link). Research: SMS has ~98% open rates; email is the notice vehicle and the desktop path. Message content is strictly neutral and service-shaped — no promotional line, ever (a marketing line would convert a lawful service message into regulated direct marketing).

Operational note (not UX copy): the SMS Sender ID must be ComReg-registered before launch or messages arrive labelled "Likely Scam" — fatal to the funnel. Sender IDs are max 11 chars and "RightTenantry" is 13, so the registered sender is **RTenantry** (decided at review, §15).

### 6.2 Invitation email (real copy)

> **Subject:** Aisling O'Brien listed you as a referee — a 5-minute form
>
> Hi Colm,
>
> Aisling O'Brien has applied to rent a home and gave us your details as her previous landlord.
>
> The landlord uses RightTenantry to collect references. Could you confirm a few details about Aisling's tenancy? It's a short form — about 5 minutes, no account needed, works on any phone.
>
> **[ Complete the reference ]**
>
> The link is unique to you and expires in 10 days.
>
> **Don't know Aisling, or don't want to take part?** [Decline here] — we'll stop contacting you and let the landlord know. No reason needed.
>
> ---
>
> **Your data, in plain terms.** We got your name and contact details from Aisling O'Brien. The landlord, {landlord_display_name}, is the data controller; RightTenantry processes your answers on their behalf to verify this application (lawful basis: legitimate interest). Your answers are shared with the landlord as part of Aisling's application, kept only as long as the application is retained, and never used for marketing. You can see, correct, delete, or object to your data at any time — details and contact routes: {privacy_notice_url}.

### 6.3 Invitation SMS (real copy)

> Hi Colm — Aisling O'Brien gave us your details as a referee for a rental application. Can you confirm a few details in a 5-min form? {form_url} From RightTenantry for the landlord. Info & your rights: {notice_url} Reply STOP to opt out.

### 6.4 Reminders (real copy)

**Reminder 1 (T+48h), email + SMS:**

> **Subject:** Still happy to help Aisling O'Brien? 5 minutes
>
> Hi Colm — a quick reminder about the reference form for Aisling O'Brien's rental application. If you've already started, the same link picks up where you left off: {form_url}
>
> Not able to help? [Decline] and we'll stop contacting you.

> SMS: Reminder: Aisling O'Brien's reference form takes about 5 min: {form_url} — RightTenantry. To stop these messages: {decline_url} or reply STOP.

**Reminder 2 (T+96h), final:**

> **Subject:** Last message from us — reference for Aisling O'Brien
>
> Hi Colm — this is our last message about Aisling O'Brien's application. If the timing is bad or you'd rather not take part, that's fine: [decline here] and we'll close this off. Otherwise the form is here until {expiry_date}: {form_url}
>
> After this we'll simply let the landlord know we couldn't reach you.

### 6.5 The referee form

**Form factor:** public SSR page (same stack and form patterns as the tenant application form), mobile-first, single column, no login — the signed link *is* the authentication. Low-density spacing per the design system (`space-y-4`, inputs `h-12`, max width `48rem`).

**Landing screen (before any question):**

```
┌─────────────────────────────────────┐
│  Reference for Aisling O'Brien      │
│                                     │
│  You're listed as a previous        │
│  landlord. Aisling applied to rent  │
│  a home, and the landlord asked     │
│  RightTenantry to collect this      │
│  reference.                         │
│                                     │
│  About 5 minutes · 11 questions ·   │
│  answers saved as you go            │
│                                     │
│  Your answers go to the landlord    │
│  as part of Aisling's application.  │
│  We keep them only as long as the   │
│  application is kept. Your rights   │
│  and our contact details:           │
│  privacy notice ↗                   │
│                                     │
│  [ Start ]                          │
│                                     │
│  Not Colm, or don't know Aisling?   │
│  Let us know →                      │
│  Rather not take part? Decline →    │
└─────────────────────────────────────┘
```

The landing screen *is* the second Art 14 moment (context, purpose, retention, rights link) and carries both escape routes — required because the form is where a wrong-number or unwilling referee actually lands.

**Question spine — mapped to the `verification` block** (per-slot sets below). Interaction rules:

- One question per screen on mobile (progressive disclosure, Typeform-style — same pattern as the tenant form); a single scrolling page on desktop.
- **Autosave per answer** (server-side) — an abandoned form still yields `partial` data, and reminders resume at the next unanswered question. Unanswered fields stay `null`/`unknown` in the contract and render as "Not answered" to the landlord.
- As-stated checks pre-fill from the application: the referee confirms or corrects — that's `tenancy_period.as_stated` and `rent_amount_confirmed`.
- No paste-blocking (accessibility); completion time and device signals are *recorded* for `fraud_signals.form_session`, never used to interrupt the referee.
- Optional fields marked "(optional)" in slate; everything else required per the form conventions.

**Previous-landlord set (10 questions):**

| # | Question | Control | Maps to |
|---|---|---|---|
| 1 | "Are you {referee_name}?" | Yes / No (No → wrong-person path, §8.3) | `identity_confirmed` |
| 2 | "What was your relationship to {applicant_first_name}?" | Their landlord · Letting agent for the property · Other (short text) | `relationship_to_applicant` |
| 3 | "Did {applicant_first_name} rent a property from you?" | Yes / No / Not sure | `tenancy_confirmed` |
| 4 | "The application says the tenancy ran {from} to {to}. Is that right?" | About right / The dates differ → two month-year fields | `tenancy_period` (+`as_stated`) |
| 5 | "The application says the rent was €{amount} a month. Is that right?" | About right / It was different → amount field / Don't remember | `rent_amount_confirmed` |
| 6 | "How was the rent payment record?" | Always on time / Mostly on time / Often late / Don't know | `rent_payment_record` |
| 7 | "How was the property looked after?" | Excellent / Good / Fair / Poor / Didn't see it after | `property_condition` |
| 8 | "Was proper notice given before leaving?" | Yes / No / Tenancy is ongoing / Don't know | `notice_given_properly` |
| 9 | "Was the deposit returned?" | In full / Partly / Withheld / Still held / Don't know | `deposit_returned` |
| 10 | "Would you rent to {applicant_first_name} again?" | Yes / No / Unsure / Prefer not to say | `would_rent_again` |
| 11 | "Anything else the landlord should know? (optional)" | Free text, 1,000 chars | `free_text_signals` |

**Employer set (8 questions):** 1. identity · 2. relationship (Manager / HR / Colleague / Other) · 3. "Does/did {name} work at {employer_name}?" · 4. employment period as-stated check · 5. role title as-stated check ("The application says their role is {title}. Right?") · 6. salary as-stated check ("The application says their salary is €{amount} a year. Is that right?" — About right / It was different → amount field / Don't know; added at review, maps to the employer-variant `salary_confirmed` field — §15) · 7. "Would you rehire them?" (Yes / No / Unsure / Prefer not to say) · 8. free text (optional).

**Character set (5 questions):** 1. identity · 2. relationship + capacity (short text) · 3. "How long have you known {name}?" (ranges) · 4. "Is there anything you'd want a landlord to know about {name}?" (free text, required — this *is* the character reference) · 5. "Would you stand as a referee for them again?" (Yes / Unsure / Prefer not to say).

Schema note: the `verification` block is landlord-shaped, and at review the contract decision landed on **per-slot field variants** (§15): the employer set maps to `employment_period` (+ as-stated), `role_confirmed`, `salary_confirmed`, `would_rehire`; the character set maps to `relationship` (+ capacity), `known_duration`, `character_statement`. Identity, as-stated checks, a judgement question, and free text stay uniform across slots.

**Thank-you screen:**

```
┌─────────────────────────────────────┐
│           ✓ (teal)                  │
│  Thank you — that's everything.     │
│                                     │
│  Your answers go to the landlord    │
│  as part of Aisling O'Brien's       │
│  application. You won't receive     │
│  more messages about this.          │
│                                     │
│  Questions about your data, or      │
│  want your answers removed?         │
│  {privacy_notice_url}               │
└─────────────────────────────────────┘
```

### 6.6 Decline, objection, and wrong-person routes

| Route | Entry points | Result |
|---|---|---|
| **Decline** (`refused`) | "Decline" link in every email/SMS + landing screen | Confirmation screen ("Understood — we've told the landlord and won't message you again."), optional one-line reason (not required), all messages stop, landlord sees **Declined to take part** |
| **Objection** (`objected`) | SMS STOP · "don't contact me" via any channel | Immediate hard stop on **every** channel — no reminders, no retries, no co-nudge about that referee. Objection logged with timestamp (Art 21 evidence). Landlord sees **Declined contact**. Applicant may substitute a different referee (§8.3, landlord-driven in v1) |
| **Wrong person / don't know applicant** | Landing screen link, decline-with-reason | Marked as wrong contact → **applicant-correction loop** (§8.3), never a retry to the same details |

### 6.7 Journey B — Colm completes it (climax beat: done before the kettle boils)

1. Tuesday 21:40, Colm sees the SMS (the email went to a folder he never checks). He taps the link on the couch.
2. Landing screen tells him who's asking and why — "answers saved as you go" lowers the commitment. He taps Start.
3. Ten single-tap questions; the rent amount is pre-filled and he just confirms. The free-text he skips.
4. **4 minutes 10 seconds: thank-you screen, and he never hears from us again.** The landlord sees a structured, signal-checked reference the next morning — Colm never had to take a call.

---

## 7. Flow 3 — Landlord: Reference Panel

### 7.1 Placement

New right-column card on application detail (v3 layout), **below Applicant Information, above Audit Trail** — it's the most time-sensitive workspace item. Mobile stack order: immediately after Applicant Information (position 8, pushing Audit Trail down). Nothing renders full-width below the grid (v3 rule).

Visibility: the card renders whenever the application has reference data (always, post-Apr-2026 forms) — even in the `off` state, because the off-state content (referee contact details + honest framing) is exactly what a landlord doing manual contact needs.

### 7.2 Panel wireframe (desktop)

```
┌──────────────────────────────────────────┐
│  Reference Checks (3)                    │
│  ─────────────────────────────────────── │
│  Starts automatically when you shortlist │
│  Aisling.  [ What this tells you ▾ ]     │
│                                          │
│  Colm Byrne · Previous landlord          │
│  ● Invitation sent — Tue 10:04           │
│                                          │
│  Sarah Daly · Employer                   │
│  ● Reference received — Wed 14:22   [▾]  │
│  ┌────────────────────────────────────┐  │
│  │ "Confirmed 2.5-year tenancy; rent  │  │
│  │  always on time; would rent        │  │
│  │  again."                           │  │
│  │                                    │  │
│  │  Tenancy confirmed    Yes          │  │
│  │  Period               As stated    │  │
│  │  Rent                 As stated    │  │
│  │  Payment record       Always on…   │  │
│  │  …                    [ Show all ] │  │
│  │                                    │  │
│  │  Worth knowing (1)                 │  │
│  │  · Form completed unusually fast   │  │
│  │    (under 2 minutes). Can happen   │  │
│  │    when someone's prepared — worth │  │
│  │    a direct conversation.          │  │
│  │                                    │  │
│  │  Confidence: medium · AI-generated │  │
│  │  summary — verify before relying.  │  │
│  │  [ View attempt log ]              │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Maeve O'Brien · Character               │
│  ● Queued                                │
└──────────────────────────────────────────┘
```

### 7.3 Panel chrome

| Element | Spec |
|---|---|
| Card | `bg-white rounded-xl shadow-xl shadow-[#1B2A4A]/5 p-6` (v3 card) |
| Heading | "Reference Checks ({n})" — `font-headline text-xl font-bold text-[#1B2A4A]` |
| Sub-line | One line of expectation-setting that tracks the panel's state (see copy, §10.3) |
| "What this tells you ▾" | Collapsible explainer (§7.8) — collapsed by default, per-user dismissed state |
| Reference row | Name + slot label (`text-sm`), status pill + timestamp (`text-xs text-slate`), expand chevron when there's detail |
| Per-row overflow (`⋯`) | Context actions per state: *Start this check now* (queued) · *Skip this reference* (queued) · *Ask Aisling to nudge* (waiting states, pre-nudge) · *Take over manually* (waiting states + unreachable) · *Export attempt log* (any started state) |
| `data-testid` | `refcheck-card`, `refcheck-row-{slot}`, `refcheck-status-{slot}`, `refcheck-expand-{slot}`, `refcheck-overflow-{slot}` |

### 7.4 State-by-state content

**Off (attestation declined):**

> **Automatic checks are off for this application.**
> Aisling chose not to have referees contacted automatically. Their details are below if you'd like to reach out yourself.
> [Referee names + contact chips — same chip treatment as v2 header contacts]

No re-ask button, no "convince them" affordance. This state is the honest decline branch: the manual flow, first-class.

**Queued (pre-shortlist):** "Starts automatically when you shortlist Aisling." Overflow: *Start this check now* (per reference — a landlord may want the previous-landlord check before shortlisting), *Skip this reference*.

**Wireframe — manual trigger (existing v3 `⋯` overflow-menu pattern, same as saved notes):**

```
  Maeve O'Brien · Character                          [⋯]
  ● Queued — starts when you shortlist Aisling
          ┌─────────────────────────────────┐
          │  Start this check now           │  → sends the invite now
          │  Skip this reference            │  → excludes from auto-start
          └─────────────────────────────────┘
```

Choosing *Start this check now* asks once, inline (brand pattern — the invite is external-facing): "Start the reference check for Maeve O'Brien? We'll email and text her the form now." [ Start check ] · Never mind. The row then moves to **Invitation sent**.

**Invitation sent / Reminder sent / Form opened:** status pill + timestamp; expand shows a mini timeline of what has happened so far and what happens next ("Next reminder in ~2 days if there's no reply"). Overflow: *Ask Aisling to nudge* (disabled with "Already asked {date}" once the T+24h auto-nudge has fired), *Take over manually*.

**Reference received (form_completed):** expanded by default on first view, collapsed on return:

- **Headline** (from `ai_summary.headline`) as a pull-quote, amber left border (the v3 hero-narrative treatment).
- **Key facts table** — the `verification` fields as definition rows: Tenancy confirmed / Period / Rent / Payment record / Property condition / Notice / Deposit / Would rent again / Relationship. Values rendered in words ("As stated", "Always on time"); unanswered fields render "Not answered" in slate — never hidden, never guessed.
- **Notable quotes** (up to 3, from `ai_summary.notable_quotes`) — special-category content redacted upstream before display (architecture rule).
- **Worth knowing** — fraud-signal block (§7.5), rendered only when ≥1 signal.
- **Confidence line**: "Confidence: {high|medium|low} · AI-generated summary — verify before relying on it." (Existing AI-disclaimer pattern, verbatim.)
- **Attempt log** link (§7.6).

**Partially completed:** same layout as received, plus a top line: "Colm answered {m} of {n} questions, then stopped. We've sent a reminder to finish." Confidence capped at medium (architecture rule) and stated.

**Contact details didn't work (awaiting_correction):**

> **We couldn't reach Colm at these details.** Check with Aisling, update them here, and we'll send the invitation again.

The landlord confirms the right details with the applicant directly (applicant contact chips render inline), edits the referee trio in place (§8.3), and re-triggers the invite. One correction cycle; if the corrected details also fail, the reference converts to **Couldn't be reached** with a `referee_number_wrong`-style flag available to the fraud lens (architecture).

**Couldn't be reached (unreachable):**

> **We couldn't reach Colm.**
> Invitation, 2 reminders, and an applicant nudge over 6 days — no reply. That happens, and it isn't a mark against Aisling.
> **[ Take over manually ]** — you'll get his details and the full attempt log to reference in your own message.

**Declined to take part (refused):**

> **Colm chose not to take part.** Nothing was collected. People decline for all sorts of reasons — this tells you nothing about Aisling.
> You can ask Aisling for another referee, or contact Colm directly.

**Declined contact (objected):**

> **Colm asked us not to contact him.** All automated contact has stopped. This tells you nothing about Aisling.
> You can ask Aisling for another referee.

Objection is deliberately *more* terminal in tone than decline: no "contact directly" suggestion — the referee exercised a legal right, and the UI must not route around it.

**Skipped by you:** slate, no timestamps. "You skipped this reference." Overflow: *Start this check* (re-enable).

**Something went wrong (failed):** "The check hit a problem on our side — not Aisling's. [ Try again ]". Follows the brand error tone (protective, no blame).

### 7.5 Fraud signals — "Worth knowing"

Decision-support framing, mechanically enforced by copy and styling rules:

| Rule | Spec |
|---|---|
| Block name | **"Worth knowing"** — never "Fraud", "Risk", "Warning", or red styling |
| Placement | Inside the completed/partial reference detail, below key facts |
| Styling | `border-l-2 border-amber-400`, calm prose (the v3 insight treatment) — the same register as "What we noticed" |
| Per-signal anatomy | Signal statement (plain) + innocent-explanation clause + suggested action. One sentence each, `text-sm` |
| Header line | "Signals are clues, not verdicts. Every one has an innocent explanation. The call is yours." |
| Never | Auto-verdicts, score changes, red badges, counts-as-demoted applicants. In v1 nothing here touches the score (re-score is v2) |

Signal copy (schema field → landlord-facing sentence):

| `fraud_signals` field | Copy |
|---|---|
| `form_session.completion_seconds` low | "Completed unusually fast (under 2 minutes). Can happen when someone's prepared — or when answers were ready-made. Worth a direct conversation." |
| `form_session.ip_matches_applicant` / `device_fingerprint_match` | "Filled in from the same connection or device as the applicant's. Innocent when they're together — but a referee's answers should be their own." |
| `form_session.geo_vs_claimed_property: inconsistent` | "Filled in from a location that doesn't match the property's area. People move and travel — treat as a prompt to verify, not a verdict." |
| `voip_or_burner` / `line_type: voip` | "The contact number is an internet (VoIP) number. Plenty of legitimate users — but it's also how a temporary number looks." |
| `contact_duplicate_of_applicant` | "The referee's contact details match the applicant's own. Usually a copy-paste slip — confirm directly with the applicant." |
| `contact_reused_within_application` | "The same number appears for two different referees on this application. Worth asking the applicant about." |
| `contact_reused_across_applications` | "This number has appeared under a different referee's name on another application. Rare innocently — worth a careful look." |
| `flags: evasive_on_dates / could_not_confirm_rent_amount` | "Couldn't confirm key details ({detail}). A poor memory is normal; a coached referee often struggles with specifics too." |

### 7.6 Attempt log

Expandable timeline per reference (same timeline visual language as the Audit Trail):

```
  ● Invitation sent — email + SMS     Tue 29 Jul, 10:04
  ● Form opened                       Tue 29 Jul, 21:12
  ● Reminder 1 sent                   Thu 31 Jul, 10:00
  ● Reminder 2 sent                   Sat 2 Aug, 10:00
  ● Applicant asked to nudge          Wed 30 Jul, 10:00
  ● Closed — no reply                 Mon 4 Aug, 10:00
```

**Export:** *Export attempt log* copies a plain-text version (reference, timeline, outcome, signals) to the clipboard with a toast ("Attempt log copied — paste it into your records or a message."). Rationale: referencing evidence ends up in deposit disputes and insurance conversations; the landlord's own records are the right home for it. Clipboard-only in v1 — no file download (decided at review, §15).

### 7.7 Warm handoff (manual fallback)

*Take over manually* (from unreachable or any waiting state) replaces the row's action area with an inline confirmation (brand pattern: inline, never modal):

> **Take over this reference yourself?**
> Automated messages stop, and Colm's details + the attempt log are yours. If he completes the form anyway, it still shows up here.
> [ Take over ] · Never mind

On confirm: automated contact ceases (gracefully — a form already in progress may still complete, and a late completion simply updates the panel and notifies the landlord), the referee's contact chips render inline, and the attempt-log export sits beside them. State label: "You're handling this one".

### 7.8 "What this tells you" (expectation-setting)

Collapsed-by-default explainer at the top of the panel. Real copy:

> A completed reference means the person at the contact details Aisling gave confirmed the facts shown. It doesn't prove that person is who they say they are, and a determined applicant can coach a referee. Treat references as one input alongside the analysis, the documents, and your own judgement — the final call is always yours.
>
> References here are collected in writing (a secure form). Nobody is called, and nothing is recorded.

The last paragraph is deliberate honesty about what v1 *is* — and the natural seam for the v2 voice upsell (§14).

### 7.9 Landlord notifications

New entries in the existing notification system, brand-voiced, no exclamation marks:

| Event | Copy |
|---|---|
| Reference received | "Reference received: Colm Byrne for Aisling O'Brien." |
| Unreachable | "Couldn't reach Colm Byrne (Aisling O'Brien's referee). You can take over from the application page." |
| Declined | "Colm Byrne declined to give a reference for Aisling O'Brien." |
| Objected | "Colm Byrne asked not to be contacted about Aisling O'Brien's application." |
| Late completion after handoff | "Colm Byrne completed the reference form after all — it's on Aisling O'Brien's application." |

### 7.10 Journey C — Niamh decides (climax beat: the answer was already there)

1. Niamh shortlists Aisling at 21:08. Behind the scenes, three invitations go out. The panel reads "Invitation sent" — she does nothing.
2. Wednesday morning over coffee: "Reference received — Colm Byrne". The headline confirms the tenancy and the payment record. One "Worth knowing" signal (fast completion) — she reads the innocent-explanation line and files it as a question for the viewing, not a rejection.
3. Sarah (employer) hasn't replied by Saturday. Panel: "Couldn't be reached — Take over manually." Niamh taps it, exports the attempt log into her records, and emails Sarah's HR address herself.
4. **The panel told her the truth at every step — including the states that say "this tells you nothing about Aisling" — and the weekend ended with more certainty than a week of phone tag would have produced.**

---

## 8. Edge States (designed explicitly)

### 8.1 Applicant won't attest
Covered: §5.3 (No path) + §7.4 (Off state). Feature off, manual flow first-class, no nagging, no score treatment.

### 8.2 Referee declines / objects
Covered: §6.6 + §7.4. Decline = polite terminal (`refused`); objection = hard stop everywhere (`objected`), timestamp-logged, landlord sees "Declined contact" with no route-around suggestion. Substitution after either is **landlord-driven and manual** in v1 (decided at review, §15): the landlord asks the applicant for another referee and edits the slot (§8.3). A self-serve applicant link is a v2 hook (§14).

### 8.3 Wrong contact details → landlord-driven correction (one cycle)

Trigger: wrong-person route (§6.6) or hard delivery failure (invalid email/number). **Never** re-contact the same details — the third party never received the Art 14 notice, and repeated messages to them are both a fairness problem and a nuisance (architecture rule).

**v1 flow (decided at review — no applicant self-serve):**

1. The panel state (§7.4) tells the landlord exactly what failed — "email bounced" / "the person who replied doesn't know Aisling" — and renders the applicant's contact chips.
2. The landlord contacts the applicant on their own channel, confirms the right details (or asks for a substitute referee), and **edits that slot's trio inline** (audit-logged; the applicant's verbal/message confirmation is the forewarning the attestation evidences, so no re-attestation step).
3. Saving re-triggers the invitation to the corrected details; the attempt log carries the full history.

One correction cycle; second failure → **Couldn't be reached** with a `referee_number_wrong`-style flag available to the fraud lens. The same manual path covers referee substitution after decline/objection (§8.2).

**Wireframe — edit + re-trigger (inline, in the reference row):**

```
  We couldn't reach Colm at these details.
  Check with Aisling, update them here, and we'll try again.
  ┌───────────────────────────────────────────────┐
  │  Name    [ Colm Byrne          ]              │
  │  Email   [ colm.byrne@…        ]              │
  │  Phone   [ +353 87 …           ]              │
  │                          [ Save & resend ]    │
  └───────────────────────────────────────────────┘
  Contact Aisling:  [📞 087…] [✉ aisling@…]       
```

### 8.4 Partial / abandoned form
Autosave per answer (§6.5). Abandoned-with-answers → reminders resume at the next question; terminal silence → `partial`, landlord sees answered fields with "Not answered" on the rest, confidence capped at medium. Abandoned-with-zero-answers → reminders continue → `unreachable`.

### 8.5 Expired link
Link TTL: 10 days from invitation (decided at review, §15). Landing page on expiry:

> **This link has expired.**
> Links last 10 days so old messages can't be reused. If you still want to give this reference, we can send a fresh one.
> [ Send me a new link ] — re-sends to the referee's email/phone on file, only if the check is still open.

If the reference is already terminal, the page says so instead ("This reference was already completed." / "…was declined." / "The landlord is handling this reference directly.") — no dead ends.

### 8.6 Late completion after handoff
Form links stay valid through warm handoff (§7.7). A completion after takeover updates the panel and notifies the landlord (§7.9). The referee is never told the landlord "gave up" — the thank-you screen is identical.

### 8.7 Referee for multiple applicants / duplicate slots
Same person legitimately refereeing twice (e.g. a letting agent) is a known pattern; the reuse *signals* (§7.5) are scoped and explained so legitimate reuse isn't styled as fraud. No referee-side account or de-dup UI in v1.

### 8.8 Landlord-trigger failures
Email bounces / SMS undelivered at T+0 → treated as wrong contact (§8.3), not retried blindly.

---

## 9. Legal Obligations → UI Moments

| Obligation (source: `research/heist-535/legal.md`) | Where it lands in this spec |
|---|---|
| **Art 13 transparency — applicant** | Attestation block copy (§5.3): what's shared, what happens, referee rights; privacy-notice link in-section. Recorded as `reference_contact_attestation` on `acknowledgement_record` — an acknowledgement, *not* a consent type |
| **Art 14 notice — referee, "at the latest at the time of the first communication"** | Invitation email carries the full plain-language notice block: controller identity ({landlord_display_name}), RightTenantry as processor, source (the applicant), purpose + legitimate-interest basis, retention, rights incl. objection, notice URL (§6.2). SMS carries the short version + notice link (§6.3). Form landing re-states it before any question (§6.5) |
| **Art 21 right to object** | Decline/objection routes in *every* message and on the form landing (§6.6); SMS STOP honoured; hard stop across all channels; timestamped evidence; landlord truth-state ("Declined contact", §7.4) with no route-around affordance |
| **Recording disclosure** | **N/A in v1** — no voice, no recording. Stated explicitly in the landlord explainer (§7.8) |
| **EU AI Act Art 50** | **N/A in v1** — no AI interacts with the referee. The *landlord-facing* AI summaries carry the existing "AI-generated — verify" disclaimer (§7.4) per house pattern |
| **Art 22 / decision-support framing** | Fraud-signal rules (§7.5: clues-not-verdicts, innocent explanations, no auto-anything); expectation-setting explainer (§7.8: "the final call is always yours"); v1 never changes the score |
| **Lawful basis discipline (legitimate interest, LIA)** | The word "consent" appears nowhere in referee- or applicant-facing copy about contact; attestation wording records transparency/forewarning, not permission (§5.3) |
| **Service-message discipline (ePrivacy)** | Referee comms contain zero promotional content (§6.1) — the legal difference between a service message and regulated direct marketing |
| **Data minimisation** | Form collects only the `verification`-mapped fields; free text optional; special-category content redacted before display (§7.4, architecture rule) |
| **Retention** | Referee notice states retention in plain terms ("kept only as long as the application is retained", §6.2); `retention_class`/`purge_after` on rows per architecture — no UI surface needed in v1 |

Two items remain **[LEGAL REVIEW]** for counsel, unchanged from the research: the Art 14 notice + LIA wording pack, and the Annex III 5(b) high-risk classification memo for the screening pipeline. This spec's copy is written to be counsel-reviewable as-is.

---

## 10. Copy Deck (consolidated)

All copy follows the brand voice: calm confidence, specific, statements not exclamations, no emojis, no "Error"/"Failed" language, contractions natural.

### 10.1 Applicant-facing

| Context | Copy |
|---|---|
| References section intro | "Your references" / "Give details for people who know you as a tenant, employee, or personally. If you're happy for us to, we'll check these references for the landlord — see the choice at the end of this section." |
| Attestation heading | "Contacting your referees" |
| Attestation body | (§5.3 wireframe, verbatim) |
| Attestation option 1 | "Yes — my referees expect to be contacted" / "They've agreed to act as my referees and know they'll hear from RightTenantry." |
| Attestation option 2 | "No — don't contact my referees automatically" / "The landlord will see my references and can contact them directly instead." |
| Attestation footer | "Either choice is fine. It changes how references are checked, not how your application is shown." |
| Attestation validation error | "Choose one option to continue." |
| Confirmation page (Yes path) | "We'll contact your referees shortly — a quick word from you that we're legitimate makes a real difference." |
| Co-nudge email (auto, T+24h) | Subject: "A quick word to {referee_first_name} helps your application" / "Hi {applicant_first_name} — we've invited {referee_name} to complete your reference, but haven't heard back yet. A quick message from you ('expect a text from RightTenantry, it's legitimate') makes a real difference. No action needed beyond that — we'll keep the process moving." |
| Correction email (wrong contact) | §8.3, verbatim |

### 10.2 Referee-facing

| Context | Copy |
|---|---|
| Invitation email | §6.2, verbatim |
| Invitation SMS | §6.3, verbatim |
| Reminder 1 / Reminder 2 | §6.4, verbatim |
| Landing screen | §6.5 wireframe, verbatim |
| Questions | §6.5 tables (per-slot sets) |
| Decline confirmation | "Understood — we've told the landlord and won't message you again about this." + optional reason: "If you'd like to say why (one line, optional): [text] [Send]" |
| Objection confirmation | "Done — no more messages from us. We've recorded that you don't want to be contacted about this application." |
| Wrong-person confirmation | "Thanks for letting us know — we'll check the details with the applicant and won't contact you again about this." |
| Thank-you screen | §6.5, verbatim |
| Expired link | §8.5, verbatim |

### 10.3 Landlord-facing

| Context | Copy |
|---|---|
| Panel heading | "Reference Checks ({n})" |
| Panel sub-line, pre-shortlist | "Starts automatically when you shortlist {applicant_first_name}." |
| Panel sub-line, in flight | "We invite, remind, and nudge — you watch it happen." |
| Panel sub-line, all terminal | "All references closed. Summaries and logs stay here." |
| Status labels | §4.2 table |
| Off state | §7.4, verbatim |
| Unreachable / Declined / Objected / Failed states | §7.4, verbatim |
| "What this tells you" | §7.8, verbatim |
| "Worth knowing" header | "Signals are clues, not verdicts. Every one has an innocent explanation. The call is yours." |
| Signal sentences | §7.5 table |
| Warm-handoff confirm | §7.7, verbatim |
| Export toast | "Attempt log copied — paste it into your records or a message." |
| Notifications | §7.9 table |
| Disclaimer line (completed summary) | "Confidence: {level} · AI-generated summary — verify before relying on it." |

---

## 11. Responsive Behaviour

| Surface | Mobile (<768px) | Desktop (≥1024px) |
|---|---|---|
| Referee form | One question per screen, progress indicator, large single-tap controls (`h-12` minimum), sticky Continue | Single scrolling page, `max-w-[48rem]` centred, same question order |
| Attestation block | Full-width card in the References section flow, radios stacked | Same, within the `48rem` form column |
| Reference panel | Stacks after Applicant Information (position 8 in the v3 mobile order); rows full-width; expanded detail inline | Right column, below Applicant Information, above Audit Trail |
| Attempt log | Same timeline, timestamps wrap under event text | Single-line rows |

Referee-form thumb targets: answer options are full-width tappable rows, not small radio circles. Free-text uses `resize-y` textareas with character counters (house pattern).

---

## 12. Accessibility

| Element | Requirement |
|---|---|
| Referee form | One-question-per-screen reduces cognitive load; progress announced (`aria-label="Question 4 of 11"`); no session timeout (autosave); no paste-blocking; visible focus ring (`ring-2 ring-amber-400 ring-offset-2`) |
| Attestation radios | `role="radiogroup"`, `aria-required="true"`, help text linked via `aria-describedby`; error announced on submit-scroll |
| Reference panel | `role="region"`, `aria-label="Reference checks"`; each row a button with `aria-expanded` + `aria-controls`; status pill text always paired with colour (never colour-only) |
| Attempt log | `role="list"` timeline, timestamps in `<time datetime>` |
| "Worth knowing" | Amber accent is decorative; signal content is text-first (no meaning in colour) |
| Decline/objection routes | Reachable without completing anything; keyboard-operable from every message link; no confirmation traps on decline |
| Contrast | Inherits the brand palette's WCAG 2.1 AA pairings; "Not answered" slate meets AA at its size |

---

## 13. Design System Alignment

- **Components reused, not invented:** `view_form_section` / `view_form_field` (referee form + attestation), `view_consent_block` anatomy (attestation card), v3 card + right-column growth rules (panel), Audit Trail timeline language (attempt log), v2 contact chips (off-state + handoff referee details), hero-narrative amber-left-border treatment (headline quote + Worth knowing), existing notification system, existing skeleton-shimmer loading (panel loads).
- **Button hierarchy preserved:** one amber primary per context (referee form: Continue/Submit; panel: none by default — actions live in overflow menus or inline confirms), destructive never filled (Skip reference is ghost, warm handoff is navy-outline secondary).
- **Colour semantics preserved:** status pills map to the house semantic set (received = teal; waiting/queued = slate; reminder/opened = navy; needs-attention states (unreachable/awaiting correction) = amber; declined/objected = slate, *not* red — refusal is not an error).
- **Voice preserved:** no exclamation marks, no emojis, specific numbers ("2 reminders over 6 days"), outcome-leads-AI-supports.

---

## 14. Forward Contract (v2 hooks — design-only, nothing built)

- **Voice door:** the three-door model (form / book a call / speak now) is the research's end-state; v1's invite and landing are structured so a "Prefer to talk? Book a short call" option can be added without restructuring (new second action beside Start on the landing; new door in the invite email).
- **Re-score (v5 additive field):** when `reference_call_results[]` ships, the panel's completed-reference data is already `verification`-shaped; the UX delta is a "references now inform the score" line in the explainer + CategoryNote surfacing — no panel redesign.
- **Recording/Art 50 copy:** v1 copy never promises "no calls, ever" — it says "References here are collected in writing" (§7.8), true now and cleanly revisable per-vacancy later.
- **Applicant self-serve correction/substitution (v2 hook):** designed in review round 1, cut for v1 in favour of the landlord-driven manual path (§8.3). The cut design — preserved for v2 — is a single-use signed email link to a minimal per-slot edit page (that slot's trio only), with re-attestation implicit on save. The cut applicant email read: *"Hi Aisling — we tried to contact {referee_name}, the referee you listed as {slot_label}, but the details didn't reach the right person. Could you check and update them? {correction_link} This link works once."* The v2 trigger for building it is landlord-support load from manual relays.
- **Employer/character schema variants** were decided at review (per-slot variants, §15): question sets map onto named per-slot fields in the contract.

---

## 15. Review Decisions

All open questions were decided across two lavish review rounds (2026-07-29 — Moses):

| # | Question | Decision | Where applied |
|---|---|---|---|
| OQ-1 | Trigger point | **Auto-queue on shortlist + manual "Start now" early** (as spec'd); shortlist fires per-application | §4.3, §7.4 |
| OQ-2 | Employer/character `verification` mapping | **Per-slot field variants** — employer: `employment_period`, `role_confirmed`, `salary_confirmed`, `would_rehire`; character: `relationship`, `known_duration`, `character_statement` | §6.5 |
| OQ-3 | Substitution & correction mechanics | **Landlord relays corrections manually — no applicant self-serve in v1** (landlord contacts the applicant, edits the trio inline, re-triggers; audit-logged) | §7.4, §8.2, §8.3, §14 (self-serve deferred to v2), §17 |
| OQ-4 | Cadence & TTL constants | **Accepted as spec'd:** co-nudge T+24h / reminders T+48h+T+96h / unreachable T+144h / link TTL 10 days | §4.3, §8.5 |
| OQ-5 | Attempt-log export format | **Clipboard plain text only in v1** | §7.6 |
| OQ-6 | SMS Sender ID | **RTenantry** (ComReg ≤11 chars); from-domain follows the existing transactional setup | §6.1 |
| OQ-7 | Parallel vs sequential slots | **All references in parallel at trigger** (as spec'd) | §7.4 (Queued) |
| OQ-8 | `refused` vs `objected` naming | **Form decline → `refused`; STOP/objection → `objected`** (as spec'd) | §4.2, §6.6, §7.4 |
| OQ-9 | Salary confirmation on employer set | **Include as an as-stated confirm question** (employer set is now 8 questions) | §6.5 (employer set) |
| OQ-10 | Landlord display name to referees | **Use the landlord's real/profile name** — already exposed to applicants | §6.2 (`{landlord_display_name}`) |
| OQ-11 | From-domain for referee email | **Send from the existing verified transactional domain** (`references@righttenantry.ie`) — no new Resend domain needed; Resend supports multiple domains, so future isolation is DNS-config only | §6.1 |

All eleven questions are decided; nothing remains open for the architecture workstream from this spec. (The two **[LEGAL REVIEW]** items — Art 14 + LIA wording pack, Annex III 5(b) memo — sit with counsel, not this document.)

---

## 16. Verification

1. Artifact exists at `_bmad-output/planning-artifacts/ux-reference-checking-v1-2026-07-29.md`; markdown renders; internal links resolve (`ux-application-detail-v3.md`, `brand-identity-and-design-system.md`, `ux-design-specification.md`, `research/heist-535/architecture.md`, `research/heist-535/fallback.md`, `research/heist-535/legal.md`, `research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md`).
2. All three flows covered with real copy: applicant (§5, §10.1), referee (§6, §10.2), landlord (§7, §10.3).
3. Every mandated edge state has an explicit design: applicant won't attest (§8.1), referee declines (§8.2), referee objects — hard stop (§8.2), wrong contact → one-cycle correction (§8.3), partial/abandoned (§8.4), expired link (§8.5).
4. Legal obligations mapped to named UI moments (§9 table); attestation is acknowledgement-not-consent; Art 14 content present in first contact; objection visible in every referee message; recording/Art 50 correctly N/A'd; decision-support framing enforced by copy + styling rules.
5. `verification`-block question mapping traceable (§6.5 tables); fraud signals map to `fraud_signals` schema fields (§7.5 table); lifecycle labels map to architecture states (§4.2 table).
6. Brand consistency: no exclamation marks, no emojis, palette/typography/component references match `brand-identity-and-design-system.md` and the v3 host spec.
7. Review decisions recorded (§15.1); no open questions remain; no invented data decisions.
8. No code files touched — PR diff contains only this artifact.

---

## 17. What's Deliberately Out of Scope

- **Voice anything.** No "speak now", no call booking, no call-status UI. v2 (RightTenantryAgents#168) owns it.
- **Re-score UX.** v1 references never change the score; the panel is display + workflow only. The v5 contract note is forward design context (§14), not a build item.
- **Referee accounts / referee-side history.** Links are single-purpose; no referee dashboard.
- **Editable message templates.** Invite/reminder copy is fixed (counsel-reviewed as a pack); per-landlord customisation is a future decision with a legal-review gate.
- **Applicant self-serve correction links.** v1 corrections and substitutions are landlord-driven and manual (§8.3 — decided at review); the signed-link applicant edit surface is v2 (§14). (Landlord-initiated referee editing is *in* scope for exactly that §8.3 flow, audit-logged.)
- **Localisation.** English-only referee surfaces in v1 (architecture: localised forms are a v2 item).
- **Downloadable attempt-log files** (clipboard-only in v1 — decided at review, §15).
- **In-product DPIA/LIA surfaces.** The DPIA and LIA are ops documents; nothing in v1 UX exposes or collects them.
