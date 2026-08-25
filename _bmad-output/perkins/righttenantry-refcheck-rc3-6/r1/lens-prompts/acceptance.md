You are an Acceptance Auditor running a SINGLE specialized lens as part of a Perkins automated review of PR #602 (RightTenantry RC3.6: Verified Webhooks — Resend + Twilio SMS inbound webhooks). This is your ONLY task: do the lens, write your output, STOP.

You have read-only access to the worktree and may verify the diff's claims against the actual code.

CONTEXT:
- Canonical diff (the EXACT bytes under review): /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/diff.patch
- Worktree at the reviewed sha (read code HERE): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1
- Project conventions: /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-6-r1/AGENTS.md

SPEC / CONTEXT (read as needed — your acceptance source of truth):
- Perkins briefing (guard rails — READ FIRST): /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-refcheck-rc3-6-r1.md
- Job briefing: /Users/moses/code/_bmad-output/briefings/righttenantry-refcheck-rc3-6.md
- Story RC3.6 (FR-RC8 wrong-contact/bounce, FR-RC9 objection): /Users/moses/code/_bmad-output/planning-artifacts/epics-reference-checking-v1-2026-07-30.md
- Architecture (AD-6 objection sticky, AD-14 transitions, AD-15 liveness, AD-16 audit row, §9.2 objection log, the webhook-verification design, §8.3 notification values): /Users/moses/code/_bmad-output/planning-artifacts/architecture-reference-checking-v1-2026-07-29.md
- Issue #548: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/issue-548.json

⚠️ GUARD RAILS — from the briefing's "CRITICAL lens-guards". Flagging a guarded item is a FALSE POSITIVE. Especially: the original briefing AC #2 ("inbound STOP→objected on Twilio webhook") was STALE and IMPOSSIBLE (Twilio alphanumeric sender is one-way; user confirmed Q1=A correction: the Twilio webhook is DELIVERY CALLBACKS ONLY). Do NOT flag "missing STOP→objected" — that path is deliberately absent. The in-app-only notification (Q3=B2, no email) is user-confirmed — do NOT flag "should email." Signature verification is load-bearing. Idempotent by event id. Objection stickiness. Route registry all-THREE. No em-dashes. Do NOT re-open rc3-1…rc3-5 findings.

--- YOUR LENS: ACCEPTANCE (source: "acceptance") ---
Audit the diff against the spec and context docs. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY this path (no other path, no prose, no markdown fencing):
/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-6/r1/acceptance.json

Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. ac-violation, scope-drift>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' only for findings with no possible code reference.>",
  "detail": "<why this violates the spec, ≤40 words — quote the AC/constraint>",
  "recommended_fix": "<≤40 words>"
}

Empty array `[]` is valid and expected. Do not invent findings to fill a quota.

ACCURACY MANDATE: NO claim will be taken at face value. Every finding is independently re-verified against the worktree + spec before it reaches the report; findings that fail verification are DISCARDED SILENTLY. Open the file. Read the lines. Quote them verbatim in `evidence`. Fewer well-grounded findings > many speculative ones. An empty array is honest.

When done, STOP. Your only job is to write the JSON array file.
