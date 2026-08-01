# Reality-check review — architecture-reference-checking-v1-2026-07-29.md

**Artifact reviewed:** `_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md` (in the `refcheck-v1-architecture` worktree)
**Reviewed against:** the same worktree's codebase (read-only), plus `~/code/RightTenantryAgents` for the one cross-repo row the artifact claims to have "verified there".
**Date of review:** 2026-07-29
**Reviewer:** reality-check lens (adversarial verification of every repo-grounded claim)

---

## Verdict

The artifact's "Verified current state" table is overwhelmingly accurate — migration filenames, line numbers, enum names, file paths, and module conventions check out in ~20 of 24 repo-grounded claims — but it contains **two substantive errors** (the internal-cron house pattern is misdescribed, and AD-10 marks two `form_session` fraud signals as "collectible today" when the applicant-side comparator data is never captured), plus three minor citation/convention inaccuracies. Internal doc links all resolve.

---

## Findings (severity-ordered)

### F1 — MEDIUM: The "internal cron" house pattern is misdescribed; the sweep's cited precedent doesn't exist as described

**Claim (§1 table):** "Internal cron: Cloud Scheduler → `POST /api/v1/internal/*` with shared-secret header" — cited as `digest`, `lifecycle/verification-reminders`. Repeated as design basis in AD-4 ("the `verification-reminders` precedent"), §5.4, and §7.2.

**Reality:** Cloud Scheduler never calls the app's HTTP routes. It invokes **Cloud Run Jobs** directly (`:run` endpoint, OIDC service account), which execute the job's `main/0` in-process:

- `deployment/terraform/scheduler.tf:106` — retention scheduler uri = `.../jobs/${google_cloud_run_v2_job.retention[0].name}:run`
- `deployment/terraform/scheduler.tf:188` — digest scheduler → Cloud Run Job
- `deployment/terraform/scheduler.tf:263` — ops-digest scheduler → Cloud Run Job
- `deployment/terraform/scheduler.tf:344` — verification-reminders scheduler → Cloud Run Job
- `docker-entrypoint.sh:144-152` — `digest` / `ops-digest` / `verification-reminders` job entry points invoked via `erl -eval ... notification@digest_job:main()`.

The `POST /api/v1/internal/*` routes exist (router.gleam:753 digest, :756 verification-reminders) and are protected by the `X-Internal-Secret` header (`response_helpers.require_internal_secret`, digest_handler.gleam:33), but the code itself documents them as the **manual** trigger, not the scheduled path:

- `server/src/notification/digest_handler.gleam:4-6`: "`handle_send_digest/2`: HTTP route (POST /api/v1/internal/digest) for **manual triggering**."
- `server/src/notification/digest_job.gleam:9-10`: "the pure worker (also reachable via POST /api/v1/internal/digest **for manual fires**)."
- `server/src/lifecycle/verification_reminder_job.gleam:1-2,14-15`: "runs hourly as a **Cloud Run Job triggered by Cloud Scheduler** ... (also reachable via the internal HTTP trigger)."

**Impact:** §5.4/AD-4 design the reference-check sweep as an HTTP route "following the precedent", when the precedent for *scheduled* work is a new Cloud Run Job + scheduler entry (terraform + docker-entrypoint), with the internal HTTP route as the optional manual fire. A build that follows the artifact literally would wire Cloud Scheduler → app HTTP endpoint — a pattern this repo does not use anywhere in production — and would skip the terraform/job work the house pattern actually requires. The shared-secret route is still worth having (for manual fires), but the AD's framing ("the existing house pattern") is wrong about which half of the pattern is the scheduled one.

### F2 — MEDIUM: AD-10 fraud table — two `form_session` signals marked "Collectible today? Yes" require applicant-side data that is never captured

**Claim (AD-10 table):** `form_session.ip_matches_applicant` — "Referee form IP vs the application-submission IP (evidentiary capture, cookie-consent precedent)" → **"Yes"**; and `form_session.device_fingerprint_match` — "User-Agent match (bounded 512)" → **"Yes, honestly weak"**.

