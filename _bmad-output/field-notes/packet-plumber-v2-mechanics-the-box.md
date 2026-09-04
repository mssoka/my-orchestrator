# field notes — packet-plumber-v2-mechanics-the-box

- 2026-08-28: Odin `case:` in a `#partial switch` swallows EVERYTHING after it — a case inserted
  below the default silently never runs (a demolish refund priced zero and the tests still mostly
  passed). Keep special cases ABOVE the default; a grep for `case:` adjacency belongs in review.
- 2026-08-28: any charge/refund priced from POST-apply topology is a hazard class: pipe_slot/
  node_slot SKIP DEAD entities and fall back to slot 0 — tombstone-then-price refunds the wrong
  tier/span (or nothing). Pattern that works: validate snapshots the pre-edit facts into a small
  struct, charge prices from the snapshot. A test demolishing pipe id 0 MASKS the bug (slot 0 is
  the accidental right answer) — always demolish a non-zero id in refund tests.
- 2026-08-28: T2 pixel goldens + palcheck are ENVIRONMENT-BOUND on this machine: the pristine base
  (03dd6f8) re-blessed locally reproduces palcheck 61-fail exactly (committed base goldens: 32) and
  `save juice` on base ≠ committed juice. T1 (sim hashes) is stable. Before chasing a palcheck/T2
  regression, re-bless the BASE in a scratch worktree and compare — if base reproduces, it's the
  render environment, not your diff; disclose and let the human/CI decide the golden source of truth.
- 2026-08-28: `.gitignore`'s `_bmad/` does NOT match the worktree bootstrap SYMLINK (trailing slash
  matches directories only) — `git add -A` stages the symlink; the repo .gitignore now carries a
  bare `_bmad` line too.
- 2026-08-28: harness `stats-check <demo>` writes its streams under `bin/` — a fresh worktree has
  no `bin/` dir and fails "cannot read live stream: Not_Exist"; `mkdir -p bin` first.
- 2026-08-28: a fail-fast TEST TABLE can be entirely VACUOUS while green: a per-file reject helper that omits ONE catalog source makes the loader die in an EARLIER file, and the helper's "wrong file" branch returns without ever checking the rule — every row passes forever. Audit rejection helpers by MUTATING one expectation to nonsense: if the suite stays green, the table is dead. Fixing the helper then exposed ~40 stale expectations (rows written against the key NAME, the loader rejects with the MESSAGE substring) — fix each against the REAL rule and re-run.
- 2026-08-28: rejection-rule needles are brittle in three ways: (1) `replace1`'s 4th arg is a COUNT, not an occurrence index; (2) after retuning a fixture value, old needles stop matching and their rows silently no-op (verify each row still fails-for-the-right-reason); (3) loader messages carry EM-DASHES — a hyphen in the want substring fails the contains() check. Copy want-strings from the loader source, never from memory.
- 2026-08-28: `Catalog_Sources` field alignment differs per helper (eras needs fewer padding spaces) — a python needle with copied alignment silently no-ops across helpers. When a patch "applies" but grep finds no trace, the needle matched a DIFFERENT helper's block; verify by grepping for the inserted comment.
- 2026-08-28: NEVER edit data/*.json comments (or any catalog byte) after a golden re-bless — catalog_hash folds and every .t1 manifest + parity manifest goes stale (a full save + input-parity save needed AGAIN). Settle all data edits FIRST, then bless once, then freeze.
- 2026-08-28: two machines blessing the same corpus with different R/B raster conventions splits the corpus (Perkins census: 116/117 swapped vs 1 warm) — after ANY cross-machine merge, re-bless the ENTIRE corpus from ONE machine and run the full T2 loop twice consecutively before trusting it.
- 2026-08-28 (THE BIG ONE): **NEVER bless T2 goldens with `odin run harness` directly.** The direct build links the standard vendor:raylib (GPU/Metal headless) whose readback is R/B-SWAPPED (BGRA) — the frames render, the T2 compare is self-consistent, the suite goes green, and NOTHING looks wrong until a blob-level census finds every frame carrying the swapped convention. The sanctioned pipeline is `tools/harness.sh` (builds the rlsw software-raylib shadow via ODIN_ROOT swap — warm-correct RGBA, bit-exact per ODN-17). Symptoms of the wrong-backend trap: palcheck raster legs fail with 0 px of EVERY canon hex; "stale" goldens that re-bless to byte-identical wrong frames; a black frame where #106's is warm. The fold-check/T1 gates stay valid (sim hashes are render-independent) — which is exactly why the trap is invisible to the T1-only sweep. ALWAYS bless + verify T2 via tools/harness.sh.
- 2026-08-28: PNG pixel-diffs in a pinched shell: hand-rolling a PNG de-filter in python works (Paeth etc.) but the channel-stride must match the actual color type (ch=4 RGBA vs 3 RGB) — a step-3 walk over an RGBA buffer misaligns channels and fabricates phantom diffs. Use PIL when available; pin the tool.
