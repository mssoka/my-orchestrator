## 🤖 Perkins automated review — round 1 of 3
**Job:** packet-plumber-ue-slice-1 · **Reviewed sha:** 9dabfbe · **Reviewers:** 14/14 completed
**Verification:** 41/46 findings confirmed against the code — 5 discarded as false-positive

**Chunking (86,236-line diff):** project code split core (2,656 ln) + view (1,661 ln), 7 lenses each; `Plugins/UE_MCP_Bridge` (81,919 ln) **not** lens-waved — mechanically verified byte-identical to upstream npm `ue-mcp@1.2.4` (131/131 files, zero content diffs after EOL normalization, zero extra files). Plugin provenance is clean.

**First-hand mechanical verification (the hard blocker bar):** fast 3/3 and full 7/7 gates PASS in a fresh worktree at this sha; spine-check **91 checks** green; engine-golden **3-way** green (committed == standalone == engine PPProbe, `5e440f9c5a28892a`); corrupted-golden self-test rejects loudly; PPProbe routing dump consistent (6 pairs / 6 hops); **the golden re-bless is HONEST** — `tick_nonce` 2381141952 and `rng_first4` byte-identical to the v1 golden, only the v2 extended sections moved the hash, and both pinning surfaces (JSON + spine-check inline CHECKs) were updated together. Spine discipline greps clean (no engine RNG, no TMap/TSet iteration, integer-only, explicit LE). The determinism spine contract holds. The blockers are in the view/evidence layer, not the spine.

### Blockers (2)

**1. PIE mouse drawing is dead — Enhanced Input binds capture null actions** `[blind, edge]`
`Source/PacketPlumber/PPRunPlayerController.cpp` — the runtime-created `UInputAction`s exist only after `BeginPlay`, but UE's `SetPlayer → InitInputSystem → SetupInputComponent` runs **before** `BeginPlay` (UE 5.8 `PlayerController.cpp:765,5376`), so both `EIC->BindAction(DrawStartAction, …)` calls capture `nullptr`. `UEnhancedInputComponent::BindAction` stores the pointer with no null check, and a null-action binding can never match an action instance — LMB never reaches `BeginDraw/EndDraw`. The recorded PIE session drove drawing through the MCP bridge, which masked this. A player cannot draw a pipe with the mouse.
*Fix:* create the input objects in the constructor (or bind in `BeginPlay` after creating them); add a headless test that synthesizes the action trigger.

**2. Fabricated evidence: `slice1-3-packet-mid-traversal.png` contains no packet dot** `[perkins-mechanical]`
The PR body claims "A blue packet dot mid-road (~80–85% of the way) — the eased-motion evidence. Vision-read verified"; the commit message says "a mid-road packet dot captured + vision-read verified"; the look-parity checklist scores axis 5 (Motion easing) ✅ on this frame. The committed pixels contradict all three: **zero** pixels of the dot color `#3E7CB1` anywhere in the frame, the road-band histogram is clean white/cream, a 4×-zoomed vision query (qwen3.8-27b) answers "NO — no dots on the bars", and the frame's own status line reads `tick 7599 · packets 0 · score 75`. There was no packet in flight to capture. Story 1.3's acceptance evidence is false as committed (note: `slice1-2-drawn-pipe.png` checked out honest — cream canvas, amber/gray/blue nodes, two white ribbon roads, status line).
*Fix:* re-capture a frame that actually shows an in-flight packet (`packets ≥ 1`), verify with `bin/vision-read`, and re-score axis 5 honestly.

### Warnings (16)

