# SHARED CONTEXT — Perkins round 1, packet-plumber v2 story 1.2 (PR #22, sha 8509fc2)

You are one lens of an automated code-review fan-out (the `code-review` skill, Headless Mode). You have read-only access to the repository. Your job: apply YOUR ONE LENS precisely, verify every claim by reading the actual code, and emit findings as JSON. Do not fix anything.

## Canonical inputs (read these; do not re-derive)

- **Canonical diff (the exact bytes under review):** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.2-window-draw-pipe/r1/diff.patch` (3368 lines; PR #22 vs the v2 base — 2372 insertions / 401 deletions across 27 files).
- **Worktree (checkout at exactly sha 8509fc2 — read files here for verification):** `/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-1-2-window-draw-pipe-r1`
- **Project conventions:** `{worktree}/project-context.md` (ODN rules, naming, the determinism spine).
- **Spec files (read what your lens needs):**
  - Round briefing (the lens-guards live here): `/Users/moses/code/_bmad-output/briefings/perkins-packet-plumber-v2-1.2-window-draw-pipe-r1.md`
  - Job briefing: `/Users/moses/code/_bmad-output/briefings/packet-plumber-v2-1.2-window-draw-pipe.md`
  - Story 1.2 card: `{worktree}/_bmad-output/planning-artifacts/sprints/stories-v2.md` (the `### Story 1.2` section, ~line 72)
  - Architecture: `{worktree}/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md` (S1 Topology, the Command_Bus, §11.1/§11.7, the ODN spine, §10.2/§10.4 T1/T2 goldens)
  - GDD: `{worktree}/_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/gdd.md` (E1.1 node+pipe, E1.2 draw interaction)
- **Prototype reference (for the from-scratch/copy check):** `/Users/moses/code/packet-plumber-prototype-ref` (a frozen Godot prototype — reference only, different language).
- **Prior round (CONTEXT ONLY — 1.2 builds on 1.1's spine; do not audit 1.1 findings as if they're new):** `/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-1.1-walking-skeleton/r1/consolidated.json`

## What this PR does (review scope)

The **first runnable `app.bin`** (slice-1 story 1.2), built ON story 1.1's determinism spine (already merged in v2): a 1280×720 raylib window rendering a hardcoded static map; the player **draws one pipe** (drag node→node, snap, cost) via a validated Command_Bus + edit fast-path; a minimal `Topology` (node+pipe SOA), `Command_Bus` (draw/validate/apply), the render/view loop — on top of the 1.1 spine. Adds a **T2 pixel golden** for the drawn frame and a **W1 CI drift-rejection negative test** (carry-forward from #21). **No routing/flow** (story 1.3 by design).

Changed files (new = +): `.github/workflows/ci.yml`, `app/main.odin`(+), `app/render/palette.odin`(+), `app/render/view.odin`(+), `core/catalog.odin`(+), `core/determinism_test.odin`, `core/serialize.odin`, `core/step.odin`, `core/topology.odin`(+), `core/topology_test.odin`(+), `core/types.odin`, `data/{balance,node_types,palette,pipe_tiers}.json`, `demos/draw.dem`(+) + `demos/boot.dem`, `goldens/{boot.t1,boot.log.bin}` (re-blessed), `goldens/{draw.t1,draw.log.bin,draw/02500ms.png}`(+), `harness/{catalogs,demo,drift,goldens,main,run}.odin`.

## ⚠️ CRITICAL LENS-GUARDS (this PR's load-bearing invariants — verify directly against the code)

