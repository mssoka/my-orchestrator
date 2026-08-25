# Briefing: packet-plumber-v2-harness-ecmp-demo

- **Standing orders:** Read `/Users/moses/code/docs/orchestration-playbook.md` "Minion standing orders" FIRST — applies in full.
- **Repo:** packet-plumber (`/Users/moses/code/packet-plumber`). **Base: `v2`** (slices 1–2 complete). **PR targets `v2`.**
- **Story:** infra mini-story (deferred from 2.2's recommendation) — **close the T2 pixel debt + add demo infrastructure**.
- **Workflow:** **gds-dev-story**. Fresh minion. Perkins: **ON**. Self-review: bmad-review-edge-case-hunter (rlsw bit-exactness, node-spawn determinism, golden blessing discipline).
- **Model:** `deepseek/deepseek-chat` (glm-5.2 capped until 09:00:47Z; deepseek is the interim fleet provider — LIVE-verified).
- **bmad-quirk heads-up:** verify every edit lands in YOUR worktree (`git status` from cwd); commit/push/PR from the worktree only.

## Mission

Three coupled infra pieces that unblock frame-level verification + richer demos:

1. **Complete the `rlsw` software-renderer harness build** (`tools/build_raylib_sw.sh`) — raylib 6.0 built with the **rlsw software renderer + PLATFORM_MEMORY** backend (architecture §10.4): bit-exact pixels on every machine, **no GPU, no display**. This is the key that lets `tools/harness.sh run` produce real T2 pixel diffs instead of the structural/hash-only verification slices 2.1–2.3 have been deferring.
2. **Add a `node-spawn` demo directive** to the `.dem` format — currently demos can `draw`/`spawn` packets but **nodes come only from the hardcoded 3-node fixture**. A `spawn_node` (or equivalent) directive lets demos build arbitrary topologies (diamonds, grids) deterministically.
3. **`ecmp.dem` + T2 retro-verify** — add a diamond-topology demo exercising 2.2's ECMP spread (needs node-spawn), AND re-run the deferred T2 pixel goldens for **2.1 (bundle), 2.2 (ECMP), 2.3 (demolish)** now that the rlsw harness works — bless the matching frames or fix + re-bless.

## The work
- **rlsw build:** get `tools/build_raylib_sw.sh` producing a working software-renderer raylib that `harness/` links. macOS target. The build is C/Make-flavored (raylib source + platform flags) — expect build-system wrangling; the goal is `tools/harness.sh run <demo>` emitting T2 pixel diffs (`goldens/_reports/<demo>/diff.png` on mismatch). `tools/raylib-sw/` has a partial prior attempt to build on.
- **node-spawn directive:** extend `harness/demo.odin`'s parser with a `spawn_node` verb (deterministic: node id, type, position — same seed → same topology). Keep the existing `draw`/`spawn`(packet) verbs intact.
- **`ecmp.dem`:** a diamond (source → 2 equal-cost mid-routers → sink); packets ECMP-spread via the 2.2 hash; `capture` the split frame; T1 (per-packet paths in hash) + T2 (the split).
- **T2 retro-verify:** run `tools/harness.sh run` for bundle/flow/draw/win/lose + the new ecmp + 2.3's demolish demo; bless matching T2 goldens (`tools/harness.sh save`, PR-reviewed); report any real pixel drift as findings (don't silently re-bless a mismatch).

## Carry-forwards
- **2.1 / 2.2 / 2.3** — their T2 pixel goldens were deferred ("needs rlsw harness"). This story builds the harness + closes that debt.
- **The `.dem` format** (`harness/demo.odin`) + the harness runner (`harness/`, `tools/harness.sh`).
- **2.2's ECMP** — `ecmp.dem` is its first harness-level regression coverage (currently ECMP is unit-test-only).

## Mandates (load-bearing)
- **rlsw bit-exactness** — the software renderer MUST be deterministic across machines (PLATFORM_MEMORY, no GPU variance). A Perkins lens-guard confirms the harness output is reproducible, not environment-dependent.
- **node-spawn determinism** — same seed → same spawned topology (no RNG drift, no map-iter in the spawn path).
- **Golden blessing discipline** — `tools/harness.sh save` is deliberate + PR-reviewed; a pixel mismatch is INVESTIGATED (real drift → finding) not silently re-blessed.
- **No engine types in `package core`** (ODN-1); the rlsw build + harness are tooling/app-side.
- **Don't regress existing demos** — bundle/flow/draw/win/lose T1 still hash-stable; their T2 either matches (bless) or drifts (finding).

## Source material (read)
1. **`_bmad-output/planning-artifacts/architecture/odin-architecture-v1.md`** — §10.4 (rlsw software renderer + PLATFORM_MEMORY), §11.7 (headless-test contract), the T1/T2 golden contract.
2. **`tools/build_raylib_sw.sh`** (the partial build script) + **`tools/harness.sh`** (the runner) + **`harness/demo.odin`** (the .dem parser) + **`harness/run.odin`** / **`harness/drift.odin`**.
3. **`demos/*.dem`** (existing demos — bundle, flow, draw, win, lose) — the directive patterns + capture points to mirror.
4. **README.md** — the "golden-image harness" section (T1/T2 contract, the harness.sh commands).

## Verify
- `tools/build_raylib_sw.sh` produces a working rlsw; `tools/harness.sh run <demo>` emits T2 pixel results (not "deferred").
- `node-spawn` directive parses + is deterministic; existing `draw`/`spawn` verbs unchanged.
- `ecmp.dem` runs: packets ECMP-spread across the diamond; T1 paths + T2 split frame captured.
- T2 retro-verify: 2.1/2.2/2.3 (+ existing) T2 goldens blessed or real drift reported as findings.
- `odin test core` still green (no core regression); core still engine-free.
- After user approval: commit, push, open PR **targeting `v2`**. **Never merge.**

## Self-report (set the pr field: `bin/ledger pr <id> <url>`)
- `bin/ledger set packet-plumber-v2-harness-ecmp-demo working` at start
- `bin/ledger set packet-plumber-v2-harness-ecmp-demo in-review "PR <url>"` + `bin/ledger pr packet-plumber-v2-harness-ecmp-demo <url>`
- `herdr notification show "pp-v2-harness" --body "<one-line>"` on finish
- Final message: the rlsw-build summary, the node-spawn directive, the ecmp.dem, + the T2 retro-verify results (how many goldens blessed vs drift-found).

## Dispatch parameters
- repo: packet-plumber · repo_root: /Users/moses/code/packet-plumber · slug: v2-harness-ecmp-demo · **base: v2**
- model: deepseek/deepseek-chat · pr_review: 1 · github_issue: (none)
- **PR target: v2** · descriptive tab label `pp-v2-harness-ecmp-demo`
