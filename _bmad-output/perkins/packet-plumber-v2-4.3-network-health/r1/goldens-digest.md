# Goldens digest — Perkins mechanical verification (NOT lens output — trust but spot contradictions)

Perkins verified these claims mechanically against the worktree at sha 8659070 (vs merge-base 948996d). Lenses should treat this as verified context and only report something that CONTRADICTS it or that this digest did not check.

## 1. .log.bin re-bless claim — VERIFIED
Claim: every pre-existing .log.bin differs ONLY in the 8 catalog_hash header bytes, same lengths.
Verification: for all 18 pre-existing goldens/*.log.bin files, `cmp -l <parent> <head>` reports exactly 8 differing bytes and equal byte counts:
boot, bundle, demolish, draw, ecmp, ecmp_cost, flow, forecast_preview, forecast_shift, lose, place, qos, qos_contention, qos_emphasis, sla, surge, warn, win — all: 8 bytes, same length. ✓
New: health_lose.log.bin, health_win.log.bin (new files, new goldens).

## 2. .t1 re-bless claim — VERIFIED (catalog_hash fold only)
Claim: existing T1 manifests shifted ONLY via the catalog_hash fold.
Verification: for every pre-existing goldens/*.t1, the ONLY non-tick-hash changed lines are the catalog_hash header line (0a6324230ab9dcba → 1106c1cc8652a91f). Zero semantic/manifest content changed in any pre-existing .t1. Sample (boot.t1):
  -catalog_hash 0a6324230ab9dcba
  +catalog_hash 1106c1cc8652a91f
  plus the full tick-hash chain (every tick hash changed — the hash chain folds the catalog_hash).
surge.t1: 4001 removed / 4001 added lines, ALL of them tick-hash lines. ✓

## 3. T2 PNG claim — VERIFIED
Claim: ZERO old T2 PNGs changed.
Verification: the only PNG files in the diff are NEW files under goldens/health_lose/ (05000ms, 21000ms, 23000ms) and goldens/health_win/ (30000ms, 75000ms, 150500ms). No pre-existing goldens/*/ png is touched. ✓

## 4. New goldens (lens-reviewable content)
- goldens/health_win.t1 — NEW manifest: t1 1, demo health_win, seed 4243, logic_hz 20, catalog_hash 1106c1cc8652a91f, ticks 3040. (Win at tick 3000 → Run_Won; the remaining 40 ticks are post-terminal frozen ticks.)
- goldens/health_lose.t1 — NEW manifest: same header shape, ticks 480 (Run_Lost at tick 452, frozen 453-480). (Run_Lost when the meter empties ~tick 452.)
- The full health_win.t1 / health_lose.t1 diffs are in chunk-C-goldens-new.patch (health_win.t1 trimmed to first 300 + last 550 lines to keep context bounded; the middle is a monotone per-tick hash list — Perkins will verify event-line positions mechanically).

## 5. What Perkins checks mechanically after the lens waves
- health_win.t1: the Run_Won event line lands at tick 3000; post-terminal ticks are byte-identical frozen hashes; ticks count == 3040.
- health_lose.t1: Run_Lost present; post-terminal frozen hashes identical.
- The .dem files' expected outcomes match the manifests.
