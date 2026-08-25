#!/usr/bin/env bash
# Assemble the 7 Perkins r4 lens prompt files (verbatim code-review skill prompts,
# headless file-output contract + r4 fix-audit re-review context). Lenses must not
# derive paths — every path pasted.
set -euo pipefail

ROUND=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-motion-readability/r4
DIFF=$ROUND/diff.patch
SPEC=/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-motion-readability.md
CONV=/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-motion-readability-r4/project-context.md
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-motion-readability-r4
PRIOR=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-motion-readability/r3/consolidated.json

SCHEMA='{
  "source": "<see YOUR LENS for your assigned value>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use '\''N/A'\'' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}'

ACCURACY='ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.'

OUTCONTRACT='Output contract:
- Write ONLY your JSON array (nothing else — no prose, no markdown fencing) to this exact file: %s
- Use the write tool with that absolute path verbatim. Do not derive or transform the path.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.
- When the file is written, STOP. Your work is done — reply with a single line: DONE.'

REREVIEW="--- RE-REVIEW CONTEXT (round 4 = fix-audit of round 3) ---

This is round 4 of a review loop. Round 3 (at parent sha 44ebc25) posted the findings below; the implementing agent then pushed fix commit 8f2ae3b claiming all of them folded. Your job has TWO parts:

PART 1 — FIX AUDIT (do this first): for each prior finding that falls in your lens, re-read the cited code at the current worktree state and classify it \`fixed\` or \`still-present\`. Do NOT trust the prior wording or the commit message — re-verify by reading the code and, where you can, by RUNNING the tests. Emit each still-present finding as a finding in your JSON with its title prefixed \`[still present since r3]\`; emit a genuinely-fixed prior BLOCKER/WARNING as a note titled \`[fixed since r3] <short title>\` (evidence = the fixing code) ONLY for the two r3 blockers B1/B2 and warnings W1-W4; fixed notes need not be reported.

PART 2 — FRESH PASS: review the whole diff at this sha with your lens as normal. The fix commit 8f2ae3b itself introduced new code (activation helper + render test in app/main.odin/app/render, trail-ring pins, harness/motion_pixel.odin ~181 new lines, harness/manifest.odin ~54 new lines, CI wiring) — delta-introduced blockers are the norm in fix rounds: scrutinize the FIX code at least as hard as the original code.

Prior r3 findings (JSON; fix-audit targets marked B1/B2/W1-W4 in evidence_ref):
"

mkdir -p "$ROUND"

shared_head() {
  cat <<EOF
You are reviewing a code diff. You have read-only access to the repository (the checkout at $WT is exactly the reviewed state) and may verify the diff's claims against the actual codebase using your available tools. You are a review lens: report findings only — never edit, fix, or write any repository file (the ONLY file you may write is your output JSON file named below).

--- PROJECT CONVENTIONS ---
EOF
  cat "$CONV"
  echo
  echo '--- DIFF ---'
  cat "$DIFF"
  echo
  echo '--- SPEC / CONTEXT ---'
  cat "$SPEC"
  echo
  echo 'Context docs referenced by the spec (kyle-design-directions.md §4, design-audit.html Q3) live under _bmad-output/ in the repo if you need them.'
  echo
  echo "$REREVIEW"
  cat "$PRIOR"
  echo
  echo '--- YOUR LENS ---'
}

shared_tail() {
  local src="$1" out="$2"
  cat <<EOF
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
$SCHEMA

Your assigned "source" value is: "$src"

$(printf "$OUTCONTRACT" "$out")

$ACCURACY
EOF
}

# ---- non-blind lenses ------------------------------------------------------
for lens in edge acceptance security architecture codebase tests; do
  out="$ROUND/$lens.json"
  {
    shared_head
    case "$lens" in
      edge)
        cat <<'EOF'
You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

r4 delta emphasis: the NEW code in the fix commit is prime edge-hunting ground — harness/motion_pixel.odin (a new headless pixel-assertion harness), harness/manifest.odin (new manifest verification), the activation-helper alpha computation, and the trail-ring test driving code.
EOF
        ;;
      acceptance)
        cat <<'EOF'
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

r4 note: the not-re-litigatable items from prior rounds stay non-findings: the 60 Hz strip substitution for the AC's literal '100 ms' (documented deviation), and the motion.dem/38-demo re-blesses (cause-documented). Only flag them if the DOCUMENTATION itself drifted further.
EOF
        ;;
      security)
        cat <<'EOF'
OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps

This is a view-layer game-rendering diff — most OWASP classes don't apply; report only what genuinely does.
EOF
        ;;
      architecture)
        cat <<'EOF'
Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

r4 fix-audit targets in your lane: (W4) the new harness/manifest.odin verification — does it actually bite on divergent timelines, and is it wired where the strip path runs? (r3 N10) the interp-alpha derivation duplication (app accum-based vs strip wall-ms-based) — the fix commit touched both sites; check whether a shared definition emerged or the duplication persists.
EOF
        ;;
      codebase)
        cat <<'EOF'
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

r4 fix-audit targets in your lane: (W3) the delivered-snap test — does the pin now actually read p.delivered (interp_continuous consulting the delivered flag), or does it still pass via anchor-mismatch? (W4) harness/manifest.odin — do its referenced files/paths/formats actually exist and match the golden .t1 layout? (r3 N1) was the `// hmm` scratch deleted? (r3 N3) was the motion_strip indentation fixed?
EOF
        ;;
      tests)
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

