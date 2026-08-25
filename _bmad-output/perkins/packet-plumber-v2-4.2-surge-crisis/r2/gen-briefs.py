#!/usr/bin/env python3
"""Generate the 49 r2 lens briefs (7 chunks x 7 lenses) for the Perkins r2 round."""
import json, os

R2 = "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r2"
WT = "/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-4.2-surge-crisis-r2"
CHUNKS = {
 "c1": "chunk-c1-spec-app-core.patch",
 "c2": "chunk-c2-data-demos-smallgoldens.patch",
 "c3": "chunk-c3-goldens-qos.patch",
 "c4": "chunk-c4-goldens-contention-emphasis-sla.patch",
 "c5": "chunk-c5-goldens-surge-a.patch",
 "c6": "chunk-c6-goldens-surge-b.patch",
 "c7": "chunk-c7-goldens-warn.patch",
}

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

ACCURACY_FULL = '''Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
ACCURACY MANDATE — this is the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.'''

ACCURACY_BLIND = '''Output contract: ONLY the JSON array. No prose, no fencing, no preamble. `[]` is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose `evidence` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in `evidence`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.'''

LENS_BRIEFS = {
 "blind": '''You are a cynical, jaded reviewer with zero patience for sloppy work. The diff chunk below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

BLINDNESS CONTRACT: you have NO other context. Do NOT read the repository, the worktree, project files, or any spec. Reading anything beyond the diff below invalidates your lens.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)''',
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
- warning: P1 gap at 80-89% OR P2 gap
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
- CONCERNS: P0 100%, P1 80-89%, overall ≥80%
- FAIL: P0 <100%, or P1 <80%, or overall <80%''',
}

SPEC_BLOCK = '''--- SPEC / CONTEXT ---
Read ALL of these files (they are your spec; the GitHub issue is "none" — the sprint story stands in for it):
- {r2}/spec/job-briefing.md  (the original job briefing)
- {r2}/spec/story-4-2.md     (the sprint story 4.2 — the canonical acceptance criteria)
- {r2}/spec/gdd-crisis.md    (GDD M5 — the crisis model + fairness rules)
- {r2}/spec/architecture-excerpts.md (ODN-4, ODN-7, S6.4, S11.3 fairness, E10/E13)
- {r2}/spec/lens-guards.md   (the reviewer lens-guards — read BEFORE anything; several are BLOCKER-class)
- {r2}/spec/r2-mandate.md    (the round-2 fix-audit mandate)
- {r2}/spec/r1-findings.md   (the r1 findings + claimed fixes — the rework you are auditing)'''.replace('{r2}', R2)

R2_CTX = '''This is Perkins review ROUND 2 — a FIX-AUDIT round of PR #36 (job packet-plumber-v2-4.2-surge-crisis). Round 1 (CHANGES_REQUESTED) produced blockers B1/B2, warnings W1-W7, notes N1-N13; the diff below is the rework claiming to fix them (commit f906725, "perkins r1: stable crisis identity, frozen attribution restore, drop-site input, test-gate pins"). The round orchestrator (Perkins) runs the authoritative fix audit against the worktree. YOUR job: find NEW findings — regressions the rework introduced, new bugs, new coverage gaps, claims visibly false in your chunk. Rules:
- Do NOT re-file an r1 finding as a new finding unless the code in YOUR chunk proves a claimed fix is absent — then file it with title prefix "STILL-PRESENT: " and category "fix-audit".
- The r1 findings + claimed fixes are listed in spec/r1-findings.md; the round-2 mandate (B1/B2/W1-W7/N1-N13 verification) is spec/r2-mandate.md.'''

def build(chunk_id, lens):
    chunk_txt = open(os.path.join(R2, CHUNKS[chunk_id])).read()
    out = os.path.join(R2, f"{lens}-{chunk_id}.json")
    parts = []
    if lens == "blind":
        parts.append(f"{LENS_BRIEFS['blind']}\n\nThe diff chunk is {chunk_id} of 7 chunks of one canonical diff (15,473 lines total, split by file group).\n\n--- DIFF (chunk {chunk_id}) ---\n{chunk_txt}\n\n--- OUTPUT ---\nReturn ONE valid JSON array. Each element must match this schema exactly:\n{SCHEMA}\n\n{ACCURACY_BLIND}\n\nFILE-OUTPUT CONTRACT: your ONLY deliverable is the file {out} — write the JSON array to that exact absolute path (overwrite if it exists), then STOP. Do not write any other file. Your final message must be exactly: \"DONE {out} <N findings>\" where N is the number of findings (0 is fine).")
    else:
        parts.append(f"You are a code-review specialist reviewing ONE chunk of a larger code diff (chunk {chunk_id} of 7 — the canonical diff was 15,473 lines, split by file group per the review protocol; findings from every chunk are merged before verification). You have read-only access to the repository at the worktree path below and may verify the diff's claims against the actual codebase using read/grep/bash (read-only). NEVER modify any file, in the repo or elsewhere.\n\n{R2_CTX}\n\n--- WORKTREE ---\n{WT}\n\n--- PROJECT CONVENTIONS ---\nRead {WT}/project-context.md — it is the project's mandatory conventions (core purity, integer-only sim, determinism spine, no-globals, arena discipline, golden harness rules). Follow it when judging the diff.\n\n--- DIFF (chunk {chunk_id}) ---\n{chunk_txt}\n\n{SPEC_BLOCK}\n\n--- YOUR LENS ---\n{LENS_BRIEFS[lens]}\n\n--- OUTPUT ---\nReturn ONE valid JSON array. Each element must match this schema exactly:\n{SCHEMA}\n\n{ACCURACY_FULL}\n\nFILE-OUTPUT CONTRACT: your ONLY deliverable is the file {out} — write the JSON array to that exact absolute path (overwrite if it exists), then STOP. Do not write any other file. Your final message must be exactly: \"DONE {out} <N findings>\" where N is the number of findings in the array (0 is fine).")
    return "\n".join(parts)

manifest = []
for c in CHUNKS:
    for lens in LENS_BRIEFS:
        brief = f"brief-{c}-{lens}.md"
        with open(os.path.join(R2, "briefs", brief), "w") as f:
            f.write(build(c, lens))
        manifest.append([c, lens, os.path.join(R2, "briefs", brief), os.path.join(R2, f"{lens}-{c}.json")])

with open(os.path.join(R2, "brief-manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1)
print("wrote", len(manifest), "briefs")
