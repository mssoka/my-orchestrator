## 🤖 Perkins automated review — round 1 of 3

**Job:** righttenantry-ai-reference-calls-research · **Reviewed sha:** afdfcd6 · **Reviewers:** 7/7 completed
**Verification:** 32/34 findings confirmed against the code — 2 discarded as false-positive

The deliverable is strong: the legal refutation rests on verbatim primary text, the evidence gate passes (P0 claims 100% traced to checkable citations; gaps honestly flagged as [GAP]/UNVERIFIED), and the resume recommendation is well-supported. But the "codebase-verified" architecture thread contains one inverted fact repeated three times, plus a set of factual/consistency defects and unspecified design paths that should be corrected before this becomes the basis for the #535 decision.

### Blockers (1)

1. **`reference_verification` weight is inverted, and the cited source says the opposite** [tests, codebase, architecture] — `heist-535/architecture.md:39`, repeated in the main report (:331, :398). The docs claim `reference_verification` was "raised 0.15 → 0.20" and is the `"most critical predictor"` per `tenant_scorer/tools/scoring_tools.py`. That file actually reads `WEIGHT_REFERENCE_VERIFICATION = 0.15` (reduced in the 2026-05-04 rebalance); the 0.15→0.20 raise and the "most critical predictor" label belong to `rental_history`. A "codebase-verified" claim that misquotes its source — in the section arguing re-score ingestion is cheap — must be corrected in all three places.

### Warnings (10)

