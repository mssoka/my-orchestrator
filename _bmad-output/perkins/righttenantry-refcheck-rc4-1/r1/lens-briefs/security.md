# LENS: security (source tag: `security`) — Perkins r1 refcheck rc4-1

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-1/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

OWASP-oriented security review of the diff. Focus areas specific to this change:

- **Data exposure — THE critical lens:** the §4.2 internal-only fields (raw referee IP, referee User-Agent inside `result.fraud_signals.form_session`, `form_token`, `objection_detail.payload_ref`) MUST NOT reach the client payload. Verify by tracing the FULL path: SQL SELECT list → `result::text` (stripped via `#-`) → `ListReferenceCallsForDetailRow` → `encode_reference_call` → wire. Attack the seam: what if a stored result is double-encoded JSON (a string inside the JSONB that itself contains the keys), or the keys appear under a different path than the guard checks? What if `result` is an object but `fraud_signals` is a JSON *string* containing the escaped keys? The `jsonb_typeof` guard's ELSE branch passes the text through VERBATIM — does any reachable shape carry the internal keys past the strip? Consider the escaped wire form (`\"referee_ip\"` inside the result JSON-string field) — is the guard checking the right byte sequences?
- **Authz:** the new read paths (`list_reference_calls_for_detail`, `get_attestation_on_file`) are keyed on `app_uuid` — is ownership enforced upstream (landlord → vacancy → application)? A cross-tenant read would leak referee PII (names, emails, phones, IPs).
- **PII in the payload:** referee contact trios (if carried) are third-party personal data — GDPR. Also `attestation_on_file` — fine. Any raw IP/UA anywhere else in the payload?
- **`verify_payload_has_no_internal_fields`** — a belt-and-braces guard — is it used in production code or only tests? If only tests, is that a defense gap? (The SQL strip is the real boundary.)
- **SQL injection:** new SQL files use `$1::uuid` parameters — confirm no string interpolation. The test-helper change in `reference_exit_routes_integration_test.gleam` moves from string concatenation to `pog.parameter` — confirm.
- **Denial of service:** one corrupt row 500-ing the whole detail endpoint (the `#-` throw) — the jsonb_typeof guards address this; confirm no OTHER per-row decode in the new read can throw the whole read (e.g. `attempts::text` NULL → decode.string failure).
- **Session/auth changes:** none expected in this diff — confirm nothing auth-related regressed.

Output: only real, verified findings with quoted evidence.
