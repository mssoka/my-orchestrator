You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Do NOT modify any file in the repository.

--- PROJECT CONVENTIONS ---
Read /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.8-qos-panel-r1/project-context.md (project conventions). Key invariants you must honor in judgment: `core/` is pure — imports only whitelisted `core:*` packages, never `vendor:*`, never `core:os`, never `core:time` (ODN-1); the sim steps only via `core.step`; integer-only sim math, floats only in the view (ODN-10); never iterate a map in core — arrays/slices only, maps lookup-only (ODN-9/10); RNG owned by Run_State (ODN-9); arena discipline (ODN-18); determinism is the project spine.

--- DIFF ---
Read the canonical diff FIRST and IN FULL: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/lens-diff.patch (2599 lines, unified format, PR #50 of solarity-services/Packet-Plumber, base branch v2). These exact bytes are the review target — never re-fetch or regenerate the diff. The PR also re-blessed goldens; their summarized surface is at /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/golden-manifest.txt (the full binary diff is Perkins-verified mechanically — do not re-derive it).

--- WORKTREE (your verification source) ---
/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.8-qos-panel-r1 — a checkout at exactly the reviewed sha (ea1026d7fd67667bca6e576baada50f7ecba1d46). Every verification read happens here. Trust this checkout, not origin/v2.

--- SPEC / CONTEXT ---
- Job briefing (the spec): /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/spec/job-briefing.md — note especially the Mission (the user-ruled design points 1-6), the numbered Acceptance criteria (1-7) and the Scope guard.
- Story 5.8 card: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/spec/stories-v2.md — the section "### Story 5.8 — QoS panel + assignment-driven auto-reservation" (~line 604).
- Architecture canon: /Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/spec/odin-architecture-v1.md — ODN-3 QoS decision + player surface (~line 474), §6.3 S3 QoS lane model (~line 1008), the E-contract glossary table (~line 1620-1640: E5 all-zero-weights default, E6 never-drop, E7 WRR floor, E8 largest-remainder, E9 drop ladder, E10 replay determinism).
- Implementation spec committed in the PR: /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.8-qos-panel-r1/_bmad-output/implementation-artifacts/spec-5-8-qos-panel.md (also visible in the diff).
--- LENS-GUARDS (dispatching orchestrator's rulings — prevents false positives; honor them) ---
- [LOAD-BEARING] Serialization + replay equality [E10]: the Cmd_Set_Emphasis payload evolution (preset u16 → weights [3]i32, SAME serialized tag, LOG_VERSION 3→4) must hold replay equality BY CONSTRUCTION — the auto-ladder and the manual editor both write through the ONE command; a v3 log must be rejected by the v4 reader. Any divergence between live and replay = a blocker.
- [LOAD-BEARING] The golden fold is Perkins-verified mechanical (byte-level): pre-existing .log.bin differ only at the version byte + catalog_hash; qos_emphasis.log.bin record bytes are exactly the documented payload evolution with preset→weights equivalence; all pre-existing PNGs byte-identical. Do not re-derive; flag only code paths that could hide semantic drift in a FUTURE re-bless.
- Ladder semantics exact: in-play lanes = assigned lanes ∪ Standard (Standard always reserved, canon-safe); streaming→Express alone = 70/30; + email→Best-effort = exactly 50/30/20; untouched pipes keep the default preset (no-QoS goldens byte-stable). A wrong split or a Standard-lane regression = a blocker.
- Never-drop safety: E6 — future non-Standard defaults can't break the auto path (never-drop by construction); no cycle deadlock on zeroed lanes. Verify both.
- Manual editor: presets + ±5 nudges, derived AUTO/MANUAL mode, revert-to-auto; the silent manual-tune clobber on lane assignment is gated on the pre-edit derived mode.
- Base = v2 — includes 5.3 pause + 5.3-pause-ux + 5.7 telemetry (5.7 touched app/main.odin emission/overlay paths). Carry-forward only; do NOT re-open settled findings.
- Scope guard: QoS panel + auto-reservation + the payload evolution ONLY — no new command kinds, no unrelated gameplay changes, nothing 5.7-telemetry or 5.3-pause owns.
--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Audit map (walk every AC; cite evidence from the worktree, not just the diff):
1. AC1 (panel + immediate split update): app/qos_panel.odin per-type rows, click-to-cycle + 1/2 class select + E/S/B lane assign; split shown with real numbers + bars; assigning updates the split immediately per the ladder.
2. AC2 (manual override): per-pipe weight edit (presets + ±5 nudges), manual pipes marked, revert-to-auto works.
3. AC3 (visual + serialization): lane widths on the pipe visual reflect the split (app/render code); node serialization (Express → Standard → Best-effort) uses the split (core).
4. AC4 (replay equality [E10]): one command path (Cmd_Set_Emphasis) for auto + manual; replay gate.
5. AC5 (goldens): no-QoS goldens byte-stable (Perkins-verified — do not re-derive); new T2 goldens for a 3-lane 50/30/20 assignment (qos_auto) + a manual-override pipe (qos_manual 60/25/15).
6. AC6 (full local suite green): Perkins is re-running the suite — do not run it yourself; audit test/demon coverage instead.
7. AC7 (PR body carries the story card + the [ASSUMPTION] notes): the PR body is in the diff at _bmad-output/reviews/5.8-qos-panel/pr-body.md — verify it carries the story 5.8 card content and the [ASSUMPTION] notes the briefing demands (harder-era gating documented as FUTURE, not built).
Also audit the two lavish-approved rulings: (a) payload evolution — preset u16 → weights [3]i32, SAME tag, LOG_VERSION 3→4, ONE command for auto + manual; NOT a new command kind; (b) ladder semantics — in-play = assigned ∪ Standard; 70/30; 50/30/20 exactly; untouched pipes keep the default preset.
Also verify the briefing's documented choice: right-click dial retired → right-click selects the pipe (documented in the PR body / implementation spec).
The canon amend (GDD M2 + ODN-3 + balance.json fields) was ALREADY on v2 pre-PR (commit 5f51236) — its absence from this diff is correct, NOT scope drift. Your `source` value is "acceptance".

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "<one of: blind | edge | acceptance | security | architecture | codebase | tests — use the value assigned to you>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Return ONLY the JSON array. No prose, no markdown fencing, no preamble.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.

FILE-OUTPUT CONTRACT (headless mode): using your file-write tool, write ONLY your JSON array (valid JSON, no prose, no markdown fencing, no preamble) to exactly this absolute path:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.8-qos-panel/r1/acceptance.json
Do not derive or guess another path — that exact path, that exact filename. After writing the file, stop. Your final message must be one line: "lens acceptance complete — N findings written".
