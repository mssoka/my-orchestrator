# Briefing — packet-plumber-v2-5.7-runtime-telemetry (stats stream + debug overlay)

- **Job id:** `packet-plumber-v2-5.7-runtime-telemetry`
- **Repo:** packet-plumber · **Base:** `v2` · **Slug:** `v2-5.7-runtime-telemetry`
- **Model policy:** `deepseek/deepseek-v4-flash` (execution role). Any mega-minion you
  spawn launches with the same model.
- **Skills policy:** `bmad-quick-dev` (implementation workflow); your own adversarial pass
  uses `bmad-review-adversarial-general` + `bmad-review-edge-case-hunter`.
- **Perkins:** `pr_review: 1` (canon-surface — the telemetry stream becomes part of the
  determinism contract).
- **Memory:** read `/Users/moses/code/docs/minion-field-notes.md` at start; badge-out your
  field-notes shard per standing orders. On in-review, run `ledger pr <job-id> <url>`.
- **Base:** `v2` — sibling jobs (5.5/5.6/5.3) may merge while you work; rebase onto
  origin/v2 when they do (you share `app/main.odin`).
- **CI NOTE:** GitHub Actions billing is blocked at the account level — your PR's CI will be
  red/not-started until the user fixes it. NOT a code failure. Run the FULL local suite
  green (`odin test`, `harness run`) before opening the PR; Perkins verifies locally.

## Mission — high-fidelity runtime telemetry (user-ordered: he sees links congesting in
play and wants data on what's actually happening — flows, hashing/routing, QoS bugs)

**The principle:** the capture layer ALREADY EXISTS — the deterministic per-tick event
stream (`state.events`, EVENT_TAG_* in `core/types.odin`), the action log, `state_dump`,
and the flow-state counters (delivered/dropped per class, loss%, SLA math in
`core/flow.odin`). This story EXPORTS and SURFACES them — no new capture semantics, no
nondeterminism risk. Everything you emit must be DERIVED from the existing deterministic
state (or the event stream) — never from wall-clock timing or render sampling.

**THIS STORY REALIZES EXISTING CANON — read first:** architecture
`odin-architecture-v1.md` **§7.2 Logging** (levels ERROR/WARN/INFO/DEBUG/TRACE,
structured one-line `[LVL] tick=N system=X msg`, console in dev + rolling file always,
core logging **sink-injected** via a `Logger_Proc` — core never touches stdout), **§7.4
Event system** (ODN-14: tick-tagged events drained by the app once per frame; debug
replay can diff event streams), and **§7.6 Debug / dev tools** (compile-gated
`-define:PP_DEBUG=true`: debug overlay — tick, fps, active packets, SLA per class;
visualization toggles — lane allocation bars, strain heatmap, slow-mo; replay-from-log;
live balance sliders). Your overlay + stream are the scheduled implementation of those
sections — follow their shape where specified.

**Part A — the stats stream (core + harness + app):**
1. Define a deterministic per-tick stats record derived from existing state: per pipe —
   offered demand, carried, dropped by class + Drop_Reason, utilization %; per class —
   demand, delivered, dropped, loss%, avg latency, SLA status; global — tick, gen, sim
   hash, score, meter. (Read `core/flow.odin` — the counters are already there; you are
   shaping them into a record.)
2. `--stats-out <path>` flag: the harness AND the app write the stream. Pick ONE format
   (CSV or JSONL — document your pick + why in the PR body). Deterministic byte output:
   same seed + same commands → identical stream file.
3. **Pin:** a golden/harness test proving the stream is replay-identical (byte-compare
   two runs of the same log) — telemetry joins the determinism contract.

**Part B — the debug overlay (app, key `D` — user ruling: regular letter keys only, NO
F-keys; D is free: R restart, T assist, E/S/B lanes, 1/2 class, U preview, X/DEL
demolish, P/SPACE pause are taken):**
`D` toggles a debug overlay. Compile-gated per arch §7.6 (`-define:PP_DEBUG=true` — dev
builds; document the build flag in the PR body). Content (user-approved list, mapped
onto arch §7.6):
- **Per-pipe readout** (on select): offered demand vs capacity, carried, drops by class +
  reason, lane weights + actual per-lane throughput, latency/queue state.
- **Per-class table:** demand, delivered, dropped, loss%, avg latency, SLA status.
- **Congestion heat:** pipes tinted by utilization % (a threshold ladder — the user
  wants to SEE congesting links at a glance).
- **Global line:** tick, gen, sim hash, score, meter.
- **Live event tail:** last N events (drops, warnings, crises) as a scrolling list —
  human-readable, from the event stream.
Overlay draws ON TOP of the normal HUD, monospace-ish, legible at 12-14px, and MUST NOT
appear in golden captures (gate it: overlay off by default + `PP_DEBUG=false` builds
exclude it — arch §7.6 and the goldens rule at line ~1452; document how the harness
keeps captures clean).

**Acceptance:**

1. `harness run <demo> --stats-out <path>` writes the stream; two runs of the same demo
   produce byte-identical files (pinned by test).
2. The app writes the same stream with the same flag; replay-identical.
3. `D` toggles the overlay live; every element above renders with real numbers (verify
   against a congested demo — pick a demo that saturates a pipe, show the utilization +
   drops).
4. Overlay never shifts goldens (default off; T1/T2 captures unchanged — any shift =
   STOP and flag).
5. Full local suite green.
6. PR body carries the story card 5.7 in
   `_bmad-output/planning-artifacts/sprints/stories-v2.md` + a sample stream excerpt from
   a congested run (the user wants to see the artifact). **UPDATE: the arch §7.6
   cross-ref is ALREADY DONE (commit `5f51236`).** Read the canon at start and
   align — do not re-amend.

**Scope guard:** telemetry only. No gameplay changes, no balance changes, no new
commands (the stream is a VIEW of existing state). The QoS panel job and the pause job
are separate.

## Dispatch parameters

```
repo: packet-plumber
repo_root: /Users/moses/code/packet-plumber
slug: v2-5.7-runtime-telemetry
base: v2
model: deepseek/deepseek-v4-flash
github_issue: (none)
pr_review: 1
```
