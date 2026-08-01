# Spine Review — `architecture-reference-checking-v1-2026-07-29.md`

**Lens:** rubric walker + adversary (BMad architecture gate, feature-altitude addendum)
**Artifact:** `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md`
**Cross-refs read in full:** canonical `architecture.md` (same folder), `research/heist-535/architecture.md` (core input), `research/heist-535/legal.md` (headline sections), `research/heist-535/fallback.md` (spot).
**Code spot-checks (2026-07-29 worktree):** `middleware.gleam` (`redact_token_route` :320, `is_public_path` :275 — three-place registry claim **verified**), `application_handler.gleam:1779` (`insert_acknowledgement_records` — **verified**, incl. conditional-write precedent for `guarantor_attestation`), `20260420000003` enum-add migration (**verified**), `claim_shortlist_notification.sql` (atomic-claim precedent — **verified**), internal cron routes (`digest`, `verification-reminders` — **verified**), `dsar`/`erase` token routes (**verified**), `max_co_applicants = 3` (matches `owner_label` CHECK 0–2 — **verified**), `retention_due_at` + `retention/` module (**verified**), `client_ip` usage sites (**verified — see F4**).

---

## 1. Does it fix the real divergence points for builders one level down?

**Mostly yes — this is a genuinely strong feature-altitude spine.** The things that would actually fork a build are mostly nailed:

- Full DDL for `reference_call` (enums, partial unique live-row index, token indexes, sweep index) — builders cannot drift on table shape.
- The cadence is a table with exact T-values, channels, and recipients (AD-4); the sweep pattern is pinned to an existing house precedent.
- The token-route contract names the three registration sites explicitly (AD-3, §5.2 checklist) — the single most copy-paste-able failure in this repo is pre-empted.
- The landlord-facing contract is a JSON shape plus *server-computed* capability hooks (AD-11), which correctly prevents the UX workstream from re-deriving state rules client-side.
- Fraud scope is honesty-labelled per signal (AD-10) rather than aspirational.
- §1 records verified-current-state *and* corrects the briefing where the repo disagrees (RLS posture) — exactly what an addendum should do.
- Deferred items (§12) each carry revisit conditions; the v2-reserved register (§6.3) correctly forbids placeholder emission.

**But four divergence points that this altitude owns are NOT fixed** — and they are the load-bearing ones: the status↔outcome mapping for v1 terminals (F1), the corrected-contact storage decision (F2), the concurrency/ownership rule for the row's mutation paths (F3), and the security envelope for the new public/webhook surface (F5). Details and constructed clashing pairs below.

## 2. Is every AD's Rule enforceable?

Enforceability audit per AD:

