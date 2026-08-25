# Lens — WEBHOOKS + PAYMENTS + OUTBOUND (Stripe, Resend, Twilio, CAPI, SSRF, injection)

## Summary

The webhook surface is, on the whole, well-defended. All three provider signature verifiers (Stripe HMAC-SHA256, Svix HMAC-SHA256, Twilio X-Twilio-Signature) use `crypto.secure_compare` for constant-time comparison with a 5-minute two-sided tolerance window where applicable, and every state-mutating webhook is idempotent (Stripe event-id claim table, Svix `resend_email_id` conflict, Twilio/Resend guarded `WHERE status IN ('queued','contact_initiated')` transitions). Outbound HTTP is uniformly timeout-capped and hosts are config-fixed — there is no SSRF sink. Uploads are validated by magic bytes with layered size caps and UUID-only storage paths, and document downloads are ownership-checked in SQL with 15-minute signed URLs. The findings below are concentrated in three places: (1) the Stripe `checkout.session.completed` handler trusts event metadata for vacancy identity and does not gate on `payment_status`, (2) the two payment-checkout routes read the `Host` header raw (the only un-allowlisted host read in the codebase), and (3) the public inbound-email auto-reply is an unauthenticated, un-rate-limited outbound mail relay whose recipient is chosen from the message body/envelope. Everything else verified clean.

---

## Findings table

| ID | Severity | Title | file:line | Confidence |
|----|----------|-------|-----------|------------|
| W-1 | Medium | `checkout.session.completed` never checks `payment_status` — vacancy unlocks before async funds settle | `payment/webhook_handler.gleam:318-330` | High (config-dependent) |
| W-2 | Medium | Unlock vacancy is keyed from event `metadata.vacancy_id`, never cross-checked against the payment row's `vacancy_id` | `payment/webhook_handler.gleam:513-530`, `payment/sql.gleam:complete_payment` | High |
| W-3 | Low | Payment checkout routes read the `Host` header raw — Stripe `success_url`/`cancel_url` are attacker-controllable (open redirect) | `router.gleam:770-794`, `payment/payment_handler.gleam:456-463` | High |
| W-4 | Medium | Inbound email auto-reply is an unauthenticated, un-rate-limited outbound mail relay (recipient from body/envelope) | `inbound_email/inbound_handler.gleam:158-190`, `email_parser.gleam:reply_recipient` | High |
| W-5 | Low | No refund/dispute webhook handling — chargeback/refund leaves vacancy unlocked and payment `completed` | `payment/webhook_handler.gleam:process_event` (default arm) | High |
| W-6 | Low | Stripe signature verifier checks only the first `v1=` — secret-rotation breaks verification | `payment/stripe_webhook.gleam:parse_signature_header` | High |
| W-7 | Low | Amount/currency not verified against expected price — any completed session unlocks (reconcile-and-warn only) | `payment/webhook_handler.gleam:598-625` | High |
| W-8 | Info | PostHog identify ships landlord email as `$set` person property, consent-independent | `auth/auth_handler.gleam:259-266, 486-490` | High |
| W-9 | Info | Twilio webhook signature carries no timestamp (no replay window), mitigated only by idempotent state | `notification/twilio_webhook.gleam:verify_signature` | High |

---

## W-1 — `checkout.session.completed` never checks `payment_status` (Medium)

**Trigger condition:** Stripe Checkout Dashboard enables an asynchronous payment method (SEPA Direct Debit, Klarna, bancontact, Sofort, etc.). For those, `checkout.session.completed` fires with `data.object.payment_status == "unpaid"` and funds settle (or fail) later via `checkout.session.async_payment_succeeded` / `async_payment_failed`.

**Evidence:** The event decoder reads only `id`, `type`, `data.object.id`, `payment_intent`, `metadata.vacancy_id`, `metadata.sku_type`, `amount_total`, and `consent.terms_of_service` — there is no `payment_status` field decoded and no branch that consults it:

```gleam
use amount_total <- decode.subfield(["data", "object", "amount_total"], decode.optional(decode.int))
// ... no decode.subfield(["data","object","payment_status"], ...) anywhere
```

