# Story 6.1 — Era definition (Email→Streaming data + the era FSM advance)

The first slice of the era layer (GDD § M4, arch §6.6 — the reserved `[LATER]`
seam, now live): era data loads from an `eras.json` catalog, and the S6 Era
FSM advances the active era. When an advance fires, the new era's unlocks load
(streaming becomes available; the demand signature switches) — catalog data
integer-only + fail-fast validated `[ODN-5]`, and no mid-crisis demand spawn
`[E14]`. Story 6.1 is the DATA + the ADVANCE MECHANIC only: the advance
CONDITIONS (sustain SLA + modernized legacy + no crisis) are story 6.2's scope;
legacy decay/modernize is 6.3 — both named as follow-ups, not built.

## What shipped

### `data/eras.json` — the era table (new catalog)

One row per era: `era` (strict int), `id`/`display_name`, **`packet_types`**
(the ACTIVE class roster — the unlock table whose flip *is* "streaming becomes
available"), **`demand_era`** (the demand.json era row carrying the era's demand
signature — the demand CONTENT stays single-source in demand.json per ODN-5;
this cross-ref binds the era to it), and **`infrastructure.{node_types,
pipe_tiers}`** (the unlock table). MVP rows: eras 1–3 (the content the current
catalogs carry); eras 4–6 arrive with their packet/node/tier content (E5.4 /
6.3 territory — follow-up).

```json
{ "era": 3, "id": "streaming_surge", "display_name": "The Streaming Surge",
  "packet_types": ["email", "streaming"], "demand_era": 3,
  "infrastructure": { "node_types": ["residential", "router_basic", "small_biz",
    "content_host", "campus", "router_mid", "router_high"],
    "pipe_tiers": ["narrow", "standard", "wide"] } }
```

**Fail-fast validation at load** (the `[ODN-5]` pattern from packet_types /
pipe_tiers; `core/catalog.odin`, `eras` block): every id cross-ref resolves to
its catalog (unknown packet/node/tier = load error); `demand_era` must exist in
demand.json; all sim fields strict integers (a decimal rejects); and **two
invariants** keep the new table and the existing per-item era gates from ever
drifting:

1. **Exact-equality vs `era_introduced`** — the roster + unlock tables must
   EXACTLY equal the per-item `era_introduced <= era` sets (a premature listing
   OR a missing unlock is a content bug the load rejects).
2. **Demand ⊆ roster** — every demand entry class of the era's demand row must
   be in the era's roster (demand never spawns a class the era hasn't
   unlocked — the fail-fast half of the unlock switch).

`eras.json` folds into `catalog_hash` (sim-relevant, like demand/crises) — the
re-bless below is the deliberate catalog-fold re-bless the field notes name.

### The S6 Era FSM (`core/era.odin`, new)

- **`Cmd_Era_Advance { to_era }`** — a **logged action-log command** (like
  draw/demolish): the harness/app record it at its apply_tick; the replay
  re-applies it from the blessed log — **the advance event is replay-
  deterministic BY CONSTRUCTION (E10)**. Validated at apply: `to_era` in the
  era table AND strictly forward (a stale/backward request is a log divergence
  → `replay_error`, never a silent no-op).
- **`era_step`** — the FSM's per-tick pass, called at the **reserved `[LATER]`
  seam** (arch §4/§6.6: after `health_update`, before `win_lose_eval`; skipped
  once terminal by the E17 barrier). Executes a pending advance when the **E14
  gate** passes (no active crisis — the registry `crisis_evaluate` settles
  above): bumps `state.era`, loads the unlocks (the roster/infra ride the
  catalog; the demand plan switches by construction — the director reads
  `cat.demand.eras[era-1]` every tick), emits the new **`Era_Advanced` event**
  (ODN-14 tag 13, new-era payload), clears the latch. **An active crisis
  DEFERS the advance until it clears** (deterministic — the fire tick is a pure
  function of the replay-deterministic crisis lifecycle) `[E14]`.
- **The 6.2 gate surface**: the advance CONDITIONS compose on this seam —
  6.2 either gates what REQUESTS an advance (condition-eval in `era_step`
  replaces the scripted request as the trigger) or tightens
  `era_advance_blocked`; the request→latch→fire mechanics pinned here never
  change. `era_class_unlocked / era_node_type_unlocked / era_pipe_tier_unlocked`
  are the unlock-table query surface (the app's tray + 6.2's gate compose on
  them).
- **The log header now carries the RUN-SETUP era** (`log_write`'s new
  `header_era` param): a mid-run advance means the header must hold the
  PRE-advance era so the replay re-applies the advance and reproduces the flip
  at the identical tick (the harness passes `demo.era`; the unit tests pass
  `state.era` — unchanged for non-advancing runs).
- **`LOG_VERSION` 4 → 5** — the new command tag (`CMD_TAG_ERA_ADVANCE`, u8(7)),
  per the canon rule: a serialization change bumps the log version, and the
  golden logs re-bless (version-field-only for no-advance demos — byte-verified;
  the advance demo re-blesses the action-log bytes).

### Golden + harness

