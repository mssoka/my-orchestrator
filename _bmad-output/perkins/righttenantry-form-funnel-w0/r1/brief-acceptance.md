You are reviewing a code diff. You have read-only access to the repository at your cwd (/Users/moses/.herdr/worktrees/RightTenantry/perkins-form-funnel-w0-r1) and may verify the diff's claims against the actual codebase using your tools. Do NOT modify any repo file.

--- PROJECT CONVENTIONS ---
Read AGENTS.md and CLAUDE.md at the repo root if present.

--- DIFF ---
The complete diff is at: /Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/diff.patch
Read it in full, in chunks (read tool with offset/limit) until you have seen every line.

--- SPEC / CONTEXT (your acceptance source — read ALL of these IN FULL before judging) ---
1. /Users/moses/code/_bmad-output/briefings/righttenantry-form-funnel-w0.md — the original job briefing (mission, W0 instrumentation pack, W1a copy pack, acceptance criteria).
2. _bmad-output/planning-artifacts/problem-solving-application-form-completion-2026-07-31.md (at your cwd) — the merged problem-solving report; the W0 instrumentation pack + W1a copy pack requirements derive from it (see Solution Evaluation / Implementation Plan / Monitoring sections).
3. _bmad-output/implementation-artifacts/spec-form-funnel-w0-w1a.md (at your cwd) — the frozen implementation spec the minion wrote; note it is THEIR spec, the briefing + report outrank it.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria (e.g. the briefing's "Acceptance" section: all W0 events firing + tested; copy pack live; "few minutes"/"10 minutes" lie gone everywhere — check `rg -i "few minutes|10 minutes"` yourself; tests present; consent gate honored; no PII in events; confirmation event must NOT fire on validation-error re-render or spam fake-confirmation; follow-ups B/C must NOT be built here).
- Deviations from spec intent.
- Missing implementation of specified behavior (e.g. section entered/completed/abandoned events with stable section ids; stable anon id surviving reloads and consent-gated; Resend open/click tracking work; two-stage doc-gathering reminder series).
- Contradictions between spec constraints and actual code.
- Scope drift — changes not asked for by the spec.

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

--- OUTPUT ---
Write ONE valid JSON array to this EXACT absolute path (use the write tool — do not derive any other path):
/Users/moses/code/_bmad-output/perkins/righttenantry-form-funnel-w0/r1/acceptance.json

Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words — quote the spec phrase violated>",
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
