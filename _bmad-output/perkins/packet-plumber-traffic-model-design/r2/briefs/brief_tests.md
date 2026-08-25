# Lens brief — TEST COVERAGE (mm-tests-r2) — Perkins round 2, PR #53

## Mechanics

- You are one lens in a headless review wave (Perkins round 2, PR #53 — docs/canon). Work ALONE. Never ask questions; never wait for input. Make reasonable reads yourself and finish.
- Canonical diff (read it FIRST, review exactly these bytes, never re-fetch or regenerate): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/diff.patch` (unified, 1620 lines — 5 markdown docs + surge-explainer.html + 3 PNGs, all additions).
- Verification worktree (read-only; detached at exactly the reviewed sha da3a50e — trust it, not origin/v2): `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r2`
- Spec (the job's charter): `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md`
- Round-1 prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r1/consolidated.json`
- When done: write ONLY your JSON array to the output path in the OUTPUT CONTRACT section, then stop.

## PROJECT CONVENTIONS

- Repo: Packet Plumber — an internet-building puzzle game (Odin + raylib). This PR is a **design-canon docs PR**: spec + story cards + GDD amendment + decision-log entry + one committed provenance artifact (surge-explainer.html + 3 PNGs, the approved r1-W3 fix). **Scope guard: design docs + story cards ONLY — code, balance.json, and implementation are the story cards' jobs, NOT this PR's.** Demanding code/tests in this diff is out of scope; story CARDS pinning future tests is the canon pattern.
- Unit conventions (the game's own, endorsed): catalog `u/s` values are consumed **per tick** (u/tick); 20 Hz logic; `packet_bandwidth` = 30 u = one packet's transit work per hop; a terminal with throughput 5 serves 5/30 ≈ 0.167 pkts/tick. 1 u = one 1500-byte frame's transit work (the ~1,000× compression onto tiers 5/15/40 is deliberate and endorsed).
- Determinism spine: all rng from `state.rng`, seed-derived, no wall-clock; replay byte-identical [E10]; golden re-bless discipline (4.3) for legitimate catalog/spawn-stream shifts; derive-don't-record (derived state like `lane_caps` is never serialized; a serialized state home would be a LOG_VERSION question).
- Canon doc set: GDD `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` (+ decision-log.md, append-only), stories `_bmad-output/planning-artifacts/sprints/stories-v2.md`, sprint plan `.../sprint-plan-v2.md`, spec `_bmad-output/implementation-artifacts/spec-traffic-model.md`, architecture `.../architecture/architecture-v1.md` (§11.7 = the E# contract table).
- Coordination constraint: GDD edits must be SECTION-ADDITIVE (no terminology rewrites — the p1P8 terminology audit owns wording and serializes behind this PR).

## LENS-GUARDS — read before reporting (prevents false positives)

This is **round 2 — a FIX-AUDIT re-review**. Round 1 (sha 7214204) verdicted NEEDS CHANGES with 2 blockers + 9 warnings; this push claims every blocker/warning fixed. Prior findings live at `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r1/consolidated.json` (read it).

- **Fix-audit mandate:** where a claimed fix touches your lens, verify it BITES (re-read the cited code/docs in the worktree — do not trust the claims). Do NOT re-report a verified-fixed item as new. Report still-present items as `"still present since round 1"` in the detail.
- **Do NOT re-litigate (settled):** the ~1,000× unit compression (endorsed); the M1-vs-shipped tier discrepancy itself (r1 W4 — the fix adds the reconciliation sentence; the discrepancy is acknowledged canon); committing the surge-explainer html/PNGs (the approved W3 fix — binaries as provenance artifacts are in-scope here); slice-5B sequencing/numbering choices (ratified); card-format conventions.
- **NOT defects:** future-tense test pins in cards (cards dispatch later implementation PRs); the explainer artifact quoting its own superseded numbers (0.2 pkts/tick) — the spec brackets them as "[Perkins r1 B2 — the operative value is NOT the explainer's 0.2...]" and supersedes; "access" flavor wording being deferred to the terminology audit (explicitly its lane).
- **Base = `v2`** — the diff is the full PR against v2; only the changed files are in scope. Prior-round notes that remain unfixed are carried forward as notes — do not escalate them to blockers.

## YOUR LENS

Test coverage analysis via traceability. This is a docs/canon PR: the "tests" are the pins the story CARDS specify for their future implementation PRs, plus the existing pinned tests the cards claim to preserve. Trace each specified behavior change in the cards (5.9 accumulator + SLA seam + surge-lands pin + one-subscriber-at-cap pin; 5.10 re-bless + headroom; 5.11 T2 all-three-types frame + catalog fold; 5.12 clustered-topology-under-surge frame) to a pinned test or golden named in the card, and to any EXISTING test in the worktree it extends or must not break (core/demand_test.odin volume pins, core/sla_test.odin sla_check_invariant, goldens/). Classify FULL / PARTIAL / NONE. Severity: blocker = P0 gap (critical path, happy + core error) OR P1 coverage <80%; warning = P1 80–89% OR P2; note = P3. Docs-PR context: a card specifying its pin is FULL coverage at the design level; a card whose load-bearing acceptance has NO named pin (re-bless only) is the gap class r1 flagged (W9/W10/W11) — verify those pins now exist and are real assertions, not prose.

Finally, emit ONE advisory-gate finding: title "Advisory test gate: PASS|CONCERNS|FAIL", category "coverage-gate", severity note|warning|blocker respectively, detail with coverage percentages. Gate: PASS = P0 100%, P1 ≥90%; CONCERNS = P1 80–89%; FAIL = P0 <100% or P1 <80%.
## OUTPUT CONTRACT

Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "tests",
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

Your output path: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/tests.json`