`run_completed_side_effects` calls `sql.complete_payment` unconditionally, which flips `status='completed'` and then `unlock_vacancy` flips `is_paid=true`. The `async_payment_failed` event falls into the default arm of `process_event` (`_ -> wisp.json_response("{}", 200)`) — an ack-and-ignore.

**Exploit sketch:** A landlord selects an async method at checkout; the webhook marks the payment completed and unlocks the vacancy while the bank transfer is still pending. If the transfer subsequently fails (`async_payment_failed`, ignored), the vacancy stays unlocked and the payment row stays `completed` with no reconciliation — the analysis was effectively delivered for free. This also breaks the "Stripe webhook only unlocks when payment is valid" invariant's spirit (payment not yet captured).

**Remediation:** Decode `data.object.payment_status` and only run the completed side-effects when it equals `"paid"`; add handlers for `checkout.session.async_payment_succeeded` (process) and `async_payment_failed` (mark failed + re-lock or refund path). Belt-and-braces: also check `data.object.status == "complete"`.

---

## W-2 — Unlock vacancy keyed from event metadata, not cross-checked against the payment row (Medium)

**Trigger condition:** A signed Stripe event arrives whose `metadata.vacancy_id` differs from the `vacancy_id` recorded on the matching `payment` row (the authoritative record). Requires Stripe-side metadata tampering or an internal bug — not directly forgeable by a tenant, but the class of "cross-vacancy unlock" is what the cross-check exists to prevent for `sku_type` and is conspicuously absent for `vacancy_id`.

**Evidence:** `complete_payment` returns only `id` and `sku_type` — never `vacancy_id`:

```gleam
// payment/sql.gleam
UPDATE payment SET status='completed', ... WHERE stripe_session_id = $1 AND status = 'pending'
RETURNING id::text, sku_type;
```

The unlock then takes `vacancy_uuid` from the event's metadata parse, not from the row:

```gleam
// webhook_handler.gleam:513-530
case vacancy_id_opt {
  None -> Error(MalformedMetadata(...))
  Some(vacancy_id) ->
    case uuid.from_string(vacancy_id) {
      Ok(vacancy_uuid) -> ... dispatch_completed_by_sku(..., vacancy_uuid, ...)
```

The `sku_type` metadata-vs-row cross-check exists (`sku_type_metadata_opt != row.sku_type → MalformedMetadata`), which demonstrates the intended pattern — but the vacancy identity gets no equivalent check. `unlock_vacancy(vacancy_uuid)` then flips `is_paid=true` on *whichever* vacancy the metadata named.

**Exploit sketch:** If metadata for a legitimately-paid session ever names vacancy B while the payment row was created for vacancy A (metadata tampering at Stripe, a code regression, or a mid-flight schema change), vacancy B is unlocked on vacancy A's charge. The only current defense is that `create_checkout_session` writes metadata from the same `vacancy_uuid` it writes into the `payment` row — a single source-of-truth mismatch would silently break it.

**Remediation:** Have `complete_payment` also `RETURNING vacancy_id`, and compare it to `metadata.vacancy_id` inside `run_completed_side_effects` (fail-closed `MalformedMetadata` on mismatch), mirroring the existing `sku_type` cross-check. This makes the payment row the sole source of truth for *which* vacancy to unlock.

---

## W-3 — Raw `Host` header flows into Stripe redirect URLs (Low)

**Trigger condition:** An authenticated landlord POSTs to `/api/v1/payment/checkout` or `/api/v1/payment/extension/checkout` with a forged `Host` header (e.g. `Host: evil.example`).

**Evidence:** The router reads the header with no allowlist — the only unvalidated `host` read in the codebase (everything else goes through `domain_helpers.validate_origin_domain` or `http_origin.canonical_origin`, both allowlisted):

```gleam
// router.gleam:770-777
let origin_host = request.get_header(req, "host") |> result.unwrap("righttenantry.ie")
payment_handler.handle_create_checkout(req, ctx.config, landlord, origin_host)
```

