# Lens: SECURITY (source: `security`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/prompts/_preamble.md` in full and internalize the lens-guards (especially the §4.2 / raw-IP-UA guard — that one produces false positives if misread) + the fix-audit scope.

OWASP-oriented security review of the diff at `5576ccb`. Identify: auth/authz gaps in new handlers; missing input validation at boundaries; unsafe secret/token/credential handling; data exposure; injection vectors (SQL, XSS, command, path traversal, SSRF); unsafe deserialization; session/cookie gaps.

## Fix-audit priority — regression guard (the B1 fix + W1 extraction must not break a security property)

- **Did the B1 fix break honest stamping?** The B1 guard SKIPS stamping on re-trigger (`created_ids == []`) and scopes the WRITE to new rows. A SKIPPED stamp must leave the honest state (the existing fraud_signals, or null), NOT a fabricated one. Verify: when `created_ids == []`, nothing is written (the submitted sibling keeps its real signals); when a new row IS stamped, it gets the honest creation object. No path where the skip writes a null/placeholder over a real signal, or stamps a fabricated value.
- **Did the W1 extraction change behavior?** `fraud_inputs.gleam` moves the helpers out of line. Verify the moved fns are byte-identical in logic (no security-relevant change — e.g. no input validation dropped, no NULLIF guard weakened in `cross_application_reuse`).

## Delta pass — the §4.2 boundary + SQL parameterization (carry from r1, re-verify at the fixed sha)

- **The §4.2 boundary.** rc3-7 stores raw `referee_ip`/`referee_user_agent` INSIDE `form_session` (by design — D5, RC4.1 strips later). The IN-SCOPE leak question is narrow: **did rc3-7 ADD any landlord-facing API response, SSR page, or notification payload that surfaces the raw IP/UA or the full `form_session` block to a client?** The `form_handler` path is the public `/apply` referee SSR — verify what it returns to the referee's browser does NOT include fraud_signals (the referee must not see their own provenance signals or the applicant's IP/UA). Verify the audit/notification payloads don't carry raw IP/UA. (Do NOT flag the in-form_session storage itself — by design.)
- **SQL injection.** All new/changed queries (`count_cross_application_contact_reuse`, `get_application_reference_contacts`, `stamp_creation_fraud_signals`, `stamp_referee_contact_invalid`, amended `get_form_context_by_form_token`, `get_application_reference_data`) must be Squirrel-parameterized (no string-interpolated SQL). Confirm params are bound (`pog.parameter(pog.text(...))`), not concatenated. NOTE: a test helper in `reference_checks_trigger_integration_test.gleam` uses a hand-written `pog.query` with string-interpolated `token` in a WHERE clause (`form_token = '<token>'`) — that is TEST-ONLY code (the token is test-controlled), but flag it as a note if present (test code should not model unsafe patterns).
- **Webhook idempotency (W1, re-verify after N3/N4).** The `claim_webhook_event` defense layer is REMOVED. Verify the remaining find+mark live-status scoping (`WHERE status IN ('queued','contact_initiated')`) still prevents double-application of a redelivered delivery-failure. Could a replay now double-transition a row? Read `apply_delivery_failure` + `mark_awaiting_correction` at the fixed sha.
- **Log hygiene.** The `wisp.log_warning` calls (`stamp_creation_fraud: ...` etc.) — do any log contact PII (email/phone/IP) or secrets? They log `uuid`/`ref.id`/query errors — verify nothing sensitive leaks.
- **`stamp_creation_fraud_signals` / `stamp_referee_contact_invalid`** take an id param — verify scoped by id (no mass-update risk); the `jsonb_set`/`$2::jsonb` casts can't be abused.

Do NOT flag the in-form_session IP/UA storage itself (by design — see guard). Do flag any NEW exposure path you actually verify.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/security.json`, using `source: "security"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