| AD | Enforceable? | Notes |
|---|---|---|
| AD-1 (one row per slot; superset enum) | **Partially** | The enum is concrete, but the *mapping* from v1 transitions to `status`/`outcome` pairs is never tabulated, and the outcome enum's own comment ("v1 emits the first five" = `completed, partial, voicemail, no_answer, busy`) contradicts the rest of the document — those are voice outcomes; v1 emits `form_completed`, `unreachable`, `objected`, `manual_recorded`. Also: `failed` is a v1-active terminal status with **no possible outcome value** (the outcome enum lacks `failed`), while the column note says outcome is "set at terminal". A checker cannot verify AD-1 compliance without the doc saying what compliant rows look like. |
| AD-2 (attestation record_type) | **Mostly** | Enum value, migration shape, transaction site, and wording ban are all checkable. Two holes: (a) server-side behavior when the checkbox is absent is unstated (form-layer required only — hard-fail vs skip-write); (b) no rule for pre-v1 applications — shortlisting a legacy row triggers referee contact with zero attestation evidence, and nothing says block-vs-proceed. |
| AD-3 (token route) | **Yes, with one wording bug** | Three-site registration, entropy, expiry, single-submission all checkable. But "no draft persistence" contradicts "re-opening shows the empty/partial form server-rendered from state" — from *what* state? Builders will split on always-empty vs partial-restore. |
| AD-4 (cadence + sweep) | **Partially** | The cadence table is enforceable; the *ownership* of sends is not (who sends T0 — trigger or sweep? See F3 pair c), and no duplicate-send/idempotency rule exists for a 15-min tick whose DB update can fail after a successful send. |
| AD-5 (one SMS client) | **Yes** | File location, provider surface, and the rejected abstraction are all checkable. |
| AD-6 (objection short-circuit) | **Partially** | Semantics are crisp; enforceability fails at concurrency — "immediately cancels everything" is unverifiable without a terminal-stickiness/guarded-transition rule (F3 pair b). Evidence fields are specified. |
| AD-7 (one correction cycle) | **No — internally contradicted** | Requires writing the corrected contact to a row whose `contact_*` the same document declares an "immutable copy" (F2). `correction_cycles ≤ 1` is checkable; where the corrected address lives is not. |
| AD-8 (WoZ manual channel) | **Partially** | `channel: "manual"` amendment is explicit and good. But the Rule never says what `status`/`outcome` a manual entry drives, whether `record-manual` mutates the live row or creates a new one, or what happens to pending `next_attempt_at` when a manual outcome is recorded on a live row. |
| AD-9 (JSONB result, v2-reserved) | **Yes** | `schema_version` embedded, verbatim field names, absence-is-the-contract for v2 fields, deterministic structuring — all checkable. Undermined only by F7 (the verbatim claim is itself violated in two places). |
| AD-10 (fraud scope) | **Partially** | The table format is excellent; one row is factually wrong (F4) and one signal lacks a storage location for its inputs, so two rows of the table are not implementable as written. |
| AD-11 (payload + hooks) | **Mostly** | Shape and hook formulas are checkable. `can_substitute_referee` surfaces a *landlord* affordance for an action §5.7/AD-7 assign to the *applicant* (landlord-side correction was an explicitly rejected alternative) — what the hook triggers is unspecified. |
| AD-12 (v5 design-only) | **Yes** | "v1 builds none of this" + conformance guarantee is a checkable non-build rule. |
| AD-13 (trigger) | **Mostly** | Slots, character-swap, skip-empty, co-applicant deferral are checkable. Whether the trigger sends T0 or enqueues for the sweep is not (F3 pair c). |

## 3. Constructed clashing pairs — two builders obeying every AD to the letter

### F1 (HIGH) — Status↔outcome mapping: the enum the doc exists to fix is itself ambiguous

The addendum gives a 12-value status enum and a 15-value outcome enum but never tabulates which outcome accompanies each v1 terminal status. The one place it gestures at this — the outcome enum comment "v1 emits the first five" — names five *voice* outcomes, contradicting §6.2, AD-4 (T+144h → `unreachable`), AD-6 (→ `objected`), and AD-8 (→ `manual_recorded`).

- **Builder A** follows §4.5 + §6.2: form submit → `status=form_completed, outcome=form_completed`; `failed` rows get `outcome=NULL` (no value exists); manual record sets `outcome=manual_recorded` on the live row and closes it.
- **Builder B** follows the enum comment literally: form submit → `outcome='completed'` (a v2-reserved value, violating AD-1's own "v1 drives only the v1-active subset"); maps `failed` → `outcome='unreachable'` (nearest available); and, since AD-8 never says, creates a *new* row for manual entries with `status='completed'` (the only "done" status that isn't form-specific), double-counting the slot.

Both obey every written Rule. Their databases are mutually unintelligible to the §10 v5 re-score reader — the exact cross-version failure AD-1's "Prevents" line claims to kill. One mapping table (v1 terminal status → outcome, result presence, who writes it) fixes it.

### F2 (HIGH) — Immutable contact snapshot vs the correction loop

§4.1: "`contact_*` is a deliberate snapshot: the trio on `application` can be edited (correction loop) or erased; the reference_call row is the record of *who was actually contacted*." AD-7 + §4.5: a correction "restarts the sequence at T0 against the new contact" on the *same* row (`awaiting_correction → queued`). No corrected-contact columns exist.

- **Builder A** overwrites `contact_email`/`contact_phone` on correction — the immutable record the column note says is the point of the columns is destroyed; the attempt log now describes messages to an address the row no longer shows.
- **Builder B** honors immutability and adds `corrected_email`/`corrected_phone` columns (or a child row) — different DDL, different fraud-join targets (`idx_reference_call_contact_phone` indexes the *wrong* column for cross-application reuse after a correction), different API payload.

