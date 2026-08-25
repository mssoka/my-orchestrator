# RightTenantry Security Audit — Data Layer Lens

**Scope:** SQL injection, Erlang FFIs, PII in logs/analytics, DSAR/erasure scoping, audit_log discipline, consent integrity, retention.
**Repo:** `righttenantry-security-audit` @ `17d5f32` (READ-ONLY). Method: exhaustive path enumeration, every claim verified against disk. No edits made.

## Summary

The data layer is in strong shape. SQL injection is architecturally impossible at the query layer — every one of the 227 `.sql` files compiles through Squirrel into `pog.query` + `pog.parameter` calls, the sole raw `pog.query` is a static `SET LOCAL` string, and the one Erlang FFI that touches the DB (`db@db_ffi.erl`) is a constant-keyed `persistent_term` cache, not a query builder. The six hand-written Erlang FFIs are clean: no `binary_to_atom`, no shell wrapping (typst runs via `spawn_executable` argv, the only `os:cmd` carries an integer pid), and the PDF temp path is a server-minted UUID. Logging and token redaction are unusually disciplined — a central `redact_token_route` covers access logs, Sentry paths, and CSP-report URLs; Sentry `CrashEvent` headers pass a six-header allowlist; inbound-email and typst paths mask/truncate.

The findings are all **defence-in-depth / compliance-hygiene** gaps rather than exploitable breaks. The two most material are: (1) `request_helpers.client_ip` trusts the *first* `X-Forwarded-For` value, which is client-spoofable — Cloudflare appends the real IP at the *end* and provides `CF-Connecting-IP` — so the consent/application "applicant IP" and the Meta CAPI `client_ip_address` egress are both forgeable; and (2) four ADK response parse-failure paths in `ai_client.gleam` log the raw upstream body, bypassing the `redact_adk_body` scrubber that covers the sibling error path. The remaining items are documented known-gaps (typst markup metacharacters), classification choices (IP as non-PII in `audit_log`; referee/co-applicant PII in the DSAR export), and dev-only or accepted-race conditions.

## Findings table

| ID | Severity | Title | File:line | Confidence |
|----|----------|-------|-----------|------------|
| F1 | Medium | `client_ip` trusts first X-Forwarded-For value (spoofable) — affects consent IP + Meta CAPI IP egress | `server/src/request_helpers.gleam:45-53` | High |
| F2 | Medium | ADK response parse-failure paths log raw body, bypassing `redact_adk_body` | `server/src/ai/ai_client.gleam:1044,1170,1189,1340` | High |
| F3 | Medium | Supabase signup/OAuth error bodies logged raw (may echo email) | `server/src/auth/supabase.gleam:308,632,651` | Medium |
| F4 | Medium | Twilio Lookup logs raw phone number to Cloud Logging + Sentry | `server/src/reference_checks/lookup.gleam:89` | High |
| F5 | Low | Digest handler logs full landlord email (unmasked) | `server/src/notification/digest_handler.gleam:216,226` | High |
| F6 | Low | Single-use erasure URL (token) logged in dev branch, bypassing central redaction | `server/src/application/application_handler.gleam:2177` | High (conditional) |
| F7 | Low | DSAR export includes referee/co-applicant/guarantor third-party PII | `server/src/dsar/dsar_handler.gleam:240-330` | High (existence) / Medium (severity) |
| F8 | Low | IP address classified as non-PII in audit_log (survives pseudonymisation) | `server/src/retention/audit_log_schema.gleam:123-124` + `pseudonymise_audit_log.sql` | High (existence) / Medium (severity) |
| F9 | Low | Typst markup metacharacters unescaped (self-documented gap) | `server/src/ai/typst_sanitize.gleam:28-38` | High (documented) |
| F10 | Low | Account-deletion pending-payment gate has a documented TOCTOU window | `server/src/account/account_handler.gleam:200-238` | High (documented) |

---

## F1 — `client_ip` trusts the first X-Forwarded-For value (spoofable)

