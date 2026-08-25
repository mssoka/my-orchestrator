# Briefing — packet-plumber-v2-5.9-demand-caps (story 5.9 — per-terminal demand caps)

- **Job id:** `packet-plumber-v2-5.9-demand-caps`
- **Repo:** packet-plumber · **Base:** `v2` @ 18781a4 (post-#60/#61 head; Silas
  resolves the exact sha at dispatch) · **Slug:** `v2-5.9-demand-caps`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion
  you spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `gds-dev-story` (story execution) — the story card below IS the
  spec; `project-context.md` for code conduct. Your own adversarial pass uses
  `gds-code-review` layers (blind hunter + edge-case hunter).
- **Perkins:** `pr_review: 1` (core flow / packet semantics — canon surface).
  **Loop ruling (user, 2026-08-17, "keep going"):** rounds run UNTIL APPROVED.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start;
  badge-out your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-v2-5.9-demand-caps <url>` yourself.
- **Story card:** `_bmad-output/planning-artifacts/sprints/stories-v2.md` §Story 5.9
  (relative to `/Users/moses/code/packet-plumber`). Read it + the DESIGN SPEC
  `_bmad-output/implementation-artifacts/spec-traffic-model.md` (the Section B
  threads, user ruling 2026-08-15) BEFORE designing. The card's pinned acceptances
  (W9/W10/W7/W6/N9) are load-bearing — they were written from prior Perkins rounds;
  treat them as contracts, not guidance.
- **Lane note (sibling in flight):** 7.1-visual-juice runs concurrently in the VIEW
  lane (k3, lavish-gated style probe → implementation). Your lane is CORE flow +
  catalogs + tests — disjoint files. ONE interaction: your spawn-stream shift may
  shift T2 pixel frames in scripted scenarios, and 7.1 is re-blessing T2 goldens
  for juice. If you land first: note the T2 impact in your PR body for 7.1's
  rebase. If you land second: your T1 re-bless must land on the juiced frames per
  the 4.3 discipline.
- **CI:** GitHub Actions is org-billing-blocked (+ a live GitHub incident today —
  git ops fine); the LOCAL suite is ground truth. `tools/ci-local.sh` (9 gates)
  must pass; keep it green.

## Mission — implement story 5.9 (per-terminal demand caps: endpoints never self-congest)

**The goal:** the demand director bounds each terminal's spawn RATE via a
per-terminal **spawn accumulator in integer milli-packet units** — throughput-
relative and uniform (`accrue_milli = cap_fraction_permille × throughput_units ÷
packet_bandwidth`, proposed `cap_fraction_permille = 500`). Endpoints never
self-congest; spawn drops become aggregation drops — congestion lives at the
shared uplink the player builds, per the honest-traffic doctrine.

**Hard requirements (all pinned by the card):**

1. **The accumulator, exactly where the card says:** `spawn_credit_milli[terminal_slot]`
   in `Flow_State` beside `lane_caps` — updated IN PLACE, derived, NEVER serialized
   (the `lane_caps` precedent); integer-only (ODN-10, `jint_strict`); accrue
   `cap_fraction_permille × throughput ÷ packet_bandwidth` milli/tick; spawn costs
   1000; pickable while `credit_milli >= 1000`; `MAX_CREDIT_MILLI = 1000 × max(1,
   ceil(cap))` type-relative.
2. **Credit-gated eligibility.** Over-cap terminals are ineligible for source
   picks (eligible set = credit-gated subset; ONE rng draw per pick preserved
   `[ODN-10]`); the volume lands on other terminals. Director §1b spawn pass ONLY
   — the legacy §1a `flow_seed_demand` fixture path is exempt (N9).
3. **The SLA invariant holds.** A credit-gated skip is NOT a demand event (never
   reaches `sla_count_demand`); a pool-dropped arrival IS;
   `demand_seen == delivered + dropped + live` (E24) holds under both paths
   (pin at `sla_test.odin:88`).
4. **Quantitative acceptances (the card's W9/W10/W7):** post-cap surge-lands on a
   known seed (≥ expected × 0.95, spawns ≤ cap × window + burst, credit ≤
   MAX_CREDIT); one-subscriber-at-cap zero-drop at its own access + transit ≤ class
   tolerance; `core/demand_test.odin` + `core/flow_test.odin` +
   `core/determinism_test.odin` RE-PINNED with positive (cap honored) + negative
   (no unbounded burst) assertions — not just a golden re-bless. The era-3 demand
   profile + 5.1 growth pacing + surge multiplier are re-validated TOGETHER —
   silent surge non-landing is a fail.
5. **Goldens per the 4.3 discipline:** T1 spawn-sequence shift is a DELIBERATE,
   cause-documented re-bless (byte-verify `.log.bin` differs only where the cap
   causes it; document the cause chain in the PR); existing goldens otherwise
   unshifted; replay byte-identical `[E10]`.

**Acceptance:**

1. Card's Given/When/Then + every pinned acceptance verified and named in the PR.
2. Full local suite green (`tools/ci-local.sh` 9/9); determinism pinned.
3. PR body carries: the accumulator design (home, math, integer invariants), the
   E24 proof, the W9/W10 numbers, the re-bless cause chain, the surge-revalidation
   evidence, citations `[ODN-3]` `[ODN-5]` `[ODN-10]` `[E10]` `[E24]` + the spec.
4. Story card status line updated in the same PR (the established pattern).

**Scope guard:** source-side demand caps ONLY. No sink-side admit accumulator (W6:
documented balance-time option), no catalog rebalance beyond the cap fraction
(5.10's narrow-access resize is the NEXT card — do not fold it in), no balance
changes beyond what the surge-revalidation requires, no UI. Sink concentration
stays as-is (weighted-random dst + E9).

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.9-demand-caps
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
