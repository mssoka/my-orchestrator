## 🤖 Perkins automated review — round 1 of 3

**Job:** packet-plumber-wire-aesthetics (Story 7.5 — wire aesthetics, shipped as routing-only infrastructure)
**Reviewed sha:** `2aaaa255490f02f9507ef8aabf2ff6aa5cdbe499` (head of `wire-aesthetics`, base `v2`)
**Reviewers:** 7/7 completed (blind, edge, acceptance, security, architecture, codebase, tests)
**Verification:** 20/20 findings confirmed against the code — 0 discarded as false-positive

**Mechanical verification track (run at the reviewed sha in the round worktree):**

- **Local suite:** `tools/ci-local.sh --mac` → **10/10 gates green** — gate 4 golden harness **34/34 demos green on the committed goldens (ZERO golden churn** — the shipped flags-off render is byte-identical to the blessed T2 frames), gate 9 replay byte-identical (pause 363,493 B + qos_contention 65,626 B).
- **Cost immunity (the load-bearing guard): CLEAN.** `draw_cost = span × cost_per_tile` on the LOGICAL geometry (`core/topology.odin:495`); `hash_topology` before/after `wire_paths_compute` is pinned; the negative control was **re-run and bites**: a phantom +3 detour span flips the pin red (`got 390 want 300`), reverted, suite 6/6 green again.
- **Determinism (the PR's pixel claim): PROVEN and reproducible.** `harness wire-preview` rendered twice into separate dirs — **all 14 PNGs SHA-256 byte-identical across runs**; routed≠straight and anchors≠straight pixel-wise (the machinery actually draws when a flag flips).
- **Canon fold: MATCHES.** The diff's `stories-v2.md` §7.5 card + `decision-log.md` 2026-08-19 entry are byte-identical to the worktree; verdict C wording ("Ship pure straight…") recorded verbatim.
- **Flags OFF by default: CONFIRMED** (`app/main.odin` + `harness/goldens.odin` set `route_wires=false`/`wire_anchors=false`; legacy draw branches are byte-for-byte pre-7.5).
- **`wire-preview` gate tool: WORKS** — emits the 14 gate frames (juice/estate × routed/straight/anchors + close-ups + fan shots), exit 0.

### Blockers (0)
None. The hard blocker class is clean: cost stays on the LOGICAL geometry (pinned + negative-controlled + T1/replay byte-identical + zero golden churn), and the shipped render is byte-for-byte the pre-7.5 straight look per gate verdict C.

### Warnings (8)
1. **Ribbon-fan pin resolves the router via nonexistent node id 8 and discards the lookup's ok — passes by coincidence of the (0,false) fallback slot** [blind, edge, acceptance, codebase, tests] — `app/render/wire_path_test.odin:317-318`. `wire_setup` spawns only ids 0-5; `node_slot(8)` returns `(0,false)` and slot 0 is coincidentally the router, so the apex-distance assertion measures the right node by accident; `rim` also uses `port_capacity 4` for an 8-port `router_mid`. Any fixture reorder silently weakens the pin. Fix: `rs, ok := pp.node_slot(&s.topology, 0)` with `expect(ok)`, `puck_rim_world(&v, 8)`.
2. **Shipped spec artifact still carries pre-verdict "full deliberate T2 re-bless" language, contradicting verdict C (no re-bless) in the same PR** [blind, acceptance] — `spec-7-5-wire-aesthetics.md:61,74,84,113`. The canon fold (stories-v2 + decision-log) is correct; only this artifact contradicts itself. Fix: rewrite the Code Map goldens line, the goldens task, and the "Given the re-bless" criterion to the no-re-bless wording.
3. **Bend-cap exit ships a polyline that may still cross/sprite-clip — the spec's "still crosses after the bend cap → STRAIGHT" half is unimplemented** [edge] — `wire_path.odin:637`. When the loop exits because `bends == WIRE_DETOUR_MAX_BENDS`, no final `scan_obstacles` runs; only the length-ratio half of the degradation contract exists (`spec-7-5:29`). Flags-off today, so no shipped-pixel impact. Fix: one final scan after the loop; if found → straight.
4. **Degradation fallback is never exercised: the only fixture produces a straight path, so the ratio/bend-cap trip is asserted vacuously** [blind, tests] — `wire_path_test.odin:233`. No fixture forces `WIRE_DETOUR_MAX_LEN_RATIO`, `WIRE_DETOUR_MAX_BENDS`, `WIRE_STUB_TILES`, or edge/sprite detours. Hard requirement #4 has no boundary coverage. Fix: add over-ratio, bend-cap, and stub-crossing fixtures asserting the n==2 fallback.
5. **The 6 wire-path pins (incl. the cost-immunity pin) are run by no ci-local gate — the suite stays 10/10 even if they rot** [acceptance, tests] — `tools/ci-local.sh:56`. Only `odin test core` is gated; `odin test app/render` is manual (green today, verified). Gate 4's T1/replay independently pins cost immunity end-to-end, so this is a durability gap, not a live defect. Fix: add an 11th gate (or extend gate 2) running `odin test app/render`, mirrored in `ci.yml`.
6. **Flags-ON render variants have zero automated coverage; the wire-preview tool is exercised by no CI gate** [tests] — `tools/ci-local.sh:61`. `preview-check` is the unrelated R2a assist check; the routed/anchor draw branches run only when a human invokes `harness wire-preview`. Fix: a smoke gate asserting exit 0 + non-empty PNGs (or hash-pin one routed frame).
7. **Frozen Intent promises anchors "aligned to the incident directions" but the code allocates a rotated regular template independent of each pipe's actual direction** [blind] — `wire_path.odin:router_anchor_index`. Anchors sit at `base + rank*16/n`; base is the MEAN incident direction, so asymmetric routers don't align anchors to the pipes' directions. Presentation-only, flags-off. Fix: snap each pipe's anchor to its own `direction16` index, or amend the spec wording.
8. **Advisory test gate: CONCERNS** [tests] — P0 100% (cost immunity dual-pinned), P1 ≈83% (degradation unexercised at the boundary, pixel determinism manual, flags-OFF unasserted), overall ≈82% (flags-ON variants unautomated). Fix: wire `odin test app/render` into CI + degradation fixtures + a wire-preview smoke gate → PASS.

### Notes (12)
- Pixel-level "rendered twice → identical SHA-256" claim has no in-tree artifact — true and reproducible (Perkins re-ran it: 14/14 byte-identical) but not durable. [acceptance, tests]
- `draw_glow_edge` recomputes `wire_path_compute` per edge instead of threading the frame's shared paths slice like the other four consumers. [blind, architecture]
- Lane-stripe composite block duplicated between the legacy and variant branches of `draw_bundles` (`view.odin:390,458`). [blind, architecture]
- `bundle_end_anchors`/`end_apex` discard `pp.node_slot`'s ok — silent fallback to slot 0. [security]
- Pin suite only exercises the primitive-fallback radii; the shipped sprite-target branches of `puck_rim_world`/`building_foot_world` are untested. [codebase]
- Dead locals in `scan_obstacles`: unused `segs` and discarded intersection point `X`. [codebase]
- `bundle_end_anchors` discards its `end` parameter (`_ = end`) then branches on it. [blind]
- `Anchor.idx` is written everywhere but never read. [blind]
- `wire_preview.odin` header documents 6 emitted PNGs; the code emits 14. [blind]
- `band_world` restates `band_width`'s formula, against the file's own ONE-definition convention. [architecture]
- `draw_bundles` requires a `paths` arg with no default while its three siblings default to nil. [blind]
- The shipped flags-OFF state (`route_wires`/`wire_anchors`) is asserted by no test. [tests]

### Reviewer agreement
- Ribbon-fan node-id-8 bug: **5 lenses** (blind + edge + acceptance + codebase + tests).
- Spec re-bless contradiction: 2 lenses (blind + acceptance).
- Degradation unexercised: 2 lenses (blind + tests).
- Pins not gated in CI: 2 lenses (acceptance + tests).
- Pixel-determinism durability: 2 lenses (acceptance + tests).
- Glow recompute / lane-stripe dup: 2 lenses each (blind + architecture).

### Verdict
**READY TO MERGE** — 0 blockers.

The hard blocker class is clean: cost stays on the LOGICAL geometry (pinned, negative-controlled, T1/replay byte-identical, zero golden churn — 34/34 demos on the committed goldens), the determinism claim is independently reproducible (14/14 frames byte-identical across two renders), and the shipped render is byte-for-byte the pre-7.5 straight look per gate verdict C. All findings are test-durability, doc-consistency, and coverage gaps in OFF-by-default infrastructure — none touches gameplay, connect/anchor/cap semantics, or cost. Worth a follow-up sweep (the node-id-8 test fix especially), but nothing gates the merge.

_Address findings and push — I re-review automatically on the new sha._
