# Briefing — packet-plumber-local-ci-suite (local container replica of the GH CI gates)

- **Job id:** `packet-plumber-local-ci-suite`
- **Repo:** packet-plumber · **Base:** `v2` @ latest head (Silas resolves the exact sha
  at dispatch) · **Slug:** `local-ci-suite`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model — name it explicitly at every spawn.
- **Skills policy:** `bmad-quick-dev` (implementation); `project-context.md` for code
  conduct. Your own adversarial pass uses `bmad-review-adversarial-general` /
  `bmad-review-edge-case-hunter` layers.
- **Perkins:** `pr_review: 1` — this is the verification gate that will gate everything
  else; it gets one Perkins round before it's trusted infrastructure.
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out
  your field-notes shard per standing orders. On in-review, run
  `ledger pr packet-plumber-local-ci-suite <url>` yourself.
- **CI note:** GitHub Actions is currently BILLING-BLOCKED (account spending limit,
  since 2026-08-16 ~09:13Z) — checks may never start on your PR. That is NOT a code
  problem and NOT a blocker: your own new local suite passing at the PR sha IS the
  ground truth (08-14 doctrine). Do not relay CI-red; note it in the PR body.

## Mission — the GH CI suite, runnable locally (container + native mac), GH untouched

**Context (user ruling 2026-08-16):** the user is hitting GitHub Actions minute/spending
limits. We are NOT changing `.github/workflows/ci.yml` — it stays exactly as-is. We are
ADDING a local replica of its gates so the suite can be run for free: in a Linux
container (the ubuntu leg) and natively on macOS (the macOS leg). "Every other thing
stays the same — we are just adding local container testing."

**The spec is the workflow.** Read `.github/workflows/ci.yml` — every gate, in order,
with the same failure semantics:

1. `tools/lint.sh` (purity + grep gates, ODN-1)
2. `odin test core` (determinism + topology contracts)
3. `odin build app -out:app.bin` (the GPU app compiles + links — link-time X11 deps
   only, never run)
4. `tools/harness.sh run` (golden harness: T1 hashes + T2 software pixels + replay
   gate — software-rendered, no GPU)
5. `tools/harness.sh preview-check` (R2a preview == sim routing)
6. PP_DEBUG compile gate: `odin build app -define:PP_DEBUG=true` AND
   `odin build harness -define:PP_DEBUG=true`
7. `tools/harness.sh stats-check pause` + `tools/harness.sh stats-check qos_contention`

(The only GH-only steps are checkout + artifact upload — the harness already writes
`goldens/_reports/` locally on failure, which is the local equivalent.)

**Deliverables:**

1. **`Dockerfile.ci`** (repo root) — reproduces the ubuntu leg: the pinned Odin release
   (fetch the linux tarball for the tag in `.odin-version`, exactly like the workflow
   does — support BOTH linux/arm64 (Apple Silicon Docker) and linux/amd64), plus the
   X11 link deps from the workflow (`libx11-dev libxcursor-dev libxrandr-dev
   libxinerama-dev libxi-dev libgl1-mesa-dev`). Debian/Ubuntu slim base, your call.
2. **`tools/ci-local.sh`** — one entrypoint:
   - Default: run all 7 gates in the container, same order, stop-on-fail with a clear
     per-gate pass/fail summary (emoji table optional but readable).
   - `--fast`: gates 1–2 only (lint + unit tests — the 10-second loop).
   - `--mac` (or auto-detect when run outside docker with `--native`): the same gates
     run natively on macOS — warn loudly if the local `odin version` doesn't match
     `.odin-version`, then proceed.
   - `--windows-cross`: compile-ONLY gate — `odin build app -target:windows_amd64`.
     EXPERIMENTAL: if the toolchain/vendor:raylib fights it, make the script report
     the failure output and exit 0-with-warning, and document what you found in the
     PR — do NOT force it green.
3. **Docs:** a short section in `README.md` (or `docs/` if a dev-docs home exists —
   follow repo convention): how to run the local suite, what it maps to in GH CI, the
   known-trap notes below.

**Known traps (investigate, don't get bitten):**

- **Build-artifact leakage across platforms.** The harness builds a software-raylib
  shadow (`tools/raylib-sw/shadow` via `build_raylib_sw.sh`) and `bin/` binaries. The
  worktree on a mac already contains MACOS builds of these — mounting it into a linux
  container runs linux against mac artifacts (or vice versa). Solve it deliberately:
  container-local build dirs, a fresh copy/rsync of the tree (excluding `bin/`,
  `tools/raylib-sw/shadow`, `goldens/_reports/`), or documented per-platform output
  dirs — your design, but a second run on either platform MUST NOT be poisoned by the
  first. State the choice in the PR.
- **The goldens must be bit-identical in the container.** They're platform-independent
  by design (software rendering) — if a hash differs in-container, that's a REAL
  finding to report, not to paper over.
- **Docker not running** → the script detects and says so plainly (it's a dev tool,
  not CI — no cryptic socket errors).
- Odin release asset naming differs per OS/arch — the workflow's case block is the
  reference; mirror it for linux/arm64 + amd64.

**Acceptance:**

1. On this Mac: `tools/ci-local.sh` runs all 7 gates green in the container at the PR
   sha; `--fast` works; the native-mac path runs green too.
2. Second consecutive run on the same machine is green (no artifact poisoning).
3. `--windows-cross` attempted; outcome (green or reported-findings) documented in the
   PR body.
4. PR body carries: the gate-mapping table (GH step ↔ local script stage), the
   artifact-isolation design choice, first-run + warm-run timings, and the
   windows-cross result.
5. `.github/workflows/ci.yml` byte-identical to base (prove it in the PR: zero diff).

**Scope guard:** local test tooling ONLY. No GH workflow edits, no gameplay/core/harness
logic changes (if a gate fails at base in the container for a REAL reason, report it —
do not patch the game to fit the container), no canon doc changes beyond the README
section.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: local-ci-suite
base: v2
model: deepseek/deepseek-v4-flash
pr_review: 1
```