**Trigger:** A client (or script) sets `X-Forwarded-For: <arbitrary>` on any request. `client_ip` takes the *first* comma-separated value, which is the client-supplied one.

**Evidence** (`server/src/request_helpers.gleam`):

```gleam
/// Best-effort client IP from the `x-forwarded-for` header.
/// Cloudflare appends the originating IP first; subsequent entries are
/// trusted intermediaries. We take only the first value, trim it, and slice
pub fn client_ip(req: Request) -> String {
  case request.get_header(req, "x-forwarded-for") {
    Ok(value) ->
      case string.split_once(value, ",") {
        Ok(#(first, _)) -> string.trim(first) |> slice_codepoint_bounded(64)
```

Cloudflare's documented behaviour contradicts the comment: when an `X-Forwarded-For` header is already present, Cloudflare **appends** the real client IP to it, and explicitly recommends reading `CF-Connecting-IP` / `True-Client-IP` instead ("Cloudflare recommends that your logs or applications look at `CF-Connecting-IP` … `CF-Connecting-IP` … have a consistent format containing only one IP address"). So `first` = spoofable; the real IP is the last entry.

**Consequence:** Three consumers inherit the spoofed value:
1. `consent/consent_handler.gleam` → `cookie_consent_log.ip_text` (consent-evidence row).
2. `application/application_handler.gleam` → `application.submitted_ip_text` (fraud/timing correlation).
3. `meta/dispatch.gleam` → `meta_client.UserData.ip` → `client_ip_address` sent to Meta CAPI (PII egress of a forgeable value).

The hard anti-abuse controls (Cloudflare edge rate-limit, honeypot, server-side timing) do **not** depend on this value, so this is not an authz bypass — it degrades the evidentiary value of the recorded IP and the accuracy of the Meta matching signal.

**Remediation:** Read `CF-Connecting-IP` (or `True-Client-IP`) first, fall back to `X-Forwarded-For` only when absent, and when falling back take the *last* entry. Update the comment.

---

## F2 — ADK response parse-failure paths log raw body, bypassing `redact_adk_body`

**Trigger:** The ADK/agent service returns a body that fails to parse (malformed JSON, missing fields, or an agent-side anonymisation regression that reintroduces PII into `detailed_insight`/`excerpt`/`rationale`).

**Evidence** (`server/src/ai/ai_client.gleam`):

```gleam
// 1044
wisp.log_error("Session response parse failure, body: " <> body)
// 1170
wisp.log_error("Run response parse failure, body: " <> body)
// 1189
wisp.log_error("No text content in run response, body: " <> body)
// 1340
wisp.log_error("Failed to parse ADK response, body: " <> body)
```

Only the error-envelope path applies the scrubber:

```gleam
// 1603
wisp.log_error("Unparseable ADK error envelope, body: " <> redact_adk_body(body))
```

The `pii_json_keys` constant (line 725) exists precisely because the v4 free-text fields — `detailed_insight`, `rationale`, `excerpt`, `action`, `reason` — "would leak straight into logs" if the agent-side anonymisation regresses. The four raw-body sites above are the run/analysis response bodies, which are exactly where those fields live, and they skip the scrubber.

**Consequence:** Applicant PII (names, addresses, employment, personal-statement fragments embedded in LLM prose) lands in Cloud Logging, which is retained past the application-deletion window.

**Remediation:** Route all four sites through `redact_adk_body` (it already truncates to 500 chars + redacts the PII key set). Keep `parse_error_response` as-is.

---

## F3 — Supabase signup/OAuth error bodies logged raw

**Trigger:** Supabase registration returns a 4xx/5xx, or OAuth token exchange returns a non-200. The response body is concatenated into the log line.

**Evidence** (`server/src/auth/supabase.gleam`):

