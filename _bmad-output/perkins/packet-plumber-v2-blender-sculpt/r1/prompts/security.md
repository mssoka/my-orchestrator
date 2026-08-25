--- YOUR LENS (source tag: security) ---

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

For THIS diff the realistic surface is: the Blender .blend fold-in (committed binary sources opened by the pipeline — embedded-script / auto-run risk, asset provenance), the Python tooling (eval/exec use, file handling in strip_png_metadata, sys.path insertion), and committed docs leaking absolute user paths. Judge what the diff actually shows.
