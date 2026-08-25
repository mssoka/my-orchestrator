---
title: 'Story 3.2 — 3-lane QoS + emphasis dial'
type: 'feature'
created: '2026-08-13'
status: 'done'
review_loop_iteration: 0
baseline_commit: 9a5a35b7a31ea65aaf7f9f28d8d48324450ecfa3
context:
  - '{project-root}/_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Pipes have no QoS: all traffic shares one undifferentiated pipe, so the player has no lever to prioritize (the story's whole differentiator is missing).

**Approach:** Add per-pipe 3-lane (Express/Standard/Best-effort) integer-WFQ weight state, a pure `qos_allocate` proc (largest-remainder, E→S→B tie order, weight-only), a per-pipe "priority emphasis" dial mapping to weight presets in `balance.json`, and per-pipe per-class lane overrides. The allocation is computed inside `flow_step` (ODN-3: QoS lives in Flow, not a peer) and made visible via a lane-proportions readout + lane-striped pipe rendering. Serialization/drops are story 3.3; SLA is 3.4.

## Boundaries & Constraints

**Always:**
- `qos_allocate :: proc(capacity: u32, w: [3]i32, default_w: [3]i32) -> [3]u32` — pure, integer, weight-only (demand NOT an input), largest-remainder with E→S→B tie order, sums in i64, all-zero `w` → `default_w` (E5). Lives in `package core` flow files, invoked by `flow_step` — never a peer system.
- All-zero weights → the catalog default preset (E5). A never-drop class lane (class with `max_loss_pct == 0`) is floored to a quantum of 1 bandwidth-unit after allocation, floors satisfied in lane order E→S→B, capacity exhaustion = defined truncation (E6); the Command_Bus rejects the edit that would zero such a lane (E6).
- The dial maps to weight presets from `balance.json` (`lane_presets` + `default_lane_preset`), wired through the existing data-driven catalog pattern — no hardcoded weights in code. Presets few + legible: balanced `[1,1,1]`, express_heavy `[4,2,1]`, best_effort_heavy `[1,2,4]`.
- All traffic starts Standard (`default_lane` already in catalogs); the player promotes/demotes per type with a per-pipe override.
- Commands are logged (action log) so replay is byte-identical (E10): new union variants + new wire tags appended; LOG_VERSION stays 2 (append-only tags — old logs still parse; existing `goldens/*.log.bin` stay byte-identical).
- Serialization of new state is SPARSE (only non-default weights / non-empty overrides) so existing T1 manifests + T2 pixels do NOT shift. If any existing golden shifts: STOP and flag — do not re-bless.
- New state is Topology-owned data (`pipe_weights`, lane overrides); the derived per-pipe allocation buffer lives on `Flow_State` and is rebuilt in `flow_step` on `Topology.gen` change (like routing/bundles), never serialized.
- Packet advance stays bundle-capacity-based (lane-gated serialization is 3.3). Allocation is computed + visible in 3.2.

**Ask First:** none — presets, keys, colors are delegated (story says "presets are YOUR call").

**Never:** No 3.3 (serialization/contention/drops), no 3.4 (SLA), no 3.5 (placement: `Cmd_Place_Router`, tray). No demand input to allocation. No new peer systems. No maps/globals/float sim state (ODN-10/13). No re-blessing existing goldens.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | `qos_allocate(10, {1,1,1}, {1,1,1})` | `{4,3,3}` (floor 3 each, remainder 1 → E) | n/a |
| E8 tie order | `qos_allocate(5, {1,0,1}, {1,1,1})` | remainder goes to E: `{3,0,2}`; sum always == capacity | n/a |
| E5 all-zero | `qos_allocate(10, {0,0,0}, {1,1,1})` | identical to `qos_allocate(10, {1,1,1}, {1,1,1})` | n/a |
| E6 floor | caps `{0,3,2}` with never-drop on E, capacity 5 | floored `{1,3,2}` (quantum added; sum may exceed capacity) | truncation: with capacity 1 + two floored lanes, floors satisfy E first, B truncates |
| E6 zeroing edit | `Cmd_Set_Emphasis{pipe, preset}` where preset zeroes a lane a never-drop class rides (or `Cmd_Set_Lane` puts a never-drop class on a zero-weight lane) | rejected | `.Invalid_Weights` |
| Bad command args | unknown pipe / preset / class / lane | rejected | `.Missing_Pipe` / `.Invalid_Preset` / `.Unknown_Class` / `.Invalid_Lane` |
| Catalog badness | preset with wrong arity / weight > MAX_WEIGHT / all-zero / missing default | rejected at load | named `Catalog_Error` |

## Code Map

