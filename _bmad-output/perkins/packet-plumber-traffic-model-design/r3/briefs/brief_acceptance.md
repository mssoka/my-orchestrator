# Lens brief — ACCEPTANCE AUDITOR (mm-acceptance-r3) — Perkins round 3, PR #53

## Mechanics

- You are one lens in a headless review wave (Perkins round 3 — FINAL automated round, PR #53 — docs/canon). Work ALONE. Never ask questions; never wait for input. Make reasonable reads yourself and finish.
- Canonical diff (read it FIRST, review exactly these bytes, never re-fetch or regenerate): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/diff.patch` (unified, 1697 lines vs `v2` — 4 markdown canon docs + surge-explainer.html + 3 PNGs, all additions).
- The r2→r3 rework delta (454 lines — what changed since the r2-reviewed sha; the fix-audit's primary focus, NOT a substitute for the canonical diff): `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/delta-r2-to-r3.patch`
- Verification worktree (read-only; detached at exactly the reviewed sha 42e4eb6 — trust it, not origin/v2): `/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-traffic-model-design-r3`
- Spec (the job's charter): `/Users/moses/code/_bmad-output/briefings/packet-plumber-traffic-model-design.md`
- Round-2 prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json`
- When done: write ONLY your JSON array to the output path in the OUTPUT CONTRACT section, then stop.

## PROJECT CONVENTIONS

- Repo: Packet Plumber — an internet-building puzzle game (Odin + raylib). This PR is a **design-canon docs PR**: spec + story cards + GDD amendment + decision-log entry + one committed provenance artifact (surge-explainer.html + 3 PNGs, the approved r1-W3 fix). **Scope guard: design docs + story cards ONLY — code, balance.json, and implementation are the story cards' jobs, NOT this PR's.** Demanding code/tests in this diff is out of scope; story CARDS pinning future tests is the canon pattern.
- Unit conventions (the game's own, endorsed): catalog `u/s` values are consumed **per tick** (u/tick); 20 Hz logic; `packet_bandwidth` = 30 u = one packet's transit work per hop; a terminal with throughput 5 serves 5/30 ≈ 0.167 pkts/tick. 1 u = one 1500-byte frame's transit work (the ~1,000× compression onto tiers 5/15/40 is deliberate and endorsed).
- Determinism spine: all rng from `state.rng`, seed-derived, no wall-clock; replay byte-identical [E10]; golden re-bless discipline (4.3); derive-don't-record (derived state like `lane_caps` is never serialized; a serialized state home would be a LOG_VERSION question); **ODN-10 integer-only state paths** (odin-architecture-v1.md:398).
- Canon doc set: GDD `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` (+ decision-log.md, append-only), stories `_bmad-output/planning-artifacts/sprints/stories-v2.md`, sprint plan `.../sprint-plan-v2.md`, spec `_bmad-output/implementation-artifacts/spec-traffic-model.md`, architecture `.../architecture/architecture-v1.md` (§11.7 = the E# contract table).
- Coordination constraint: GDD edits must be SECTION-ADDITIVE (no terminology rewrites — the p1P8 terminology audit owns wording and serializes behind this PR).

## LENS-GUARDS — read before reporting (prevents false positives)

This is **round 3 of 3 — the FINAL automated round, a FIX-AUDIT on the r2 rework**. Round 2 (sha da3a50e) verdicted NEEDS CHANGES with 1 blocker + 6 warnings + 13 notes; this push (the single commit 42e4eb6) claims the blocker + all 6 warnings + notes N1/N5/N8/N9/N11 fixed. Prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (read it).

- **Fix-audit mandate:** verify each claimed fix BITES (re-read the cited locations in the worktree at 42e4eb6 — do not trust the claims). Do NOT re-report a verified-fixed item as new. Report still-present items with `"still present since round 2"` in the detail, at their r2 severity.
- **Do NOT re-litigate (settled in r1/r2):** the ~1,000× unit compression (endorsed); the M1-vs-shipped tier discrepancy (acknowledged canon); committing the surge-explainer html/PNGs (approved provenance artifacts); slice-5B sequencing/numbering (ratified); card-format conventions; the u/s-vs-u/tick arithmetic convention (r2-rejected); "5.9 changes no catalog" (r2-rejected — balance.json folds catalog_hash).
- **NOT defects:** future-tense test pins in cards; the explainer artifact quoting its own superseded numbers (spec brackets + supersedes; provenance disclaimer added); terminology wording (p1P8 audit's lane); integer-division truncation in the accrual (≤1 milli/tick, negligible, ODN-10-blessed).
- **Base = `v2`** — the diff is the full PR against v2; only the changed files are in scope. Prior-round notes that remain unfixed are carried forward as notes — do not escalate them to blockers.
- **Final-round precision:** a genuine BLOCKER = the canon text as written would mislead the implementing minion or breaks a hard contract (ODN-10 integer-only state, catalog-load fail-fast, E10 replay/derive-don't-record, a cited code seam that doesn't exist). Cosmetic/citation polish = note; a real but non-contract-breaking gap = warning.

## FIX-AUDIT (round 3 — your PRIMARY job)

Round 2 verdict: NEEDS CHANGES (1 blocker B1, 6 warnings W2-W7, 13 notes N1-N13 — full list with evidence in the r2 consolidated.json). The r3 push claims ALL of them fixed except notes N2/N3/N4/N6/N7/N10/N12 (not claimed — expect them carried). Classify EVERY r2 blocker and warning (and spot-check the notes) as `fixed` or `still-present` by re-reading the cited locations in the worktree at sha 42e4eb6 — do not trust the r3 claims or the decision-log's own r2-notes entry (verify the BYTES). Emit one finding per r2 item that is NOT fully fixed, with severity = its r2 severity, detail prefixed `still present since round 2:`, and evidence from the CURRENT file bytes. Check the fix landed in EVERY canon surface that carried the defect (spec Thread 2, card 5.9, GDD M6, decision-log item 1) — a fix that bites in one surface but not another is still-present.

Key claimed fixes to verify BITE:
- **B1 (integer/fixed-point re-spec):** `spawn_credit_milli` (milli-packets), `cap_fraction_permille` (int; 500) in balance.json, `accrue_milli = cap_fraction_permille × throughput_units ÷ packet_bandwidth`, spawn costs 1000, pickable while `credit_milli >= 1000` — integer-coherent and LOADABLE (`core/catalog.odin:675` `parse_integers = true` + `jint_strict`; balance.json header "All state-affecting values are int (ODN-10)"). NO residual float state anywhere in the four surfaces (hunt for stray CAP_FRACTION/0.5/fractional wording).
- **W2 (state home):** Flow_State beside `lane_caps` (`core/flow.odin:96`), updated IN PLACE by flow.odin §1b; the "rebuilt by the spawn pass" contradiction removed; card 5.9 Systems line → flow [ODN-3]; demand.odin named stateless. Verify against the actual flow.odin/demand.odin structure.
- **W3 (decision-log item 4):** "data change, not a code change" replaced with the CODE-change truth (Terminal_Role closed enum + touch points).
- **W4 (type-relative ceiling):** `MAX_CREDIT_MILLI(type) = 1000 × max(1, ceil(cap))`; campus 150 u/s → accrue 2500, ceiling 3, achieves cap long-run. Check the math at every stated value.
- **W5 (no-burst + latency):** residential ceiling 1 → no burst; the 600 ms > 500 ms math stated; W10 pin asserts end-to-end transit ≤ class latency tolerance.
- **W6 (quantitative pins):** W9/W10 pins state rate envelopes on a known seed (≥ 0.95 × expected surge volume; ≤ cap × window + burst allowance; credit ≤ MAX_CREDIT) — real quantitative assertions, not prose.
- **W7 (re-pin surface):** `core/demand_test.odin` (volume + spawn-histogram pins, the `effective_volume` surge pin) + `core/flow_test.odin` + `core/determinism_test.odin` named with positive + negative assertions — verify those test files exist in the worktree.
- Notes claimed: N1 (E24 → pin cited `sla_test.odin:88` `sla_check_invariant` — verify the pin exists there), N5 ([E3] tag dropped from card 5.10), N8 (`core/growth.odin:76` — verify the constant is at :76), N9 (director-spawned scope on the "never at endpoints" claim), N11 (provenance disclaimer head on the decision-log entry).

Also append, as a FINAL element of your array, one note-severity finding titled `Fix audit: <n>/<m> r2 blockers+warnings verified fixed` with a one-line-per-item classification list in `evidence` (B1: fixed|still-present, W2: ..., W3: ..., W4: ..., W5: ..., W6: ..., W7: ...).

## YOUR LENS (new findings)

Beyond the fix-audit: audit the diff against the spec and context docs above. Identify violations of specific acceptance criteria / mission deliverables (the briefing's four design threads, Given/When/Then shape, real-world rationale cited, balance-lever placement, determinism constraints, explicit conflict resolution with existing canon E22/E9/4.1/5.1/5.8), deviations from spec intent, contradictions between spec constraints and the actual docs, and scope drift — changes not asked for by the spec. For each finding, reference the violated AC or constraint in `detail` (quote the exact phrase from the spec when possible).

## OUTPUT CONTRACT

Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "acceptance",
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

Your output path: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/acceptance.json`
