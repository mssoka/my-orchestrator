# Lens: Security (source: `security`) — Perkins RC3.5 r1

Read and follow `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/lens-prompts/_shared_context.md` first (inputs, invariants, output contract). Then apply this lens.

## YOUR LENS — OWASP-oriented security review of the diff
Identify:
- Auth/authz gaps in new endpoints, routes, or handlers (the manual-fire route `POST /api/v1/internal/reference-checks`; verify `response_helpers.require_internal_secret` is actually applied and the route is NOT in a public/unauthed section).
- Missing input validation at system boundaries.
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages). The sweep mints form tokens, reads RESEND_API_KEY/TWILIO — check none are logged.
- Data exposure (sensitive fields — referee PII, contact data — in logs, Sentry tags, or responses).
- Injection vectors (SQL, command, path traversal). The sweep builds SQL via Squirrel (parameterised) — but the integration test and any raw `pog.query` string concatenation (`'... WHERE id = '' <> row_id <> ...'`) is a SQL-injection surface; check it.
- Unsafe deserialization, insecure defaults, missing CSRF protection.
- The form-token mint strength (`wisp.random_string(48)`) and TTL.

For Sentry captures: the sweep tags Sentry events with `reference_call_id` (a UUID, not PII) — verify no referee PII lands in Sentry message/tags.

## OUTPUT
Write ONLY your JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/security.json`
Use `"source": "security"`. Then stop.