1. **REPLAY-EQUALITY OVER DRAW (the load-bearing invariant):** the draw/apply path MUST route through the action-log + state-hash. A RECORDED draw sequence must reproduce byte-identical frames — re-stepping `(seed, action_log)` with draw actions → identical `state_hash` sequences + identical rendered frames. The replay test MUST cover a DRAW sequence (not just the 1.1 empty-map case) and be NON-VACUOUS. Look at: `core/determinism_test.odin::test_replay_byte_identical` (now draws 2 pipes), `core/serialize.odin::state_writer` (serializes the Topology — nodes+pipes slot-by-slot incl alive flags), `harness/run.odin::replay_hashes` + `verify_replay`.
2. **ODN-1 — `package core` must have NO engine symbols.** `core/` imports only `core:*` (never `vendor:raylib`, `core:os`, `core:time`). raylib lives ONLY in `app/`. A raylib/engine type leaking into `package core` = blocker. Look at: every `import` in `core/*.odin`; `tools/lint.sh` gate 1.
3. **ODN-10 — core is integer-only + no map ITERATION** (map ACCESS by key is allowed; iterating a map breaks determinism because Odin map order is unspecified). New Topology/Command_Bus/catalog code must respect this. Look at: `core/topology.odin`, `core/catalog.odin`; `tools/lint.sh` gate 3.
4. **The T2 pixel golden must be REAL:** byte/pixel-EXACT comparison, not fuzzy or absent. Look at: `harness/goldens.odin::compare_images` (`pa[i] != pb[i]` per pixel, returns -1 on dimension mismatch → fail), `check_golden` (mismatch>0 fails, mismatch<0 fails); the golden `goldens/draw/02500ms.png`.
5. **The W1 CI negative test must ACTUALLY be in CI** (the #599-r2 / verification-gap lesson: a local-only check does not count). A deliberately-drifted action log fed to the replay gate must be REJECTED, in a CI-exercised step. Look at: `.github/workflows/ci.yml` step "W1 drift-rejection negative test" → `tools/harness.sh drift-check`; `harness/drift.odin::drift_check` + `make_drift_mutations`.
6. **The draw interaction is real:** drag node→node, snap (inclusive radius E4), validate, cost, appear — and the drawn pipe is RECORDED in the action-log (a draw that bypasses the action-log breaks replay-equality). Look at: `app/main.odin::handle_input` (fast-path applies + appends to `action_log` with `apply_tick = tick+1`), `core/topology.odin::validate_draw`/`apply_draw`/`topology_apply_edit`.
7. **From-scratch, not a copy:** the Godot prototype is reference-only; flag any wholesale copy of its render/topology code. (Data-value reuse, e.g. pipe-tier numbers, is allowed and expected.)

### DO NOT FLAG (expected by design — flagging these is a FALSE POSITIVE that will be discarded):
- The absence of routing / packet flow — story 1.3 by design.
- The window existing — story 1.2 IS the window (headless-only was 1.1).
- `LOG_VERSION` bumping 1→2 — deliberate; v1 logs are rejected, 1.1 goldens re-blessed with this story.
- `boot.log.bin` / `boot.t1` changing — the `catalog_hash` changed because the catalog grew (added node_types/pipe_tiers); goldens deliberately re-blessed.
- The app's edit fast-path applying a draw immediately + logging `apply_tick = next` — this is the E10 step-boundary convention (draw happens after step(T) in handle_input → belongs to T+1's pre-step application; converges with replay at every step boundary). Verify it if you doubt the convergence, but do not flag it by default.
- `harness/goldens.odin::swizzle_rb` using `LoadImageColors` + manual pixel swap, or the `// NOTE: never UnloadImage(dimg)` comment — these are deliberate rlsw-readback normalizations, not bugs.

## EMPIRICAL GATE STATUS (Perkins ran these at sha 8509fc2 — ALL GREEN; do not re-report as failures, but you MAY re-run any of them to confirm a specific claim):
- `tools/lint.sh` → all 4 gates green (core import purity, no file-scope var, no map iteration, no bare `_` discards).
- `odin test core` → 15/15 tests pass (incl. `test_replay_byte_identical` with 2 drawn pipes, the topology validation contracts, the binary-log round-trip + rejections).
- `odin build app -out:app.bin` → builds clean (1.38 MB).
- `tools/harness.sh run` → boot + draw demos PASS (T1 state-hash manifests + T2 pixel golden + the replay gate).
- `tools/harness.sh drift-check` → 11 mutations across 2 demos ALL rejected (W1 gate bites).

## OUTPUT CONTRACT (read carefully — your output is consumed mechanically)

Write ONE valid JSON array to your assigned output path (given in your lens file). Schema per element:
```
{
  "source": "<the value assigned to you: blind | edge | acceptance | security | architecture | codebase | tests>",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag, e.g. replay-equality, odn1-leak, golden-fuzzy, ci-gap, boundary, coupling>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<the EXACT lines you READ from the file/diff that prove the claim, pasted verbatim. 'N/A' ONLY for findings with no possible code reference. Do not paraphrase. If you cannot quote the lines, you have not done the work — drop the finding.>",
  "detail": "<why this is a problem, ≤40 words>",
  "recommended_fix": "<the change to apply, ≤40 words>"
}
```
Rules:
- Return ONLY the JSON array (the file must contain nothing but the array — no prose, no markdown fencing, no preamble). `[]` is valid and expected when you find nothing.
- Do NOT invent findings to fill a quota. Accuracy > volume. An empty array is an honest answer.
- ACCURACY MANDATE: every finding is independently re-verified against the actual code before it reaches the report. Findings whose `evidence` cannot be located verbatim, or whose claims contradict the code, are DISCARDED silently. So: open the file, read the lines, quote them exactly. Hedging ("might", "could") means you haven't verified — either verify and report crisply, or drop it.
- When done writing your JSON file, stop. Do not attempt fixes, do not push, do not modify any file other than your one output file.
