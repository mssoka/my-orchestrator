# Lens brief — TEST COVERAGE (mm-tests-r3) — Perkins round 3, PR #53

## Mechanics

- You are one lens in a headless review wave (Perkins round 3 — FINAL automated round, PR #53 — docs/canon). Work ALONE. Never ask questions; never wait for input. Make reasonable reads yourself and finish.
- Canonical diff (read it FIRST, review exactly these bytes, never re-fetch or regenerate): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/diff.patch` (unified, 1697 lines vs `v2` — 4 markdown canon docs + surge-explainer.html + 3 PNGs, all additions).
- The r2→r3 rework delta (454 lines — what changed since the r2-reviewed sha; useful fix-audit focus, NOT a substitute for the canonical diff): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/delta-r2-to-r3.patch`
- Verification worktree (read-only; detached at exactly the reviewed sha 42e4eb6 — trust it, not origin/v2): `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r3`
- Spec (the job's charter): `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md`
- Round-2 prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (your r2 warnings W6-quantitative-pins and W7-re-pin-surface are the round's claimed fixes)
- When done: write ONLY your JSON array to the output path in the OUTPUT CONTRACT section, then stop.

## PROJECT CONVENTIONS

- Repo: Packet Plumber — an internet-building puzzle game (Odin + raylib). This PR is a **design-canon docs PR**: spec + story cards + GDD amendment + decision-log entry + one committed provenance artifact (surge-explainer.html + 3 PNGs, the approved r1-W3 fix). **Scope guard: design docs + story cards ONLY — code, balance.json, and implementation are the story cards' jobs, NOT this PR's.** Demanding code/tests in this diff is out of scope; story CARDS pinning future tests is the canon pattern.
- Unit conventions (the game's own, endorsed): catalog `u/s` values are consumed **per tick** (u/tick); 20 Hz logic; `packet_bandwidth` = 30 u = one packet's transit work per hop; a terminal with throughput 5 serves 5/30 ≈ 0.167 pkts/tick. 1 u = one 1500-byte frame's transit work (the ~1,000× compression onto tiers 5/15/40 is deliberate and endorsed).
- Determinism spine: all rng from `state.rng`, seed-derived, no wall-clock; replay byte-identical [E10]; golden re-bless discipline (4.3); derive-don't-record; **ODN-10 integer-only state paths**.
- Canon doc set: GDD `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` (+ decision-log.md, append-only), stories `_bmad-output/planning-artifacts/sprints/stories-v2.md`, sprint plan `.../sprint-plan-v2.md`, spec `_bmad-output/implementation-artifacts/spec-traffic-model.md`, architecture `.../architecture/architecture-v1.md` (§11.7 = the E# contract table).
- Coordination constraint: GDD edits must be SECTION-ADDITIVE (no terminology rewrites — the p1P8 terminology audit owns wording and serializes behind this PR).

## LENS-GUARDS — read before reporting (prevents false positives)

This is **round 3 of 3 — the FINAL automated round, a FIX-AUDIT on the r2 rework**. Round 2 (sha da3a50e) verdicted NEEDS CHANGES with 1 blocker + 6 warnings + 13 notes; this push (the single commit 42e4eb6) claims the blocker + all 6 warnings + notes N1/N5/N8/N9/N11 fixed. Prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (read it).

- **Fix-audit mandate — YOUR r2 findings are the headline claims:** W6 (pins quantitative) and W7 (re-pin surface named). Verify they BITE: W9/W10 pins must state real quantitative assertions (rate envelopes on a known seed: surge volume ≥ 0.95 × expected, per-terminal spawns ≤ cap × window + burst allowance, credit ≤ MAX_CREDIT) — not prose; W7 must name the actual unit-test surface (`core/demand_test.odin` volume + spawn-histogram pins incl. the `effective_volume` surge pin, `core/flow_test.odin` per-spec spawn counts, `core/determinism_test.odin` byte-identical replay) with positive + negative assertions — verify those test files EXIST in the worktree and contain the pins the card claims to re-pin (e.g. does demand_test.odin actually carry exact volume pins + an effective_volume surge pin? does sla_test.odin:88 carry sla_check_invariant?).
- Do NOT re-report a verified-fixed item as new. Report still-present items with `"still present since round 2"` in the detail, at their r2 severity.
- **Do NOT re-litigate (settled in r1/r2):** the ~1,000× unit compression; the M1-vs-shipped tier discrepancy; committing the surge-explainer html/PNGs; slice-5B sequencing/numbering; card-format conventions; the u/s-vs-u/tick arithmetic (r2-rejected); "5.9 changes no catalog" (r2-rejected).
- **NOT defects:** future-tense test pins in cards (cards dispatch later implementation PRs — this PR's job is to NAME the pins); the explainer artifact's superseded numbers; terminology wording; integer-division truncation in the accrual (≤1 milli/tick, negligible).
- **Base = `v2`** — the diff is the full PR against v2. Prior-round notes that remain unfixed are carried forward as notes — do not escalate them to blockers.
- **Final-round precision:** a genuine BLOCKER = a load-bearing acceptance with NO named pin at the design level (the r1 W9/W10 gap class) or a card pointing at a test surface that doesn't exist. Cosmetic/citation polish = note; a real but non-load-bearing gap = warning.

## YOUR LENS

Test coverage analysis via traceability. This is a docs/canon PR: the "tests" are the pins the story CARDS specify for their future implementation PRs, plus the existing pinned tests the cards claim to preserve or re-pin. Trace each specified behavior change in the cards (5.9 milli-credit accumulator + SLA seam + quantitative W9/W10 pins + unit-test re-pin surface; 5.10 re-bless + headroom; 5.11 T2 all-three-types frame + catalog fold; 5.12 clustered-topology-under-surge frame) to a pinned test or golden named in the card, and to any EXISTING test in the worktree it extends, must not break, or must re-pin (core/demand_test.odin volume pins, core/flow_test.odin, core/sla_test.odin sla_check_invariant, core/determinism_test.odin, goldens/). Classify FULL / PARTIAL / NONE. Severity: blocker = P0 gap (critical path, happy + core error) OR P1 coverage <80%; warning = P1 80–89% OR P2; note = P3. Docs-PR context: a card specifying its pin is FULL coverage at the design level.

Finally, emit ONE advisory-gate finding: title `Advisory test gate: PASS|CONCERNS|FAIL`, category "coverage-gate", severity note|warning|blocker respectively, detail with coverage percentages. Gate: PASS = P0 100%, P1 ≥90%; CONCERNS = P1 80–89%; FAIL = P0 <100% or P1 <80%.

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

Your output path: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/tests.json`
