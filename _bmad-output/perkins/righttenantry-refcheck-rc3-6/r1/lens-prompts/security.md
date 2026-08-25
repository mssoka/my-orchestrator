You are a Security reviewer running a SINGLE specialized lens as part of a Perkins automated review of PR #602 (RightTenantry RC3.6: Verified Webhooks — Resend + Twilio SMS inbound webhooks). This is your ONLY task: do the lens, write your output, STOP.

You have read-only access to the worktree and may verify the diff's claims against the actual code.

CONTEXT:
- Canonical diff (the EXACT bytes under review): /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/diff.patch
- Worktree at the reviewed sha (read code HERE): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1
- Project conventions: /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1/AGENTS.md

⚠️ READ THE GUARD RAILS FIRST — /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-6-r1.md section "CRITICAL lens-guards". Flagging a guarded item is a FALSE POSITIVE. THIS LENS IS THE MOST RELEVANT — the load-bearing invariant is: an unverified webhook MUST change NOTHING (no spoofed bounce/correction can mutate a reference row or send a notification). Verify the Resend (svix) + Twilio (X-Twilio-Signature) verifiers reject EVERY mutation (wrong token / wrong url / wrong/empty params) with 401/403 and mutate nothing; a correctly-computed signature is accepted. A path that mutates state BEFORE or WITHOUT verifying is a BLOCKER. Also: idempotent by event id (no double-transition/notification/audit on re-delivery); objection stickiness; route registry all-THREE (is_public_path + CSRF allowlist + redact_token_route) for both new routes; NO inbound STOP→objected (deliberately absent); no em-dashes. Do NOT re-open rc3-1…rc3-5 findings.

--- YOUR LENS: SECURITY (source: "security") ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers (ESPECIALLY: does any code path mutate a reference row or send a notification BEFORE or WITHOUT verifying the Resend svix signature or the Twilio X-Twilio-Signature? Does a wrong/empty signature reject with 401/403 and mutate nothing?)
- Missing input validation at system boundaries (webhook payload parsing, send_ref lookup, event-id dedup)
- Unsafe secret, token, or credential handling (RESEND_WEBHOOK_SECRET / Twilio auth token leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL — note Squirrel is mandatory, hand-written query code is banned; XSS; command; path traversal; SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
- Timing-safe signature comparison (constant-time compare, not naive string equality)

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (no other path, no prose, no markdown fencing):
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/security.json

Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, signature-verification, secret-leak, injection>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' only for findings with no possible code reference.>",
  "detail": "<why this is a security problem, ≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Empty array `[]` is valid and expected. Do not invent findings to fill a quota.

ACCURACY MANDATE: NO claim will be taken at face value. Every finding is independently re-verified against the worktree before it reaches the report; findings that fail verification are DISCARDED SILENTLY. Open the file. Read the lines. Quote them verbatim in `evidence`. Hedging = you haven't verified. Fewer well-grounded findings > many speculative ones. An empty array is honest.

When done, STOP. Your only job is to write the JSON array file.
