#!/usr/bin/env python3
"""Generate the 14 lens prompt files (7 lenses x 2 chunks) for Perkins rc4-4 r2 (fix-audit round)."""
import pathlib

BASE = pathlib.Path("/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-4/r2")
WORKTREE = "/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc4-4-r2"
SPECS = [
    "original-job-briefing.md — the original job briefing (mission + requirements)",
    "epics-reference-checking-v1-2026-07-30.md — epic; story RC4.4 starts around line 692",
    "ux-reference-checking-v1-2026-07-29.md — UX spec; §7.6 attempt log, §7.9 notification copy, OQ-5 toast",
    "architecture-reference-checking-v1-2026-07-29.md — architecture (AR-RC13 one-stable-contract)",
    "perkins-briefing-r2.md — the ROUND-2 briefing; read 'CRITICAL lens-guards' and 'Round-2 mandate' sections first",
    "prior-findings-r1.json — round-1 consolidated findings (2 blockers, 8 warnings, 13 notes); the rework in this diff claims to fix them",
]
SPEC_LIST = "\n".join(
    f"{i}. {BASE}/spec/{name}" for i, name in enumerate(SPECS, start=1)
)

SCHEMA = '''{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}'''

ACCURACY = '''ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.'''

BLIND_ACCURACY = '''ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.'''

LENS_BRIEFS = {
    "edge": '''You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.''',
    "acceptance": '''Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).''',
    "security": '''OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps''',
    "architecture": '''Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?''',
    "codebase": '''Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?''',
    "tests": '''Test coverage analysis via traceability.

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
- FAIL: P0 <100%, or P1 <80%, or overall <80%''',
}

SOURCES = ["blind", "edge", "acceptance", "security", "architecture", "codebase", "tests"]
CHUNKS = {"c1": 1, "c2": 2}

ROUND2_HEADER = """--- ROUND-2 RE-REVIEW (this diff is a fix round) ---
You are reviewing round 2 of this PR. The diff below contains the ORIGINAL work PLUS a rework commit that claims to fix round-1 review findings (commit: 'fix(refcheck): RC4.4 r1 — post-correction cadence restart latches once; lifecycle-line survival, legacy terminal fallback, label/scan/pin gaps'). Round-1 findings are in the prior-findings file listed in the spec list above — read it.

Your output must contain ONLY:
1. NEW findings — defects introduced by the rework, or things r1 never raised that this diff still gets wrong.
2. RESIDUAL findings — where the commit claims a fix but the diff/codebase shows the fix is absent, wrong, or incomplete, so the underlying r1 defect persists or a NEW defect arises. Reference the r1 finding's title in your `detail` (e.g. 'residual of r1 B1: …').

Do NOT re-emit r1 findings that the diff genuinely fixes. Do NOT re-emit unchanged r1 findings the commit does not claim to fix (the orchestrator audits carries separately) — unless the fix attempt itself introduced a new problem. Do NOT re-litigate the r1 VERIFIED-CLEAN list: AR-RC13 server-built timeline, codec completeness 5/5, expand-only migration, §7.9 verbatim bodies, preference matrix, no-duplicate-terminals pin, back-compat decode.

Verify the commit's claims against the codebase by opening the cited files in the worktree — e.g. the cadence-restart latch (application_detail_handler.gleam build_send_entries) must reset ONLY the first post-correction batch and its test must pin ≥2 post-correction batches; the OQ-5 export toast arms must be pinned to verbatim copy; 3 of 5 terminal writers' terminalized_at stamps must have integration assertions.
"""

def shared_prompt(lens, source, chunk, diff_text):
    out = f"{BASE}/{lens}.{chunk}.json"
    return f"""You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read {WORKTREE}/AGENTS.md and treat it as the project conventions.

--- DIFF ---
This is chunk {CHUNKS[chunk]} of 2 (file-group split) of the PR diff. Review exactly these bytes:

{diff_text}

--- SPEC / CONTEXT ---
Read these spec files (all of them; in order of priority):
{SPEC_LIST}

The repository you may read for verification is at {WORKTREE} (READ-ONLY — do not modify anything).

--- YOUR LENS ---
{LENS_BRIEFS[lens]}

{ROUND2_HEADER}
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{SCHEMA}

Output contract:
- Write ONLY the JSON array (no prose, no markdown fencing, no preamble, no trailing text) to this exact file using your Write tool: {out}
- Overwrite the file if it already exists.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not continue reviewing, do not modify anything else, do not emit further output beyond a one-line confirmation of what you wrote.

{ACCURACY}"""

def blind_prompt(chunk, diff_text):
    out = f"{BASE}/blind.{chunk}.json"
    return f"""You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

ROUND-2 NOTE: the diff includes a rework commit claiming to fix prior review findings: 'fix(refcheck): RC4.4 r1 — post-correction cadence restart latches once; lifecycle-line survival, legacy terminal fallback, label/scan/pin gaps'. Treat these claims as unproven — look for bugs in the new hunks, claims the hunks don't deliver, contradictions, and missed spots.

CRITICAL ISOLATION RULE: your blindness is prompt-level — your tools COULD read repository files or spec documents, but doing so invalidates your lens and your findings will be discarded. Do NOT read any repository file, spec file, or document other than the diff below.

--- DIFF ---
{diff_text}

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{SCHEMA}

Output contract:
- Write ONLY the JSON array (no prose, no markdown fencing, no preamble, no trailing text) to this exact file using your Write tool: {out}
- Overwrite the file if it already exists.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Do not continue reviewing, do not modify anything else, do not emit further output beyond a one-line confirmation of what you wrote.

{BLIND_ACCURACY}"""

# Read chunks
c1 = (BASE / "chunks/diff.c1.patch").read_text()
c2 = (BASE / "chunks/diff.c2.patch").read_text()
diffs = {"c1": c1, "c2": c2}

out_dir = BASE / "prompts"
out_dir.mkdir(exist_ok=True)

for chunk, diff_text in diffs.items():
    for lens, source in zip(SOURCES, SOURCES):
        if lens == "blind":
            content = blind_prompt(chunk, diff_text)
        else:
            content = shared_prompt(lens, source, chunk, diff_text)
        path = out_dir / f"{lens}.{chunk}.prompt.md"
        path.write_text(content)
        print(f"wrote {path.name} ({len(content)} chars)")
