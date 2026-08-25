#!/usr/bin/env python3
import os

OUT = "/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r3"
WT = "/Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r3"

SHARED = f"""You are reviewing a code diff in the RightTenantry repo. You have read-only access to the repository worktree and may verify the diff's claims against the actual codebase using your tools. Do NOT modify, build, or write any repo file. The ONLY file you may write is your output JSON at the path given below.

--- PROJECT CONVENTIONS ---
Read {WT}/AGENTS.md for project conventions.

--- DIFF ---
The canonical diff is at {OUT}/diff.patch - read it fully with the read tool. Review exactly these bytes; do not re-generate or re-fetch the diff.

--- WORKTREE (verification) ---
{WT} is a checkout at exactly the reviewed state (sha 0f94e043a50851ecbd9bb82d1ec752f75823338f). Every verification read happens here. Your cwd is already this worktree.

--- SPEC / CONTEXT ---
Read both:
- /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md (original job spec: 5 mobile UX fixes + acceptance criteria)
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-mobile-layout-1-r3.md (round-3 reviewer briefing; the "Lens-guards" section names what each round-2 blocker fix must satisfy)

--- PRIOR ROUND (this is a FIX-AUDIT round, round 3) ---
The round-2 consolidated findings are at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r2/consolidated.json. Round 2 ended NEEDS CHANGES with 2 blockers (B1: demo click arm bypasses notification_target_path - vacancy-typed demo clicks no-op; B2: late ApiReturnedLeaderboard response re-fabricates a wrong vacancy id), 2 warnings (vacancy_detail pb-28 untested; filter-pill shrink-0 untested), 6 notes. This diff is the fix for those.
Do NOT re-report r2 findings as new. If an r2 finding's fix is MISSING or insufficient, report it as a finding titled "<original title> (still present since round 2)" with severity at least as high as round 2.
Do NOT re-litigate: the r2 blocker fixes themselves (audit that they LANDED and BITE), the client-side resolution choice (user-approved), or the 5-fix list.

--- ROUND-3 HARD BLOCKER CLASS (carried) ---
The notification deep-link contract: BOTH entity types (vacancy AND application) navigate + mark read; no fabricated vacancy ids (real AI-failure notifications carry only the application id); vacancy behavior unchanged.

--- ROUND-3 LENS-GUARDS (from the r3 briefing - verify each BITES) ---
- B1 (r2) fix: the helper (with resolve_application_vacancy) must be moved into a NEUTRAL module both arms import; the demo arm must CALL it; BOTH arms must be pinned by tests. Verify vacancy-typed demo clicks now NAVIGATE (the r1/r2 miss was demo clicks no-op'ing) and the real arm still routes through the same helper (no contract drift).
- B2 (r2) fix: the plain leaderboard response message ApiReturnedLeaderboard (and the page variant) must carry the vacancy id and apply only on match (like the refresh handler's vacancy_detail_request_id). Verify the exact r2 repro: VacancyDetail(A) fetch in flight -> navigate to B -> A's response lands -> A's rows must NOT tag as B, and the resolver must not fabricate.
- Also check: the neutral-module move didn't break the real arm; the demo arm's pins are real (revert-style: a wrong path must fail a test); no regression on the demo r1-r5 gauntlet classes; r2 warnings (vacancy_detail pb-28 test, filter-pill shrink-0 test) and notes status.
"""

BLIND = f"""You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have - no project files, no spec, no codebase access. Reading anything beyond the diff INVALIDATES your lens; do not open any other file except this prompt file. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone - no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose

--- DIFF ---
The diff is at {OUT}/diff.patch - read it fully with the read tool. It is your ONLY input.

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: {OUT}/blind.json
Each element:
{{
  "source": "blind",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff. Use 'N/A' only when the claim is about something genuinely absent from the diff. Paraphrased or reconstructed evidence is hallucination - drop the finding instead.>",
  "detail": "<=40 words>",
  "recommended_fix": "<=40 words>"
}}

Output contract: the file contains ONLY the JSON array. No prose, no fencing. [] is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose evidence cannot be located in the diff, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in evidence. Speculation without quoted evidence is dropped. Accuracy > volume - an empty array is an honest answer when nothing is wrong.

When done, reply with one line: "DONE blind <n> findings".
"""

SCHEMA = """Each element must match this schema exactly:
{{
  "source": ""{src}"",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}}

Output contract: the file contains ONLY the JSON array. No prose, no fencing, no preamble. [] is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE - the most important instruction in this prompt: NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY. Open the file. Read the relevant lines. The evidence field must contain the EXACT lines you read. Hedging language ("might", "could", "possibly") is a signal you have not verified - either verify and report crisply, or do not report. Prefer fewer, well-grounded findings over many speculative ones.

When done, reply with one line: "DONE {src} <n> findings".
"""