**Reality:** No applicant IP or User-Agent is captured at application submission. `request_helpers.client_ip` / `client_user_agent` have exactly three call sites, all **landlord-side**:

- `server/src/payment/payment_handler.gleam:157` — payment-terms acceptance (landlord)
- `server/src/consent/consent_handler.gleam:196` — cookie consent (landlord)
- `server/src/meta/dispatch.gleam:40` — Meta Conversions API

`application_handler.gleam` / `application/sql.gleam` contain no `client_ip`/`ip_text`/`user_agent` usage. No IP/UA column exists on `application`, `audit_log` (initial_schema.sql:161-169 has no IP column), or anywhere applicant-facing — the only IP storage in the schema is `session.ip_address` (landlord sessions, `00000000000001_initial_schema.sql:35`), `cookie_consent_log.ip_text` (`20260523224800:37`), and `payment_terms_acceptance.ip_text`.

**Impact:** the referee-side half of both signals is collectible (the mechanism exists), but the *match* requires a comparator that does not exist. Collecting applicant IP/UA at submission is new scope — and notably a new GDPR data-collection surface of exactly the kind AD-10's own rationale refuses for geo-IP ("new vendor, new DPIA surface"). Either AD-10 must add "capture applicant IP/UA at submission" to v1 scope (with the legal surface that implies), or both signals belong in the "No → emits unknown/null" column alongside `geo_vs_claimed_property`. As written, the "collectible today: Yes" rows are wrong.

### F3 — LOW: `UNIQUE(application_id, record_type)` provenance miscited

**Claim (§1 table):** `acknowledgement_record(...)` + `UNIQUE(application_id, record_type)` attributed to "initial schema + `20260421185540` + `20260422000001`".

**Reality:** the constraint exists (and survives the rename), but none of the three cited migrations creates it. It was added by **`20260402233721_add_personal_statement_and_consent_unique.sql`** as `unique_consent_per_application UNIQUE (application_id, consent_type)`; `20260422000001` renamed the column underneath it (Postgres keeps the constraint). The cited trio does correctly account for the rest of the shape (`granted_at`/`revoked_at` from initial_schema.sql:142-148; `policy_version NOT NULL` + FK CASCADE→SET NULL from `20260421185540:20-43`; `record_type` name from `20260422000001:28`). Also note the initial schema's original FK was `ON DELETE CASCADE` (initial_schema.sql:144) — the SET-NULL survival the artifact relies on is entirely a `20260421185540` retrofit, which the artifact does state correctly elsewhere; only the UNIQUE's source file is missing.

### F4 — LOW: §4.1 "follows the dsar/erase token convention (high-entropy, unique partial index, expiry)" — expiry is no longer part of that convention

**Claim (§4.1 column notes):** "`form_token` follows the dsar/erase token convention (high-entropy, unique partial index, expiry)."

