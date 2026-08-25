#!/bin/bash
set -e
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r1
LENSOUT="$OUT/lens-out"
CONV=$(cat "$WT/project-context.md")
BRIEF=$(cat "$OUT/spec-briefing.md")
PRBODY=$(python3 -c "import json;print(json.load(open('$OUT/spec-prbody.json'))['body'])")
mkdir -p "$LENSOUT"

SCHEMA='{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use N/A ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, <=40 words>",
  "recommended_fix": "<the change to apply, <=40 words>"
}

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
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.'

for WAVE in code g1 g2 g3 g4 g5 g6; do
  DIFF=$(cat "$OUT/chunks/wave-$WAVE.diff")
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
  "evidence": "<the exact diff lines that prove the claim, pasted verbatim from the diff above. Use N/A only when the claim is about something genuinely absent from the diff (e.g. a missing test file). Paraphrased or reconstructed evidence is hallucination — drop the finding instead.>",
  "detail": "<=40 words>",
  "recommended_fix": "<=40 words>"
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
$(cat "$OUT/prompts/_briefs/$LENS.txt")

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
echo BUILT_OK; ls "$OUT/prompts" | wc -l
