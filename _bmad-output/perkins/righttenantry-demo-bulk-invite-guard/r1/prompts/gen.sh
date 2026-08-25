#!/bin/bash
set -euo pipefail
R1=/Users/moses/code/_bmad-output/perkins/righttenantry-demo-bulk-invite-guard/r1
WT=/Users/moses/.herdr/worktrees/RightTenantry/perkins-righttenantry-demo-bulk-invite-guard-r1

shared_head() {
cat <<'EOF'
You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT edit any repository file — your only write is the JSON output file named below.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/RightTenantry/perkins-righttenantry-demo-bulk-invite-guard-r1/AGENTS.md IN FULL before judging anything. Those are the project conventions (Gleam/Lustre monorepo: client/ SPA, server/ Wisp API, shared/ types; copy.gleam owns all landlord-facing strings; no JS FFI; explicit error handling).

--- DIFF (the canonical bytes under review — review exactly these) ---
EOF
}

spec_section() {
cat <<'EOF'

--- SPEC / CONTEXT (the job briefing — your spec) ---
EOF
cat "$R1/job-briefing.md"
cat <<'EOF'

The PR under review: https://github.com/solarity-services/RightTenantry/pull/636 — its body is fetchable via `gh pr view 636 --json title,body` (repo solarity-services/RightTenantry). Spec rule 3 requires the real-mode validation-error gap to be FLAGGED in the PR (not fixed) — the PR body is part of the compliance surface.

--- YOUR LENS ---
EOF
}

output_contract() {
local lens="$1"
cat <<EOF

--- OUTPUT ---
Write ONE valid JSON array to this EXACT path: $R1/$lens.json
Write ONLY the JSON array to that file (no prose, no markdown fencing, no preamble). Then stop.

Each element must match this schema exactly:
{
  "source": "$lens",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
EOF
}

# ---- blind (isolated: diff only) ----
{
cat <<'EOF'
You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

BLINDNESS RULE: reading anything beyond the diff below INVALIDATES your lens. Do NOT open repository files, do NOT read AGENTS.md, do NOT run git/gh commands to fetch more context. The diff is the whole world.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
EOF
cat "$R1/diff.patch"
cat <<EOF

--- OUTPUT ---
Write ONE valid JSON array to this EXACT path: $R1/blind.json
Write ONLY the JSON array to that file (no prose, no fencing, no preamble). Then stop.

Each element must match this schema exactly:
{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use 'N/A' only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>"
}

Empty array [] is valid. Do not invent findings to fill a quota.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose evidence cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in evidence. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
EOF
} > "$R1/prompts/blind.md"

# ---- edge ----
{
shared_head
cat "$R1/diff.patch"
spec_section
cat <<'EOF'
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.
EOF
output_contract edge
} > "$R1/prompts/edge.md"

# ---- acceptance ----
{
shared_head
cat "$R1/diff.patch"
spec_section
cat <<'EOF'
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).
EOF
output_contract acceptance
} > "$R1/prompts/acceptance.md"

# ---- security ----
{
shared_head
cat "$R1/diff.patch"
spec_section
cat <<'EOF'
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps
EOF
output_contract security
} > "$R1/prompts/security.md"

# ---- architecture ----
{
shared_head
cat "$R1/diff.patch"
spec_section
cat <<'EOF'
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?
EOF
output_contract architecture
} > "$R1/prompts/architecture.md"

# ---- codebase ----
{
shared_head
cat "$R1/diff.patch"
spec_section
cat <<'EOF'
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?
EOF
output_contract codebase
} > "$R1/prompts/codebase.md"

# ---- tests ----
{
shared_head
cat "$R1/diff.patch"
spec_section
cat <<'EOF'
Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics to check:
- New/modified API endpoints without matching coverage
- Auth/authz paths missing negative tests
- Happy-path-only coverage where error handling is implied
- New DB operations without integration coverage
- New state transitions without boundary tests

Test level mix (unit/integration/E2E): flag mismatches as findings.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS → note, CONCERNS → warning, FAIL → blocker
- detail: rationale with coverage percentages
- recommended_fix: what would raise the gate

Gate thresholds:
- PASS: P0 100%, P1 ≥90%, overall ≥80%
- CONCERNS: P0 100%, P1 80–89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%
EOF
output_contract tests
} > "$R1/prompts/tests.md"

echo "generated:"; ls -la "$R1/prompts/"