```gleam
// 308 — OAuth token exchange
wisp.log_error("OAuth token exchange failed (" <> int.to_string(status) <> "): " <> resp.body)
// 632 — registration 400/409/422
wisp.log_info("Registration failed (" <> int.to_string(status) <> "): " <> resp.body)
// 651 — registration other status
wisp.log_error("Registration failed with status " <> int.to_string(status) <> ": " <> resp.body)
```

Supabase auth error bodies can echo the submitted identifier (e.g. `email` in a signup error). Contrast with the two paths that *do* withhold the body — `recover_password` (logs status only, "keeps enumeration-clean") and email verification (explicit comment: "Do NOT log resp.body — …error bodies can echo the token_hash or email"). Those two comments confirm the team already knows the body is unsafe on this client; the signup/OAuth sites just weren't covered.

**Consequence:** Email addresses (and possibly token material on OAuth failures) in Cloud Logging.

**Remediation:** Mirror the verification path — log status only, or truncate + redact email/token keys before logging the body.

---

## F4 — Twilio Lookup logs raw phone number to Cloud Logging + Sentry

**Trigger:** Twilio Lookup (reference-check phone validation) returns a non-success status; the raw phone is interpolated into both the Sentry message and the `wisp.log_warning`.

**Evidence** (`server/src/reference_checks/lookup.gleam:83-92`):

```gleam
capture_failure(
  sentry,
  message: "Twilio Lookup HTTP " <> int.to_string(status) <> " for phone " <> phone,
  tags: [#("http_status", int.to_string(status))],
)
wisp.log_warning(
  "Twilio Lookup failed: HTTP " <> int.to_string(status) <> " for phone " <> phone,
)
```

