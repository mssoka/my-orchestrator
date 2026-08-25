# Lens brief — ACCEPTANCE AUDITOR (source: `acceptance`) — Perkins round 1, packet-plumber-v2-spawn-feel

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1/project-context.md first — the project's rules for agents (Odin + raylib; pure core ODN-1; integer-only sim paths ODN-10; arena discipline ODN-18; owned RNG ODN-9; events not callbacks ODN-14; render determinism §10.4).

--- DIFF ---
Read the canonical diff (the exact change under review):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/diff.patch
The repo at /Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-spawn-feel-r1 is checked out at exactly the reviewed state — verify against it. Note: the diff includes `_pr_body_spawn_feel.md` (the PR's own body — its claims are part of what you audit).

--- SPEC / CONTEXT ---
Read /Users/moses/code/_bmad-output/briefings/packet-plumber-v2-spawn-feel.md — the job briefing. This IS the spec (no GitHub issue). Its hard rules: (1) view-layer ONLY — no sim-state writes, sim-validity timing unchanged; (2) tick-anchored for T2 stability — animations are pure functions of (tick, effect state), goldens re-blessed cause-documented if capture ticks shift; (3) rate is out of scope; (4) MM model: the reveal is a moment, not a cutscene.

STANDING RULINGS (spec amendments — do NOT file findings against these; audit that they landed, not whether they should exist):
- The estate-r1 folds are IN SCOPE of this job per the wave plan: `core/catalog.odin` `new_area_seed_tiles` parsing `jint_strict` (+ decimal rejection test), the `strict_spawn_class` bad-free `defer delete` removals in `core/growth_test.odin`, and the diameter guard tightened to `(w-1)²+(h-1)²` (+ boundary-48 accept row, 49/50/51 reject rows). These are deliberate follow-up folds relayed via the orchestrator.
- Briefing item 4 (cadence-pacing variation) was conditional — "if the 2 s cadence stays". The pace-tuning job landed first and the cadence is now 4 s (80 ticks), so non-implementation is spec-compliant, not scope drift.
- The visual AESTHETIC verdict is deferred to the human review (vision model rate-limited; noted in the PR body). Aesthetic quality is OUT of scope for this audit — verify mechanics and acceptance criteria, not beauty.
- 2 pre-existing bad-frees in `core/health_test.odin` are explicitly out of scope (noted in the PR body).

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Key ACs to audit mechanically against the actual code (do not trust the PR body's claims):
- "Spawn capture sequence (pre→pop) shows: telegraph ring → reveal scale/fade → pipe highlight; no instant pops" — does demos/spawn_feel.dem's capture list actually cover a pre→pop→settle sequence, and does the render wiring draw all three effects?
- "Sim-validity timing unchanged (node becomes valid at the same tick)" — verify no core/sim write path changed: does anything in app/render/spawn_fx.odin write to the live Run_State, or does the shadow stay isolated? Does core/step behavior change at all (the only core/ changes are catalog parsing + a test helper)?
- "View-layer ONLY — the reveal must not write to sim state" — trace every call the render code makes into core.
- "Tick-anchored for T2 stability" — is every animation a pure function of (tick, effect state)? Any wall-clock/time-based input into the effects?
- "goldens re-blessed cause-documented if capture ticks shift" — the node_health 20000ms.png re-bless: is the cause story (capture tick lands on a growth window) consistent with node_health.dem's capture ticks? Is the claimed no-re-bless for growth 88000ms consistent (t1760 window rejected → no spawn)?
- Serialization unchanged: LOG_VERSION / event-stream format untouched?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. ac-violation, scope-drift>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words — quote the violated spec phrase>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract: write ONLY the JSON array (no prose, no markdown fencing, no preamble) to this EXACT absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-spawn-feel/r1/acceptance.json
An empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota. Then stop — do not wait for input.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
