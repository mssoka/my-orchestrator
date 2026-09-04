# Packet Plumber: Language/Engine Safety — Odin vs Rust vs Godot
**Decision-grade research · 2026-08-28 · job packet-plumber-lang-safety-research**

> **⚖️ USER RULING (lavish session, 2026-08-28, in-artifact): "A — stay on Odin + harden (P0-P3 as proposed)"** · Phase-2 CI leg: **nightly windowed on the mac runner** ("simplest, catches the class now"). Session c5a278e1f7b8eff1, ended by user after queueing both answers. The language call is settled: NO port; P1 refinements + P2 nightly app-driver leg are the follow-up work.

- **Decision (USER's ruling):** stay on Odin + harden, port the game to Rust, or move to Godot — triggered by tonight's playtest crash on merged #107.
- **Lead question (user, verbatim):** "Rust because of the memory safety, to avoid bugs like this that might be hidden and hit in production? … or is it a false premise that Rust would have prevented this?"
- Epistemics: FACT = measured on this repo @ v2 3960644 or cited [n] (source table at the end). OPINION = labeled. The full evidence chain lives in `research/digests/D1–D6`.

---

## 0. Executive summary

1. **The premise is NOT false — Rust would have prevented tonight's specific bug at compile time** (the shallow-copy-then-destroy pattern does not compile in safe Rust [R1]). So would Godot's refcounting for script-level state [G1]. That part of the premise survives scrutiny cleanly. **Confirmed twice over:** the landed fix PR #108 (r1 APPROVED, review 5055486548) root-caused the identical mechanism — an owned-vs-borrowed aliasing bug enabled by Odin's allocator-in-the-slice-header design: the value copy carried the LIVE heap allocator inside the aliased headers, which is exactly why the first destroy freed *silently through the correct allocator* instead of erroring — the very feature that guards against cross-allocator frees is what let an aliased free succeed. In Rust the type system owns this boundary; there is no header to copy.
2. **But the bug is root-caused, tiny, and structurally killable in Odin.** Measured this run: `shadow_clone` (the spawn-telegraph predictor's state clone) missed the 2 new Box arrays #107 added; `run_destroy(shadow)` freed the LIVE run's Box buffers; a later telegraph re-predict freed the dangling pointer → SIGABRT. RED→GREEN proven under lldb: a 2-line clone fix → 8 scripted spawn connections, clean exit (digest D1). It is the **3rd instance of one known pattern** in the same proc — the proc's own comments predicted it.
3. **The false step would be "preventable in Rust ⇒ port."** The port costs ~58k LOC (app/render = rewrite, not rebind), the golden corpus + determinism spine (the reason Odin won the 2026-08 bake-off), and iteration speed (Bevy's own docs treat compile time as a standing tax [R3][R4]) — to close a bug family that Odin's own tooling (`Tracking_Allocator` [O1]) plus a structural test closes deterministically for about a day of work.
4. **The real finding is a coverage gap, not a language gap:** every safety net (13 CI gates, 5 Perkins rounds, 22.7k test LOC) is aimed at the SIM; the faulting path is APP-only (harness grep: 0 calls to `spawn_fx_predict`). ~5.7k LOC of app-layer effects run only under the user's cursor. The scripted app-driver built for this research proves that gap is closeable in CI.
5. **Recommendation (OPINION, argued in §5):** Stay on Odin; ship the 2-line fix (in flight); harden the class structurally (exhaustive clone test + tracking-allocator CI + arena-shadow refactor + an app-layer e2e leg); set explicit written criteria for what future evidence would justify a Rust (or Godot) move. The bake-off record stands — tonight's evidence argues with it honestly and loses on the pillars, wins only on an axis it never weighed (§3).

---

## 1. What actually happened tonight (FACT — root-caused this run)

```
SIGABRT ← libmalloc POINTER_BEING_FREED_WAS_NOT_ALLOCATED ← Odin _heap_free
  ← delete_dynamic_array ← box_destroy (box.odin:44)
  ← run_destroy (types.odin:621)
  ← spawn_fx_predict (spawn_fx.odin:303)   ← main.odin:882, every frame
```

- Reproduced faithfully from a scripted real-input playtest (repo untouched; /tmp copy @ the merged HEAD); crash report byte-signature identical to the user's two `.ips`. Full stack captured under lldb (digest D1).
- **Mechanism:** #107 added `Box_State{pieces, spools}` to `Run_State` and enabled the Box at run start. `shadow_clone` deep-clones 55 of the state tree's ~57 dynamic fields — not the Box's 2. The shadow's struct-copy carried the LIVE run's array headers (Odin dynamic arrays store data-ptr + allocator in the header), so `run_destroy(&shadow)` freed the live run's Box storage — silently. The app then ran on dangling pointers (the Box HUD reads them every frame), until a later telegraph re-predict (every connection bumps topology.gen) freed the dangling pointer again → abort. User hit it on connect 3, repro on connect 1: the class is deterministic, the detonation rides heap-reuse variance.
- **Proof:** +2 `clone_dyn` lines in `shadow_clone` → same scripted playtest connects 8 spawn buildings (mutation-gate standard ≥5), clean exit. RED→GREEN.
- **It is a recurring class, on the record:** the same proc's comments document instances #1 (tx ring, v2-network-units) and #2 (residency ledger, v2-arch-egress S5 — "the spawn_feel heap-abort"). Tonight is #3. Same shape every time: new dynamic field on `Run_State`, clone list not updated. No structural guard existed; each instance was caught by crash, not by test.
- **The fix has LANDED as PR #108** (open, r1 APPROVED — review 5055486548; user-held merge): the same 2-line clone root cause found independently there, PLUS a per-tick `batch` scratch LEAK sibling fixed in the same PR, PLUS two new gates (the 57-array alias pin test + a 5-spawn-window playtest leg), mutation-verified RED→GREEN by Perkins USING the tracked allocator. The class sweep at that sha: 55 deletes vs 53 clones + 2 by-design zeroed — the family is closed and now test-guarded. (Full fold-in: digests/D1 addendum.)
- **Why nothing caught it (FACT, two complementary legs):** (a) the harness never calls `spawn_fx_predict` (grep: 0 refs in harness/) — the predictor, input effects, HUD-string paths and audio feed are app-only surface; (b) per #108's review: every existing `shadow_clone` fixture ran box-OFF — zero-value Box headers are nil, `delete` no-ops, so the aliasing was invisible to every test that DID touch the proc. The 13 CI gates + `box on` demo exercise the sim (clean); all 5 Perkins rounds on #107 reviewed economy/serialization semantics — the miss is a cross-file lifetime invariant (types.odin × spawn_fx.odin × main wiring) no lens was briefed to check.

**Bug-space taxonomy (FACT):** tonight's bug is a *stale-alias lifetime bug* (manual clone-list discipline), single-threaded, allocator-correct. It is NOT raw-pointer misuse (the repo has zero raw frees), NOT a Box-economy logic bug, NOT a determinism failure (replay/T1 held throughout).

---

## 2. Falsify the premise — rigorously, per option (the lead question)

### 2.1 Would Rust have prevented THIS bug? — **YES, at compile time.** [R1]

The bug's shape is literally the textbook example: two values sharing one heap buffer, both dropped → double free. In safe Rust, `let shadow = state;` MOVES ownership (the original is invalidated; using it is error E0382), and there is no way to "destroy the copy" while the original lives without `unsafe` or a hand-written `Clone` that aliases — both visible in review. The shadow-clone design compiles into exactly two safe shapes (real deep clone, or borrow) and neither can express tonight's bug.

**What Rust does NOT close (the honest inversion):**
- Logic bugs (spool arithmetic, era caps, routing) — identical exposure; tonight's Box logic was clean but the next logic bug ships equally on both languages.
- Determinism discipline — Rust's type system does not order map iteration or pin float behavior; the repo's integer-only/array-only rules stay CONVENTION in Rust too. The determinism spine would be rebuilt by the same discipline, not inherited from the language.
- Leaks (safe Rust leaks happily; Rc cycles leak) — same exposure as Odin.
- The predict-by-cloning DESIGN itself — fine in Rust, just forced to pay the real deep-clone cost the Odin bug accidentally skipped.
- `unsafe` renderer interop / custom allocators / FFI — the moment the port wraps wgpu or raylib C, a narrower hole re-opens (bounded, reviewable, but real).

**Net (FACT-based):** Rust closes the *memory-corruption* portion of the bug space at compile time — including tonight's — and closes data races (irrelevant today, relevant if multithreading ever lands). It closes neither logic bugs, nor determinism hazards, nor leaks.

### 2.2 Would GC'd Godot have prevented it? — **YES, for script-level state.** [G1]

`RefCounted` objects are released when unreferenced; a script cannot perform the invalid free. The residual bug families Godot DOES have: refcount cycles that leak (documented), orphaned nodes (the classic Godot leak), stale shallow `duplicate()` reads (logic bug, not corruption), dangling signals — plus C++-level engine bugs outside your control, and C#'s GC delays if that route is taken. So the corruption class closes; a softer stale-data class remains.

### 2.3 Would "Odin + best practices" have prevented it? — **Not at write time; YES at CI time, deterministically.** [O1]

Odin has no compile-time ownership (by design, on the record [O2]) — the clone-list bug compiles. But `core:mem`'s `Tracking_Allocator` fires a `bad_free_callback` with the **source location** on the FIRST free of a pointer the allocator doesn't own — i.e., tonight's bug aborts at `spawn_fx.odin:303` in a CI leg with file:line, before any user sees it, no heap-reuse lottery. **PROVEN, not proposed:** the landed #108's Perkins mutation leg used exactly this — removing the fix lines produced tracked-allocator bad-frees at `box.odin:44-45` across a 5-window scripted leg, deterministically. Add the (now-landed) 57-array alias-pin test and the class is structurally dead (§5). FACT: the tooling existed all along, un-used.

### 2.4 Verdict on the premise

**The premise survives: Rust/GC genuinely prevent tonight's class.** The decision-relevant correction is different: prevention is also purchasable in Odin for ~a day of work — so the question is not "which language prevents this" (all three can, eventually) but "what does each option cost to reach the same protection, and what does it put at risk" (§4).

---

## 3. The bake-off record — argued with, honestly (briefing Q2)

FACTS from the record (PRs #13/#15/#16 + the durable analysis doc):

- Godot was LOCKED; PR #13 was a devil's-advocate steelman of Odin. The steelman's 4 pillars: determinism native vs fought in GDScript; server re-sim trivial vs aspirational (m6); data-oriented sim, not scene graph; "you don't need what Godot sells." The pivot enabler was the user's LLM-coding reframe.
- The doc's own final re-weighting TILTED BACK TO GODOT for the near-term launch ("Godot is the pragmatic launch tool; Odin is the architectural option to revisit") — and the USER overrode: "let's move to Odin. Let's own it end to end."
- The pivot then DELIVERED its promises (verified on disk): the determinism spine is real (owned PCG32, integer-only, T1 hash + 50 demos + 148 goldens + drift gate, all green tonight), and the sim held perfectly under tonight's crash.

**What tonight adds to that record (FACT):** one under-weighted axis — memory-safety discipline in the app layer — surfaced exactly where neither the bake-off nor the harness looked. The cost of "own it end to end" is now measurable: 232 manual delete sites, a 57-field state tree cloned by a hand-maintained list, 3 instances of the same lifetime class, and an app layer (~5.7k LOC of input/predictor/HUD/audio effects) with no automated coverage — policed, until tonight, solely by playtest.

**Does that re-open the bake-off? (OPINION):** No — a re-open must claim a pillar failed (determinism/sim fitness: it didn't), the LLM-coding reframe inverted (an LLM wrote the bug and 5 review rounds missed it — a real dent, but the same LLM ecosystem root-caused it in ~2h with the toolchain), or the goal moved (it hasn't: desktop Steam-first per FORGE #6). What tonight DOES justify is spending on the under-weighted axis: hardening + app-layer coverage — which is exactly §5's plan.

---

## 4. Decision matrix

Hard gates (fail = cut): (a) replay corpus re-provable, (b) shipped-game behavior not gratuitously reset, (c) fix for tonight's class ships THIS WEEK regardless of option. All three options pass (a) in principle; B/C risk (b) heavily; only A trivially satisfies (c).

Weights (OPINION — re-weight to taste; the matrix is the deliverable, not the totals):

| Criterion (weight) | A. Odin + harden | B. Port to Rust (bevy/wgpu) | C. Move to Godot 4.7 |
|---|---|---|---|
| Closes tonight's class (15) | ✅ CI-time, deterministic [O1] | ✅✅ compile-time [R1] | ✅ runtime model [G1] |
| Memory-corruption bugs in general (15) | ⚠️ tracking-allocator net at CI, not write-time | ✅✅ safe-Rust default shapes | ✅ script-level; engine C++ outside control |
| Determinism spine survives (20) | ✅✅ inherited, proven | ⚠️ portable by discipline; must RE-PROVE 50 demos + re-bless 148 goldens on a new renderer | ❌ fought (bake-off pillar 1, m6) — spine rebuilt on faith |
| Cost/time to equal protection (15) | ✅✅ ~days (guards + CI leg, §5) | ❌ ~58k LOC: sim ports 1:1, app/render REWRITES (92 rl procs, 8.85k render LOC); corpus event | ❌ full rewrite; corpus does not transfer |
| New-bug risk DURING the move (10) | ✅ none (additive) | ❌ high: ports historically inject exactly the class being fled (OPINION) | ❌ high, same |
| Iteration loop speed (10) | ✅✅ seconds-scale builds, golden loop intact | ⚠️ Bevy compile time is a documented standing tax [R3][R4] | ✅ editor loop (the bake-off's Godot edge) |
| Agent/LLM ergonomics (10) | ⚠️ Odin = rarer language for models (OPINION; mitigated by repo canon + harness readability) | ✅✅ best-known language | ✅ well-known + editor tooling |
| Ecosystem/5-yr regret (5) | ✅ Odin 1.0 Jan 2027 (spec + compat) [O3]; small community | ✅✅ huge ecosystem; Bevy still pre-1.0 cadence [R2] | ✅✅ mature engine, 4.7 stable [G1] |
| **Weighted feel (not a score — see caveat)** | **wins on gates 3-5** | **wins only if safety weight ≫ all** | **wins only if goal moves (editor/mobile/shipping-first)** |

Cut in screening (record, per selection method): D) Hybrid Odin-core + Rust-app — double FFI surface, two toolchains, splits the state-tree invariant across a boundary: strictly worse than A or B on every axis except hedging (OPINION).

---

## 5. Recommendation + phased plan (OPINION, evidence-cited)

**Recommended: A — stay on Odin, harden the class, close the app-layer gap. Write down the port triggers.**

Rationale in one breath: tonight's class is preventable in Odin deterministically and cheaply (§2.3); the port spends the project's crown jewel (determinism spine, proven tonight of all nights) and re-opens the exact bug class during the migration; and the evidence that would justify B/C (a hardening-proof-resistant memory-safety pattern, or a goal change) is definable in advance — so write it down and re-decide on evidence, not on the adrenaline of a crash night.

**Phase 0 — DONE (landed as PR #108, r1 APPROVED, user-held merge):** the 2-line `shadow_clone` Box clone + the `batch` leak sibling, with two new gates beyond what this plan proposed: the 57-array alias-pin test (`test_spawn_fx_shadow_clone_box_owns_every_array` — the Phase-1 exhaustiveness guard, landed) and a 5-spawn-window playtest leg with the box verbs. Mutation-verified RED→GREEN by Perkins via the tracked allocator.

**Phase 1 — remaining refinements (days):**
1. Harden the landed alias gate (Perkins r1 W1): the fixture skips len==0 pins — 15/57 are vacuous (health 9, era_gate 5, lane 1); enable health + advance gate + a lane command in the fixture, or fail-loud on vacuous pins.
2. Refactor `spawn_fx_predict`'s shadow onto a scratch ARENA + `free_all` — the per-array destroy path (the bug's habitat) disappears; core:mem's documented idiom for frame-scope temporaries [O1]. (Perkins r1's architecture finding agrees: move the clone/mirror toward core or make the invariant core-owned.)
3. Debug/CI builds run the sim corpus + the new predict legs under the tracking allocator nightly (bad free ⇒ abort with file:line — deterministic; #108's mutation run is the working recipe).

**Phase 2 — app-layer CI leg (the actual gap):** productize the scripted app driver (place routers, wait for growth windows, connect spawns, exercise predictor/HUD/audio feeds) as a nightly leg; today it is the only net that would have caught tonight's bug pre-merge. (My prototype runs windowed on macOS; the harness's rlsw software-renderer path is the headless vehicle to evaluate.)

**Phase 3 — conventions:** PR-checklist pin ("new `[dynamic]` on Run_State ⇒ update 4 lists: shadow_clone / serialize / run_destroy / the round-trip test"); a Perkins memory-discipline lens addition (diff-grep for Run_State dynamic-field additions ⇒ flag the clone list).

**Port-decision criteria (write these on the row; re-open only on evidence):**
- A 2nd memory-corruption class reaches the user AFTER Phase 1-3 land (i.e., hardening demonstrably insufficient), or
- the project adds threaded/concurrent gameplay (Rust's Send/Sync becomes load-bearing), or
- the goal moves to mobile/editor-first shipping (Godot's bake-off edges become decisive), or
- Bevy reaches 1.0/stable-renderer-API AND the Odin toolchain regresses (e.g., 1.0 slips badly) — combined, not either alone.

---

## 6. Hidden-bug risk, quantified (briefing Q4)

- **The class census (FACT, post-#108):** 3 corruption incidents ever, all `shadow_clone`, all the same shape — now swept (55 deletes vs 53 clones + 2 by-design zeroed, asserted in the landed test) and test-guarded; PLUS 1 leak sibling (per-tick `batch` scratch, fixed in #108) surfaced by the new leg — evidence the predictor surface had exactly one more hidden bug of the softer class. The 232 delete sites are not uniform risk — the sim's frees are defer-scoped and harness-covered; all incidents lived in the app layer's cross-struct lifetimes. Phase 1's remaining refinements close the vacuous-pin gap Perkins flagged.
- **Coverage census (FACT):** sim + render-golden surface ≈ 49k LOC under CI; app-effects surface ≈ 5.7k LOC with zero automated coverage; predictor + input effects + HUD strings + audio feed = tonight's exact habitat. Phase 2 is the net for that 5.7k.
- **Per option:** A catches siblings at CI (tracking allocator + round-trip + app leg) — after Phase 1-2, a residual sibling needs to be OUTSIDE the state-clone family AND outside the scripted app path. B/C prevent corruption-shaped siblings by construction but import migration-shaped new bugs during the rewrite (uncapped, OPINION).

## 7. Open questions

1. Can the scripted app driver run fully headless under rlsw (no window) on CI? (Prototype is windowed; rlsw is proven for render goldens — needs a 1-day spike.)
2. Does Odin's `Tracking_Allocator` overhead fit the nightly corpus budget? (Docs don't state overhead; measure on the 50-demo corpus.)
3. Bevy's render-graph maturity for THIS game's 2D canvas style (bezier pipes, glow telegraphs) — only matters if a port trigger fires; don't spend now [R2].

## 8. Sources

| # | Claim it supports | Publisher | Pub | Accessed | Conf |
|---|---|---|---|---|---|
| [R1] | Move semantics; double-free unrepresentable (E0382) | [Rust Book ch.4](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html) | current | 2026-08-28 | high |
| [R2] | Bevy 0.19 (2026-06-19), 0.19.1 (2026-08-12); ECS data-driven; pre-1.0 cadence | [bevy.org/news](https://bevy.org/news/bevy-0-19/) + [crates.io/bevy](https://crates.io/crates/bevy) | 2026-06/08 | 2026-08-28 | high |
| [R3] | Rust/Bevy compile time = documented standing tax | [Bevy book: fast compiles](https://github.com/bevyengine/bevy-website/blob/main/content/learn/book/development-practices/fast-compiles.md) | current | 2026-08-28 | high |
| [R4] | Rendering ≈75% of Bevy compile time | [bevyengine/bevy#23642](https://github.com/bevyengine/bevy/issues/23642) | 2026-04 | 2026-08-28 | high |
| [R5] | 3-yr Bevy production-readiness retrospective | [jms55: Bevy's Fifth Birthday](https://jms55.github.io/posts/2025-09-03-bevy-fifth-birthday/) | 2025-09 | 2026-08-28 | medium |
| [O1] | Tracking_Allocator + bad_free_callback(Source_Code_Location); arena idiom; "ownership model not strict" | [core:mem docs](https://pkg.odin-lang.org/core/mem/) | current | 2026-08-28 | high |
| [O2] | Odin rejects ownership/borrow; handles+generations recommended | [gingerBill: Fatal Flaw of Ownership Semantics](https://www.gingerbill.org/article/2020/06/21/the-ownership-semantics-flaw/) | 2020-06 | 2026-08-28 | high (primary opinion) |
| [O3] | Odin 1.0 "Odin 2027": RC Dec 2026, 1.0 Jan 2027; spec + backward compat; manual memory stays | [SourceFeed: Odin sets 1.0](https://sourcefeed.dev/a/odin-sets-its-10-release-for-january-2027) | 2026-07 | 2026-08-28 | medium-high |
| [G1] | RefCounted auto-release; cycle leaks; C# GC delay; Godot 4.7 stable | [Godot docs: RefCounted](https://docs.godotengine.org/en/stable/classes/class_refcounted.html) | 4.7 current | 2026-08-28 | high |
| [D1-D3] | Crash root cause, measurements, bake-off record | this repo @ v2 3960644 (lldb stack, wc/grep, PRs #13/#15/#16) | 2026-08-28 | 2026-08-28 | measured |

*Staleness: version claims (R2, G1, O3) age fastest — re-check before acting if >1 quarter passes. The repo measurements are pinned to v2 3960644.*
