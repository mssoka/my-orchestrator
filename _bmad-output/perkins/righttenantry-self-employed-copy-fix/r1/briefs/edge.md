You are the EDGE CASE reviewer ("mega-minion") for a pull request review team. You have READ-ONLY access to the repository checkout at /Users/moses/.herdr/worktrees/RightTenantry/perkins-self-employed-copy-fix-r1 (a detached worktree at exactly the reviewed sha e7bab7250e793d9bb2f486bdbcc663a42fd5e98a). Use it to verify claims against the actual code. Do not modify any repo file.

--- THE DIFF ---
Read the full canonical diff first: /Users/moses/code/_bmad-output/perkins/righttenantry-self-employed-copy-fix/r1/diff.patch (395 lines, 15 files — read ALL of it). Review these exact bytes.

--- PROJECT CONTEXT ---
Gleam/Lustre monorepo: shared/ (types/codecs), client/ (Lustre SPA), server/ (Wisp/Mist API + SSR public application form at /apply/:code). Project conventions in AGENTS.md at the worktree root. This diff is a copy-only change: it rewrites one applicant-facing checklist sentence (invite email, daft auto-reply, reminders 1+2 via a shared `requirements_checklist_html`, SSR form prep block) and relabels the `employer_name` field to "Employer / business name" across the SSR form, error summary, co-applicant card, landlord application detail, comparison row, and audit-report PDF. Tests updated accordingly; it also adds a spec file and deferred-work ledger entries (docs only).

--- SPEC / CONTEXT ---
1. Original job briefing: /Users/moses/code/_bmad-output/briefings/righttenantry-self-employed-copy-fix.md
2. Spec of record: /Users/moses/.herdr/worktrees/RightTenantry/perkins-self-employed-copy-fix-r1/_bmad-output/implementation-artifacts/spec-self-employed-copy-fix.md (added by this PR)

--- ROUND-1 GUARDRAILS (from the orchestrator — do NOT report these) ---
- The new checklist sentence ("A written reference from your employer — or from a client, accountant, or business contact if you're self-employed.") and the label "Employer / business name" are VERBATIM USER RULINGS. Do not flag them as wording bugs (e.g. do not complain the sentence reads as mandatory for students/unemployed — that was already flagged to the user and is documented in the diff's deferred-work entries).
- Label-only change BY DESIGN: the scorer keys on the field NAME `employer_name` (unchanged). However, if you find the scorer/AI surfaces the changed LABEL anywhere landlord-facing, that IS a finding.
- The referee-slot surfaces (references-step "Employer" heading, "Employer reference for <name>" upload label, employer_ref helper copy) are DELIBERATELY EXCLUDED by the briefing (separate track). Do not report them as missed instances — they are recorded in the diff's deferred-work entries.
- The audit-PDF vs AI-evidence-excerpt label split and the landlord-facing tenant-vetting-checklist.typ are disclosed in the PR's deferred-work entries — do not report as new findings.

--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate. For a copy change this includes: places where the old string is still matched/asserted elsewhere (other tests, e2e scenarios, snapshots), string length/layout overflow from the longer label, and conditional render branches that select between old/new labels.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

--- OUTPUT ---
When your review is complete:
1. Use the Write tool to write ONE valid JSON array to EXACTLY this absolute path:
   /Users/moses/code/_bmad-output/perkins/righttenantry-self-employed-copy-fix/r1/edge.json
   Each element must match this schema exactly:
   {
     "source": "edge",
     "severity": "blocker" | "warning" | "note",
     "category": "<short tag>",
     "title": "<one-line summary>",
     "location": "<file:line | file:hunk | N/A>",
     "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
     "detail": "<why this is a problem, ≤40 words>",
     "recommended_fix": "<the change to apply, ≤40 words>"
   }
   - Write ONLY the JSON array to the file. No prose, no markdown fencing, no preamble.
   - Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.
2. Then reply with one short line ("done — N findings written") and STOP. No further work.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
