# Lens: SECURITY (source: `security`) — Perkins r2 FIX-AUDIT

OWASP-oriented security review of the fix delta. Identify:
- Auth/authz gaps in new/changed endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session/cookie handling gaps

**This is a FIX-AUDIT round.** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/lens-common.md` FIRST — fix-audit scope (B1+W1-W5 verify FIXED), lens-guards (do NOT re-litigate, do NOT re-open rc3-4).

Security-relevant focus for this delta:
- The new `sentry_client.capture` calls (W3 / B1): do they leak PII (applicant/referee email/phone, reference_call id) into Sentry tags/messages? The `capture` tags include `reference_call_id` and messages include `row.id` + `query_error(err)` text + the notification `reason` — verify nothing sensitive bleeds.
- `wisp.log_error` in `dispatch_warm_handoff`: does the logged string leak PII?
- The manual-fire route (`sweep_handler`): shared-secret auth still intact; the W4 fix threads `Disabled` sentry — confirm no authz regression.
- `now_iso()` / `timestamp.system_time()`: no input handling, low risk — but confirm.
- Squirrel parameterization: the delta touches no SQL files (all SQL pre-exists); confirm no raw string SQL was introduced.

**Inputs:** `lens-common.md`, `delta-r1-r2.patch`, `diff.patch`, `r1/consolidated.json`. Verify against worktree `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` (read-only).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/security.json` — then stop.
Schema per element:
```
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ from the file, verbatim>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>",
  "round2_audit": "<FIXED | STILL OPEN | NEW | CARRIED-N<n> | N/A>"
}
```
ONLY the JSON array in the file. `[]` is valid. Open the file, read the cited lines. Speculation without quoted evidence is dropped.
