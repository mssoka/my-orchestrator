# Lens: SECURITY (source: `security`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/prompts/_preamble.md` in full and internalize the lens-guards (especially the §4.2 / raw-IP-UA guard — that one produces false positives if misread).

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Specifics worth checking in THIS diff (verify against the worktree):
- **The §4.2 boundary.** rc3-7 stores raw `referee_ip`/`referee_user_agent` INSIDE `form_session` (by design — D5, RC4.1 strips later). The IN-SCOPE leak question is narrow: **did rc3-7 ADD any landlord-facing API response, SSR page, or notification payload that surfaces the raw IP/UA or the full `form_session` block to a client?** The form_handler path is the public `/apply` referee SSR — verify what it returns to the referee's browser does NOT include fraud_signals (the referee must not see their own provenance signals). Verify the audit/notification payloads don't carry raw IP/UA.
- **SQL injection.** All new queries (`count_cross_application_contact_reuse`, `get_application_reference_contacts`, `stamp_creation_fraud_signals`, `stamp_referee_contact_invalid`, amended `get_form_context_by_form_token`, `get_application_reference_data`) must be Squirrel-parameterized (no string-interpolated SQL). Confirm parameters are bound, not concatenated.
- **Webhook idempotency (W1).** The `claim_webhook_event` defense layer was REMOVED. Verify the remaining find+mark live-status scoping (`WHERE status IN ('queued','contact_initiated')`) still prevents double-application of a redelivered delivery-failure. Could a replay now double-transition a row? Read `apply_delivery_failure` + `mark_awaiting_correction` carefully.
- **Log hygiene.** The new `wisp.log_warning` calls — do any log contact PII (email/phone/IP) or secrets? The `event_id`/`source` logging is fine; verify nothing sensitive leaks.
- **`stamp_creation_fraud_signals` / `stamp_referee_contact_invalid`** take an id param — verify they're scoped by id (no mass-update risk) and the `jsonb_set`/`$2::jsonb` casts can't be abused.

Do NOT flag the in-form_session IP/UA storage itself (by design — see guard). Do flag any NEW exposure path you actually verify.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/security.json`, using `source: "security"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
