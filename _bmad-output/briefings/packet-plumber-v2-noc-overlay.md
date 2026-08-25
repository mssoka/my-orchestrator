# packet-plumber-v2-noc-overlay

## Task

Dev-mode debug overlay — a "NOC-style dashboard" (user directive
2026-08-22: "would be nice to get a dev option, for debug, to see
where/why packets are dropping — what's happening on a NOC-style
dashboard overlay"). The user is losing games to drops at last-mile
links despite fat pipes + top-tier routers; the sim KNOWS every drop
reason (enums exist) but the player can't see it.

## Scope (what the overlay shows)

1. **Drop counter by reason enum** — live totals per drop class:
   E9 lane-bound shed (lowest-priority lane, per bundle/lane),
   E22 pool exhaustion (map-wide), Saturated_Bundle, Router_Ports_Full
   (canon #14), any other drop paths in core. Which reason dominates =
   the diagnosis.
2. **Per-bundle/lane queue depth vs the E9 bound** (balance
   lane_queue_packets = 6) — a live bar that turns red at the bound.
3. **Global pool utilization vs E22 cap** (pool_max_packets = 512).
4. **Per-pipe utilization vs capacity** (pipe tiers: narrow 10 /
   standard 15 / wide 40 u/s; transit = ceil(packet_bandwidth /
   capacity_units)) — highlight pipes at/over 100%.
5. **Last-N drop log** — tick stamp + bundle/lane/terminal id + reason
   + class, scrollable (a NOC alarm feed).
6. **Per-class drop breakdown** — which traffic classes shed most
   (surge/campus/email...), live rates.

## Rules (hard)

1. **ZERO determinism impact.** Read-only over the sim: no mutation of
   sim state, no new randomness, no timing changes. T1/T2/replay must
   stay byte-identical with the overlay ON (it's view + diagnostics
   only). If any probe needs state the sim doesn't expose, add a
   zero-payload diagnostic read, never a sim-side change. The 44/47
   golden re-bless classes stay untouched — overlay renders only under
   the dev flag.
2. **Dev-gated.** Hidden in normal play (a dev flag / key toggle, e.g.
   F- or D-key, or --dev launch). The fun-test gate stays clean;
   normal runs byte-identical.
3. Reuse existing drop-reason enums (core/types.odin: Saturated_Bundle,
   Pool_Exhaustion, Router_Ports_Full + the E9/E22 shed paths) — expose
   the sim's own classifications, don't duplicate logic.
4. Follow the view-layer conventions: hud_test.odin / motion_test.odin
   patterns; @(test) gates where practical (a small test asserting the
   overlay renders without touching sim state is welcome).
5. NO aesthetic ceremony — this is a dev tool; keep the engine's
   current style. Vision/aesthetic verdicts deferred (rate-limited).

## Acceptance

- Overlay toggle works in dev mode; normal runs show nothing new.
- Live numbers shown match the sim's own state at a tick boundary
  (spot-checked against a debug dump or test).
- T1/T2/replay byte-identical with the overlay active (prove in PR
  body: streams hash-equal with overlay on vs off).
- Drop-reason taxonomy maps 1:1 to the code's enums (a finding if a
  drop path is unclassified).
- PR body includes a screenshot of the overlay mid-game (mechanical
  capture; vision verdict not required).
- pr_review: 1.

## Skills policy

bmad-quick-dev.

## Model policy

deepseek-v4-flash, --thinking max. No vision model needed.

## Dispatch parameters

- repo: packet-plumber
- repo_root: /Users/moses/code/packet-plumber
- slug: packet-plumber-v2-noc-overlay
- base: v2 (fresh head at dispatch)
- model: deepseek-v4-flash
- worktree: yes
- pr_review: 1
- parallel-safe: view-layer + dev flag only; no goldens, no sim
  files (rebase-on-demand if a sibling merge lands first)
