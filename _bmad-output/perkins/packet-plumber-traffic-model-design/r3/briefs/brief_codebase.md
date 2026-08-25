# Lens brief — CODEBASE FIT (mm-codebase-r3) — Perkins round 3, PR #53

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
- Determinism spine: all rng from `state.rng`, seed-derived, no wall-clock; replay byte-identical [E10]; golden re-bless discipline (4.3); derive-don't-record; **ODN-10 integer-only state paths**.
- Canon doc set: GDD `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` (+ decision-log.md, append-only), stories `_bmad-output/planning-artifacts/sprints/stories-v2.md`, sprint plan `.../sprint-plan-v2.md`, spec `_bmad-output/implementation-artifacts/spec-traffic-model.md`, architecture `.../architecture/architecture-v1.md` (§11.7 = the E# contract table).
- Coordination constraint: GDD edits must be SECTION-ADDITIVE (no terminology rewrites — the p1P8 terminology audit owns wording and serializes behind this PR).

## LENS-GUARDS — read before reporting (prevents false positives)

This is **round 3 of 3 — the FINAL automated round, a FIX-AUDIT on the r2 rework**. Round 2 (sha da3a50e) verdicted NEEDS CHANGES with 1 blocker + 6 warnings + 13 notes; this push (the single commit 42e4eb6) claims the blocker + all 6 warnings + notes N1/N5/N8/N9/N11 fixed. Prior findings: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r2/consolidated.json` (read it).

- **Fix-audit mandate:** where a claimed fix touches your lens, verify it BITES (re-read the cited code/docs in the worktree — do not trust the claims). Do NOT re-report a verified-fixed item as new. Report still-present items with `"still present since round 2"` in the detail, at their r2 severity.
- **Do NOT re-litigate (settled in r1/r2):** the ~1,000× unit compression (endorsed); the M1-vs-shipped tier discrepancy (acknowledged canon); committing the surge-explainer html/PNGs (approved provenance artifacts); slice-5B sequencing/numbering (ratified); card-format conventions; the u/s-vs-u/tick arithmetic convention (r2-rejected); "5.9 changes no catalog" (r2-rejected).
- **NOT defects:** future-tense test pins in cards; the explainer artifact's superseded numbers (spec brackets + supersedes; provenance disclaimer added); terminology wording (p1P8 audit's lane); integer-division truncation in the accrual (≤1 milli/tick, negligible).
- **Base = `v2`** — the diff is the full PR against v2. Prior-round notes that remain unfixed are carried forward as notes — do not escalate them to blockers.
- **Final-round precision:** a genuine BLOCKER = the canon text as written would mislead the implementing minion or breaks a hard contract (ODN-10, catalog-load fail-fast, E10 replay, a cited code seam that doesn't exist). Cosmetic/citation polish = note; a real but non-contract-breaking gap = warning.

## YOUR LENS

Reality check against the actual codebase. Verify by reading files in the worktree, not by assuming:
- Do files, functions, types, line numbers, and imports referenced in the diff actually exist and match? The rework cites MANY seams — verify each: `core/flow.odin:96` (lane_caps in Flow_State), `core/flow.odin:85` ("NEVER serialized"), `core/flow.odin:646` (`for k in 0..<vol` integer spawn loop), flow.odin §1a (`flow_seed_demand` legacy path) vs §1b (director spawn pass) — do these sections exist as described? `core/catalog.odin:675` (`parse_integers = true`), jint_strict (~:1043-1049 — does it reject non-Integer?), `core/catalog.odin:22` (Terminal_Role closed enum), `core/catalog.odin:1011` (role_from_name), `collect_terminals` role selector, `core/growth.odin:76` (GROWTH_MIN_SEP_TILES :: i32(3) — is :76 the declaration?), `core/sla_test.odin:88` (sla_check_invariant — does the pin live there?), `core/demand_test.odin` / `core/flow_test.odin` / `core/determinism_test.odin` (do these test files exist — the W7 re-pin surface?), data/node_types.json throughput values (residential 5, content_host 80 — and is there any 150 u/s type or is campus hypothetical?), data/packet_types.json email latency_tol_ms 500.
- Do the stated derived numbers check out against the code's actual values (accrue_milli at each type's real throughput: 500×5÷30=83, 500×80÷30=1333)?
- Does the SLA-accounting claim match the code (a capped spawn skipped before `flow_try_spawn` never reaches `sla_count_demand`; a pool-dropped arrival counts demand then drops — check flow.odin's spawn path + sla call sites)?
- Are naming conventions consistent with the project's canon docs (`spawn_credit_milli`, `cap_fraction_permille` vs existing balance.json key style — check data/balance.json's actual keys)? Would `cap_fraction_permille: 500` load under the actual catalog parse?
- Does the diff duplicate logic/text that already exists elsewhere, or leave orphan text — references to files/sections that don't exist or wrong line anchors (line-number citations are the project's evidence standard — drift is a finding)?

## OUTPUT CONTRACT

Return ONE valid JSON array. Each element must match this schema exactly:
{
  "source": "codebase",
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

Your output path: `/Users/moses/code/_bmad-output/perkins/packet-plumber-traffic-model-design/r3/codebase.json`
