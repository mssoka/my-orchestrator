You are reviewing a code diff (round 2 of an automated review loop). You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r2 — a detached worktree at exactly the reviewed sha 7bb582443d3844d6d349d0144b4caab42c81f196) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line (~5100 lines).

--- ROUND 2 CONTEXT ---
This PR was reviewed once already (round 1). The findings below were delivered to the author; the head commit ("fix: Perkins r1 — RLS-safe sender-state view, single stage-2 gate, test pins") claims to address them. Where they touch your lens, verify the fix actually landed and is correct — and review the whole diff fresh for regressions and new issues.

R1 findings:
1. [blocker, security] Security-definer view inbound_email_sender_state bypasses RLS — enquirer emails readable via public anon key (supabase/migrations/20260731213000_add_inbound_email_sender_state_view.sql:22)
2. [warning, blind+architecture] Stage-2 2-day eligibility gate triplicated across mark/count/list SQL — view centralises only the inputs (mark_followup_reminders_for_vacancy.sql / count_awaiting_for_vacancy.sql / list_awaiting_for_vacancy.sql)
3. [warning, edge] Self-heal stamp-clear silently no-ops if the batched send queue outlasts the new 10-minute freshness window (clear_followup_for_sender.sql; inbound_handler.gleam ~692/733/755)
4. [warning, acceptance] Daft auto-reply in production copy sheet still promises "It takes about 10 minutes" (_bmad-output/creative-campaign/02-production-copy-sheet.md:542)
5. [warning, acceptance] Invite email subject suffix-positions the property name — violates 'property-name-first email subjects' (email_client.gleam:339)
6. [warning, tests] Resend tags array + both new reminder subject lines untested (email_client.gleam:545)
7. [warning, tests] data-section-id SSR emission on all 8 sections has zero server-side assertions
8. [warning, tests] Stage-1 self-heal clear untested; no aged-stamp (>10 min) negative test on either clear
9. [warning, tests] Send-failure → stamp-clear wiring runs in background against empty key, never asserted
10. [warning, tests] Advisory test gate: CONCERNS

--- SPEC / CONTEXT (read these if your lens needs intent — your primary lens is the code itself) ---
1. /Users/moses/code/_bmad-output/briefings/righttenantry-form-funnel-w0.md — the original job briefing.
2. _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md (at your cwd) — the frozen implementation spec.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r2/edge.json

Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: the file must contain ONLY the JSON array. No prose, no fencing, no preamble. Empty array `[]` is valid. Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames or assume.
- The `evidence` field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it.
- Hedging language ("might", "could", "possibly") means you have not verified — either verify and report crisply, or drop it.
- Prefer fewer, well-grounded findings over many speculative ones. Accuracy > volume.

After writing the file, reply with one line: count of findings written. Then stop.