`origin_host` then flows into the Stripe session's `success_url` / `cancel_url`:

```gleam
// payment_handler.gleam:456-463
let scheme = case string.contains(origin_host, "localhost") { True -> "http" False -> "https" }
let base = scheme <> "://" <> origin_host
let success_url = base <> "/vacancies/" <> vacancy_id <> success_query_param_for(sku)
let cancel_url  = base <> "/vacancies/" <> vacancy_id
```

These are sent verbatim to Stripe (`stripe_client.create_checkout_session`), which redirects the browser to them after payment. Stripe does not, by default, restrict redirect domains.

**Exploit sketch:** The victim is the attacker themselves (they set their own Host), so this is a self-inflicted open redirect — the paying landlord's browser lands on `https://evil.example/vacancies/...?payment=success&session_id=cs_...` instead of the app. The `session_id` leaked is the attacker's own, and `handle_verify_payment` is ownership-gated, so no cross-user secret leaks. Real impact is low, but it is an inconsistency with the rest of the codebase, could matter if a reverse-proxy misconfiguration ever forwards untrusted Host, and would let a phishing page mimic the post-payment flow. The `string.contains(origin_host, "localhost")` scheme sniff is also bypassable (`Host: evil.localhost.example` → `http://`).

**Remediation:** Route the two checkout handlers through `domain_helpers.validate_origin_domain(req)` (or `http_origin.canonical_origin`) instead of the raw `host` header, so redirect hosts are pinned to the allowlist exactly like the vacancy-creation and email-link paths already are.

---

## W-4 — Inbound email auto-reply is an unauthenticated outbound mail relay (Medium)

**Trigger condition:** Anyone emails a vacancy's public inbound address (per-vacancy reply-to). The webhook is Svix-signed, but Svix only authenticates *Resend* as the sender — the person who triggered the inbound email is unauthenticated, and the app replies to an address it extracts from the message.

**Evidence:**

```gleam
// inbound_handler.gleam (auto-reply path)
let contact = email_parser.extract_contact(email_text)
let valid_sender_email = email_parser.valid_contact_email(contact)
let reply_to = email_parser.reply_recipient(valid_sender_email, payload.from_address)
case reply_to { Some(recipient) -> email_client.send_auto_reply(resend_api_key, recipient, ...) }
```

`reply_recipient` accepts the *body-extracted* address (first non-portal email-like token, validated by `is_valid_email`) or, failing that, the envelope `from_address`:

```gleam
// email_parser.gleam
pub fn reply_recipient(valid_sender_email, from_address) {
  case valid_sender_email { Some(e) -> Some(e); None -> ... Some(from_address) }
}
```

