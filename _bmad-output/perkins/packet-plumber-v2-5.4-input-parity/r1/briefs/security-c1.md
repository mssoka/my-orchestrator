You are reviewing a code diff as ONE specialist lens in a multi-lens headless review. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. NEVER edit any repository file.

Read these inputs first, exactly:
- DIFF (canonical — review exactly these bytes; never re-fetch or regenerate the diff): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.4-input-parity/r1/chunk1.patch
- WORKTREE (checkout at exactly the reviewed sha — every verification read happens here): /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.4-input-parity-r1
- PROJECT CONVENTIONS: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.4-input-parity-r1/project-context.md
- SPEC / CONTEXT (read both):
  - /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-5.4-input-parity.md (original job briefing — the spec)
  - /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.4-input-parity/r1/spec-story-5.4.md (story card)

--- ROUND-SPECIFIC LENS GUARDS (from the chief reviewer — obey strictly) ---
**The ONE hard blocker — mouse mapping preserves current behavior EXACTLY.** The intent layer is parity-BY-CONSTRUCTION [FORGE #6]/[ODN-12]: raw device event -> typed Intent -> validated Command. Any behavioral delta in the mouse path (click targets, drag, hover, wheel) vs the pre-change behavior is a blocker. A scripted device-event T1 golden must cover across-inputs parity.

**Verify specifically:**
- Every raw input path (touch, mouse, controller) now funnels through the intent layer — no bypass path left on the old direct handlers.
- Validation exists at the Command stage; invalid/out-of-contract intents are rejected, not silently dropped or coerced.
- NO LOG_VERSION bump and NO serialization change (inputs are never serialized — replay [E10] unaffected).
- Landscape = camera-fit flag-only ([§18 OQ-1]) — no gameplay change smuggled into the parity refactor.

**What NOT to re-litigate (do NOT file findings on these):** the FORGE #6 / ODN-12 architecture rulings (the intent layer IS the sanctioned design); the merged 5.2/5.8 serialization discipline; the post-rebase adoption hunks (the Cmd_Set_Emphasis -> Cmd_Set_Weights rename across the intent layer + the input_parity manifest catalog_hash re-bless with values unchanged — the terminology canon, already merged to base via #55); the deliberate two-finger-pan no-op (Pan intent mapped but the camera-fit view has no pan state — a flagged, deliberate deferral per [§18 OQ-1]; camera work is a later story).

**Flag for verification:** T1 goldens across-inputs (scripted device events) — confirm they're real parity pins, not just re-blessed.

**Severity calibration:** this is a gameplay prototype slice. Prototype-rigor concerns (missing mobile UI polish, no physical-device testing, deferred camera work) are NOT blockers. Reserve "blocker" for genuine correctness/parity/determinism defects.

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
When your analysis is complete, write your final answer as ONE valid JSON array to this EXACT absolute path using the Write tool:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.4-input-parity/r1/security.c1.json
The file must contain ONLY the JSON array — no prose, no markdown fencing, no preamble. Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The JSON file is your ONLY deliverable. Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not do anything else.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.