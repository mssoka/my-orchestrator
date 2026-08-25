#!/usr/bin/env python3
# gen-prompts.py — build all <wave>-<lens>.md prompts for the r4 lens waves
import os, json

R4 = '/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4'
WORKTREE = '/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r4'
WAVES = ['code','g1','g2','g3','g4','g5']
LENSES = ['blind','edge','acceptance','security','architecture','codebase','tests']

conventions = open(f'{WORKTREE}/project-context.md').read()
briefing = open(f'{R4}/spec-briefing.md').read()
prbody = json.load(open(f'{R4}/spec-prbody.json'))['body']

ORIENT = {
'code': "This chunk contains ALL code, data, demo-fixture and documentation changes of the PR (every non-goldens file). It carries the ENTIRE round-4 delta (the r3-fold: core/demand_test.odin, harness/palcheck.odin, harness/main.odin, harness/fold_check.odin).",
'g1': "This chunk contains the fold-critical and NEW goldens: boot.t1 (the canonical fold-proof demo), node_health.t1 + terminal_types.t1 (the demos that spawn the new terminal classes), the input-parity t1s, and every binary golden stub (.log.bin/.png — 'Binary files differ' lines).",
'g2': "This chunk contains the 8 largest re-blessed .t1 goldens as head/tail EXCERPTS (bodies elided mid-file with an explicit marker; full files are in the worktree under goldens/).",
'g3': "This chunk contains re-blessed .t1 goldens (forecast_preview, health_lose, qos_manual), whole.",
'g4': "This chunk contains re-blessed .t1 goldens (qos_emphasis, qos_auto, sla, qos_contention, demolish_node, router_tiers, router_ceiling, place), whole.",
'g5': "This chunk contains the remaining re-blessed .t1 goldens (ecmp, demolish, demolish_bundle, audio_throttle, bundle, lose, win, flow, draw, forecast_shift, ecmp_cost), whole.",
}

ROUND_CTX = """NOTE — round context: this is round 4 (fix-audit, cap lifted — loop until approved) on the SAME PR. The reviewed sha is the r3-fold head (0161c2b) — a CODE-ONLY fold on the r3-reviewed tree: the goldens/ tree is byte-identical to the r3-reviewed set (git-diff-empty, mechanically proven). Treat as EXPECTED, not findings:
- the wholesale .t1 re-bless / tick-1 shifts / catalog_hash-only diffs in .log.bin headers — the documented deliberate catalog-fold design; r1-r3 mechanically certified it (8-byte log.bin partition, 72-png byte identity, the splice proof independently reproduced). Do NOT re-flag the re-bless's existence; auditing its CAUSE documentation/consistency remains fair.
- every .png golden rendering the #67 procedural background tiles (rebased base).
- r3-certified SETTLED items — do not re-litigate: the honest W9 re-pin design (B1-r1: EXPECTED/window/campus-must-exist/campus-must-source, the grown-mesh start map doctrine), the r1 W1-W4 fixes (palcheck sprite scan, ratio-split windows, PR citations, inertness test), the rebase delta, the roster math + era gates, the #65 sprite wiring + canon shapes, the 7.1 sprite pipeline, the 5.9/5.10 accumulator contracts, the fair-crisis grown-mesh start-map, the fallback-model caveat.

What is NEW at this reviewed head — the r3-fold delta, exactly 4 files (+138/-17), the fix fold answering r3's blocker + warning + notes. Delta-introduced regressions are exactly what this round hunts — scrutinize these hardest:
1. r3-B1 (was THE blocker): test_role_absent_demand_inert double-freed the trimmed era-3 entries (deferred delete(trimmed) ran LIFO against catalogs_destroy(cat2) on the aliased array; odin-test's tracking allocator masked it in-suite). The fold REMOVES the defer and documents ownership. Verify the ownership transfer is actually sound now (no leak, no double-free, no use-after-free).
2. r3-W1: W9's crowd floor was vacuous (fixture pre-seeds 14 streaming terminals; hosts>=8 held with growth dead). The fold adds a growth-born count (node_id >= 20 — fixture spawns 20 nodes first, ids monotonic E11) and pins growth_born >= 1. Verify the >= 20 threshold is actually correct against the fixture (count the seeded nodes) and the pin bites.
3. r3-N3: campus-half floor now quantitative: campus_window_spawns >= 10*WINDOW*95/100 (was existence-only > 0). Note the literal 10 (campus vol 1 x multiplier 10) — check consistency with the derived EXPECTED.
4. r3-N4: test_terminal_class_profiles' SURGE_AT now derives from the set-piece (was hardcoded 1200).
5. r3-N5: W9's EXPECTED now derives: sum of streaming-class entry volumes x surge.multiplier x WINDOW (was literal 20).
6. r3-N6: run_inert now captures + frees record_run's hash stream (was a 2x4.69KiB leak).
7. r3-N7: palcheck unit-pins sprite_index_building (content_host->4, small_biz->9, campus->10, residential->0) and raises pixel floors (>150 small_biz, >500 campus; measured 176/1100).
8. r3-N11: NEW harness subcommand `fold-check <prev-hash> <prev-tick1>` (harness/fold_check.odin + main.odin verb) — the re-runnable fold-splice verifier (exit 0 PASS / 1 FAIL / 2 usage). Scrutinize: the splice offset (33..40), the boot run setup (seed 42, era 0, fixture), parse/arg handling, exit-code paths, and whether it actually proves fold-only-ness.
"""