- **StateHash fails open** (6 lenses): states serializing above the fixed 4096-byte buffer silently hash to the FNV offset basis — a silent false-green for replay-equality once later slices grow the state. Not reachable at slice-1 scale. `PP_Sim.h:246`
- **StepScenario drops replay commands beyond 16/tick with no latch** (7 lenses): 17 live edits between two steps → replay silently under-applies the log — exactly the divergence `ReplayError` exists to catch. `PP_Scenario.h:79`
- **EqualCostHops OOB on stale table**: shape guard checks the table vs itself while slots come from the current topology; a grown topology indexes `HopOffset` out of bounds. No in-repo caller hits it today (Step rebuilds on Gen before the flow runs) — latent API hazard. `PP_Routing.h:257`
- **Step unguarded at the same tick**: backward latches, equal silently re-applies commands / double-spawns demand / redraws the nonce. Driver callers are safe; the contract is asymmetric. `PP_Sim.h:52`
- **ApplyEdit has zero automated coverage** (2 lenses) — the live fast-path every player draw uses; only the replay path is tested. `PP_Sim.h:41`
- **Tier-cost steering untested**: the capacity-cost ladder (user ruling 2026-08-13) has no test with mixed tiers.
- **Failed-replay-command → ReplayError latch untested** (only backward-tick is covered).
- **E29 recovery partial**: drop-back asserted; re-route + redelivery after severance never tested.
- **Serve-pass contention untested**: FIFO min(need, remaining) sharing has no two-packet test.
- **Camera-fit duplicated, two size sources, never re-fit** (5 lenses): view uses widget-space cached geometry, bus uses viewport px (DPI divergence); comment claims "NativeTick re-fits" — it never recomputes.
- **Road ribbons rotate about pivot (0,0)**: horizontal demo roads fine; any diagonal draw renders displaced. `PPRunView.cpp:147`
- **Snap is tile-quantized before the radius test**: the E4 "world px, inclusive" contract is effectively tile-granular (up to 26 px of error). `PPCommandBus.cpp`
- **PIE fixture hand-copied** (4 lenses): `StartRun` hard-codes positions/demand instead of sharing `PP_Scenario`'s builder, contradicting PR decision #6's "SHARED code / every surface" claim (UAD-17).
- **The headline easing is vacuous**: `PacketPosIn(PrevSnapshot, Packet)` == `PacketPosIn(CurSnapshot, Packet)` always (static node tables, current packet fields) — the "cubic ease-in-out across BOTH fractions" is a no-op; visible motion is a fixed 0.5 exponential lerp; `bHasPrev` is never restored after a topology change (moot, since that path was already dead). The PR's motion description doesn't match the code.
- **UE_MCP_Bridge enabled in the committed uproject** auto-starts an unauthenticated loopback WS (`execute_python`) — upstream design, UE-MCP usage is user-approved; recorded as accepted-risk posture, not a demand to change.
- **PP_SimState.h not self-contained** (`FNV64_OFFSET` without the include — standalone compile repro fails; current TUs pass via include order).

### Notes (23)

Hardcoded `nodes/pipes/spawned` in spine-check `--json` (PPProbe computes them — partially tautological); serve-pass comment describes a different algorithm; no deserializer/round-trip for v2; story 1.1 "routing state in the hash" wording vs the documented canon deviation; `std::fill` without `<algorithm>` (compiles via transitive includes); UnknownTier branch, degenerate spawn, BundleTier untested; "every 20 ticks" comment vs `+= 10` loop; U-E2 guard can't see the gitignored `DefaultInput.ini` it names (and is Config/-only vs its "tracked tree" comment); `delivered` and `score` both emit `State.Score`; `LastEditError` written never read (no rejection UI despite the comment's promise); unused `GetCommandBus()`/`GetAccumulatedSeconds()`/`bOnEdge`; shadow 12%-comment vs 0.14-code; topology-change detection by counts only (no Gen in snapshot); "appears THIS frame" is really ≤ 50 ms (next tick); new dots glide in from the canvas corner for a few frames; PPProbe hardcodes `save_magic`/`save_version` literals; routing dump mixes slot and id label spaces; `GetMousePosition` return ignored; `FlowSeedDemand` unvalidated ids; BlueprintCallable NaN-cast edge; **advisory test gate: CONCERNS** (spine coverage strong; gaps concentrate in the new view/bus surfaces).

### Reviewer agreement
Highest-confidence multi-lens sets: StateHash fail-open (6 lenses), StepScenario 16-cap (7), camera-fit duplication/never-re-fit (5), fixture hand-copy vs UAD-17 (4), input-bind null actions (2, engine-source verified), same-tick re-step (3), EqualCostHops staleness (3).

**Verdict:** NEEDS CHANGES

The spine is in excellent shape — determinism, gates, golden discipline, and plugin provenance all verified first-hand and clean. The two blockers are view-layer truth problems: a dead mouse-input path masked by bridge-driven evidence, and an evidence PNG that doesn't contain what the PR, commit, and checklist claim it shows.

_Address findings and push — I re-review automatically on the new sha.
After round 3, the human takes over._
