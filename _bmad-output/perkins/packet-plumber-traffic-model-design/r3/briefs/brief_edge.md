# Lens brief — EDGE CASE HUNTER (mm-edge-r3) — Perkins round 3, PR #53

## Mechanics

- You are one lens in a headless review wave (Perkins round 3 — FINAL automated round, PR #53 — docs/canon). Work ALONE. Never ask questions; never wait for input. Make reasonable reads yourself and finish.
- Canonical diff (read it FIRST, review exactly these bytes, never re-fetch or regenerate): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/diff.patch` (unified, 1697 lines vs `v2` — 4 markdown canon docs + surge-explainer.html + 3 PNGs, all additions).
- The r2→r3 rework delta (454 lines — what changed since the r2-reviewed sha; useful fix-audit focus, NOT a substitute for the canonical diff): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/delta-r2-to-r3.patch`
- Verification worktree (read-only; detached at exactly the reviewed sha 42e4eb6 — trust it, not origin/v2): `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r3`
- Spec (the job's charter): `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md`
- Round-2 prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json`
- When done: write ONLY your JSON array to the output path in the OUTPUT CONTRACT section, then stop.

## PROJECT CONVENTIONS

- Repo: Packet Plumber — an internet-building puzzle game (Odin + raylib). This PR is a **design-canon docs PR**: spec + story cards + GDD amendment + decision-log entry + one committed provenance artifact (surge-explainer.html + 3 PNGs, the approved r1-W3 fix). **Scope guard: design docs + story cards ONLY — code, balance.json, and implementation are the story cards' jobs, NOT this PR's.** Demanding code/tests in this diff is out of scope; story CARDS pinning future tests is the canon pattern.
- Unit conventions (the game's own, endorsed): catalog `u/s` values are consumed **per tick** (u/tick); 20 Hz logic; `packet_bandwidth` = 30 u = one packet's transit work per hop; a terminal with throughput 5 serves 5/30 ≈ 0.167 pkts/tick. 1 u = one 1500-byte frame's transit work (the ~1,000× compression onto tiers 5/15/40 is deliberate and endorsed).
- Determinism spine: all rng from `state.rng`, seed-derived, no wall-clock; replay byte-identical [E10]; golden re-bless discipline (4.3) for legitimate catalog/spawn-stream shifts; derive-don't-record (derived state like `lane_caps` is never serialized; a serialized state home would be a LOG_VERSION question); **ODN-10 integer-only state paths** (odin-architecture-v1.md:398).
- Canon doc set: GDD `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` (+ decision-log.md, append-only), stories `_bmad-output/planning-artifacts/sprints/stories-v2.md`, sprint plan `.../sprint-plan-v2.md`, spec `_bmad-output/implementation-artifacts/spec-traffic-model.md`, architecture `.../architecture/architecture-v1.md` (§11.7 = the E# contract table).
- Coordination constraint: GDD edits must be SECTION-ADDITIVE (no terminology rewrites — the p1P8 terminology audit owns wording and serializes behind this PR).

## LENS-GUARDS — read before reporting (prevents false positives)

This is **round 3 of 3 — the FINAL automated round, a FIX-AUDIT on the r2 rework**. Round 2 (sha da3a50e) verdicted NEEDS CHANGES with 1 blocker + 6 warnings + 13 notes; this push (the single commit 42e4eb6) claims the blocker + all 6 warnings + notes N1/N5/N8/N9/N11 fixed. Prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (read it).

- **Fix-audit mandate:** where a claimed fix touches your lens, verify it BITES (re-read the cited code/docs in the worktree — do not trust the claims). Do NOT re-report a verified-fixed item as new. Report still-present items with `"still present since round 2"` in the detail, at their r2 severity.
- **Do NOT re-litigate (settled in r1/r2):** the ~1,000× unit compression (endorsed); the M1-vs-shipped tier discrepancy (acknowledged canon); committing the surge-explainer html/PNGs (approved provenance artifacts); slice-5B sequencing/numbering (ratified); card-format conventions; the u/s-vs-u/tick arithmetic convention (r2-rejected); "5.9 changes no catalog" (r2-rejected — balance.json folds catalog_hash).
- **NOT defects:** future-tense test pins in cards (cards dispatch later implementation PRs); the explainer artifact quoting its own superseded numbers (the spec brackets + supersedes them; r2 N11's provenance disclaimer is now added); terminology wording (the p1P8 audit's lane); integer-division truncation in the milli-credit accrual (at most 1 milli/tick — negligible and the ODN-10-blessed form).
- **Base = `v2`** — the diff is the full PR against v2; only the changed files are in scope. Prior-round notes that remain unfixed are carried forward as notes — do not escalate them to blockers.
- **Final-round precision:** a genuine BLOCKER = the canon text as written would mislead the implementing minion or breaks a hard contract (ODN-10 integer-only state, catalog-load fail-fast, E10 replay/derive-don't-record, a cited code seam that doesn't exist). Cosmetic/citation polish = note; a real but non-contract-breaking gap = warning.

## YOUR LENS

You are a pure path tracer. Do not comment on whether the design is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed text itself — no fixed checklist. Examples: arithmetic boundaries in the new milli-credit formulas (`accrue_milli = cap_fraction_permille × throughput_units ÷ packet_bandwidth` at every roster value in `data/node_types.json`; `MAX_CREDIT_MILLI(type) = 1000 × max(1, ceil(cap))` with `ceil(cap) = (accrue_milli + 999) ÷ 1000` — verify every derived number the text states: residential 83, content_host 1333, campus 150 u/s 2500/ceiling 3; can EVERY type actually achieve its cap long-run under the ceiling? what of a hypothetical type whose accrue_milli × 1000 barely exceeds its ceiling?); zero-throughput or not-yet-live terminals; the eligible set empty (all terminals credit-starved — where does the volume go?); a spec's volume exceeding total capped capacity; group-bias draw when no cluster member exists or the cluster is at cap; growth radius vs E31 packing; the SLA seam (skip-before-flow_try_spawn vs pool-drop) at the boundaries. Verify specified seams against the worktree code the canon cites (core/flow.odin §1a/§1b, flow_try_spawn E22, E9 admission, core/growth.odin E31, core/demand.odin).

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

## OUTPUT CONTRACT

Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. boundary, coupling, coverage-gap>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the exact lines you READ from the file/diff that prove the claim, pasted verbatim. Use 'N/A' ONLY for findings that have no possible code reference. Do not paraphrase. Do not reconstruct from memory. If you cannot quote the lines, you have not done the work to file the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}

- Write ONLY the JSON array to your assigned output path (below) — no prose around it in the file — then STOP.
- Empty array `[]` is valid and expected when you find nothing. Do not invent findings to fill a quota.

ACCURACY MANDATE — the most important instruction in this brief:

NO claim you make will be taken at face value. Every finding will be independently re-verified against the actual codebase before it reaches the report. Findings that fail verification are DISCARDED SILENTLY.

- Open the file. Read the relevant lines. Do not guess from filenames, do not assume from similar-looking code, do not generalise from one example to another.
- The `evidence` field must contain the EXACT lines you read. A finding without locatable evidence is a hallucination — drop it before it leaves your output.
- Hedging language ("might", "could", "possibly") signals you have not verified. Either verify and report crisply, or do not report.
- Prefer fewer, well-grounded findings over many speculative ones. An empty array is an honest answer.

Your output path: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/edge.json`
