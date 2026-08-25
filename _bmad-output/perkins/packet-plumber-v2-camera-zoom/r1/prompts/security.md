--- YOUR LENS (source tag: security) ---

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a desktop game (Odin + raylib) with no network surface, so classic web vectors mostly don't apply — focus on what does: the new env-var-driven PP_DEBUG/PP_CAM_E2E drive paths (can they run in release builds? do they write anywhere unsafe?), input-injection surfaces, file writes (screenshot paths), and any debug surface that leaks into release builds.