Direct contradiction inside the artifact; both readings are defensible. (Also note: the snapshot's "or erased" rationale is moot under CASCADE — the row dies with the application; the snapshot only ever survives *edits*.)

### F3 (HIGH) — Mutation-path ownership: one row, seven writers, no guard rule

Writers of a `reference_call` row: shortlist trigger (create), sweep (messages, attempt log, terminals), form POST (terminal + result), resend-events webhook (bounce → `awaiting_correction`), twilio-sms webhook (STOP → `objected`; delivery status), correction route (→ `queued` + new contact), record-manual route (AD-8). The artifact never states a concurrency or single-writer rule — despite the repo already having the exact precedent it could have cited (`claim_shortlist_notification.sql`: `UPDATE ... WHERE ... IS NULL RETURNING`, documented in `application_detail_handler.gleam:729-735`).

- **Pair (a) — sweep vs form POST.** Referee submits at T+96h−ε while the sweep processes the due reminder. Builder A's sweep re-checks status inside a guarded update (`... WHERE id=$1 AND status='contact_initiated'`); Builder B's does read-modify-write from the row it read at tick start. B's sweep overwrites `form_completed` back to `contact_initiated`, nulls the submission's attempt-log append, and the referee receives "Reminder 2 (final)" *after submitting* — plus the landlord warm-handoff for a completed reference. Same ADs, opposite systems.
- **Pair (b) — STOP vs bounce.** Twilio STOP and a Resend bounce arrive concurrently. AD-6 says objection "short-circuits everything"; AD-7 says bounce → `awaiting_correction`. Nothing orders them. Builder A makes terminal states sticky (objected wins); Builder B last-writer-wins (awaiting_correction wins → the applicant is asked to "correct" the contact of a referee who exercised Art 21 → a fresh message to an objecting referee — the precise DPC failure AD-6 exists to prevent).
- **Pair (c) — T0 ownership.** AD-4's sweep "processes rows where `next_attempt_at <= now()`"; AD-13 creates rows `queued`. Nothing sets `next_attempt_at` at creation or says the trigger sends T0 itself. Builder A sends the invite in the shortlist handler and leaves `next_attempt_at` for T+24h; Builder B sets `next_attempt_at=now()` and lets the sweep send; Builder C does both → duplicate T0 invites (the nuisance/fairness failure AD-7 cites) and a double-bumped `attempt_count` that shifts the whole cadence.
- **Pair (d) — attempts JSONB.** "Append-only" is stated as intent, not mechanism. Builder A uses `attempts = attempts || $1::jsonb` (atomic); Builder B reads, appends in Gleam, writes back. Under (a)/(b), B loses entries — the warm-handoff attempt log (a compliance-relevant artifact, §9.1/§8.3) is silently wrong.

One stated rule — "all transitions via guarded UPDATE naming the expected pre-state; terminal states sticky; attempts appended atomically; T0 sent by the sweep" — collapses all four pairs.

### F4 (MEDIUM-HIGH) — `ip_matches_applicant` is marked "Collectible today: Yes". It is not.

Verified against the worktree: nothing captures the applicant's IP at submission. `create_application.sql` has no IP column; `insert_acknowledgement_records` writes no IP; `client_ip` is called only in `consent_handler` (cookie banner, keyed by anonymous `consent_token`, **not** linked to any application), `payment_handler`, and Meta dispatch. AD-10's honesty table — the AD's own load-bearing device — is wrong on the row that matters most for its credibility.

- **Builder A** adds an IP column to `application` at submission — a new applicant PII category with no Art-13 notice update decided anywhere in the doc.
- **Builder B** tries to join `cookie_consent_log` via `consent_token` — fails (no link to applications), emits garbage or crashes the signal.
- **Builder C** notices the gap and emits `"unknown"` like `geo_vs_claimed_property` — divergent from the doc the other two followed.

Related: §7.3 captures "invite-opened (first GET)" for `form_session.completion_seconds`, but §4.1's DDL has no column for it — builders split between an `attempts` entry, a new column, and a cookie. AD-10's table needs one more honesty pass and the storage locations named.

### F5 (MEDIUM-HIGH) — Operational envelope silence on the new attack surface

The canonical doc owns this dimension and the addendum inherits it, but the addendum *adds* surface without extending the envelope:

1. **Webhook authentication is never stated.** §7.2 adds `webhooks/resend-events` and `webhooks/twilio-sms`; the canonical webhook table specifies signature verification for Stripe and Resend inbound. The addendum says nothing. An unauthenticated Twilio webhook is a state-mutation path guarded by nothing: anyone can POST a STOP and object any row, or POST a delivery-failure and force `awaiting_correction`. Builder A verifies Twilio's `X-Twilio-Signature`; Builder B puts the route behind `is_public_path` and ships. Both "followed the addendum".
2. **No rate-limit/abuse posture for the new anonymous POSTs.** `/reference/:token` and the correction route are public, unauthenticated, write referee PII, and flip state. The canonical Cloudflare posture names exactly three rate-limited endpoints; the `/apply` precedent adds honeypot + timing validation. The addendum decides none of this for its new routes. One builder adds rules + honeypot; another ships open.
3. **No liveness rule for the sweep.** A silently dead 15-minute cron means no reminders, no terminals, no warm handoffs — the feature fails invisibly. Canonical posture is Sentry-from-day-one; the addendum extends no observability (dead-man alert, per-tick log, Sentry capture on webhook failures) to any of the new machinery.

### F7 (MEDIUM) — "Field names verbatim" is violated twice, silently

§6.1 declares heist-535's schema binding, "field names verbatim". AD-8 does this properly for `channel` (explicitly records adding `"manual"`). But:

- The outcome enum is silently extended: `unreachable`, `form_completed`, `manual_recorded` are **not** in heist-535's outcome literal (heist-535's own semantics table uses `unreachable` but its enum omits it — an upstream inconsistency the addendum fixes without recording the fix).
- AD-7's fraud flag is `referee_contact_invalid`; heist-535's is `referee_number_wrong` for the same signal.