- `core/qos.odin` (NEW) -- `qos_allocate` (E5/E8), lane resolution, `qos_apply_floor` (E6), `qos_pipe_caps` (allocate + floor per pipe)
- `core/types.odin` -- `Cmd_Set_Emphasis` / `Cmd_Set_Lane` variants + `Edit_Error` additions; Flow_State `lane_caps`
- `core/topology.odin` -- `pipe_weights` + overrides data; validate/apply for the new commands
- `core/serialize.odin` -- wire tags 4/5 + sparse weights/override sections in `state_writer`; log read/write cases
- `core/flow.odin` -- `flow_step`: rebuild `lane_caps` on gen change (the E6 floor home)
- `core/catalog.odin` + `data/balance.json` -- `lane_presets` + `default_lane_preset` parsing/validation; `data/palette.json` lane colors (cosmetic)
- `core/qos_test.odin` (NEW), `core/catalog_test.odin`, `core/determinism_test.odin` -- pins below
- `app/main.odin`, `app/render/view.odin` -- select-pipe readout, right-click emphasis cycle, class lane keys, lane-stripe render (default-identical)
- `harness/demo.odin`, `harness/run.odin` -- `emphasis`/`lane` demo directives + lowering; `demos/qos_emphasis.dem` (NEW)

## Tasks & Acceptance

**Execution:**
- [x] `data/balance.json` -- add `lane_presets` (3 presets) + `default_lane_preset` -- data-driven dial wiring
- [x] `core/catalog.odin` -- parse/validate presets (arity, 0..MAX_WEIGHT, no all-zero, default resolves) -- ODN-5
- [x] `core/qos.odin` -- allocator + lane resolution + floor + `qos_pipe_caps` -- the ODN-3 procs
- [x] `core/topology.odin` -- `pipe_weights` (init at draw to default preset) + override list; validate/apply `Cmd_Set_Emphasis`/`Cmd_Set_Lane` incl. E6 rejection; gen bump -- Topology owns QoS data
- [x] `core/types.odin` -- new command structs, `Edit_Error` values, `Flow_State.lane_caps` -- state model
- [x] `core/serialize.odin` -- tags 4/5; sparse weights/override sections in `state_writer`; log write/read cases -- replay + golden stability
- [x] `core/flow.odin` -- rebuild `lane_caps` in `flow_step` on gen change (floor applied) -- "QoS inside Flow"
- [x] `core/qos_test.odin` (NEW) -- E5/E6/E8 pins, tie order, sum==capacity sweep, floor semantics, bus rejections, round-trip + replay with new commands -- durable pins
- [x] `core/catalog_test.odin` + `core/determinism_test.odin` -- preset validation rows + test-catalog defaults + never-drop test class -- fail-fast + replay pins
- [x] `app/render/view.odin` -- lane-stripe render (byte-identical for default weights) + readout geometry -- visible allocation
- [x] `app/main.odin` -- pipe selection, right-click emphasis cycle, per-class lane keys, HUD readout -- the emphasis dial UI
- [x] `harness/demo.odin` + `harness/run.odin` -- `at <ms> emphasis <pipe> <preset>` + `at <ms> lane <pipe> <class> <lane>` directives -- golden scripting
- [x] `demos/qos_emphasis.dem` (NEW) -- draws + emphasis + override + captures (before/after) -- T2 lane-proportions golden

**Acceptance Criteria:**
- Given the `qos_allocate` proc, when distributing any (capacity, weights) with weights in domain, then caps sum to exactly capacity, remainders go E→S→B, and all-zero weights fall back to the default preset (E5/E8).
- Given a never-drop class (max_loss_pct 0) bound to a lane, when the pipe's weights would give that lane 0, then the edit is rejected (E6); when allocation otherwise yields 0, `flow_step` floors it to 1 in lane order with capacity-truncation.
- Given the emphasis dial, when the player sets a pipe's emphasis, then the pipe's `lane_caps` + rendered lane stripes + readout change accordingly, and the change rides the action log (replay byte-identical).
- Given the new demo `qos_emphasis.dem`, when run through the harness, then its T1 manifest + T2 captures are blessed deliberately and the existing 10 demos' goldens are unchanged.
- Given the app, when the player right-clicks a pipe, then the emphasis cycles through the balance.json presets and the lane-proportions readout updates.

## Spec Change Log

## Design Notes

