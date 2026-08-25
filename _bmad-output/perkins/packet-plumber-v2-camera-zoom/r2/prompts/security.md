--- YOUR LENS (source tag: security) ---

OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a desktop game (Odin + raylib) with no network surface, so classic web vectors mostly don't apply — focus on what does:

- The settings file parser (app/settings.odin): a user-controlled binary file read from the HOME dotfile path — the new v1/v2 branching (6-byte vs 7-byte), out-of-range byte handling, checksum validation, and what a malicious/corrupt file can achieve. Check the length guards before every data[i] index — an out-of-bounds read on a short file is the class of bug that matters here.
- The new env-var drives (PP_CAM_E2E, existing PP_NOC_E2E / PP_DEBUG): can they leak into release builds? What do they gate (screenshot writes to bin/)? Is the write path (rl.TakeScreenshot) constrained to a fixed path or can it be influenced?
- The settings SAVE path (write-then-rename atomic pattern) — any temp-file symlink/race concern on a shared machine is in scope but weight it realistically (single-user desktop).
- Input-injection surfaces: the poll's synthesized-release guard appends to inp.events from device state — no trust boundary, but flag if it can be driven into unbounded growth.