The v2 consumer (`reference_validator_agent`) is built by a different team reading heist-535 as the contract. Builder-of-v1 (addendum) emits `referee_contact_invalid`; builder-of-v2 (heist-535) matches on `referee_number_wrong` → the claim-integrity signal silently never fires, and §10's "v2 is a read-and-send, not a migration" guarantee is broken. The addendum needs an explicit "amendments to heist-535" register, as it already does for `channel`.

### F8 (LOW-MEDIUM) — Enforceability nits

- **TEXT CHECK vs canonical enum rule.** §4.1 uses TEXT+CHECK for `channel`, `ref_slot`, `owner_label`, `retention_class`; canonical enforcement says "Postgres ENUMs for status fields — never TEXT with string literals". The preamble says canonical wins on disagreement → a builder can legitimately rewrite the DDL as enums. Deviation should have been acknowledged and owned.
- **Warm-handoff duplication.** AD-4 schedules landlord notifications at both T+96h (warm handoff) and T+144h (terminal); §8.3 gives one enum value (`reference_unreachable`) apparently covering both. One builder sends two notifications; another sends one + status change.
- **No audit_log decision.** Canonical requires audit on status changes; objection, substitution, manual-record are landlord-visible, compliance-weighted state changes; the addendum is silent on audit entries for the lifecycle.
- **Substitution trigger.** §5.7's substitution link to the applicant is sent… when, by what? Presumably the landlord's `can_substitute_referee` affordance, but the flow (landlord clicks → applicant emailed a tokenized link) is never stated (see AD-11 row above).
- **Attestation conditionality.** Precedent (`guarantor_attestation`) writes conditionally on presence; §3.1 implies unconditional (required checkbox) — fine, but the pre-v1-application gap (AD-2 row above) is the real hole.

## 4. Deferred / Open Questions — divergence-safety audit

