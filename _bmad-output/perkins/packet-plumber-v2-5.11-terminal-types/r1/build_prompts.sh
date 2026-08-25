#!/bin/bash
set -e
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r1
CONV=$(cat "$WT/project-context.md")
BRIEF=$(cat "$OUT/spec-briefing.md")
PRBODY=$(python3 -c "import json;print(json.load(open('$OUT/spec-prbody.json'))['body'])")
LENSOUT="$OUT/lens-out"
mkdir -p "$LENSOUT"

SCHEMA='{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use '\''N/A'\'' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Write ONLY the JSON array (no prose, no markdown fencing, no preamble) to the file named in the FILE-OUTPUT line below using your file-writing tool, then stop.
- Return ONLY the JSON array as your final answer too. Empty array [] is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The evidence field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.'

declare -A BRIEFS
BRIEFS[edge]='You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn'\''t account for, input the new code doesn'\''t validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.'

BRIEFS[acceptance]='Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in detail (quote the exact phrase from the spec when possible).'

BRIEFS[security]='OWASP-oriented security review of the diff. Identify:
- Auth/authz gaps in new endpoints, routes, or handlers
- Missing input validation at system boundaries
- Unsafe secret, token, or credential handling (leaks to logs, client responses, error pages)
- Data exposure (sensitive fields in responses, logs, or client-visible state)
- Injection vectors (SQL, XSS, command, path traversal, SSRF)
- Unsafe deserialization, insecure defaults, missing CSRF protection
- Session or cookie handling gaps'

BRIEFS[architecture]='Architectural fit review. Given the diff and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?'

BRIEFS[codebase]='Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in location.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in location.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?'

BRIEFS[tests]='Test coverage analysis via traceability.

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
- FAIL: P0 <100%, or P1 <80%, or overall <80%'

for WAVE in code g1 g2 g3 g4 g5 g6; do
  CHUNK="$OUT/chunks/wave-$WAVE.diff"
  DIFF=$(cat "$CHUNK")
  case $WAVE in
    code) ORIENT="This chunk contains ALL code, data, demo-fixture and documentation changes of the PR (every non-goldens file).";;
    g1) ORIENT="This chunk contains the NEW golden files (terminal_types.*), the re-blessed node_health.* golden files, every binary golden stub (one-line 'Binary files differ' entries for .log.bin/.png files), plus head+tail EXCERPTS of the six largest re-blessed .t1 tick-hash dumps (elision marked inline). Other .t1 goldens are reviewed in other chunks of the same canonical diff (big-diff chunking).";;
    g2) ORIENT="This chunk contains re-blessed golden .t1 tick-hash dumps: qos_manual, qos_emphasis, qos_auto, sla, qos_contention. Part of the canonical PR diff (big-diff chunking).";;
    g3) ORIENT="This chunk contains re-blessed golden .t1 tick-hash dumps: health_lose, forecast_preview, input_parity_draw, input_parity_draw_wide, win, lose, flow, draw. Part of the canonical PR diff (big-diff chunking).";;
    g4) ORIENT="This chunk contains the re-blessed golden .t1 tick-hash dump: juice (whole file). Part of the canonical PR diff (big-diff chunking).";;
    g5) ORIENT="This chunk contains the re-blessed golden .t1 tick-hash dump: audio (whole file). Part of the canonical PR diff (big-diff chunking).";;
    g6) ORIENT="This chunk contains re-blessed golden .t1 tick-hash dumps: router_tiers, router_ceiling, place, ecmp, ecmp_cost, demolish, demolish_bundle, audio_throttle, bundle, demolish_node, boot, forecast_shift. Part of the canonical PR diff (big-diff chunking).";;
  esac
  for LENS in blind edge acceptance security architecture codebase tests; do
    P="$OUT/prompts/$WAVE-$LENS.md"
    if [ "$LENS" = blind ]; then
      cat > "$P" <<EOF
You are a cynical, jaded reviewer with zero patience for sloppy work. The diff below is ALL the context you have — no project files, no spec. Assume problems exist. Be skeptical. Look for what's missing, not just what's wrong. Precise, professional tone — no profanity, no personal attacks.

$ORIENT

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
$DIFF

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
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

Output contract: write ONLY the JSON array (no prose, no fencing, no preamble) to the file
$LENSOUT/blind-$WAVE.json
using your file-writing tool, then stop. Also return the JSON array as your final answer. [] is valid.

ACCURACY MANDATE: no claim you make will be taken at face value. Every finding will be cross-checked against the actual diff before reporting. Findings whose evidence cannot be located in the diff above, or whose claims contradict what the diff actually shows, are DISCARDED silently. Quote the exact diff lines in evidence. Speculation without quoted evidence is dropped. Accuracy > volume — an empty array is an honest answer when nothing is wrong.
EOF
    else
      cat > "$P" <<EOF
You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. The repository checkout at the reviewed state is at:
$WT
(all verification reads happen there; treat it as the source of truth).

Chunk orientation: $ORIENT

--- PROJECT CONVENTIONS ---
$CONV

--- DIFF ---
$DIFF

--- SPEC / CONTEXT ---
The original job briefing (the spec for this work):

$BRIEF

The PR body (the implementing minion's claims — audit them):

$PRBODY

--- YOUR LENS ---
${BRIEFS[$LENS]}

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
$SCHEMA

FILE-OUTPUT: write ONLY your JSON array to the file
$LENSOUT/$LENS-$WAVE.json
using your file-writing tool, then stop. (Your source value is: $LENS)
EOF
    fi
  done
done
echo BUILT; ls prompts | wc -l
