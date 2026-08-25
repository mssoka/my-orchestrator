# Lens brief — ACCEPTANCE AUDITOR (source: `acceptance`) — Perkins round 4, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4/project-context.md first — the project's rules for agents (Odin + raylib; pure core ODN-1; integer-only sim paths ODN-10; arena discipline ODN-18; owned RNG ODN-9; events not callbacks ODN-14; render determinism §10.4: no transcendentals in the raster path, tick-anchored animations).

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r4 is checked out at exactly the reviewed state — verify against it. The diff's first file (_pr_body_spawn_feel.md) is the PR's own claims document — audit code against BOTH the briefing spec and those claims.

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md (the job briefing — this IS the spec).

--- ROUND CONTEXT (r4) ---
This is round 4. r1 blockers: B1 (highlight radius unit mix — claimed fixed to tile units) and B2 (vacuous pending-commands test — claimed reworked to a legal router place with anti-vacuity + negative legs). The PR rebased twice (#82 trail rings; #83 scale/shadows — sprite_blit merged with Shadow_Spec + tint). Audit whether the FIXES satisfy the review's demands and whether the rebase claims hold in the code. Settled rulings you must NOT re-litigate: the telegraph+reveal direction itself; the shadow-sim prediction living in the render package (documented accepted risk); the estate-r1 folds (jint_strict, bad-frees, diameter guard); aesthetic quality verdicts (deferred to human review).

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Briefing acceptance criteria to audit specifically:
1. "Spawn capture sequence (pre→pop) shows: telegraph ring → reveal scale/fade → pipe highlight; no instant pops" — is the mechanism present in the code, tick-anchored?
2. "Sim-validity timing unchanged (node becomes valid at the same tick); goldens re-blessed cause-documented if capture ticks shift" — view-layer only? Any sim-state write? LOG_VERSION/serialization untouched?
3. "Local suite green" (claimed 236/236 core, 22/22 render, 48/48 demos, 11/11 gates — you may spot-check but the orchestrator runs the suites).
4. Briefing rule 4 (cadence pacing signal) — documented as moot (4 s cadence); is the documentation honest?
5. PR-body claims that the code contradicts (e.g. the "Reduced-motion: ... the highlight steady" claim vs what spawn_fx_draw_highlight actually does under reduced_motion).

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. ac-violation, scope-drift, doc-contradiction>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r4/acceptance.json
An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