| Item | Safe? | Assessment |
|---|---|---|
| §12 Voice everything → v2 | **Safe** | v2-reserved register (§6.3) forbids placeholder emission; enum values inert. |
| §12 v5 re-score → v2 | **Safe** | AD-12's non-build rule is enforceable. |
| §12 Co-applicant triggering | **Safe** | Schema-ready, trigger deferred; attestation semantics for co-applicant referees will need one line when revisited (the attestation is the primary applicant's). |
| §12 Localization, geo-IP, fingerprint, coached-score, voice-print, scheduling links | **Safe** | AD-10 already emits honest null/"unknown" for each. |
| Q1 ComReg Sender-ID | **Safe** | External launch dependency, correctly flagged hard-blocking, not a design fork. |
| Q2 Twilio provisioning | **Safe** | Same. |
| Q3 Inbound SMS webhook | **Safe as scoped** | In v1, flagged for review — but see F5(1): its *authentication* is not an open question, it's an unasked one. |
| **Q4 Objection-evidence survival at erasure** | **UNSAFE (medium-high)** | The direction is decided ("snapshot before delete") but the vehicle is not ("`reference_objection_log`-style" **or** "the FK is revisited"). The erasure-flow builder and the reference builder can each build a different store (new table vs `audit_log` variant vs SET NULL) — two owners for one evidence entity, and it's the entity AD-6's Art 21 compliance claim rests on. §9.3 compounds it by listing `objection_evidence` as a v1 `retention_class` with **no entity that carries it**. This is a build-gating schema decision parked in Open Questions. |
| Q5 Free-text display posture | **Safe** | Counsel-gated **with a named fallback** (store, withhold display) — the correct pattern. |
| Q6 Counsel pack | **Safe** | Launch-gating, not build-gating, as stated. |
| *(unlisted)* Per-row `purge_after` sweep | **Soft gap** | §9.3 stamps `purge_after` at terminal ("follows the application's retention schedule") — but `retention_due_at` may be NULL pre-close, so the stamped value is undefined; and no v1 consumer of `idx_reference_call_purge` exists (implied-future but absent from §12). Low risk; should be one line either in §9.3 or §12. |

## 5. Silent structural dimensions at this altitude

- **Security envelope for new surface** — F5. The most consequential silence.
- **Concurrency/ownership rules** — F3. A feature doc introducing a cron + webhooks + public POSTs against one row must state the guard rule; the repo precedent existed to cite.
- **Observability for new machinery** — F5(3) (sweep liveness, webhook failure capture); also no metrics decision for the funnel AD-8 says it protects (PostHog events on referee funnel? undecided — minor).
- **Tests** — §13's build shape lists no test files; canonical structure convention is one test module per server module. Minor, but a checker will ask.
- **Shared-package codecs** — the `reference_calls[]` payload crosses the compilation boundary (canonical: shared types + codecs); unmentioned. Builders will follow canonical habit, but one line would have closed it.
- **Audit trail** — F8.

## 6. What the artifact gets right (keep)

1. §1 verified-current-state table with an honest correction of the briefing (RLS posture) — the addendum audits its own inputs rather than inheriting their errors.
2. AD structure (Rule / Binds / Prevents / Rationale / Rejected) is consistently filled with *real* rejected alternatives, not strawmen.
3. The enum-superset strategy (AD-1) with an explicit v2-reserved register (§6.3) is the right way to buy v2 cheapness without v1 placeholder pollution.
4. AD-8 (WoZ in v1) with the metric-corruption rationale — the funnel-integrity argument is exactly the kind of second-order effect spines exist to catch.
5. AD-10's honesty-table *format* (collectible-today column) — the right device, needing one more honest pass (F4).
6. §9 legal flags each get a designed-in mechanism rather than a disclaimer, and counsel items are correctly separated into launch-gating vs build-gating.
7. Scope discipline: the UX workstream is given a data contract + server-computed hooks instead of a screen spec (AD-11); the v5 contract is design-only with a conformance guarantee (AD-12).

---

## Verdict & required amendments

**Verdict:** A strong, mostly enforceable spine that correctly scopes itself against the canonical doc — but it does not pass the gate as-is: three high-severity holes (F1 status↔outcome mapping incl. the contradictory enum comment and homeless `failed`/manual outcomes; F2 immutable-snapshot vs correction-loop contradiction; F3 missing mutation-ownership/guard rule across seven writers), one factually wrong "collectible today" claim (F4), one silent security envelope on the new public/webhook surface (F5), and one divergence-unsafe open question on Art 21 evidence (Q4).

**Minimum amendments to pass (all small, none re-scope v1):**
1. One table: v1 terminal/lifecycle transitions → (`status`, `outcome`, result presence, writer, notification) — resolving F1, the "first five" comment, the `failed`-outcome gap, and AD-8's manual-entry semantics.
2. One paragraph: concurrency rule — guarded updates naming expected pre-state, terminal states sticky, atomic `attempts` append, T0 owned by the sweep (F3).
3. One decision: corrected-contact storage (overwrite with audit, or corrected columns) + fix the immutability claim (F2).
4. One line each: webhook signature verification, rate-limit posture for `/reference/*`, sweep liveness (F5).
5. Correct AD-10's IP row to "not collectible today" + name the capture decision; name the invite-opened storage (F4).
6. Promote Q4's vehicle to a decision (or move it to §13 as a build item with a named table); reconcile §9.3's `objection_evidence` class (§4 audit).
7. An explicit "amendments to heist-535" register covering the outcome-enum extension and the flag-slug rename (F7).
