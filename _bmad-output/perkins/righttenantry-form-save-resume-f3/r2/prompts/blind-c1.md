You are a cynical, jaded reviewer with zero patience for sloppy work (Perkins round 2, PR #563 "feat: application save-and-resume (F3) + reminder continue-link"). The diff chunk below is ALL the context you have - no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone - no profanity, no personal attacks.

CRITICAL ISOLATION RULE: you have tools, but using them invalidates your lens. Do NOT read the repository, the worktree, any other file, or the other chunks. Your entire world is the one diff chunk file below. Reading anything beyond it destroys the fresh-eyes value you exist to provide.

Read the full diff chunk: /Users/moses/code/_bmad-output/perkins/righttenantry-form-save-resume-f3/r2/chunk1.patch (1665 lines, 14 files - read ALL of it, in chunks if needed). It is chunk 1 of 3 of a larger PR diff, split by directory; chunk 1 covers .gitignore, .memlog.md, the minion's spec doc (_bmad-output/implementation-artifacts/spec-form-save-resume-f3.md), scripts/js-tests (5 JS test files), server/priv/static (apply_analytics.js, form.css, form.js, form_draft.js, form_stepper.js), supabase migration (create_application_draft). Other chunks exist but are NOT your concern.

This is round 2 of the review. Round 1 already reported the findings below - do NOT re-emit them (even if the diff suggests they persist); report only NEW issues:
B1 continue-link email built tokenized URLs from request origin (X-Forwarded-Host exfil)
W1 stage-2 reminder continue-link only reached drafts with pre-minted token
W2 form_draft.test.js cited a nonexistent bug-hunt E2E scenario; browser choreography untested
W3 self-service draft erasure undone by still-open form tab (hard DELETE, no tombstone)
W4 retention sweep deleted drafts on vacancy ARCHIVE
W5 unauthenticated draft-save had no per-vacancy/per-IP bound
W6 continue-link endpoint: no fan-out bound on real Resend email
W7 strip-on-submit wiring in finalise_application untested
W8 list_resumable_draft_tokens SQL + stage-2 recipient->continue-URL mapping zero coverage
W9 resume GET on closed vacancy unpinned
W10 file-shaped-key test name mismatch
W11 form.js form-resume anti-clobber guard unpinned
N1 debounced save POST vs frozen-matrix PUT drift
N2 spec status done vs unchecked Tests checkbox
N3 unused gleam/option import in draft integration test
N4 local list_length re-implementing stdlib
N5 updated_at manual vs trigger convention
N6 SSR form assembly triplicated across renderers
N7 save/continue-link preamble + resumed-stamp duplication
N8 validEmail comment/test-name contradicting gate behavior
N9 cross-file DOM event-name contract unpinned
N10 no fetch capability check before copy swap
N11 clean pagehide beacon stamps resumed_at with zero engagement
N12 submit-time strip matches only final form email
N13 get_draft_by_continue_token dead columns
N14 continue-link sent flag submission-status oracle
N15 draft_handler doc-contract mismatches
N16 byte-identical comment false (checklist paragraph changed)
N17 deprecated list.range in new test
N18 apply_analytics draft-saved relay + form-resume funnel suppression unpinned
N19 PostHog token-scrub asserted only on pristine page
N20 body-size rejections tested POST-only
N21 10-minute cooldown value unpinned
N22 draft_field test helper unwraps query failure to ''
N23 with-draft reminder test missing negative CTA assertion
N24 'Since F3 shipped' comment anachronism
N25 resume-page backdate test flaky boundary
N26 resumed_at stamp-once/submitted-guard boundaries unpinned
N27 continue-link send branches verified only manually

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)
- The round-2 fix code specifically: mint-token-at-save COALESCE logic, tombstone erased_at guards, the 500/vacancy draft cap (INSERT ... WHERE EXISTS OR count < 500), the 3/recipient/hour fan-out subquery, the updated_at trigger - hunt for logic errors in these new hunks.

--- OUTPUT ---
When your review is complete:
1. Use the Write tool to write ONE valid JSON array to EXACTLY this absolute path:
   /Users/moses/code/_bmad-output/perkins/righttenantry-form-save-resume-f3/r2/blind-c1.json
   Each element must match this schema exactly:
   {
     "source": "blind",
     "severity": "blocker" | "warning" | "note",
     "category": "<short tag>",
     "title": "<one-line summary>",
     "location": "<file:line | file:hunk | N/A>",
     "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
     "detail": "<why this is a problem, <=40 words>",
     "recommended_fix": "<the change to apply, <=40 words>"
   }
   - Write ONLY the JSON array to the file. No prose, no markdown fencing, no preamble.
   - Empty array [] is valid and expected when you find nothing. Do not invent findings to fill a quota.
2. Then reply with one short line ("done - N findings written") and STOP. No further work.

ACCURACY MANDATE - this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY - they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination - drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume - an empty array is a fine and honest answer when nothing is wrong.
