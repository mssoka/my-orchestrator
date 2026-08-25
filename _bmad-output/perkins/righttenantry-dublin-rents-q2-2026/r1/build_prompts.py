#!/usr/bin/env python3
"""Build the 7 verbatim lens prompts for Perkins round r1 (righttenantry-dublin-rents-q2-2026)."""
import json, pathlib

R1 = pathlib.Path("/Users/moses/code/_bmad-output/perkins/righttenantry-dublin-rents-q2-2026/r1")
DIFF = (R1 / "diff.patch").read_text()
BRIEFING = (R1 / "job-briefing.md").read_text()
issue = json.loads((R1 / "issue-529.json").read_text())
ISSUE = f"# GitHub issue #529 (the spec's source of truth)\n\n**Title:** {issue['title']}\n\n{issue['body']}"

CONVENTIONS = """You are running as pi inside the repo worktree — the repo root AGENTS.md is auto-loaded as project context; read it for full conventions. Digest of the conventions most relevant to reviewing this diff:

- Gleam/Lustre monorepo: shared/ (types+codecs), client/ (Lustre SPA), server/ (Wisp/Mist JSON API + SSR content pages). This diff touches server/ only (content registry + committed static assets + a unit test).
- Content posts are Gleam consts in server/src/content/ — data displayed in the UI comes from these (they ARE the database for static content). All landlord-facing copy follows a calm, specific brand voice; no raw error strings in user-facing text.
- Rent-data posts follow a strict three-figure discipline: asking rents (Daft) vs new-tenancy registered rents (RTB/ESRI) vs existing-tenancy registered rents (RTB/ESRI) — never conflated. Every € figure in a rent post carries a `VERIFY before prod` comment and must match the live published reports named in the sources block.
- Rent Pressure Zone cap/CPI figures derive from server/src/content/rpz.gleam consts (shared across every rent/cap page) — content posts must not hardcode their own cap percentages out of sync with rpz.
- No `let assert` in production code (tests are exempt). Squirrel for all SQL. data-testid on interactive UI. Content pages are SSR, not SPA.
"""

LENS_BRIEFS = {
    "edge": """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.""",

    "acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

The spec's acceptance criteria (verify each against the actual code in your worktree, not just the diff):
1. `/resources/dublin-rents-q2-2026` renders, 404s nothing, appears in sitemap.xml + `/resources` hub newest-first
2. All € figures verified against the live reports named in the sources block (Daft Q2 2026 asking rents; RTB/ESRI latest index; three-figure discipline: asking vs new-registered vs existing-registered, never conflated; headline figure table carries its VERIFY-before-prod comment like Q1)
3. No hardcoded cap percentage in copy (derives from rpz) — check the post title/body for hardcoded cap percentages and check what rpz.gleam's consts actually say
4. Also-in-scope per the spec: cpi const freshness (CSO June 2026 CPI = 3.4%, published 9 Jul 2026 — the spec said bump rpz's cpi const fields in this PR if stale; check the CURRENT state of rpz.gleam in your worktree and whether this PR handled or needed that)""",

    "security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps""",

    "architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?""",

    "codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specific reality checks for this diff: the new RentPost const's fields against the RentPost type; the OG-card pin added to server/test/content/content_test.gleam against how that test iterates pairs; the committed og-dublin-rents-q2-2026.png/svg against how sibling posts' OG cards are stored and referenced (compare dublin-rents-q1-2026).""",

    "tests": """Test coverage analysis via traceability.

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
- FAIL: P0 <100%, or P1 <80%, or overall <80%""",
}

SCHEMA = """Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "{SOURCE}",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong."""

FILE_CONTRACT = """
--- FILE OUTPUT (headless mode — mandatory) ---
Do NOT print the JSON array as your reply. Instead, write ONLY your JSON array (nothing else — no prose, no fencing) to exactly this absolute path using your Write tool:

{path}

Then reply with a single short line confirming the file was written. The path is given verbatim — do not derive, transform, or relocate it. After writing the file, stop."""

BLIND_PROMPT = f"""You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

ISOLATION (this is the Blind Hunter lens): reading anything beyond the diff above — repository files, directories, git history, the web — INVALIDATES your lens. The diff is your entire context. Do not use any tool except to write your output file.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

--- DIFF ---
{DIFF}

--- OUTPUT ---
{SCHEMA.replace("{SOURCE}", "blind")}
{FILE_CONTRACT.format(path=str(R1 / "blind.json"))}"""

def shared(source, lens_brief):
    return f"""You are reviewing a code diff. You have read-only access to the repository (your cwd is the worktree at exactly the reviewed state) and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository; your only permitted write is your output file named below.

--- PROJECT CONVENTIONS ---
{CONVENTIONS}

--- DIFF ---
{DIFF}

--- SPEC / CONTEXT ---
# Original job briefing (dispatch spec)

{BRIEFING}

{ISSUE}

--- YOUR LENS ---
{lens_brief}

--- OUTPUT ---
{SCHEMA.replace("{SOURCE}", source)}
{FILE_CONTRACT.format(path=str(R1 / f"{source}.json"))}"""

prompts = {"blind": BLIND_PROMPT}
for src, brief in LENS_BRIEFS.items():
    prompts[src] = shared(src, brief)

outdir = R1 / "prompts"
outdir.mkdir(exist_ok=True)
for name, text in prompts.items():
    (outdir / f"{name}.txt").write_text(text)
    print(f"{name}: {len(text)} chars")
