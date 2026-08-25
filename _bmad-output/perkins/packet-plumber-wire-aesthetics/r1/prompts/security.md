You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file.

--- PROJECT CONVENTIONS ---
Read the project conventions file at:
/Users/moses/.herdr/worktrees/packet-plumber/perkins-wire-aesthetics-r1/project-context.md

--- DIFF ---
Read the canonical diff FIRST and IN FULL at:
/Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1/diff.patch
(2147 lines, 13 files, PR #70 of solarity-services/Packet-Plumber, base branch `v2`, story 7.5 "wire aesthetics — routing + junction shaping, shipped as routing-only infrastructure"). These exact bytes are the review target — never re-fetch or regenerate. There are NO binary/golden files in this diff (the shipped render keeps both routing flags OFF, so T2 goldens are byte-identical — no re-bless).

--- WORKTREE (verify claims here) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-wire-aesthetics-r1
A checkout at exactly the reviewed sha 2aaaa255490f02f9507ef8aabf2ff6aa5cdbe499. Trust this checkout, not origin/v2. Every verification read happens here.

--- SPEC / CONTEXT ---
Read these spec files:
- /Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1/spec-briefing.md (original job briefing — hard requirements + acceptance list)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1/spec-story-card.md (story 7.5 card — Given/When/Then + status line + decision-log 2026-08-19)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1/spec-pr-body.md (PR body — what shipped + verification claims under audit)
- /Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1/spec-perkins-guards.md (round-1 review guards — the acceptance canon, read this FIRST)

--- ROUND GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- ONE hard blocker class — the cost-immunity spine: cost MUST stay on the LOGICAL geometry (pipe_span × cost_per_tile on the straight A→B segment); the detour/routing machinery is presentation-only and must never change gameplay, connect/anchor/cap semantics, or cost. The shipped pin suite (`wire_path_test.odin`, 6 tests) includes a negative-controlled cost-immunity pin and determinism pins. A regression here = real blocker.
- Gate verdict C (user ruling 2026-08-19, the lavish gate): "Ship pure straight (routing OFF, anchors OFF) — Story 7.5 becomes routing-only infrastructure." The diff ships the machinery OFF by default — the game render is byte-identical to the pre-7.5 straight look, and no re-bless was performed. Routing/anchors OFF by default is the DESIGN, not a defect — do NOT flag "feature not visible".
- What NOT to re-litigate: the 08-17 "want it" ruling (detours + junction shaping are wanted), the 08-19 gate verdict C, the shipped flags-off state, canon rulings already applied (7.1 light-canvas, D9 map, 5.12 estates).
- What to flag for verification: the canon fold (stories-v2.md §7.5 + decision-log 2026-08-19) matches the diff; the harness `wire-preview` gate tool + preview-check gate; T1/T2/replay pass with zero golden churn; the determinism claim (render twice → same hash) actually reproducible in-tree.
- CI note: GitHub Actions is billing-blocked today (runners never start) — NOT a signal. The local suite (`tools/ci-local.sh --mac`) is ground truth; the orchestrator re-ran it at the reviewed sha if needed for the report. Do not run the full suite inside a lens.

--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Context: this is a local offline game (Odin + raylib, software renderer) — no network surface, no user input beyond local keyboard/mouse. Assess security-relevant robustness of the new code: array bounds, unchecked integer arithmetic, division by zero, index safety on the new path tables, float-to-int truncation in geometry, any state mutation from the view layer (ODN-1 view purity is a security-adjacent invariant: the view must never write sim state).

--- OUTPUT ---
Write ONE valid JSON array to this exact path (and nowhere else):
/Users/moses/code/_bmad-output/perkins/packet-plumber-wire-aesthetics/r1/security.json
Each element must match this schema exactly:
{
  "source": "security",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

Output contract:
- The file must contain ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not fix anything. Do not run tests that mutate state.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is a fine and honest answer when nothing is wrong.
