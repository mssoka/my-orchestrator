You are the SECURITY reviewer ("mega-minion") for a pull request review team (Perkins round 3 — FINAL, job righttenantry-form-save-resume-f3, PR #563, "feat: application save-and-resume (F3) + reminder continue-link"). You have READ-ONLY access to the repository checkout at /Users/moses/.herdr/worktrees/RightTenantry/perkins-form-save-resume-f3-r3 (a detached worktree at exactly the reviewed sha 8789054f998c64db804dc36c8fdfeca88b134249). Use it to verify claims against the actual code. Do not modify any repo file.

--- THE DIFF (your chunk) ---
Read the full diff chunk first: /Users/moses/code/_bmad-output/perkins/righttenantry-form-save-resume-f3/r3/chunk2.patch (2274 lines, 23 files - read ALL of it, in chunks if needed). Review these exact bytes. The full PR diff (5416 lines, 46 files) exceeded the big-diff threshold and was split into 3 chunks by directory; you are reviewing chunk 2 of 3, which covers server/src/ — application handler/draft_handler/draft_view/form_copy/form_pages/form_view, generated + hand SQL (draft + retention), csrf, middleware, router, inbound email handler, notification email client, retention job. Files outside your chunk exist in the worktree - read them freely for context, but anchor findings in your chunk where possible.

--- PROJECT CONVENTIONS ---
Read AGENTS.md at the worktree root - its rules are binding review criteria (Gleam/Lustre monorepo; Squirrel-generated SQL only; no JavaScript FFI; no `let assert` outside tests; explicit HTTP timeouts on outbound calls; brand-voice copy in form_copy.gleam/copy.gleam; expand-only migrations; audit-on-state-change and /apply consent capture are defended invariants).

--- ROUND-3 CONTEXT (established — do NOT report these as findings) ---
This is ROUND 3 (FINAL). Round 1 (sha d99a6737) produced 39 findings; round 2 (sha 11fcaa3f) produced 37 more + carried 11 round-1 notes. The orchestrator owns the fix audit. DO NOT re-report any prior finding — the full list is below. Hunt ONLY for NEW issues: defects in the round-3 fix hunks (wrapped host timers in form_draft.js, the sent-flag removal in draft_handler.gleam, spec text edits) and anything rounds 1-2 missed.
ROUND-2 FINDINGS (do not re-emit, even if still broken):
B1 detached window.setTimeout/clearTimeout breaks debounced save (Illegal invocation) — FIXED this round: the WRAPPED timer code you will see in form_draft.js IS the fix; hunt for defects in the fix, don't re-report the original bug
W1 fresh-session blank form wholesale-replaces a rich prior draft with empty strings
W2 fan-out bound counts stamped rows not sends (~4-6x overshoot of "max 3/recipient/hour")
W3 500/vacancy draft cap counts stripped (submitted) + tombstoned (erased) rows
W4 cap-blocked draft INSERT silently answers ok:true
W5 fan-out 3/hour bound is check-then-act (concurrent claims all pass)
W6 plus/dot email aliases defeat the per-recipient bound
W7 resume start-step wiring (form-resume -> firstIncompleteIndex) pinned only at pure-function level
W8 claim_continue_link_send submitted/erased zero-row guards unpinned by tests
W9 form_draft.js script-tag inclusion unpinned on pristine + error re-render pages
W10 round-1 B1 origin-via-origin_domain fix has no automated test pin
N1 DOMContentLoaded bootstrap passes Event as env (latent under defer)
N2 migration header still claims lazy token minting + row-removal erasure
N3 spec Suggested Review Order still says expiry sweep covers archived vacancies
N4 vacancy closed mid-session: saver disabled but UI still promises saves + misreports deterministic continue failure as transient
N5 client-plausible but server-invalid email: saves 400 silently forever; continue misreports as transient
N6 500-cap races concurrent inserts of distinct pairs (approximate bound)
N7 resumed_at stamped for empty-fields continue-link payload but not identical save payload
N8 dead COALESCEs in claim RETURNING + list_resumable SELECT
N9 DuplicateApplication branch never strips a coexisting live draft
N10 draft upload-slot filter re-encodes document_upload's slot-name whitelist
N11 vacancy+draft lookup preamble triplicated across SSR draft handlers
N12 five draft copy constants in form_copy.gleam are unreferenced orphans
N13 W9 closed-vacancy resume test asserts only absence of resume markers (never closed-vacancy-notice)
N14 W3 tombstone retains erased applicant's plaintext email as suppression key (deliberate, documented)
N15 Transfer-Encoding body-size rejection tested POST-only
N16 erasure GET confirm on never-valid token unpinned
N17 seed_draft_with_token redundant UPDATE after minting upsert
N18 list_resumable_draft_tokens lacks erased_at guard
N19 new token endpoints lack the Cloudflare per-IP rule /erase//dsar/ have
N20 four new public draft routes have no router-level pin
N21 vacancy_short_code helper duplicated x3 in integration tests
N22 form_view_now_ms / near_future_date alias-wrapper style drift
N23 fan-out bound's 1-hour window value unpinned
N24 empty-fields no-wipe guard unpinned on the continue-link path
N25 failed-save dirty-retry path in form_draft.js has no wiring test
N26 application_draft updated_at trigger has no test asserting it fires
CARRIED ROUND-1 NOTES still present (do not re-emit):
r1-N6 SSR form assembly triplicated across renderers (deferred refactor)
r1-N7 save/continue-link decode-validate-lookup preamble + resumed-stamp duplication (deferred)
r1-N8 form_draft.test.js test name 'rejects the near-misses that must not gate a save' contradicts gating
r1-N11 clean pagehide beacon sends resume_token -> stamps resumed_at with zero engagement
r1-N12 strip matches only the final form email; residual earlier-email draft undocumented
r1-N15 lookup_accepting_vacancy doc claims 'Lookup outcomes are JSON' but DB/uuid arms return text/plain 500
r1-N18 apply_analytics draft-saved relay listener + form-resume funnel early-return wiring-unpinned
r1-N22 draft_field test helper unwraps query failure to '' (empty-string assertions pass on missing row)
r1-N27 no forced-DB-error test of the continue-link upsert-abort branch
FIXED THIS ROUND (verified by orchestrator — do not re-report): r2-B1 (timer wrap, empirically verified in Chromium), r1-N14 (sent flag dropped — uniform ok:true; the no-oracle response code you see IS the fix), r1-N1 (spec corrected to POST / PUT|POST).
- Drafts carry FIELD VALUES ONLY by design — "no documents in drafts" is spec requirement 4, not a gap.
- The migration having been applied only to a local Docker test DB is per project policy — not a finding.
- The stepper seam (the rt:form-step-changed custom event) is the sanctioned save trigger documented by the merged F1 stepper PR — not an undocumented coupling.
- Deferred refactors (r1-N6/N7) and consciously-accepted trade-offs documented in the spec change log are NOT new findings.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

--- OUTPUT ---
When your review is complete:
1. Use the Write tool to write ONE valid JSON array to EXACTLY this absolute path:
   /Users/moses/code/_bmad-output/perkins/righttenantry-form-save-resume-f3/r3/security-c2.json
   Each element must match this schema exactly:
   {
     "source": "security",
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
