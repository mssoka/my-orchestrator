# Lens brief: security (source value: `security`)

First read the shared review brief at
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/shared-block.md`
and follow it exactly (inputs, spec, output contract, accuracy mandate).

Your assigned source value is `security`. Write your findings JSON array to:
`/Users/moses/code/_bmad-output/perkins/righttenantry-ai-reference-calls-research/r1/security.json`

## Your lens (from the code-review skill)

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

**Calibration for this docs-only PR:** there is no executable code in the diff. Apply
the lens as: (a) secrets, credentials, personal data, or confidential information
committed into the research documents themselves; (b) recommendations in the documents
that would create concrete security/privacy exposure if implemented as written (e.g.
recording/transcript retention without limits, PII in the handoff schema without
protection, spoofable caller identity unaddressed). Only report exposure that is
concretely described in the diff — quote it.
