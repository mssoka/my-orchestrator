# Story 6.3 — Upgrade lifecycle (legacy decay + modernize)

Implements stories-v2 §Story 6.3 / GDD M4 (E5.3) — the upgrade lifecycle: **pipes become legacy in later eras; effective throughput decays; modernize (tier up) or demolish.** The 6.2 advance gate's legacy predicate — the documented seam — is now RESOLVED: it is the definition the gate and the lifecycle share, and the decay is REAL sim behavior (the routing/drop ladders serve reduced effective capacity — never a view-only illusion).

- **CI: `tools/ci-local.sh` 10/10** (native macOS; lint gates incl. palcheck green).
- **Golden proof:** the eras.json fold (the decay factor) is the ONLY shift for every era-0/1 demo: `harness fold-check` PASS (boot's tick-1 = old hash with the old catalog_hash spliced at bytes 33..40), all 45 `.log.bin` files differ from HEAD only in the version field (5→6) + the catalog-hash header bytes (verified byte-position-wise), and every era-0/1 T2 is byte-identical. The era-≥2 goldens re-blessed for the decay's traffic-density shift (the 42 changed T2 frames are all era-≥2 demos; vision-verified on advance_fire: the queued stack at the decayed bottleneck, scene structure unchanged). The new `legacy_decay.dem` + `legacy_modernized.dem` pair is the story's golden: identical seed/topology/demand, one run modernizing at the fire — the T1 contrast IS the measurability contract.

## The legacy-decay model

- **The predicate (the 6.2 seam, resolved):** a pipe is legacy iff its tier < the current era's newest unlocked tier (`era_pipe_is_legacy` — unchanged from 6.2; it is now THE shared definition). Gate and lifecycle agree **by construction** — the cross-test (`test_legacy_gate_lifecycle_agreement`) pins the agreement wherever the decay factor is active (eras ≥ 2) and pins the one documented split (era 1: the gate's modernization bar names below-newest pipes while the foundation era's factor 1000 decays nothing — neglect them and era 2's factor bites).
- **The factor:** `data/eras.json` gains `legacy_decay_permille` per era — integer 1..1000, **fail-fast validated** at load (missing/decimal/out-of-range rejects; [ODN-5]). Era 1: 1000 (no decay — nothing predates it); eras 2–3: 500. The factor is a per-era tuning knob (the era that governs defines how harshly the pipes it left behind decay).
- **The authority:** `pipe_effective_capacity(cat, era, tier)` — the single capacity read every consumer folds through: raw tier capacity × the era's factor ÷ 1000 (integer, floored — ODN-10) when the pipe is legacy. Both derived capacity views read it: `bundles_rebuild` (pooled bundle caps — a legacy member contributes its DECAYED share, so a mixed bundle's pool reflects the decay) and `qos_pipe_caps` (per-pipe lane allocation). Both are derived (never serialized) → replay recomputes identically → **no per-pipe legacy state rides the T1 hash**.
- **The era flip engages decay:** `era_step`'s fire rebuilds the derived capacity views (bundles + lane caps — the flip is not a topology mutation, so the gen trigger alone would leave them stale); the NEXT tick serves at the decayed rates. Deterministic — replay re-runs the identical flip + rebuild.

## Modernize (the tier-up) and demolish

- **`Cmd_Set_Pipe_Tier{pipe, tier}`** — a LOGGED command (replay-determinate; `CMD_TAG_SET_PIPE_TIER` = 8, **LOG_VERSION 5→6**). Validated: pipe live (`.Missing_Pipe`), tier in catalog range (`.Unknown_Tier`), **strictly upward** (`.Not_An_Upgrade` — a downgrade would silently re-legacy a modernized pipe; same-tier is a no-op the bus rejects). Apply: set the tier + bump gen (rule 1 — routing costs (the capacity-cost ladder), bundle caps and lane caps all rebuild at the next step). The legacy state clears **by construction** (the predicate reads the tier). Demo language: `at <n>ms modernize <pipe> <tier>` (group order after demolishes).
- **Demolish (2.3)** restores by construction — a demolished legacy pipe leaves the pooled bundle at the modern members' full capacity (`test_demolish_clears_legacy`).

## Why draw-era tracking was NOT the model

