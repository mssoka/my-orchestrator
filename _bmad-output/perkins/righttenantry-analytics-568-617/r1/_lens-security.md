# Lens: Security (source: `security`)

Read your shared context first: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/_shared.md — it defines your inputs, the round-specific guards, the output schema, and the accuracy mandate. Your assigned `source` value is `security`. Your output path is: /Users/moses/code/_bmad-output/perkins/righttenantry-analytics-568-617/r1/security.json

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries (note: the OAuth initiate URL now accepts first-touch query params — attacker-controlled input into a signed cookie; check clamping, key allow-listing, cookie size)
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state — e.g. does anything leak the first-touch params or Meta event data to third parties?)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps (the new `rt_first_touch` cookie: signing, expiry, clear-on-terminal-response, host prefix, consent implications)