- **`demos/era_advance.dem`** — the story's named golden: era 2 → advance →
  era 3; the T1 pins the era-advanced state (era byte + the `Era_Advanced`
  event ride the hash); the captures show email-only traffic pre-advance and
  streaming triangles joining post-advance ("the internet evolves — new
  traffic appears"). **T1/replay determinism proven for the advance event**:
  the replay gate re-applies the blessed advance command and reproduces the
  manifest bit-for-bit.
- Demo verb: `at <n>ms advance <era>` (lowered to a logged `Cmd_Era_Advance`;
  the target validates against the era table + the demo's start era at lower
  time — fail loud).
- **The deliberate re-bless**: the eras.json catalog fold shifts `catalog_hash`
  (and every per-tick hash it rides) for all 35 demos; the **fold-check gate
  passes** (boot's tick-1 shift is the catalog fold alone — bytes 33..40,
  mechanically proven); the `.log.bin` re-bless is **header-only** (version
  byte 4→5 + the catalog_hash field; command bytes byte-identical — verified);
  **all T2 pixels byte-identical** (zero `.png` churn — no sim behavior
  change). The input-parity manifests re-blessed the same way (fold-only).

## Tests

- **`core/era_test.odin`** (6 new): the advance fires + the demand signature
  switches (`test_era_advance_fires_and_switches_demand` — era 2→3, streaming
  in the era-3 plan); **the E14 deferral** (`test_era_advance_e14_deferred_by_crisis`
  — a REAL engine crisis on the surge tick; the advance stays locked through
  the active window and fires on the crisis-CLEAR tick); invalid advances
  latch `replay_error`; **replay identity** for both the fired and the
  E14-deferred advance (live vs replay byte-identical hashes).
- **`core/catalog_test.odin`** (20 new fail-fast rows): malformed eras docs,
  unknown refs, demand_era out-of-range/decimal/missing, both invariant
  directions (premature listing + missing unlock/roster), and the demand-⊄-roster
  rejection — plus the `check_ok` positive assertions.
- **GWT trace (stories-v2 6.1)**: Given eras.json + the FSM → the catalog
  load tests + the golden; When an advance fires → Then unlocks load (roster
  query + demand plan + the golden's T1), fail-fast validation (the negative
  rows), no mid-crisis spawn (the E14 test).

## Decisions & rationale

- **Advance-as-logged-command (not run-setup)**: the advance must be replay-
  deterministic; riding the action log makes it so BY CONSTRUCTION (the log IS
  the replay artifact) and gives the LOG_VERSION bump a natural home. 6.2's
  condition-eval replaces the trigger, never the mechanics. (Alternative
  rejected: a run-setup advance schedule would thread a new Demo_Replay field
  through every replay path for no benefit.)
- **E14 = defer, not drop**: an active crisis DEFERS the advance (the latch
  holds; `era_step` re-checks each tick) rather than cancelling it — the
  contract's "defers new demand until it clears" is honored literally, and the
  deferral is a pure function of the deterministic crisis lifecycle.
- **`demand_era` is a binding, not an indirection**: the demand CONTENT stays
  single-source in demand.json (ODN-5); eras.json names the binding + the load
  validates it. An era row with no demand row is a load error, never a silent
  no-demand era.
- **Serialization discipline**: `era_advance_to` is ABSENT-WHEN-0 in the state
  dump (a no-advance run writes zero new bytes — every no-advance golden stays
  fold-only); the `Era_Advanced` event rides the tag-conditional payload (the
  shared `class` field carries the new era, documented); `LOG_VERSION` bumps
  per the canon serialization rule.
- **Architecture doc not amended**: the arch §6.6 `[LATER]` line and the
  demand.json "era-FSM story owns their re-tune" comment remain accurate — the
  re-tune (eras 1/2 balance) is a gameplay story (6.2/6.3 territory), and the
  stories-v2 status line is the live record (the 5.12 pattern).

## Follow-ups (out of scope, named)

- **6.2** — the advance CONDITIONS (sustain SLA ≥ 95% across the milestone
  window + modernized legacy + no crisis `[E15]`): compose on
  `era_advance_blocked` / the request surface above.
- **6.3** — legacy decay + modernize/demolish (`eras.json` gains the legacy
  table).
- **Eras 1/2 demand re-tune** (dormant in the MVP; the app runs era 3 from
  tick 1) + **eras 4–6 content** (packet/node/tier rosters) — full-game scope.
- **App-side advance trigger** (a player-facing advance is 6.2's launchable
  increment; this slice proves the mechanic in the harness/golden).

## Canon fold

- `stories-v2.md` § Story 6.1 → `Status: implemented 2026-08-19` (same-PR
  edit, the 7.4 pattern).

## Verification

- `tools/ci-local.sh --mac` **10/10** (purity gates, 205 core tests, app build,
  golden harness 35/35 + replay gates, palcheck, drift-check, preview-check,
  PP_DEBUG builds, stats-check, input-parity 24/24).
- Fold-check PASS (catalog-fold-only re-bless); T2 pixels byte-identical; log
  re-bless header-only (byte-verified).
