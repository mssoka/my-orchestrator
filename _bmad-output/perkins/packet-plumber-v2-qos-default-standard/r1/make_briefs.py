#!/usr/bin/env python3
"""Assemble the 7 Perkins lens briefs for the code chunk of PR #73 (round 1)."""
import pathlib

R1 = pathlib.Path("/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-qos-default-standard/r1")
WT = pathlib.Path("/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-qos-default-standard-r1")

DIFF = (R1 / "chunk-code.patch").read_text()
CONVENTIONS = (WT / "project-context.md").read_text()
SPEC_JOB = pathlib.Path("/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-qos-default-standard.md").read_text()
SPEC_ROUND = pathlib.Path("/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-qos-default-standard-r1.md").read_text()
SPEC_PR = (R1 / "pr-body.md").read_text()
SPEC_IMPL = (WT / "_bmad-output/implementation-artifacts/spec-v2-qos-default-standard.md").read_text()

SPEC = (
    "### ORIGINAL JOB BRIEFING (the spec: user report + acceptance criteria)\n"
    + SPEC_JOB
    + "\n\n### PERKINS ROUND-1 BRIEFING (lens-guards: what is canon, what not to re-litigate)\n"
    + SPEC_ROUND
    + "\n\n### PR BODY (root cause + decisions, as authored by the implementer)\n"
    + SPEC_PR
    + "\n\n### IMPLEMENTATION SPEC ARTIFACT (committed in this PR)\n"
    + SPEC_IMPL
)

CHUNK_NOTE = (
    "CHUNK CONTEXT: This diff is the code+script+docs chunk of PR #73 (branch v2-qos-default-standard). "
    "The PR also re-blesses 151 golden files (goldens/*.bin, *.png, *.t1) — that golden re-bless chunk is "
    "NOT part of this diff and is verified separately by mechanical means (harness fold-check, byte-level "
    "log.bin diffs, full local CI suite). Do not file findings about golden files being changed/re-blessed; "
    "DO file findings if the code itself is wrong.\n"
)

SCHEMA = """{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}"""

OUTPUT_CONTRACT = """--- OUTPUT ---
Write ONE valid JSON array — and NOTHING else — to the file:
  {out_file}
using your file-writing tool. Each element must match this schema exactly:
""" + SCHEMA + """

Output contract:
- The file contains ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- After writing the file, STOP. Your task is complete.

ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong."""

SHARED_HEAD = """You are reviewing a code diff. You have read-only access to the repository (your cwd is the repo root at exactly the reviewed state) and may verify the diff's claims against the actual codebase using your available tools. Review READ-ONLY: do not modify, create, or delete any repository file (your ONLY write is the output JSON file named below, outside the repo).

--- PROJECT CONVENTIONS ---
{conv}

--- DIFF (the review target) ---
{diff}

--- SPEC / CONTEXT ---
{spec}

--- CHUNK NOTE ---
{chunk}
"""

LENS_BRIEFS = {
    "edge": """--- YOUR LENS ---
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Pay particular attention to: the QoS weight arithmetic (zero-assignment pipes, 1/2/3-lane ladder rungs, weight sums, capacity splits, division/rounding), save/load round-trips of QoS state, era advance and pipe tier-change paths that reallocate capacity, and the E5/E6/E7 allocator guard interactions.""",

    "acceptance": """--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).

The governing canon (from the user report, 2026-08-19): a pipe with NO player QoS configuration carries ALL traffic on the Standard lane at 100% of capacity; Express/Best-effort carry nothing until the player assigns a type; the auto-ladder engages ONLY from the player's FIRST type→lane assignment (1 used lane = 100% · 2 = 70/30 · 3 = 50/30/20 — data-driven from balance.json lane_auto_reserve_ladder, NO hardcoded splits); the default survives save/load, era advance, and pipe upgrade/tier changes (no silent re-split). Verify EACH of these against the code (qos_unconfigured_weights() must be the single source at EVERY read site: pipe creation/apply_draw, resting fallback, serialization absent-when-empty default, E5 allocator fallback). One missed read site = drift resurface = blocker.

Also audit the required tests exist and actually assert the canon: zero-assignment → 100% Standard full-capacity under oversubscription; first assignment flips to ladder rung; removal of all assignments returns to 100%; save/load + era + tier survival.""",

    "security": """--- YOUR LENS ---
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

Note: this is an offline desktop game (Odin + raylib) — calibrate severity accordingly; a finding that matters only for a web service is a note here, not a blocker. Deserialization (save/load) robustness against corrupted or hostile save files IS in scope.""",

    "architecture": """--- YOUR LENS ---
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

Specific design claims in the PR body to evaluate against the code: qos_unconfigured_weights(cat) as the single data-driven source for the resting default (ODN-5 data-driven balance.json); the ladder row [100] being lane_auto_reserve_ladder[0] rather than a new constant; never-drop fold gated on assigned; E6 guard checking settled weights; demos mirroring the app's auto-follow weights.""",

    "codebase": """--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in location.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in location.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specifically hunt for MISSED READ SITES of the unconfigured default: grep for every consumer of pipe weights (qos_pipe_weights, qos_auto_weights, qos_pipe_caps, lane_presets, default_preset_idx, def_w, weights reads in app/, harness/, demos/) and check each now resolves to the 100%-Standard default for unconfigured pipes — a site still yielding the old balanced [1,1,1] preset is exactly the drift this PR fixes resurfacing.""",

    "tests": """--- YOUR LENS ---
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

The critical behaviours to trace (from the spec): zero-assignment → 100% Standard (oversubscribed Standard uses FULL capacity); first type→lane assignment engages the ladder rung; removing all assignments returns to 100% Standard; default survives save/load AND era advance AND pipe tier change/upgrade; never-drop class interactions with the untouched default. Also: are the re-pinned stats/crisis shape pins asserting the NEW allocation, and do the lane-only fixture changes (sla_weights, lane_pipe_setup, test_congested_run) mirror the app's actual auto-follow weights?

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

BLIND = """You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec, no codebase. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

ISOLATION RULE: reading any file other than this brief invalidates your lens. Your entire context is the DIFF section below. Do not open, list, or search any other path.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (comments, doc statements in the diff)

--- DIFF ---
{diff}

{output}"""

def out_contract(lens):
    return OUTPUT_CONTRACT.replace("{out_file}", str(R1 / f"{lens}.json"))

def main():
    for lens, brief in LENS_BRIEFS.items():
        text = SHARED_HEAD.format(conv=CONVENTIONS, diff=DIFF, spec=SPEC, chunk=CHUNK_NOTE)
        text += brief + "\n\n" + out_contract(lens) + "\n"
        (R1 / f"brief-{lens}.md").write_text(text)
        print(f"brief-{lens}.md", len(text))
    blind = BLIND.format(diff=DIFF, output=out_contract("blind").replace(
        "the actual codebase before it reaches the report",
        "the diff above before it reaches the report"))
    (R1 / "brief-blind.md").write_text(blind)
    print("brief-blind.md", len(blind))

if __name__ == "__main__":
    main()