You may run the test suites (`odin test app/render`, `odin test core`) and inspect CI wiring (.github/workflows/ci.yml, tools/ci-local.sh, tools/harness.sh) to verify what actually gates — claims must be checked against what really runs.

r4 fix-audit targets in your lane (verify BY EXECUTION where possible, not by reading claims):
- (B1) the activation is now PINNED: main.odin's accum->alpha helper must be unit-pinned AND an rlsw render test must assert the drawn pixel at alpha=0.5 — check that dropping the interp_alpha argument at the draw_packets call site would now FAIL a test (read the test to see if it really goes through draw_packets with the arg, or merely re-tests the helper). Run `odin test app/render`.
- (B2) the advisory gate: recompute it at THIS sha. Last round it FAILED (P1 67%, overall 57%). Does it flip to PASS with the new pins (activation wiring, trail ring/echo, motion-pixel harness, manifest-verify)?
- (W1) remote CI parity: does .github/workflows/ci.yml now run the render/input/audio/harness suites AND the motion-pixel gate? Read the yml — do not assume the local mirror implies the remote.
- (W2) trail-ring mechanics: do the new pins actually assert ring fill order, drop-oldest shift, the 0.5px move gate, stationary no-push, and fades[trail_n-1-k] indexing — or only a subset?

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
        ;;
    esac
    echo
    shared_tail "$lens" "$out"
  } > "$ROUND/lens-$lens.md"
done

# ---- blind hunter (isolated: diff only) ------------------------------------
out="$ROUND/blind.json"
{
  cat <<'EOF'
You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

Focus on:
- Obvious bugs visible from the diff alone
- Dead code, unused symbols
- Inconsistent changes across hunks (one place updated, another missed)
- Broken invariants visible in the diff
- Suspicious control flow
- Contradictions within the diff itself
- Changes that don't match their claimed purpose (commit message, file header comment, etc.)

ISOLATION RULE: reading anything beyond the diff below invalidates your lens. Do NOT open repository files, do NOT explore any directory — the diff text below is your entire universe. Your only tool use is writing your output file.

--- DIFF ---
EOF
  cat "$DIFF"
  echo
  cat <<EOF
--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
$SCHEMA

Your assigned "source" value is: "blind"

$(printf "$OUTCONTRACT" "$out")

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose \`evidence\` cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in \`evidence\`. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
EOF
} > "$ROUND/lens-blind.md"

wc -l "$ROUND"/lens-*.md
