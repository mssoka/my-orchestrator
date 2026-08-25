# Lens task — CODEBASE FIT (source: codebase) — round 2

You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools. Your cwd IS the repository worktree at exactly the reviewed state (PR #94 head 1cb1b4b, base v2) — verify against it, not against any other checkout.

--- PROJECT CONVENTIONS ---
Read project-context.md in the worktree root (the project's conventions file) and apply it.

--- DIFF ---
The canonical diff (review EXACTLY these bytes — read it first, in full):
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-network-units/r2/diff.patch
(unified diff, 1245 lines, 15 files)

--- SPEC / CONTEXT ---
The binding spec (the original job briefing — read it IN FULL; it is short and every line is load-bearing):
/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-network-units.md
There is NO GitHub issue — the job briefing IS the spec. The PR also carries its own implementation-spec artifact (`_bmad-output/implementation-artifacts/spec-packet-plumber-v2-network-units.md`, included in the diff as a new file) — that artifact is the IMPLEMENTATION's own plan, NOT the binding spec; deviations between it and the job briefing above are exactly what you must audit.

--- ROUND CONTEXT (round 2 fix-audit — binding) ---
This is ROUND 2 of this PR's review. Round 1 (@48c0e82) filed findings; the author pushed fix commit 1cb1b4b (top commit in this diff) claiming to address them. The diff you review is the FULL PR diff including that fix commit.

Prior-round findings ALREADY FILED (do NOT re-file as new unless the FIX itself is defective):
- B1 (blocker): NOC queue-row right-aligned util% glyph-collided the Best-effort lane's queue-count digit. Fix claims: lane pitch 108->104, bar 70->64, util anchor reserve 96->82 (util_r px+416), 12 px clearance, KYLE re-read.
- W1: tier line rates derive to 67/100/267 Mbps rather than the briefing's nominal 10/100/1000 ladder (a single SIM_TIME_SCALE makes the nominal ladder unsatisfiable without pace drift). HELD for a user ruling — UNTOUCHED by design. Do NOT re-file.
- W2: tx-ring window semantics (expiry boundary, slot reuse, rebuild reset, defensive bounds) had no direct tests. Fix claims bundles_test additions.
- W3: noc_pipe_rows predicate swap (carried>=cap -> util_pct>=red) had no discriminating test. Fix claims an 89/90-boundary + cap-0 pin and an amber-boundary pin for noc_queue_rows.
- W4: advisory test gate CONCERNS (derivative of W2/W3).
- N1-N12 notes: zero-cap -> ~800 Mbps defensive inversion; stale 96px comments; hardcoded 90/6/512 section headers; stats stream marker v1 despite the 18th column; impossible CSV fixture pair (util 100 / tx 0); untested bps formatter tiers; dead line_rate_bytes_per_tick; same-tick re-step accumulation comment; node-health pct semantics; sim warnings queue-keyed; Bundles struct doc drift.

NOT defects — do NOT file these (standing rulings):
- The user ruling to use real networking terms, and the utilization-bug fix itself (queue-occupancy masquerading as utilization WAS a bug).
- The MM-pace feel hard constraint (byte-identical golden timing) — its preservation is required, not a defect.
- E9/E22 bounds unchanged (6 packets / 512 pool) — required, not a defect.
- The derived 67/100/267 Mbps ladder (W1 — held for the user).
- The GitHub-CI billing-block state — environmental, not this PR.

--- YOUR LENS ---
Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Round-2 codebase focus: the fix commit's geometry claims are FONT-METRIC claims — verify the re-anchor math yourself from the code constants (NOC_PANEL_W = 360*140/100, lane pitch 104, bar 64, util reserve 82, count at bx+22+64+4) and assets/fonts/ibm_plex_mono_regular.ttf advance semantics (raylib MeasureTextEx at size 18) if you can; confirm the fix commit's own comment numbers ([px+351.2, px+359.6] count ink; ~px+372.8 util first glyph; 12 px clearance) are internally consistent with the code constants. Also: every noc_panel_rows/noc_queue_rows caller updated for the new amber_pct parameter; line_rate_bytes_per_tick fully unreferenced after removal; the PR-body r2-fold header's sha reference (8a6f3f5) — does that object exist in git?

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
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

FILE-OUTPUT CONTRACT (headless override — authoritative): do NOT print the JSON as your reply. Write ONLY the JSON array (no prose, no markdown fencing) to EXACTLY this absolute path with your write tool, then stop:
/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-network-units/r2/codebase.json

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