SPEC = f"""--- SPEC / CONTEXT ---
The original job briefing (the spec for this work):

{briefing}

The PR body (the implementing minion's claims — audit them):

{prbody}
"""

SHARED_HEAD = """You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
{WORKTREE}
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: {ORIENT}

{ROUND_CTX}

--- PROJECT CONVENTIONS ---
{CONV}

--- DIFF ---
{DIFF}
"""

LENS_BRIEFS = {
'edge': """You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.""",
'acceptance': """Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).""",
'security': """OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps""",
'architecture': """Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?""",
'codebase': """Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?""",
'tests': """Test coverage analysis via traceability.

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

BLIND_HEAD = """You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

{ORIENT}

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

BLINDNESS RULE: this prompt and the diff embedded below are your ONLY permitted input. Do NOT read any other file, do NOT list directories, do NOT inspect any repository or run exploratory commands — reading anything beyond this prompt invalidates your lens. Your ONLY permitted tool use is writing your output file named below.

--- DIFF ---
{DIFF}
"""

SCHEMA = """--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{{
  "source": "{SOURCE}",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use N/A ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}}

Output contract:
- Write ONLY the JSON array (no prose, no markdown fencing, no preamble) to the file named in the FILE-OUTPUT line below using your file-writing tool, then stop.
- Also return ONLY the JSON array as your final answer. Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT: write ONLY your JSON array to the file
{OUTFILE}
using your file-writing tool, then stop. (Your source value is: {SOURCE})"""

os.makedirs(f'{R4}/prompts', exist_ok=True)
for w in WAVES:
    diff = open(f'{R4}/chunks/{w}.diff').read()
    for lens in LENSES:
        out = f'{R4}/lens-out/{lens}-{w}.json'
        if lens == 'blind':
            body = BLIND_HEAD.format(ORIENT=ORIENT[w], DIFF=diff) + SCHEMA.format(SOURCE='blind', OUTFILE=out)
        else:
            head = SHARED_HEAD.format(WORKTREE=WORKTREE, ORIENT=ORIENT[w], ROUND_CTX=ROUND_CTX, CONV=conventions, DIFF=diff)
            body = head + SPEC + '\n--- YOUR LENS ---\n' + LENS_BRIEFS[lens] + '\n\n' + SCHEMA.format(SOURCE=lens, OUTFILE=out)
        open(f'{R4}/prompts/{w}-{lens}.md','w').write(body)
print('wrote', len(WAVES)*len(LENSES), 'prompts')
