# Briefing: packet-plumber-lang-safety-research

RESEARCH job — decision-grade, NO-PR. Deliverable = research report +
lavish decision artifact for the user. You investigate and recommend;
the language/engine call is the USER's ruling, not yours.

## The question (verbatim from the user, 2026-08-28)

"Using Rust for Odin dev, or Rust, or just using Godot — Rust because of
the memory safety, to avoid bugs like this that might be hidden and hit
in production? What are Odin's best practices to avoid this?"

Trigger context: the merged #107 (The Box) shipped an invalid-free crash
(`POINTER_BEING_FREED_WAS_NOT_ALLOCATED` from Odin `_heap_free`, hit on
the 3rd spawn connection in the user's playtest; fix in flight as
box-crash-third-spawn). The user is asking whether the LANGUAGE is the
problem.

## Research questions

0. **FALSIFY THE PREMISE FIRST (lead question, user-posed 2026-08-28):
   "or is it a false premise that Rust would have prevented this?"**
   Do not assume Rust/GC would have caught tonight's bug. Once the
   crash heist (box-crash-third-spawn) lands its root cause, take the
   ACTUAL faulty code path and map it rigorously to each option's
   semantics: is the bug (a) unrepresentable in safe Rust / GC'd
   Godot, (b) a deterministic caught panic/error instead of UB,
   (c) still possible (unsafe Rust, custom allocators, C# unsafe,
   GDScript engine bugs)? State WHICH PORTION of the bug space each
   option genuinely closes, with the real code as the test case.
   Also invert it: name bug classes Rust does NOT close (logic,
   leaks-safe-by-design, races in shared-state designs) so the
   comparison is honest.
1. **Rust instead of Odin.** Would Rust's ownership/borrow model have
   prevented THIS bug class (invalid/double free in growable
   collections) at compile time? What does porting cost in THIS repo's
   terms — measure it (LOC by module, render stack dependencies, FFI
   surface, the sim/harness, golden corpus)? What does idiomatic
   gamedev Rust look like today (bevy/wgpu vs the current custom
   renderer) and what are the real risks of a port (scope, timeline,
   gameplay-logic re-verification, perf characteristics for this
   game's workload)?
2. **Godot instead of the current stack.** What Godot buys (managed
   memory, engine tooling, scene system) and what it costs (rewrite,
   GDScript/C# vs native code, determinism for the sim corpus, golden
   harness portability). IMPORTANT HISTORY: a prior engine bake-off
   LOCKED Godot and a lavish verdict REVERSED it to Odin (2026-08 era:
   odin-architecture / forge6 / port-limits followed). The research
   must surface WHY Odin won then and state honestly what changed (or
   hasn't) since — a re-open must argue with that record, not ignore it.
3. **Stay on Odin + harden.** Odin's best practices and tooling for
   memory safety, mapped concretely onto THIS codebase:
   - Allocator discipline: arenas / `temp_allocator` /
     `tracking_allocator` / `assert`-checked allocators; where the
     codebase's manual `free`s live (inventory them) and which could
     move to arena/lifetime patterns.
   - Checked-allocator CI: running the sim corpus + motion strips under
     Odin's debug/checked allocator nightly (the harness already
     replays scenarios headlessly — quantify what % of free-heavy paths
     the corpus exercises today, i.e., the HIDDEN-bug exposure).
   - Odin language roadmap facts (ownership/borrowing plans, if any) —
     cite sources, do not speculate.
   - Code-review pins / conventions that catch this class at PR time
     (Perkins lens additions? a memory-discipline lens?).
4. **The hidden-bug risk, quantified.** Tonight's crash was CAUGHT in
   playtest; how many siblings could lurk? Per option (port / engine /
   harden): what safety net catches them, when, at what cost.
5. **Recommendation.** A decision matrix + a recommended path with a
   PHASED plan (e.g., harden-now-regardless + port-decision criteria:
   what future evidence should trigger a Rust/Godot move vs keep).

## Method

- Web research (Rust gamedev state, Odin allocator/safety practice and
  roadmap, Godot determinism/managed-memory tradeoffs) — CITE SOURCES.
- Codebase grounding: READ-ONLY on the packet-plumber main checkout
  (measure LOC, free-sites inventory, harness coverage) — the report's
  port-cost and hardening numbers must be THIS repo's, not generic.
- Distinguish FACT (measured/cited) from OPINION (labeled) — the lavish
  artifact shows its work.

## Ops

- No-PR job: artifacts to
  `_bmad-output/implementation-artifacts/packet-plumber-lang-safety-research/`;
  report rendered via lavish (loopback-serve if assets 403). On finish:
  `herdr notification show "packet-plumber-lang-safety-research"
  --body "<one-liner>"` (verify shown:true). Ledger transitions are
  Silas'.
- READ-ONLY on the repo. bash 3.2 — no arrays.

## Skills policy

- Primary: `bmad-deep-recon` (technical type, choose-between shape).
- Report render: `lavish`.

## Model policy (USER-ORDERED — exception to the ops-tier default)

- Minion: **zai-coding-cn/glm-5.3** (pro, NOT flash), `--thinking max`.
- Any mega-minion / research fan-out spawns ALSO pin
  zai-coding-cn/glm-5.3 --thinking max — no flash anywhere on this job
  (explicit user instruction 2026-08-28).

## Dispatch parameters

- repo: packet-plumber (read-only grounding)
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-lang-safety-research
- base: v2 (read-only reference; no branch)
- model: zai-coding-cn/glm-5.3 --thinking max
- github_issue: (none)
- pr_review: none — research, no PR