LENSES = {
    "edge": """You are a pure path tracer. Do not comment on whether the code is good or bad - list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself. Examples: boundary conditions (empty lists, nulls, None options, zero counts), concurrent operations and race conditions, unhandled error paths, off-by-one errors, state the new code doesn't account for, input the new code doesn't validate.

Round-3 specifics you MUST trace in the actual worktree code:
- The r2 repro (B2 fix): VacancyDetail(A) fetch in flight -> navigate to VacancyDetail(B) -> A's ApiReturnedLeaderboard response lands. Verify the message now carries the vacancy id and applies ONLY on match. Trace EVERY site that constructs ApiReturnedLeaderboard and its page variant - a missed construction site or a match guard that falls through incorrectly is a finding. What happens on id mismatch: is the response dropped silently, and is that safe (e.g. does anything depend on the leaderboard being non-empty after navigation)?
- The B1 fix: trace the demo arm (client/src/demo/demo_update.gleam UserClickedNotification) - it must call the shared helper from the neutral module. Trace vacancy-typed demo notifications end to end: does the demo store contain a matching vacancy so navigation actually fires? What if the demo vacancy id doesn't exist in the route set?
- notification_target_path: all entity_type/entity_id combinations (Some/None, known/unknown, demo vs real).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard; discard handled ones silently. No editorializing.""",

    "acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift - changes not asked for by the spec

This is a FIX-AUDIT round (round 3). Verify EACH round-2 blocker fix BITES, exactly per the round-3 briefing Lens-guards:
- B1 (r2): the helper (with resolve_application_vacancy) must live in a NEUTRAL module imported by both arms (client.gleam real arm and demo_update.gleam demo arm); the demo arm must call it; BOTH arms pinned by tests; vacancy-typed demo clicks must now NAVIGATE; no contract drift between arms. Read the actual files to confirm.
- B2 (r2): ApiReturnedLeaderboard (and the page variant) must carry the vacancy id and apply only on match, like the refresh handler's vacancy_detail_request_id. Verify the exact r2 repro in the actual code.
- Also audit the r2 warnings/notes in the prior consolidated.json: fixed or still present (vacancy_detail pb-28 test, filter-pill shrink-0 test, stepper md:justify-end, let _ discard, leaderboard_vacancy_id set-site pins, empty class attr, comment drift).
- Original acceptance: mobile re-sweep classes (compare bar padding, stepper semantics, filter chip ellipsis, 44px tap targets) must not have regressed in this diff.

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).""",

    "security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new or changed routes/handlers
- Missing input validation at system boundaries (notification entity_type/entity_id strings come from the server payload - check the client doesn't build URLs from unvalidated ids in a way that enables open redirect or route injection)
- Unsafe secret, token, or credential handling
- Data exposure (sensitive fields in client-visible state)
- Injection vectors (XSS via route construction, path traversal)
- Insecure defaults, missing CSRF protection, session/cookie gaps

This diff is client-only (Gleam/Lustre SPA) - calibrate accordingly; do not invent server-side concerns not reachable from this diff.""",

    "architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (Lustre MVU, shared helpers, copy.gleam for strings)?
- The B1 (r2) fix moves notification_target_path and resolve_application_vacancy into a NEUTRAL module importable by both client.gleam and demo/demo_update.gleam without import cycles. Verify: where does the neutral module live, is the placement sensible (not a grab-bag), are its dependencies minimal, do both arms actually import it, and is there no residual duplicated routing logic?
- The B2 (r2) fix adds a vacancy id to ApiReturnedLeaderboard and its page variant. Verify the message-shape change is consistent across msg.gleam, all construction sites, and all update handlers - no orphan constructor with the old shape.
- Is there a simpler alternative with the same outcome?
- Will it create technical debt? Does complexity match the problem?""",

    "codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (the neutral module, notification_target_path, resolve_application_vacancy, ApiReturnedLeaderboard's new field in msg.gleam, demo_update.gleam call sites)
- Are naming conventions and style consistent?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in location.)
- Are new dependencies (imports, packages) available, or do they need adding? Check client gleam.toml if a new module implies one.
- Are there existing tests this diff likely breaks? (Name them in location.) The client suite was 637 green at round 2 - sanity-check the claimed count delta against the new tests in the diff.
- Does it leave orphan code - functions, exports, types no longer referenced after the move to the neutral module (e.g. stale copies in client.gleam)?""",

    "tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage.

Round-3 specifics you MUST check by reading the test files in the worktree (client/test/client_test.gleam, client/test/demo/demo_flow_test.gleam, and any new test module for the neutral helper):
- B1 (r2) fix pins: both the real arm AND demo arm route through the helper, with REAL tests (revert-style: a wrong target path or a demo vacancy no-op must fail a test). Confirm the demo vacancy-navigation test actually drives UserClickedNotification through demo_update, not just the helper in isolation.
- B2 (r2) fix regression test: a late ApiReturnedLeaderboard carrying vacancy A's id while the route/tag is B must NOT apply A's rows, and the resolver must not resolve. Read the test and confirm it asserts the negative, not just construction.
- r2 warnings: vacancy_detail pb-28 test, filter-pill shrink-0 test - did they land this round or are they still absent?
- The demo r1-r5 gauntlet classes must not regress (demo_flow_test).
- The claimed suite count (637+ at round 2) - count the tests added in this diff and sanity-check.

Blind-spot heuristics: new state transitions without boundary tests, happy-path-only coverage, new message fields without mismatch-case tests.

Finally, emit ONE additional finding representing the advisory gate:
- title: "Advisory test gate: PASS" | "...CONCERNS" | "...FAIL"
- category: "coverage-gate"
- severity: PASS -> note, CONCERNS -> warning, FAIL -> blocker
- detail: rationale
Gate thresholds: PASS: P0 100%, P1 >=90%, overall >=80%; CONCERNS: P0 100%, P1 80-89%; FAIL: P0 <100% or P1 <80% or overall <80%.""",
}

os.makedirs(f"{OUT}/prompts", exist_ok=True)

with open(f"{OUT}/prompts/blind.md", "w") as f:
    f.write(BLIND)

for src, brief in LENSES.items():
    p = SHARED + f"""
--- YOUR LENS ---
{brief}

--- OUTPUT ---
Write ONE valid JSON array (nothing else in the file) to this EXACT path: {OUT}/{src}.json
""" + SCHEMA.format(src=src)
    with open(f"{OUT}/prompts/{src}.md", "w") as f:
        f.write(p)

print("wrote", sorted(os.listdir(f"{OUT}/prompts")))