- **Sparse serialization is the golden-stability mechanism.** `pipe_weights` serializes only pipes whose weights differ from the default preset; overrides only when non-empty; new commands never appear in old demos. Existing runs produce byte-identical T1 hashes and pixel-identical T2 frames — no re-bless.
- **Floor semantics:** `qos_apply_floor(caps, never_drop[3]bool, capacity)`: walk lanes E→S→B; a never-drop lane with cap 0 is set to 1 while a floor budget (capacity) remains; exhaustion truncates later floors. On realistic pipes this may oversell the sum by a quantum — defined, 3.3's gap-fill absorbs it.
- **Lane resolution:** a class rides lane = per-pipe override (last-write-wins over the flat list) else the class's `default_lane`. Never-drop lanes for a pipe = lanes any never-drop class rides on it.
- **Demo golden:** `qos_emphasis.dem` captures at ~1000ms (default balanced) and ~5000ms (after `emphasis` + `lane` directives) — the T2 diff IS the "lane proportions changing" golden.

## Verification

**Commands:**
- `odin test core -debug` -- 61 existing + new tests green
- `tools/lint.sh` -- all 5 gates green
- `tools/harness.sh run` -- all demos PASS incl. the new `qos_emphasis` (T1 + replay + T2); existing goldens unchanged
- `tools/harness.sh save qos_emphasis` -- deliberate bless of the new golden (only this demo)
- `tools/harness.sh run` again -- PASS after bless
- `tools/harness.sh drift-check` -- every mutation rejected
- `odin build app` + run: right-click a pipe cycles emphasis; readout updates; stripes render; keys 1/2 + E/S/B set per-class lanes


## Suggested Review Order

**The allocator — E5/E6/E8 contracts**

- Weight-only largest-remainder partition; ties break E→S→B; sums in i64
  [`qos.odin:40`](../../core/qos.odin#L40)

- Never-drop floor: lane order, capacity truncation — the E6 backstop
  [`qos.odin:155`](../../core/qos.odin#L155)

- The flow-side allocation: allocate + floor, per pipe (the readout's truth)
  [`qos.odin:173`](../../core/qos.odin#L173)

- Class→lane resolution: per-pipe override else catalog default_lane
  [`qos.odin:108`](../../core/qos.odin#L108)

**The edit surface — dial + override commands**

- Emphasis validation incl. the E6 zeroing rejection (bus = primary guard)
  [`topology.odin:294`](../../core/topology.odin#L294)

- Override purge on demolish (dead-pipe hygiene, deterministic)
  [`topology.odin:242`](../../core/topology.odin#L242)

**Replay + the golden-stability mechanism**

- New wire tags (append-only; LOG_VERSION stays 2)
  [`serialize.odin:51`](../../core/serialize.odin#L51)

- Sparse + absent-when-empty QoS sections — why existing goldens didn't shift
  [`serialize.odin:182`](../../core/serialize.odin#L182)

- Derived lane_caps rebuilt in flow_step on gen change (never serialized)
  [`flow.odin:196`](../../core/flow.odin#L196)

**The data — emphasis presets**

- lane_presets parsing + fail-fast validation (duplicates rejected)
  [`catalog.odin:481`](../../core/catalog.odin#L481)

- The dial positions (balanced / express_heavy / best_effort_heavy)
  [`balance.json:7`](../../data/balance.json#L7)

**The UI — dial, keys, readout**

- Right-click dial cycle (fast-path apply + log; rejections toasted)
  [`main.odin:368`](../../app/main.odin#L368)

- Pipe hit-testing (point-to-segment, ties → lower id)
  [`main.odin:316`](../../app/main.odin#L316)

- Per-class lane keys (1/2 + E/S/B) on the selected pipe
  [`main.odin:400`](../../app/main.odin#L400)

- The lane-proportions readout (fresh qos_pipe_caps, temp-arena strings)
  [`main.odin:514`](../../app/main.odin#L514)

**The render — lane segments**

- Length-proportional Express→Standard→Best segments; default = byte-identical
  [`view.odin:166`](../../app/render/view.odin#L166)

- The selected-pipe halo (palette-driven)
  [`view.odin:399`](../../app/render/view.odin#L399)

**The golden + the harness**

- The T2 "lane proportions changing" demo (default → express-heavy → best-effort-heavy)
  [`qos_emphasis.dem:16`](../../demos/qos_emphasis.dem#L16)

- The new demo directives (emphasis / lane verbs)
  [`demo.odin:258`](../../harness/demo.odin#L258)

**The pins**

- E8 known-values + sum==capacity sweep; E5 fallback; E6 floor semantics
  [`qos_test.odin:42`](../../core/qos_test.odin#L42)

- Bus rejections incl. the never-drop zeroing guard
  [`qos_test.odin:123`](../../core/qos_test.odin#L123)

- The sparse-contract pin (dump walker: zero QoS bytes on default runs)
  [`qos_test.odin:207`](../../core/qos_test.odin#L207)

- Replay byte-identity with emphasis + lane commands
  [`qos_test.odin:299`](../../core/qos_test.odin#L299)

- Fail-fast catalog rows (presets incl. duplicates)
  [`catalog_test.odin:108`](../../core/catalog_test.odin#L108)
