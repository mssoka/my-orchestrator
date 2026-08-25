Slice 1: W3 MCP proof + sim spine in engine + the MM look (stories 0.1, 1.1–1.3)

## Slice 1 — the UE port's first vertical slice: MCP proof + sim spine in engine + the MM look

Stories **0.1** (W3 MCP editor-driving proof), **1.1** (sim spine in engine, headless), **1.2** (PIE + static render + draw one pipe), **1.3** (one packet flows). The determinism spine is untouched in semantics — the v2 serialization extension + golden re-bless are deliberate + cause-documented (below). The win/lose stub (1.4) is NOT in this dispatch's scope (the briefing names 0.1 + 1.1→1.3).

---

### Story 0.1 — W3 MCP proof (the bootstrap's unmet acceptance item) ✅

The agent loop every later slice's T2 verification depends on, proven end-to-end BEFORE the slice-1 build:

- **Bridge deployed + editor up:** `ue-mcp` bridge plugin (`Plugins/UE_MCP_Bridge`, non-interactive deploy via the package's deploy-cli) compiled + the editor boots with the bridge (`npx ue-mcp doctor` clean: bridge v0.3.0, everything aligned) AND the official Unreal MCP server on :8000.
- **Asset query (editor-open):** `asset.list` on `/Game` → `{"success":true,"assetCount":0,...}` (the project had no Content at slice 0 — the query itself is the proof; the RunLevel map now ships with this PR).
- **Screenshot + vision-read verify:** `editor.capture_screenshot` → `docs/goldens/screens/slice0-1-editor-baseline.png` → verified by the local vision model (detailed on-topic description: UE editor viewport, template landscape, axis gizmo — quoted in the session).
- **Recorded session:** proven commands appended to `docs/agent-playbook.md` (bridge deploy + rebuild recipe, port.json gotcha, screenshot filename behavior).
- **Carried hygiene folded in:** format gate SKIP-vs-PASS distinction (`SKIPABLE:` gates in `local-ci.sh` — a skipped gate is never recorded PASS), PPProbe negative-args leg (`--probe-negative`: bad `-seed`/`-ticks` fail loud, log-truth asserted), `compare-golden.sh --self-test` (a corrupted golden MUST fail loud), U-E2 Config fix (AndroidFileServer plugin disabled — the editor boot kept re-dirtying `DefaultEngine.ini`; the new Config-porcelain assertion caught it, the plugin disable fixed it).

### Story 1.1 — sim spine in the engine (headless) ✅

The routing 4-rule spine as UE-header-free headers, driven by the fixed-tick driver, proven on all three golden surfaces:

- **`PP_Topology.h`** (S1): nodes/links, integer grid, monotonic ids (E11), the validate-then-apply edit authority (E3 self-loop, E26 terminal-pair, span rule).
- **`PP_Routing.h`**: the per-hop forwarding table (Dijkstra per destination, insertion-order tie-breaks — rule 1: rebuilt only on topology change, synchronously inside the tick) + ECMP (`splitmix64(src,dst,class,pkt_id) mod N` — rule 2, pure hash, no sim-rng draw). Derived, never serialized (the Odin canon decision).
- **`PP_Bundles.h`**: parallel-pipe bundles, cap = **static sum at table-build** (rule 3).
- **`PP_Flow.h`**: slice-1 flow — spawn from legacy demand (no rng draw), per-hop advance by bandwidth units, deliver at sink, E29 severed-edge drop-back.
- **`PP_Sim.h`**: `Step` applies the tick's replay commands (validate-then-apply; a backward tick or failed replayed command latches `ReplayError` — never silent), rebuilds derived views on gen change, runs the flow. v2 serialization (catalog_hash / score / replay_error / topology / flow / action-log sections).
- **`PP_Scenario.h`**: the SHARED golden scenario builder (fixture + draws + demand) — all three surfaces use it, so the numbers CANNOT drift (UAD-17).
- **`FPPSimDriver`** (UAD-2): clamped float accumulator → integer ticks; unit-tested.
- **Extended dual-runner suite:** spine-check 43 → **91 checks** (topology/routing/bundles/flow/replay/golden); automation mirrored (14/14 incl. `PacketPlumber.Topology.Rules`, `Routing.ECMP`, `Bundles.CapIsSum`, `Flow.DeliverAndE29`, `Determinism.GoldenScenario`, `Driver.Accumulator`); PPProbe dumps the routing table + writes the extended golden JSON.
- **Golden schema single-sourced:** `docs/goldens/SCHEMA.md` — the three writers (spine-check printf, commandlet, compare-golden KEYS) all derive from it.

**GOLDEN RE-BLESS (deliberate + cause-documented, per the AGENTS.md discipline):**
`state_hash` fbe6fae2655cadf7 → **5e440f9c5a28892a**, `save_version` 1 → 2. **Proof the fold is honest: `tick_nonce` (2381141952) and `rng_first4` are byte-IDENTICAL to the v1 golden** — the RNG contract did not move; only the extended v2 layout (topology/flow/action-log/catalog_hash sections) + the full scenario changed the hash. 3-way compare green (committed golden == standalone spine-check == engine PPProbe, incl. `topology_summary`, `forwarding_summary`, `flow_summary`, `catalog_hash`).

### Story 1.2 — PIE window + static render + draw one pipe ✅

- **PIE session:** the RunLevel map (created via ue-mcp level tools) + `APPRunGameMode` (owns sim + driver + command bus; fixture = the golden's source/router/sink, run setup) + `UPPRunView` (C++-only UMG — no content assets).
- **Draw one pipe:** Enhanced Input (runtime-created actions) + `FPPCommandBus` — E4 snap (exact integer px compare, inclusive), validate-then-apply via the live fast-path (edit lands this frame, logged `apply_tick = next` — ODN-2). The recorded session drove BeginDraw/EndDraw through the bridge: the FIRST drag used coordinates off the nodes and was **correctly rejected by the bus** (no snap → MissingNode); the correct drags drew both pipes instantly.
- **The MM look (UAD-22 baseline):** warm-cream canvas (#F5F0E4), flat amber/gray/blue nodes with soft blob shadows, ribbon roads with rounded casing + rounded caps — all rounded-box brushes in UMG. See the T2 frames below.

### Story 1.3 — one packet flows (you see it move) ✅

- The flow (spine, 1.1) carries the per-hop advance; the view's packet-dot pool (UAD-8) interpolates between the snapshot pair (20 Hz sim → 60 fps view) with MM-style cubic ease-in-out across BOTH the inter-snapshot fraction AND the edge progress (presentation-only — never sim state, ODN-1). Dots persist across ticks (the static world rebuilds only on topology change).
- **Recorded in PIE:** both pipes drawn → packets flowed (score climbed past 139) → a mid-road packet dot captured + vision-read verified.

---

## The look-parity evidence (PR body requirement)

**Committed surface (UE frames + checklist score):**

| Frame | What it proves |
|---|---|
| `docs/goldens/screens/slice1-2-drawn-pipe.png` | The static fixture in the MM look: cream canvas, amber source / gray router / blue sink nodes with soft shadows, TWO white ribbon roads with rounded ends connecting them, status line `tick … · packets … · score … · 20 Hz`. Vision-read verified (content quoted in the session). |
| `docs/goldens/screens/slice1-3-packet-mid-traversal.png` | A blue packet dot mid-road (gray→blue segment, ~80–85% of the way) — the eased-motion evidence. Vision-read verified. |

**Look-parity checklist score** (full detail: `docs/goldens/look-parity-checklist.md`):

| # | Axis (UAD-22) | Slice-1 score |
|---|---|---|
| 1 | Palette (warm-cream canvas, muted node hues) | ✅ |
| 2 | Road rendering (ribbon roads with rounded casing) | ✅ |
| 3 | Shadows (soft blob shadows) | ✅ |
| 4 | AA (clean edges, no aliased diagonals) | ✅ |
| 5 | Motion easing (1.3: ease-in-out, arrival settle) | ✅ |

**IP guardrail honored:** the ACTUAL Mini Motorways reference frame stays **local — never committed**. It is not on this machine; the side-by-side against a real MM frame + the user's eyes at review is the open question the slice map anticipated (the checklist is scored against the documented MM look + the local reference when the user provides/captures one). The committed surface is the UE frame + the score.

## Decisions & rationale

1. **Determinism spine untouched in semantics; the serialized layout extended (v2).** The existing fields/behaviors (RNG, heartbeat, FNV-1a-64, LE field-by-field, replay-equality) are byte-identical; topology/flow/action-log sections were ADDED, `SAVE_VERSION` bumped, golden re-blessed deliberately with the honest-fold proof (tick_nonce unchanged). The backward-tick behavior changed from silent-ignore to `ReplayError` latch — the bootstrap's own comment said "the latch arrives with real commands"; it arrived.
2. **Forwarding table + bundles are DERIVED, never serialized** (the Odin canon decision, core/routing.odin): the Topology's pipes ride the hash, so a topology change replays byte-identically without binding replay to the rebuild algorithm. "Topology + routing state in the hash" is satisfied by construction (the table is a pure function of the serialized topology); the PPProbe routing dump + summaries make it visible.
3. **MM look implemented with UMG rounded-box brushes, zero content assets.** C++-first (no Blueprints, no textures): palette tokens are view-layer constants in `PPRunView.cpp` (the JSON palette catalog lands with 3.1, UAD-5). The tilted-camera depth cue + true radial-gradient shadow falloff are deliberate slice-2 refinements (the checklist is scored honestly, not padded).
4. **AndroidFileServer plugin disabled (U-E2).** The editor boot re-wrote the AFS section into `DefaultEngine.ini` on every launch (different security token each time). The new Config-porcelain CI assertion caught it; disabling the plugin (desktop-first project, never needs Android USB deployment) fixed it. `Config/DefaultInput.ini` is gitignored (editor-generated legacy-input boilerplate; Enhanced Input does not read it).
5. **`BeginDraw`/`EndDraw` are BlueprintCallable** — the same seam the Enhanced Input actions and the MCP bridge drive (one legality path for every input surface, UAD-12). This is what made the recorded bridge-driven draw session possible.
6. **The golden scenario is SHARED code** (`PP_Scenario.h`) — every surface builds the identical fixture/draws/demand, so the 3-surface identity is by construction, not by copy-paste.

## Files changed

**Sim spine (UE-header-free, dual-runner):** `Source/PacketPlumberCore/Public/PacketPlumberCore/` +`PP_Balance.h` `PP_Topology.h` `PP_Routing.h` `PP_Bundles.h` `PP_Flow.h` `PP_Scenario.h`, ~`PP_SimState.h` `PP_Sim.h`
**Engine layer:** `Source/PacketPlumber/` +`PPSimDriver.h` `PPViewSnapshot.h` `PPCommandBus.*` `PPRunGameMode.*` `PPRunPlayerController.*` `PPRunView.*`, ~`PacketPlumber.Build.cs`
**Tests:** `tests/spine_check.cpp` (43→91 checks), `Source/PacketPlumberCoreTests/` +`PP_Slice1SimTests.cpp` `PPSimDriverTests.cpp`, ~`PP_DeterminismTests.cpp`, ~`PacketPlumberCoreTests.Build.cs`
**Probe + gates:** ~`Source/PacketPlumberEditor/PPProbeCommandlet.cpp`, ~`scripts/local-ci.sh` `run-tests-headless.sh` `compare-golden.sh`, ~`PacketPlumberUE.uproject` (+`Plugins/UE_MCP_Bridge`, AndroidFileServer disabled)
**Content + config:** +`Content/Maps/RunLevel.umap` (LFS), ~`Config/DefaultEngine.ini` `DefaultGame.ini` (GameDefaultMap + GameMode), +`.gitignore` (DefaultInput.ini)
**Docs + evidence:** +`docs/goldens/SCHEMA.md` `look-parity-checklist.md`, +`docs/goldens/screens/slice0-1-editor-baseline.png` `slice1-2-drawn-pipe.png` `slice1-3-packet-mid-traversal.png`, ~`docs/agent-playbook.md` `docs/timings.md`, ~`docs/goldens/probe-seed42-ticks100.json` (re-blessed)

## Gates

- Fast 3/3 ✅ (format / spine 91 checks / static)
- Full 7/7 ✅ (build + 14/14 automation + PPProbe + negative-args + 3-way golden compare + mismatch self-test + U-E2 Config assertion)
- Look-parity: T2 frames vision-read-verified; checklist scored; MM reference stays local (open question: user-provided frame for the literal side-by-side)