1. **Consent infrastructure claims are outdated** [codebase, architecture] — `architecture.md:24-25`, main report:322. `consent_record` was renamed to `acknowledgement_record` (column `record_type`; enum now includes `guarantor_attestation`) by migration `20260422000001`, explicitly to repudiate consent-as-lawful-basis. The proposed `reference_calling` "consent type" repeats exactly the misreading the rename was designed to prevent — and sits awkwardly next to the report's own Art 6(1)(f) recommendation.
2. **Wrong SKU in the viability economics** [architecture] — main report:424,:521 claims "RightTenantry already charges EUR 99/vacancy for AI analysis". Per `payment_sku.gleam` + CLAUDE.md, unlimited AI analysis is the €299 `VacancyUnlock`; €99 is the 14-day `VacancyExtension`. The margin conclusion only strengthens at €299, but the product fact is wrong in a codebase-grounded document.
3. **Mid-call hang-up has no outcome value or policy** [edge] — the outcome enum (`architecture.md:70`) has no `partial`; verification exists only for `completed`, and no doc says whether partial answers are kept, scored, or re-attempted.
4. **The web-form branch has no fraud-signal parity with voice** [edge] — the recommended design makes the form the completion engine, but the fraud stack covers only calls. A form link can be forwarded to a coached accomplice; the Xref/Refapp IP/device checks the doc itself cites are never applied to the form path.
5. **Referee objection/STOP does not short-circuit the escalation chain** [edge] — "refusal honoured (Art 21), STOP across channels" is asserted, but the fallback chain (reminders → applicant co-nudge → landlord warm handoff) proceeds unconditionally; nothing tells the landlord the referee objected.
6. **wrong_number/invalid_number outcomes have no applicant-correction loop** [edge] — retries would redial an uninvolved third party (who never received the Art 14 notice), and a wrong number is itself an unrouted fake-referee signal.
7. **Re-score semantics for non-completed outcomes are undefined** [edge] — field presence per outcome and how `reference_validator_agent` should treat `unreachable` (called "a real data point") are unspecified in the v5 contract.
8. **The March design is characterised inconsistently** [blind] — fallback.md Q1 validates "25–40% answer *with* SMS pre-notification" as plausible (matching the March doc's own table: SMS 30 min pre-call, then 25–40% on attempt 1), while the main report labels the March design "cold-first" and calls 25–40% "~2× reality for a cold unknown call". The strawman should be removed; compare like with like.
9. **Phenom: "first production product" vs "already a live category"** [blind] — main report:369 vs :273 (Revla, RefChecker, Virvell named as live hiring products). Unreconciled.
10. **Recordings + full transcripts stored with no retention/redaction policy** [security] — the schema and `reference_call` table persist referee voice recordings and verbatim transcripts (third-party personal data; the legal thread itself notes incidental special-category risk) with no retention period, purge rule, or redaction step.

### Notes (17)

- **Missing Table of Contents** [acceptance, architecture] — the bmad-domain-research step-06 synthesis structure mandates a `## Table of Contents`; the 659-line report has none (all ten content sections are present).
- **initial_schema.sql citation lines off** [codebase] — :75-77 covers only `landlord_ref_*`; `employer_ref_*` is :78-80, `character_ref_*` was added by the later migration (:18-20).
- **Orchestration briefs committed** [architecture] — `heist-535/brief-{legal,fallback,fraud,providers}.md` are mega-minion process prompts; no other research folder commits such artifacts.
- **Vapi "$50M Series B" uncited** [tests] — appears in both provider tables; no funding source anywhere in the diff.
- **Orphan "Art 50 grace runway ends 2 Dec 2026" claim** [blind] — fallback.md:141, sourced to two secondary blogs; uncorroborated by the legal thread's primary-text analysis (applies 2 Aug 2026; plan against it).
- **Scenario B arithmetic** [blind] — branches sum to 55–80%, stated total is "60–75% (optimistic 80%)"; the synthesis flattens to "~60–80%".
- **"Each thread file has an appendix source log / gap log" is false** [blind] — only fallback.md and providers.md do.
- **tenantreferencing.ie vs TenantReference.ie** [blind] — one thread reports a dead domain, another an operator since ~2012/2013; never reconciled.
- **Inconsistent relative cross-reference paths** [blind] — `research/heist-535/...` (unresolvable from the report's own directory) vs `heist-535/...`.
- **Employer refs behind switchboard/IVR have no traversal path** [edge] — the March 2026 doc had a Gatekeeper row; the new docs dropped it.
- **Recording-refusal branch undecided** [edge] — "stop recording or end call" left as two alternatives; transcript presence for unrecorded calls unstated.
- **Applicant attestation has no decline branch** [edge].
- **≤3-retry attempt accounting undefined** [edge] — which outcomes decrement the counter; reschedule interaction.
- **AMD misclassification unhandled** [edge] — human gets the voicemail message / voicemail gets the live agent.
- **language_barrier outcome has no handling path** [edge].
- **Within-application cross-slot number reuse unchecked** [edge] — same number as landlord AND employer ref matches neither the across-applications check nor the applicant check.
- **Advisory evidence gate: PASS** [tests] — P0 claims 100% FULL support; ~94% FULL-or-better across ~35 traced claims.

### Reviewer agreement

Highest-confidence findings (independent lenses converging): the **`reference_verification` weight inversion** (tests + codebase + architecture — blocker), the **consent_record → acknowledgement_record rename** (codebase + architecture), and the **missing Table of Contents** (acceptance + architecture).

<details><summary>Verification notes (2 findings discarded)</summary>

- "67–75% unanswered matches no other statement" (blind) — **rejected**: the figure is verbatim from the March 2026 research doc ("67-75% of calls from unknown numbers go unanswered").
- "Default Twilio media URLs are unauthenticated bearer links" (security) — **rejected as outdated**: Twilio enabled HTTP auth on media URLs by default (2023 changelog). Storing the recording SID and serving audio via an authenticated endpoint remains good practice, but the claimed default exposure no longer holds.
</details>

**Verdict:** NEEDS CHANGES

One factual inversion in the load-bearing codebase-grounded section (repeated 3×), two further wrong codebase facts (consent infra, pricing SKU), and a handful of unspecified design paths. Everything found is mechanically fixable in one pass; the research core — legal refutation, provider pick, completion model, fraud stack — stands.

_Address findings and push — I re-review automatically on the new sha. After round 3, the human takes over._
