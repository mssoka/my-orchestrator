# v2 estate spawning — strict cluster placement for director-spawned terminals

The 08-21 play-session ruling ("not so great looking topology") applied:
director-spawned terminals now form **strict estates** — every growth spawn is
exactly one of two classes, **ATTACH** (within `radius_tiles` of a member of an
eligible cluster — the estate extends) or **SEED** (no eligible cluster → a
fresh area ≥ `new_area_seed_tiles` from every live terminal, still in the
outward-from-mesh annulus). No third class, no strays.

The delta over 5.12 (all in `balance.json` `growth_groups` unless noted):

| knob | before | after |
|---|---|---|
| `bias_prob_permille` (attach fraction) | 750 (0.75 — the 08-17 "NOT 100%" mix) | **1000 (strict — every spawn attach-or-seed)** |
| `max_members` (estate cap) | 8 | **5** (the ruling: "after ~5 nodes a NEW area elsewhere") |
| `new_area_seed_tiles` | — (new) | **10** (2× the adjacency radius — routing room between sections, within the era-3 connect span 18) |
| `min_members` / `radius_tiles` / `member_weight_permille` | 3 / 5 / 250 | unchanged |

Plus two zero-draw rejection predicates in `core/growth.odin` that close the
stray classes the strict audit exposes (draw order/counts per attempt
unchanged — the rng interleaving shifts only through acceptance):

1. **`growth_attach_radius_ok`** — the attach candidate must sit within the
   *Euclidean* radius of its anchor. The 5.12 compass draw's diagonal
   directions placed candidates at up to dist×√2 (5.7–7.1 tiles) from the
   anchor — outside the adjacency radius, inside the seed floor: the exact
   third class the ruling deletes.
2. **Anchor is a LIVE TERMINAL only** — the derived cluster view leaves dead
   slots' `id` at 0, which collides with cluster 0's id (the fixture
   residential at slot 0): a raw id match could anchor an "attach" on a
   ROUTER — another stray source (pre-existing 5.12 defect, invisible to the
   old pins).

## Before / after (measured, same seed 42, same ticks — growth.dem)

Coordinate dumps + rendered captures at `docs/captures/v2-estate-spawning/`
(`before/`, `after/`, `spawn-audit-before.txt`, `spawn-audit-after.txt`).
Honest attribution: the strays are killed by the **two predicates in code**
(the Euclidean attach-radius closure + the live-terminal anchor guard) and the
**seed floor**; the defaults (bias 1000, cap 5) set the regime. The
before/after lens is old **policy** vs new **policy** — identical audit, same
seed, same ticks.

**The strict audit lens applied to both runs** (ATTACH = within 5 tiles of a
then-live terminal; SEED = ≥ 10 tiles from every then-live terminal):

| run | spawns | ATTACH | SEED | **STRAY** |
|---|---|---|---|---|
| before (5.12 policy) | 19 | 12 | 0 | **7 (37%)** — five diagonal-escape attaches at 5.66–7.07 tiles + the coin-miss/uniform draws at 6.4–8.9 tiles |
| after (strict policy) | 13 | 12 | 1 | **0** |

The after map at t1760 reads as three compact 5-member estates (the cap) —
final derived clusters: {res fixture + 4}, {host fixture + 4}, and the seeded
estate at {20,6}…{16,10} — every terminal sits within 5 tiles of a sibling,
every singleton is a fresh seed. The static-start capture (t30) is
byte-identical before/after (no render surface moved).

**Quantified skip rate + capacity note:** the after run spawned on 13 of 21
era-1 windows (8 skipped — the bounded rejection budget exhausted on the
denser map, deterministic by design). The strict policy also reads as fewer,
larger sections per map than the old mix: estates of 5 span ~12–20 tiles and
seeds must clear 10 tiles from every terminal — the intended "distinct
sections" reading. The knobs (`radius_tiles`, `new_area_seed_tiles`,
`terminal_min_sep_tiles`) are the iteration surface if the fun-test wants
denser or sparser sections.

**The one-line cap change, demonstrated** (`max_members: 8` in balance.json,
`spawn-audit-after-cap8.txt`): the same seed run grows estates to **8**
members before seeding a new area — the cap is a data knob, one line.

## Decisions & rationale

- **Strict over emergent (shape (a) of the briefing):** probabilistic strays
  can't satisfy "no lone nodes far from any cluster" deterministically; strict
  attach-or-seed satisfies both acceptance maps by construction and reuses the
  5.12 machinery — the delta is two predicates + defaults.
- **Canon flag, not a rewrite:** the 08-21 acceptance supersedes the 08-17
  "estates, but NOT 100% of the time" doctrine **at the default**. The 08-17
  doctrine is not deleted: `bias_prob_permille < 1000` restores the
  minority-isolate mix as a data option, now seed-distance-respecting. The
  spatial-lane canon (08-12) governs pipe rendering — untouched, no tension.
  Both flags are in the GDD decision-log entry (2026-08-21).