**Exploit sketch:** An attacker sends a message to `apply-<code>@inbound...` with `victim@third-party.com` as the first email-like token in the body (or as the envelope From). The platform then sends `victim@third-party.com` a branded "complete your application" email from its own sending domain. There is no application-layer rate limit on this path (only Resend/Svix's own inbound limits), so it is a 1:1 spam/abuse relay using the platform's domain reputation, potentially hitting arbitrary third parties. The vacancy is correctly resolved by `to_address` (the true recipient), so this is *not* a cross-vacancy attach — the concern is purely outbound-mail abuse.

**Remediation:** Restrict the auto-reply recipient to the envelope `from_address` only (drop the body-email preference for replying, or require the body address to equal the envelope address); add a per-vacancy/per-source rate limit or daily cap on auto-replies; consider suppressing auto-reply to domains that aren't the originating mailbox's domain.

---

## W-5 — No refund/dispute webhook handling (Low)

**Trigger condition:** A landlord's payment is refunded or a chargeback/dispute is filed (`charge.refunded`, `charge.dispute.created`, `charge.dispute.closed`).

**Evidence:** `process_event` routes only `checkout.session.completed` and `checkout.session.expired`; every other event type hits the default arm:

```gleam
// webhook_handler.gleam process_event
_ -> wisp.json_response("{}", 200)  // unknown event type — ack without claiming
```

There is no `charge.refunded` / `charge.dispute.*` / `checkout.session.async_payment_failed` handling anywhere. A refund or chargeback leaves `payment.status='completed'` and `vacancy.is_paid=true` — the vacancy remains unlocked and AI analyses remain available despite the charge being reversed.

**Exploit sketch:** A landlord pays to unlock, consumes the analyses, then disputes the charge. The system never re-locks the vacancy or marks the payment refunded. The code comments acknowledge this is "manual until policy" (`refund_handling_manual_until_policy`), but the defended invariant "Stripe webhook only unlocks a vacancy when the payment is valid" has no symmetric revocation path — a real integrity gap rather than a phantom edge case.

**Remediation:** Add handlers for `charge.refunded` (mark payment refunded, optionally re-lock the vacancy) and `charge.dispute.created` (flag for manual review + Sentry). At minimum, surface these events to Sentry so ops can act instead of silently acking.

---

## W-6 — Stripe verifier checks only the first `v1=` signature (Low)

**Trigger condition:** Stripe secret rotation. During rotation Stripe signs webhooks with *multiple* secrets and sends multiple `v1=` entries in `Stripe-Signature`; the receiving endpoint should accept if *any* signature matches a configured secret.

**Evidence:**

```gleam
// stripe_webhook.gleam
fn parse_signature_header(header) {
  let parts = string.split(header, ",")
  let v1 = parts |> find_prefixed("v1=")  // returns the FIRST v1= only
  ...
}
```

If the first `v1=` corresponds to the newly-added secret (or the ordering is otherwise unfavorable), `crypto.secure_compare` fails against the single configured `STRIPE_WEBHOOK_SECRET` → 401 → Stripe retries and eventually gives up. This is an availability failure during rotation, not a bypass (HMAC can't be forged).

**Remediation:** Try every `v1=` in the header against the secret (and, ideally, support a set of secrets during rotation), accepting on any match.

---

## W-7 — Amount/currency never verified against expected price (Low)

**Trigger condition:** Any completed session unlocks regardless of the charged amount. Only the SKU's *presence* is cross-checked (`sku_type`), never the amount or currency.

**Evidence:** `log_amount_drift` logs and returns `Nil` — the reconcile value is written to the row, and unlock proceeds:

```gleam
// webhook_handler.gleam:598-625
fn log_amount_drift(amount_total_opt, sku_type, config) -> Nil {
  let expected = case sku_type { "vacancy_extension" -> ...; _ -> config.stripe_vacancy_price_cents }
  case amount_total_opt { Some(n) if n != expected -> wisp.log_warning(...) _ -> Nil }
}
```

There is no currency check either (`"EUR"` is hardcoded at the CAPI fire, not validated against the row). Because `line_items[0][price]` is the env `STRIPE_*_PRICE_ID` and sessions are server-created, the amount is not client-controllable — the risk is config-integrity (env price ID drifting from the Dashboard price) rather than direct exploitation. `allow_promotion_codes=true` makes sub-list-price legitimately reachable, which is why reconcile-and-warn is a deliberate posture.

**Exploit sketch:** If `STRIPE_VACANCY_PRICE_ID` in env ever points at a mispriced price object (e.g. a €0 or €1 test price in the live Dashboard), completed sessions for that price would unlock vacancies for effectively nothing — and the only signal would be a warning log. Not directly attackable, but the "does any `checkout.session.completed` unlock?" question answers: yes, with no amount/currency gate.

**Remediation:** Reject (or loudly alert + still reconcile) when `amount_cents` is below a floor or when `currency != "eur"`, and add a startup check that the env price ID's `unit_amount` matches `STRIPE_*_PRICE_CENTS`. Also fix the SKU-blind fallback at `webhook_handler.gleam:337-344` which falls back to the *unlock* price even for extension sessions.

---

## W-8 — PostHog identify ships landlord email, consent-independent (Info)

**Trigger condition:** Every signup and login.

**Evidence:** `$set` person properties include the raw email; the signup identify is explicitly "consent-independent" (first-party attribution), and neither `analytics_granted` nor `marketing_granted` is consulted for the PostHog identify:

```gleam
// auth_handler.gleam:259-266
posthog_client.identify_with_set_once(posthog, row.id, [#("email", json.string(email_lower))], attribution...)
// auth_handler.gleam:486-490
posthog_client.identify(posthog, row.id, [#("email", json.string(l.email))])
```

`distinct_id` is the landlord UUID (pseudonymous); no client IP is included in the server-side capture. This is a data-minimization/privacy observation rather than a breach: landlord email is sent to a third-party analytics processor without an analytics-consent gate, in contrast to the Meta CAPI path which gates `CompleteRegistration`/`Lead` on `marketing_granted`.

**Remediation:** Gate the PostHog `$set email` property on `analytics_granted` (or hash it), consistent with the Meta path's consent posture. If PostHog is treated as a sub-processor under the privacy notice, confirm the email field is disclosed there.

---

## W-9 — Twilio webhook signature has no timestamp (Info)

**Trigger condition:** A captured, valid Twilio status callback is replayed.

**Evidence:** Twilio's `X-Twilio-Signature` is `HMAC-SHA256(auth_token, url + sorted-params)` — it authenticates the payload but contains no timestamp, so unlike Stripe/Svix there is no freshness window:

```gleam
// twilio_webhook.gleam verify_signature — no timestamp validation
```

Replay is mitigated by idempotency: `apply_delivery_failure` only transitions rows whose status is `IN ('queued','contact_initiated')`, and a stale bounce against a post-correction row is stood down by the `genuine_failure` timestamp comparison. So a replayed `failed` status cannot re-drive state once the row has left the live set. This is defense-by-idempotency rather than by freshness — acceptable, but worth recording that the Twilio callback path has no replay window, unlike its Stripe/Svix siblings.

**Remediation:** None strictly required given idempotency; optionally track `MessageSid`+`MessageStatus` in a small dedup table if stricter replay resistance is wanted.

---

## SSRF sink inventory

Every outbound HTTP client, its host source, and whether any request-derived data reaches the URL. **Verdict: no SSRF — all fetch hosts are fixed constants or env config; no request-derived host.**

| Sink | URL/host source | Request-derived data in URL? | Verdict |
|------|-----------------|------------------------------|---------|
| `payment/stripe_client.gleam` | fixed `api.stripe.com` | `success_url`/`cancel_url` carry the raw `Host` header (see W-3) — host itself is fixed | Clean (host), W-3 for redirect target |
| `notification/email_client.gleam` | fixed `api.resend.com` | `email_id` appended to path (from Svix-signed payload) | Clean |
| `notification/sms_client.gleam` | fixed `api.twilio.com` + env `account_sid` | none | Clean |
| `reference_checks/lookup.gleam` | fixed `lookups.twilio.com` | `phone` percent-encoded into path (E.164) | Clean (fixed host, encoded path) |
| `meta/meta_client.gleam` | fixed `graph.facebook.com` + env api_version + digits-validated `pixel_id` | `source_url_base` from env config, not request | Clean |
| `posthog/posthog_client.gleam` | env `POSTHOG_API_HOST` (normalised) | none | Clean |
| `auth/supabase.gleam` | env `SUPABASE_URL` | `auth_user_id` (UUID from DB) in admin path; `redirect_to` hardcoded server-side | Clean |
| `storage/storage_client.gleam` | env `supabase_url` | `bucket`/`path` from UUIDs + server-derived extension | Clean |
| `ai/ai_client.gleam` | env `AI_SERVICE_URL` (also the identity-token audience) | none | Clean |
| `sentry/sentry_client.gleam` | fixed Sentry ingest | none | Clean |

`origin_domain` usage note: `vacancy.origin_domain` flows into email/reference-check URLs (`email_client.build_entity_url`, `reference_checks/form_handler.gleam:696`, `sweep.gleam:704`) but is **validated at write time** via `domain_helpers.validate_origin_domain` (allowlist: `righttenantry.ie`, `www`, `localhost`, or the `-755972035138.europe-west1.run.app` suffix), so a forged `Host`/`X-Forwarded-Host` cannot poison it.

---

## Verified-clean surfaces

- **Stripe signature verification** (`payment/stripe_webhook.gleam`) — constant-time `crypto.secure_compare`, 5-min two-sided tolerance, HMAC over `{ts}.{body}` with the full `whsec_` secret. ✓
- **Svix signature verification** (`inbound_email/svix.gleam`) — constant-time, 5-min two-sided tolerance, correct `{id}.{timestamp}.{body}` construction, `whsec_` base64-decode. ✓
- **Twilio signature verification** (`notification/twilio_webhook.gleam`) — constant-time, correct sorted-params canonicalization; `Disabled` config returns 403 (no unguarded path). ✓
- **Stripe event dedup** — `claim_stripe_event` `INSERT … ON CONFLICT (event_id) DO NOTHING` inside the same transaction as the state change, so a crash rolls back the claim and Stripe retries cleanly. ✓
- **Inbound email dedup** — `create_inbound` `ON CONFLICT (resend_email_id)`; auto-reply fires only on the freshly-inserted row. ✓
- **Reference-check webhook idempotency** — guarded `WHERE status IN ('queued','contact_initiated')` transitions; stale-bounce stand-down via post-correction timestamp comparison. ✓
- **`origin_domain` validation** (`domain_helpers.validate_origin_domain`, `http_origin.canonical_origin`) — allowlist + hostname-charset check; the only unvalidated host read is the W-3 checkout route. ✓
- **Meta CAPI** (`meta/meta_client.gleam`, `meta/dispatch.gleam`) — email & external_id SHA-256-hashed, empty fields omitted, access token in body not query string, `source_url_base` config-fixed, `_fbp`/`_fbc` length-capped + format-validated, `Lead`/`CompleteRegistration` gated on `marketing_granted` at call sites (`auth_handler.gleam:1443`, `vacancy_handler.gleam:1981`); Purchase is a documented legitimate-interest carve-out. ✓
- **PostHog capture key** (`public_capture_key`) — shape-validated (`phc_` + base64url) before embedding in inline `<script>`, preventing script-context breakout on public pages. ✓
- **Uploads** (`storage/file_validation.gleam`, `application/document_upload.gleam`) — magic-byte type detection (PDF/JPEG/PNG only), 5MB per-file / 12-file / 17MB aggregate caps, field-name whitelist, category server-derived, storage path = `vacancy_uuid/application_uuid/file_uuid.ext` (no user-controlled segments), orphan-blob cleanup. ✓
- **Document download** (`application_detail_handler.handle_document_download`) — ownership enforced in SQL (document→application→vacancy→`vacancy.user_id`), 15-min signed URL TTL, `cache-control: no-store, private`, `referrer-policy: no-referrer`. ✓
- **Email HTML injection** (`notification/email_client.gleam`) — every user-derived field (`property_name`, names, addresses, URLs) passes `escape_html`; `headers` (List-Unsubscribe / Reply-To) are hardcoded. ✓
- **Email header injection** — all mail goes through the Resend JSON API (`subject`/`html` as JSON strings), so CRLF in `property_name` cannot inject SMTP headers; no raw SMTP path exists. ✓
- **Bulk invite / reminders** (`inbound_email/inbound_handler.gleam`) — recipient emails validated via `is_valid_email`, 10-recipient cap, vacancy ownership checked, atomic stamp+send with self-healing clear-on-failure. ✓
- **GCP identity token** (`ai/ai_client.gleam`) — audience = `AI_SERVICE_URL`, metadata-server fetch with `metadata-flavor: Google`, fail-closed on Cloud Run (`K_SERVICE`/`ENV` detection), dev fallback gated on non-hosted env only. ✓
- **Supabase GoTrue** (`auth/supabase.gleam`) — `redirect_to` hardcoded server-side (`password_reset_handler.gleam:77`); admin endpoints use `service_role` only with server-derived UUIDs. ✓
