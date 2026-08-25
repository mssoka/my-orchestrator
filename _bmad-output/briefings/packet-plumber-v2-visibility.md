# Briefing — packet-plumber-v2-visibility (make invisible chokepoints visible — the user-ordered visibility job)

- **Job id:** `packet-plumber-v2-visibility`
- **Repo:** packet-plumber · **Base:** `v2` @ post-#53/#54 merge head (Silas resolves the
  exact sha at dispatch; journal base pull recorded @ e7fa548) · **Slug:** `v2-visibility`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial
  pass uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (gameplay-surface rendering + GDD canon amendment).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-visibility <url>` yourself.
- **Source artifact (READ FIRST):** `/Users/moses/code/_bmad-output/implementation-artifacts/surge-explainer/surge-explainer.html`
  — the lavish explainer from the user's surge screenshot: Section A (the machine),
  Section B (the levers that relieve each state — mechanics, with numbers), **Section C
  (the five invisible design gaps — confirmed in code, one line each)**. Section D1/D2
  (font + resize) already shipped in #52 — out of scope here.
- **CI:** green. Full local suite must pass.

## Mission — the design tenet, made visible

**The user ruling (2026-08-14, canon):** "If players need a manual to play, that's a
design failure" — the game must be legible IN the game. The user's own confusion in
the surge run (packets vanishing with no visible cause; unexplained rings) is
**evidence of real visibility debt, not user error**. This job spends that debt:
telegraph-in-game, not docs-out-of-game.

The explainer's Section C names the five gaps, each confirmed in code:

| # | Gap | What's missing | Code ref |
|---|---|---|---|
| 1 | **Pool exhaustion** (E22 pool) | Global pool cap + map-wide shedding have NO HUD surface — the only symptom is the cascade of spawn drops + the SLA gauges | `core/flow.odin:476` |
| 2 | **Drop sites** | Drops are recorded per tick (class, reason, bundle) for the crisis engine but never rendered — no marker where the shed happened | `core/flow.odin:146-152` (Drop_Site scratch) |
| 3 | **Queue depth** | The 6-packet lane bound has no depth readout — the only telegraph is the 4.1 pipe-pressure halo, which starts at 70% of the bound | `core/warnings.odin:165-182` |
| 4 | **Why-dropped** | SLA gauges show loss% + latency but never WHY (pool vs queue) — the reason tag exists in every drop event, unused by the UI | `core/serialize.odin` (Packet_Dropped payload) |
| 5 | **Node strain cause** | The rings show THAT a node is stuck, not WHAT is stuck (which class, how many packets) | `core/warnings.odin:197` |

**The centerpiece asks (the user's words, via the queue note):** **pool pressure**
(gap 1 — a HUD surface for the pool cap + shedding) and **drop feedback** (gap 2 —
drop-site markers where the shed happened, + gap 4 — the why-dropped reason on the
SLA surface). Gaps 3 and 5 are in-scope too — but **gap 5 is HALF-ANSWERED by story
5.2, which just merged**: per-node 🔴 traceability (utilization numbers on hover) is
the existing surface. Extend it with class/packet detail where cheap; do NOT build a
parallel strain surface.

**Design direction (your call, evidence-backed):** pick the surface(s) that make the
state legible at a glance and validate against the explainer's Section B levers
(what relieves each state — the numbers must line up). Prefer minimal, readable
surfaces over chrome: the HUD shouldn't scream when healthy (the 5.2 quiet-at-green
canon applies to everything you add).

**Hard requirements:**

1. **Determinism discipline (the family spine).** Everything you add is
   **presentation-side** where possible: HUD rendering, markers drawn from existing
   per-tick data (the Drop_Site scratch + Packet_Dropped reason tags already exist —
   read them, don't re-derive or re-record). **No `LOG_VERSION` bump**, T1/replay
   byte-identical `[E10]` — prove it in the PR body (a replayed run shows identical
   visuals implied by identical state; the markers/gauge are derived from state, not
   serialized).
2. **Golden discipline (the font-resize precedent).** T1 must NOT move. Any new HUD
   surface that changes rendered output = a DELIBERATE T2 fold: re-bless + LIST the
   affected goldens in the PR, one line each. No silent golden drift.
3. **Terminology canon (the audit verdicts — Phase 2 rename PR is IN FLIGHT on the
   terminology-audit pane).** New HUD strings MUST use the renamed networking terms:
   **drop precedence** (NOT "drop ladder"), **congestion / utilization** (NOT
   "pressure / strain"), and **lane stays "lane" on the player HUD** (the Q1 split:
   sim/queue surfaces rename to class queue, player HUD + core identifiers keep
   lane). Cite the canon lines in the PR. The rename PR may merge mid-flight →
   rebase guard armed (conflict sensor watches); merge `origin/v2` clean if flagged.
4. **GDD canon amendment (section-additive, the traffic-model M6 precedent):** land
   the visibility canon line in the GDD decision-log —
   `_bmad-output/planning-artifacts/gdds/gdd-packet-plumber-2026-08-05/decision-log.md`
   (+ gdd.md touch only if a section needs it): legibility in-game is a design
   requirement; invisible chokepoints are defects, not mysteries; every loss state
   the player can hit must be readable without a manual.

**Acceptance:**

1. Pool-pressure surface + drop feedback (markers + why-dropped reason) live and
   legible at a glance; queue depth + node-strain-cause addressed or explicitly
   deferred in the PR with the reason.
2. T1 byte-identical; deliberate T2 fold listed; full local suite green.
3. PR body carries: which gaps shipped vs deferred + why, the surfaces chosen +
   the Section B numbers they validate against, the no-LOG_VERSION proof, the
   terminology citations, the canon amendment.
4. GDD decision-log amendment in the same PR.

**Scope guard:** visibility ONLY. No balance changes, no mechanic changes, no new
command kinds, no serialization changes. The explainer's Section B design threads
(narrow-as-access, caps, groups) are the traffic-model story cards 5.9–5.12 —
OUT of scope, they ride their own slots post-5.4.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-visibility
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