The 6.2 seam's speculative "real model" (per-pipe draw era) was evaluated and rejected: (a) GDD M1 names narrow the **"baseline legacy" tier** — legacy is a TIER property, not a draw-era one (a narrow drawn in the current era is still the era's oldest technology); (b) the 6.2 gate + its blessed golden `advance_block_legacy.dem` (a narrow stub drawn in era 2 blocks the era-2 gate) pin the tier-based predicate — draw-era flags would have silently un-blocked it, rewriting shipped canon; (c) the briefing's own cross-test (gate + lifecycle agree) is satisfied BY CONSTRUCTION with one shared predicate — two state sources (flags + predicate) could drift. The story's scope guard ("decay + modernize ONLY") keeps the model minimal.

## The 6.2 gate cross-test

The gate's blocking set is the decayed set: `test_legacy_gate_lifecycle_agreement` pins (a) per (era, tier): gate-legacy == decayed wherever the factor is active, (b) on a live mixed topology: the gate blocks on the legacy narrow, and the modernize flips BOTH the gate and the decay in one move. The 6.2 goldens survive: `advance_block_legacy.dem` stays byte-identical modulo the fold (the stub carries no traffic); `advance_fire.dem` re-blesses with the decay engaged post-fire (its standard pipes are legacy in era 3 — the story's "decayed" state).

## Tests (9 new durable contracts, `core/legacy_test.odin`)

Predicate + decay math (era boundaries, integer math) · the derived views fold the decay (lane caps + pooled bundle) · the era flip engages decay (15 → 7 u/s across the fire) · modernize validate/apply · modernize replay identity · the log wire round-trip · demolish clears legacy · the gate↔lifecycle cross-test · **decayed vs modernized throughput** (the story's GWT: identical topology + demand at era 3, one run modernized — the decayed run sheds, the modernized delivers all 20).

The 6.3 era-3 decay re-staged the rate-sensitive test fixtures (era-3 narrows/standards are legacy now): the crisis engine tests pin their MECHANICS on the honest legacy shape (the shared narrow fixture — GDD M5 degradation) with the attribution stages re-pinned; the stats test pins the decay IN the stats surface (standard cap 15 → 7); the W10/W11 access contracts re-pin on WIDE (the era-3 modern access — a decayed access self-congests, which is the honest 6.3 consequence); E16's drain-rate contract re-tuned its grace values (the decayed access sheds email early — the E16 contract is the drain RATE, never the grace values).

## Decisions & rationale

- **Legacy = tier < the era's newest, with a per-era decay factor** (not per-pipe draw-era flags) — see "Why draw-era tracking was NOT the model". The factor lives in eras.json (the briefing's "eras.json or a sibling catalog" — [ODN-5], fail-fast).
- **The decay folds the DERIVED capacity views** (bundles + lane caps) instead of serialized per-pipe state — keeps every no-advance golden byte-valid (modulo the catalog fold) and replay-identical by construction.
- **The era flip rebuilds the views at the fire** — the flip is not a topology mutation; without the rebuild the next tick would serve at pre-decay rates (the golden would still be deterministic, but the decay would lag — the story says decay engages on the advance).
- **`Not_An_Upgrade` is a typed rejection** — the modernize command is strictly upward; downgrades are demolish-and-redraw territory (2.3).
- **Era 1's factor is 1000** (the foundation era leaves nothing behind) while its gate bar still names below-newest pipes — the documented split (the modernization requirement vs the decay consequence); pinned explicitly in the cross-test.
- **Metaphor boundary [GDD §M4]:** nothing here forces Era 6 abstraction — decay, modernize and demolish are all literal plumbing. No Era 6 content invented.
- **Scope guard honored:** decay + modernize ONLY, this era transition; no multi-era ladders beyond eras.json; no view work beyond the existing canon surfaces (the app's QoS-panel + paused-twin call sites updated for the new capacity signature only).

## Citations

- GDD §M4 (era progression + infrastructure lifecycle), GDD M1 (the tier table — narrow = "baseline legacy"), GDD M5 (the degradation crisis on left-behind pipes).
- stories-v2 §Story 6.3 (the card this implements) + §Story 6.2 (the gate's seam) + §Story 6.1 (the era FSM + infra table).
- The landed 6.1 PR (eras.json era table) + 6.2 PR (the advance gate + legacy predicate seam).
- `docs/` arch §6.6 (the S6 seam), ODN-5 (catalog fail-fast), ODN-10 (integer-only), ODN-14 (events), the 4-rule spine (derived views).

**Decisions & rationale** (this section) is the takeover handoff: a fresh minion can resume review rounds cold.

