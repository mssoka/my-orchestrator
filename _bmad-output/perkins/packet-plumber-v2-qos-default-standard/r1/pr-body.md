## Summary

User ruling 2026-08-19 (verbatim): *"in networking when no queue is configured, all traffic should be on the standard queue and would take 100% of the capacity. And that should be the auto. Everything on standard and 100% until we start implementing QoS."*

A pipe with **no player QoS configuration now carries ALL traffic on the Standard lane at 100% of capacity**. Express and Best-effort hold nothing until the player assigns a type to them. The auto-ladder engages only from the player's first type→lane assignment (1 in-play lane = 100% · 2 = 70/30 · 3 = 50/30/20, from `balance.json` `lane_auto_reserve_ladder` — no hardcoded splits).

## Divergence root cause

This is CANON restated (GDD M2: "all traffic starts on Standard and the player actively engineers QoS" + the 08-14 ladder "1 class queue used = 100%"), not a new decision — the **5.8 implementation drifted**:

- `apply_draw` appended `lane_presets[default_preset_idx].weights` — the **balanced `[1,1,1]` preset (≈33/33/33)** — as every new pipe's resting weights.
- `qos_pipe_weights` and `qos_auto_weights` returned the same balanced preset for unconfigured pipes.
- The drift was **documented as canon** in the 5.8 `balance.json` comment ("untouched pipes keep the default preset, not the ladder"), which is what made it look intentional.

The fix makes the unconfigured state the **ladder's 1-lane row** (`lane_auto_reserve_ladder[0] = [100]` → Standard 100%) at every read site, data-driven (ODN-5).

## Changes

**Core (`core/`)**
- `qos.odin` — new `qos_unconfigured_weights(cat)` (single data-driven source for the resting default); `qos_auto_weights` drops the `!assigned` balanced early-return (untouched pipes flow through the ladder path: in-play = exactly `{Standard}` → row `[100]`); the never-drop fold now engages only once the player has ≥1 assignment (an untouched pipe is exactly `{Standard}` = 100% — a never-drop class defaulting off Standard there is backstopped by the E6 flow floor); `qos_pipe_weights` fallback + `qos_pipe_caps` E5 fallback use the helper; new `qos_auto_weights_after` (the ladder result with a candidate override folded in).
- `topology.odin` — `apply_draw` writes `qos_unconfigured_weights`; `validate_set_lane` E6 guard checks the **settled** weights (the auto-follow result for auto pipes, the manual set otherwise), so a never-drop class's FIRST assignment can engage the ladder (the auto-follow it triggers reserves the lane) while manual zeroing edits are still rejected.
- `serialize.odin` — the absent-when-empty default (`def_w`) is the unconfigured default; default pipes still serialize ZERO QoS bytes (sparse contract intact).
- `catalog.odin` / `data/balance.json` — comments corrected (the 5.8 "untouched pipes keep the default preset" clause was the documented bug; the 08-19 ruling supersedes it).

**Tests (`core/*_test.odin`)** — pins moved from balanced `{1,1,1}` to `{0,100,0}`; new AC tests:
- `test_qos_unconfigured_default_100pct_standard` — fresh pipe, zero assignments → full capacity (15/15) to Standard, nothing held for unused lanes; lone Standard packet crosses in 2 on-edge ticks (full-capacity flow).
- `test_qos_first_assignment_engages_ladder` — first assignment flips the pipe to the ladder rung (70/30, then 50/30/20); removing all assignments returns to `{0,100,0}`.
- `test_qos_unconfigured_never_drop_untouched` — an untouched pipe is exactly `{0,100,0}` even with a never-drop class defaulting off Standard; the E6 flow floor backstops it (Express floored to 1).
- `test_qos_unconfigured_survives_tier_change` — a tier change reallocates the NEW capacity entirely to Standard (no silent re-split).
- Lane-only fixtures (`lane_pipe_setup`, `test_congested_run`, the crisis construction) now mirror the app's auto-follow weights (the ladder result the app writes after categorizing); `sla_weights` helper added. Stats/crisis shape pins re-pinned to the new allocation (the aggregation mechanism itself is unchanged — one aggregated row, no per-event duplicates).

**App (`app/`)** — comment accuracy only (`qos_mode_manual`'s AUTO derivation still holds: untouched = weights == auto == the 100% Standard default).

**Demos (`demos/`)** — `sla`, `qos_contention`, `audio_throttle` gained the app-mirroring auto-follow weights so their scenarios keep their intent; "default balanced" capture comments updated to "100% Standard".

**Harness** — `palcheck`'s zoomed lane-stripe oracle sets explicit Express weights on the wide pipe (a default pipe no longer shows an Express stripe).

## Golden re-bless — deliberate + cause-documented

The fix legitimately changes pinned behavior (the unconfigured allocation), so goldens were deliberately re-blessed (`harness save`):

- **32 demos fold-only:** the `.log.bin` differs from the pre-bless golden in EXACTLY the 8 `catalog_hash` bytes (byte-verified per file; `balance.json`'s corrected comment folds into the catalog hash). `harness fold-check 5f86ef16ca1c0ece 0e1e1afe9129ff2f` **PASSES** — boot's tick-1 shift is mechanically proven to be the catalog fold alone. Identical commands + unchanged catalog values ⇒ identical sim behavior for these demos.
- **3 demos behavioral by design:** `audio_throttle`, `sla`, `qos_contention` gained the auto-follow `Cmd_Set_Weights` entries (intent-preserving, see above).
- **T2 captures re-render** every default pipe as a single 100% Standard band (previously 3 equal bands) — verified the diffs are confined to the lane-band regions of pipes. `input_parity` manifests re-blessed (fold-only).

## Decisions & rationale

- **"1 used = 100%" counts in-play lanes (Standard always in-play).** Standard is the default home of every un-categorized type (08-12 canon) and is always reserved (08-14 ruling) — so the ladder's rung 1 (`[100]`) IS the zero-assignment state. This matches the GDD's own ladder wording ("1 class queue used = 100%").
- **Never-drop fold gated on `assigned`.** An untouched pipe is exactly `{Standard}` = 100% per the 08-19 ruling ("until we start implementing QoS"). MVP data is unaffected (all defaults pinned to Standard); the E6 flow floor remains the backstop for the hypothetical future never-drop non-Standard default.
- **E6 guard semantics.** The guard now checks the pipe's SETTLED weights (the auto-follow result for auto pipes). This is what lets the first assignment of a never-drop class engage the ladder — the auto-follow it triggers reserves the lane by construction (every in-play lane gets a positive share), so no never-drop class can ever sit on a zeroed lane via the auto path.
- **Demos write auto weights.** The harness demos previously categorized lanes without the weights the app auto-writes (a stale lane-only shortcut). With the new default, lane-only categorized pipes would sit at 0% for their assigned lanes (E7 floors only) — so the demos now write the app-mirroring ladder result to preserve their stated intent.

## Verification

- `tools/ci-local.sh --mac` — **10/10 gates green** (lint, unit tests, app build, golden harness + replay, palcheck, drift-rejection, assist preview, PP_DEBUG builds, stats replay-identity, input parity).
- `harness fold-check` — mechanical fold-only proof for the re-bless.
- `python3` JSON validation + `odin test core` 209/209 green.