**Reality:** two of three attributes are right — 48-char URL-safe tokens (~288 bits, application_handler.gleam:1755-1759) and a partial unique index (`20260421185540:12-13`, `idx_application_erasure_token ... WHERE erasure_token IS NOT NULL`). But the expiry leg was **deliberately removed**: `20260423120000_drop_erasure_token_expires_at.sql` dropped `erasure_token_expires_at` with an explicit rationale ("a separate clock added a dead-letter window ... Row lifetime is now the single source of truth"). The 30-day expiry in AD-3 is a *new, deliberate* design decision for referee forms (and a reasonable one, since `reference_call` rows are not the applicant's own row lifetime) — but it is not "the dsar/erase convention"; if anything the repo's considered position on token expiry clocks is sceptical. Wording should be "high-entropy, unique partial index" + "expiry: new for this table (AD-3)".

### F5 — LOW (nits): small citation imprecisions

- §1 table cites `middleware.gleam:275,319` for the token-route registry. 275 is `is_public_path` (correct); 319 is the final comment line *above* `fn redact_token_route` (the function is at **320**). Immaterial but off-by-one.
- §1 says `insert_acknowledgement_records` "writes `data_processing`, `ai_analysis`, `guarantor_attestation` in one tx". The third write is **conditional** on `any_guarantor_present` (application_handler.gleam:1815-1832); the unconditional writes are the first two. The AD-2 design (a fourth, checkbox-gated write) is unaffected — the phrasing just overstates the current behaviour.
- §1 "Shortlist exists as a landlord action (`application_shortlist_notified`)" — the parenthetical is the *migration filename* shorthand; the actual artefacts are the `shortlist_notified_at` column (`20260527145213:13-14`) and the status-PATCH action + `maybe_send_shortlist_notification` (application_detail_handler.gleam:679,735). Correct in substance, loose in naming.

---

## Verified-accurate claims (spot-checked with file:line evidence)

| Artifact claim | Evidence | Status |
|---|---|---|
| Reference trios `landlord_ref_*`/`employer_ref_*` at initial_schema.sql:75-80 | exact lines 75-80 | ✅ |
| `character_ref_*` trio + `application_co_applicant.employer_ref_*` from `20260420000001` | migration lines 18-26 (both ALTERs) | ✅ |
| Enum type still named `consent_type`; only the column renamed | initial_schema.sql:12 (`CREATE TYPE consent_type`); `20260422000001:28` renames column only | ✅ |
| `ALTER TYPE consent_type ADD VALUE IF NOT EXISTS` precedent | `20260420000003:8` (`guarantor_attestation`) | ✅ |
| `insert_acknowledgement_records` at application_handler.gleam:1779, called in the submission tx | fn at :1779; call at :1502 inside `pog.transaction` (:1487) | ✅ |
| Resend client with `send_email_with_headers` | notification/email_client.gleam:45 (pub fn), api.resend.com at :71 | ✅ |
| No SMS/Twilio infra anywhere | grep of server/src, supabase/migrations, client/src, config.gleam — only a copy-paste UI hint string in client.gleam:3633 | ✅ |
| `/dsar/:token` + `/erase/:token` registered in three places (redact_token_route, is_public_path, router) | middleware.gleam:282-283, :322-323; router.gleam:833-843 | ✅ |
| redact_token_route covers Sentry + access log + CSP reports | middleware.gleam:330 (sentry_safe_path), :341 (access_log_line), :353-359 (redact_token_url for CSP) | ✅ |
| ~288-bit path tokens | application_handler.gleam:1755-1759 (48 URL-safe chars) | ✅ |
| Public SSR `/apply/:code` GET+POST, no session | router.gleam:776 (GET), :783 (POST); `["apply", _]` in is_public_path (middleware.gleam:278) | ✅ |
| Evidentiary IP/UA capture bounded 64/512, cookie_consent_log precedent | request_helpers.gleam:26-36 (64), :41-46 (512); `20260523224800:37-38` CHECK constraints match | ✅ |
| Retention sweep on `application.retention_due_at`; acknowledgement_record survives via SET NULL | retention/sql.gleam:443-449; `20260421185540:37-43`; landlord_deletion.gleam:56 (SET NULL on cascade) | ✅ |
| RLS: `rls_auto_enable` event trigger, service_role bypass, zero per-table policies | `20260512175704` (function + trigger + header comment); grep `CREATE POLICY` across all migrations → none | ✅ |
| `payload_schema_version = "v4"`, two-step session+run, additive response contract | ai_client.gleam:43, :2, :513; contract_v4.gleam:1-9 ("existing flow keeps working unchanged for these new fields") | ✅ |
| `notification_type` extended by `ALTER TYPE ... ADD VALUE`; dispatch respects `notification_preference` (realtime/daily/off) | `20260423100001:7`, `20260522152938:17`; notification_dispatch.gleam:341,359-361 | ✅ |
| Shortlist landlord action exists (`shortlist_notified_at`, `20260527145213`) | migration adds column; application_detail_handler.gleam:570 (`shortlisted` status), :679/:735 notification | ✅ |
| Trios are form-layer-mandatory, DB-nullable | application_handler.gleam:434-485 `require_non_empty` per slot (character/landlord/employer, conditional); columns nullable in schema | ✅ |
| Existing Resend inbound-email webhook (for the §5.5 "alongside" claim) | router.gleam:763-764; inbound_handler.gleam:30-31 (`resend_webhook_secret`) | ✅ |
| `updated_at` trigger-function pattern exists for ai_analysis/vacancy | `20260409000001` (`update_updated_at_column()` + BEFORE UPDATE trigger); `20260410000001` (vacancy conditional variant) | ✅ |
| Document-download branded-error pages precedent (§5.2) | router.gleam:301-315 → `document_download_session_expired`/`_policy_reaccept` branded pages (application_detail_handler.gleam:290) | ✅ |
| Erasure flow already handles audit evidence (§9.2/Q4) | retention/deletion.gleam:9-16 (pseudonymise audit_log, write retention-delete audit entry); landlord_deletion.gleam:45-58 (archive PTA before delete) | ✅ |
| Migration house style: header comment stating intent | observed across all read migrations | ✅ |
| No pre-existing `reference_call` artefact | grep across migrations + server/src → none | ✅ |
| RightTenantryAgents row: `reference_verification` weight 0.15, `reference_validator_agent`, `check_reference_contact_duplicates` "verified there" | `~/code/RightTenantryAgents`: tenant_scorer/tools/scoring_tools.py:15 (`WEIGHT_REFERENCE_VERIFICATION = 0.15`), tenant_scorer/agents/reference_validator.py, tenant_scorer/tools/reference_tools.py:39 | ✅ (cross-repo, verified on disk) |

## Internal doc links — all resolve

Relative to `_bmad-output/planning-artifacts/`:

- `architecture.md` ✅ · `prd.md` ✅ · `research/heist-535/` ✅ (dir) · `research/heist-535/architecture.md` ✅ · `research/heist-535/legal.md` ✅ · `research/domain-ai-voice-reference-checking-tenant-screening-research-2026-07-21.md` ✅

## Cross-document claims vs the heist-535 inputs (spot-checked)

- `schema_version: "refcall-v1"` — heist-535/architecture.md:80 ✅
- `channel: "voice | form"` (AD-8's claim that heist-535 had exactly those two) — :86 ✅
- "`reference_call_results[]` entry for EVERY terminal outcome" — :160 ✅
- v5 re-score "recommended placement (a)" — :246-248 ✅
- 90-day audio purge (voice-only) — :233 ✅
- never-redial-wrong-number prohibition — :185-186 ✅
- 85–98% written-first completion vs ~25–45% voice-only (AD-4 rationale) — fallback.md:177, :376; domain research :169 ✅

## Asserted but not verifiable from this repo (flagged, not counted as errors)

- GitHub issue #548 and the "2026-07-29 gate amendment" content; RightTenantryAgents#168 — no offline source.
- ComReg Sender-ID "Likely Scam" labelling since 2025-07-03 (Q1) — external regulatory claim; the artifact itself marks it as an open question, which is the right posture.
- "Perkins r1 on #540" (§3.2) — external review-thread reference.

## Recommended corrections before gate sign-off

1. **§1 + AD-4 + §5.4 + §7.2:** reword the cron precedent to "Cloud Scheduler → Cloud Run Job (`main/0` via docker-entrypoint), with an optional `X-Internal-Secret` internal HTTP route for manual fires" — and add the terraform/scheduler + entrypoint work to build-shape item 5 (currently only the HTTP route is listed).
2. **AD-10:** move `form_session.ip_matches_applicant` and `form_session.device_fingerprint_match` to the "No" column (or explicitly scope applicant-side IP/UA capture at submission as new v1 data collection with its GDPR surface called out, alongside the Q5 counsel item).
3. **§1 table:** add `20260402233721` as the source of the `UNIQUE(application_id, record_type)` constraint.
4. **§4.1:** drop "expiry" from the dsar/erase convention list (cite `20260423120000`'s rationale) and present the 30-day expiry as this table's own decision.
5. Nits: middleware.gleam:319→320; note `guarantor_attestation`'s conditional write; name `shortlist_notified_at` rather than the migration shorthand.