- **Seed distance 10 = 2× the adjacency radius:** visually distinct sections
  on the 40×30 map, inside the era-3 connect span (18) so E31 connectability
  stays satisfiable; the bounded rejection budget keeps it honest on dense
  maps (deterministic skip, no stall).
- **Fail-fast loader (ODN-5):** `new_area_seed_tiles` is a named key —
  missing / ≤ `radius_tiles` / bias 0 or 1001 all reject naming the key; bias
  range widened 1..999 → 1..1000 (0 still invalid).

## Save/action-log compatibility

The `balance.json` knob changes fold into `catalog_hash` (every golden shifts
— the established re-bless precedent): old action logs / saves from earlier
builds **replay-fail under the new hash** — the app and harness refuse
mismatched manifests, by design (ODN-11). Nothing from an earlier build is
loadable into this one; this is the documented cost of a catalog retune.

## Golden re-bless (deliberate, cause-documented)

All 45 demos' T1 manifests + action logs + T2 captures and the input-parity
manifests re-blessed (`harness save` + `harness input-parity save`). Every
shift is caused by (a) the catalog_hash fold (the new knob values + comments)
and (b) the genuine behavioral change (estate spawns — the point of the
story). **`harness fold-check` PASS** (prev `dfe3e342b56679fb` /
`4eaa272171fac065`): boot's tick-1 shift is the catalog fold alone — no
serialization/layout drift. Replay gate: every blessed log re-sims its
manifest bit-for-bit.

## Tests

The acceptance pins re-pinned (updated, never deleted) in `core/growth_test.odin`:
- **`test_groups_estates_strict`** — the parametrized strict attach-or-seed
  audit (the renamed re-pin) on seed 9, at BOTH caps: every spawn is audited
  against its then-live terminal subset with the mechanism-exact class rule
  (eligible cluster existed → ATTACH required; every cluster at the cap →
  SEED required; fresh map → seed), a **mid-run seed** (spawn index > 0 — the
  cap-to-new-area acceptance cannot pass on the forced first spawn alone),
  estates form (≥ min_members), every final-view singleton is a fresh seed,
  E31 + compactness hold. `max_members: 8` (acceptance criterion 3 — the
  one-line change) is a repeatable leg of the same test, not a one-off
  capture.
- **`test_groups_strict_audit_with_fixture`** (new) — the same audit on the
  fixture map (residential at slot 0): pins the dead-slot anchor collision fix.
- **`test_groups_optin_mix_seeds_audit_clean`** (new) — bias 750 (the 08-17
  "NOT 100%" data option): every spawn attach-or-seed, seed-distance-
  respecting, and a coin-miss SEED (seed-class spawn while an eligible cluster
  existed — mechanically impossible at bias 1000) is asserted: the branch
  would regress silently without the pin. Loader positive row: bias 750 loads
  clean.
- **`test_growth_seed_sep_predicate`** + **`test_growth_attach_radius_predicate`**
  (new pure-unit pins, no seed dependence).
- Loader pins: bias 1000 valid (was a rejection), new key rows (missing / at
  radius / below radius / negative) reject naming the key; the shared
  `test_catalog` fixture mirrors the new data.
- Surviving pins adapted: `test_growth_outward_bias_annulus` (the annulus
  bound now holds for both families by construction — E31 keeps ATTACH
  candidates ≥ the 4-tile floor and ≤ span), E31 + determinism + replay pins
  re-verified on the new stream.

Full suite: `tools/ci-local.sh --mac` **10/10 green**.

## How the evidence was produced

- **Before** captures + dumps: the baseline code at `4ccc8c75` (the spec's
  baseline commit, old balance) in a scratch worktree; the growth.dem
  scenario replayed there and the OLD blessed T2 frames extracted from git.
- **After** captures + dumps: this branch's code + balance, same scenario.
- Same seed 42, same ticks (t30/t300/t900/t1760), the same audit lens
  (positions only — ATTACH within 5 of a then-live terminal, SEED ≥ 10 from
  every then-live terminal).
- The coordinate-dump tool was a scratch program, deleted by design after
  producing the dumps — the dumps + captures in `docs/captures/` are the
  durable artifact.

## Out of scope (per the briefing)

Spawn timing (`terminal_spawn_interval_ticks` stays 80), `terminal_min_sep_tiles`
(stays 4 — the E31 packing floor), node-type visual identity, routing
semantics, serialization / LOG_VERSION — all untouched. E31 is the hard
contract throughout; growth spawns TERMINALS only, outward from the
player-placed mesh.

## Fun-test gate

Merge ≠ done: the user plays `odin run app` after merge; the knobs
(`max_members`, `new_area_seed_tiles`, `radius_tiles`) are the expected
iteration surface for the follow-up tuning round (the cap change is one line).

