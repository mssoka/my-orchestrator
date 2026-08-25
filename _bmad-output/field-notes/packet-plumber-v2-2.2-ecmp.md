# packet-plumber-v2-2.2-ecmp — field-note shard

- 2026-08-11 (self): the absolute-path trap bit AGAIN (reinforces the
  2026-08-11 field note). cwd was the worktree, but my `write`/`edit` calls
  used absolute paths to `/Users/moses/code/packet-plumber/...` (the MAIN
  checkout) — picked up from reading source material — so all 3 edits landed
  in the main checkout, worktree clean. `odin test`/`lint`/`harness` all
  `cd`'d to the main checkout too, so they passed against the WRONG tree.
  FIX: resolve every edit to the WORKTREE path (cwd-relative or
  `~/.herdr/worktrees/<repo>/<slug>/...`); after edits, `git status` from
  cwd BEFORE trusting a green test run. Recovery: cp the files into the
  worktree, cmp-verify, revert the main checkout, re-run gates in the
  worktree.
- 2026-08-11 (self): the rlsw software-renderer harness ALREADY EXISTS and
  works (2.1 blessed pixel goldens; `tools/build_raylib_sw.sh` clones raylib
  6.0 + builds `libraylib_sw.a` ~40s). A briefing carry-forward claimed "T2
  pixel-unverified until the rlsw harness exists" — STALE (ground-truth
  first: the goldens/ pixel dirs + the shadow build disproved it). rlsw is
  gitignored, so it's ABSENT in a fresh worktree — point the harness build
  at the main checkout's shadow: `ODIN_ROOT=<main>/tools/raylib-sw/shadow
  odin build harness -out:bin/harness` (compiles the worktree's core/harness
  against the main's pre-built rlsw).
- 2026-08-11 (self): ECMP determinism design that kept ALL goldens valid —
  (a) the routing table is DERIVED (not serialized), so restructuring its
  internal layout (flat single-hop -> packed equal-cost sets) has ZERO T1
  impact; (b) `ecmp_pick % 1 == 0`, so single-path scenarios (count==1)
  produce byte-identical per-packet paths; (c) ECMP only engages at count>=2
  junctions no existing scenario has. Net: purely additive, no re-bless. The
  pure hash reuses `splitmix64` (the same primitive rng.odin uses for seed
  expansion — sanctioned by ODN-9 as the "deterministic finalizer, NOT a
  sim-rng draw"); a naive Perkins grep for `splitmix64` in routing would
  false-positive — the real guard is "no rng_next/rng_range/state.rng in the
  routing path", backed by a behavioral test (flow-run vs no-flow-run rng
  state bit-identical).
