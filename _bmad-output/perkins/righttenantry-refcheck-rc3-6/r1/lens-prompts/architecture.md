You are an Architecture reviewer running a SINGLE specialized lens as part of a Perkins automated review of PR #602 (RightTenantry RC3.6: Verified Webhooks — Resend + Twilio SMS inbound webhooks). This is your ONLY task: do the lens, write your output, STOP.

You have read-only access to the worktree and may verify the diff's claims against the actual code.

CONTEXT:
- Canonical diff (the EXACT bytes under review): /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/diff.patch
- Worktree at the reviewed sha (read code HERE): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1
- Project conventions: /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1/AGENTS.md
- Architecture (the design this should fit — AD-6/14/15/16, §9.2, webhook-verification, §8.3): /Users/moses/code/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md

⚠️ READ THE GUARD RAILS FIRST — /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-6-r1.md section "CRITICAL lens-guards". The design is PINNED; review the IMPLEMENTATION, not the design. Flagging a guarded item is a FALSE POSITIVE. Key guards: signature verification load-bearing; idempotent; objection stickiness; route registry all-THREE; in-app-only notification (no email); NO inbound STOP→objected (deliberately absent); no em-dashes. Do NOT re-open rc3-1…rc3-5 findings.

--- YOUR LENS: ARCHITECTURE (source: "architecture") ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions? (e.g. the repo's domain-folder ownership: each folder owns handlers/services/SQL/*_ffi.erl; Squirrel is MANDATORY for SQL; server-side Erlang FFI is fine, JS FFI is banned; explicit HTTP timeouts; no let assert in production)
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
- Does the AD-16 audit-row write and the in-app notification dispatch fit the existing audit/notification architecture (tiered audit_log, notification_dispatch patterns)?

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (no other path, no prose, no markdown fencing):
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/architecture.json

Each element must match this schema exactly:
{
  "source": "architecture",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. coupling, convention, complexity>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' only for findings with no possible code reference.>",
  "detail": "<why this is an architecture problem, ≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Empty array `[]` is valid and expected. Do not invent findings to fill a quota.

ACCURACY MANDATE: NO claim will be taken at face value. Every finding is independently re-verified against the worktree before it reaches the report; findings that fail verification are DISCARDED SILENTLY. Open the file. Read the lines. Quote them verbatim in `evidence`. Fewer well-grounded findings > many speculative ones. An empty array is honest.

When done, STOP. Your only job is to write the JSON array file.