The phone is a reference/character-referee number (a natural person's PII). It is unmasked in both sinks.

**Consequence:** Third-party phone numbers in Cloud Logging and forwarded to Sentry (a third-party processor).

**Remediation:** Mask the phone (reuse the `mask_email_for_log` pattern, e.g. keep last 4 digits) before both the Sentry `message` and the log line.

---

## F5 — Digest handler logs full landlord email (unmasked)

**Trigger:** Weekly digest send (success or failure) logs the landlord's full email.

**Evidence** (`server/src/notification/digest_handler.gleam`):

```gleam
// 216
wisp.log_info("Digest sent to " <> landlord.email <> " — " <> int.to_string(list.length(rows)) <> " vacancies")
// 226
wisp.log_warning("Digest email failed for " <> landlord.email <> ": " <> err)
```

The inbound-email module masks enquirer addresses (`mask_email_for_log`, `j***@example.com`) specifically because "logs outlive that purge". The digest path has no equivalent masking.

**Consequence:** Landlord email addresses persist in Cloud Logging beyond the point the landlord may have deleted their account.

**Remediation:** Apply the same masking helper (or a shared `mask_email_for_log`) to both digest lines.

---

## F6 — Single-use erasure URL (token) logged in dev branch

**Trigger:** `RESEND_API_KEY` unset (dev/unconfigured env) while sending the confirmation email. The full `erasure_url` — including the 288-bit single-use erasure token — is written to the log.

**Evidence** (`server/src/application/application_handler.gleam:2172-2180`):

```gleam
// Dev / unconfigured environment. The erasure_token is persisted but
// there's no delivery path. Log prominently so an operator ... can reach the applicant out-of-band.
wisp.log_warning(
  "confirmation email skipped (no RESEND_API_KEY) — orphaned erasure_url for app "
  <> row.id <> ": " <> erasure_url,
)
```

This is an application-level log line that bypasses the central `redact_token_route` (which only covers access-log paths, Sentry paths, and CSP URLs — not arbitrary log arguments). Production always sets `RESEND_API_KEY`, so the branch is dev-only, but the discipline is violated: a capability token is written verbatim to a log stream.

**Consequence:** In a dev/staging environment, the single-use Art. 17 deletion token is visible to anyone with log access; the `/erase` token is the sole auth for that endpoint.

**Remediation:** Log the application id and the *redacted* URL (`/erase/<redacted>`), never the full token.

---

## F7 — DSAR export includes referee/co-applicant/guarantor third-party PII

**Trigger:** A DSAR (Art. 15/20) export for a primary applicant.

**Evidence** (`server/src/dsar/dsar_handler.gleam` — `serialize_application` / `serialize_co_applicant`): the export includes `landlord_ref_name/phone/email`, `employer_ref_name/phone/email`, `character_ref_name/phone/email`, `guarantor_name/relationship/phone/email/employer`, and the full `co_applicants` array (names, income, employment, guarantor details).

All rows are correctly scoped to the single `application_id` — there is **no cross-application or cross-landlord leakage** (verified: every query is keyed on `app_uuid`, no joins reach other landlords' rows; the only vacancy-derived field is `property_name`/`vacancy_id`). The third-party data is what the *applicant themselves submitted* into their own application, which is the standard defence under Art. 15 (the data "concerning" the applicant includes the referee references they provided). This is flagged as an Art. 15(4) "rights and freedoms of others" consideration rather than a leak.

**Consequence:** Low. Referee/co-applicant/guarantor personal data is disclosed to the primary applicant on request. Defensible, but should be a conscious, documented decision (and may warrant redaction of referee contact fields where the referee did not consent).

**Remediation:** Review whether referee/guarantor contact fields should be redacted from the export under Art. 15(4); if retained, record the rationale in the DSAR SQL header (the module already documents the AI-analysis inclusion policy there).

---

## F8 — IP address classified as non-PII in `audit_log` (survives pseudonymisation)

**Trigger:** Retention pseudonymisation of `audit_log.details` (on application deletion / landlord deletion PTA archive).

**Evidence** (`server/src/retention/audit_log_schema.gleam`): `ConsentIpText` and `ConsentUserAgent` are in the `NonPiiKey` enum (lines ~123-124), so they are **not** in the deny-list in `pseudonymise_audit_log.sql`:

```sql
SET details = (COALESCE(details, '{}'::jsonb) - ARRAY[
  'applicant_email','applicant_phone','applicant_name','first_name','last_name',
  'email','phone','personal_statement','employer_name','employer_contact',
  'address','dob','guarantor_name','guarantor_email','guarantor_phone'
]::text[]) || jsonb_build_object('pseudonymised_at', ...)
```

IP addresses are personal data under EU law (CJEU Breyer C-582/14). The PTA-archive path (`landlord_deletion.gleam`) deliberately retains `ip_text` as chargeback-defence evidence for the Art. 16(m) waiver — a defensible purpose — but the classification means it is *never* stripped from the 6-year audit store.

**Consequence:** Low. Landlord/consent IP addresses persist in `audit_log` for the 6-year AI-Act window with no pseudonymisation. Arguably justified for the PTA evidence case, but the blanket non-PII classification is broader than that one purpose.

**Remediation:** Split the classification — keep a purpose-scoped "consent_ip_text" on the PTA evidence archive, but ensure the generic audit-log pseudonymisation path either strips IPs or the retention is justified in writing.

---

## F9 — Typst markup metacharacters unescaped (self-documented gap)

**Trigger:** A personal statement or LLM-emitted `detailed_insight` containing a leading `=`, `*`, `_`, `#`, or `[`.

**Evidence** (`server/src/ai/typst_sanitize.gleam`), the module's own header:

```
KNOWN GAP: Typst metacharacters (`*`, `=`, `#`, `[`, `_`) are NOT escaped here.
`audit_report.typ` renders v4 prose via `text(...)[#var]` content blocks, which
interpret these characters as markup. A stray `=Heading` in a personal statement
... would render as an actual heading, not as the literal text.
```

**Consequence:** Low. Formatting/markup injection into the generated PDF (e.g. a line beginning with `=` renders as a heading). The module notes it "can't break out of the rendering sandbox" and it's tracked as a warning from a prior review. This is a rendering-integrity issue, not an information-disclosure one.

**Remediation:** Render the prose fields via `raw(var)` in `audit_report.typ`, or escape the metacharacter set in a Typst-specific sanitizer.

---

## F10 — Account-deletion pending-payment gate has a documented TOCTOU window

**Trigger:** A landlord starts a Stripe Checkout in tab A and completes account deletion in tab B within the ~50ms transaction window.

**Evidence** (`server/src/account/account_handler.gleam:200-238`): the gate `has_pending_payment` runs **before** the deletion transaction, and fails closed on read error (500). But the check is not inside the tx:

```
Residual TOCTOU race ACCEPTED at current volumes: a landlord who starts a checkout
in tab A AND clicks delete in tab B within the ~50ms tx window could still produce
an orphan charge — the pending row inserts after this check returns Ok(False) ...
Manual refund path covers the orphan charge if it ever fires.
```

**Consequence:** Low. A vanishingly rare orphan Stripe charge requiring a manual refund. Explicitly accepted and documented with a mitigation path. Not a bypass of the *intent* of the gate (the gate works for the realistic abandoned-checkout case).

**Remediation:** Deferred (documented). Hardening would move the check inside the tx or make the webhook fail-closed on a missing vacancy.

---

## Logs that carry PII — inventory

Every call site that interpolates user-derived data into `wisp.log_*` / Sentry `message`, plus the field leaked.

| # | File:line | Sink | Field(s) | Notes |
|---|-----------|------|----------|-------|
| 1 | `ai/ai_client.gleam:1044` | log | ADK session-create body | raw, unredacted |
| 2 | `ai/ai_client.gleam:1170` | log | ADK run response body | raw, unredacted — **F2** |
| 3 | `ai/ai_client.gleam:1189` | log | ADK run response body | raw, unredacted — **F2** |
| 4 | `ai/ai_client.gleam:1340` | log | ADK response body | raw, unredacted — **F2** |
| 5 | `auth/supabase.gleam:308` | log | OAuth token-exchange body | raw — **F3** |
| 6 | `auth/supabase.gleam:632` | log | signup body (400/409/422) | raw — **F3** |
| 7 | `auth/supabase.gleam:651` | log | signup body (other) | raw — **F3** |
| 8 | `reference_checks/lookup.gleam:83-89` | log + Sentry | reference phone | raw — **F4** |
| 9 | `notification/digest_handler.gleam:216` | log | landlord email | full — **F5** |
| 10 | `notification/digest_handler.gleam:226` | log | landlord email | full — **F5** |
| 11 | `application/application_handler.gleam:2177` | log | erasure URL (single-use token) | dev-only — **F6** |
| 12 | `notification/sms_client.gleam:163` | log + Sentry | Twilio error body (≤512 chars) | echoes To/Body per module comment |
| 13 | `payment/stripe_client.gleam` (multiple) | log | Stripe error body (≤512 chars) | `truncate_for_log`, bounding only |
| 14 | `notification/email_client.gleam:159,204` | log | Resend error body | raw `resp.body` |
| 15 | `storage/storage_client.gleam:226,234` | log | Supabase Storage error body | raw `resp.body` (paths, not emails) |

Truncation sites (12, 13) are **bounding, not redaction** — the first 512 chars of an error body can still contain a phone/email echoed by the upstream. They are listed here as lower-confidence PII-adjacent lines.

## Verified-clean list (no action required)

- **SQL injection:** all 227 `.sql` files Squirrel-parameterized; the sole raw `pog.query("SET LOCAL statement_timeout = '8s'")` (`payment/payment_handler.gleam:473`) is a static literal; no Gleam-side SQL string building; no `fracture`; all `LIMIT`/`ORDER BY` are literals or `$n`; `($3 || ' seconds')::interval` (`ai/sql/update_analysis_failed.sql:28`) binds `$3` as a typed parameter before Postgres concatenation.
- **Erlang FFIs (all six):** no `binary_to_atom`/`list_to_atom`; no SQL; `ai@audit_report_ffi.erl` uses `spawn_executable` with a flat argv (no shell) and `os:cmd` only with an integer pid; PDF output path is a server UUID (`ai/audit_report.gleam`), so no traversal; JSON payload size-capped at 120 KB (below `MAX_ARG_STRLEN`).
- **Sentry `CrashEvent` headers:** filtered through a six-header `safe_headers` allowlist (`sentry_client.gleam`) — auth/cookie/authorization headers never reach Sentry.
- **Capability-token path redaction:** `redact_token_route` (`middleware.gleam:333`) covers `/dsar`, `/erase`, `/apply/…/resume`, `/apply/…/draft-erasure`, `/reference` in access logs, Sentry paths (`sentry_safe_path`), and CSP-report URLs (`redact_token_url`, which also drops query+fragment).
- **typst diagnostics:** truncated to 240 chars (`truncate_for_log`, `ai_report_handler.gleam:396`) before logging; `sanitize_filename` is a strict alphanumeric+`-_` allowlist (no CRLF/header injection in the PDF `content-disposition`).
- **inbound email:** enquirer addresses masked via `mask_email_for_log` (`inbound_handler.gleam`); logged values are `event_type` / `email_id` / `to_address` (system reply-to), not enquirer PII.
- **PostHog:** no client-IP forwarding (only `content-type` header set); `distinct_id` is a landlord UUID or `applicant-<code>-<entropy>`; the only PII property is the landlord's own email as `$set` (first-party identify).
- **Meta CAPI consent gating:** `consent_check.marketing_granted` fails closed (missing/malformed/stale cookie → `False`); Lead + CompleteRegistration are gated (`vacancy_handler:1981`, `auth_handler:1519`); Purchase is the documented legitimate-interest carve-out and carries no IP/UA (`webhook_handler:1056,1146`). Email and `external_id` are SHA-256 hashed.
- **DSAR/erasure token model:** 288-bit token = sole auth; GET `/dsar/:token` is a static no-oracle page; POST writes the audit row before returning the body (fail-closed); export runs in a `READ ONLY REPEATABLE READ` transaction; erasure is single-use by row deletion and renders success on re-run (no token-validity oracle).
- **audit_log discipline:** typed `AuditEvent` registry + typed `PiiKey`/`NonPiiKey` registry; `pii()`/`non_pii()` are the only way to build `details`; the pseudonymise deny-list is kept in lockstep with the PII registry by a test (`sql_deny_list_matches_pii_registry_test`). All three defended invariants verified present: `AiDecisionRecorded` (`ai_client:1790`), `StatusChanged`/`StatusAutoChanged` (`vacancy_handler:122`, `application_detail_handler:690`), `PaymentCompleted`/`PaymentFailed` (`webhook_handler:930,978`).
- **Consent capture:** `gdpr_consent` is a required submit field (`application_handler:506-511`); consent records + application insert in one tx; guarantor-attestation consent captured; `landlord_id` for cookie consent derived from the session cookie (never the body); same-origin guard (`is_same_origin_request`) replaces CSRF on the anonymous endpoint.
- **Retention completeness:** `deletion.delete_application` is transactional + idempotent; `consent_record` survives via `SET NULL` (6-year promise); `storage_purge` enqueues to a retry queue on failure (no silent orphan); landlord deletion is atomic with PTA evidence archived first and GoTrue/Stripe/Storage cascades strictly post-commit.

## Draft-save-pre-consent note (Scope 7, informational)

`application/draft_handler.gleam` stores form values (applicant PII) without `gdpr_consent` — the field is explicitly excluded from the draft filter (`key != "gdpr_consent"`, line 110) and the module header documents "consent is captured at submit". This is defensible under Art. 6(1)(b) (steps taken at the data subject's request prior to entering a contract — the applicant chose to save a draft of their own data) and there is a self-service `draft-erasure` token endpoint. Flagged only so the lawful-basis rationale is a conscious, documented decision rather than an omission; no change required.
