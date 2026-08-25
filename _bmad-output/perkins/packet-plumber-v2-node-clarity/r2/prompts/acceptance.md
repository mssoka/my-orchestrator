You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
Read `/Users/moses/.herdr/worktrees/packet-plumber/perkins-packet-plumber-v2-node-clarity-r2/project-context.md` — that file's content IS the PROJECT CONVENTIONS block below.

--- DIFF ---
The diff under review is the exact bytes of `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r2/diff.patch` — read that file; its content IS the DIFF block. (1257 lines, unified format. The long `goldens/**` section is binary PNG re-blesses — expected and documented in the spec/PR body; judge the text hunks on their merits.)

--- SPEC / CONTEXT ---
Read these two files; together their content IS the SPEC / CONTEXT block:
1. `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-node-clarity.md` — the job briefing (THE spec: task, hard rules, acceptance).
2. `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r2/pr-body.md` — the PR body (the implementer's claims, the documented deviations D1–D7, and the "Rebase follow-up (r2)" section).

--- ROUND CONTEXT (r2 — rebase-delta fix-audit) ---
Round 1 reviewed this PR's substance (hue families, chips, tier markers) and APPROVED it (0 blockers, 5 warnings, 12 notes). Since then PR #77 (v2-network-pop) MERGED to the base first; this branch rebased onto the merged v2, resolved the palette `_comment` conflict keeping BOTH PRs' notes on one line, and re-blessed all 45 goldens under the COMBINED palette (commit 28be432, cause-documented in the PR body's "Rebase follow-up" section). The diff you review is the FULL PR vs the #77-merged base.

NOT re-litigatable (user rulings / r1 approvals — do not flag these as findings):
- The hue-family separation + chips + tier markers direction itself; the blur-gate ≥ 15° acceptance bar.
- The tuned anchors D2 (campus #A87250) and D3 (small_biz #6E9B74) — documented honest deviations, gate-driven.
- The 45-demo T2 re-bless being deliberate and cause-documented.
- The wash-at-draw-time approach (D1) and chips-skip-under-health-ring (D5).

The r2 review questions (frame your lens around them): (a) is the rebase onto the #77-merged base clean — both PRs' content kept, no token-key collisions (#77 owns router_led/pipe_*/packet_*/lane_*; this PR only ADDS *_family/router_tier_* keys)? (b) is the combined-palette re-bless sound — T1/spine byte-identity (the diff must contain ZERO .t1/.log.bin hunks) and the claimed blur-gate numbers unchanged (min pair 22.6°, sat band 0.289)? (c) any NEW issue introduced by the rebase or the second re-bless? Prior-round findings are carried forward separately by the orchestrator — your job is the current state, fresh eyes.

--- YOUR LENS ---
Audit the diff against the spec and context docs above. Identify:
- Violations of specific acceptance criteria
- Deviations from spec intent
- Missing implementation of specified behavior
- Contradictions between spec constraints and actual code
- Scope drift — changes not asked for by the spec

For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

Notes binding this audit:
- The spec's hard rule 1 says palette tokens + draw layer only — no geometry, no sim. Verify mechanically (the diff must not touch geometry, sim semantics, serialization, LOG_VERSION, or packet contracts).
- The spec's anchor hexes were explicitly allowed to be tuned by the documented deviations D2/D3 in the PR body (same hue family, tuned hex, gate-driven). Verify the DEVIATION TEXT matches the code (tokens in data/palette.json vs the hexes the PR body claims); do NOT re-litigate the anchor tuning itself.
- The blur-test gate (σ6, ≥15° pairwise, sat band ≤0.30) IS the acceptance — the PR body's r2 section claims the numbers are UNCHANGED after the rebase (min pair 22.6°, band 0.289 — #77's vivid pipes must not shift the σ6 node samples). You may run `python3 tools/blur_gate.py goldens/terminal_types/05000ms.png` from the worktree root to check the claim mechanically (if the environment lacks PIL or it fails to run, report the claim as unverified-by-you, not as a finding).
- The PR body's "Rebase follow-up (r2)" section makes specific claims — audit EACH against the diff + worktree: the `_comment` resolution keeps BOTH PRs' notes (read data/palette.json's actual `_comment`); token additions are additions-only (no pre-existing token value changed by THIS diff); the LED pin survival claim (#77's router_led [0,205,90] "drives the fallback draw path only" — check where p.router_led is read in app/render/view.odin and whether the sprite path bakes LEDs instead); "a11y mode tables remain byte-untouched on both sides" (the a11y GOLDEN PNGs change because the scene changed — the claim is about the palette.json `modes` tables; verify no modes-table hunks in the diff).
- Scope-drift: the `.memlog.md` + `_bmad-output/pr-bodies/**` hunks are job bookkeeping; the `tools/__pycache__/*.pyc` deletion is stray hygiene. Judge these on the spec's "palette tokens + draw layer only" rule as applied to SHIPPED code paths.

--- OUTPUT ---
Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. auth, boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference (e.g. a missing-spec concern). Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

Output contract:
- Write your JSON array to the file `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-node-clarity/r2/acceptance.json` — that file must contain ONLY the JSON array (no prose, no markdown fencing, no preamble). Then reply with one short line confirming the write, and stop.
- Empty array `[]` is valid and expected when you find nothing.
- Do not invent findings to fill a quota.

ACCURACY MANDATE — this is the most important instruction in this prompt:

NO claim you make will be taken at face value. Every finding you emit will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY — they will not appear in the report, you will not be asked to defend them, you get no second chance.

Therefore:
- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. If you cannot paste them, you have not verified the issue and the finding does not belong in your output. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly", "potentially") is a signal that you have not actually verified the issue. Either verify it and report it crisply, or do not report it.
- Prefer fewer, well-grounded findings over many speculative ones. The user values accuracy over volume — an empty array is a fine and honest answer when nothing is wrong.
