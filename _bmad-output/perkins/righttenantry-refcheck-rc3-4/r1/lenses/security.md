LENS: security (source tag: "security") — Security review. EXACT OUTPUT PATH: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/security.json`

**FIRST: read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/_shared_header.md` for the output contract, schema, and accuracy mandate.** Then apply your lens below.

## YOUR LENS — OWASP-oriented security review of the diff

The new routes are token-capability routes (`/reference/:token/...`) — the ~288-bit form_token IS the auth (AD-3); the referee has no login. Identify:

- **Auth/authz:** can a terminal/expired/unknown token be acted on? Is every state transition guarded by the pre-state in the SQL WHERE? Can an attacker submit/decline/object a row they shouldn't?
- **CSRF:** the `["reference", ..]` prefix skip is the design (token IS the capability) — verify it covers all new POSTs (a 403 on a legit referee would be a real bug); verify no new route is OUTSIDE the prefix.
- **Token handling:** does the form_token leak into logs, Sentry messages, audit details, notification bodies, objection_log payload, or the HTML? The `redact_token_route` prefix should redact the path. Confirm.
- **Input validation at boundaries:** the decline `reason` (free text) — XSS if rendered? Stored where? The `_focus_seconds` parse. The objection `payload_ref` (IP/UA) — is it sanitised before JSON?
- **Injection:** SQL is Squirrel-typed (verify the generated `sql.gleam` passes typed params, no string interpolation into SQL). The `result.gleam` attempts parsing.
- **Objection evidence integrity:** `reference_objection_log` single writer (only `apply_objection`), Art 21 evidence survives parent deletions (no FK cascade), `payload_ref` provenance.
- **Double-submit / replay:** one-submission enforcement — no duplicate audit/notification/result on a second POST.

For each finding, paste the exact code lines. `[]` is a fine answer.
