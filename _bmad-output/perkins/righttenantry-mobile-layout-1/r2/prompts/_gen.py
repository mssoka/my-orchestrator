#!/usr/bin/env python3
import os

OUT = "/Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r2"
WT = "/Users/moses/.herdr/worktrees/RightTenantry/perkins-mobile-layout-1-r2"

SHARED = f"""You are reviewing a code diff in the RightTenantry repo. You have read-only access to the repository worktree and may verify the diff's claims against the actual codebase using your tools. Do NOT modify, build, or write any repo file. The ONLY file you may write is your output JSON at the path given below.

--- PROJECT CONVENTIONS ---
Read {WT}/AGENTS.md for project conventions.

--- DIFF ---
The canonical diff is at {OUT}/diff.patch - read it fully with the read tool. Review exactly these bytes; do not re-generate or re-fetch the diff.

--- WORKTREE (verification) ---
{WT} is a checkout at exactly the reviewed state (sha 3acbf6ba72268bee91462230d480358f8b86799e). Every verification read happens here.

--- SPEC / CONTEXT ---
Read both:
- /Users/moses/code/_bmad-output/briefings/righttenantry-mobile-layout-1.md (original job spec: 5 mobile UX fixes + acceptance criteria)
- /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-mobile-layout-1-r2.md (round-2 reviewer briefing; the "Lens-guards" section names what each round-1 blocker fix must satisfy)

--- PRIOR ROUND (this is a FIX-AUDIT round) ---
The round-1 consolidated findings are at /Users/moses/code/_bmad-output/perkins/righttenantry-mobile-layout-1/r1/consolidated.json. Round 1 ended NEEDS CHANGES with 2 blockers (B1: stale-leaderboard fabricated vacancy id; B2: no navigation pin for vacancy-typed notifications), 2 warnings, 4 notes. This diff is the fix for those.
Do NOT re-report r1 findings as new. If an r1 finding's fix is MISSING or insufficient, report it as a finding titled "<original title> (still present since round 1)" with severity at least as high as round 1.
Do NOT re-litigate: the client-side resolution choice (loaded leaderboard + leaderboard_vacancy_id tag, else graceful no-op), the user-approved 5-fix list, or the existence of the r1 fixes themselves unless they failed to land.

--- ROUND-2 HARD BLOCKER CLASS ---
The notification deep-link contract: BOTH entity types (vacancy AND application) navigate + mark read; no fabricated vacancy ids (application resolution must require leaderboard_vacancy_id == route vid); vacancy behavior unchanged. A pure notification_target_path/3 routing decision must exist and BOTH the real arm (client.gleam) and demo arm (demo_update.gleam) must route through it, with real tests pinning it (a wrong target path must fail a test).
"""

BLIND = f"""You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have - no project files, no spec, no codebase access. Reading anything beyond the diff INVALIDATES your lens; do not open any other file. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone - no profanity, no personal attacks.

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

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself. Examples: boundary conditions (empty lists, nulls, None options, zero counts), concurrent operations and race conditions (e.g. leaderboard fetch responses arriving out of order with route changes - check whether a late ApiReturnedLeaderboard for vacancy A can overwrite the tag after navigating to vacancy B), unhandled error paths, off-by-one errors, state the new code doesn't account for, input the new code doesn't validate.

Pay special attention to the round-1 repro: VacancyDetail(A) -> navigate to /vacancies/B/edit or /compare (stale Success) -> click an application-typed notification of A -> must NOT resolve to B. Trace every route entry that touches model.leaderboard / leaderboard_vacancy_id and confirm the tag cannot go stale. Trace notification_target_path for all entity_type/entity_id combinations (Some/None, known/unknown, demo vs real).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard; discard handled ones silently. No editorializing.""",

    "acceptance": """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift - changes not asked for by the spec

This is a FIX-AUDIT round. Verify EACH round-1 blocker fix BITES, exactly per the round-2 briefing Lens-guards:
- B1: the leaderboard must be tagged with the vacancy id it was fetched for (leaderboard_vacancy_id set on fetch/response) and resolve_application_vacancy must require it to equal the route vid (or leaderboard reset on the other vacancy-scoped route entries). Verify the exact r1 repro in the actual code: client/src/client.gleam handle_browser_change + resolve_application_vacancy. Real AI-failure notifications carry only the application id (server/src/ai/ai_notifications.gleam) - the resolver must not fabricate a vacancy id from a stale source.
- B2: a pure notification_target_path/3 routing decision (vacancy -> /vacancies/<vid>, application -> resolved app detail, others/unknown -> None) must pin BOTH entity types + the no-op cases; the real AND demo click arms must BOTH route through it. Verify by reading client.gleam and client/src/demo/demo_update.gleam that both call the same helper.
- Also audit the r1 warnings/notes in the prior consolidated.json: fixed or still present.

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).""",

    "security": """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new or changed routes/handlers
- Missing input validation at system boundaries (notification entity_type/entity_id strings are attacker-influenceable only via server payload - check the client doesn't build URLs from unvalidated ids in a way that enables open redirect or route injection)
- Unsafe secret, token, or credential handling
- Data exposure (sensitive fields in client-visible state)
- Injection vectors (XSS via route construction, path traversal)
- Insecure defaults, missing CSRF protection, session/cookie gaps

This diff is client-only (Gleam/Lustre SPA) - calibrate accordingly; do not invent server-side concerns not reachable from this diff.""",

    "architecture": """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions (Lustre MVU, shared helpers, copy.gleam for strings)?
- Does it introduce unnecessary coupling between modules? Note r1 flagged deep-link logic duplicated between the real arm (client.gleam) and demo arm (demo_update.gleam) - the fix claims a shared pure helper notification_target_path/3; verify the duplication is actually resolved and the helper lives somewhere both arms can import without cycles.
- Is there a simpler alternative with the same outcome?
- Will it create technical debt? Does complexity match the problem?""",

    "codebase": """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (notification_target_path in client.gleam, leaderboard_vacancy_id in model.gleam, demo_update.gleam call sites)
- Are naming conventions and style consistent?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in location.)
- Are new dependencies available?
- Are there existing tests this diff likely breaks? (Name them in location.) The client suite was 632 green at round 1 and is claimed 637 green now - sanity-check that test count delta matches the new tests in the diff.
- Does it leave orphan code - functions, exports, types no longer referenced?""",

    "tests": """Test coverage analysis via traceability.

For each behaviour change in the diff, trace to a test (new in the diff, or existing). Classify as FULL / PARTIAL / NONE coverage.

Round-2 specifics you MUST check by reading client/test/client_test.gleam and client/test/demo/demo_flow_test.gleam in the worktree:
- The notification_target_path pins must be REAL (revert-style: a wrong target path must fail a test) - read the tests and confirm they assert exact paths for vacancy, application, unknown, and None cases.
- Both the real arm AND demo arm must route through the helper, and tests must cover both.
- The stale-leaderboard repro (B1) must have a regression test: stale Success leaderboard tagged with vacancy A + route vid B must NOT resolve.
- r1 warnings: vacancy_detail pb-28 test, filter-pill shrink-0 test - did they land?
- The demo r1-r5 gauntlet classes must not regress (demo_flow_test).

Blind-spot heuristics: new state transitions without boundary tests, happy-path-only coverage, new model fields without tests.

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
